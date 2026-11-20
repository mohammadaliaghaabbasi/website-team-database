---
name: film-studio
description: >-
  استودیو فیلم‌سازی حرفه‌ای — سیستم تولید فیلم کامل با معماری «تولیدکنندهٔ اجرایی» (Executive
  Producer). این اسکیل متدولوژی OpenMontage + آلوانا + MovieAgent را با استک ابزارهای کاربر
  (Google Gemini Pro، Nano Banana، Google Flow/Veo، Gemini Omni Flash) و ابزارهای داخلی
  (z-ai image/TTS/LLM + ffmpeg) ترکیب می‌کند. هر وقت کاربر گفت «فیلم بساز»، «مستند بساز»،
  «تریلر بساز»، «ویدیوی سینمایی بساز»، «با Gemini/Veo/Flow ویدیو بساز»، «پکیج تولید ویدیو
  بده»، «استودیو فیلم» یا خواست از موضوعی فیلم حرفه‌ای بسازد — این اسکیل را اجرا کن.
  خروجی: پکیج تولید کامل (فیلمنامه + شات‌لیست + پرامپت‌های آماده‌ی کپی-پیست برای هر ابزار)
  و/یا فیلم نهایی تدوین‌شده (MP4 با روایت، زیرنویس فارسی RTL، موسیقی، تیتراژ).
---

# 🎬 استودیو فیلم‌سازی حرفه‌ای (Film Studio)

> **فلسفه:** من «تولیدکنندهٔ اجرایی» (EP) استودیو هستم. کاربر مالک خلاقیت است.
> ابزارها عصای دست کارگردانی‌اند. هر تولید از ۷ مرحلهٔ ساخت‌یافته می‌گذرد و هیچ تولیدی
> بدون عبور از خط تولید (pipeline) انجام نمی‌شود.

**منابع متدولوژی** (ترکیب بهترین‌ها از تحقیق ۲۰۲۶):
- **OpenMontage** (۶۸K ستاره) — معماری pipeline + مهارت‌های کارگردان مرحله + پروتکل تصمیم
- **آلوانا** (فیلم تحلیل‌شده «هزاره‌های خاموش») — سبک مستند نقاشی‌گونه + ساختار روایی
- **MovieAgent / FilmAgent** — بانک شخصیت + نقش‌های کارگردان/فیلمنامه‌نویس/استوری‌برد
- **راهنماهای رسمی گوگل** — فرمول‌های پرامپت Nano Banana / Veo 3.1 / Flow / Omni Flash
- **video-producer** (اسکیل داخلی قبلی) — موتور تدوین ffmpeg اثبات‌شده

---

## ۱) قاعدهٔ صفر — همه‌چیز از خط تولید می‌گذرد

هر درخواست فیلم/ویدیو باید این مسیر ۷ مرحله‌ای را طی کند (الگوبرداری از OpenMontage):

```
موضوع کاربر
   │
   ▼
[۰] INTAKE      → دسته‌بندی درخواست + انتخاب MODE و PIPELINE (این SKILL.md)
[۱] RESEARCH    → جستجوی وب (۸+ جستجو) → research_brief.md (واقعیت، نه توهم)
[۲] CONCEPT     → ۲-۳ کانسپت متمایز → انتخاب کاربر (GATE)
[۳] SCREENPLAY  → screenplay.json (قلب سیستم) (GATE)
[۴] SHOT LIST   → تجزیه به شات + پرامپت هر ابزار → production_package/ (GATE)
[۵] ASSETS      → تولید تصاویر/ویدیو/صدا (بیرونی یا داخلی) (GATE پکیج)
[۶] ASSEMBLY    → timeline.json → assemble.py → final.mp4
[۷] QC          → qc_check.py + بازبینی فریم → تحویل به download/
```

**قواعد الزامی:**
- قبل از نوشتن یک کلمه فیلمنامه، RESEARCH واقعی انجام بده (web_search حداقل ۸ جستجو).
- هر مرحله خروجی ملموس روی دیسک می‌سازد (`projects/<slug>/`).
- تصمیم‌های بزرگ (کانسپت، فیلمنامه، شات‌لیست، تولید دارایی) نیازمند تأیید کاربرند —
  بعد از ارائهٔ خلاصهٔ مرحله، نوبتت را تمام کن و منتظر پاسخ بمان.
- تصمیم‌ها را در `decision_log` ثبت کن (append-only): چه گزینه‌هایی بود، چه انتخاب شد، چرا.

---

## ۲) سه حالت اجرا (MODE) — انتخاب بر اساس ابزارهای در دسترس

