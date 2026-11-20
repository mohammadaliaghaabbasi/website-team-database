#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Collect real GitHub star counts + descriptions for a curated repo list.
Results -> data/gh_data.json (safe to re-run, resumes)."""
import json, re, subprocess, time, os

OUT = "data/gh_data.json"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"

# (repo, Persian note) — verified owner/name pairs only.
REPOS = {
  "01-استراتژی و مدیریت": {
    "مدیریت پروژه و مستندسازی": [
      ("mermaid-js/mermaid", "دیاگرام‌سازی فلوچارت و معماری (doc-as-code)"),
      ("hoppscotch/hoppscotch", "تست و مستندسازی API، جایگزین متن‌باز Postman"),
      ("github-changelog-generator/github-changelog-generator", "تولید خودکار تغییرات پروژه (Changelog)"),
      ("plantuml/plantuml", "رسم دیاگرام UML از متن ساده"),
      ("dbdiagram-io/dbml", "زبان مدل‌سازی و مستندسازی دیتابیس"),
      ("appsmithorg/appsmith", "ساخت پنل ادمین و ابزار داخلی بدون کد"),
      ("outline/outline", "ویکی و دانش‌نامه تیمی"),
    ],
  },
  "02-تحقیق کاربر": {
    "ابزار تحقیق و تحلیل رفتار": [
      ("formbricks/formbricks", "نظرسنجی و تحقیق کاربر متن‌باز"),
      ("posthog/posthog", "تحلیل رفتار کاربر، ضبط جلسه و فیچر فلگ"),
      ("umami-software/umami", "آنالیتیکس سبک و حریم‌خصوصی‌محور"),
      ("matomo-org/matomo", "جانشین متن‌باز Google Analytics"),
      ("plausible/analytics", "آنالیتیکس ساده و بدون کوکی"),
    ],
  },
  "03-برندینگ": {
    "ابزار برندینگ بصری": [
      ("excalidraw/excalidraw", "وایت‌برد طراحی دستی برای کانسپت برند"),
      ("processing/p5.js", "طراحی خلاقانه و ژنراتیو آرت"),
      ("fontsource/fontsource", "مخزن فونت‌های وب برای هویت تایپوگرافی"),
      ("googlefonts/fontmake", "طراحی و ساخت فونت اختصاصی"),
    ],
  },
  "04-طراحی UX": {
    "ابزار UX": [
      ("penpot/penpot", "طراحی و پروتوتایپ متن‌باز، جانشین Figma"),
      ("tldraw/tldraw", "بوم طراحی بی‌نهایت برای وایرفریم"),
      ("drawdb-io/drawdb", "طراحی آنلاین ERD و دیاگرام — ترند"),
      ("excalidraw/excalidraw", "وایرفریم و اسکچ سریع دستی"),
      ("style-dictionary/style-dictionary", "مدیریت توکن‌های دیزاین سیستم"),
    ],
  },
  "05-طراحی UI": {
    "کتابخانه‌های کامپوننت": [
      ("shadcn-ui/ui", "کامپوننت‌های کپی‌شدنی — ترند طلایی ۲۰۲۴-۲۰۲۵"),
      ("ant-design/ant-design", "سیستم کامپوننت سازمانی React"),
      ("mui/material-ui", "پیاده‌سازی Material Design برای React"),
      ("radix-ui/primitives", "کامپوننت‌های پایه دسترس‌پذیر بدون استایل"),
      ("chakra-ui/chakra-ui", "کامپوننت‌های مدرن با پشتیبانی RTL"),
      ("adobe/react-spectrum", "سیستم کامپوننت دسترس‌پذیر Adobe"),
      ("marmelab/react-admin", "پنل ادمین آماده برای React"),
    ],
    "دیزاین سیستم": [
      ("storybookjs/storybook", "مستندسازی و تست بصری کامپوننت‌ها"),
    ],
    "موشن و سه‌بعدی": [
      ("motion-dev/motion", "کتابخانه انیمیشن Motion (Framer Motion سابق)"),
      ("pmndrs/react-three-fiber", "رندر Three.js با React — وب سه‌بعدی"),
      ("theatre-js/theatre", "انیمیشن با محیط ویرایش بصری حرفه‌ای"),
      ("d3/d3", "ویژوالایز داده‌های پیچیده"),
      ("chartjs/Chart.js", "چارت‌های آماده جاوااسکریپت"),
    ],
  },
  "06-تولید محتوا و CMS": {
    "ویرایشگر محتوا": [
      ("microsoft/monaco-editor", "ادیتور کد وب — همان VS Code"),
      ("toeverything/AFFiNE", "نوشتن و همکاری تیمی روی محتوا"),
      ("siyuan-note/siyuan", "نوشتن بلوکی و مدیریت دانش شخصی"),
    ],
    "CMS": [
      ("strapi/strapi", "هدلس CMS پیشرو جاوااسکریپت"),
      ("directus/directus", "CMS داده‌محور روی هر دیتابیس SQL"),
      ("payloadcms/payload", "CMS تایپ‌اسکریپتی مدرن"),
      ("sanity-io/sanity", "پلتفرم محتوای ساخت‌یافته"),
      ("wagtail/wagtail", "CMS پایتونی دوستدار سئو"),
      ("tryghost/ghost", "نشر محتوا و خبرنامه"),
      ("keystonejs/keystone", "CMS و پلتفرم اپلیکیشن گراف‌محور"),
    ],
    "مدیریت رسانه": [
      ("immich-app/immich", "مدیریت عکس و ویدیو با AI — پرترند گیت‌هاب"),
      ("photoprism/photoprism", "گالری عکس هوشمند شخصی"),
    ],
  },
  "07-فرانت‌اند": {
    "کتابخانه‌ها و فریمورک‌ها": [
      ("facebook/react", "محبوب‌ترین کتابخانه UI جهان"),
      ("vuejs/vue", "فریمورک پیشرونده جاوااسکریپت"),
      ("angular/angular", "فریمورک کامل سازمانی گوگل"),
      ("sveltejs/svelte", "کامپایل‌محور و فوق‌سبک"),
      ("solidjs/solid", "کارایی بالاتر از React با API آشنا"),
      ("preactjs/preact", "جایگزین ۳ کیلوبایتی React"),
    ],
    "متافریمورک": [
      ("vercel/next.js", "متافریمورک شماره یک React"),
      ("nuxt/nuxt", "متافریمورک پیشرو Vue"),
      ("remix-run/remix", "وب استاندارد-محور از سازندگان React Router"),
      ("qwik-dev/qwik", "بارگذاری صفر جاوااسکریپت — آینده‌نگر"),
      ("withastro/astro", "سایت‌ساز جزیره‌ای محتوا-محور — ترند"),
    ],
    "زبان و ابزار ساخت": [
      ("microsoft/TypeScript", "جاوااسکریپت تایپ‌دار — استاندارد صنعت"),
      ("tailwindlabs/tailwindcss", "CSS utility-first محبوب تاریخ"),
      ("vitejs/vite", "ابزار ساخت نسل جدید فرانت‌اند"),
      ("evanw/esbuild", "باندلر فوق‌سریع نوشته‌شده با Go"),
      ("web-infra-dev/rspack", "باندلر سازگار Webpack با Rust"),
      ("webpack/webpack", "باندلر کلاسیک صنعت"),
    ],
  },
  "08-بک‌اند": {
    "Node.js": [
      ("expressjs/express", "فریمورک وب مینیمال و پراستفاده Node"),
      ("fastify/fastify", "فریمورک پرسرعت Node"),
      ("nestjs/nest", "فریمورک سازمانی تایپ‌اسکریپتی"),
      ("koajs/koa", "نسل بعدی فریمورک Express"),
      ("gofiber/fiber", "Express مانند، ساخته‌شده بر Fasthttp"),
      ("honojs/hono", "فریمورک فوق‌سبک چند-رانتایم — داغ ۲۰۲۵"),
      ("socketio/socket.io", "ارتباط بلادرنگ WebSocket"),
    ],
    "Python": [
      ("django/django", "فریمورک کامل پایتون — باتری‌همراه"),
      ("pallets/flask", "میکروفریمورک کلاسیک پایتون"),
      ("fastapi/fastapi", "API مدرن با تایپ‌ها — ترند پایتون"),
      ("encode/django-rest-framework", "REST برای جنگو"),
      ("encode/starlette", "ASGI پایه پرسرعت"),
    ],
    "PHP": [
      ("laravel/framework", "فریمورک PHP با اکوسیستم کامل"),
      ("symfony/symfony", "فریمورک PHP سازمانی"),
      ("slimphp/Slim", "میکروفریمورک PHP"),
      ("PHPMailer/PHPMailer", "ارسال ایمیل استاندارد PHP"),
    ],
    "Go و Java و C#": [
      ("gin-gonic/gin", "فریمورک Go پراستفاده"),
      ("go-chi/chi", "روتر سبک و استاندارد Go"),
      ("spring-projects/spring-boot", "فریمورک غول جاوا"),
      ("quarkusio/quarkus", "جاوا بومی-کلود نسل جدید"),
      ("dotnet/aspnetcore", "فریمورک وب مایکروسافت"),
    ],
    "Rust": [
      ("tokio-rs/axum", "فریمورک وب ماژولار Rust"),
      ("actix/actix-web", "فریمورک Rust پرسرعت"),
    ],
    "API و پیام‌رسانی": [
      ("grpc/grpc", "فریمورک RPC مدرن گوگل"),
      ("graphql/graphql-js", "پیاده‌سازی مرجع GraphQL"),
      ("rabbitmq/rabbitmq-server", "صف پیام کلاسیک"),
      ("apache/kafka", "استریم توزیع‌شده رویدادها"),
      ("redis/redis", "کش در حافظه و صف سبک"),
    ],
    "احراز هویت": [
      ("keycloak/keycloak", "مدیریت هویت سازمانی Red Hat"),
      ("goauthentik/authentik", "مدیریت هویت و SSO متن‌باز"),
      ("authelia/authelia", "احراز هویت دو مرحله‌ای و SSO"),
      ("nextauthjs/next-auth", "احراز هویت آماده Next.js (Auth.js)"),
    ],
  },
  "09-دیتابیس": {
    "SQL": [
      ("postgres/postgres", "دیتابیس رابطه‌ای پیشرفته جهان"),
      ("mysql/mysql-server", "دیتابیس پرکاربرد وب"),
      ("sqlite/sqlite", "دیتابیس فایل‌محور سبک"),
      ("timescale/timescaledb", "پستگرس برای داده سری-زمانی"),
      ("cockroachdb/cockroach", "SQL توزیع‌شده مقیاس‌پذیر"),
    ],
    "NoSQL": [
      ("mongodb/mongo", "دیتابیس سند-محور محبوب"),
      ("clickhouse/clickhouse", "OLAP فوق‌سریع ستونی"),
      ("influxdata/influxdb", "دیتابیس سری-زمانی"),
      ("supabase/supabase", "پستگرس + API آماده — محبوب ۲۰۲۵"),
    ],
    "ORM": [
      ("prisma/prisma", "ORM تایپ‌اسکریپتی محبوب"),
      ("drizzle-team/drizzle-orm", "ORM سبک SQL-محور — ترند"),
    ],
  },
  "10-فروشگاهی": {
    "پلتفرم فروشگاه": [
      ("medusajs/medusa", "کامرس هدلس ماژولار — ترند ۲۰۲۵"),
      ("saleor/saleor", "کامرس GraphQL-محور"),
      ("woocommerce/woocommerce", "فروشگاه وردپرسی پراستفاده"),
      ("sylius/sylius", "کامرس PHP مبتنی بر Symfony"),
      ("vendure-ecommerce/vendure", "کامرس هدلس تایپ‌اسکریپتی"),
      ("spree/spree", "کامرس کلاسیک Rails"),
      ("stripe/stripe-node", "SDK رسمی درگاه Stripe"),
    ],
  },
  "11-امنیت": {
    "امنیت وب": [
      ("OWASP/CheatSheetSeries", "مرجع کامل امنیت وب OWASP"),
      ("trufflesecurity/trufflehog", "کشف کلیدهای لو رفته در گیت"),
      ("aquasecurity/trivy", "اسکن آسیب‌پذیری کد و کانتینر"),
      ("wazuh/wazuh", "پلتفرم امنیت و مانیتورینگ تهدید"),
      ("hashicorp/vault", "مدیریت رمز و اسرار سازمانی"),
      ("fail2ban/fail2ban", "محافظت از حملات Brute Force"),
    ],
    "تست نفوذ": [
      ("sqlmapproject/sqlmap", "تست خودکار تزریق SQL"),
      ("zaproxy/zaproxy", "اسکنر امنیتی OWASP ZAP"),
      ("nmap/nmap", "اسکنر شبکه و پورت افسانه‌ای"),
    ],
    "WAF و وب‌سرور امن": [
      ("coreruleset/coreruleset", "قوانین WAF استاندارد ModSecurity"),
      ("caddyserver/caddy", "وب‌سرور با HTTPS خودکار"),
    ],
  },
  "12-تست و QA": {
    "تست خودکار": [
      ("microsoft/playwright", "تست E2E چندمرورگری — ترند اول"),
      ("cypress-io/cypress", "تست E2E محبوب توسعه‌دهندگان"),
      ("SeleniumHQ/selenium", "پدر تست خودکار وب"),
      ("puppeteer/puppeteer", "کنترل کروم هدلس از گوگل"),
      ("testing-library/react-testing-library", "تست رفتار کامپوننت React"),
      ("vitest-dev/vitest", "تست واحد نسل جدید Vite"),
      ("jestjs/jest", "تست واحد کلاسیک جاوااسکریپت"),
      ("pytest-dev/pytest", "استاندارد تست پایتون"),
    ],
    "تست بار": [
      ("grafana/k6", "تست بار اسکریپت‌پذیر گرافانا"),
      ("locustio/locust", "تست بار توزیع‌شده پایتونی"),
    ],
  },
  "13-DevOps": {
    "کانتینر": [
      ("moby/moby", "موتور Docker متن‌باز"),
      ("kubernetes/kubernetes", "ارکستریتور کانتینر غول"),
      ("k3s-io/k3s", "کوبرنتیز سبک لبه و IoT"),
      ("portainer/portainer", "مدیریت گرافیکی کانتینر"),
      ("goharbor/harbor", "رجیستری ایمیمن کانتینر ابری"),
    ],
    "CI/CD": [
      ("actions/runner", "رانر GitHub Actions خودمیزبان"),
      ("argoproj/argo-cd", "استقرار GitOps کوبرنتیز"),
      ("woodpecker-ci/woodpecker", "CI/CD متن‌باز خودمیزبان"),
      ("drone/drone", "CI/CD کانتینری کلاسیک"),
    ],
    "زیرساخت به‌کد": [
      ("hashicorp/terraform", "زیرساخت به‌صورت کد — استاندارد"),
      ("pulumi/pulumi", "زیرساخت با زبان‌های برنامه‌نویسی واقعی"),
      ("ansible/ansible", "اتوماسیون پیکربندی سرور"),
    ],
    "مانیتورینگ": [
      ("grafana/grafana", "داشبورد مانیتورینگ استاندارد صنعت"),
      ("prometheus/prometheus", "پایش متریک و هشدار"),
      ("grafana/loki", "تجمع لاگ سبک گرافانا"),
      ("netdata/netdata", "مانیتورینگ بلادرنگ سرور"),
    ],
    "وب‌سرور و پروکسی": [
      ("nginx/nginx", "وب‌سرور و ریورس‌پروکسی کلاسیک"),
      ("traefik/traefik", "ریورس‌پروکسی مدرن کانتینری"),
    ],
    "ابر و شبیه‌ساز": [
      ("localstack/localstack", "شبیه‌ساز کامل AWS روی سیستم شما"),
      ("minio/minio", "ذخیره‌سازی سازگار S3 خودمیزبان"),
    ],
  },
  "14-سئو": {
    "ابزار سئو و جستجو": [
      ("GoogleChrome/lighthouse", "ممیزی سئو، عملکرد و دسترس‌پذیری گوگل"),
      ("meilisearch/meilisearch", "جستجوی فوری سایت — تجربه گوگل‌مانند"),
      ("typesense/typesense", "موتور جستجوی سریع و کم‌حافظه"),
      ("iamvishnusankar/next-sitemap", "سایت‌مپ خودکار برای Next.js"),
    ],
  },
  "15-عملکرد": {
    "بهینه‌سازی سرعت": [
      ("lovell/sharp", "پردازش و فشرده‌سازی تصویر فوق‌سریع"),
      ("GoogleChrome/web-vitals", "سنجه‌های حیاتی سرعت از گوگل"),
      ("kevva/imagemin", "فشرده‌سازی تصاویر وب"),
      ("webp-sh/webp_server_go", "سرو تصویر WebP خودکار"),
    ],
  },
  "16-آنالیتیکس": {
    "تحلیل و رشد": [
      ("growthbook/growthbook", "A/B تست و فیچر فلگ متن‌باز"),
      ("flagsmith/flagsmith", "فیچر فلگ و آزمایش سرویس‌ها"),
      ("shlinkio/shlink", "کوتاه‌کننده لینک با آمار کامل"),
    ],
  },
  "17-حقوقی": {
    "انطباق و حریم خصوصی": [
      ("Lissy93/web-check", "بررسی امنیت و اطلاعات عمومی سایت"),
      ("Osano/cookieconsent", "بنر رضایت کوکی GDPR"),
    ],
  },
  "18-پشتیبانی": {
    "کمک‌دسک و انجمن": [
      ("chatwoot/chatwoot", "پشتیبانی چندکاناله متن‌باز"),
      ("discourse/discourse", "انجمن گفتگو استاندارد جهان"),
      ("zammad/zammad", "کمک‌دسک تیکتینگ حرفه‌ای"),
      ("glpi-project/glpi", "مدیریت خدمات ITIL"),
      ("freescout-help-desk/freescout", "کمک‌دسک سبک ایمیلی"),
      ("peppermint-sh/peppermint", "تیکتینگ مدرن خودمیزبان"),
      ("docmost/docmost", "مستندات و ویکی تیمی"),
      ("BookStackApp/BookStack", "ویکی سازمانی ساده و منظم"),
    ],
    "بکاپ و آپ‌تایم": [
      ("restic/restic", "بکاپ رمزنگاری‌شده مدرن"),
      ("duplicati/duplicati", "بکاپ ابری زمان‌بندی‌شده"),
      ("louislam/uptime-kuma", "مانیتور آپ‌تایم خودمیزبان محبوب"),
    ],
  },
  "19-بازاریابی": {
    "ایمیل و اتوماسیون": [
      ("listmonk-app/listmonk", "خبرنامه و ایمیل مارکتینگ خودمیزبان"),
      ("mautic/mautic", "اتوماسیون مارکتینگ متن‌باز"),
      ("novuhq/novu", "نوتیفیکیشن مولتی‌کانال اینباکس و پوش"),
    ],
    "سوشال مدیا": [
      ("postizapp/postiz", "مدیریت پست سوشال مدیا متن‌باز — ترند"),
      ("mixpost/mixpost", "زمان‌بند سوشال مدیا خودمیزبان"),
    ],
  },
}

def fetch_repo(fullname):
    name = fullname.strip()
    url = f"https://github.com/{name}"
    try:
        r = subprocess.run(
            ["curl", "-s", "--max-time", "25", "-H", f"User-Agent: {UA}",
             "-H", "Accept: text/html", url],
            capture_output=True, text=True, timeout=40)
        html = r.stdout
        if not html or len(html) < 50000:
            return {"ok": False, "stars": None, "desc_en": "", "err": f"short page ({len(html)}b)"}
        m = re.search(r'<strong>([\d.,]+)(k?)</strong>\s*stars', html)
        stars = None
        if m:
            num, suf = m.group(1), m.group(2)
            try:
                stars = int(float(num.replace(",", "")) * (1000 if suf == "k" else 1))
            except ValueError:
                pass
        d = re.search(r'og:description" content="([^"]+)"', html)
        desc_en = ""
        if d:
            desc_en = d.group(1).split(". Contribute to")[0].strip()
        return {"ok": stars is not None, "stars": stars, "desc_en": desc_en,
                "err": None if stars is not None else "star pattern not found"}
    except subprocess.TimeoutExpired:
        return {"ok": False, "stars": None, "desc_en": "", "err": "timeout"}
    except Exception as e:
        return {"ok": False, "stars": None, "desc_en": "", "err": str(e)}

def main():
    data = {}
    if os.path.exists(OUT):
        try:
            data = json.load(open(OUT, encoding="utf-8"))
        except Exception:
            data = {}
    all_repos = {}
    for cat, groups in REPOS.items():
        if not isinstance(groups, dict):
            continue
        for group, items in groups.items():
            for full, note in items:
                if isinstance(full, tuple):
                    full = full[0]
                if full:
                    all_repos[full.strip()] = note
    print(f"Unique repos: {len(all_repos)}", flush=True)
    todo = [r for r in all_repos if r not in data or not data[r].get("ok")]
    print(f"To fetch: {len(todo)}", flush=True)
    for i, name in enumerate(todo, 1):
        res = fetch_repo(name)
        data[name] = res
        status = f"{res['stars']:,}" if res.get("ok") else f"FAIL:{res.get('err')}"
        print(f"[{i}/{len(todo)}] {name}: {status}", flush=True)
        if i % 10 == 0:
            json.dump(data, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        time.sleep(2.0)
    json.dump(data, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    ok = [r for r in data if data[r].get("ok")]
    print(f"\nDONE ok={len(ok)}/{len(data)}")
    for r, v in data.items():
        if not v.get("ok"):
            print(f"  FAIL {r}: {v.get('err')}")

if __name__ == "__main__":
    main()
