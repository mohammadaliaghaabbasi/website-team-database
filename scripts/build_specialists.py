#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build specialists_data.json — 52 role cards for the docx simulator document."""
import json

S = []

def add(role, roleEn, section, mission, skills, stack, practice, path, interview):
    S.append({
        "role": role, "roleEn": roleEn, "section": section, "mission": mission,
        "skills": skills, "stack": [{"name": n, "repo": r} for n, r in stack],
        "practice": [{"name": n, "url": u, "note": note} for n, u, note in practice],
        "path": path, "interview": interview,
    })

# ================= 1. استراتژی و مدیریت =================
add("مدیر پروژه دیجیتال", "Digital Project Manager", "مرحله ۱ — استراتژی و مدیریت",
    "هماهنگی کل چرخه ساخت سایت از نیازمندی تا انتشار و نگهداشت",
    ["تخمین زمان و بودجه با روش‌های Agile", "مدیریت اسپرینت و رترواسپکتیو", "ابزارهای Kaban و برد تسک",
     "مستندسازی تصمیمات و ADR", "مدیریت ریسک و وابستگی‌ها", "ارتباط مؤثر با ذی‌نفعان"],
    [("GitHub Projects (بورد پروژه)", "github/features/issues"), ("Excalidraw (نقشه راه)", "excalidraw/excalidraw"),
     ("Outline (دانش‌نامه تیم)", "outline/outline"), ("Mermaid (دیاگرام流程)", "mermaid-js/mermaid")][:0] or
    [("Outline (دانش‌نامه تیم)", "outline/outline"), ("Mermaid (دیاگرام فرآیند)", "mermaid-js/mermaid")],
    [("GitHub Projects", "github.com/features/issues", "برد کانبان و اسپرینت داخل گیت‌هاب"),
     ("OpenProject", "openproject.org", "مدیریت پروژه متن‌باز"),
     ("Excalidraw", "excalidraw.com", "وایت‌برد نقشه راه و رترو")],
    ["یادگیری Scrum و Kanban (۱ ماه)", "راه‌اندازی برد پروژه و مستندات تیم (۱ ماه)",
     "مدیریت نخستین پروژه کوچک ۳-نفره (۳ ماه)", "اخذ گواهی PMP یا CSM (اختیاری)"],
    "پروژه‌ای ۲ هفته‌ای از برنامه عقب افتاده؛ سه عضو تیم منتظر تسک هستند. چه اقداماتی به ترتیب انجام می‌دهید؟")

add("مدیر محصول", "Product Owner", "مرحله ۱ — استراتژی و مدیریت",
    "تعیین چه چیزی ساخته شود و با چه اولویتی — مالک Backlog",
    ["نوشتن User Story و معیار پذیرش", "اولویت‌بندی با RICE و MoSCoW", "تحلیل داده محصول",
     "ساخت MVP و آزمون فرضیه", "مدیریت انتظارات ذی‌نفعان", "نقشه راه محصول"],
    [("PostHog (تحلیل محصول)", "posthog/posthog"), ("Appsmith (پنل داخلی)", "appsmithorg/appsmith")],
    [("PostHog", "posthog.com", "فیچر فلگ و تحلیل رفتار کاربر"),
     ("DrawDB", "drawdb.app", "طراحی فلوچارت فرآیند محصول")],
    ["یادگیری چارچوب‌های اولویت‌بندی (۱ ماه)", "نوشتن ۲۰ User Story واقعی (۱ ماه)",
     "ساخت MVP با فرم نظرسنجی و Landing (۲ ماه)", "تحلیل داده و تکرار محصول (مداوم)"],
    "چگونه تصمیم می‌گیرید کدام فیچر برای نسخه اول سایت انتخاب شود؟ روش RICE را روی یک مثال توضیح دهید.")

add("تحلیلگر کسب‌وکار", "Business Analyst", "مرحله ۱ — استراتژی و مدیریت",
    "ترجمه نیاز کسب‌وکار به مستندات فنی قابل اجرا برای تیم توسعه",
    ["تحلیل و مدل‌سازی فرآیند (BPMN)", "نوشتن SRS و مستندات نیازمندی", "مصاحبه با ذی‌نفعان",
     "تحلیل فاصله (Gap Analysis)", "مدیریت تغییر نیازمندی‌ها", "اسناد قابلیت نگهداشت"],
    [("Mermaid (دیاگرام BPMN)", "mermaid-js/mermaid"), ("PlantUML (یو‌ام‌ال)", "plantuml/plantuml"),
     ("DBML (مدل داده)", "dbdiagram-io/dbml")],
    [("PlantUML Web", "plantuml.com", "نوشتن دیاگرام فرآیند به کد"),
     ("DrawDB", "drawdb.app", "طراحی ERD و فلوچارت"),
     ("Balsamiq trial", "balsamiq.com", "ماکاپ سریع مستندات")],
    ["یادگیری نمادهای BPMN و UML (۱ ماه)", "مستندسازی یک فرآیند واقعی کسب‌وکار (۱ ماه)",
     "مصاحبه با ۵ ذی‌نفع و استخراج نیاز (۲ ماه)", "تسلط بر SRS و مدیریت تغییر (۲ ماه)"],
    "ذی‌نفعی نیاز متناقض با تیم فنی مطرح می‌کند. چطور بدون آسیب به رابطه آن را مدیریت می‌کنید؟")

add("مشاور استراتژی دیجیتال", "Digital Strategy Consultant", "مرحله ۱ — استراتژی و مدیریت",
    "تعیین مسیر درآمد و رشد سایت هم‌راستا با اهداف کسب‌وکار",
    ["طراحی مدل درآمدی (اشتراک/تبلیغ/فروش)", "تحلیل بازار و جایگاه‌یابی", "تعریف KPI های شمال",
     "استراتژی قیمت‌گذاری", "تحلیل SWOT دیجیتال", "طراحی قیف فروش"],
    [("PostHog (کشف رفتار)", "posthog/posthog"), ("Umami (آمار سبک)", "umami-software/umami")],
    [("GA4 Demo Account", "analytics.google.com", "حساب دمو با داده واقعی"),
     ("Looker Studio", "lookerstudio.google.com", "ساخت داشبورد KPI")],
    ["مطالعه مدل‌های درآمدی وب (۱ ماه)", "تحلیل ۵ سایت موفق حوزه هدف (۱ ماه)",
     "تعریف KPI و داشبورد برای یک کسب‌وکار واقعی (۲ ماه)"],
    "سایتی ترافیک بالا اما نرخ تبدیل ۰/۲٪ دارد. چه فرضیه‌هایی مطرح و چگونه آزمایش می‌کنید؟")

# ================= 2. تحقیق و تجربه کاربر =================
add("پژوهشگر تجربه کاربر", "UX Researcher", "مرحله ۲ — تحقیق کاربر",
    "کشف نیاز و رفتار واقعی کاربران با روش‌های علمی پژوهش",
    ["مصاحبه عمیق و کاردسورتینگ", "طراحی پرسشنامه و تحلیل آماری", "ساخت پرسونا",
     "تست استفاده‌پذیری THINK ALOUD", "تحقیق ثانویه و رقبا", "ترجمه یافته‌ها به بینش طراحی"],
    [("Formbricks (نظرسنجی درون‌محصولی)", "formbricks/formbricks"),
     ("Umami (تحلیل ناشناس)", "umami-software/umami"), ("Matomo", "matomo-org/matomo")],
    [("Microsoft Clarity", "clarity.microsoft.com", "ضبط جلسه و هیت‌مپ رایگان"),
     ("Google Forms", "forms.google.com", "پرسشنامه پرسونا"),
     ("Hotjar free", "hotjar.com", "هیت‌مپ رفتار کاربر")],
    ["یادگیری روش‌های پژوهش کیفی (۱ ماه)", "اجرای ۵ مصاحبه کاربر واقعی (۱ ماه)",
     "تحلیل داده و ساخت پرسونا (۱ ماه)", "گزارش بینش و ارائه به تیم طراحی (مداوم)"],
    "چه زمانی بین مصاحبه کیفی و نظرسنجی کمّی یکی را انتخاب می‌کنید؟ برای هر کدام یک سناریو بگویید.")

add("معمار اطلاعات", "Information Architect", "مرحله ۲ — تحقیق کاربر",
    "ساختاردهی محتوا و ناوبری سایت برای یافتن آسان اطلاعات",
    ["کاردسورتینگ و تکسونومی", "طراحی سایت‌مپ و ناوبری", "لیبل‌گذاری و الگوی نام‌گذاری",
     "فلو کاربر (User Flow)", "بهینه‌سازی جستجوی درون‌سایتی", "دسترس‌پذیری ساختار"],
    [("Excalidraw (فلو)", "excalidraw/excalidraw"), ("DrawDB (ساختار)", "drawdb-io/drawdb")],
    [("Optimal Workshop trial", "optimalworkshop.com", "کاردسورتینگ آنلاین"),
     ("tldraw", "tldraw.com", "بوم فلو کاربر"),
     ("Penpot", "penpot.app", "وایرفریم ساختار")],
    ["یادگیری اصول IA و تکسونومی (۱ ماه)", "اجرای کاردسورتینگ با ۱۵ کاربر (۱ ماه)",
     "طراحی سایت‌مپ کامل یک سایت واقعی (۱ ماه)", "تست ناوبری و تکرار (مداوم)"],
    "کاربران در آزمون درخت، مسیر اشتباهی برای یافتن محصول می‌روند. چگونه ساختار را اصلاح می‌کنید؟")

