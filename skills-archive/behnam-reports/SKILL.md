# اسکیل دامنهٔ «گزارش‌ها و خروجی‌ها» — چاپ بهنام
## نقش
قانون‌گذار گزارش‌های مالی دفتر کل (تب ۷ زیرتب «گزارش‌های مالی»)، خروجی‌های xlsx/CSV حسابداری و پورسانت، آمار داشبورد، آرشیو بکاپ سرور و امضای نسخهٔ داده‌ها..endpointهای این دامنه: /api/reports، /api/admin/backup-export، /api/data-version و خروجی‌های سمت کلاینت AccountingModule/StaffPerformanceManagerDashboard/OpsDashboard.

## قوانین تخصصی (نمیشکند!)
- GET /api/reports فقط با requireStaff 'canViewAccounting' (functions/api/reports.ts:29)؛ خروجی: سود و زیان دوره (درآمد 4101، VAT 2101، بهای تمام‌شده 5101-5999، هزینه 6101-6999)، تراز آزمایشی معین از buildTrialBalance روی journal_entries، سنی مطالبات از ماندهٔ واقعی سفارش‌ها (status=delivered و remaining<=0 حذف؛ مبنا dueDate ایزو و در نبودش زمان ثبت) و تعداد اسناد. قانون صادقانگشت سربرگ فایل: «هیچ عددی تخمینی به تراز اضافه نمی‌شود؛ دفتر خالی = گزارش خالی».
- خروجی xlsx سه‌شیت (موج ۲۲): AccountingModule.tsx:837-899 با `await import('xlsx')` (lazy-import — جزو باندل اولیه نیست)؛ شیت‌های «اسناد دوبل» (همان ستون‌های CSV هلو/سپیدار/محک)، «مالی پرسنل» (کارکرد/پورسانت) و «مانده مشتریان» (تجمیع بر اساس تلفن، مرتب نزولی بدهی). اعداد باید «عدد واقعی (نه متن)» بمانند تا نرم‌افزار مالی جمع بزند؛ شکست lazy-import → fallback به CSV همیشه‌کار.
- CSV هلو/سپیدار: handleExportAccountingCSV در AccountingModule.tsx:786-833 با BOM `'\uFEFF'` + CRLF + سلول‌های کوتیشن‌دار؛ نگاشت واحد کد معین 10101-10106 بر اساس paymentMethod (رفع باگ B8: cash دیگر هم‌جا با 10103 صادر نمی‌شود) و بستانکار 70101. ابزار عمومی src/utils/csv.ts (toCsv/downloadCsv با BOM و escape) مسیر مشترک خروجیِ پورسانت (StaffPerformanceManagerDashboard:708)، عملیات (OpsDashboard:196) و دفتر کل (AccountingModule:1753) است.
- کارت‌های آمار داشبورد = فیلتر واقعی (موج ۲۱): کلیک کارت‌های DashboardStats چهار وضعیت all_active/in_production/ready_delivery/urgent را به‌عنوان statusFilter به کانبان می‌فرستد (App.tsx:533؛ فیلتر واقعی KanbanBoard.tsx:141-144) — آمار فقط نمایشی باقی نمی‌ماند. فیلتر بازهٔ زمانی (امروز/ماه/سال) جداست و در StaffPerformanceManagerDashboard.tsx:140-149 روی createdAt/claimedAt اعمال می‌شود.
- بکاپ سرور: GET /api/admin/backup-export فقط با 'canManageAdmin' + audit backup.server_export؛ از جدول‌های واقعی D1 می‌خواند (نه اسنپ‌شات مرورگر). اسرار هرگز از سرور خارج نمی‌شوند: sessions/otps/rate_limits/push_subscriptions اصلاً صادر نمی‌شوند، meta کلیدهای شبیه sms/otp/secret/token/password/apikey ماسک، staff با sanitizeStaff (بدون هش رمز)، uploads/rate_limits فقط COUNT؛ chat_messages از موج ۱۲ کامل (آخرین ۲۰۰۰ — payloadها URL آپلودند نه base64) تا ری‌استور تاریخچه ناممکن نشود؛ POST همان مسیر = ۴۰۵ (functions/api/admin/backup-export.ts:20-21,107-114,139-141).
- امضای دادهٔ مرجع: GET /api/data-version عمومی و بی‌وزن است — فقط شمارندهٔ rev، بدون دادهٔ شخصی؛ کلاینت هر ۶۰ ثانیه می‌خواند و تغییر → re-bootstrap بی‌صدا؛ سفارش‌ها/چت‌ها/اعلان‌ها جداگانه زنده همگام می‌شوند (functions/api/data-version.ts:1-10).
- صداقت پول در گزارش پرسنل (د۱۲): «unset compensation = unset money» — بدون compensation واقعی، پورسانت/قابل‌پرداخت صفر است و مودال حقوق با فیلد خالی باز می‌شود (نه پیش‌فرض ساختگی ۱۵ میلیون) (StaffPerformanceManagerDashboard.tsx:163-169,215-219 و AccountingModule.tsx:609-612).
- ری‌استور بکاپ هرگز مخرب نیست: PUT کلکشن chats فقط merge-only INSERT OR IGNORE است (functions/api/collections/[name].ts:188-214) — رکورد سمت سرور با payload کلاینت پاک نمی‌شود.