| MODE | نام | چه زمانی | چه کسی چه کاری می‌کند |
|------|-----|----------|----------------------|
| **A** | `google-suite` | کاربر Gemini Pro + Nano Banana + Flow/Veo + Omni Flash دارد (استک اصلی کاربر) | من: تحقیق/فیلمنامه/پکیج پرامپت/تدوین. کاربر: اجرای پرامپت‌ها در ابزارهایش و بازگرداندن دارایی‌ها |
| **B** | `in-house` | تولید سریع داخلی بدون ابزار بیرونی | من همه‌چیز: `video-producer` pipeline (z-ai image + TTS + ffmpeg) |
| **C** | `hybrid` | ترکیب: مثلاً کی‌فریم‌ها داخلی، موشن با Veo، تدوین با من | تقسیم کار per-shot در شات‌لیست |

**MODE A — جریان اصلیِ کاربر (پکیج تولید):**
1. من `production_package/` می‌سازم: پرامپت‌های آماده‌ی کپی-پیست برای:
   - **Gemini Pro**: تقویت کانسپت/فیلمنامه (اختیاری — من خودم هم می‌نویسم)
   - **Nano Banana**: شیت شخصیت (Ingredients) + کی‌فریم هر شات + جفت‌فریم اول/آخر
   - **Flow/Veo 3.1**: پرامپت هر شات (فرمول ۵بخشی + تایم‌استمپ + Ingredients)
   - **Omni Flash**: دستورهای جراحی ویرایش مکالمه‌ای (جمله‌های کوتاه + «Keep everything else the same.»)
2. کاربر پرامپت‌ها را در ابزارهایش اجرا می‌کند و فایل‌ها را در `assets/` پروژه می‌گذارد
   (clips ویدیویی mp4 / تصاویر png / صدای روایت wav).
3. من با `assemble.py` تدوین نهایی می‌کنم (رسم زیرنویس، میکس صدا، تیتراژ).

**MODE B — خط داخلی:** مستقیماً از `skills/video-producer/SKILL.md` اجرا کن
(اسکیل خواهری — همان موتور تدوین را استفاده می‌کند).

**انتخاب MODE در INTAKE:** اگر کاربر ابزار گوگلی را نام برد → A. اگر گفت «خودت بساز» → B.
اگر بخشی را خودش می‌سازد → C. در پروژه (`project.json`) ثبت و در طول تولید ثابت نگه دار —
تغییر MODE = تصمیم جدید در decision_log.

---

## ۳) پنج PIPELINE — انتخاب بر اساس ژانر

| Pipeline | برای | الگوی روایی |
|----------|------|-------------|
| `documentary` | مستند روایی/علمی/تاریخی | cold-open قلاب → عنوان → بدنه → پایان احساسی (سبک آلوانا) |
| `cinematic` | تریلر/برندفیلم/تیزر | beat map صعودی → reveal → landing |
| `explainer` | آموزشی/توضیح مفهوم | قلاب → تنش → مفهوم‌ها → اثبات → جمع‌بندی |
| `short-form` | ریلز/تیک‌تاک/شورت (۹:۱۶) | hook ۳ ثانیه‌ای → چرخهٔ سریع → CTA |
| `montage` | موزیک‌ویدئو/مودپیس | قطع ریتمیک روی موسیقی، بدون/کم روایت |

انتخاب pipeline را در INTAKE با یک جمله به کاربر اعلام کن و در `project.json` ثبت کن.

---

## ۴) ساختار پروژه (یکسان برای همهٔ MODEها)

```
projects/<slug>/
├── project.json          # شناسنامه: mode, pipeline, stage status, decision_log
├── artifacts/            # خروجی هر مرحله
│   ├── research_brief.md
│   ├── concepts.md
│   ├── screenplay.json   # قلب سیستم (اسکیما در references/screenplay-schema.md)
│   └── decision_log.json
├── production_package/   # MODE A/C: پرامپت‌های آماده (ساخت با build_package.py)
│   ├── 00_README.md      # راهنمای اجرا برای کاربر
│   ├── 01_character_sheets.md
│   ├── 02_shot_prompts.md
│   ├── 03_audio_plan.md
│   └── timeline.json     # نقشهٔ تدوین
├── assets/               # دارایی‌های بازگشتی/تولیدی
│   ├── clips/            # شات‌های ویدیویی (Veo/Omni/mp4)
│   ├── images/           # کی‌فریم‌ها/تصاویر (png/jpg)
│   ├── voice/            # روایت (wav/mp3)
│   └── music/            # موسیقی
├── work/                 # فایل‌های کاری assemble.py
└── output/final.mp4      # تحویل نهایی → کپی به /home/z/my-project/download/
```

ایجاد پروژه: `python3 scripts/init_project.py <slug> --mode A --pipeline documentary --title "..."`

---

## ۵) قرارداد ارتباط تصمیم (از OpenMontage — الزامی)

- **اعلام قبل از اجرا:** قبل از هر تولید پرهزینه/مهم، بگو: کدام ابزار، کدام مدل، چرا،
  نمونه است یا批量.
- **اجازه قبل از تغییر بزرگ:** تعویض ابزار/سبک/رندر/حذف روایت یا موسیقی = اول بپرس.
- **ثبت تصمیم‌ها:** `decision_log` در `project.json` — append-only؛ هر تغییر، مدخل جدید
  با همان (category, subject).
