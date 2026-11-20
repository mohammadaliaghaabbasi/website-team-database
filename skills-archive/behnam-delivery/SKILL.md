# اسکیل دامنهٔ «تحویل و پیک» — چاپ بهنام
## نقش
قانون‌گذار دو ستون انتهایی کانبان (ready_delivery → delivered)، تقویم وعدهٔ تحویل، وظایف نقش delivery (پیک/صحافی و تحویل)، رهگیری عمومی ناشناس و دادهٔ تماس/آدرس پیک. Endpointهای تحت قانون: /api/track، PATCH /api/orders/:id (گذار وضعیت)، /api/attendance (کارکرد پیک).

## قوانین تخصصی (نمیشکند!)
- چرخهٔ تحویل: ready_delivery («۵. آماده تحویل / ارسال») → delivered («۶. تحویل شده و تسویه»)؛ گذار با درگ کانبان یا دکمهٔ «تحویل شد» صف اقدام انجام می‌شود (KanbanBoard.tsx KANBAN_STAGES سطر ۵۵-۶۲؛ ActionQueueToday.tsx سطر ۱۸۲-۲۰۰).
- گذار به ready_delivery خودکار پیامک می‌فرستد اگر smsConfig.isActive و autoSendOnReadyDelivery فعال باشد (قالب مدیر با trigger on_ready_delivery) و هم‌زمان اعلان درون‌اپ مشتری با notify می‌سازد (functions/api/orders/[id].ts سطر ۹۵-۱۳۰).
- وضعیت delivered سفارش را از همهٔ نماهای جاری بیرون می‌برد: تعریف حوضچهٔ آزاد !assignedDesignerId && status !== 'delivered' (scoping.ts isInOpenPool سطر ۶۰-۶۱؛ آینهٔ سرور permissions.ts سطر ۱۷۱-۱۷۳)، تقویم وعده سفارش‌های تحویل‌شده را نمی‌نشاند (DeliveryPromiseCalendar.tsx سطر ۱۰۰) و isOverdue برای delivered همیشه false است (KanbanBoard.tsx سطر ۱۶۳-۱۶۶).
- تقویم وعدهٔ تحویل فقط روی dueDate واقعی ISO می‌نشیند (F12)؛ وعده‌های متنی «امروز/فردا/پس‌فردا/پایان هفته» با resolvePromiseDayKey صادقانه روی روز خودشان می‌نشینند (موج ۱۲) و فقط «هماهنگی تلفنی» در سطل «بدون تاریخ دقیق» می‌ماند؛ ظرفیت روز ۶+ = پر (DeliveryPromiseCalendar.tsx سطر ۷-۱۳ و ۹۶-۱۲۴؛ lib/dueDate).
- رهگیری عمومی ناشناس (track.ts): فقط GET با کد NP-\d{4,8}؛ rate limit ۳۰ درخواست/۱۰ دقیقه/آی‌پی؛ خروجی فقط فیلدهای امن (وضعیت، شاخص مرحله، dueTime، deliveryType، fileStatus، تعداد اقلام، تایم‌لاین) — هرگز تلفن، مبالغ، اقلام یا یادداشت داخلی (functions/api/track.ts سطر ۱۴-۶۴).
- تایم‌لاین رهگیری فقط از ردیف‌های «تغییر وضعیت مرحله به:» در interactions سفارش ساخته می‌شود (track.ts سطر ۳۶-۴۵) — هر تغییر وضعیت باید interaction با همین الگو ثبت کند وگرنه مشتری پیشرفت را نمی‌بیند.
- نقش delivery (پیک — برچسب «واحد صحافی و تحویل»): پیش‌فرض سرور canViewOrders+canEditOrders+canViewCustomers (functions/lib/permissions.ts سطر ۶۸-۷۲)؛ اما فرم پرسنلِ کلاینت برای پیک canEditOrders=false ذخیره می‌کند (AdminControlPanel.tsx سطر ۶۰۷) و آینهٔ کلاینت canEditOrdersFor برای نقش delivery فقط مجوز صریح true را می‌پذیرد (scoping.ts سطر ۲۵-۳۲) — پس پیکِ تازه‌ساخت تماشاچیِ ویرایش است تا مدیر صریحاً مجوزش را باز کند.
- آدرس/تماس برای پیک: phone + address روی CustomerInfo سفارش (types/index.ts سطر ۴۹-۵۷) و نوع تحویل فقط یکی از سه مقدار in_person_pickup | courier_snapp | post_tipax است که سرور وارسی می‌کند (types سطر ۱۶۳؛ functions/api/orders/index.ts سطر ۱۵۹-۱۶۰)؛ تلفن مشتری روی کارت کانبان برای تماس پیش از ارسال نمایان است (KanbanBoard.tsx سطر ۵۰۹).

