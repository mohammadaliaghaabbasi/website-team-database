---
name: skill-hunter
description: Use this skill when the user wants to find, evaluate, or install new AI agent skills from GitHub (repos containing SKILL.md files), shares a GitHub link to a skills collection, or asks to grow/upgrade the skill library ("اسکیل جدید پیدا کن", "این ریپو به دردت می‌خوره؟", "موتور اسکیل", "find skills", "add to our system"). Runs the hunt.py engine: GitHub search → shallow clone → security scan (prompt-injection, obfuscation, exfiltration) → relevance scoring for the user's domains (شرکت‌ساز formula, FounderOS agency work, Instagram/marketing, Next.js coding) → verdict per skill (INSTALL / MAYBE / SKIP) → install with provenance.
---

# Skill Hunter — موتور شکار اسکیل

ابزار اصلی: `python3 /home/z/my-project/scripts/skill-engine/hunt.py`

## گردش کار استاندارد

1. **جستجو** (وقتی کاربر منبع جدید خواست):
   ```bash
   GH_TOKEN=<توکن کاربر اگر در جلسه داده؛ بدون توکن هم کار می‌کند> \
     python3 scripts/skill-engine/hunt.py search --limit 20
   ```
   گزارش در `scripts/skill-engine/reports/search-*.md`

2. **غربال** هر ریپوی کاندیدا:
   ```bash
   python3 scripts/skill-engine/hunt.py vet owner/repo
   ```
   خروجی: حکم هر اسکیل + دلیل فارسی + هشدارهای امنیتی در `reports/vet-*.json`

3. **بازبینی انسانی هشدارها** (الزامی قبل از نصب هر چیزی با 🟡):
   - متن‌های «تزریق پرامپت» در فایل‌های md/json اغلب دفاعی/آزمونی‌اند → فایل را باز کن و متن را بخوان
   - دامنهٔ ناشناس در کد اجرایی → ببین فقط URL لوگو/CDN است یا ارسال داده
   - `child_process`/`.env` در ابزارهای قانونی (سرور محلی، اسکریپت) معمولاً بی‌خطر است

4. **نصب** (فقط موارد منتخب — حکم موتور پیشنهاد است، قضاوت نهایی با تو):
   ```bash
   python3 scripts/skill-engine/hunt.py install owner/repo --skills name1 name2
   ```
   هر نصب: `skills/<name>/` + `.provenance.json` (ریپو/شا/لایسنس/تاریخ)

5. **ثبت**: یک بلاک در `worklog.md` + اگر کاربر خواست پوش به `mohammadaliaghaabbasi/sherkatsaz` (پوشهٔ `skills/` + `skill-engine/`)

## قواعد سخت

- توکن هرگز در فایل ذخیره نمی‌شود — فقط env/آرگومان لحظه‌ای
- FAIL امنیتی (تزریق/obfuscation در کد اجرایی) = هرگز نصب نکن
- بدون لایسنس = فقط استفادهٔ محلی، بازتوزیع/پوش ممنوع (نمونهٔ ردشده: anthropics/skills)
- نام تکراری با اسکیل‌های موجود = SKIP (موتور خودش تشخیص می‌دهد)
- سهمیهٔ بهداشت کانتکست: حداکثر ~۱۵ اسکیل خارجی جدید در هر دوره؛ هر اسکیل نصب‌شده یک ورودی به فهرست اسکیل‌های جلسات بعد اضافه می‌کند — فقط موارد پرفایده را نصب کن
- حوزه‌های ارتباط (ثبت‌شده در GOOD_KEYWORDS داخل hunt.py): بازاریابی/فروش/آفر/قیمت‌گذاری، CRO/کپی‌رایتینگ، برنامه‌نویسی Next.js/TS/Python، تست/دیباگ/ریویو، ایده‌پردازی/پلنینگ، فارسی/RTL
- حذفی‌های بازار ایران: ایمیل سرد، سرویس‌های تحریمی (Twilio/SendGrid/HubSpot/Salesforce/Stripe)

## منابع شناخته‌شده

| ریپو | وضعیت |
|---|---|
| coreyhaines31/marketingskills | نصب‌شده (۱۲ اسکیل منتخب، ۲۰۲۶-۱۰-۲۷) |
| obra/superpowers | نصب‌شده (۶ اسکیل کارگاهی، ۲۰۲۶-۱۰-۲۸) |
| addyosmani/agent-skills | نصب‌شده (۲ اسکیل، ۲۰۲۶-۱۰-۲۸) |
| Leonxlnx/taste-skill | نصب‌شده (design-taste-frontend — ضد-طراحی ژنریک، ۲۰۲۶-۱۰-۲۸؛ هشدار cdp.mjs بازبینی شد: false-positive کلاینت CDP محلی) |
| pbakaus/impeccable | نصب‌شده (impeccable — واژگان طراحی/آدیت، Apache-2.0، ۲۰۲۶-۱۰-۲۸؛ modern-screenshot.umd.js = باندل npm رسمی) |
| affaan-m/ECC | نصب‌شده (۷ اسکیل استک ما: react-performance, frontend/backend-patterns, prisma-patterns, agent-security-hardening, marketing-campaign, brand-voice — ۲۰۲۶-۱۰-۲۸) |
| anthropics/skills | ردشده — بدون لایسنس + تکراری (docx/pdf/pptx/xlsx) |
| msitarzewski/agency-agents | ردشده — فرمت SKILL.md ندارد (پرامپت‌های agent است) |
| tt-a1i/archify | ردشده — اسکیل اصلی ۱۷MB حجیم + همپوشانی با charts |
| DietrichGebert/ponytail | ردشده — فرانت‌متر ناقص + همپوشانی با اسکیل‌های ریویو |
| ECC/social-publisher | ردشده — وابسته به SocialClaw/API متا (سرویس خارجی پولی) |

فهرست کامل نصب‌شده‌های خارجی: `ls /home/z/my-project/skills/*/.provenance.json`

## نگهداری

- کلمات کلیدی/حذفی‌ها را در سرِ فایل hunt.py به‌روز کن وقتی حوزهٔ کاری کاربر تغییر کرد
- برای به‌روزرسانی اسکیل نصب‌شده: `hunt.py install <repo> --skills <name>` روی شای جدید (پوشهٔ هم‌نام را اول دستی پاک کن)