- **بدون جایگزینی پنهان:** اگر مسیر تأییدشده مسدود شد، گزینه‌ها را ارائه بده، نه سکوت.
- **موسیقی همیشه در PROPOSAL روشن شود** (کتابخانهٔ شخصی / تولید / بدون موسیقی).

---

## ۶) دستورهای سریع

```bash
SKILL=/home/z/my-project/skills/film-studio

# شروع پروژه جدید
python3 $SKILL/scripts/init_project.py my-film --mode google-suite \
        --pipeline documentary --title "THE SILENT MILLENNIA" --title-fa "هزاره‌های خاموش"

# ساخت پکیج تولید از screenplay.json (پرامپت‌های NB/Veo/Omni + timeline)
python3 $SKILL/scripts/build_package.py projects/my-film

# تدوین نهایی (بعد از بازگشت دارایی‌ها به assets/)
python3 $SKILL/scripts/assemble.py projects/my-film

# کنترل کیفیت
python3 $SKILL/scripts/qc_check.py projects/my-film
```

---

## ۷) محدودیت‌های سخت (تست‌شده)

| مورد | مقدار |
|------|-------|
| زبان روایت TTS داخلی | فقط انگلیسی (voice=`jam`)، هر جمله ≤ ۹۰۰ کاراکتر |
| زیرنویس فارسی | فونت Vazirmatn (کپی از `skills/video-producer/assets/fonts/`)، RTL با libass |
| کلیپ Veo 3.1 | ۴/۶/۸ ثانیه، ۷۲۰p/۱۰۸۰p، 16:9 یا 9:16 — شات‌لیست را با این گام‌ها ببند |
| کلیپ Omni Flash | ۳-۱۰ ثانیه، 720p/24fps، ویرایش = پرامپت کوتاه جراحی + «Keep everything else the same.» |
| تصویر Nano Banana | 1K/2K/4K، نسبت‌های 1:1 تا 21:9، حداکثر ۱۴ تصویر مرجع در هر پرامپت |
| روایت | ۱۵۰-۱۶۰ wpm برای مستند/آموزشی؛ ۱۲۰-۱۴۰ برای سینمایی/شاعرانه |
| تعداد شات | ۶-۱۶ برای فیلم ۶۰-۱۲۰ ثانیه‌ای (هر شات ۴-۱۰ ثانیه) |

---

## ۸) نقشهٔ مراجع (قبل از هر مرحله مربوطه بخوان)

| فایل | محتوا | کی بخوان |
|------|-------|----------|
| `references/google-suite-guide.md` | فرمول‌های پرامپت NB/Veo/Flow/Omni + الگوهای Ingredients/First-Last/Timestamp | قبل از SHOT LIST (همیشه) |
| `references/cinematography-language.md` | واژگان دوربین/نور/حرکت + فرمول ۵وجهی + قواعد ضد-ذهنی | قبل از SHOT LIST |
| `references/storytelling.md` | قالب‌های قوس روایی، قلاب‌ها، قواعد ریتم، But-Therefore | قبل از SCREENPLAY |
| `references/production-methodology.md` | جزئیات مراحل، گیت‌های کیفیت، QC پس از رندر | قبل از ASSEMBLY/QC |
| `references/alvana-method.md` | سبک مستند نقاشی‌گونه + ساختار آلوانا | pipeline=documentary |
| `references/landscape.md` | تحقیق ۲۰۲۶: مقایسهٔ OpenMontage و بدیل‌ها + آنچه قرض گرفتیم | ارجاع/به‌روزرسانی |

**مسیرهای خواهری:**
- `../video-producer/` — خط داخلی کامل (MODE B) + فونت‌ها + اسکیمای ساده‌تر
- `../storyboard-manager/` — ردیابی خط داستان (برای پروژه‌های چندقسمتی)

---

## ۹) خطایابی سریع

| نشانه | علت | راه‌حل |
|-------|-----|-------|
| TTS داخلی 429 | rate-limit | ۲۰s صبر، retry (اسکریپت‌ها خودکار retry دارند) |
| زیرنویس فارسی مربع | فونت نصب نیست | `fc-list \| grep Vazirmatn` — نبود: از video-producer/assets/fonts نصب کن |
| کلیپ Veo با صدای ناخواسته | صدا در خود پرامپت Veo ساخته شده | در assemble از `duck_clip_audio` یا `mute_clip` استفاده کن |
| شات‌ها ناهم‌سبک | style_prompt ثابت نگه داشته نشده | هر پرامپت باید style بلاک یکسان verbatim داشته باشد |
| شخصیت بین شات‌ها تغییر می‌کند | attributes تکرار نشده | ۳-۶ ویژگی ظاهری شخصیت را verbatim در «هر» پرامپت تکرار کن |
| طول کلیپ‌ها با تایم‌لاین نمی‌خواند | گام‌های ۴/۶/۸s | مدت شات ویدیویی را به multiples واقعی کلیپ‌های تولیدشده بسنج |
