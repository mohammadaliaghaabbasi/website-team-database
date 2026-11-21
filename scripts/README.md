# ⚙️ اسکریپت‌های بازتولید

همه از **ریشه ریپو** اجرا می‌شوند (`python3 scripts/xxx.py`). مسیرها نسبی‌اند؛ نیازی به تغییر ندارید.

| اسکریپت | کار | پیش‌نیاز |
|---|---|---|
| `gh_collect.py` | واکشی ستاره واقعی ریپوها از github.com → `data/gh_data.json` | curl؛ resume-able |
| `build_specialists.py` | تولید `data/specialists_data.json` (کارت متخصص‌ها را همینجا ویرایش/اضافه کنید) | python3 خالص |
| `build_inspiration.py` | تولید `data/inspiration_data.json` (صفحات الهام هر نقش را همینجا ویرایش کنید) | python3 خالص |
| `build_xlsx.py` | ساخت اکسل ۲۲ شیتی → `deliverables/…xlsx` | `pip install openpyxl` |
| `build_docx.js` | ساخت ورد شبیه‌ساز → `deliverables/…docx` | `npm install docx` |
| `check_urls.sh` | اعتبارسنجی همه لینک‌های الهام → `inspiration_url_report.txt` | curl |

## بازتولید کامل (بعد از هر تغییر داده)

```bash
python3 scripts/build_specialists.py   # فقط اگر کارت متخصص عوض شد
python3 scripts/build_inspiration.py   # فقط اگر صفحات الهام عوض شد
python3 scripts/build_xlsx.py
node scripts/build_docx.js             # PDF را با LibreOffice بسازید:
soffice --headless --convert-to pdf deliverables/*.docx --outdir deliverables/
```

راهنمای افزودن ابزار/متخصص/بخش: [`docs/EXTENDING.md`](../docs/EXTENDING.md)
