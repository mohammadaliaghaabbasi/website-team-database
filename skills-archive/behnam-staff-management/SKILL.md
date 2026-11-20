# اسکیل دامنهٔ «مدیریت پرسنل» — چاپ بهنام
## نقش
قانون‌گذار خوشهٔ «سازمان و امنیت» در پنل مدیریت: زیرتب «پرسنل و کلمات عبور» (ایجاد/حذف پرسنل، نقش‌ها، ماتریس دسترسی)، مودال حقوق و پورسانت، پروفایل خودی پرسنل، ریست رمز مدیرِ، و لاگ حسابرسی (F17)..endpointهای این دامنه: PUT /api/collections/staff، /api/auth/admin-reset-password، /api/audit و برش staff در /api/bootstrap.

## قوانین تخصصی (نمیشکند!)
- دروازهٔ کلاینت: باز شدن پنل مدیریت فقط با isAdmin || canManageAdmin || canManagePricing || canManageStaff (Navbar.tsx:137)؛ تب «عملکرد و پورسانت» فقط با canViewPerformance === true (Navbar.tsx:132). ماتریس ۶ نقش (admin/designer/operator/accountant/delivery/reception) × ۱۱ مجوز در functions/lib/permissions.ts — ترتیب اعمال: پیش‌فرض نقش ← سطوح ذخیره‌شدهٔ ماتریس ← نقش admin همیشه کامل (stored override نمی‌تواند مدیر را از هیچ بخشی قفل کند — permissions.ts:92-94).
- ایجاد پرسنل: فرم «تعریف پرسنل جدید» شش نقش دارد و «پذیرش و ثبت سفارش حضوری» (value=reception) از موج ۲۱ قابل انتخاب است (AdminControlPanel.tsx:247,1610). سرور در PUT staff: username را lowercase، رمز اولیهٔ کارگاهی ۱۲۳۴ را هش‌شده ثبت و role نامعلوم را به 'reception' برمی‌گرداند (functions/api/collections/[name].ts:147-159).
- گاردهای حذف: حذفِ خودِ فراخوان ممنوع؛ حذف آخرین admin ممنوع؛ حذف همراه با پاک‌سازی sessions آن پرسنل؛ نتیجه در audit staff.save با شمارندهٔ saved/deleted (collections/[name].ts:163-185).
- مسیر پروفایل خودی (موج ۲۰ — رفع ۴۰۳ بی‌مورد): PUT /api/collections/staff با نشستِ بدون canManageStaff فقط ردیف خودِ فراخوان را می‌پذیرد و فقط SELF_FIELDS = name, family, phone, bio, customGreeting, customization, avatarColor, avatarUrl را merge می‌کند؛ نقش/دسترسی/حقوق/username و سایر پرسنل هرگز عبور نمی‌کنند؛ بدون ردیف خودی = ۴۰۳ «برای تغییر اطلاعات سایر پرسنل به مجوز مدیریت نیاز است»؛ audit با action=staff.selfProfile و فهرست فیلدها (collections/[name].ts:85-133).
- برش bootstrap پرسنل (موج ۲۰): در فهرست visibleStaff ردیفِ خودِ کاربر کامل است؛ برای دیگران compensation (حقوق/پورسانت) فقط با canSeeFinancials (canViewPerformance || canViewAccounting || canManageStaff) و username/permissions فقط با canManageStaff سرو می‌شود (bootstrap.ts:157-176) — حقوق فقط admin/accountant/دارندهٔ مجوز می‌بیند.
- ریست رمز: POST /api/auth/admin-reset-password با 'canManageStaff'؛ حداقل ۶ کاراکتر؛ hash+salt واقعی، نابودی همهٔ نشست‌های هدف (destroyAllSessions) و audit staff.reset_password — نوشتن `password` خام در payloadstaff از اول strip می‌شد و جعلی بود (functions/api/auth/admin-reset-password.ts:15-50).
- مودال حقوق و پورسانت: «تنظیمات حقوق و پورسانت «{نام}»» در StaffPerformanceManagerDashboard.tsx:899-921 با دو فیلد baseSalaryMonthly/commissionPercentage؛ ذخیره از مسیر onUpdateStaff → updateStaff → PUT staff (گارد canManageStaff سمت سرور)؛ فیلد خالی باز می‌شود — پیش‌فرض ساختگی ممنوع (د۱۲).
- لاگ حسابرسی (F17): logAudit در functions/lib/db.ts:609-631 با try/catch (هرگز جریان اصلی را نمی‌شکند) در جدول audit_log؛ GET /api/audit فقط 'canManageAdmin' با limit کلامپ‌شدهٔ 10-300 (پیش‌فرض 100) (functions/api/audit.ts:17-28) — «چه کسی، کِی، چه کاری» فقط برای مدیر.
- نوشتن کلکشن staff روی سرور فقط با canManageStaff (COLLECTION_WRITE_PERMISSION در functions/lib/permissions.ts:112) — ماتریسِ زیرتب staff «مستندِ قانون» است؛ اجرای واقعی هم‌زمان در کلاینت (src/lib/scoping.ts) و سرور (requireStaff + bootstrap) قفل است (AdminControlPanel.tsx:1511-1513).

