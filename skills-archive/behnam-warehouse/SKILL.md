# اسکیل دامنهٔ انبار و مواد اولیه — چاپ بهنام
## نقش
قانون‌گذار موجودی، خرید/مصرف، گردش انبار، انبارگردانی و هشدار خرید.
## قوانین تخصصی
- حرکت کالا فقط با «سند»: createMovement('in'|'out') در /api/inventory؛ خرید می‌تواند هم‌زمان سند هزینه بسازد.
- هشدار کمبود = موجودی ≤ آستانهٔ ماده (stockAlertThreshold)؛ فعال‌سازی موجودی هر ماده از تب «محصولات و تعرفه‌ها».
- انبارگردانی: شمارش واقعی → اسناد اصلاحی خودکار (adjust)، نه ویرایش دستی موجودی.
- بهای تمام‌شدهٔ سفارش از مصرف ثبت‌شده (computeTotalIssuedCost) — در پروندهٔ سفارش نمایش داده می‌شود.
- دستهٔ «تابلوسازی/تخته شاسی» = shasi_craft (دقیقاً همین مقدار؛ sign_craft هرگز).
- گارد: canViewWorkshop || canViewAccounting || canManagePricing.
## فایل‌ها
src/components/WarehouseModule.tsx · WorkshopDevices.tsx · src/utils/warehouse.ts · functions/api/inventory.ts · StockCountModal
## ممنوع
- تغییر مستقیم موجودی بدون سند؛ حذف سند گردش؛ نادیده‌گرفتن هشدار خرید در داشبورد عملیات.
