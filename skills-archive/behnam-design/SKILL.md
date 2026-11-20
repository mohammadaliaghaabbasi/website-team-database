# اسکیل دامنهٔ «طراحی و گرافیک» — چاپ بهنام
## نقش
قانون‌گذار حوضچهٔ آزاد و برداشتن کار (claim)، تخصیص/تغییر طراح، فیلتر طراح کانبان، چرخهٔ تایید طرح مشتری، فایل‌های سفارش و visibility آپلودها، آلبوم عمومی نمونه‌کار و هزینهٔ طراحی در ویزارد. Endpointهای تحت قانون: PATCH /api/orders/:id (گارد تخصیص)، /api/orders/:id/customer-file، /api/uploads، collections عمومی (portfolio).

## قوانین تخصصی (نمیشکند!)
- حوضچهٔ آزاد = سفارشِ بدون assignedDesignerId و غیرتحویل‌شده (isInOpenPool) — برای همهٔ پرسنل دیده می‌شود؛ موج ۱۲ آن را فیلتر می‌کرد و حوضچه خالی می‌شد (باگ رفع‌شده) — scoping.ts سطر ۵۴-۷۳؛ آینهٔ سرور permissions.ts سطر ۱۶۵-۱۷۳؛ گارد آزمون sprint24Pool.
- دکمهٔ دائمی «حوضچهٔ آزاد — کارهای بدون طراح» با شمارندهٔ زنده در خود کانبان است؛ claim «برداشتن کار به نام من» همیشه مجاز است: store.claimOrder طراح را به نام خودی می‌گذارد، claimedAt را ثبت و یادداشت «کار توسط طراح «X» تحویل گرفته شد.» در تاریخچه می‌نویسد (KanbanBoard.tsx سطر ۳۴۲-۴۰۱ و ۵۳۱-۵۳۹؛ useStore.ts سطر ۸۸۰-۸۹۱).
- تخصیص مجدد کارِ دیگری فقط مدیر/حسابدار (گارد سرور موج ۲۰): تغییر assignedDesignerId به کسی غیر از خودِ فراخوان، فقط برای دارندهٔ canViewPerformance || canViewAccounting || canManageStaff مجاز است؛ وگرنه 403 «تغییر طراح سفارش فقط توسط مدیر انجام می‌شود.» — از آن رو که گارد فقط وقتی طراحِ قبلی وجود داشته باشد می‌بندد، برداشتنِ کارِ بی‌طراح (claim) همیشه باز می‌ماند (functions/api/orders/[id].ts سطر ۶۷-۸۰؛ گارد آزمون س۹ sprint27SecurityWaves).
- هر PATCH سفارش با audit changedKeys ثبت می‌شود (کدام فیلدها واقعاً عوض شدند) و ویرایش outdated با 409 conflict رد می‌شود (orders/[id].ts سطر ۴۷-۵۹ و ۱۳۳-۱۵۱).
- فیلتر طراح کانبان: همه / بدون طراح (آزاد در حوضچه) / هر طراح یا admin — فیلترِ unassigned دقیقاً یعنی حوضچه (KanbanBoard.tsx سطر ۱۲۵-۱۳۰ و ۲۲۳-۲۳۷).
- چرخهٔ تایید طرح چهارحالته: designApprovalStatus = not_sent | waiting_customer_approval | approved_by_customer | revision_requested؛ هم پروندهٔ پرسنل و هم پرتال مشتری این وضعیت را کنترل و هر دو سمت سرور ذخیره می‌کنند (types/index.ts سطر ۱۶۸؛ OrderDetailsModal.tsx سطر ۴۴۳-۴۵۳؛ CustomerPortalAccount.tsx سطر ۷۷۰-۸۰۵).
- فایل جدید مشتری فقط روی سفارشِ خودش: POST /api/orders/:id/customer-file نشست مشتری می‌خواهد و customer_phone باید با صاحب سفارش یکی باشد (403 در غیر این صورت)؛ سقف ۱۰ ارسال/ساعت/آی‌پی؛ فایل قبلی در interactions نسخه‌بندی می‌شود و fileStatus به 'uploaded' برمی‌گردد (functions/api/orders/[id]/customer-file.ts سطر ۲۷-۶۸).
- visibility فایل‌ها (موج ۲۰): آپلودِ پرسنل = 'public'، آپلود مشتری/ناشناس = 'session'؛ فایلِ session بدون نشستِ همان ۴۰۴ می‌خورد — هرگز آن را به public تبدیل نکن (functions/api/uploads/index.ts سطر ۹۳؛ functions/api/uploads/[id].ts سطر ۳۵-۴۶؛ گارد آزمون س۵).
- آلبوم عمومی نمونه‌کار (PublicShowcase): چیدمان کد است و محتوا فقط از پنل مدیریت می‌آید (نوشتنِ portfolio/server-side با canManageAdmin)؛ قاعدهٔ featuredSubset: آیتم‌های featured اول، در نبودِ ستاره، جدیدترین‌ها تا سقف — بخش عمومی هرگز خالی از باکس نمی‌افتد (PublicShowcase.tsx سطر ۷۰-۸۰؛ permissions.ts COLLECTION_WRITE_PERMISSION سطر ۱۱۶).
- ادعای واترمارک دروغین حذف شد (موج ۲۱): فیلد watermarkedPreviewUrl در تایپ هست اما پرتال هیچ ادعای «واترمارک ضدکپی» نمی‌نویسد؛ بازگرداندن این ادعا بدون پیاده‌سازی واقعی ممنوع است (گارد ی۶ sprint27UserFixes روی PublicPortal.tsx).
- هزینهٔ طراحی در ویزاردِ پذیرش: گام ثبت «هزینه طراحی درخواستی (تومان — اختیاری)» دارد و درفت‌محافظ موج ۲۲ سبد چندقلمی + هزینهٔ طراحی + حالت استعلام را از رفرش نجات می‌دهد (PublicPortal.tsx سطر ۵۳۱، ۱۹۱۹، ۲۱۶۰-۲۱۶۳؛ NewOrderModal.tsx سطر ۸۶۴؛ e2e portal.spec.ts سناریوی درفت).

