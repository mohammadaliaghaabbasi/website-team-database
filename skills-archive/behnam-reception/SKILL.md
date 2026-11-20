# اسکیل دامنهٔ «پذیرش و ویزارد سفارش» — چاپ بهنام
## نقش
قانون‌گذار ویزارد ۳ گامی ثبت سفارش (عمومی و ثبت سریع پذیرش در NewOrderModal)، سبد چندقلمی، قیمت‌گذاری «پیش از مالیات»، حالت استعلام، درفت‌محافظ، استخراج مشخصات با AI (functions/api/ai/extract-order-specs.ts) و دسته‌بندی‌های محصول.

## قوانین تخصصی (نمیشکند!)
- ویزارد ۳ گام با ریل کلیک‌پذیر (aria-current)، چیپ‌های خلاصه با پرش به گام مربوطه، استپر تعداد ۱..۱۰۰۰۰ و دکمهٔ ثبت فقط یک‌بار (ب۱) — تست قفل: calculatorWizard.test.ts.
- سبد چندقلمی (Task 48): هر قلم materialId و finishingIds خودش را نگه می‌دارد؛ ویرایش قلم به گام مشخصات برمی‌گردد؛ پاک‌سازی کل سبد دومرحله‌ای و بدون window.confirm (sprint17MultiLine.test.ts)؛ سقف سرور ۲۰ قلم (functions/api/orders/index.ts:73).
- قیمت «پیش از مالیات»: برآورد هر عدد در گام ۲ بدون مالیات (PublicPortal.tsx:1748)؛ موتور واحد سمت کلاینت/سرور src/utils/pricing.ts → functions/lib/pricing.ts (VAT_RATE=0.1، خط 7). سرور همهٔ قیمت‌ها را بازمحاسبه و فیلدهای مالی کلاینتِ ناشناس/مشتری را می‌بُرد (orders/index.ts «B3»)؛ فقط ثبتِ پرسنلی (isStaffSubmission، خطوط 64-67) فیلدهای مالی را نگه می‌دارد.
- حالت استعلام: isQuoteInquiry → inquiryStatus=waiting_for_quote (PublicPortal.tsx:869-870)؛ چرخهٔ وضعیت‌ها waiting_for_quote/quoted/approved_by_customer/rejected در پرونده و بج کانبان (اسکیل کانبان).
- درفت‌محافظ کامل (موج ۲۲): localStorage با کلید behnam_portal_draft_v1 (PublicPortal.tsx:514-565) — دسته، متریال، ابعاد، تعداد، فینیشینگ، کل سبد (portalCart)، هزینهٔ طراحی، اطلاعات تماس و حالت استعلام بعد از رفرش زنده می‌مانند؛ نگارش debounce‌شده و خواندن با تری‌کچ (خط 537 «ignore corrupt draft»).
- پذیرش حضوری (NewOrderModal): بیعانه الزامی است — `prepayment<=0` → خطای «ثبت سفارش بدون بیعانه ممکن نیست — حداقل ۵۰٪» (NewOrderModal.tsx:296-298,1147-1150)؛ status نهایی = prepayment>0 ? payment_approved : draft_pending (خط 368). در ویزارد عمومی سفارش همیشه draft_pending و prepayment:0 صادقانه می‌آید (PublicPortal.tsx:840-855).
- AI استخراج مشخصات: POST /api/ai/extract-order-specs best-effort است — بدون binding یا هر شکلی → {available:false} و فرم دستی تنها مسیر می‌ماند؛ فقط تصویر؛ rate-limit ۱۲/۱۰ دقیقه/IP؛ ابعاد/تعداد با سقف‌های امن (extract-order-specs.ts:1-5,71-76,93-95).
- دستهٔ «تابلوسازی/تخته شاسی» = shasi_craft، هرگز sign_craft (src/types/index.ts:27، WorkshopDevices.tsx:278، defaultData.ts:601,1142؛ تست sprint27UserFixes ی۴ خطوط 60-64). دستهٔ AI هم فقط همین ۸ مقدار معتبر است (VALID_CATEGORIES).
- سفارش عمومی در حوضچهٔ آزاد می‌افتد (assignedDesignerId=undefined؛ preferredDesignerId اختیاری از انتخاب مشتری — PublicPortal.tsx:861-867)؛ برداشتن به نام خودی مجاز، تخصیص/تغییر کارِ دیگری فقط مدیر (functions/api/orders/[id].ts:67-80).
- نقش «پذیرش» (reception) از فرم پرسنل قابل ایجاد است (موج ۲۱، تست sprint27UserFixes ی۱۰) — دسترسی پیش‌فرض: سفارش‌ها، مشتریان و پیام‌رسان‌ها.

