# اسکیل دامنهٔ کانبان و جریان سفارش — چاپ بهنام
## نقش
قانون‌گذار ۶ ستون، حوضچهٔ آزاد، برداشتن کار، مغایرت کیفی، چرخهٔ استعلام و پروندهٔ جامع.
## قوانین تخصصی
- ستون‌ها: draft_pending → payment_approved → in_production → finishing_qc → ready_delivery → delivered؛ بدون بیعانه، ورود به in_production مسدود است (canMoveForward).
- حوضچهٔ آزاد = سفارش بدون assignedDesignerId و غیرتحویل‌شده؛ برای همهٔ پرسنل دیده می‌شود و «برداشتن به نام من» (claim) همیشه مجاز است.
- تخصیص مجدد کارِ دیگری فقط مدیر/حسابدار (گارد سرور در PATCH /api/orders/:id)؛ claim به نام خودی آزاد.
- استعلام قیمت: بج + فیلتر «فقط استعلام‌ها» + وضعیت waiting_for_quote/quoted/approved_by_customer/rejected در پرونده؛ هر تغییر در interactions ثبت می‌شود.
- اکشن‌های پرداخت/کیفی فقط برای دارندهٔ canEditOrders؛ فاکتور/واتساپ/پرونده برای همهٔ بینندگان.
- همهٔ دکمه‌های فقط-آیکونی باید title/aria-label داشته باشند (TooltipLayer).
## فایل‌ها
src/components/KanbanBoard.tsx · OrderDetailsModal.tsx · ActionQueueToday.tsx · DeliveryPromiseCalendar.tsx · src/lib/scoping.ts · functions/api/orders/[id].ts
## ممنوع
- دورزدن گارد بیعانه؛ حذف ستون/جابه‌جایی ترتیب؛ نمایش دکمه‌های ویرایش به پرسنل بدون canEditOrders.