add("تستر استفاده‌پذیری", "Usability Tester", "مرحله ۲ — تحقیق کاربر",
    "ارزیابی سیستماتیک سایت با کاربران واقعی پیش از انتشار",
    ["طراحی سناریو و تسک تست", "روش Think-Aloud و ثبت مشاهده", "تحلیل HEURISTIC نیلسن",
     "متریک‌های SUS و NPS", "گزارش‌دهی یافته‌ها با اولویت", "تست دورکاری مودریت‌نشده"],
    [("Umami (تحلیل رفتار)", "umami-software/umami"), ("PostHog (ضبط جلسه)", "posthog/posthog")],
    [("Microsoft Clarity", "clarity.microsoft.com", "مشاهده رفتار واقعی کاربران"),
     ("Hotjar", "hotjar.com", "ضبط جلسه و نظرسنجی")],
    ["یادگیری ۱۰ اصل هیوریستیک نیلسن (۲ هفته)", "ارزیابی کارشناسی ۳ سایت معروف (۱ ماه)",
     "اجرای تست با ۵ کاربر واقعی (۱ ماه)", "نوشتن گزارش حرفه‌ای و پیگیری اصلاح (مداوم)"],
    "در تست استفاده‌پذیری، کاربری نتواند سبد خرید را پیدا کند اما انصراف دهد. یافته‌ را چطور گزارش می‌کنید؟")

# ================= 3. برندینگ =================
add("طراح هویت بصری", "Brand Identity Designer", "مرحله ۳ — برندینگ",
    "خلق چهره منحصربه‌فرد برند: لوگو، رنگ، تایپوگرافی",
    ["طراحی لوگو با اصول گرید", "انتخاب پالت رنگی و روانشناسی رنگ", "جفت‌فونت فارسی/لاتین",
     "ساخت برندبوک", "طراحی الگوهای گرافیکی", "کاربردپذیری برند در دیجیتال"],
    [("Excalidraw (اسکچ)", "excalidraw/excalidraw"), ("P5.js (ژنراتیو آرت)", "processing/p5.js"),
     ("Fontsource (فونت وب)", "fontsource/fontsource")],
    [("Coolors", "coolors.co", "تولید پالت رنگی"),
     ("Google Fonts", "fonts.google.com", "جست‌وجوی فونت وب"),
     ("Penpot", "penpot.app", "طراحی وکتور لوگو")],
    ["مطالعه روانشناسی رنگ و تایپوگرافی فارسی (۱ ماه)", "تحلیل ۱۰ برند موفق حوزه هدف (۲ هفته)",
     "طراحی هویت کامل یک برند فرضی (۲ ماه)", "ساخت پورتفولیو برندینگ (۱ ماه)"],
    "برندی می‌گوید «لوگوی ما باید همه چیز درباره کسب‌وکارمان بگوید». چگونه پاسخ می‌دهید؟")

add("طراح فونت", "Type Designer", "مرحله ۳ — برندینگ",
    "طراحی حروف و فونت اختصاصی برای هویت منحصربه‌فرد",
    ["طراحی حروف روی گرید", "کشیدگی و نقطه‌گذاری فارسی", "کERNING و متریک",
     "تولید فونت وب (WOFF2)", "ساخت وزن‌های متنوع", "خوانایی در اندازه‌های ریز"],
    [("Fontmake (ساخت فونت)", "googlefonts/fontmake"), ("Fontra (ویرایش فونت)", "googlefonts/fontra")],
    [("Fontra", "fontra.org", "ویرایشگر فونت وب"),
     ("Google Fonts", "fonts.google.com", "مطالعه فونت‌های متن‌باز"),
     ("Fontsource", "fontsource.org", "بسته‌بندی فونت وب")],
    ["یادگیری آناتومی حروف فارسی (۲ ماه)", "طراحی الفبای کامل یک وزن (۳ ماه)",
     "تبدیل به فونت وب قابل استفاده (۱ ماه)", "طراحی وزن دوم و خانواده (۶ ماه)"],
    "چرا فونت اختصاصی برای یک برند منطقی است اما برای استارتاپ کوچک معمولاً نه؟")

# ================= 4. طراحی UX =================
add("طراح تجربه کاربری", "UX Designer", "مرحله ۴ — طراحی UX",
    "طراحی مسیر روان و لذت‌بخش کاربر برای رسیدن به هدف",
    ["وایرفریم و پروتوتایپ", "طراحی User Flow و Journey Map", "الگوهای طراحی UI Pattern",
     "طراحی فرم و کاهش اصطکاک", "موبایل-فرست و ریسپانسیو", "همکاری با پژوهشگر و UI"],
    [("Penpot (طراحی متن‌باز)", "penpot/penpot"), ("Excalidraw (وایرفریم)", "excalidraw/excalidraw"),
     ("Style Dictionary (توکن)", "style-dictionary/style-dictionary")],
    [("Penpot", "penpot.app", "وایرفریم و پروتوتایپ رایگان"),
     ("tldraw", "tldraw.com", "بوم طراحی فلو"),
     ("Coolors", "coolors.co", "پالت هماهنگ")],
    ["یادگیری فرآیند طراحی دوتایی (۱ ماه)", "وایرفریم‌سازی ۵ صفحه یک سایت واقعی (۱ ماه)",
     "پروتوتایپ کلیک‌خور و تست با کاربر (۱ ماه)", "تسلط بر دیزاین سیستم (۲ ماه)"],
    "دو الگوی متفاوت برای صفحه پرداخت طراحی کنید و بگویید کدام را برای فروشگاه لباس انتخاب می‌کنید و چرا.")

add("طراح تعامل", "Interaction Designer", "مرحله ۴ — طراحی UX",
    "طراحی رفتار سیستم در پاسخ به عمل کاربر",
    ["طراحی حالت‌های خالی و خطا", "میکرواینترکشن و بازخورد", "انیمیشن معنادار UI",
     "طراحی درگ‌انددراپ", "گشتالت در تعامل", "دسترس‌پذیری تعامل"],
    [("Motion (انیمیشن)", "motion-dev/motion"), ("React Aria (دسترس‌پذیری)", "adobe/react-spectrum")],
    [("Motion Docs", "motion.dev", "مستندات تعاملی انیمیشن"),
     ("Storybook", "storybook.js.org", "مرور حالت‌های کامپوننت")],
    ["مطالعه الگوهای تعامل موبایل و وب (۱ ماه)", "طراحی حالت‌های کامل یک فرم (۲ هفته)",
     "پیاده‌سازی میکرواینترکشن با Motion (۱ ماه)", "تست تعامل با کاربران (مداوم)"],
    "کاربر دکمه خرید را دوبار می‌زند چون بازخوردی نمی‌بیند. راه‌حل طراحی شما چیست؟")

add("طراح دسترس‌پذیری", "Accessibility Specialist", "مرحله ۴ — طراحی UX",
    "تضمین استفاده همه — از کم‌بینا تا حرکت‌محدود — از سایت",
    ["استاندارد WCAG 2.2", "سیمانتیک HTML و ARIA", "کنتراست و اندازه هدف لمس",
     "ناوبری کیبورد و فوکوس", "خوانندگان صفحه (Screen Reader)", "تست با کاربران دارای معلولیت"],
    [("React Spectrum (کامپوننت a11y)", "adobe/react-spectrum"), ("Radix (پایه a11y)", "radix-ui/primitives")],
    [("WebAIM WAVE", "wave.webaim.org", "ارزیابی آنلاین دسترس‌پذیری"),
     ("NVDA Screen Reader", "nvaccess.org", "خواننده صفحه رایگان"),
     ("Lighthouse a11y", "developers.google.com/web/tools/lighthouse", "ممیزی دسترس‌پذیری")],
    ["مطالعه WCAG 2.2 سطح AA (۱ ماه)", "ارزیابی ۵ سایت با WAVE (۲ هفته)",
     "رفع ۲۰ مشکل دسترس‌پذیری یک سایت واقعی (۱ ماه)", "تست با NVDA و کیبورد (مداوم)"],
    "سایتی فرم را با label پنهان و placeholder تنها منتشر کرده. چه مشکلاتی ایجاد می‌کند و چگونه رفع می‌کنید؟")

# ================= 5. طراحی UI =================
add("طراح رابط کاربری", "UI Designer", "مرحله ۵ — طراحی UI",
    "طراحی ظاهر نهایی سایت: رنگ، تایپ، کامپوننت و جزئیات",
    ["تایپوگرافی وب و سلسله‌مراتب", "پالت رنگی و کنتراست", "طراحی Grid و فاصله‌گذاری",
     "طراحی State های کامپوننت", "آیکون‌کشی و تصویرسازی", "آماده‌سازی Design Handoff"],
    [("Storybook (مستندات کامپوننت)", "storybookjs/storybook"), ("Chakra UI (کامپوننت)", "chakra-ui/chakra-ui"),
     ("Material UI", "mui/material-ui")],
    [("Penpot", "penpot.app", "طراحی UI متن‌باز"),
     ("Storybook", "storybook.js.org", "کتابخانه کامپوننت زنده"),
     ("Google Fonts Icons", "fonts.google.com/icons", "آیکون‌های استاندارد")],
    ["یادگیری اصول تایپوگرافی و رنگ (۱ ماه)", "بازطراحی UI سه سایت معروف (۱ ماه)",
     "طراحی کامل ۸ صفحه یک محصول (۲ ماه)", "ساخت دیزاین سیستم شخصی (۲ ماه)"],
    "دیزاینر UX فلو را تحویل داده. فرآیند شما از فلو تا فایل نهایی تحویل به برنامه‌نویس چگونه است؟")