## قراردادهای بین‌بخشی (مذاکره با اسکیل‌های دیگر)
- خروجی به behnam-kanban: سفارش نو یا در draft_pending (ویزارد عمومی) یا payment_approved (بیعانهٔ حضوری)؛ gate ورود به in_production فقط با تأیید بیعانه (canMoveForward). نشانهٔ شکست: سفارش بدون بیعانه وارد تولید شود یا سفارش نو در ستون اول دیده نشود.
- خروجی به behnam-accounting: بیعانهٔ ثبت‌شده در NewOrderModal تراکنش اول سفارش می‌شود و فقط واریزِ موفق سند دوبل می‌سازد (pending پول نیست). نشانهٔ شکست: دریافتی نقد/پوز پذیرش بدون اثر در کارکرد مالی/پورسانت یا تراکنش pending در تراز.
- خروجی به behnam-warehouse: اقلام فقط متریالِ تعریف‌شده در تعرفهٔ materials را می‌فرستند (موجودی/آستانهٔ هشدار همان ماده در انبار مدیریت می‌شود)؛ ویزارد متریال نمی‌سازد و مصرف/گردش واقعی از مسیر انبار است. نشانهٔ شکست: قلم با متریال ناشناخته در پرونده/انبار.
- خروجی به behnam-kanban/طراحی (تخصیص): preferredDesignerId → سرور صحتش را وارسی می‌کند؛ وگرنه حوضچهٔ آزاد. claim به نام خودی آزاد است، تغییر طراحِ دیگری فقط مدیر (orders/[id].ts گارد موج ۲۰). نشانهٔ شکست: پرسنل عادی کارِ طراح دیگر را به خودش یا ثالث بگیرد.

## چک‌لیست دیباگ
1. دسته‌ها: `rg -n "sign_craft" src` → فقط منفیِ تست (sprint27UserFixes.test.ts:62)؛ کد واقعی فقط shasi_craft.
2. درفت‌محافظ: `rg -n "behnam_portal_draft_v1|DRAFT_KEY" src/components/PublicPortal.tsx` → سالم؛ e2e «wizard navigates through its 3 steps and preserves contact info» رفرش را می‌آزماید.
3. Vitest دامنه: calculatorWizard.test.ts · sprint17MultiLine.test.ts · sprint8CalcMath.test.ts · pricingTotals.test.ts (مالیات/تخفیف) · sprint6AiUpload.test.ts · sprint27UserFixes.test.ts (shasi_craft/نقش پذیرش).
4. پراب AI: POST /api/ai/extract-order-specs با uploadId غیرتصویری یا بدون env.AI → {ok:true, available:false} — فرم دستی نباید بسته شود؛ uploadId نامعتبر → 422.
5. پراب ثبت سفارش: POST /api/orders بدون نام/تلفن معتبر → 422؛ ۲۱ قلم → 422؛ بیش از ۸ سفارش/ساعت/IP → 429 (orders/index.ts:57-61).
6. بیعانهٔ حضوری: NewOrderModal با prepayment=0 خطای فارسی ۵۰٪ می‌دهد و status پیشنهادی payment_approved می‌سازد (NewOrderModal.tsx:296-298,368).

## فایل‌ها
src/components/PublicPortal.tsx (ویزارد + سبد + درفت) · src/components/NewOrderModal.tsx (ثبت سریع پذیرش/پرسنلی) · src/utils/pricing.ts · src/data/defaultData.ts (تعرفه/دسته‌ها) · src/types/index.ts (دسته‌های معتبر) · functions/api/orders/index.ts · functions/api/ai/extract-order-specs.ts · functions/lib/pricing.ts

## ممنوع
- دور زدن بازمحاسبهٔ سرور: فرستادن فیلد مالی قابل‌اعتماد از کلاینت در مسیر عمومی، یا برگرداندن فیلدهای مالی کلاینت برای ناشناس/مشتری (فقط isStaffSubmission استثناست).
- ثبت سفارش پرسنلی بدون بیعانه یا سست‌کردن gate بیعانهٔ ورود به in_production.
- بازگرداندن sign_craft یا مقدار دستهٔ خارج از فهرست معتبر (کلاینت و VALID_CATEGORIES سرور).
- شکستن درفت‌محافظ: حذف/تغییر کلید behnam_portal_draft_v1، نگهداری جزئی‌تر از سبد+طراحی+استعلام، یا نوشتن مسیرهای دیگر روی آن.
- بستن ثبت سفارش وقتی AI {available:false} می‌دهد — AI هرگز gate مسیر دستی نیست.

## مذاکره (پیوند به ارکستراتور)
- این اسکیل عضو دورهمی دیباگ است؛ قراردادهای ستون فقرات و دفتر مذاکره در behnam-debug-orchestra/SKILL.md نگهداری می‌شود. هر تغییر عرضی این دامنه باید در ماتریس ارکستراتور ثبت و از چرخهٔ behnam-qa-release عبور کند.
