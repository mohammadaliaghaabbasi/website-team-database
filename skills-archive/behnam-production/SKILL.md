# اسکیل دامنهٔ «کارگاه، دستگاه‌ها و عملیات» — چاپ بهنام
## نقش
قانون‌گذار تب کارگاه (دستگاه‌ها + انبار)، دفتر کارکرد دستگاه‌ها، سرویس دوره‌ای و نگهداری (F14)، داشبورد عملیات، صف اقدام امروز، متراژ تولید و شفافیت دمو. Endpointهای تحت قانون: /api/machine-log، /api/maintenance، /api/inventory (مشترک با اسکیل انبار). جدول‌ها: machine_logs، device_maintenance، گردش انبار.

## قوانین تخصصی (نمیشکند!)
- دستگاه‌ها IoT نیستند؛ «دفتر کارکرد» منبع حقیقت است: ساعت/متراژ/خروجی هر شیفت دستی ثبت می‌شود و ثبت کارکرد با ساعت مثبت، cumulativeHours دستگاه را همان‌جا بالا می‌برد (WorkshopDevices.tsx MachineWorkLog → api.addMachineLog؛ machine-log.ts سطر ۸۹: حداقل یکی از ساعت/متراژ/تعداد اجباری است).
- گارد دفتر کارکرد (موج ۲۰): GET و POST مسیر /api/machine-log هر دو به مجوز canViewWorkshop گارد دارند و ثبت در audit با action='machine.log' می‌رود (functions/api/machine-log.ts سطر ۵۲ و ۷۵).
- سرویس دوره‌ای از ساعت کارکرد واقعی حساب می‌شود: پیش‌فرض صادقانهٔ بازار SERVICE_DEFAULT_HOURS=۲۰۰؛ isServiceDue وقتی است که hoursSinceService ≥ serviceIntervalHours؛ «ثبت سرویس انجام شد» lastServiceHours را برابر cumulativeHours می‌کند تا شمارنده صفر شود (WorkshopDevices.tsx سطر ۴۲-۴۸ و ۸۰۲-۸۱۶).
- متراژ امروز داشبورد عملیات از دفتر کارکرد واقعی تجمیع می‌شود، نه اعداد ثابت seed (موج ۲۱): api.machineLogs() → جمع metersProduced ردیف‌های امروز؛ فقط در نبود سرور (دمو/آفلاین) fallback به مجموع totalMetersToday دستگاه‌ها است و همان‌جا برچسب «(تخمینی)» می‌آید (OpsDashboard.tsx سطر ۱۴۸-۱۷۱ و ۳۲۳).
- برچسب CMYK صادقانه است: «سطح رنگ (CMYK) — تخمینی» — تا سنسور واقعی متصل نشده این سطح‌ها تخمینی‌اند و هیچ ادعای دقیقی نباید نوشته شود (WorkshopDevices.tsx سطر ۵۳۱).
- دستهٔ دستگاه «تابلوسازی» فقط مقدار معتبر shasi_craft می‌نویسد؛ sign_craft مقدار معیوبِ حذف‌شدهٔ موج ۲۱ است (WorkshopDevices.tsx سطر ۲۷۸؛ گارد آزمون ی۴ در sprint27UserFixes).
- حذف دستگاه فقط نقش admin با prop زندهٔ onDeleteMachine (د۹)؛ حذف رکورد نگهداری (موج ۲۱) با endpoint DELETE /api/maintenance?id= و confirm خطرناک استور (WorkshopDevices.tsx سطر ۴۱۹-۴۲۸ و ۶۱۷-۶۳۸؛ maintenance.ts سطر ۹۴-۱۰۵).
- هر سه متد نگهداری (GET/POST/DELETE) با canViewWorkshop گارد دارند و ثبت، audit با action='device.maintenance' می‌سازد (functions/api/maintenance.ts سطر ۲۸/۵۲/۹۷؛ KINDS: maintenance/repair/calibration/downtime).
- سوددهی دستگاه‌ها فقط برای دارندهٔ canViewAccounting رندر می‌شود: درآمد تخصیصی = سفارش‌های هم‌نام دستگاه یا هم‌دسته خدمت؛ هزینه = سرویس/تعمیر + مصرف موادِ ثبت‌شده روی همان دستگاه (WorkshopDevices.tsx MachineProfitPanel سطر ۹۵۳-۱۰۴۶؛ utils/warehouse machineProfitability).
- صف اقدام امروز سه سطل دارد (تازه‌ها draft_pending / بیعانهٔ pending / ready_delivery) و سه نما «صف / تقویم وعده تحویل / داشبورد عملیات» روی یک سگمنت مشترک‌اند — هیچ نمای جدیدی جدا از این سگمنت نساز (ActionQueueToday.tsx سطر ۸۵-۱۳۶).
- شفافیت دمو: پول نمایشی همیشه از پول واقعی جدا دیده می‌شود — بج «نمایشی امروز» با isDemoTransaction و ستون «شامل نمایشی» در CSV گزارش عملیات (OpsDashboard.tsx سطر ۱۱۹-۱۲۷ و ۱۸۳-۲۱۴). تنها شبیه‌سازِ کد، «شبیه‌سازی پیام» اینباکس است که فقط در حالت آفلاین/دمو نمایش داده می‌شود (SocialOmnichannelInbox.tsx سطر ۶۳؛ گارد ی۱۱ sprint27UserFixes) — شبیه‌ساز تولیدی در کارگاه وجود ندارد و ساختنش از خودت ممنوع.