add("متخصص دیزاین سیستم", "Design System Engineer", "مرحله ۵ — طراحی UI",
    "ساخت کتابخانه یکپارچه کامپوننت برای مقیاس‌پذیری طراحی",
    ["توکن‌های طراحی (رنگ/فاصله/تایپ)", "مستندسازی کامپوننت", "نسخه‌بندی و تغییرات",
     "هماهنگی طراحی-کد", "دسترس‌پذیری در مقیاس", "حکمرانی دیزاین سیستم"],
    [("Style Dictionary", "style-dictionary/style-dictionary"), ("Storybook", "storybookjs/storybook"),
     ("Radix Primitives", "radix-ui/primitives")],
    [("Storybook", "storybook.js.org", "ساخت DS با مستندات زنده"),
     ("Style Dictionary", "styledictionary.com", "مدیریت توکن چندپلتفرمی")],
    ["یادگیری معماری توکن‌ها (۱ ماه)", "ساخت DS کوچک با ۱۵ کامپوننت (۲ ماه)",
     "اتصال توکن‌ها به کد با Style Dictionary (۱ ماه)", "نسخه‌بندی و مستندسازی عمومی (مداوم)"],
    "تیم‌ها کامپوننت سفارشی خارج از دیزاین سیستم می‌سازند. چگونه انضباط را برقرار می‌کنید؟")

add("موشن دیزاینر", "Motion Designer", "مرحله ۵ — طراحی UI",
    "جان‌بخشی به رابط با انیمیشن‌های معنادار و هدفمند",
    ["اصول انیمیشن دیزنی در UI", "Timing و Easing", "انیمیشن لودینگ و انتقال صفحه",
     "SVG و Lottie", "انیمیشن RTL فارسی", "بهینه‌سازی کارایی انیمیشن"],
    [("Motion", "motion-dev/motion"), ("React Three Fiber (سه‌بعدی)", "pmndrs/react-three-fiber"),
     ("Theatre.js", "theatre-js/theatre")],
    [("Motion", "motion.dev", "تمرین تعاملی انیمیشن"),
     ("LottieFiles", "lottiefiles.com", "انیمیشن‌های آماده Lottie")],
    ["مطالعه اصول موشن (۱ ماه)", "ساخت ۱۰ میکرواینترکشن (۱ ماه)",
     "طراحی انیمیشن Onboarding کامل (۱ ماه)", "یادگیری وب سه‌بعدی با R3F (۲ ماه)"],
    "انیمیشنی زیبا اما کند دارید و مدیر محصول نگران سرعت سایت است. چه مصالحه‌ای پیشنهاد می‌دهید؟")

# ================= 6. محتوا و CMS =================
add("کپی‌رایتر وب", "Web Copywriter", "مرحله ۶ — تولید محتوا",
    "نوشتن متن‌های صفحه که بفروشند و رتبه بگیرند",
    ["نوشتن Headline و CTA", "روایت برند و لحن (Tone of Voice)", "ساختار هرم وارونه",
     "نوشتن فرم و پیام خطا", "A/B تست متن", "سئو-نویسی بدون牺牲 خوانایی"],
    [("Ghost (نشر محتوا)", "tryghost/ghost"), ("Monaco (ادیتور)", "microsoft/monaco-editor")],
    [("Hemingway", "hemingwayapp.com", "ساده‌سازی و خوانایی"),
     ("ChatGPT/Claude", "chat.openai.com", "ایده‌پردازی و پیش‌نویس")],
    ["مطالعه کلاسیک‌های کپی‌رایتینگ (۱ ماه)", "نوشتن ۱۰ لندینگ واقعی/فرضی (۲ ماه)",
     "A/B تست سرتیترها (۱ ماه)", "تخصصی‌شدن در یک صنعت (مداوم)"],
    "برای صفحه اصلی یک استارتاپ فین‌تک، سه سرتیتر متفاوت با زوایای روانی مختلف بنویسید.")

add("مدیر محتوا", "Content Manager", "مرحله ۶ — تولید محتوا",
    "برنامه‌ریزی، تقویم و انتشار محتوای مستمر سایت",
    ["تقویم محتوایی", "مدیریت تیم نویسنده", "سئو کلاستر محتوا",
     "CMS و گردش کار انتشار", "آنالیز عملکرد محتوا", "بازنویسی و به‌روزرسانی"],
    [("Strapi", "strapi/strapi"), ("Directus", "directus/directus"), ("Ghost", "tryghost/ghost")],
    [("Strapi Cloud", "strapi.io", "دموی هدلس CMS"),
     ("Obsidian", "obsidian.md", "تقویم و ایده‌های محتوا")],
    ["یادگیری اصول ادیتوری (۱ ماه)", "ساخت تقویم سه‌ماهه محتوا (۲ هفته)",
     "مدیریت انتشار ۲۰ محتوا (۲ ماه)", "تحلیل و بازنویسی بر پایه داده (مداوم)"],
    "ترافیک ۳۰٪ مقالات قدیمی سایت افت کرده. استراتژی به‌روزرسانی محتوای شما چیست؟")

add("عکاس و فیلم‌ساز محصول", "Product Photographer", "مرحله ۶ — تولید محتوا",
    "تولید تصاویر و ویدیوی حرفه‌ای محصول و فضای برند",
    ["عکاسی محصول با نورپردازی", "رتوش و رنگ‌بندی", "ویدیو معرفی محصول",
     "موشن‌گرافیک تبلیغاتی", "بهینه‌سازی رسانه برای وب", "آرشیو و نام‌گذاری دارایی‌ها"],
    [("Immich (آرشیو هوشمند)", "immich-app/immich"), ("PhotoPrism", "photoprism/photoprism"),
     ("Sharp (بهینه‌سازی)", "lovell/sharp")],
    [("Immich demo", "demo.immich.app", "تجربه آرشیو AI"),
     ("GIMP", "gimp.org", "ویرایش تصویر متن‌باز"),
     ("DaVinci Resolve", "blackmagicdesign.com", "تدوین حرفه‌ای رایگان")],
    ["یادگیری نورپردازی محصول (۱ ماه)", "عکاسی ۳۰ محصول واقعی (۱ ماه)",
     "تدوین ویدیو با DaVinci (۲ ماه)", "ساخت ریلز معرفی محصول (مداوم)"],
    "محصولی شیشه‌ای و بازتابنده دارید و عکس‌هایش همیشه درشت‌نمایی می‌شوند. راه‌حل فنی شما؟")

add("تولیدکننده محتوای گرافیکی", "Visual Content Creator", "مرحله ۶ — تولید محتوا",
    "طراحی اینفوگرافیک، بنر و تصاویر سوشال هم‌راستا با برند",
    ["اینفوگرافیک داده-محور", "طراحی بنر تبلیغاتی", "قالب‌سازی سوشال مدیا",
     "ایلاستریشن برداری", "داشبورد تصویری داده", "انیمیشن GIF ساده"],
    [("P5.js (ژنراتیو)", "processing/p5.js"), ("D3 (داده-محور)", "d3/d3")],
    [("Canva", "canva.com", "قالب‌های سوشال"),
     ("Penpot", "penpot.app", "طراحی وکتور"),
     ("Coolors", "coolors.co", "پالت هماهنگ برند")],
    ["یادگیری اصول داده‌ویژوالایزیشن (۱ ماه)", "ساخت ۱۰ اینفوگرافیک (۱ ماه)",
     "طراحی ست کامل سوشال یک برند (۲ هفته)", "تسلط بر D3 برای نمودار سفارشی (۲ ماه)"],
    "داده‌ای خشک و جدولی دارید. چگونه تصمیم می‌گیرید کدام بخش آن اینفوگرافیک شود و کدام نه؟")

# ================= 7. فرانت‌اند =================
add("توسعه‌دهنده فرانت‌اند", "Frontend Developer", "مرحله ۷ — فرانت‌اند",
    "پیاده‌سازی رابط کاربری با کد تمیز، سریع و ریسپانسیو",
    ["HTML سیمانتیک و CSS مدرن", "جاوااسکریپت/TypeScript", "ریسپانسیو و موبایل-فرست",
     "مدیریت State", "دسترس‌پذیری و RTL", "بهینه‌سازی رندر"],
    [("React", "facebook/react"), ("Vue", "vuejs/vue"), ("Tailwind CSS", "tailwindlabs/tailwindcss"),
     ("TypeScript", "microsoft/TypeScript")],
    [("Frontend Mentor", "frontendmentor.io", "چالش طراحی به کد"),
     ("CSS Battle", "cssbattle.dev", "مسابقه روزانه CSS"),
     ("CodePen", "codepen.io", "زمین بازی و ایده")],
    ["تسلط بر HTML/CSS/JS (۳ ماه)", "یادگیری React و TypeScript (۳ ماه)",
     "ساخت ۵ پروژه واقعی ریسپانسیو (۳ ماه)", "مکانیزم رندر، SSR و بهینه‌سازی (۲ ماه)"],
    "صفحه‌ای با لیست ۱۰هزار آیتم کرش می‌کند. تکنیک‌های رفع و بهینه‌سازی آن را توضیح دهید.")

add("توسعه‌دهنده ری‌اکت", "React Developer", "مرحله ۷ — فرانت‌اند",
    "تخصص در اکوسیستم React برای رابط‌های تعاملی پیچیده",
    ["کامپوننت و Hookهای پیشرفته", "مدیریت State سمت کلاینت", "React Query و کش سرور",
     "تست با Testing Library", "بهینه‌سازی رندر (memo/useMemo)", "Server Components"],
    [("React", "facebook/react"), ("Next.js", "vercel/next.js"), ("shadcn/ui", "shadcn-ui/ui")],
    [("StackBlitz", "stackblitz.com", "پروژه React در مرورگر"),
     ("Frontend Mentor", "frontendmentor.io", "چالش‌های UI واقعی")],
    ["تسلط بر JS مدرن و TypeScript (۲ ماه)", "یادگیری عمیق React و هوک‌ها (۲ ماه)",
     "ساخت اپ CRUD با Next.js (۱ ماه)", "تست و بهینه‌سازی (۱ ماه)"],
    "useEffect نامتناسب باعث درخواست تکراری می‌شود. چگونه صحت وابستگی‌ها را تشخیص می‌دهید؟")

