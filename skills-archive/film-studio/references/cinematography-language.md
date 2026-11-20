# Cinematography Language — واژگان و فرمول پرامپت ویدیو (جهانی)

> منبع: OpenMontage `skills/creative/video-gen-prompting.md` (بر پایهٔ مطالعهٔ
> CMU/Harvard "Building a Precise Video Language") + راهنماهای رسمی Veo.
> قانون: مدل‌ها Subject+Scene را خوب می‌فهمند ولی در Motion/Spatial/Camera خطا
> می‌کنند — پرامپت باید هر ۵ اسلات را صریح پر کند.

## فرمول ۵وجهی اسکلت (canonical)

```
[Subject]        نوع + ویژگی‌های بصری کلیدی + افتراق‌گذاری وقتی چند سوژه هست
[Subject Motion] اکشن‌ها به‌ترتیب زمانی؛ تعامل سوژه-شیء و سوژه-سوژه
[Scene]          اورلی‌ها (جدا!) + POV + مکان + ساعت روز + دینامیک صحنه
[Spatial]        اندازهٔ شات + موقعیت در قاب + عمق (FG/MG/BG) + ارتفاع دوربین
                 — و اینکه این‌ها در طول کلیپ چگونه تغییر می‌کنند
[Camera]         سرعت پخش → اعوجاج لنز → ارتفاع → زاویه → فوکوس/DoF → ثبات → حرکت
```

> **پرامپت خودکفا:** پرامپت را طوری بنویس که کسی که ویدیو را ندیده، از متن Alone بتواند
> سوژه/صحنه/موشن/دوربین را تصور کند. اگر تصور نمی‌شود، مدل هم رندر نمی‌کند.

**طول پرامپت:** کوتاه‌تر = آزادی خلاقانهٔ بیشتر | بلندتر = کنترل بیشتر.
- Veo 3.1: ۱۰۰-۲۵۰ کلمه (فلات بعد از ~۲۵۰) | Omni Flash: متوسط، یک شات
- کلیپ هیرو: ۲۰۰-۴۰۰ کلمه | اینزرت: ۸۰-۱۵۰

## قاب‌بندی (Shot Types)

| Shot | کاربرد |
|------|--------|
| Wide / establishing | باز کردن صحنه، زمینهٔ مکان |
| Full / long | سوژه سرتاپا + محیط |
| Medium | از کمر، تعادل جزئیات/زمینه |
| Medium close-up | از سینه، صمیمیت گفتگو |
| Close-up | چهره/شیء کلیدی، تأکید احساس |
| Extreme close-up | جزئیات منزوی (چشم، قطره، بافت) |
| Over-the-shoulder | قاب گفتگو |
| POV | تماشاگر = شخصیت |
| Bird's-eye / top-down | نمای نقشه‌ای، احساس تقصیر وردیگن (omniscient) |
| Worm's-eye | نگاه به بالا، عظمت |
| Dutch / canted | افق کج، بی‌قراری/تنش |
| Low angle | قدرت/سلطه |
| High angle | کوچکی/آسیب‌پذیری |

## حرکت دوربین — سه خانوادهٔ جدانشدنی

| خانواده | پایه‌ها | قاعده |
|---|---|---|
| **Translation** (جابه‌جایی فیزیکی) | dolly in/out، truck L/R، pedestal up/down | `dolly forward toward subject` |
| **Rotation** (چرخش در جا) | pan L/R، tilt up/down، roll CW/CCW | `pan right across the room` |
| **Lens-only** (بدون حرکت) | zoom in/out، rack focus، pull focus، focus tracking | `zoom in` ≠ `dolly in` |
| **Hybrid/امضا** | dolly zoom (vertigo)، arc/orbit، crane، whip pan، tracking، handheld | `vertigo` فقط لحظهٔ رمزگشایی |
| **ثبات** | static (سخت‌گیرانه)، micro-shake، locked-off | `static` = صفر حرکت/زوم/فوکوس |