## قراردادهای بین‌بخشی (مذاکره با اسکیل‌های دیگر)
- ورودی از behnam-kanban: سفارش‌های رسیده به ready_delivery + گارد بیعانهٔ canMoveForward (ورود به in_production بدون بیعانه مسدود است — تحویل پشت سرِ آن) — نشانهٔ شکست قرارداد: باجهٔ تحویل خالی می‌ماند یا سفارشِ بی‌بیعانه در چرخه ظاهر می‌شود.
- خروجی به behnam-crm/پرتال مشتری: اعلان status_change روی هر گذار (audience=customer، targetPhone مشتری) + وضعیت امن برای رهگیری عمومی /api/track (orders/[id].ts سطر ۹۷-۱۰۴؛ track.ts) — نشانهٔ شکست: مشتری تغییر وضعیت را در پرتال نمی‌بیند یا رهگیری 422/429 برمی‌گرداند.
- خروجی به behnam-hr: کارکرد پیک از حضور (clockIn/clockOut با تفکیک حضوری/دورکاری در /api/attendance) و شیفت‌های باز «حاضرین در کارگاه» داشبورد عملیات + عملکرد پرسنل (StaffPerformanceManagerDashboard با attendanceLogs و فیلتر زمانی) — نشانهٔ شکست: داشبورد «۰ شیفت باز» با وجود پیک حاضر، یا غیبت پیک در دفتر حضور.
- ورودی از behnam-production: نشانهٔ «آماده تحویل» داشبورد عملیات همان منبع سفارش‌ها را می‌خواند؛ هر تغییری در وضعیت‌ها باید هر دو نما را با همگام‌سازی ۶۰ ثانیه‌ای به‌روز کند (OpsDashboard.tsx readyNow) — نشانهٔ شکست: عدد باجه در صف اقدام و داشبورد اختلاف می‌گیرد.

## چک‌لیست دیباگ
- `rg -n "ready_delivery|delivered" functions/api/orders/\[id\].ts` → پیامک خودکار + notify روی گذار؛ بدون کانفیگ پیامک، ارسال بی‌صدا رد می‌شود (mock).
- `rg -n "isInOpenPool|status !== 'delivered'" src/lib/scoping.ts functions/lib/permissions.ts` → کلاینت و سرور باید یک تعریف داشته باشند.
- `rg -n "hitRateLimit|NP-" functions/api/track.ts` → گارد نرخ و الگوی کد؛ تست e2e «رهگیری کد ناموجود» باید found:false ببیند.
- `rg -n "canEditOrdersFor|role === 'delivery'" src/lib/scoping.ts src/components/AdminControlPanel.tsx` → وضعیت مجوز ویرایش پیک.
- تست‌ها: Vitest `sprint27SecurityWaves` (س۸ دموی ورود)، `sprint25Hardening`، `sprint6LiveOrder` (api.track)؛ e2e: `e2e/portal.spec.ts` سناریوی رهگیری.
- پراب سرور: GET /api/track?code=NP-999999 → {found:false}؛ GET /api/track?code=abc → 422؛ ۳۱ بار پشت‌سرهم → 429؛ GET /api/track برای سفارشِ تحویل‌شده → وضعیت delivered با شاخص آخر.
- رفتار مورد انتظار: پس از «تحویل شد»، سفارش از حوضچه/تقویم/دیرکردها حذف و در سابقهٔ پرتال مشتری ثبت شود.

## فایل‌ها
src/components/KanbanBoard.tsx · ActionQueueToday.tsx · DeliveryPromiseCalendar.tsx · src/lib/dueDate.ts · src/lib/scoping.ts · StaffPerformanceManagerDashboard.tsx · functions/api/track.ts · functions/api/orders/[id].ts · functions/api/orders/index.ts · functions/api/attendance/clock.ts · src/types/index.ts (deliveryType/CustomerInfo)

## ممنوع
- حذف دموی ورود پرسنل (کد نمایشی دومرحله‌ای functions/api/auth/login.ts سطر ۸۰) و دموی OTP مشتری با کلید خاموشی OTP_DEVCODE=off (functions/api/auth/customer/otp.ts سطر ۷۱) — حفظ اجباریِ قرارداد کاری کارفرما.
- لو دادن فیلد غیرامن در /api/track (تلفن/مبلغ/اقلام/یادداشت) یا بالا بردن سقف rate limit برای «راحتی».
- نشاندن سفارش تحویل‌شده در حوضچه/تقویم یا احیای isOverdue برای delivered.
- افزودن مقدار چهارم deliveryType بدون وارسی سرور در orders/index.ts؛ حذف پیامک/اعلان خودکار ready_delivery.
- دادن دسترسی ویرایش/حسابداری به نقش پیک به‌صورت پیش‌فرض — فقط مجوز صریح توسط مدیر.

## مذاکره (پیوند به ارکستراتور)
- این اسکیل عضو دورهمی دیباگ است؛ قراردادهای ستون فقرات و دفتر مذاکره در behnam-debug-orchestra/SKILL.md نگهداری می‌شود. هر تغییر عرضی این دامنه باید در ماتریس ارکستراتور ثبت و از چرخهٔ behnam-qa-release عبور کند.
