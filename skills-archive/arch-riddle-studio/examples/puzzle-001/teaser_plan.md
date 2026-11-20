# 🎬 تیزر معمای #۰۰۱ «مربعِ تنها» — فیلمنامه و پکیج تولید (MODE A)

> ۱۰.۰ ثانیه | 9:16 | بدون گفتار | موسیقی آمبیِنت + ضرب قلب
> ابزار: کی‌فریم‌ها با **Nano Banana Pro 2** → موشن با **Veo 3.1** → رتوش جراحی با **Omni Flash** → تدوین با دستیار (film-studio/assemble.py)

---

## STYLE BLOCK (در «هر» پرامپت عیناً تکرار شود — قاعدهٔ ثبات سبک)

```
STYLE: Minimalist brutalist architecture photography, raw board-formed concrete
with visible wood-grain formwork texture, warm late-afternoon sunlight with long
sharp shadows, small Persian courtyard with an ancient dark-green cypress tree,
muted earthy palette (concrete gray, warm ochre, deep cypress green, aged brass),
photorealistic, cinematic composition, 35mm lens feel, high detail, no people,
no text, no watermark.
```

---

## SHOT LIST

### S1 — قلاب (0–2.5s) | دوربین: orbit مورب
**محتوا:** دوربین به‌آرامی حول حجم پله‌های بتنیِ «درهم» می‌چرخد. پله‌ها به‌ظاهر بی‌هدف در هم تنیده‌اند. نورِ موربِ بعدازظهر، سایه‌های تیز می‌سازد.

**Nano Banana (کی‌فریم اول):**
```
[STYLE BLOCK above]
SCENE: Aerial-ish three-quarter view of a monolithic brutalist concrete stair
volume in a small Persian courtyard, stairs pointing in contradictory directions
like an M.C. Escher sketch made real, long dramatic shadows, a small ancient
cypress tree standing apart in a corner, a tiny brass disc embedded in the
ground at the center of the courtyard. Aspect ratio 9:16.
```

**Veo 3.1 (موشن — فرمول ۵بخشی):**
```
Action: Slow cinematic orbit around a chaotic brutalist concrete stair volume
in a Persian courtyard at late afternoon; camera moves 30 degrees clockwise at
eye level; shadows crawl across the concrete.
Subject: monolithic stair volume, contradictory stair directions, cypress tree.
Scene: small Persian courtyard, board-formed concrete, warm low sun.
Style: [STYLE BLOCK]
Camera motion: smooth orbital move, slight handheld breathing.
Ambiance: soft wind, distant birds only, no music (music added in edit).
Duration: 4s, 9:16, 1080p.
```

### S2 — جزئیات مشکوک (2.5–5s) | دوربین: close-up رد‌شده
**محتوا:** سریع‌ترین کات: سه کلوزآپ ۰.۸ ثانیه‌ای از «تداخل‌های عجیب» — لبهٔ پله‌ای که به دیوار می‌رسد و ناپدید می‌شود؛ دست‌اندازِ برنجیِ کوچک در کف که دوربین «مورب» از روی‌اش رد می‌شود (نیم‌ثانیه، مشروط به دقت بیننده)؛ سایهٔ نرده که لحظه‌ای به شکل «؟» می‌افتد.

**Nano Banana (کی‌فریمها — ۳ قاب):**
```
[STYLE BLOCK]
SCENE: Extreme close-up of two concrete stair edges meeting at an impossible,
contradictory angle, wood-grain formwork texture in sharp detail.
9:16.
```
```
[STYLE BLOCK]
SCENE: Low-angle macro shot of a small polished brass disc embedded flush in
concrete courtyard pavement, partially catching golden sunlight.
9:16.
```
```
[STYLE BLOCK]
SCENE: Long shadow of a thin steel railing cast on a raw concrete wall,
naturally shaped like a question mark, warm afternoon light.
9:16.
```

**Veo:** سه کلیپ ۴ثانیه‌ای از هر کی‌فریم با حرکت minimal (dolly-in آرام). در تدوین به ۰.۸ث کات می‌شوند.

### S3 — تعلیق (5–8s) | دوربین: dolly-in به‌سمت «تقریباً»
**محتوا:** دوربین از سطح کف به‌سمت مرکز حیاط پیش می‌رود — پله‌ها در حال «به‌هم‌نشستنِ» تقریبی‌اند (پارالاکس) — انگار یک ثانیه دیگر همه‌چیز قفل می‌شود… و کات، پیش از قفل.

**Nano Banana (کی‌فریم اول/آخر — جفت‌فریم برای Veo):**
```
[STYLE BLOCK]
SCENE: Camera at the far edge of the courtyard, stair volume still chaotic
from this near-miss angle, brass disc visible ahead on the ground.
9:16.
```
```
[STYLE BLOCK]
SCENE: Camera now just 1 meter from the brass disc at knee height looking up
at the stair volume — stairs ALMOST aligning into a near-square but still
slightly twisted, teasing one more step of alignment. Cypress tree close behind.
9:16.
```

**Veo 3.1 (First/Last Frame — W1):** از جفت‌فریم بالا، حرکت گلایدِ به‌جلو؛ «تقریباً قفل» — نه قفل.

### S4 — امضا (8–10s) | کات به بلک
**محتوا:** کات به سیاه. تایپوگرافی طلایی: «؟» بزرگ، زیرش کوچک: «معمای ۰۰۱». (این شات با PIL در تدوین ساخته می‌شود — بدون ابزار بیرونی.)

---

## دستورهای Omni Flash (رتوش جراحی)

| کلیپ | دستور (مکالمه‌ای) |
|------|-------------------|
| S1 (اگر پله‌ها هم‌جهت از آب درآمدند) | `Make the stairs point in more contradictory directions.` + `Keep everything else the same.` |
| S2-brass (اگر دایره برنجی گم شد) | `Make the brass disc clearly visible and polished.` + `Keep everything else the same.` |
| S3-last (اگر قفل کامل شد!) | `Keep the stair alignment slightly imperfect and twisted.` + `Keep everything else the same.` — ⚠️ این مهم‌ترین دستور است: قفل نباید در تیزر اتفاق بیفتد |

---

## موسیقی
پدِ سینتی آرام (root+fifth) + ضربِ قلب از ثانیهٔ ۵ که در ۷.۵ به‌شدت تند می‌شود → کات سکوتِ ثانیهٔ ۸ → «دینگ» ظریفِ فلز برنجی با امضای «؟».
(تولید داخلی با `make_music.py` اسکیل video-producer، یا کتابخانهٔ کاربر.)

---

## تدوین (چک‌لیست)
- [ ] ۴ کلیپ Veo → `assets/clips/S1..S3.mp4`
- [ ] تایم‌لاین: S1(2.5s) + S2(0.8×3) + S3(2.5s) + بلک‌فریم امضا(2s) = 10.0s
- [ ] کاتِ S3 دقیقاً ۰.۳ ثانیه پیش از «قفلِ کامل»
- [ ] زیرنویس ندارد (بی‌کلام) — متن روی بلک‌فریم: طلایی
- [ ] خروجی: 9:16، 1080×1920، 30fps
- [ ] QC: دایرهٔ برنجی در S2 قابل مشاهده ولی «فرعی» باشد — نه واضح