> **dolly ≠ zoom.** dolly جابه‌جایی دوربین؛ zoom تغییر فاصلهٔ کانونی. **pan ≠ truck.**
> pan می‌چرخد، truck جابه‌جا می‌شود. مدل‌ها را با توکن غالب دنبال می‌کنند.

## ارتفاع و زاویه

- ارتفاع: aerial-level (ارتفاع پهپاد) / overhead / eye-level / hip-level /
  ground-level (مچ پا) / water-level / underwater
- زاویه: bird's-eye (سختِ top-down) / high / level / low / worm's-eye /
  Dutch ثابت / Dutch چرخان
- **bird's-eye = سختِ top-down؛ aerial = ارتفاع.** پهپاد ۴۵ درجه = high angle از ارتفاع aerial.

## نور

| اصطلاح | اثر |
|--------|-----|
| Natural light | نرم/واقعی (آفتاب صبح، ابری، مهتاب) |
| Golden hour | گرم، سایهٔ بلند، رمانتیک |
| High-key | روشن/یکنواخت — کمدی، لایف‌استایل |
| Low-key | تیره/کنتراست بالا — تریلر، درام |
| Rembrandt | مثلث نور روی گونه |
| Film noir | سایهٔ عمیق، هایلایت تیز |
| Volumetric | پرتو مرئی در غبار/مه |
| Backlighting | سیلوئت |
| Side lighting | دراماتیک، سایهٔ جهت‌دار |
| Practical lights | منابع داخل قاب (چراغ، شمع، نئون) |
| Rim / edge | جدا کردن سوژه از پس‌زمینه |

جهت‌ها: key/fill/bounce/rim/spill/negative fill. رنگ دما: warm (tungsten/amber) /
cool (daylight/blue) / mixed.

## لنز و فوکوس

- Wide-angle (24-35mm): دید باز، پرسپکتیو اغراق‌شده | Telephoto (85mm+): فشرده،
  ایزوله | Anamorphic: کشیدگی + flare امضایی
- Distortion: **fisheye** (انحنای شدید لبه‌ها) ≠ **barrel** (انحنای ملایم خطوط)
- DoF: deep focus (همه تیز) / shallow (بوکه) / extremely shallow / **rack focus**
  (جهش فوکوس بین دو سوژه) / **pull focus** (آهسته‌تر) / focus tracking (دنبال سوژهٔ متحرک)
- وقتی DoF در شات تغییر می‌کند: صفحهٔ فوکوس شروع **و** پایان را برچسب بزن (FG/MG/BG).

## گذار سوژه (Subject Transitions)

| برچسب | معنی |
|--------|------|
| **revealing** | سوژهٔ جدید وارد قاب می‌شود (حرکت سوژه یا دوربین) |
| **disappearing** | سوژه خارج می‌شود |
| **switching** | فوکوس از A به B (با کات/rack focus/whip) |
| **complex alternating** | رفت‌وبرگشت مکرر فوکوس (کراس‌کات دیالوگ) |

علت را نام ببر: `by subject movement` یا `by camera movement`.

## لنگر هویت (Identity Anchoring) — مهم‌ترین قانون consistency

> در هر شاتِ پرامپتِ چندتایی، همان ۳-۶ ویژگی افتراق‌گذار هر شخصیت را **verbatim**
> تکرار کن. ضمیر و «همان شخصیت» کار نمی‌کند.
>
> مثال: «آنگ — کچل، خالکوبی فلش‌آبی روی پیشانی، ردای نارنجی-زرد — عصایش را می‌کارد…
> آنگ — کچل، خالکوبی فلش‌آبی روی پیشانی، ردای نارنجی-زرد — به دوربین برمی‌گردد.»

## افکت‌های زمانی

| Primitive | تعریف |
|-----------|-------|
| Time-lapse | بسیار سریع‌تر از واقعی (شبیه دویدن ابر) |
| Fast-motion | کمی سریع‌تر (1x-3x) |
| Slow-motion | کندتر از واقعی |
| Stop-motion | حرکت گسسته فریم‌به‌فریم |
| Speed-ramp | ترکیب سریع/کند در یک شات |
| Time-reversed | پخش معکوس |

