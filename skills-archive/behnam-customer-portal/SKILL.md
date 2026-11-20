# اسکیل دامنهٔ «پرتال مشتری» — چاپ بهنام
## نقش
قانون‌گذار CustomerPortalAccount (اعلان‌ها/هدر/آمار/اکشن‌های سفارش/امنیت حساب)، کل endpointهای نشست مشتری (auth/customer/*)، مرز دادهٔ مشتری (orders/mine و اکشن‌های سنداری)، visibility فایل‌ها و چت زندهٔ مشتری.

## قوانین تخصصی (نمیشکند!)
- نشست مشتری فقط بر پایهٔ شمارهٔ تأییدشده: session.kind='customer' و subjectId=شماره؛ همهٔ endpointهای مشتری اول resolveSession دارند — mine.ts:11، customer-action.ts:29، payment-request.ts:34-37، customer-file.ts:27-30، password.ts:19-22.
- فیلتر سمت سرور (گارد آزمون دارد): GET /api/orders/mine با `WHERE customer_phone = session.subjectId` (functions/api/orders/mine.ts:13-16) — مشتری فقط سفارش‌های خودش؛ هیچ endpoint فهرست سفارش دیگران ندارد. تست: sprint27SecurityWaves.
- مالکیت در هر اقدام: اگر customer_phone ≠ session.subjectId → 403 «این سفارش به حساب شما تعلق ندارد» (payment-request.ts:53-55، customer-file.ts:44-46، customer-action.ts:48-50).
- اقدام‌های مجاز مشتری فقط سه‌تاست: تأیید طرح/درخواست اصلاح (customer-action.ts:39-41 فقط approve_design|request_revision)، ارسال فایل جدید (customer-file.ts)، ارسال رسید پرداخت که تراکنش «pending» می‌سازد و هیچ اثری در مانده ندارد (payment-request.ts) — تأیید و تغییر مانده فقط سنداریِ پرسنل است (payments.ts:64-79: مبلغ ذخیره‌شدهٔ سرور مبناست، نه مبلغ کلاینت).
- visibility فایل‌ها (موج ۲۰): فایل مشتری/ناشناس = session و بدون نشست → 404 (functions/api/uploads/[id].ts:35-38)؛ فایل آپلود پرسنل = public؛ ردیف‌های قدیمی بدون برچسب public می‌مانند تا گالری نشکند. تست: sprint27SecurityWaves س۵.
- چت مشتری فقط کانال خودش (موج ۲۰): کانال قفل به website_live_chat و threadKey قفل به session.subjectId؛ ورودی دستی بی‌اثر (functions/api/chats/message.ts:74-82)؛ پرسنل بدون canViewChat نمی‌تواند پاسخ دهد (خطوط 53-63).
- اعلان‌ها scoping با ID: مشتری فقط ردیف‌های `audience='customer' AND target_phone=subjectId` را می‌خواند/می‌خواند-شده علامت می‌زند (functions/api/notifications.ts:27-34,71-72).
- رمز شخصی: حداقل ۶ کاراکتر؛ تغییر رمز موجود currentPassword می‌خواهد (functions/api/auth/customer/password.ts:27 و ادامه)؛ وضعیت در استور customerHasPassword — ورود دوم با password-login.ts.
- دموی ورود (کد نمایشی OTP) حفظ اجباری کارفرما؛ پیش‌فرض روشن، خاموشی فقط OTP_DEVCODE=off (functions/api/auth/customer/otp.ts:67-76)؛ throttle ارسال مجدد ۶۰ ثانیه/شماره (خطوط 29-36).
- رفرش زندهٔ سبک (ح۶): GET /api/orders/mine چند کیلوبایت برای refreshCustomerOrders است — دانلود مجدد payload عمومی برای پرتال ممنوع (mine.ts:1-2).

## قراردادهای بین‌بخشی (مذاکره با اسکیل‌های دیگر)
- خروجی به behnam-kanban (وضعیت سفارش): payload سفارش (status + interactions) که کانبان جابه‌جا می‌کند همان دادهٔ mine.ts پرتال است؛ هر تغییر وضعیت کارگاه → اعلان مشتری. نشانهٔ شکست: پرتال وضعیت کهنه نشان دهد یا اعلان تغییر مرحله نرسد.
- خروجی به behnam-accounting (رسید→تأیید): رسید مشتری = تراکنش pending در payment-request؛ فقط تأیید پرسنل در payments مانده را کم می‌کند و سند دوبل می‌سازد (دفتر کل). نشانهٔ شکست: ماندهٔ مشتری بدون تأیید پرسنل تغییر کند یا تراکنش pending در تراز بیاید (قانون حسابداری: pending پول نیست).
- خروجی به behnam-crm (ارتباطات): پیام چت مشتری → chat_messages + صندوق مرکزی پرسنل؛ اعلان‌ها target_phone-scoped. نشانهٔ شکست: پیام مشتری در کانال/threadKey دیگری ثبت شود یا به صندوق پرسنل نرسد.
- ورودی از behnam-rbac (scoping): مرز نشست (kind='customer') و برش bootstrap به دادهٔ خود مشتری (customerProfileOwn در useStore). نشانهٔ شکست: endpoint مشتری با نشست پرسنل باز شود یا bootstrap دادهٔ مشتری دیگر را بفرستد.

## چک‌لیست دیباگ
1. گاردها: `rg -n "kind !== 'customer'|customer_phone !== session.subjectId" functions/api` → همهٔ endpointهای سنداری گارد دارند؛ تست Vitest: sprint27SecurityWaves.test.ts (س۲/س۵)، serverAuth.test.ts.
2. پراب بدون نشست: GET /api/orders/mine → 401؛ POST /api/orders/:id/customer-action → 401؛ GET /api/uploads/:id خصوصی → 404؛ POST /api/orders/:id/payment-request → 401.
3. پراب مالکیت: رسید/فایل/اقدام روی سفارشِ شمارهٔ دیگر با نشست مشتری معتبر → 403 (نه 404).
4. پراب OTP: دو درخواست در ۶۰ ثانیه → 429؛ کد ۴ رقمی با TTL ۵ دقیقه (functions/lib/auth.ts OTP_TTL_MS)؛ devCode فقط در mock و تا وقتی OTP_DEVCODE≠off.
5. رفتار اعلان: mark-read با ID مشتریِ دیگر نباید ردیف دیگری را تغییر دهد (notifications.ts:71-72)؛ تست sprint27SecurityWaves س۳/س۴.
6. e2e: e2e/portal.spec.ts — «staff login modal opens from the header and has demo login» و سناریو ویزارد/درفت؛ Vitest: sprint6LiveOrder.test.ts (رفرش زنده)، sprint6Push.test.ts (اعلان مرورگر).

## فایل‌ها
src/components/CustomerPortalAccount.tsx · CustomerLoginModal.tsx · CustomerProfileModal.tsx · CustomerLiveChatWidget.tsx · src/store/useStore.ts (slices مشتری: customerOrders/customerProfileOwn/customerHasPassword) · src/hooks/usePushNotifications.ts · functions/api/orders/{mine,[id]/customer-action,[id]/customer-file,[id]/payment-request,[id]/payments}.ts · functions/api/auth/customer/{otp,verify,password,password-login,profile}.ts · functions/api/{notifications,chats/message,uploads/[id]}.ts

## ممنوع
- **حذف دموی ورود مشتری** (کد نمایشی OTP/کادر دموی ۰۹۱۳۳۹۳۹۹۸۸) — قرارداد کاری کارفرما؛ خاموشی فقط با OTP_DEVCODE=off.
- فیلتر دادهٔ مشتری در کلاینت یا هر endpoint که سفارش/پروفایل/چت مشتری دیگر را بدهد — فیلتر همیشه WHERE سمت سرور.
- اجازهٔ تغییر status/مالی سفارش از مسیر مشتری؛ مشتری فقط pending می‌سازد و تأیید مبلغ با مبلغ ذخیره‌شدهٔ سرور انجام می‌شود.
- سرو کردن فایل visibility=session بدون نشست، یا تغییر visibility فایل‌های خصوصی به public (فقط فایل‌های پرسنلی public است).
- حذف تأیید دومرحله‌ای خروج یا دور زدن throttleهای rate-limit endpointهای مشتری.

## مذاکره (پیوند به ارکستراتور)
- این اسکیل عضو دورهمی دیباگ است؛ قراردادهای ستون فقرات و دفتر مذاکره در behnam-debug-orchestra/SKILL.md نگهداری می‌شود. هر تغییر عرضی این دامنه باید در ماتریس ارکستراتور ثبت و از چرخهٔ behnam-qa-release عبور کند.
