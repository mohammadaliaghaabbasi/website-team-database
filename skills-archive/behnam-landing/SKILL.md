# اسکیل دامنهٔ «صفحهٔ عمومی و محتوا» — چاپ بهنام
## نقش
قانون‌گذار پرتال عمومی (PublicPortal + PublicShowcase با ۱۲ سکشن)، ویزارد عمومی قیمت، رهگیری زندهٔ ناشناس (functions/api/track.ts)، صفحات اعتماد (اینماد/قوانین)، محتوای CMS (siteContent + SiteContentEditor) و مرز نشست مشتری در CustomerLoginModal.

## قوانین تخصصی (نمیشکند!)
- تک‌منبع ۱۲ بخش صفحه: PUBLIC_SECTIONS در src/components/SectionDotsNav.tsx:23-36؛ منوی موبایل نوار بالا از همان می‌خواند (src/components/Navbar.tsx:42,774) — هیچ مقصدی بیرون از این فهرست نیست (تست sprint22DataFlow.test.ts:49-62).
- رهگیری ناشناس فقط فیلدهای امن: functions/api/track.ts فقط مرحله/موعد/timeline را می‌دهد (بدون تلفن، مبلغ، اقلام، یادداشت داخلی)؛ rate-limit ۳۰ جست‌وجو/۱۰ دقیقه/IP (خط 15)؛ الگوی کد: `NP-\d{4,8}` **یا** `ORD-\d{4}-\d{4}` (M3 نشست ۲ — جست‌وجوی ORD روی ستون order_number با باکت مستقل سخت‌گیرانهٔ trackord ۱۲/۱۰دقیقه چون ترتیبی و شمارش‌پذیرتر است)؛ کد ناموجود = found:false نه خطا. fallback دمو/آفلاین کلاینت (PublicPortal.tsx:932-939) و دیپ‌لینک hash حفظ شده‌اند.
- پیش‌فاکتور «پیش از مالیات»: برآورد هر عدد در گام ۲ بدون مالیات است (PublicPortal.tsx:1748)؛ VAT فقط ۱۰٪ در جمع نهایی از موتور مشترک functions/lib/pricing.ts:7 و بیعانهٔ پیشنهادی ۵۰٪ (PublicPortal.tsx:636-638). سرور همهٔ قیمت‌ها را بازمحاسبه و فیلدهای مالی کلاینت را می‌بُرد (functions/api/orders/index.ts «B3»).
- اینماد وصل به CMS (موج ۲۱): TrustLinksRow با content.legal.enamadUrl لینک واقعی می‌شود و تا آن روز صادقانه «در حال دریافت» است (src/components/portal/TrustLinksRow.tsx:55-75)؛ LegalPagesOverlay سه صفحهٔ قانون/حریم/درباره را از legal.* می‌خواند (LegalPagesOverlay.tsx:35-36، سقف‌ها در functions/lib/contentLimits.ts:37).
- واترمارک واقعی فقط در پروندهٔ پرسنل: applyBehnamWatermark (src/utils/watermark.ts) و آپلود سمت سرور در src/components/OrderDetailsModal.tsx:131-159؛ ادعای «واترمارک ضدکپی» روی پیش‌نمایش فایل مشتری در PublicPortal حذف شد (موج ۲۱، تست sprint27UserFixes.test.ts:73-75) — ادعا بدون فناوری برنمی‌گردد.
- سه subtitle بی‌اثر steps/calculator/clients از SiteContentEditor حذف شدند (موج ۲۱؛ SiteContentEditor.tsx:266-268,297,324؛ تست sprint27UserFixes.test.ts:66-71) — ورودی فریبندهٔ CMS دیگر برنمی‌گردد.
- دموی ورود مشتری = حفظ اجباری (قرارداد کارفرما): کادر «بازدید نمونه» با شمارهٔ 09133939988 و دکمهٔ پرکردن شماره (CustomerLoginModal.tsx:180-192) + کد نمایشی OTP داخل details بسته (خطوط 318-328)؛ خاموشی سراسری فقط با env OTP_DEVCODE=off و پیش‌فرض روشن (functions/api/auth/customer/otp.ts:67-76، تست sprint27SecurityWaves س۸).
- نوشتن CMS فقط با canManageAdmin (functions/lib/permissions.ts:114) و با سقف متنی contentLimits؛ هر ذخیره audit-logged (functions/api/collections/[name].ts).
- سفارش عمومی صادقانه ثبت می‌شود: status=draft_pending، بدون تخصیص (حوضچهٔ آزاد)، prepayment:0 و هیچ تراکنش ساختگی کلاینتی (PublicPortal.tsx:840-870).

