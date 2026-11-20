# Examples — پروژه‌های نمونه

## demo-test — «سنگ و رود» (تست کامل خط تولید)

پروژه‌ی کوچک ۳-شاته (۲۸ ثانیه) برای اعتبارسنجی کل خط تولید:

- **mode:** hybrid | **pipeline:** documentary | **resolution:** 720p 16:9
- شات S01 = کلیپ ویدیویی (شبیه‌سازی خروجی Veo: mp4 با صدای خودش، duck زیر روایت)
- شات‌های S02/S03 = تصویر + Ken Burns (pan-right / zoom-in)
- روایت EN + زیرنویس فارسی RTL + موسیقی بستر + عنوان روی شات اول + تیتراژ ۵ نقشی
- گذارها: crossfade ×2 + fade-black آخر → تیتراژ

اجرای بازتولید کامل:

```bash
SKILL=/home/z/my-project/skills/film-studio
E=$SKILL/examples/demo-test

python3 $SKILL/scripts/init_project.py demo-test --mode hybrid \
        --pipeline documentary --title "THE STONE AND THE RIVER" --dir examples
# screenplay.json را در artifacts/ بگذار (الگو: همین مثال)
python3 $SKILL/scripts/build_package.py $E            # پکیج پرامپت + timeline
python3 $SKILL/scripts/make_test_assets.py $E         # دارایی تستی (جایگزین: دارایی واقعی)
python3 $SKILL/scripts/assemble.py $E                 # تدوین → output/final.mp4
python3 $SKILL/scripts/qc_check.py $E                 # QC → artifacts/qc_report.json
```

نتیجه‌ی تست‌شده: `output/final.mp4` — ۲۷٫۷s، h264/aac، QC=PASS،
زیرنویس فارسی با z-ai vision تأیید شد (حروف متصل، RTL، خوانا).

## ساختار هر پروژه

```
project.json + artifacts/ + production_package/ + assets/{clips,images,voice,music} + work/ + output/
```

اسکیمای screenplay در `../references/screenplay-schema.md`.
