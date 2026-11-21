# 📦 داده‌ها — منبع حقیقت ریپو

این پوشه تنها جایی است که باید ویرایش کنید تا خروجی‌ها تغییر کنند (به‌جز کارت متخصص که منبعش `scripts/build_specialists.py` است).

| فایل | محتوا | تولیدکننده | مصرف‌کننده |
|---|---|---|---|
| `gh_data.json` | ستاره واقعی + توضیح ۱۸۲ ریپو | `scripts/gh_collect.py` | build_xlsx، build_docx |
| `sections_data.json` | ساختار ۱۹ بخش × زیربخش × ابزار | extractor (از REPOS) | build_xlsx |
| `specialists_data.json` | ۶۱ کارت متخصص شبیه‌ساز | `scripts/build_specialists.py` | build_docx |
| `practice_data.py` | ۲۱ تخصص × ۸۲ پلتفرم تمرین | دستی | build_xlsx (شیت تمرین) |
| `inspiration_data.json` | ۶۱ نقش × ۲۴۷ صفحه الهام و الگو | `scripts/build_inspiration.py` | build_docx (سکشن الهام هر کارت) |

ساختار دقیق فیلدها: [`docs/DATA-MODEL.md`](../docs/DATA-MODEL.md)
⚠️ فایل‌های `deliverables/` را هرگز دستی ویرایش نکنید — بازتولید می‌شوند و تغییرات از بین می‌رود.