## قراردادهای بین‌بخشی (مذاکره با اسکیل‌های دیگر)
- ورودی از behnam-rbac (مرز نشست مشتری): verify OTP/رمز → session kind='customer' → view customer_account؛ طبق قانون موج ۱۸ سایت همیشه با صفحهٔ اول عمومی باز می‌شود حتی با نشست پرسنل. نشانهٔ شکست: باز شدن سایت روی پنل پرسنل، یا نشت نشست مشتری به ERP.
- ورودی از behnam-crm/مدیریت (CMS→لندینگ): کلید siteContent از collections → رندر PublicPortal؛ کلیدهای حذف‌شده (سه subtitle) نباید دوباره رندر/ادیت شوند. نشانهٔ شکست: تغییر متن در پنل مدیریت روی صفحه اعمال نشود یا کلید مرده دوباره در ادیتور ظاهر شود.
- خروجی به behnam-reception (پذیرش): سفارش ویزارد → POST /api/orders با status=draft_pending و اقلام sanitize شده → ستون «ثبت و بررسی طراح» کانبان. نشانهٔ شکست: سفارش نو در کانبان دیده نشود یا قیمت سرور با پیش‌فاکتور کلاینت نخواند (ناهماهنگی موتور pricing).
- خروجی به behnam-customer-portal: مودال ورود مشتری توکن/نشست می‌سازد و CustomerPortalAccount را باز می‌کند (requestCustomerOtp/verifyCustomerOtp در store). نشانهٔ شکست: ورود موفق ولی پرتال مشتری دادهٔ خودش را نگیرد (refreshCustomerSlice خالی).

## چک‌لیست دیباگ
1. گاردهای محتوا: `rg -n "PUBLIC_SECTIONS" src/components` → فقط SectionDotsNav تعریف و Navbar مصرف؛ تست Vitest: sprint22DataFlow.test.ts، siteContent.test.ts، contentContracts.test.ts.
2. ادعای واترمارک: `rg -n "واترمارک ضدکپی" src/components/PublicPortal.tsx` → باید خالی باشد؛ واترمارک واقعی فقط در OrderDetailsModal (`rg -n "applyBehnamWatermark" src/components`).
3. سه subtitle: `rg -n "draft.(calculator|steps|clients).subtitle" src/components/SiteContentEditor.tsx` → خالی (تست sprint27UserFixes ی۵).
4. پراب رهگیری: GET /api/track?code=NP-000000 → {"found":false}؛ GET /api/track?code=bad → 422؛ تکرار >۳۰ بار → 429. e2e: «tracking section is interactive and rejects unknown codes gracefully».
5. پراب دموی ورود: POST /api/auth/customer/otp شمارهٔ 09133939988 → devCode در پاسخ (تا وقتی OTP_DEVCODE=off نیست).
6. e2e لندینگ: e2e/portal.spec.ts — لندینگ/محاسبه‌گر/خدمات/ویزارد+رفرش درفت/مودال پرسنل/رهگیری (۶ سناریو). بعد از هر تغییر CMS: بامپ نسخهٔ SW مطابق الگوی موج‌ها تا کش نسخه‌دار بروز شود.

## فایل‌ها
src/components/PublicPortal.tsx · PublicShowcase.tsx · SectionDotsNav.tsx · Navbar.tsx · portal/TrustLinksRow.tsx · LegalPagesOverlay.tsx · CustomerLoginModal.tsx · SiteContentEditor.tsx · admin/{PortfolioManager,OffersManager,ClientsManager,TeamManager,SocialLinksManager}.tsx · src/data/{siteContent,siteShowcase}.ts · src/utils/watermark.ts · functions/api/track.ts · functions/api/collections/[name].ts · functions/lib/{contentLimits,pricing}.ts

## ممنوع
- **حذف دموی ورود مشتری** (کادر ۰۹۱۳۳۹۳۹۹۸۸ یا کد نمایشی OTP) — خط قرمز صریح کارفرما؛ تنها مسیر خاموشی OTP_DEVCODE=off است.
- بازگرداندن ادعای واترمارک بدون applyBehnamWatermark واقعی، یا افزودن ورودی CMS بی‌اثر (سه subtitle و هر کلید رندرنشدنی).
- غنی‌کردن خروجی رهگیری ناشناس فراتر از فیلدهای امن track.ts (تلفن/مبلغ/اقلام/یادداشت = نشت داده).
- تغییر ترتیب/شناسهٔ ۱۲ سکشن PUBLIC_SECTIONS بدون همگام‌سازی CMS و تست‌ها؛ ساخت تراکنش پرداخت ساختگی در کلاینت (فقط مسیرهای صادقانهٔ رسید/درگاه نمایشی در نقاط واقعی پرداخت).

## مذاکره (پیوند به ارکستراتور)
- این اسکیل عضو دورهمی دیباگ است؛ قراردادهای ستون فقرات و دفتر مذاکره در behnam-debug-orchestra/SKILL.md نگهداری می‌شود. هر تغییر عرضی این دامنه باید در ماتریس ارکستراتور ثبت و از چرخهٔ behnam-qa-release عبور کند.