add("متخصص Next.js", "Next.js Specialist", "مرحله ۷ — فرانت‌اند",
    "سایت‌های SSR/ISR سریع و سئو-پسند با اکوسیستم Next",
    ["App Router و Server Components", "SSR/SSG/ISR", "مسیریابی و API Route",
     "بهینه‌سازی تصویر/فونت", "Edge و Middleware", "احراز هویت Auth.js"],
    [("Next.js", "vercel/next.js"), ("shadcn/ui", "shadcn-ui/ui"), ("Auth.js", "nextauthjs/next-auth")],
    [("Next.js Learn", "nextjs.org/learn", "آموزش رسمی تعاملی"),
     ("Vercel Hobby", "vercel.com", "هاست رایگان پروژه")],
    ["یادگیری React پیش‌نیاز (۲ ماه)", "دوره Next.js Learn رسمی (۱ ماه)",
     "ساخت فروشگاه SSR با ISR (۱ ماه)", "استقرار و بهینه‌سازی تولید (۲ هفته)"],
    "صفحه‌ای باید هم سئو عالی و هم داده کاربر لاگین‌شده داشته باشد. معماری رندر شما؟")

add("توسعه‌دهنده انیمیشن وب", "Web Animation Developer", "مرحله ۷ — فرانت‌اند",
    "پیاده‌سازی انیمیشن روان ۶۰fps بدون قربانی کردن سرعت",
    ["انیمیشن CSS و Web Animations API", "GSAP/Motion در React", "انیمیشن اسکرول (Scroll-driven)",
     "FLIP و layout animation", "بهینه‌سازی GPU", "Reduced Motion برای a11y"],
    [("Motion", "motion-dev/motion"), ("React Three Fiber", "pmndrs/react-three-fiber"),
     ("Lottie", "airbnb/lottie-web")],
    [("Motion", "motion.dev", "مستندات تعاملی"),
     ("CSS Battle", "cssbattle.dev", "تمرین CSS پیشرفته")],
    ["یادگیری اصول انیمیشن و easing (۱ ماه)", "پیاده‌سازی ۲۰ میکرواینترکشن (۱ ماه)",
     "پروژه لندینگ انیمیشن-محور (۱ ماه)", "وب سه‌بعدی با R3F (۲ ماه)"],
    "انیمیشنی روی موبایل ارزان لگ می‌زند. چگونه پروفایل و بهینه‌سازی می‌کنید؟")

add("متخصص دسترس‌پذیری فرانت‌اند", "Frontend Accessibility Engineer", "مرحله ۷ — فرانت‌اند",
    "پیاده‌سازی کد فرانت‌اند سازگار با WCAG برای همه کاربران",
    ["HTML سیمانتیک", "ARIA درست در جای درست", "مدیریت فوکوس در SPA",
     "تست با Screen Reader", "کنتراست و واحدهای نسبی", "CI خودکار a11y"],
    [("Radix Primitives", "radix-ui/primitives"), ("React Aria", "adobe/react-spectrum")],
    [("WebAIM WAVE", "wave.webaim.org", "ارزیابی سریع صفحات"),
     ("NVDA", "nvaccess.org", "خواننده صفحه ویندوز"),
     ("axe DevTools", "deque.com/axe", "اسکن خودکار a11y")],
    ["مطالعه WCAG و ARIA (۱ ماه)", "بازسازی ۳ کامپوننت a11y-پسند (۱ ماه)",
     "تست کامل یک سایت با NVDA (۲ هفته)", "راه‌اندازی CI با axe (۲ هفته)"],
    "منوی کشویی فقط با موس کار می‌کند. چه تغییری در DOM و رفتار کیبورد لازم است؟")

# ================= 8. بک‌اند =================
add("مهندس بک‌اند", "Backend Engineer", "مرحله ۸ — بک‌اند",
    "موتور سایت: APIها، منطق کسب‌وکار و کارایی پایدار",
    ["طراحی REST/GraphQL", "احراز هویت و امنیت API", "معماری لایه‌ای و تمیز",
     "کش و صف", "لاگ و مانیتورینگ", "تست یکپارچه"],
    [("Express", "expressjs/express"), ("NestJS", "nestjs/nest"), ("FastAPI", "fastapi/fastapi"),
     ("PostgreSQL", "postgres/postgres")],
    [("Roadmap.sh", "roadmap.sh/backend", "نقشه راه کامل بک‌اند"),
     ("Postman", "postman.com", "طراحی و تست API"),
     ("Supabase", "supabase.com", "پستگرس + API آماده")],
    ["یادگیری یک زبان سرور و SQL (۳ ماه)", "ساخت API کامل CRUD با احراز هویت (۲ ماه)",
     "آزمون بار و امنیت (۱ ماه)", "معماری میکروسرویس و صف (۲ ماه)"],
    "اندپوینتی زیر بار ۱۰x کند می‌شود. فرآیند تشخیص و رفع شما به ترتیب چیست؟")

add("توسعه‌دهنده Node.js", "Node.js Developer", "مرحله ۸ — بک‌اند",
    "سرورهای جاوااسکریپت پرسرعت و ایزومورفیک",
    ["Event Loop و غیرهمگامی", "Express/Fastify/Nest", "استریم و بافر",
     "Worker Thread", "NPM و مدیریت پکیج", "دیباگ و Profiling"],
    [("Express", "expressjs/express"), ("Fastify", "fastify/fastify"), ("NestJS", "nestjs/nest"),
     ("Hono (ترند)", "honojs/hono")],
    [("Node.js Docs", "nodejs.org", "مستندات رسمی با REPL"),
     ("Roadmap.sh", "roadmap.sh/backend", "مسیر یادگیری")],
    ["تسلط بر JS مدرن و async (۲ ماه)", "ساخت API با Express سپس Nest (۲ ماه)",
     "استریم و بهینه‌سازی حافظه (۱ ماه)", "مقیاس‌پذیری با Redis و صف (۲ ماه)"],
    "سرور Node شما Memory Leak دارد. ابزار و مراحل تشخیص نشتی را شرح دهید.")

add("توسعه‌دهنده پایتون وب", "Python Web Developer", "مرحله ۸ — بک‌اند",
    "بک‌اند پایتونی برای APIهای سریع و اتصال به دنیای داده و AI",
    ["Django و ORM", "FastAPI و Pydantic", "معماری اپ پایتون",
     "Celery و وظایف پس‌زمینه", "Test با pytest", "استقرار با Gunicorn/Uvicorn"],
    [("FastAPI", "fastapi/fastapi"), ("Django", "django/django"), ("Flask", "pallets/flask")],
    [("FastAPI Docs", "fastapi.tiangolo.com", "مستندات تعاملی Swagger"),
     ("Supabase", "supabase.com", "دیتابیس برای تمرین API")],
    ["تسلط بر پایتون و SQL (۲ ماه)", "ساخت API با FastAPI و مستندسازی (۱ ماه)",
     "پروژه جنگو با پنل ادمین (۲ ماه)", "Celery و استقرار (۱ ماه)"],
    "چرا برای API پایتون، FastAPI و برای سایت محتوایی جنگو انتخاب می‌شود؟ یک مثال واقعی بگویید.")

add("توسعه‌دهنده PHP / لاراول", "Laravel Developer", "مرحله ۸ — بک‌اند",
    "وب‌سایت‌ها و فروشگاه‌های سریع با اکوسیستم بالغ PHP",
    ["PHP مدرن 8+", "لاراول: Eloquent/Blade/Queue", "استقرار و بهینه‌سازی OPcache",
     "امنیت لاراول", "تست با Pest/PHPUnit", "اکوسیستم پکیج‌ها"],
    [("Laravel", "laravel/framework"), ("Symfony", "symfony/symfony"), ("PHPMailer", "PHPMailer/PHPMailer")],
    [("Laravel Bootcamp", "bootcamp.laravel.com", "آموزش رسمی پروژه‌محور"),
     ("Laracasts free", "laracasts.com", "ویدیوهای آموزشی")],
    ["یادگیری PHP مدرن (۲ ماه)", "ساخت CRUD با لاراول (۱ ماه)",
     "پروژه کامل فروشگاه/بلوگ (۲ ماه)", "تست، صف و استقرار (۱ ماه)"],
    "کوئری Eloquent شما روی جدول میلیونی کند است. چه گزینه‌هایی برای بهینه‌سازی دارید؟")

add("توسعه‌دهنده Go", "Go Developer", "مرحله ۸ — بک‌اند",
    "سرویس‌های سبک و مقیاس‌پذیر با زبان همزمانی‌محور گوگل",
    ["Goroutine و Channel", "Gin/Chi برای API", "ساختار پروژه استاندارد",
     "gRPC سرویس", "تست و بنچمارک", "کامپایل و استقرار تک‌باینری"],
    [("Gin", "gin-gonic/gin"), ("Chi", "go-chi/chi"), ("gRPC", "grpc/grpc")],
    [("Go Tour", "go.dev/tour", "آموزش تعاملی رسمی"),
     ("Go by Example", "gobyexample.com", "نمونه کدهای موضوعی")],
    ["یادگیری Go با Tour رسمی (۱ ماه)", "ساخت REST API با Gin (۱ ماه)",
     "سرویس gRPC و همزمانی (۱ ماه)", "پروژه میکروسرویس واقعی (۲ ماه)"],
    "Goroutineهای شما Deadlock می‌کنند. چگونه با channel و context جلوی آن را می‌گیرید؟")