## قراردادهای بین‌بخشی (مذاکره با اسکیل‌های دیگر)
- ورودی از behnam-kanban: سفارش‌های حوضچه (isInOpenPool) + مجوز canEditOrdersFor برای claim/تخصیص؛ گارد سرور PATCH مرز نهایی است — نشانهٔ شکست قرارداد: claim پرسنل 403 می‌خورد یا دکمهٔ برداشتن برای تماشاچی‌ها نشان داده می‌شود.
- خروجی به behnam-accounting/پذیرش: هزینهٔ طراحی انتخابیِ گام ثبت به جمع پیش‌فاکتور و درفت می‌رود و باید «یک مبلغ در همه نماها» بماند (PublicPortal.tsx سطر ۲۱۶۰-۲۱۶۳؛ calculatorWizard.test سطر ۸۸) — نشانهٔ شکست: مبلغ طراحی از جمع کل می‌افتد یا درفت بعد از رفرش خالی است.
- خروجی به behnam-crm/پرتال مشتری: فایل/پیش‌نمایش طرح با visibility صحیح (پرسنل=public، مشتری/ناشناس=session) + وضعیت تایید طرح و اعلان status_change روی هر گذار (uploads/index.ts سطر ۹۳؛ CustomerPortalAccount.tsx) — نشانهٔ شکست: مشتری فایلِ سفارش دیگران را می‌بیند یا فایل session بدون نشست 200 برمی‌گرداند.
- خروجی به behnam-rbac: تغییر طراح و هر ویرایش سفارش با changedKeys در لاگ حسابرسی (F17) ثبت می‌شود (orders/[id].ts سطر ۱۴۱-۱۵۰) — نشانهٔ شکست: جابه‌جایی کار بین طراحان بدون ردپای حسابرسی.

