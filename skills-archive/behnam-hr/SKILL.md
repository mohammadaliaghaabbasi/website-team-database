# اسکیل دامنهٔ منابع انسانی، حضور و پورسانت — چاپ بهنام
## نقش
قانون‌گذار حضور/غیاب، مرخصی، شیفت، دورکاری، کارکرد مالی پرسنل و تنظیمات حقوق.
## قوانین تخصصی
- حضور با تفکیک «حضوری کارگاه» / «دورکاری منزل»؛ ثبت ورود/خروج از /api/attendance/clock (فقط خودِ شخص).
- مرخصی: POST/GET /api/attendance/leave (سطرهای خودش)؛ تصمیم مدیر = PUT همان endpoint با canManageAdmin.
- لاگ‌ها در جدول واقعی attendance؛ بدون مجوز عملکرد فقط ردیف‌های خود پرسنل سرو می‌شود.
- پورسانت از سفارش‌های واقعی محاسبه می‌شود (وصول بیعانه × درصد) + حقوق پایه ماهانه؛ تنظیم از مودال «تنظیمات حقوق و پورسانت» با canManageStaff.
- ثبت دستی تردد فقط توسط مدیر؛ هر رکورد با ثبت‌کننده و قابل تأیید/رد.
- ثبت سرویس دستگاه/متراژ از دفتر کارکرد (machine-log) است، نه از فیلدهای دموی دستگاه.
## فایل‌ها
src/components/StaffPerformanceManagerDashboard.tsx · StaffWorkloadView.tsx · LeaveRequestsCard/LeaveDecisionsCard · functions/api/attendance/* · functions/lib/attendance.ts
## ممنوع
- نمایش حقوق/پورسانت دیگران بدون canViewPerformance/canViewAccounting (bootstrap حذفش می‌کند — نباید کلاینت دورش بزند)؛ ثبت تردد به نام دیگری.
