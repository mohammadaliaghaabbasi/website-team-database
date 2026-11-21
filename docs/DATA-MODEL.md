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

## `inspiration_data.json` — صفحات الهام و الگو

تولیدشده توسط `scripts/build_inspiration.py` (خودِ آن فایل منبع ویرایش است). ایده: پیش از شروع هر کار، از گالری‌ها و مراجع تخصصی همان حوزه بازدید کن — نمونه واقعی، الگوی آماده، ترند روز. کلید = نام فارسی نقش (باید دقیقاً با `specialists_data.json` هم‌خوان باشد):

```json
{
  "طراح رابط کاربری": [
    {
      "name": "Land-book — گالری لندینگ واقعی",
      "url": "https://land-book.com/",
      "note": "هزاران لندینگ پیج دستچین با فیلتر صنعت؛ قبل از طراحی حتماً مرور شود"
    }
  ]
}
```

مصرف‌کننده: `build_docx.js` — سکشن «صفحات الهام و الگو (قبل از شروع کار مرور شود)» در هر کارت. اگر نقشی کلید نداشته باشد، سکشن حذف می‌شود (خرابی ایجاد نمی‌کند).

## `practice_data.py` — پلتفرم‌های تمرین (پایتون)

دیکشنری `PRACTICE`: کلید = تخصص فارسی، مقدار = لیست‌های `[نام، آدرس، توضیح]`. مصرف‌کننده: `build_xlsx.py` (شیت «شبیه‌ساز و تمرین»). کلیدها باید با نام تخصص‌های کارت ورد هم‌خوان بمانند تا cross-reference دستی ممکن باشد.

## جریان داده

```
REPOS (gh_collect.py) ─▶ gh_data.json ─┐
              │                        ├─▶ build_xlsx.py ─▶ اکسل ۲۲ شیت
              └▶ sections_data.json ───┘
build_specialists.py ─▶ specialists_data.json ─▶ build_docx.js ─▶ ورد
build_inspiration.py ─▶ inspiration_data.json ─▶ build_docx.js (سکشن الهام هر کارت)
practice_data.py ────────────────────────────▶ build_xlsx.py (شیت ۲۱)
```

## `workflow_data.json` — سیستم برنامه‌ریزی صفر تا صد

```jsonc
{
  "meta":     { "title", "subtitle", "version", "date", "idea" },          // هویت سند
  "phases":   [ { "name", "stages", "motto", "color" } ],                  // ۶ فاز
  "rules":    [ { "title", "text" } ],                                     // ۶ قانون طلایی
  "stages":   [ {                                                          // ۱۹ مرحله
    "id", "title", "titleEn", "phase",
    "goal",                                                                 // چرا این مرحله هست
    "entry":  [ ... ],      // ورودی‌ها — چه می‌گیرد (از خروجی مراحل قبل)
    "activities": [ ... ],  // فعالیت‌ها — چه می‌کند
    "exit":   [ ... ],      // خروجی‌ها — چه تحویل می‌دهد (ورودی مراحل بعد)
    "roles":  [ ... ],      // مسئولان — زیرمجموعه ۶۱ نقش specialists_data.json
    "tools":  [ [repo, desc], ... ],  // ابزارها — زیرمجموعه sections_data.json
    "gate",                 // معیار عبور قابل اندازه‌گیری
    "duration", "parallel", // توالی و موازی‌سازی
    "aiBrief"               // پرامپت شروع وایب‌کدینگ
  } ]
}
```

**قیدهای صحت (در build_workflow.py اعمال می‌شود):** هر نام در `roles` باید در `specialists_data.json` و هر ریپو در `tools` باید در `sections_data.json` موجود باشد — اسکریپت هنگام تولید خطا/گزارش می‌دهد.
**مصرف‌کنندگان:** `WORKFLOW.md`، `scripts/build_workflow_docx.js`، `scripts/workflow_sheet.py` (شیت اکسل).
