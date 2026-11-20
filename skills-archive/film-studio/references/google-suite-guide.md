# Google Suite Guide — پرامپت‌نویسی برای Gemini Pro / Nano Banana / Flow+Veo 3.1 / Omni Flash

> منبع: راهنماهای رسمی گوگل (Cloud Blog، DeepMind، ai.google.dev) + اسکیل‌های Layer-3
> از OpenMontage. این فایل حافظهٔ فنی استودیو برای استکِ کاربر است.

## نقشهٔ نقش ابزارها در استودیو

| ابزار | نقش استودیویی | خروجی |
|-------|--------------|-------|
| **Gemini Pro** | سرنویسنده/محقق (refinement کانسپت، غنی‌سازی پرامپت، ترجمه) | متن |
| **Nano Banana** (Gemini Image) | طراح تولید/استوری‌بردیست (شیت شخصیت، کی‌فریم، Ingredient) | تصویر |
| **Google Flow + Veo 3.1** | فیلم‌بردار (تولید شات‌های متحرک با صدا) | کلیپ ۴/۶/۸s |
| **Gemini Omni Flash** | تدوینگر VFX (ویرایش مکالمه‌ای کلیپ‌ها) | کلیپ ویرایش‌شده |

**جریان طلایی (Google's own recipe):** Nano Banana کی‌فریم می‌سازد → Veo بین کی‌فریم‌ها
را متحرک می‌کند → Omni Flash تصحیح/ویرایش می‌کند → (Lyria/موسیقی جدا).

---

## ۱) Nano Banana — تولید و ویرایش تصویر

### فرمول‌های رسمی (۵ حالت)

**الف) تولید بدون مرجع:**
```
[Subject] + [Action] + [Location/context] + [Composition] + [Style]
```
مثال: `[Subject] A striking fashion model in a tailored brown dress. [Action] Posing
with a confident, statuesque stance. [Location] Deep cherry red studio backdrop.
[Composition] Medium-full shot, center-framed. [Style] Fashion editorial, medium-format
analog film, pronounced grain, cinematic lighting.`

**ب) تولید با مرجع (Ingredients):**
```
[Reference images] + [Relationship instruction] + [New scenario]
```
مثال: `Using the attached napkin sketch as the structure and the fabric sample as the
texture [Refs], transform this into a high-fidelity 3D armchair render [Relationship].
Place it in a sun-drenched minimalist living room [Scenario].`
- تا **۱۴ تصویر مرجع** در یک پرامپت؛ نقش هر تصویر را صریح بگو (شخصیت/محصول/سبک/پس‌زمینه).

**ج) ویرایش مکالمه‌ای (بدون مرجع جدید):** تغییر را دقیق بگو + چه چیزی دست‌نخورده بماند:
`Remove the man from the photo` — به‌طور ضمنی بقیه ثابت می‌ماند.

**د) اطلاعات زنده:** `[Search request] + [Analytical task] + [Visual translation]`

**هـ) متن/تایپوگرافی در تصویر:**
- متن را در "کوتیشن" بگذار: `"URBAN EXPLORER"`
- فونت را توصیف یا نام ببر: `bold white sans-serif` / `Century Gothic`
- **Text-first hack:** اول در گفتگو متن‌ها را نهایی کن، بعد تصویر با آن متن بخواه.
- ترجمه/لوکالیزیشن: پرامپت به یک زبان + `translate the text into Korean and Arabic`.

### پرامپت مثل مدیر خلاق (Creative Director)

1. **نور را طراحی کن:** `three-point softbox setup` / `Chiaroscuro lighting, harsh high
   contrast` / `Golden hour backlighting creating long shadows`
2. **دوربین/لنز/فوکوس:** `shot on GoPro` / `low-angle shot, shallow depth of field (f/1.8)`
   / `macro lens` / `wide-angle lens`
3. **رنگ و فیلم‌استوک:** `as if on 1980s color film, slightly grainy` /
   `cinematic color grading, muted teal tones`
4. **جنس و بافت:** نه «کت شلوار» بلکه `navy blue tweed`؛ نه «زره» بلکه
   `ornate elven plate armor, etched with silver leaf patterns`

### قواعد طلایی
- **مثبت بنویس** («خیابان خالی» نه «بدون ماشین»).
- فعل قوی اول پرامپت = عمل اصلی.
- **تکرار سبک:** بلاک سبک (پالت/نور/بافت/گرید) را verbatim در هر کی‌فریم تکرار کن.
- تکرار ویژگی‌های شخصیت: ۳-۶ صفت ظاهری، verbatim، در هر شات.
- Specs: 1K/2K/4K (NB2: +512px) | نسبت‌ها 1:1, 3:2, 2:3, 3:4, 4:3, 4:5, 5:4, 9:16,
  16:9, 21:9 (NB2 Flash: +1:4, 4:1, 1:8, 8:1) | تا ۱۴ مرجع | خروجی text+image.

