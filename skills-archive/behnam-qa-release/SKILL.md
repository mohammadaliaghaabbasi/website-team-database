# اسکیل دامنهٔ کیفیت، رگرسیون و رلیز — چاپ بهنام

## نقش
قانون‌گذار چرخهٔ رلیز سایت چاپ بهنام: بامپ Service Worker → رگرسیون کامل → build → دیپلوی Cloudflare Pages → پراب تولیدی → commit/push → ورک‌لاگ. هیچ تغییری «تمام‌شده» نیست تا این چرخه سبز نشده باشد. این اسکیل داور نهایی «تغییر نکن تا رگرسیون سبز شود» است.

## قوانین تخصصی (نمیشکند!)
- رگرسیون کامل قبل از هر دیپلوی، به همین ترتیب: `npm run lint` (ESLint + tsc --noEmit) → `npm run test` (Vitest) → `npm run e2e` (Playwright) → `npm run build`. حتی یک قرمز = بدون دیپلوی.
- بامپ SW **همیشه قبل از build** انجام شود، نه بعد از آن (خطای تکراری گذشته): در `public/sw.js` نسخهٔ فعلی `behnam-print-vNN` خوانده و به `vNN+1` تبدیل می‌شود. نسخهٔ لایو فعلی مرجع است، نه حافظه.
- توکن Cloudflare هرگز چاپ/لاگ/commit نمی‌شود؛ استخراج با: `export CLOUDFLARE_API_TOKEN=$(python3 -c "import re;print(re.search(r'NEW_TOKEN\s*=\s*[\"\x27]([^\"\x27]+)',open('/home/z/my-project/scripts/update-gh-secrets.py').read()).group(1))")` و `export CLOUDFLARE_ACCOUNT_ID=5e127b8d385ee8dbfa4079e606cd4793`.
- دیپلوی: `wrangler pages deploy dist --project-name=chap-behnam --branch=main` (بعد از build). مخزن: `mohammadaliaghaabbasi/Chap-behnam` (PAT داخل remote URL — هرگز در خروجی نمایش داده نشود).
- پراب تولیدی اجباری پس از هر دیپلوی: `https://chap-behnam-6eg.pages.dev/` = 200؛ `/sw.js` شامل نسخهٔ جدید `behnam-print-vNN`؛ `/api/bootstrap` = 200 و `ok:true`؛ `/api/seed` بدون توکن = 403 (گارد موج ۲۰)؛ مقایسهٔ نام فایل باندل `dist/index.html` با `index.html` لایو (باید MATCH باشد).
- آزمون گارد دائمی: الگوی `readFileSync` + استخراج بین دو نشانه + regex assertions (نمونه‌ها: `src/__tests__/sprint27*.test.ts`). هر وصلهٔ امنیتی/رفع معیوب باید گارد آزمون داشته باشد تا رگرسیون بعدی نقضش را بگیرد. نام‌گذاری بر اساس موج: sprint26/27/...
- کارهای نیمه‌کاره فقط با کد به ترانک می‌روند؛ رفتار دمو باید پس از هر رلیز روی تولید با لاگین واقعی تست شود.
- اصل بنیادین کارفرما: **هیچ قابلیتی حذف/تخریب نمی‌شود؛ دموی ورود مشتری و پرسنل حفظ اجباری است.** هر رگرسیونی که این را نقض کند، رلیز را متوقف می‌کند.
- پیام خطای کاربر-رو فارسی باشد؛ تغییرات UI با رشدهای تاریخی سازگار بماند (RTL، برچسب‌ها).

## چک‌لیست دیباگ (پروتکل رلیز)
1. `grep -oE "behnam-print-v[0-9]+" public/sw.js` → نسخهٔ فعلی؛ +1 کن.
2. `npm run lint && npm run test && npm run e2e && npm run build` — همه سبز.
3. توکن‌ها را export کن؛ `wrangler pages deploy dist --project-name=chap-behnam --branch=main`.
4. پراب: `curl -s -o /dev/null -w "%{http_code}" https://chap-behnam-6eg.pages.dev/` و `/sw.js` و `/api/bootstrap` و `curl -s -X POST .../api/seed` (انتظار 403).
5. `curl -s .../index.html | grep -oE "assets/index-[^\"']+"` را با `dist/index.html` مقایسه کن → MATCH.
6. `git add -A && git commit && git push`؛ CI گیت‌هاب (Deploy Workers) باید سبز شود.
7. سکشن ورک‌لاگ بنویس (Task ID، رگرسیون‌ها، SW، hash، نتیجهٔ پراب).

## قراردادهای بین‌بخشی (مذاکره با اسکیل‌های دیگر)
- ورودی از همهٔ اسکیل‌های دامنه: هر وصله با گارد آزمون sprintNN — نشانهٔ شکست: رگرسیون قرمز یا گارد مفقود.
- خروجی به behnam-debug-orchestra: وضعیت سبز/قرمز چرخه + نسخهٔ لایو — منبع حقیقتِ «چه چیزی روی تولید است».
- خروجی به behnam-staff-management: تأیید سلامت دموی ورود پرسنل روی تولید پس از هر رلیز.
- ورودی از behnam-rbac: پراب‌های گارد امنیتی (seed 403، uploads بدون نشست 404، bootstrap برش‌خورده) در هر رلیز چک می‌شوند.

## فایل‌ها
package.json (scripts) · playwright.config.ts · src/__tests__/ (گاردهای sprintNN) · e2e/ (سناریوها) · public/sw.js · scripts/update-gh-secrets.py (فقط منبع توکن)

## ممنوع
- دیپلوی با رگرسیون قرمز یا بدون پراب؛ بامپ SW بعد از build؛ چاپ/لاگ توکن و PAT؛ حذف آزمون گارد برای «سبزراه‌کردن»؛ حذف دموی ورود مشتری/پرسنل؛ ادعای رلیز بدون ورک‌لاگ.
