# اسکیل دامنهٔ حسابداری و مالی — چاپ بهنام
## نقش
قانون‌گذار هر تغییر در AccountingModule، /api/journal، /api/reports، /api/invoices، /api/expenses، صندوق/پوز و فاکتور رسمی.
## قوانین تخصصی (نمیشکند!)
- کدینگ معین ثابت: pos_card=10101، online_gateway=10102، card_to_card=10103، cash=10104، cheque=10105، credit=10106؛ درآمد فروش=70101. هر تغییر کد = خرابی هلو/سپیدار.
- تراکنش‌های «در انتظار تأیید» (رسید مشتری) هرگز در مانده حساب نمی‌آیند تا تأیید پرسنل (server-authoritative در /api/orders/:id/payments).
- VAT فقط ۱۰٪ و فقط در فاکتور رسمی (postedNet/postedVat)؛ قیمت پیش‌فاکتور ویزارد «پیش از مالیات» است.
- سند دوبل باید متعادل باشد (isJournalBalanced)؛ استهلاک/انتقال بین حساب‌ها فقط از «ثبت سند دستی».
- ابطال فاکتور رسمی = سند معکوس (postedRemaining)، هرگز DELETE.
- خروجی: CSV برای هلو/سپیدار با BOM؛ xlsx سه‌شیت (اسناد دوبل/مالی پرسنل/مانده مشتریان) اعداد عددی.
- گارد دسترسی: همهٔ endpointهای مالی requireStaff('canViewAccounting')؛ حذف تراکنش نمایشی فقط در گزارش‌ها.
## فایل‌ها
src/components/AccountingModule.tsx · functions/api/{journal,reports,invoices,expenses,expense-categories}.ts · src/utils/ledger.ts
## ممنوع
- تغییر کلیدهای ACCOUNT_CODES بدون همگام‌سازی سمت سرور؛ نمایش مانده منفی بدون برچسب؛ حذف بج «نمایشی» تراکنش‌های دمو.