add("طراح API", "API Designer", "مرحله ۸ — بک‌اند",
    "طراحی قراردادهای تمیز و ماندگار بین سیستم‌ها",
    ["REST maturity و HATEOAS", "OpenAPI/Swagger", "نسخه‌بندی و deprecation",
     "GraphQL Schema Design", "Webhook و رویداد", "امنیت OAuth2/JWT"],
    [("GraphQL", "graphql/graphql-js"), ("gRPC", "grpc/grpc"), ("Hoppscotch", "hoppscotch/hoppscotch")],
    [("OpenAPI Spec", "swagger.io/spec", "مستندات استاندارد"),
     ("Hoppscotch", "hoppscotch.io", "تست تعاملی API"),
     ("Postman", "postman.com", "مجموعه تست API")],
    ["مطالعه طراحی APIهای بزرگ عمومی (۱ ماه)", "طراحی OpenAPI برای یک فروشگاه (۱ ماه)",
     "پیاده‌سازی و مستندسازی خودکار (۱ ماه)", "طراحی GraphQL معادل (۱ ماه)"],
    "کلاینتی فیلد حیاتی را در API v1 بد طراحی شده می‌خواهد؛ v2 آماده است. استراتژی مهاجرت شما؟")

add("مهندس احراز هویت", "Auth Engineer", "مرحله ۸ — بک‌اند",
    "ورود امن و بی‌دردسر کاربران با OAuth/OIDC و MFA",
    ["OAuth 2.0 و OpenID Connect", "JWT در برابر Session", "MFA و Passkey/WebAuthn",
     "SSO سازمانی SAML", "مدیریت نقش RBAC/ABAC", "جلوگیری از حملات احراز هویت"],
    [("Keycloak", "keycloak/keycloak"), ("Auth.js", "nextauthjs/next-auth"), ("Authentik", "goauthentik/authentik")],
    [("Keycloak Demo", "keycloak.org", "دموی آنلاین SSO"),
     ("Auth0 Docs", "auth0.com/docs", "مستندات آموزشی OIDC")],
    ["یادگیری OAuth2/OIDC (۱ ماه)", "پیاده‌سازی ورود گوگل/گیت‌هاب (۲ هفته)",
     "ساخت SSO با Keycloak (۱ ماه)", "MFA و Passkey (۱ ماه)"],
    "چرا JWT در LocalStorage ناامن تلقی می‌شود و جایگزن‌های آن چیست؟")

# ================= 9. دیتابیس =================
add("مدیر دیتابیس", "Database Administrator", "مرحله ۹ — دیتابیس",
    "سلامت، کارایی و پشتیبان‌گیری دیتابیس قلب سایت",
    ["طراحی اسکیما و نرمال‌سازی", "ایندکس‌گذاری و Query Plan", "پشتیبان‌گیری و بازیابی",
     "همسان‌سازی Replica", "امنیت و دسترسی", "مانیتورینگ کارایی"],
    [("PostgreSQL", "postgres/postgres"), ("MySQL", "mysql/mysql-server"), ("ClickHouse", "clickhouse/clickhouse")],
    [("SQLZoo", "sqlzoo.net", "تمرین تعاملی SQL"),
     ("pgAdmin", "pgadmin.org", "محیط مدیریت پستگرس"),
     ("DB Fiddle", "db-fiddle.com", "تست کوئری آنلاین")],
    ["تسلط بر SQL و طراحی اسکیما (۲ ماه)", "یادگیری عمیق پستگرس و ایندکس (۲ ماه)",
     "پشتیبان‌گیری و بازیابی تمرینی (۱ ماه)", "بهینه‌سازی کوئری‌های واقعی (مداوم)"],
    "کوئری‌ای که در تست سریع بود در تولید کند شده. مراحل تحلیل EXPLAIN شما؟")

add("مدل‌ساز داده", "Data Modeler", "مرحله ۹ — دیتابیس",
    "طراحی ساختار داده که کسب‌وکار فردا را هم پوشش دهد",
    ["مدل‌سازی Conceptual/Logical/Physical", "ERD و نرمال‌سازی", "الگوهای طراحی داده",
     "مهاجرت اسکیما", "DWH و ستاره", "داده نیمه‌ساختاریافته JSONB"],
    [("PostgreSQL (JSONB)", "postgres/postgres"), ("DBML", "dbdiagram-io/dbml"), ("Supabase", "supabase/supabase")],
    [("DrawDB", "drawdb.app", "طراحی آنلاین ERD"),
     ("dbdiagram.io", "dbdiagram.io", "مدل‌سازی با DBML")],
    ["یادگیری نرمال‌سازی و الگوها (۱ ماه)", "مدل‌سازی ۵ سناریوی واقعی (۱ ماه)",
     "پیاده‌سازی و مهاجرت با SQL (۱ ماه)", "الگوهای DWH (۱ ماه)"],
    "مشتری می‌خواهد فیلد سفارشی نامحدود برای محصولات. JSONB در برابر EAV را تحلیل کنید.")

add("مهندس ORM و Data Access", "ORM Engineer", "مرحله ۹ — دیتابیس",
    "پل میان کد و دیتابیس با ORMهای مدرن و تایپ‌دار",
    ["Prisma/Drizzle در TS", "Django ORM/SQLAlchemy", "الگوی Repository",
     "مهاجرت خودکار", "N+1 و بارگذاری تنبل", "تراکنش و ایزولاسیون"],
    [("Prisma", "prisma/prisma"), ("Drizzle ORM", "drizzle-team/drizzle-orm"), ("Supabase", "supabase/supabase")],
    [("Prisma Docs", "prisma.io/docs", "مستندات تعاملی ORM"),
     ("Drizzle Playground", "drizzle.run", "زمین play آنلاین")],
    ["یادگیری SQL پیش‌نیاز (۱ ماه)", "تسلط بر Prisma و مهاجرت‌ها (۱ ماه)",
     "رفع N+1 و بهینه‌سازی (۲ هفته)", "مقایسه و مهاجرت به Drizzle (۲ هفته)"],
    " ORM همه‌چیز را راحت کرده اما کوئری سنگینی تولید می‌کند. چگونه از SQL خام در جای درست استفاده می‌کنید؟")

# ================= 10. فروشگاهی =================
add("توسعه‌دهنده فروشگاه آنلاین", "E-commerce Developer", "مرحله ۱۰ — فروشگاهی",
    "ساخت فروشگاه سریع و امن با درگاه و مدیریت انبار",
    ["معماری فروشگاه (B2C/B2B2)", "درگاه پرداخت و تسویه", "مدیریت انبار و SKU",
     "سبد خرید و Checkout", "مالیات و صورت‌حساب", "انطباق PCI-DSS"],
    [("Medusa", "medusajs/medusa"), ("WooCommerce", "woocommerce/woocommerce"),
     ("Stripe SDK", "stripe/stripe-node")],
    [("Medusa Docs", "docs.medusajs.com", "راه‌اندازی لوکال هدلس"),
     ("Stripe Test Mode", "stripe.com/docs/testing", "درگاه آزمایشی با کارت تست"),
     ("Shopify Partners", "partners.shopify.com", "سندباکس توسعه")],
    ["یادگیری اصول تجارت الکترونیک (۱ ماه)", "ساخت فروشگاه با Medusa/Woo (۲ ماه)",
     "اتصال درگاه تست و تسویه (۱ ماه)", "بهینه‌سازی Checkout و CRO (مداوم)"],
    "در میانه پرداخت، اتصال بانک قطع می‌شود و پول کاربر برگشت نمی‌خورد. سیستم Reconcile شما؟")

add("متخصص پرداخت", "Payments Specialist", "مرحله ۱۰ — فروشگاهی",
    "یکپارچه‌سازی امن درگاه‌ها و کاهش تراکنش ناموفق",
    ["استاندارد PCI-DSS", "درگاه‌های داخلی و بین‌المللی", "Webhook و تایید تراکنش",
     "پرداخت اشتراکی Recurring", "پول‌بازی و تسویه", "کشف تقلب"],
    [("Stripe", "stripe/stripe-node"), ("Medusa Payments", "medusajs/medusa")],
    [("Stripe Test", "stripe.com/docs/testing", "شبیه‌ساز کامل پرداخت"),
     ("Stripe Webhooks", "stripe.com/docs/webhooks", "شبیه‌ساز رویداد")],
    ["مطالعه PCI و امنیت پرداخت (۱ ماه)", "پیاده‌سازی پرداخت کامل تست (۱ ماه)",
     "Webhook و Reconciliation (۲ هفته)", "اشتراکی و Refund (۲ هفته)"],
    "کاربری می‌گوید پولش کشیده شده اما سفارش ثبت نشده. لاگ و رویدادها را چگونه بررسی می‌کنید؟")

# ================= 11. امنیت =================
add("متخصص امنیت وب", "Web Security Specialist", "مرحله ۱۱ — امنیت",
    "سد مقابل XSS و SQLi و CSRF و داده‌های در معرض خطر",
    ["OWASP Top 10", "امنیت Cookie و Header", "CSP و SRI",
     "اسکن آسیب‌پذیری خودکار", "رمزنگاری داده", "پاسخ به رخداد"],
    [("OWASP CheatSheet", "OWASP/CheatSheetSeries"), ("Trivy", "aquasecurity/trivy"),
     ("TruffleHog", "trufflesecurity/trufflehog")],
    [("OWASP WebGoat", "owasp.org/www-project-webgoat", "تمرین عملی آسیب‌پذیری"),
     ("PortSwigger Academy", "portswigger.net/web-security", "آکادمی رایگان تست نفوذ"),
     ("DVWA", "github.com/digininja/dvwa", "برنامه آسیب‌پذیر عمدی")],
    ["مطالعه OWASP Top 10 (۱ ماه)", "حل لبه‌های WebGoat و Academy (۲ ماه)",
     "اسکن و گزارش سایت واقعی (مجاز) (۱ ماه)", "هاردنینگ و CI امنیتی (مداوم)"],
    "فرمی بدون توکن CSRF منتشر شده. سناریوی حمله و دو راه مقابله server-side را توضیح دهید.")