## قراردادهای بین‌بخشی (مذاکره با اسکیل‌های دیگر)
- ورودی از behnam-accounting: journal_entries با کدینگ قراردادی (4101 فروش، 2101 VAT، 5101-5999 بهای تمام‌شده، 6101-6999 هزینه) برای /api/reports و سند دوبل — نشانهٔ شکست قرارداد: تراز خالی یا PnL غلط؛ پاسخ درست یعنی «گزارش خالی»، نه عدد ساختگی.
- ورودی از behnam-kanban: جدول orders (remainingBalance/dueDate/createdAt/claimedAt) برای سنی مطالبات، شیت «مانده مشتریان» و آمار داشبورد؛ خروجی معکوس: statusFilter چهارحالته داشبورد → کانبان — نشانهٔ شکست: aging صفر با سفارش بدهکار موجود یا کلیک کارت بدون فیلتر کانبان.
- ورودی از behnam-hr: attendanceLogs (totalMinutesWorked/locationType) برای ستون‌های کارکرد در «مالی پرسنل» و CSV پورسانت؛ ورودی از behnam-staff-management: staff.compensation (baseSalaryMonthly/commissionPercentage) — نشانهٔ شکست: پورسانت از پیش‌فرض ساختگی محاسبه شود (ممنوع — د۱۲).
- خروجی به behnam-accounting: xlsx سه‌شیت + CSV هلو/سپیدار با BOM (ورودی مستقیم نرم‌افزارهای هلو/سپیدار/محک/رافع) — نشانهٔ شکست: اعداد متنی/فارسی‌شکسته در اکسل یعنی BOM یا type عددی نشکسته.
- خروجی به behnam-rbac / behnam-staff-management: آرشیو JSON بکاپ سرور (با ماسک اسرار) برای بازیابی بلندمدت + rev دادهٔ مرجع برای همگام‌سازی چندپرسنلی — نشانهٔ شکست: رکورد پرسنل با password_hash در بکاپ، یا تغییر تعرفه بدون بالا رفتن data-version.

## چک‌لیست دیباگ
- گاردها: `rg -n "canViewAccounting" functions/api/reports.ts` و `rg -n "canManageAdmin|logAudit" functions/api/admin/backup-export.ts`.
- تست‌های Vitest: `npx vitest run src/__tests__/sprint11Management.test.ts` («toCsv با BOM اکسل‌پسند + Escape درست»)، `sprint27UserFixes` («کلیک کارت آمار = فیلتر واقعی کانبان (۴ حالت)»)، `sprint27SecurityWaves` (برش bootstrap، «حقوق/پورسانت … حذف می‌شود»).
- پراب سرور: GET /api/reports با نشست طراح → ۴۰۳؛ GET /api/admin/backup-export → فایل JSON با kind=behnam-d1-backup + رکورد audit؛ GET /api/data-version → فقط {ok,rev,serverTime}.
- رفتار مورد انتظار خروجی: xlsx = سه شیت با نام‌های فارسی و سلول‌های عددی؛ CSV در اکسل فارسیِ سالم با BOM باز کند؛ سند بدون offlineAccountingSync → «سند موقت N» و «در انتظار ثبت».
- رگرسیون ثابت پس از هر تغییر: tsc 0 / eslint 0 / Vitest سبز / build OK و SW bump (قرارداد موج ۲۲ — SW v66 فعلی).

## فایل‌ها
functions/api/reports.ts · functions/api/admin/backup-export.ts · functions/api/data-version.ts · functions/lib/ledger.ts · src/components/AccountingModule.tsx (خروجی‌ها: 786-905) · src/components/DashboardStats.tsx · src/components/KanbanBoard.tsx (statusFilter 141-148) · src/components/StaffPerformanceManagerDashboard.tsx (بازهٔ زمانی + بکاپ سرور 255-320) · src/components/OpsDashboard.tsx · src/utils/csv.ts · src/lib/api.ts

## ممنوع
- افزودن عدد تخمینی/پیش‌فرض مالی به تراز، aging یا پورسانت — «دفتر خالی = گزارش خالی» و «unset compensation = unset money».
- حذف lazy-import xlsx (برگشت به باندل اولیه) یا تبدیل اعداد عددی شیت‌ها به متن فارسی.
- خروجی CSV بدون BOM / بدون escape؛ صدور بکاپ با هش رمز، توکن یا session؛ حذف ماسک meta.
- برگرداندن ری‌استور چت/بکاپ به مسیر مخرب DELETE-all؛ چسباندن فیلتر بازهٔ زمانی به جای فیلتر واقعی کارت‌های آمار (عقب‌گرد موج ۲۱).
- حذف دموی ورود (پرسنل/مشتری) در هر مسیر گزارش‌گیری و پراب — قرارداد کارفرما، حفظ اجباری.

## مذاکره (پیوند به ارکستراتور)
- این اسکیل عضو دورهمی دیباگ است؛ قراردادهای ستون فقرات و دفتر مذاکره در behnam-debug-orchestra/SKILL.md نگهداری می‌شود. هر تغییر عرضی این دامنه باید در ماتریس ارکستراتور ثبت و از چرخهٔ behnam-qa-release عبور کند.