## قراردادهای بین‌بخشی (مذاکره با اسکیل‌های دیگر)
- ورودی از behnam-warehouse: هشدار خرید = lowStockList(استور materials) با آستانهٔ هر ماده؛ داشبورد کلیکش را با setCurrentTab('workshop') + setWorkshopSub('warehouse') دیپ‌لینک می‌کند (OpsDashboard.tsx سطر ۵۹-۶۱ و ۲۴۷-۲۵۷) — نشانهٔ شکست قرارداد: کارت «هشدار خرید مواد» همیشه صفر است یا کلیک به انبار نمی‌رود.
- ورودی از behnam-kanban: سفارش‌های غیرتحویل‌شده با فیلدهای machine و serviceCategory صف هر دستگاه را می‌سازند؛ کلیک کارت آمار، statusFilter کانبان را ست می‌کند (WorkshopDevices.tsx getOrdersForMachine سطر ۱۴۱-۱۴۸؛ App پاس statusFilter) — نشانهٔ شکست: «صف سفارشات این دستگاه» خالی می‌ماند با وجود کار زیر چاپ.
- خروجی به behnam-delivery: وضعیت دستگاه‌ها + سطل «آماده تحویل در باجه» با دکمهٔ «تحویل شد» → status='delivered' (ActionQueueToday.tsx سطر ۱۸۲-۲۰۰) — نشانهٔ شکست: سفارش آماده در باجه تحویل نمی‌شود و در داشبورد می‌ماند.
- خروجی به behnam-rbac: هر ثبت/حذف کارکرد و نگهداری در لاگ حسابرسی (machine.log / device.maintenance) ثبت می‌شود (machine-log.ts سطر ۱۱۶-۱۲۳؛ maintenance.ts سطر ۸۲-۸۹) — نشانهٔ شکست: رکورد بدون ردپای حسابرسی در جدول می‌نشیند.

## چک‌لیست دیباگ
- `rg -n "canViewWorkshop" functions/api/machine-log.ts functions/api/maintenance.ts` → هر دو/هر سه مسیر گارد دارند؛ بدون نشست = 401.
- `rg -n "sign_craft|shasi_craft" src/components/WorkshopDevices.tsx` → فقط shasi_craft.
- `rg -n "CMYK\) — تخمینی|api.deleteMaintenance" src/components/WorkshopDevices.tsx` → گاردهای موج ۲۱ (ی۸).
- `rg -n "machineLogs\(\)|logMetersToday \?\? machines.reduce" src/components/OpsDashboard.tsx` → متراژ واقعی (ی۹).
- تست‌ها: Vitest `sprint27UserFixes` (ی۴/ی۸/ی۹/ی۱۱)، `dashboardStats`، `sprint3Wave2` (د۹ حذف دستگاه)؛ e2e: `npx playwright test e2e/portal.spec.ts`.
- پراب سرور: GET /api/machine-log بدون نشست → 401؛ POST /api/maintenance با kind نامعتبر → 422.
- رفتار مورد انتظار داشبورد: بدون سرور، متراژ امروز با پسوند «(تخمینی)» نمایش داده شود؛ با سرور، عدد دفتر کارکرد بدون برچسب.

## فایل‌ها
src/components/WorkshopDevices.tsx · WarehouseModule.tsx · OpsDashboard.tsx · ActionQueueToday.tsx · src/utils/warehouse.ts · src/lib/api.ts (machineLogs/addMachineLog/maintenance/addMaintenance/deleteMaintenance/inventory) · functions/api/machine-log.ts · functions/api/maintenance.ts · functions/api/inventory.ts

## ممنوع
- حذف دموی ورود پرسنل (کد نمایشی دومرحله‌ای در functions/api/auth/login.ts سطر ۸۰) و دموی OTP مشتری با کلید خاموشی OTP_DEVCODE=off (functions/api/auth/customer/otp.ts سطر ۷۱) — حفظ اجباریِ قرارداد کاری کارفرما.
- بازگرداندن اعداد ثابت دمو به متراژ امروز یا حذف برچسب «تخمینی» از CMYK/متراژ؛ نوشتن sign_craft.
- حذف گارد canViewWorkshop از machine-log/maintenance یا دورزدن confirm در حذف رکورد/دستگاه.
- ساختن شبیه‌ساز تولید در محیط واقعی (هر شبیه‌سازی فقط در حالت دمو/آفلاین).
- تبدیل سه نمای صف اقدام (صف/تقویم/داشبورد) به تب جداگانه؛ نمایش گزارش سوددهی به پرسنلِ بدون canViewAccounting.

## مذاکره (پیوند به ارکستراتور)
- این اسکیل عضو دورهمی دیباگ است؛ قراردادهای ستون فقرات و دفتر مذاکره در behnam-debug-orchestra/SKILL.md نگهداری می‌شود. هر تغییر عرضی این دامنه باید در ماتریس ارکستراتور ثبت و از چرخهٔ behnam-qa-release عبور کند.