---

## ۲) Veo 3.1 (و Flow) — تولید ویدیو

### فرمول رسمی ۵بخشی
```
[Cinematography] + [Subject] + [Action] + [Context] + [Style & Ambiance]
```
مثال: `Medium shot, a tired corporate worker, rubbing his temples in exhaustion, in
front of a bulky 1980s computer in a cluttered office late at night. Lit by harsh
fluorescent overhead lights and the green glow of the monochrome monitor. Retro
aesthetic, shot as if on 1980s color film, slightly grainy.`

### واژنان سینمایی مؤثر
- **حرکت دوربین:** dolly / tracking / crane / aerial / slow pan / POV
- **قاب‌بندی:** wide / close-up / extreme close-up / low angle / two-shot
- **لنز/فوکوس:** shallow depth of field / wide-angle / soft focus / macro / deep focus

### صدا (ساختار Soundstage)
- دیالوگ در کوتیشن با گوینده: `A woman says, "We have to leave now."` (لحن/لهجه/احساس قابل تعیین)
- `SFX: thunder cracks in the distance`
- `Ambient noise: the quiet hum of a starship bridge`
- موسیقی: `A swelling, gentle orchestral score begins to play`

### نگیتیو پرامپت
مثبت بنویس: `a desolate landscape with no buildings or roads` (نه «no man-made structures»).

### سه Workflow پیشرفته رسمی (قلب استودیو)

**W1 — First & Last Frame (گذار کنترل‌شده):**
1. NB فریم شروع را می‌سازد (پرامپت A).
2. NB فریم پایان را می‌سازد (پرامپت B — مثلاً POV دیگر همان لحظه).
3. Veo با هر دو تصویر: «دوربین ۱۸۰ درجه arc می‌زند، از نمای روبه‌رو به POV پشت سر
   خواننده می‌رسد» + دیالوگ/صدا.

**W2 — Ingredients to Video (صحنهٔ دیالوگ با شخصیت ثابت):**
1. NB برای هر شخصیت + لوکیشن Ingredient می‌سازد.
2. Veo با مراجع: `Using the provided images for the detective, the woman, and the
   office setting, create a medium shot of the detective behind his desk. He looks up
   and says in a weary voice, "Of all the offices in this town, you had to walk into mine."`
3. شات معکوس با همان Ingredients → قاب‌بندی دیگری از همان صحنه.

**W3 — Timestamp Prompting (چندشات در یک تولید):**
```
[00:00-00:02] Medium shot from behind a young female explorer with a leather satchel
and messy brown hair in a ponytail, as she pushes aside a large jungle vine to reveal
a hidden path.
[00:02-00:04] Reverse shot of the explorer's freckled face, her expression filled with
awe as she gazes upon ancient, moss-covered ruins. SFX: rustle of leaves, distant birds.
[00:04-00:06] Tracking shot following her as she runs her hand over carvings on a stone wall.
[00:06-00:08] Wide, high-angle crane shot revealing the lone explorer small in the vast
temple complex. SFX: swelling gentle orchestral score.
```

### مشخصات فنی Veo 3.1
- 720p/1080p | 16:9 یا 9:16 | کلیپ ۴/۶/۸ ثانیه | صدا هم‌زمان | Add/Remove object |
  Ingredients (با صدا) | First&Last frame | watermark SynthID.

### قواعد Flow
- **Ingredients:** عنصر بصری ثابت (شخصیت/شیء/سبک) — با Imagen/NB ساخته یا آپلود؛
  حداکثر ۳ ingredient در هر پرامپت.
- **Frames to Video:** فریم شروع را تعیین کن (از آپلود یا فریم تولید قبلی) → کنترل
  دقیق ترکیب‌بندی و گذار نرم.
- **Scenebuilder:** استوری‌برد داخل Flow: **Jump To** (شخصیت را به لوکیشن جدید ببر،
  ظاهر حفظ می‌شود) + **Extend** (کلیپ را ادامه بده بر اساس فریم‌های آخر).
- Gemini برای تقویت پرامپت: «بگو همهٔ جزئیات ضروری پرامپت‌های قبلی را تکرار کند» تا
  consistency بین کلیپ‌ها حفظ شود.

---

## ۳) Gemini Omni Flash — تولید + ویرایش مکالمه‌ای

