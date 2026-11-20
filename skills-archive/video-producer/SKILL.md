---
name: video-producer
description: >-
  سیستم تولید ویدئوی خودکار — خط تولید کامل «ایده → ویدیوی نهایی». با این اسکیل از یک ایده،
  فیلم‌نامه می‌نویسیم، صحنه‌ها را با AI نقاشی می‌کنیم، روایت صوتی می‌سازیم، زیرنویس فارسی
  می‌سوزانیم، موسیقی آمبیانت سینتز می‌کنیم و با ffmpeg تدوین سینمایی (حرکت Ken Burns،
  کراس‌فید، کارت عنوان، تیتراژ پایانی) انجام می‌دهیم و MP4 نهایی تحویل می‌دهیم.
  هر وقت کاربر گفت «ویدیو بساز»، «فیلم بساز»، «روایت تصویری بساز»، «ویدیوی یوتیوب/اینستاگرام
  درست کن»، «مستند کوتاه بساز»، «ویدیو با هوش مصنوعی»، «همین متن/موضوع رو ویدیو کن» یا
  «video/film/documentary/reel بساز» — از این اسکیل استفاده کن، حتی اگر کلمه «ویدیو»
  صریحاً نیامده باشد ولی خروجی بصری-روایی خواسته شده باشد.
---

# سیستم تولید ویدئوی خودکار (Video Producer)

> الگوی این اسکیل از تحلیل سیستم آلوانا (alvana.me/auto) و فیلم «هزاره‌های خاموش» استخراج
> شده: **هر هوش مصنوعی استاد یک کار؛ کنار هم یک شاهکار.**
> تیم ما: فیلمنامه (خودت/GLM) + نقاشی صحنه‌ها (image-generation) + صدای راوی (TTS انگلیسی)
> + زیرنویس فارسی (libass + Vazirmatn) + موسیقی (سینتز ffmpeg) + موتور تدوین (`assemble.py`).

## معماری خط تولید (۶ فاز)

```
ایده کاربر
   │
   ▼
[۱] SCREENPLAY   → خودت screenplay.json می‌نویسی (قلب سیستم)
[۲] PLATES       → scripts/generate_images.sh (تصویر هر صحنه + پلیت تیتراژ)
[۳] VOICE        → scripts/generate_voice.sh (روایت انگلیسی هر صحنه)
[۴] MUSIC        → scripts/make_music.py (پد آمبیانت هم‌مدت ویدیو)
[۵] ASSEMBLY     → scripts/assemble.py (Ken Burns + کراس‌فید + زیرنویس + تیتراژ)
[۶] QC           → ffprobe + چک فریم + تحویل به download/
```

**قانون طلایی:** هر فاز خروجی ملموس روی دیسک می‌سازد. اگر فازی شکست خورد، همان فاز را
(نه کل خط تولید) اصلاح و دوباره اجرا کن. اسکریپت‌ها idempotent هستند — اجرای دوباره فقط
فایل‌های گم‌شده را بازسازی می‌کند.

## محدودیت‌های سخت فنی (قبل از نوشتن فیلمنامه بخوان!)

این محدودیت‌ها در تست واقعی تأیید شده‌اند — رد کردنشان = خروجی خراب:

| محدودیت | مقدار | دلیل |
|---|---|---|
| زبان روایت TTS | فقط **انگلیسی** (voice=`jam`) | TTS فارسی پشتیبانی نمی‌شود (تست شد → خروجی بی‌معنی) |
| زیرنویس | **فارسی** با فونت Vazirmatn از assets | RTL با libass+fribidi+harfbuzz درست رندر می‌شود |
| هر جمله روایت | ≤ 900 کاراکتر | سقف TTS = 1024 کاراکتر |
| تصویر صحنه | فقط سایز `1344x768` | سپس در تدوین به 1280x720 crop/motion می‌شود |
| تعداد صحنه‌ها | 4–16 صحنه | تعادل کیفیت/زمان تولید |
| مدت هر صحنه | 6–20 ثانیه | روایت + padding |
| fps / رزولوشن خروجی | 30fps, 1280x720, H.264+AAC | سازگار با یوتیوب/اینستاگرام |

## فاز ۱ — فیلمنامه (خودت می‌نویسی، این مهم‌ترین کار توست)

ساختار روایت را از فیلم الگو بردار: **cold-open قلاب‌دار → عنوان → بدنه موضوعی →
پایان‌بندی احساسی → تیتراژ**. جمله‌ها کوتاه، کنایی، آهنگین. روایت انگلیسی ساده و شاعرانه
بنویس (مثل: "Every story you know about the past was written down by someone.")

فایل `screenplay.json` در پوشه پروژه بساز (الگوی کامل: `references/screenplay-schema.md`):

```json
{
  "project": "my-film",
  "title": "THE WIND CATCHERS",
  "title_fa": "بادگیرها",
  "style_prompt": "cinematic painted documentary style, hand-painted texture, warm ochre and amber palette, soft golden hour light, volumetric dust rays, no text, no watermark",
  "voice": "jam",
  "speed": 0.95,
  "music": { "enabled": true, "root_hz": 110, "volume_db": -23 },
  "scenes": [
    {
      "narration": "In the desert of central Iran, water was never taken for granted.",
      "subtitle": "در کویر مرکزی ایران، آب هرگز بدیهی نبود.",
      "visual_prompt": "aerial view of an ancient adobe city at golden hour, wind towers rising from rooftops",
      "motion": "zoom-in",
      "title_overlay": true
    }
  ],
  "credits": [
    { "role": "WRITTEN & DIRECTED BY", "name": "GLM" },
    { "role": "PAINTED IN CODE BY", "name": "Z-AI Image" },
    { "role": "VOICE BY", "name": "Z-AI TTS" },
    { "role": "MUSIC BY", "name": "Synth Engine" },
    { "role": "MADE WITH", "name": "Video Producer Skill" }
  ]
}
```