دستگاه‌های دیگر: freeze-frame / rapid cuts / continuous long take / fade in-out /
**match cut** (پیوستگی بصری بین صحنه‌ها).

## صدا (مدل‌های دارای صدا: Veo 3.1 / Omni / LTX-2)

- **Ambient:** باد، باران، ترافیک، زمزمهٔ جمعیت، پرندهٔ جنگل، هوم ماشینی
- **Diegetic:** قدم، صدای در، شیشه، تایپ
- **Voice:** whisper / calm narration / energetic announcer / gravitas
- **Music mood:** `soft piano in background` / `upbeat electronic`
- دیالوگ در کوتیشن: `Character says: "Hello world."`

## سبک‌ها

- **سینمایی:** film noir / period drama / thriller / documentary / arthouse /
  epic space opera / 1970s romantic drama / 90s doc-style
- **انیمیشن:** Ghibli / anime / Pixar-like 3D / stop-motion / claymation /
  hand-painted 2D-3D hybrid / cel-shaded / low-poly
- **جنبش‌های هنری:** امپرسیونیستی / سورئال / آرت‌دکو / باوهاوس / آبرنگ /
  ذغالی / مرکب / رمان گرافیکی / بلوپرینت
- **گرید/استوک:** گرمِ کداک / خنکِ فوجی / 16mm سیاه‌سفید / 35mm photochemical /
  grain وینتیج / halation / teal-and-orange

## قانون ضد-ذهنی (Anti-Subjective) — بنیادین

> **صفت احساسی را با علتِ بصریِ احساس جایگزین کن.**
> - `sad character` → `tears on cheek, shoulders slumped, staring at empty chair`
> - `cinematic mood` → `low-key Rembrandt key + 35mm anamorphic + crushed shadows`
> - `epic` → `low-angle, 24mm wide, sun directly behind subject, lens flare on the rim`
>
> «inspiring / powerful / moody / epic» پیکسل را قید نمی‌کنند.

| ❌ | چرا | ✅ |
|---|-----|-----|
| `Beautiful scene` | مبهم | `Wet cobblestone street, warm streetlamp glow reflecting in puddles` |
| `Person moves quickly` | اکشن نامرئی | `Woman sprints three steps and vaults over the railing` |
| `Cinematic look` | پیش‌فرض همهٔ مدل‌ها | `anamorphic lens, shallow DOF, golden hour lighting` |
| متن/لوگو | رندر متن نامطمئن | از متن داخل صحنه پرهیز کن یا نقص را بپذیر |
| فیزیک پیچیده | آرتیفکت | رقص/راه‌رفتن OK؛ انفجار ریسکی |
| چند گوینده | هم‌گویی خراب | یک گوینده در هر کلیپ + reaction shot |
| نور متناقض | `روشن ظهر`+`سایهٔ تیره` | یک ست نور، تعهد کن |

## استراتژی تکرار (Iteration)

1. ساده شروع کن: سوژه+اکشن+مکان.
2. یک عنصر در هر بار اضافه کن: اول دوربین، بعد نور، بعد سبک.
3. شات بد شد → عقب برگرد: دوربین ثابت، اکشن ساده، دوباره.
4. consistency بین کلیپ‌ها → همان description سبک/نور/گرید را عیناً تکرار کن.
5. نتیجهٔ خوب = seed را ذخیره کن (در ابزارهایی که seed دارند؛ Omni ندارد).

## قالب آمادهٔ پرامپت (template)

```
[Shot]: Medium close-up, slight low angle
[Camera]: Slow dolly-in
[Subject]: A weathered fisherman in his 60s, salt-and-pepper beard, dark wool sweater
[Action]: Pulls the rope hand-over-hand, muscles straining, pauses and looks out to sea
[Setting]: Wooden dock at dawn, calm grey ocean, distant fog bank, seagulls wheeling
[Lighting]: Soft overcast with warm break in clouds, gentle rim light from rising sun
[Style]: Documentary cinematography, 35mm film grain, muted earth tones, cold blue-grey
[Audio]: Rope creaking, water lapping, distant gull cries, wind
```