مدل: `gemini-omni-flash-preview` — ۳-۱۰s، 720p/24fps، MP4 با صدا، 16:9 یا 9:16.

### پرامپت تولید
صحنه + دوربین + نور + موشن + صدا را توصیف کن:
> Continuous, unbroken handheld shot of a fluffy tabby cat sitting on a sunny
> windowsill... The cat's tail twitches slowly... Sunbeams illuminate dust motes.

- **تک‌شات را صریح اجبار کن:** `In a single continuous shot` / `No scene cuts.`
- **نگیتیو در نثر:** `No dialogue.` / `No extra sound effects.` (پارامتر negative_prompt ندارد)
- **کیفیت:** `Consider micro-detail, expression and timing to create a very rich,
  detailed but entirely natural scene.`
- **تایم‌کد:** `[0-3s] A person is walking [3-6s] They stop and turn around`
- **متن روی صفحه:** `One word on screen at a time: 'did, you, know...' each word 1s.`

### تصاویر مرجع (تگ‌ها)
با `reference_image_paths` به‌ترتیب بفرست و در پرامپت نقش‌دهی کن:
- `<FIRST_FRAME>` → فریم آغازین: `<FIRST_FRAME> a woman is walking`
- `<IMAGE_REF_N>` (از ۰): `in the style of <IMAGE_REF_0> a woman <IMAGE_REF_1> is walking`
- بگو هر تصویر «چه هست» (شخصیت/محصول/سبک/پس‌زمینه)؛ موشن را مشخص توصیف کن.

### ویرایش مکالمه‌ای (تمایز اصلی Omni)
**پرامپت ویرایش = کوتاه و جراحی.** دقیقاً فقط دلتا:
1. کلیپ پایه را تولید کن → `interaction_id` را نگه دار.
2. با `previous_interaction_id` + `operation="edit_video"` فقط تغییر را بگو.
3. همیشه: **`Keep everything else the same.`**
4. لایه‌لایه تصحیح کن: یک نوبت نور، یک نوبت دوربین، یک نوبت اکشن، یک نوبت صدا.

| ❌ ننویس | ✅ بنویس |
|---|---|
| «در ویدیوی مرد روی مبل، لطفاً یک گربهٔ کوچک سیاه اضافه کن و...» | `Add a cat that jumps onto his lap, he begins to pet it. Keep everything else the same.` |
| «لطفاً موبایل را حذف کن و پس‌زمینه را این‌طوری کن که...» | `Make the phone invisible. Keep everything else the same.` |

نمونه‌های کارا: `Make this video anime` / `Change the lighting to be more dramatic` /
`Change the text on the sign to say 'Omni Flash'`.

### محدودیت‌ها (preview)
بدون seed/temperature/system-instruction | بدون extension و first/last-frame | ویدیوی مرجع
≤۳s قابل‌قبول ولی قابل‌اتکا نیست | انگلیسی کامل، بقیهٔ زبان‌ها تست‌نشده | ویرایش ویدیوی
آپلودی در EEA/CH/UK در دسترس نیست | سریع‌تر و ارزان‌تر از Veo برای تکرار — برای شات
سینمایی هیرو → Veo/Seedance؛ برای تکرار و ویرایش → Omni.

---

## ۴) Gemini Pro — سرنویسنده

استفاده‌های اصلی در استودیو:
1. **غنی‌سازی کانسپت:** «۵ زاویهٔ روایی متمایز برای موضوع X با مخاطب Y»
2. **تقویت پرامپت Veo** (از راهنمای Flow):
   > You are the world's most intuitive visual communicator and expert prompt engineer.
   > You possess a deep understanding of cinematic language, narrative structure,
   > emotional resonance, filmic coverage and the capabilities of Google's Veo AI model.
   > Transform my conceptual ideas into meticulously crafted, narrative-style
   > text-to-video prompts that are visually breathtaking and technically precise.
   — برای consistency بین کلیپ‌ها صریح بگو: «تکرار همهٔ جزئیات ضروری از پرامپت‌های قبلی».
3. **ترجمهٔ روایت/زیرنویس** بین فارسی-انگلیسی با لحن حفظ‌شده.
4. **بازخورد ساختاری روی فیلمنامه** (beat map، تنش، پالس‌های ریتمی).

نکته: خودت (GLM) می‌توانی همهٔ این‌ها را انجام دهی — Gemini Pro را وقتی بگذار که کاربر
نسخهٔ انسانی-بازبینی‌شده می‌خواهد یا می‌خواهید دو مغز روی فیلمنامه کار کنند.
