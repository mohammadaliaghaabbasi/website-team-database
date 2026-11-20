# اسکیل دامنهٔ «ارتباطات: چت، اینباکس، اعلان، پیامک» — چاپ بهنام
## نقش
قانون‌گذار چت زنده و صندوق پیام‌رسان‌ها (تب ۵)، کانال‌های ربات، اعلان‌های پرسنل/مشتری و ارسال پیامک..endpointهای این دامنه: /api/chats/*، /api/inbox/*، /api/notifications، /api/sms/send و برش‌های چت/پیامک در /api/bootstrap.

## قوانین تخصصی (نمیشکند!)
- تاریخچهٔ چت: GET /api/chats?since= با گارد requireStaff 'canViewChat' (functions/api/chats/index.ts:13)؛ since>0 = دلتای cursor، since=0 = اسنپ‌شات کامل از همان مسیر readChats که bootstrap می‌خواند تا پولر ۲۰ ثانیه‌ای هرگز اینباکس تازه را با [] پاک نکند.
- پاسخ پرسنل: POST /api/chats/message برای نشست staff اول resolvePermissions(...).canViewChat را چک می‌کند؛ نبودِ مجوز = ۴۰۳ «دسترسی به پیام‌رسان‌ها برای حساب شما محدود شده است» (موج ۲۰ — functions/api/chats/message.ts:54-65). محافظ سوءاستفاده: ۲۰ پیام/دقیقه per-IP → ۴۲۹.
- قفل کانال مشتری (موج ۲۰): نشست مشتری فقط با channel='website_live_chat' و threadKey=session.subjectId می‌نویسد؛ ورودی دستی channel/threadKey بی‌اثر است (message.ts:74-82) و «مشتری فقط در گفتگوی چت زندهٔ خودش» دارد.
- پاسخ روی تردهای خارجی: فقط kindهای telegram/bale/eitaa واقعاً دوسویه‌اند (EXTERNAL_KINDS در functions/lib/inbox.ts)؛ ارسال staff با threadKey نامتجابق kind = ۴۲۲، بدون ربات متصل = ۴۰۹ با ارجاع به «پنل مدیریت ← ربات پیام‌رسان»؛ رسیدهٔ delivered روی پیام ذخیره می‌شود (T22). واتساپ/روبیکا فقط بج/شبیه‌ساز/لینک wa.me هستند، کانکتور بات ندارند.
- رسید خواندن: POST /api/chats/read {threadKey} فقط یک UPDATE هدفمند روی ستون is_read + payload (json_set) می‌زند؛ بازگشت به «DELETE کل جدول + reinsert» ممنوع (ز۵ — read.ts:1-47).
- وب‌هوک: POST /api/inbox/webhook/:channelId/:secret — احراز فقط با secret مسیر؛ secret غلط = ۴۰۴ استلثی (functions/api/inbox/webhook/[channelId]/[secret].ts:9-11,86-88). dedupe با id قطعی `ext-<kind>-<chatId>-<messageId>` (INSERT OR IGNORE → dedupe:true)؛ شکل ناشناخته = ۲۰۰ ok تا retry-storm نشود. سفارش پیش‌نویس فقط با confidence>=0.7 و شماره تماس؛ وگرنه فقط اعلان staff «سفارش بالقوه بدون شماره تماس». auto-ack فقط چت خصوصی (channel.autoAck && !isGroup).
- مدیریت کانال‌ها: GET/POST/DELETE /api/inbox/channels و POST /api/inbox/channels/check همگی requireStaff 'canManageAdmin'؛ توکن در فهرست ماسک می‌شود (sanitizeInboxChannel)، توکن ماسک/خالی قبلی را نمی‌پوشاند، kind پس از ساخت تغییر نمی‌کند (۴۲۲)؛ check اتصال واقعی getMe می‌زند و status=connected/error را می‌نویسد؛ همه در audit_log با action های inbox.channel.save/check/delete.
- اعلان‌ها: GET /api/notifications پرسنل = audience='staff' (LIMIT 100)، مشتری = audience='customer' AND target_phone=session.subjectId (LIMIT 50). POST {ids} (موج ۲۰ — رفع IDOR نوشتاری): هر UPDATE با قید مالکیت audience/target_phone زده می‌شود؛ مشتری نمی‌تواند اعلان دیگری را «خواندم» بزند (functions/api/notifications.ts:60-75). هر رخداد حساس با notify() (functions/lib/notify.ts) + Web Push بست‌بی‌ضرر fan-out می‌شود.
- شبیه‌ساز فقط-دمو (موج ۲۱): دکمهٔ «شبیه‌سازی پیام ورودی (دمو)» فقط وقتی store.offline=true رندر می‌شود (SocialOmnichannelInbox.tsx:63-66,247-256)؛ در حالت آنلاین فرستنده واقعی ثبت می‌شود و رکورد گمراه‌کننده ساختنش ممنوع است.
- پیامک: POST /api/sms/send فقط با 'canManageAdmin' (موج ۱۲ — هزینهٔ واقعی کاوه‌نگار)؛ بدون KAVENEGAR_API_KEY حالت mock/queued (functions/lib/sms.ts)؛ لاگ در meta smsLogs (آخرین ۵۰۰). bootstrap کانفیگ پیامک را فقط به دارندهٔ canManageAdmin با apiKey ماسک‌شده می‌دهد (bootstrap.ts:184) و PUT smsConfig هیچ‌وقت کلید ماسک/خالی را روی کلید ذخیره‌شده نمی‌نویسد (functions/api/collections/[name].ts:262-270). نکته: نوشتن کلکشن smsLogs برخلاف endpoint ارسال، با canViewChat باز است (COLLECTION_WRITE_PERMISSION در functions/lib/permissions.ts:108).

## قراردادهای بین‌بخشی (مذاکره با اسکیل‌های دیگر)
- ورودی از behnam-rbac: مجوز canViewChat / canManageAdmin / canViewCustomers از functions/lib/permissions.ts + نشست از resolveSession — نشانهٔ شکست قرارداد: ۴۰۳ «دسترسی به پیام‌رسان‌ها…» یا برش liveChatMessages/smsConfig در bootstrap.
- ورودی از behnam-crm: customerProfiles (فقط با canViewCustomers در bootstrap.ts:190) برای نام نمایشی فرستنده + قالب‌های پیام messageTemplates (ensureDefaultTemplates) برای پاسخ سریع صندوق — نشانهٔ شکست: فرستندهٔ ناشناس «مشتری» و پاسخ سریع خالی.
- خروجی به behnam-kanban: «تبدیل پیام به سفارش» + سفارش پیش‌نویس AI (createOrderLeadFromAi) با پیام سیستمی «🤖 سفارش پیش‌نویس … ثبت شد» به صف سفارش‌ها — نشانهٔ شکست: پیام سفارشیِ بی‌شماره، فقط اعلان staff می‌شود و lead ساخته نمی‌شود.
- خروجی به behnam-staff-management: هر save/check/delete کانال + خطاهای ارسال به logAudit؛ notify(audience:'staff') سوخت اعلان‌های NotificationBell — نشانهٔ شکست: audit_log بدون inbox.channel.* یا زنگ اعلان ساکت.
- خروجی به behnam-kanban/مالی (مسیر رسید): notify() در functions/api/orders/index.ts:201 و orders/[id].ts:97 اعلانِ تغییر وضعیت/رسید مشتری را می‌سازد — شکستش یعنی پرتال مشتری بی‌خبر می‌ماند.

## چک‌لیست دیباگ
- گاردها را با `rg -n "canViewChat" functions/api/chats functions/api/bootstrap.ts` و `rg -n "canManageAdmin" functions/api/inbox functions/api/sms` راستی‌آزمایی کن.
- تست‌های Vitest: `npx vitest run src/__tests__/sprint27SecurityWaves.test.ts` (۱۹ آزمون گارد: «تاریخچهٔ چت فقط با canViewChat سرو می‌شود»، «پاسخ پرسنل نیازمند canViewChat است»، «مشتری فقط در گفتگوی چت زندهٔ خودش می‌نویسد»، «notifications با ID فقط روی ردیف‌های خودِ فراخوان»، «کانفیگ پیامک فقط برای دارندهٔ canManageAdmin») و `sprint27UserFixes` («شبیه‌سازی پیام فقط در حالت آفلاین/دمو نشان داده می‌شود»).
- پراب سرور: GET /api/chats?since=0 با نشست بدون canViewChat → ۴۰۳؛ POST /api/chats/message مشتری با channel دستی → کانال قفل website_live_chat؛ وب‌هوک با secret اشتباه → ۴۰۴؛ POST /api/inbox/channels/check با توکن بات غلط → status=error.
- رفتار مورد انتظار اینباکس: پولینگ /api/chats هر ۲۰s فقط دلتا؛ بازکردن ترد → /api/chats/read و صفر شدن بج؛ پاسخ خارجی → delivered:true یا ۵۰۲ با متن خطای پیام‌رسان.
- تغییر وضعیت سفارش در کانبان باید بدون رفرش، هم زنگ پرسنل و هم نوار اعلان پرتال مشتری را تازه کند (notify + pushInBackground).

## فایل‌ها
functions/api/chats/index.ts · chats/message.ts · chats/read.ts · functions/api/inbox/channels/{index,check,webhook}.ts · functions/api/inbox/webhook/[channelId]/[secret].ts · functions/api/notifications.ts · functions/api/sms/send.ts · functions/lib/{inbox,notify,sms,push,ai,orderLead}.ts · src/components/SocialOmnichannelInbox.tsx · CustomerLiveChatWidget.tsx · NotificationBell.tsx · SMSDispatchModule.tsx · src/components/admin/InboxChannelsManager.tsx · AdminControlPanel.tsx (زیرتب sms / bots / templates)

## ممنوع
- حذف یا کور کردن دموی ورود پرسنل/مشتری — قرارداد کاری کارفرماست و «حفظ اجباری» دارد (خاموشی فقط با کلید قراردادی مثل OTP_DEVCODE=off).
- سرو کردن تاریخچهٔ چت/کانفیگ پیامک/لاگ پیامک به نشستِ بی‌مجوز، یا حذف rate-limit و قفل کانال مشتری.
- شبیه‌ساز پیام را در حالت آنلاین فعال‌کردن؛ افزودن ادعای کانکتور بات برای واتساپ/روبیکا که کانکتور واقعی ندارند.
- بازگشت مسیر read/restore چت به DELETE-all (به‌جای UPDATE هدفمند / merge-only INSERT OR IGNORE).
- خروج وب‌هوک از الگوی secret-in-path و ۴۰۴ استلثی؛ لاگ‌کردن توکن ربات در audit.

## مذاکره (پیوند به ارکستراتور)
- این اسکیل عضو دورهمی دیباگ است؛ قراردادهای ستون فقرات و دفتر مذاکره در behnam-debug-orchestra/SKILL.md نگهداری می‌شود. هر تغییر عرضی این دامنه باید در ماتریس ارکستراتور ثبت و از چرخهٔ behnam-qa-release عبور کند.
