# اسکیل دامنهٔ مدیریت دسترسی‌ها و امنیت — چاپ بهنام
## نقش
قانون‌گذار نقش‌ها، مجوزهای یازده‌گانه، مرز مشتری/پرسنل، لاگ حسابرسی و وصله‌های امنیتی.
## قوانین تخصصی (قرارداد موج ۲۰ — گارد آزمون دارد، نمیشکند)
- ۶ نقش: admin/designer/operator/accountant/delivery/reception (پذیرش از فرم قابل ایجاد است). ۱۱ مجوز تکی؛ admin همیشه کامل.
- هر endpoint حساس requireStaff + مجوز؛ چت فقط با canViewChat؛ machine-log فقط با canViewWorkshop؛ bootstrap دادهٔ حساس (حقوق/چت‌ها/پروفایل‌ها/پیامک) را بر اساس مجوز می‌بُرد؛ ردیفِ خود کاربر کامل می‌ماند.
- مشتری فقط دادهٔ خودش (customer_phone = session.subjectId)؛ ناشناس فقط فیلدهای امن رهگیری (بدون نام/مبلغ/تلفن/طرح).
- فایل‌ها: پرسنل آپلود = public؛ مشتری/ناشناس = session (بدون نشست ۴۰۴)؛ ردیف‌های قدیمی public می‌مانند.
- اعلان‌ها با ID فقط برای مالک؛ seed بدون SEED_TOKEN = ۴۰۳؛ هر عملیات حساس در لاگ حسابرسی (logAudit) ثبت می‌شود.
- دموی ورود (کد نمایشی OTP و کادر دموی مشتری) به خواستهٔ کارفرما حفظ است؛ خاموشی فقط با OTP_DEVCODE=off.
## فایل‌ها
functions/lib/permissions.ts · db.ts(requireStaff) · src/lib/scoping.ts · AdminControlPanel(ماتریس) · functions/_middleware.ts
## ممنوع
- گارد فقط-کلاینتی؛ دادهٔ همه برای همه؛ تغییر ROLE_PERMISSION_DEFAULTS بدون همگام‌سازی هر دو سمت؛ حذف حالت‌های دموی ورود.