## قراردادهای بین‌بخشی (مذاکره با اسکیل‌های دیگر)
- خروجی به behnam-rbac (همهٔ دامنه‌ها): resolvePermissions + ROLE_PERMISSION_DEFAULTS + COLLECTION_WRITE_PERMISSION منبع واحدِ مجوزِ همهٔ endpointهاست — نشانهٔ شکست قرارداد: پیش‌فرض نقش‌ها یا نام کلیدهای ۱۱گانه در کلاینت و سرور ناهمگام شود.
- ورودی از behnam-hr: attendanceLogs (برای پرسنلِ بدون canViewPerformance فقط ردیف‌های خودش — bootstrap.ts:150-154) و درخواست‌های مرخصی برای کارتابل/عملکرد؛ خروجی به behnam-hr: کارت حضور شخصی، ثبت دستی حضور مدیر و شیفت (StaffPerformanceManagerDashboard) — نشانهٔ شکست: حضورِ دیگران برای پرسنل عادی نشت کند.
- خروجی به behnam-comms: حساب پرسنل + مجوز canViewChat (چت‌های پرسنلی فقط با همین مجوز در هر دو سمت) و ۲FA پیامکی هر حساب (موج ۱۳) — نشانهٔ شکست: پرسنلِ بدون canViewChat پاسخ چت را ببیند یا بفرستد.
- ورودی از behnam-kanban: سفارش‌های واقعی (assignedDesignerId/assignedOperator/claimedAt) مبنای محاسبهٔ کارکرد، درآمدزایی و پورسانت در شیت «مالی پرسنل» — نشانهٔ شکست: آمار عملکرد از داده‌های ساختگی به‌جز سفارش‌های واقعی ساخته شود.
- خروجی به behnam-reports: staff.compensation برای شیت «مالی پرسنل» — فقط با برش مجوزدار bootstrap؛ نشانهٔ شکست: حقوق دیگران در bootstrap یک پرسنل عادی ظاهر شود (تست موج ۲۰ گارد دارد).

## چک‌لیست دیباگ
- گاردها: `rg -n "canManageStaff" functions/api/collections functions/api/auth functions/api/bootstrap.ts` و `rg -n "delete clone.compensation" functions/api/bootstrap.ts`.
- تست‌های Vitest: `npx vitest run src/__tests__/sprint27SecurityWaves.test.ts` («حقوق/پورسانت و username/permissions دیگران حذف می‌شود؛ ردیف خودِ کاربر کامل می‌ماند»، «مسیر staff.selfProfile فقط فیلدهای شخصی خودِ فراخوان را می‌پذیرد») و `sprint27UserFixes` («نقش پذیرش از فرم پرسنل قابل انتخاب است»)؛ e2e مربوط: `npx playwright test e2e/portal.spec.ts` — «staff login modal opens from the header and has demo login».
- پراب سرور: PUT /api/collections/staff با نشست بدون canManageStaff شامل فقط ردیف خودی → {ok:true,selfProfile:true}؛ همان درخواست با نقش/حقوق تغییریافته یا ردیف دیگری → ۴۰۳/بی‌اثر؛ POST admin-reset-password با رمز ۵ کاراکتری → ۴۲۲.
- رفتار مورد انتظار bootstrap: با حساب طراح، staff دیگران بدون compensation/username/permissions؛ ردیف خودش کامل؛ GET /api/audit با حساب غیرمدیر → ۴۰۳.
- چرخهٔ رمز: ریست مدیر → همهٔ نشست‌های پرسنل هدف می‌میرد و ورود بعدی با رمز جدید؛ تغییر رمز خودی از StaffChangePasswordModal مسیر جدا دارد.

## فایل‌ها
src/components/AdminControlPanel.tsx (زیرتب staff 1488+ / ماتریس 1511+ / فرم پرسنل 1560-1624 / مودال دسترسی 1733+) · StaffPerformanceManagerDashboard.tsx (عملکرد/حقوق/بکاپ) · StaffProfileModal.tsx · StaffChangePasswordModal.tsx · StaffLoginModal.tsx (دموی ورود — حفظ اجباری) · Navbar.tsx (گاردهای تب) · functions/api/collections/[name].ts (staff/selfProfile) · functions/api/auth/admin-reset-password.ts · auth/{login,2fa,verify-2fa}.ts · functions/api/audit.ts · functions/api/bootstrap.ts · functions/lib/permissions.ts · functions/lib/db.ts (logAudit/sanitizeStaff/destroyAllSessions) · src/data/defaultData.ts (بذر پرسنل اولیه)

## ممنوع
- حذف دموی ورود پرسنل (کادر StaffLoginModal و ورود نمایشی) — قرارداد کاری کارفرماست، «حفظ اجباری» و بخشی از e2e؛ تغییرش فقط با اطلاع کارفرما.
- سست‌کردن مسیر self-profile (عبور نقش/دسترسی/حقوق/username یا ردیف دیگران) یا گره‌زدن دوبارهٔ پروفایل خودی به canManageStaff (عود به ۴۰۳ موج ۱۹).
- نشت داده: برگرداندن compensation/username/permissions دیگران یا فهرست کامل پرسنل به bootstrap عمومی/نشست بی‌مجوز.
- حذف گاردهای حذف پرسنل (خود-حذفی، آخرین admin، پاک‌سازی sessions) یا ریست رمز بدون هش/بدون audit.
- نوشتن دستی در audit_log از کلاینت یا logAudit را از عملیات حساس برداشتن؛ اعمال تغییر مجوز فقط از رابط و بدون ثبت در F17.

## مذاکره (پیوند به ارکستراتور)
- این اسکیل عضو دورهمی دیباگ است؛ قراردادهای ستون فقرات و دفتر مذاکره در behnam-debug-orchestra/SKILL.md نگهداری می‌شود. هر تغییر عرضی این دامنه باید در ماتریس ارکستراتور ثبت و از چرخهٔ behnam-qa-release عبور کند.