قواعد فیلمنامه:
- `style_prompt` **پیشوند ثابت** هر visual_prompt است → یکدستی بصری کل فیلم (راز آلوانا).
- `subtitle` ترجمه وفادار-not-لفظی همان جمله روایت است.
- `motion`: یکی از `zoom-in | zoom-out | pan-left | pan-right` — متناوب انتخاب کن تا ریتم تکراری نشود.
- صحنه اول `"title_overlay": true` بگذار (عنوان بزرگ روی تصویر اول fade می‌شود).
- `credits` را با نقش‌های واقعی ابزارهایی که استفاده کردی پر کن.

## فاز ۲ تا ۵ — اجرای خط تولید

پس از نوشتن screenplay.json در `examples/<project>/` (یا مسیر دلخواه):

```bash
SKILL=/home/z/my-project/skills/video-producer
PROJ=<project-dir>

# ۲) تصاویر صحنه‌ها + پلیت تیتراژ (z-ai image, 1344x768)
bash $SKILL/scripts/generate_images.sh $PROJ

# ۳) روایت صوتی هر صحنه (z-ai tts → wav)
bash $SKILL/scripts/generate_voice.sh $PROJ

# ۴) پد موسیقی آمبیانت (ffmpeg sine synthesis)
python3 $SKILL/scripts/make_music.py $PROJ

# ۵) تدوین نهایی: Ken Burns + کراس‌فید + زیرنویس فارسی + عنوان + تیتراژ
python3 $SKILL/scripts/assemble.py $PROJ
```

خروجی نهایی: `$PROJ/output/final.mp4` — آن را به `/home/z/my-project/download/` کپی کن
و مسیر را به کاربر بده.

## نکات اجرایی که در تست آموخته شد

- **زیرنویس چسبیده (burned-in)** با فایل ASS ساخته می‌شود (توسط `assemble.py`). متن فارسی را
  خام در ASS بگذار — libass خودش RTL و اتصال حروف را درست انجام می‌دهد. کاراکترهای `{}` ویژه
  ASS را در متن زیرنویس استفاده نکن.
- **همگام‌سازی صدا/تصویر**: مدت هر صحنه = 0.6s lead + مدت روایت + 0.8s tail. روایت دقیقاً
  ۰٫۶ ثانیه بعد از شروع دیداری صحنه شروع می‌شود (بعد از کامل شدن کراس‌فید ۰٫۸ ثانیه‌ای —
  ریتم طبیعی گویندگی مستند).
- **کراس‌فید 0.8 ثانیه** بین صحنه‌ها؛ شروع صحنه‌ها در تایم‌لاین نهایی به‌صورت cumulative
  با کسر فیدها توسط assemble.py محاسبه می‌شود — دستی چیزی جابه‌جا نکن.
- **موسیقی**: پد سینتی root+fifth+octave با tremolo آهسته و lowpass؛ ولوم پایین
  (-23dB) که روایت را نپوشاند. mood تهاجمی نخواهد شد — این موتور vol-1 قابل کنترل است.
- اگر ویدیو برای اینستاگرام Reels خواستی: فعلاً خروجی افقی بساز و کاربر را آگاه کن که
  قالب عمودی در نقشه راه اسکیل است (crop مرکزی + زیرنویس جابه‌جا) — برای v1 افقی پیش‌فرض.
- **QC نهایی الزامی**: `ffprobe` مدت/کدک را چک کن + با ffmpeg 3 فریم شروع/وسط/انتها
  استخراج کن و با `z-ai vision` کیفیت را چک کن (زیرنویس خواناست؟ تصویر سالم است؟).

## مسیرهای مرجع

- `references/screenplay-schema.md` — اسکیمای کامل screenplay.json + قواعد نوشتاری
- `examples/demo-yazd/` — پروژه نمونه تست‌شده (ویدیوی «بادگیرها») — الگوی دقیق ساختار پوشه
- `assets/fonts/Vazirmatn-*.ttf` — فونت زیرنویس فارسی (کاربرد در ASS + پلیت تیتراژ)
- `evals/evals.json` — تست‌کیس‌های پیشنهادی برای بهبود آینده اسکیل

## خطایابی سریع

| نشانه | علت | راه‌حل |
|---|---|---|
| TTS خطای 429 | rate-limit | 20s صبر کن، retry — اسکریپت‌ها خودکار retry دارند |
| زیرنویس‌ها مربع/جدا‌جدا | فونت پیدا نشده | fc-list \| grep Vazirmatn — اگر خالی: فونت را از assets نصب کن |
| صدا و تصویر ناهمگام | دستکاری دستی مدت‌ها | فقط screenplay.json را ویرایش کن و assemble.py را دوباره اجرا کن |
| تصویر صحنه mismatch | پرامپت مبهم | visual_prompt را با جزئیاتِ ملموس (سوژه، نور، قاب) بازنویسی کن |
| ffmpeg خطای zoompan | فریم‌شمارش | همیشه `fps=30` و `d=<frames>` عدد صحیح — assemble.py مدیریت می‌کند |