add("تستر نفوذ", "Penetration Tester", "مرحله ۱۱ — امنیت",
    "هک اخلاقی قانونی برای یافتن حفره پیش از مهاجمان",
    ["Recon و شناسایی سطح حمله", "استثناات وب: SQLi/XSS/SSRF", "Burp Suite حرفه‌ای",
     "نوشتن گزارش نفوذ", "مهندسی اجتماعی (مجاز)", "اخلاق و دامنه مجاز"],
    [("SQLMap", "sqlmapproject/sqlmap"), ("OWASP ZAP", "zaproxy/zaproxy"), ("Nmap", "nmap/nmap")],
    [("Hack The Box", "hackthebox.com", "آزمایشگاه عملی نفوذ"),
     ("TryHackMe", "tryhackme.com", "مسیرهای یادگیری امنیت"),
     ("PortSwigger Academy", "portswigger.net/web-security", "تمرین تخصصی وب")],
    ["یادگیری شبکه و لینوکس (۲ ماه)", "حل ماژول‌های وب Academy (۲ ماه)",
     "ماشین‌های HTB آسان تا متوسط (۳ ماه)", "گزارش‌نویسی حرفه‌ای (مداوم)"],
    "SQLi زمان-محور (time-based) پیدا کردید اما خروجی مستقیم ندارد. چگونه داده را استخراج می‌کنید؟")

add("مهندس پاسخ به رخداد", "Incident Response Engineer", "مرحله ۱۱ — امنیت",
    "مهار سریع نفوذ و بازگشت سرویس با کمترین خسارت",
    ["چرخه IR: آماده‌سازی تا درس‌آموخته", "تحلیل لاگ و Forensic", "ISOLATION و مهار",
     "ارتباط بحران", "Playbook رخداد", "شبیه‌سازی Tabletop"],
    [("Wazuh (SIEM)", "wazuh/wazuh"), ("TruffleHog (کشف راز)", "trufflesecurity/trufflehog")],
    [("TryHackMe SOC", "tryhackme.com", "مسیر تحلیلگر SOC"),
     ("Wazuh demo", "wazuh.com", "پلتفرم SIEM متن‌باز")],
    ["یادگیری چرخه NIST IR (۱ ماه)", "راه‌اندازی SIEM خانگی Wazuh (۱ ماه)",
     "تحلیل ۱۰ سناریوی لاگ (۱ ماه)", "شبیه‌سازی بحران تیمی (مداوم)"],
    "ساعت ۳ بامداد درگاه پرداخت ترافیک غیرعادی به یک IP ناشناس دارد. پنج اقدام اول شما؟")

# ================= 12. تست و QA =================
add("مهندس تست خودکار", "Test Automation Engineer", "مرحله ۱۲ — تست و QA",
    "تست‌های E2E و یکپارچه پایدار که جلو رگرسیون را می‌گیرند",
    ["Playwright/Cypress", "Page Object Model", "تست API یکپارچه",
     "Mock و Stub", "CI خودکار تست", "Flaky Test Management"],
    [("Playwright", "microsoft/playwright"), ("Cypress", "cypress-io/cypress"), ("Vitest", "vitest-dev/vitest")],
    [("Playwright Docs", "playwright.dev", "مستندات و sandbox تعاملی"),
     ("DemoQA", "demoqa.com", "المان‌های تمرین اتومیشن"),
     ("the-internet", "the-internet.herokuapp.com", "صفحات تمرینی مصنوعی")],
    ["یادگیری JS/TS و انتخاب ابزار (۱ ماه)", "نوشتن ۵۰ تست E2E پایدار (۲ ماه)",
     "تست API و یکپارچه‌سازی CI (۱ ماه)", "الگوهای پیشرفته و نگهداشت (مداوم)"],
    "تست‌ها به صورت تصادفی Fail می‌شوند. چگونه Flakiness را ریشه‌یابی و حذف می‌کنید؟")

add("مهندس تست بار", "Performance Test Engineer", "مرحله ۱۲ — تست و QA",
    "سنجش مرز تحمل سایت زیر بار واقعی و کشف گلوگاه",
    ["سناریوی بار واقع‌گرایانه", "k6 و Grafana", "تحلیل متریک: TPS/Latency/Errors",
     "شناسایی گلوگاه", "تست Soak و Spike", "گزارش بهره‌وری"],
    [("k6", "grafana/k6"), ("Locust", "locustio/locust")],
    [("k6 Cloud", "k6.io", "اسکریپت و اجرای بار"),
     ("Grafana Play", "play.grafana.org", "داشبورد متریک تمرینی")],
    ["یادگیری مفاهیم تست بار (۲ هفته)", "نوشتن سناریو k6 برای یک سایت (۱ ماه)",
     "تحلیل نتایج و یافتن گلوگاه (۱ ماه)", "تست Soak/Spike و گزارش (مداوم)"],
    "زیر بار ۱۰۰۰ کاربر، CPU سرور ۱۰۰٪ می‌شود اما دیتابیس خاموش است. فرضیه‌های شما؟")

add("مهندس کیفیت دستی", "Manual QA Engineer", "مرحله ۱۲ — تست و QA",
    "چشم تیز کشف باگ‌هایی که اسکریپت‌ها نمی‌بینند",
    ["نوشتن Test Plan و Case", "تست اکتشافی Session-Based", "تست ریسپانسیو و بین‌مرورگری",
     "تست دسترس‌پذیری", "گزارش باگ حرفه‌ای", "Verificate از نظر کاربر نهایی"],
    [("Playwright (کمکی)", "microsoft/playwright"), ("Selenium", "SeleniumHQ/selenium")],
    [("the-internet", "the-internet.herokuapp.com", "صفحات تمرینی مصنوعی"),
     ("DemoQA", "demoqa.com", "المان‌های تمرینی"),
     ("BrowserStack free", "browserstack.com", "تست بین‌مرورگری ابری")],
    ["یادگیری اصول تست و Case نوشتن (۱ ماه)", "اجرای ۲۰۰ تست دستی مستند (۱ ماه)",
     "تست اکتشافی و Bug Bounty داخلی (۱ ماه)", "همکاری نزدیک با تیم اتومیشن (مداوم)"],
    "بگی فقط در Safari موبایل ظاهر می‌شود. چگونه گزارشی می‌نویسید که توسعه‌دهنده سریع ریشه را بفهمد؟")

# ================= 13. DevOps =================
add("مهندس DevOps", "DevOps Engineer", "مرحله ۱۳ — DevOps",
    "زیرساخت به‌کد، استقرار خودکار و اطمینان از تداوم سرویس",
    ["لینوکس و شبکه", "Docker و Kubernetes", "CI/CD Pipeline",
     "IaC با Terraform", "مانیتورینگ و هشدار", "بهبود مستمر فرآیند"],
    [("Kubernetes", "kubernetes/kubernetes"), ("Terraform", "hashicorp/terraform"),
     ("Docker/Moby", "moby/moby"), ("GitHub Actions Runner", "actions/runner")],
    [("Killercoda", "killercoda.com", "محیط تمرین لینوکس/کوبرنتیز"),
     ("Play with Docker", "labs.play-with-docker.com", "داکر رایگان در مرورگر"),
     ("LocalStack", "localstack.cloud", "شبیه‌ساز AWS لوکال")],
    ["تسلط بر لینوکس و شبکه (۲ ماه)", "داکر و کامپوز (۱ ماه)",
     "CI/CD با GitHub Actions (۱ ماه)", "کوبرنتیز و Terraform (۳ ماه)"],
    "استقرار جدید باعث افت ۲۰٪ کارایی شده. چگونه بدون Downtime به نسخه قبل برمی‌گردید؟")

add("مهندس پلتفرم", "Platform Engineer", "مرحله ۱۳ — DevOps",
    "ساخت پلتفرم داخلی که توسعه‌دهندگان خودشان مستقر شوند",
    ["Internal Developer Platform", "قالب‌سازی و Golden Path", "ArgoCD و GitOps",
     "Self-Service CI/CD", "چند-مستأجری", "قابلیت اطمینان SLO"],
    [("ArgoCD", "argoproj/argo-cd"), ("Kubernetes", "kubernetes/kubernetes"), ("Portainer", "portainer/portainer")],
    [("Play with K8s", "labs.play-with-k8s.com", "خوشه تمرینی رایگان"),
     ("ArgoCD Demo", "cd.apps.argoproj.io", "دموی زنده GitOps")],
    ["پیش‌نیاز DevOps (۴ ماه)", "GitOps با ArgoCD (۱ ماه)",
     "ساخت IDP کوچک برای تیم (۲ ماه)", "SLO و قابلیت اطمینان (مداوم)"],
    "تیم‌ها از پلتفرم داخلی شما استفاده نمی‌کنند و سراغ سرور شخصی می‌روند. واکنش شما؟")

add("مهندس قابلیت اطمینان", "Site Reliability Engineer", "مرحله ۱۳ — DevOps",
    "سایت همیشه بالا، همیشه سریع — با هدف‌گذاری خطا و اتوماسیون",
    ["SLO/SLI/Error Budget", "مانیتورینگ Three Pillars", "Troubleshooting سیستماتیک",
     "Capacity Planning", "Postmortem بدون سرزنش", "اتوماسیون Toil"],
    [("Prometheus", "prometheus/prometheus"), ("Grafana", "grafana/grafana"),
     ("Loki (لاگ)", "grafana/loki"), ("Netdata", "netdata/netdata")],
    [("Grafana Play", "play.grafana.org", "داشبورد تمرینی"),
     ("Netdata demo", "learn.netdata.cloud", "مانیتورینگ بلادرنگ")],
    ["یادگیری مانیتورینگ و متریک (۱ ماه)", "ساخت Stack کامل Prom/Grafana (۱ ماه)",
     "تعریف SLO برای یک سرویس (۱ ماه)", "Postmortem و اتوماسیون (مداوم)"],
    "SLO ماهانه ۹۹/۹٪ در روز ۲۰ خراب شده. چگونه بین سرعت انتشار و Error Budget تعادل برقرار می‌کنید؟")

