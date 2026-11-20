# 📐 مدل داده

ساختار فایل‌های `data/` — منبع حقیقت کل ریپو.

## `gh_data.json` — ستاره‌های واقعی گیت‌هاب

واکشی‌شده توسط `scripts/gh_collect.py` از صفحات عمومی `github.com/{owner}/{repo}` (الگوی استخراج: `<strong>NNNk</strong> stars`).

```json
{
  "owner/repo": {
    "ok": true,              // موفقیت واکشی
    "stars": 252800,         // عدد صحیح ستاره
    "desc_en": "...",        // توضیح انگلیسی از og:description
    "err": null,             // پیام خطا اگر ok=false
    "real": "owner/repo"     // فقط اگر نام ریپو fallback شده باشد
  }
}
```

- کلیدها همان `owner/repo` هستند که در `REPOS` (داخل gh_collect.py) تعریف شده‌اند.
- فیلد `real` وقتی ظاهر می‌شود که نام اصلی ریپو با کلید فرق داشته باشد (مثلاً کلید `motion-dev/motion` ولی ریپوی واقعی `framer/motion`).

## `sections_data.json` — ساختار ۱۹ بخش

تولیدشده از `REPOS` داخل `gh_collect.py` (extractor در تاریخچه ساخت). آرایه دوتایی:

```json
[
  ["01-استراتژی و مدیریت", [
      ["مدیریت پروژه و مستندسازی", [
          ["mermaid-js/mermaid", "دیاگرام‌سازی فلوچارت و معماری (doc-as-code)"],
          ["hoppscotch/hoppscotch", "تست و مستندسازی API، جایگزین متن‌باز Postman"]
      ]]
  ]],
  ["02-تحقیق کاربر", [ ... ]]
]
```

سطح‌ها: `بخش → زیربخش → [ریپو، توضیح فارسی]`. مصرف‌کننده: `build_xlsx.py` (شیت‌های ۱ تا ۱۹ و شیت خلاصه).

## `specialists_data.json` — ۶۱ کارت متخصص

تولیدشده توسط `scripts/build_specialists.py` (خودِ آن فایل منبع ویرایش است). مصرف‌کننده: `build_docx.js`.

```json
[
  {
    "role": "مدیر پروژه دیجیتال",
    "roleEn": "Digital Project Manager",
    "section": "مرحله ۱ — استراتژی و مدیریت",
    "mission": "هماهنگی کل چرخه ساخت سایت از نیازمندی تا انتشار و نگهداشت",
    "skills": ["...", "..."],                 // ۶ رشته
    "stack": [ {"name": "ابزار", "repo": "owner/repo"} ],   // ستاره از gh_data.json
    "practice": [ {"name": "پلتفرم", "url": "example.com", "note": "توضیح"} ],
    "path": ["گام ۱", "گام ۲", "گام ۳", "گام ۴"],
    "interview": "سوال مصاحبه شبیه‌ساز"
  }
]
```

نکته مهم: `stack[].repo` کلید اتصال به `gh_data.json` است — اگر ریپو نبود، ستاره «—» درمی‌آید.

## `practice_data.py` — پلتفرم‌های تمرین (پایتون)

دیکشنری `PRACTICE`: کلید = تخصص فارسی، مقدار = لیست‌های `[نام، آدرس، توضیح]`. مصرف‌کننده: `build_xlsx.py` (شیت «شبیه‌ساز و تمرین»). کلیدها باید با نام تخصص‌های کارت ورد هم‌خوان بمانند تا cross-reference دستی ممکن باشد.

## جریان داده

```
REPOS (gh_collect.py) ─▶ gh_data.json ─┐
              │                        ├─▶ build_xlsx.py ─▶ اکسل ۲۲ شیت
              └▶ sections_data.json ───┘
build_specialists.py ─▶ specialists_data.json ─▶ build_docx.js ─▶ ورد
practice_data.py ────────────────────────────▶ build_xlsx.py (شیت ۲۱)
```
