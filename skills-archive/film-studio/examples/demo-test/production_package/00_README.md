# 🎬 پکیج تولید — THE STONE AND THE RIVER (سنگ و رود)

**Mode:** hybrid | **Pipeline:** documentary |
**هدف:** ~45s، 16:9 |
**مدت پلان‌شده:** 29s (بدنه 19s + تیتراژ 10s)

## ترتیب اجرا (در ابزارهای خودت)

1. **شیت‌های شخصیت** → `01_character_sheets.md` — هر پرامپت را در Nano Banana اجرا کن؛
   خروجی را در `assets/images/char_<id>.png` ذخیره کن (Ingredient).
2. **کی‌فریم هر شات** → `02_shot_prompts.md` بخش NB — خروجی در
   `assets/images/<SHOT_ID>.png` (در صورت داشتن فریم آخر: `assets/images/<SHOT_ID>_end.png`).
3. **شات‌های متحرک** → همان فایل، بخش Veo — در Flow/Veo با «Frames to Video» (کی‌فریم
   = فریم اول) یا «Ingredients to Video» (شخصیت‌ها) اجرا کن؛ خروجی در
   `assets/clips/<SHOT_ID>.mp4`.
4. **ویرایش جراحی (اختیاری)** → همان فایل، بخش Omni — جمله‌های کوتاه +
   «Keep everything else the same.»
5. **روایت** → `03_audio_plan.md` را به TTS دلخواه بده (یا از من بخواه)؛
   فایل‌ها در `assets/voice/<SHOT_ID>.wav`.
6. **موسیقی** → طبق پلان؛ در `assets/music/track.wav`.
7. **بازگشت به من** → بگو «دارایی‌ها آماده‌ست» تا `assemble.py` را اجرا کنم:
   `python3 <skill>/scripts/assemble.py /home/z/my-project/skills/film-studio/examples/demo-test`

## یادآوری consistency
- بلاک Style در همهٔ پرامپت‌ها ثابت است — تغییرش نکن.
- ویژگی‌های شخصیت verbatim تکرار می‌شوند — paraphrase نکن.
- اگر شاتی جواب نداد: اول دوربین را ساده کن، بعد اکشن، بعد سبک.
