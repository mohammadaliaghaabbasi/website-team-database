#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Practice platforms & simulators per specialty — shared data for xlsx + docx."""

# هر متخصص: نقش، لینک پلتفرم تمرین/شبیه‌ساز، توضیح فارسی
PRACTICE = {
  "مدیر پروژه": [
    ("GitHub Projects", "github.com/features/issues", "برد کانبان و اسپرینت داخل گیت‌هاب — تمرین واقعی مدیریت تسک"),
    ("OpenProject", "openproject.org", "نرم‌افزار متن‌باز مدیریت پروژه آبشاری و Agile"),
    ("Excalidraw+ Boards", "excalidraw.com", "وایت‌برد برای رترواسپکتیو و نقشه راه تیمی"),
  ],
  "تحلیلگر کسب‌وکار": [
    ("DrawDB", "drawdb.app", "طراحی آنلاین ERD و فلوچارت فرآیند کسب‌وکار"),
    ("PlantUML Web Server", "plantuml.com", "نوشتن دیاگرام فرآیند به‌صورت کد"),
    ("Balsamiq Wireframes (trial)", "balsamiq.com", "ماکاپ سریع و کاغذی برای مستندات نیازمندی"),
  ],
  "تحقیقات کاربر": [
    ("Hotjar (free tier)", "hotjar.com", "هیت‌مپ و ضبط جلسه کاربران واقعی سایت"),
    ("Microsoft Clarity", "clarity.microsoft.com", "ضبط جلسه و هیت‌مپ رایگان مایکروسافت"),
    ("Google Forms", "forms.google.com", "ساخت پرسشنامه و نظرسنجی پرسونا"),
  ],
  "طراح UI": [
    ("Penpot", "penpot.app", "جانشین متن‌باز Figma — طراحی UI و پروتوتایپ"),
    ("Figma (free)", "figma.com", "استاندارد صنعت طراحی UI و دیزاین سیستم"),
    ("Storybook", "storybook.js.org", "ساخت و مرور زنده کامپوننت‌های UI"),
    ("Google Fonts Icons", "fonts.google.com/icons", "کتابخانه آیکون Material برای UI"),
  ],
  "طراح UX": [
    ("Penpot", "penpot.app", "وایرفریم و پروتوتایپ کلیک‌خور متن‌باز"),
    ("tldraw", "tldraw.com", "بوم بی‌نهایت برای فلوی کاربر و IA"),
    ("Coolors", "coolors.co", "تولید پالت رنگی هماهنگ برای طراحی"),
  ],
  "کپی‌رایتر": [
    ("Hemingway Editor", "hemingwayapp.com", "ساده‌نویسی و خوانایی متن تبلیغاتی"),
    ("Grammarly", "grammarly.com", "ویرایش گرامر و لحن متن انگلیسی"),
    ("ChatGPT / Claude", "chat.openai.com", "پیش‌نویس اولیه متن و ایده‌پردازی"),
  ],
  "توسعه‌دهنده فرانت‌اند": [
    ("CodePen", "codepen.io", "زمین بازی HTML/CSS/JS و گالری ایده"),
    ("JSFiddle", "jsfiddle.net", "تست سریع قطعه‌کد فرانت‌اند"),
    ("StackBlitz", "stackblitz.com", "اجرای کامل پروژه React/Vue در مرورگر"),
    ("CSS Battle", "cssbattle.dev", "مسابقه روزانه نوشتن CSS هدفمند"),
    ("Frontend Mentor", "frontendmentor.io", "چالش‌های واقعی طراحی به کد"),
  ],
  "توسعه‌دهنده بک‌اند": [
    ("Roadmap.sh Backend", "roadmap.sh/backend", "نقشه راه کامل یادگیری بک‌اند"),
    ("LocalStack", "localstack.cloud", "شبیه‌ساز AWS روی سیستم شخصی"),
    ("Supabase", "supabase.com", "پستگرس ابری + Auth + API آماده برای تمرین"),
    ("Postman", "postman.com", "طراحی و تست API — استاندارد صنعت"),
    ("Hoppscotch", "hoppscotch.io", "جانشین متن‌باز و سبک Postman"),
  ],
  "مدیر دیتابیس (DBA)": [
    ("pgAdmin + PostgreSQL", "pgadmin.org", "محیط گرافیکی مدیریت پستگرس"),
    ("MongoDB Atlas (free)", "mongodb.com/atlas", "دیتابیس ابری رایگان برای تمرین"),
    ("SQLZoo", "sqlzoo.net", "تمرین تعاملی کوئری SQL"),
    ("DB Fiddle", "db-fiddle.com", "تست کوئری آنلاین بدون نصب"),
    ("DrawDB", "drawdb.app", "طراحی ERD و اسکیمای دیتابیس"),
  ],
  "متخصص فروشگاه آنلاین": [
    ("Medusa Dev Server", "docs.medusajs.com", "راه‌اندازی لوکال فروشگاه هدلس مدرن"),
    ("WooCommerce + WordPress", "woocommerce.com", "فروشگاه‌سازی با اکوسیستم وردپرس"),
    ("Shopify Partner Sandbox", "partners.shopify.com", "محیط توسعه رایگان شاپیفای"),
    ("Stripe Test Mode", "stripe.com/docs/testing", "درگاه پرداخت آزمایشی با کارت تست"),
  ],
  "متخصص امنیت وب": [
    ("OWASP WebGoat", "owasp.org/www-project-webgoat", "آموزش تعاملی آسیب‌پذیری‌های وب با تمرین عملی"),
    ("Hack The Box", "hackthebox.com", "آزمایشگاه عملی نفوذ و دفاع (مجاز)"),
    ("TryHackMe", "tryhackme.com", "مسیرهای یادگیری امنیت با ماشین‌های مجازی"),
    ("PortSwigger Web Security Academy", "portswigger.net/web-security", "آکادمی رایگان تست نفوذ وب از سازنده Burp"),
    ("DVWA", "github.com/digininja/dvwa", "برنامه آسیب‌پذیر عمدی برای تمرین امنیت"),
  ],
  "مهندس QA / تست": [
    ("Playwright Docs + Sandbox", "playwright.dev", "تست E2E چندمرورگری با مستندات تعاملی"),
    ("Sauce Labs Demo", "saucelabs.com", "تست بین‌مرورگری ابری"),
    ("the-internet (Heroku)", "the-internet.herokuapp.com", "صفحات تمرینی مصنوعی برای تست خودکار"),
    ("k6 Cloud", "k6.io", "اسکریپت و اجرای تست بار"),
    ("DemoQA", "demoqa.com", "المان‌های تمرینی برای Selenium/Playwright"),
  ],
  "مهندس DevOps": [
    ("Killercoda", "killercoda.com", "محیط‌های کاتاکودا جدید برای تمرین لینوکس/داکر/کوبرنتیز"),
    ("Play with Docker", "labs.play-with-docker.com", "دوره داکر رایگان در مرورگر"),
    ("Play with Kubernetes", "labs.play-with-k8s.com", "خوشه کوبرنتیز موقت رایگان"),
    ("LocalStack", "localstack.cloud", "شبیه‌ساز سرویس‌های AWS لوکال"),
    ("Vagrant by HashiCorp", "vagrantup.com", "ماشین‌های مجازی یکسان‌سازی‌شده برای تمرین"),
  ],
  "متخصص سئو": [
    ("Google Search Console", "search.google.com/search-console", "مانیتور ایندکس و کلمات کلیدی سایت خودت"),
    ("Screaming Frog (free)", "screamingfrog.co.uk/seo-spider", "خزشگر سئو تا ۵۰۰ URL رایگان"),
    ("Google Lighthouse", "developers.google.com/speed/pagespeed/insights", "ممیزی سئو فنی و Core Web Vitals"),
    ("Ahrefs Webmaster Tools", "ahrefs.com/webmaster-tools", "برای سایت خودت رایگان است"),
    ("Rich Results Test", "search.google.com/test/rich-results", "تست اسکیما و نتایج غنی"),
  ],
  "متخصص عملکرد": [
    ("PageSpeed Insights", "pagespeed.web.dev", "سنجش Core Web Vitals واقعی گوگل"),
    ("WebPageTest", "webpagetest.org", "آزمایش عملکرد از نقاط مختلف جهان"),
    ("Chrome DevTools Performance", "developer.chrome.com/docs/devtools", "پروفایل رندر و حافظه"),
    ("k6 by Grafana", "k6.io", "تست بار و پایداری زیر فشار"),
  ],
  "تحلیلگر داده / آنالیتیکس": [
    ("Google Analytics Demo Account", "analytics.google.com", "حساب دموی رسمی گوگل با داده واقعی فروشگاه"),
    ("PostHog Demo", "posthog.com", "پلتفرم تحلیل محصول با داده نمونه"),
    ("Looker Studio", "lookerstudio.google.com", "ساخت داشبورد از GA4 رایگان"),
    ("Kaggle", "kaggle.com", "دیتاست‌های واقعی برای تمرین تحلیل"),
  ],
  "مدیر CRM": [
    ("Twenty CRM", "twenty.com", "CRM متن‌باز مدرن برای تمرین"),
    ("EspoCRM Demo", "espocrm.com/demo", "دموی آنلاین CRM متن‌باز"),
    ("HubSpot Free CRM", "hubspot.com", "نسخه رایگان CRM و اتوماسیون فروش"),
  ],
  "پشتیبان فنی / کمک‌دسک": [
    ("Chatwoot Cloud", "chatwoot.com", "پشتیبانی چندکاناله با نسخه ابری رایگان"),
    ("Zammad Demo", "zammad.com/en/demo", "دموی آنلاین کمک‌دسک متن‌باز"),
    ("UVdesk Open Source", "uvdesk.com", "تیکتینگ متن‌باز برای تمرین"),
  ],
  "مدیر سوشال مدیا": [
    ("Postiz Cloud", "postiz.com", "زمان‌بندی پست با نسخه ابری"),
    ("Buffer Free Plan", "buffer.com", "زمان‌بندی رایگان شبکه‌های اجتماعی"),
    ("Canva", "canva.com", "طراحی گرافیک پست با قالب‌های آماده"),
  ],
  "تولیدکننده محتوا": [
    ("Obsidian", "obsidian.md", "نوشتن و اتصال ایده‌ها برای تقویم محتوایی"),
    ("DaVinci Resolve (free)", "blackmagicdesign.com/products/davinciresolve", "تدوین حرفه‌ای ویدیو رایگان"),
    ("GIMP", "gimp.org", "ویرایش تصویر متن‌باز"),
    ("CapCut Web", "capcut.com", "تدوین سریع ویدیوی سوشال"),
  ],
  "متخصص ایمیل مارکتینگ": [
    ("Listmonk Demo", "listmonk.app", "دموی آنلاین خبرنامه‌ساز متن‌باز"),
    ("Mailchimp Free", "mailchimp.com", "تا ۵۰۰ مخاطب رایگان — تمرین کمپین"),
    ("Keila", "keila.io", "خبرنامه متن‌باز ساده"),
  ],
}