## چک‌لیست دیباگ
- `rg -n "تغییر طراح سفارش فقط توسط مدیر" functions/api/orders/[id].ts` → گارد موج ۲۰؛ پراب: PATCH سفارشِ دارای طراح با assignedDesignerId دیگر توسط پرسنل معمولی → 403، توسط مدیر → 200.
- `rg -n "isInOpenPool|حوضچهٔ آزاد" src/lib/scoping.ts src/components/KanbanBoard.tsx functions/lib/permissions.ts` → تعریف و دکمهٔ دائمی حوضچه.
- `rg -n "session\?\?\.kind === 'staff'|row.visibility === 'session'" functions/api/uploads/index.ts functions/api/uploads/[id].ts` → گاردهای visibility (س۵)؛ پراب: GET /api/uploads/:id فایلِ session بدون کوکی → 404.
- `rg -n "واترمارک ضدکپی" src/components/PublicPortal.tsx` → باید بدون نتیجه باشد (ی۶).
- تست‌ها: Vitest `sprint27SecurityWaves` (س۵/س۹)، `sprint24Pool`، `sprint25Hardening` (claim async)، `calculatorWizard`، `sprint15PortfolioShop`؛ e2e: `e2e/portal.spec.ts` (درفت‌محافظ + رهگیری).
- پراب فایل مشتری: POST /api/orders/:id/customer-file بدون نشست → 401؛ با نشستِ مشتریِ دیگری → 403؛ بیش از ۱۰ بار در ساعت → 429.
- رفتار مورد انتظار: برداشتن کار به نام خودی بدون خطا؛ حوضچه پس از claim بلافاصله از فهرست آزاد خارج شود و بج طراح روی کارت بنشیند.

## فایل‌ها
src/components/KanbanBoard.tsx · OrderDetailsModal.tsx · PublicShowcase.tsx · PublicPortal.tsx (ویزارد/درفت) · NewOrderModal.tsx · CustomerPortalAccount.tsx · src/lib/scoping.ts · src/store/useStore.ts (claimOrder/reassignOrder) · functions/api/orders/[id].ts · functions/api/orders/[id]/customer-file.ts · functions/api/uploads/index.ts · functions/api/uploads/[id].ts · functions/lib/permissions.ts

## ممنوع
- حذف دموی ورود پرسنل (کد نمایشی دومرحله‌ای functions/api/auth/login.ts سطر ۸۰) و دموی OTP مشتری با کلید خاموشی OTP_DEVCODE=off (functions/api/auth/customer/otp.ts سطر ۷۱) — حفظ اجباریِ قرارداد کاری کارفرما.
- دورزدن گارد تخصیص مجدد (سِم در PATCH /api/orders/:id) یا سست کردن شرط prevDesigner به‌نحوی که تغییر کارِ دیگران برای غیرمدیر باز شود.
- تبدیل فایل session مشتری به public؛ حذف وارسی مالکیت در customer-file؛ نمایش دکمهٔ برداشتن/ویرایش به پرسنلِ بدون canEditOrders.
- حذف قاعدهٔ featuredSubset یا اتصال آلبوم عمومی به دادهٔ دستیِ کد به‌جای collections پنل؛ بازگرداندن ادعای واترمارک بدون پیاده‌سازی واقعی.
- حذف درفت‌محافظ (سبد چندقلمی + هزینهٔ طراحی + حالت استعلام) از گام ثبت ویزارد.

## مذاکره (پیوند به ارکستراتور)
- این اسکیل عضو دورهمی دیباگ است؛ قراردادهای ستون فقرات و دفتر مذاکره در behnam-debug-orchestra/SKILL.md نگهداری می‌شود. هر تغییر عرضی این دامنه باید در ماتریس ارکستراتور ثبت و از چرخهٔ behnam-qa-release عبور کند.