add("مدیر وب‌سرور", "Web Server Administrator", "مرحله ۱۳ — DevOps",
    "پیکربندی و حفاظت از لایهٔ خدمت‌دهی وب",
    ["Nginx و Caddy", "TLS/SSL و OCSP", "Load Balancing",
     "کش و CDN", "Rewrite و امنیت هدر", "بهینه‌سازی اتصال"],
    [("Nginx", "nginx/nginx"), ("Caddy", "caddyserver/caddy"), ("Traefik", "traefik/traefik")],
    [("Nginx Playground", "nginx-playground.dev", "تست کانفیگ آنلاین"),
     ("Let's Encrypt", "letsencrypt.org", "گواهی رایگان TLS")],
    ["یادگیری HTTP و لینوکس (۱ ماه)", "کانفیگ کامل Nginx با TLS (۱ ماه)",
     "Load Balance و کش (۱ ماه)", "هاردنینگ و CDN (۱ ماه)"],
    "بعد از فعال‌سازی HTTP/2 سرعت دانلود افت کرده. چه پارامترهایی را بررسی می‌کنید؟")

# ================= 14. سئو =================
add("متخصص سئو فنی", "Technical SEO Specialist", "مرحله ۱۴ — سئو",
    "زیرساخت سایت را برای موتورهای جستجو شفاف و سریع می‌کند",
    ["Core Web Vitals", " robots و sitemap و canonical", "Schema Markup",
     "رندر و ایندکس JS", "معماری URL و لینک داخلی", "لاگ‌آنالیز خزش"],
    [("Lighthouse", "GoogleChrome/lighthouse"), ("Next Sitemap", "iamvishnusankar/next-sitemap")],
    [("Search Console", "search.google.com/search-console", "مانیتور ایندکس سایت خودتان"),
     ("Screaming Frog", "screamingfrog.co.uk/seo-spider", "خزش تا ۵۰۰ URL رایگان"),
     ("Rich Results Test", "search.google.com/test/rich-results", "تست اسکیما")],
    ["یادگیری نحوه کار موتور جستجو (۱ ماه)", "ممیزی فنی کامل یک سایت واقعی (۱ ماه)",
     "پیاده‌سازی Schema و Core Web Vitals (۱ ماه)", "لاگ‌آنالیز و بهینه‌سازی خزش (مداوم)"],
    "سایت SPA شما فقط صفحات اول را ایندکس می‌کند. راه‌حل‌های رندر را مقایسه کنید.")

add("متخصص سئو محتوا", "Content SEO Specialist", "مرحله ۱۴ — سئو",
    "برنامه کلمات کلیدی و محتوای رتبه‌گیر برای کل سایت",
    ["تحقیق کلمه کلیدی و Search Intent", "خوشه‌بندی Topic Cluster", "بهینه‌سازی On-Page",
     "E-E-A-T و اعتبار محتوا", "به‌روزرسانی محتوای قدیمی", "تحلیل SERP رقبا"],
    [("Strapi (CMS)", "strapi/strapi"), ("Ghost (نشر)", "tryghost/ghost")],
    [("Ahrefs Webmaster Tools", "ahrefs.com/webmaster-tools", "رایگان برای سایت خودتان"),
     ("Google Trends", "trends.google.com", "روند کلمات کلیدی"),
     ("AnswerThePublic", "answerthepublic.com", "سوالات واقعی کاربران")],
    ["یادگیری Search Intent و انواع آن (۱ ماه)", "ساخت خوشه محتوایی ۱۰ تایی (۲ ماه)",
     "رصد رتبه و بهینه‌سازی تکراری (مداوم)", "به‌روزرسانی محتوای فرسوده (فصلی)"],
    "صفحه‌ای رتبه ۸ دارد برای کلمه پرجستجو. چک‌لیست ارتقای آن به صفحه اول چیست؟")

add("متخصص سئو محلی", "Local SEO Specialist", "مرحله ۱۴ — سئو",
    "دیده‌شدن کسب‌وکار در جستجو و نقشه شهر خودش",
    ["پروفایل Google Business", "NAP یکدست و Citations", "نظرات و مدیریت پاسخ",
     "سئوی محلی On-Page", "Local Pack", "تحلیل رقیب محلی"],
    [("Meilisearch (جستجوی سایت)", "meilisearch/meilisearch")],
    [("Google Business Profile", "business.google.com", "مدیریت پروفایل کسب‌وکار"),
     ("Google Maps", "google.com/maps", "تحلیل Local Pack رقبا"),
     ("Local Falcon trial", "localfalcon.com", "نقشه رتبه محلی")],
    ["یادگیری فاکتورهای رتبه محلی (۲ هفته)", "بهینه‌سازی کامل پروفایل یک کسب‌وکار واقعی (۱ ماه)",
     "ساخت ۲۰ Citation یکدست (۲ هفته)", "مدیریت نظرات و گزارش ماهانه (مداوم)"],
    "رستورانی در Local Pack دیده نمی‌شود اما رقیب ۲۰۰ متری‌تر اول است. سه اقدام اول شما؟")

# ================= 15. عملکرد =================
add("مهندس عملکرد وب", "Web Performance Engineer", "مرحله ۱۵ — عملکرد",
    "سایت را به سریع‌ترین نسخه ممکن خودش تبدیل می‌کند",
    ["Core Web Vitals عمیق", "زنجیره درخواست و Critical Path", "بهینه‌سازی تصویر و فونت",
     "کش مرورگر و CDN", "باندل و Tree-shaking", "پروفایل رندر JS"],
    [("web-vitals", "GoogleChrome/web-vitals"), ("Sharp (تصویر)", "lovell/sharp"),
     ("esbuild", "evanw/esbuild")],
    [("PageSpeed Insights", "pagespeed.web.dev", "سنجش CWV واقعی"),
     ("WebPageTest", "webpagetest.org", "آزمون از نقاط جهان"),
     ("Chrome DevTools", "developer.chrome.com/docs/devtools", "پروفایل کارایی")],
    ["یادگیری نحوه کار رندر مرورگر (۱ ماه)", "بهینه‌سازی یک سایت واقعی تا سبز (۱ ماه)",
     "پروفایل JS و حذف گلوگاه (۱ ماه)", "رصد مداوم RUM (مداوم)"],
    "LCP سایت ۴ ثانیه است. پنج اقدام اولویت‌دار شما به ترتیب اثر چیست؟")

add("مهندس کش و CDN", "Caching & CDN Engineer", "مرحله ۱۵ — عملکرد",
    "سرو محتوا از نزدیک‌ترین نقطه جهان به کاربر",
    ["استراتژی کش چندلایه", "CDN و Edge", "Cache-Control و ETag",
     "Invalidation", "تصویر و ویدیو Adaptive", "A/B در Edge"],
    [("Nginx (کش)", "nginx/nginx"), ("Caddy", "caddyserver/caddy"), ("Traefik", "traefik/traefik")],
    [("Cloudflare free", "cloudflare.com", "CDN رایگان برای تمرین"),
     ("WebPageTest", "webpagetest.org", "مقایسه قبل/بعد کش")],
    ["یادگیری هدرهای HTTP کش (۲ هفته)", "پیاده‌سازی کش Nginx لوکال (۲ هفته)",
     "اتصال CDN واقعی و تست (۱ ماه)", "Invalidation و A/B در Edge (۱ ماه)"],
    "محتوای جدید منتشر شده اما کاربران نسخه قدیمی می‌بینند. استراتژی Invalidation شما؟")

# ================= 16. آنالیتیکس =================
add("تحلیلگر داده وب", "Web Data Analyst", "مرحله ۱۶ — آنالیتیکس",
    "تبدیل داده رفتار کاربر به تصمیم‌های محصول",
    ["GA4 و مدل رویداد", "داشبوردسازی Looker", "کوهورت و Retention",
     "تحلیل قیف", "آمار پایه و معناداری", "دموکراسی داده در تیم"],
    [("PostHog", "posthog/posthog"), ("Umami", "umami-software/umami"), ("Matomo", "matomo-org/matomo")],
    [("GA4 Demo Account", "analytics.google.com", "داده واقعی فروشگاه گوگل"),
     ("Looker Studio", "lookerstudio.google.com", "داشبورد رایگان"),
     ("PostHog Demo", "posthog.com", "محصول با داده نمونه")],
    ["یادگیری GA4 و SQL پایه (۱ ماه)", "ساخت داشبورد فروش واقعی (۱ ماه)",
     "تحلیل قیف و کوهورت (۱ ماه)", "A/B تحلیل و تصمیسازی (مداوم)"],
    "بازدید سایت دو برابر شده اما فروش ثابت. چگونه این معما را تحلیل می‌کنید؟")

add("متخصص بهینه‌سازی نرخ تبدیل", "CRO Specialist", "مرحله ۱۶ — آنالیتیکس",
    "بیشتر کردن فروش بدون یک بازدید اضافه — با تست و روانشناسی",
    ["فرآیند تحقیق CRO", "نظریه A/B تست و آمار", "روانشناسی قانع‌کردن",
     "تحلیل فرم و Checkout", "Heatmap و ضبط جلسه", "اولویت‌بندی ICE"],
    [("GrowthBook", "growthbook/growthbook"), ("PostHog (Feature Flag)", "posthog/posthog")],
    [("GrowthBook Demo", "growthbook.io", "پلتفرم تست A/B متن‌باز"),
     ("Microsoft Clarity", "clarity.microsoft.com", "هیت‌مپ و ضبط رایگان"),
     ("GA4 Demo", "analytics.google.com", "داده قیف واقعی")],
    ["یادگیری آمار A/B تست (۱ ماه)", "تحقیق کیفی با Clarity (۲ هفته)",
     "اجرای ۵ تست A/B واقعی (۲ ماه)", "ساخت برنامه CRO سالانه (مداوم)"],
    "تستی برنده شده اما بعد از انتشار، فروش بیشتر نشده. چه توضیحی دارد؟")

# ================= 17. حقوقی =================
add("مشاور حقوقی دیجیتال", "Digital Legal Advisor", "مرحله ۱۷ — حقوقی",
    "حفاظت حقوقی سایت: قوانین، حریم خصوصی و قراردادها",
    ["قوانین تجارت الکترونیک", "GDPR و حریم خصوصی", "تنظیم شرایط استفاده",
     "حق مالکیت محتوا", "قرارداد توسعه و SLA", "انطباق کوکی"],
    [("Umami (بدون کوکی)", "umami-software/umami")],
    [("Osano CookieConsent", "osano.com/cookieconsent", "بنر رضایت رایگان")],
    ["مطالعه قوانین تجارت الکترونیک هدف (۱ ماه)", "تنظیم ۵ سند حقوقی نمونه (۱ ماه)",
     "ممیزی انطباق یک سایت واقعی (۱ ماه)"],
    "سایتی بدون بنر کوکی به اتحادیه اروپا سرویس می‌دهد. ریسک‌ها و اقدامات اصلاحی؟")

# ================= 18. پشتیبانی =================
add("کارشناس پشتیبانی فنی", "Technical Support Specialist", "مرحله ۱۸ — پشتیبانی",
    "حل مشکلات کاربران با سرعت و همدلی — خط مقدم رضایت",
    ["مدیریت تیکت و SLA", "عیب‌یابی راهنمای کاربر", "نوشتن مقاله راهنما",
     "مهارت‌های ارتباطی و همدلی", "اسکالATION به تیم فنی", "تحلیل ریشه مشکل"],
    [("Chatwoot", "chatwoot/chatwoot"), ("Zammad", "zammad/zammad"), ("GLPI", "glpi-project/glpi")],
    [("Chatwoot Cloud", "chatwoot.com", "پشتیبانی چندکاناله رایگان"),
     ("Zammad Demo", "zammad.com/en/demo", "دموی آنلاین کمک‌دسک")],
    ["یادگیری محصول و عیب‌یابی (۱ ماه)", "پاسخ به ۱۰۰ تیکت تمرینی/واقعی (۲ ماه)",
     "نوشتن ۱۰ مقاله راهنما (۱ ماه)", "تحلیل ریشه و بهبود محصول (مداوم)"],
    "کاربری عصبانی با تیکت تکراری نوشته. پاسخ شما و روند رسیدگی چگونه است؟")

add("مدیر انجمن و مرکز کمک", "Community Manager", "مرحله ۱۸ — پشتیبانی",
    "ساخت جامعه‌ای که کاربران همدیگر را کمک کنند",
    ["مدیریت انجمن Discourse", "گیمیفیکیشن و سطح کاربر", "سیاست‌های انجمن",
     "رویداد و AMA", "مدیریت بحران جامعه", "سنجش سلامت انجمن"],
    [("Discourse", "discourse/discourse"), ("Chatwoot", "chatwoot/chatwoot")],
    [("Discourse Demo", "try.discourse.org", "انجمن تمرینی رسمی"),
     ("meta.discourse.org", "meta.discourse.org", "انجمن حرفه‌ای واقعی")],
    ["مطالعه مدیریت انجمن‌های بزرگ (۱ ماه)", "مدیریت انجمن تمرینی (۲ ماه)",
     "طراحی برنامه گیمیفیکیشن (۱ ماه)", "رویداد و AMA ماهانه (مداوم)"],
    "کاربر فعالی شروع به انتشار اطلاعات نادرست در انجمن شما کرده. برخورد شما؟")

add("مهندس نگهداشت", "Maintenance Engineer", "مرحله ۱۸ — پشتیبانی",
    "به‌روز و امن نگه‌داشتن سایت در طول سال‌ها",
    ["برنامه به‌روزرسانی", "بکاپ و بازیابی آزمایشی", "پایش خرابی بی‌صدا",
     "مدیریت دیون فنی", "پچ امنیتی سریع", "مستندسازی عملیاتی"],
    [("Restic (بکاپ)", "restic/restic"), ("Uptime Kuma", "louislam/uptime-kuma"),
     ("Duplicati", "duplicati/duplicati")],
    [("Uptime Kuma demo", "uptime.kuma.pet", "دموی مانیتور آپ‌تایم"),
     ("Restic Docs", "restic.net", "بکاپ رمزنگاری‌شده")],
    ["یادگیری چرخه نگهداشت (۲ هفته)", "راه‌اندازی پایش و بکاپ واقعی (۱ ماه)",
     "شبیه‌سازی بازیابی فاجعه (۲ هفته)", "برنامه به‌روزرسانی فصلی (مداوم)"],
    "آپدیت وابستگی باعث خرابی تولید شد. چگونه از این پس فرآیند آپدیت را ایمن می‌کنید؟")

# ================= 19. بازاریابی =================
add("مدیر دیجیتال مارکتینگ", "Digital Marketing Manager", "مرحله ۱۹ — بازاریابی",
    "استراتژی و اجرای جذب کاربر از همه کانال‌های دیجیتال",
    ["استراتژی چندکاناله", "بودجه‌بندی و ROI", "داشبورد شاخص‌ها",
     "همکاری با تیم محتوا و سئو", "اتوماسیون مارکتینگ", "تحلیل رقبا"],
    [("PostHog", "posthog/posthog"), ("Mautic", "mautic/mautic")],
    [("GA4 Demo", "analytics.google.com", "داده واقعی برای تحلیل"),
     ("Looker Studio", "lookerstudio.google.com", "داشبورد شاخص‌ها"),
     ("Mautic demo", "mautic.org", "اتوماسیون متن‌باز")],
    ["یادگیری مفاهیم مارکتینگ دیجیتال (۱ ماه)", "مدیریت کمپین کوچک واقعی (۲ ماه)",
     "تحلیل ROI و بهینه‌سازی (۱ ماه)", "استراتژی سالانه چندکاناله (مداوم)"],
    "بودجه تبلیغات نصف شده. چگونه کمپین‌ها را اولویت‌بندی می‌کنید تا فروش حفظ شود؟")

add("متخصص تبلیغات کلیکی", "PPC Specialist", "مرحله ۱۹ — بازاریابی",
    "خرید هوشمند ترافیک: هر کلیک سودآور باشد",
    ["گوگل‌ادز و ساختار کمپین", "امتیار کیفیت و QS", "لیبل نرخ تبدیل",
     "ریتارگتینگ", "لیدینگ و فرم تبلیغ", "منفی‌سازی کلمات"],
    [("Shlink (ردیابی لینک)", "shlinkio/shlink")],
    [("Google Ads Demo", "ads.google.com", "حساب تمرینی با کد تخفیف"),
     ("Google Skillshop", "skillshop.withgoogle.com", "آموزش رسمی رایگان")],
    ["گذراندن Skillshop گوگل (۱ ماه)", "اجرا کمپین کوچک واقعی با بودجه کم (۱ ماه)",
     "بهینه‌سازی و منفی‌سازی (۱ ماه)", "تسلط بر ریتارگتینگ و فرم (۲ ماه)"],
    "CPC کمپین بالا رفته و CVR افت کرده. چک‌لیست عیب‌یابی شما؟")

add("مدیر سوشال مدیا", "Social Media Manager", "مرحله ۱۹ — بازاریابی",
    "حضور فعال و رشدآور برند در شبکه‌های اجتماعی",
    ["استراتژی محتوای سوشال", "زمان‌بندی و تقویم", "کپی و کپشن‌نویسی",
     "تحلیل بینش شبکه", "همکاری با اینفلوئنسر", "مدیریت بحران سوشال"],
    [("Postiz", "postizapp/postiz"), ("Mixpost", "mixpost/mixpost"), ("Novu (نوتیف)", "novuhq/novu")],
    [("Postiz Cloud", "postiz.com", "زمان‌بندی با نسخه ابری"),
     ("Buffer free", "buffer.com", "پلن رایگان زمان‌بندی"),
     ("Canva", "canva.com", "طراحی پست")],
    ["یادگیری الگوریتم‌های شبکه‌ها (۱ ماه)", "مدیریت یک پیج واقعی ۳ ماهه (۳ ماه)",
     "تحلیل Insights و بهینه‌سازی (مداوم)", "کمپین اینفلوئنسر (۱ ماه)"],
    "پستی منتقدانه وایرال شده. پروتکل پاسخ شما در ساعت اول؟")

add("متخصص ایمیل مارکتینگ", "Email Marketing Specialist", "مرحله ۱۹ — بازاریابی",
    "رساندن پیام درست به صندوق ورودی — و کلیک شدن",
    ["لیست‌سازی Opt-in دوگانه", "طراحی ایمیل ریسپانسیو", "اتوماسیون Welcome/Cart",
     "تفکیک و شخصی‌سازی", "Deliverability و SPF/DKIM", "A/B تست سوژه"],
    [("Listmonk", "listmonk-app/listmonk"), ("Mautic", "mautic/mautic"), ("Novu", "novuhq/novu")],
    [("Listmonk demo", "listmonk.app", "دموی خبرنامه متن‌باز"),
     ("Mailchimp free", "mailchimp.com", "تا ۵۰۰ مخاطب رایگان"),
     ("Keila", "keila.io", "خبرنامه متن‌باز")],
    ["یادگیری اصول Deliverability (۲ هفته)", "ساخت اتوماسیون خوش‌آمد (۲ هفته)",
     "کمپین ماهانه و A/B (۱ ماه)", "تفکیک و شخصی‌سازی پیشرفته (مداوم)"],
    "نرخ باز شدن ایمیل‌ها ماهانه افت می‌کند. چه فاکتورهایی را بررسی و بهینه می‌کنید؟")

json.dump(S, open("data/specialists_data.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"saved {len(S)} specialists")
sections = {}
for s in S:
    sections[s["section"]] = sections.get(s["section"], 0) + 1
for k, v in sections.items():
    print(f"  {k}: {v}")
