// گزارش کامل ریپو website-team-database — سند Word فارسی RTL
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  Header, Footer, PageNumber, AlignmentType, HeadingLevel, WidthType,
  BorderStyle, ShadingType, TableLayoutType, SectionType, NumberFormat,
  TableOfContents, PageBreak,
} = require("docx");
const fs = require("fs");
const path = require("path");

const ROOT = __dirname + "/..";
const GH = JSON.parse(fs.readFileSync(path.join(ROOT, "data", "gh_data.json"), "utf-8"));
const WF = JSON.parse(fs.readFileSync(path.join(ROOT, "data", "workflow_data.json"), "utf-8"));
const INS = JSON.parse(fs.readFileSync(path.join(ROOT, "data", "inspiration_data.json"), "utf-8"));
const SPEC = JSON.parse(fs.readFileSync(path.join(ROOT, "data", "specialists_data.json"), "utf-8"));

// آمار واقعی از داده‌ها
const stats = {
  sections: 19,
  tools: 183,
  repos: Object.keys(GH).length,
  okRepos: Object.values(GH).filter(v => v.ok).length,
  specialists: SPEC.length,
  inspirationRoles: Object.keys(INS).length,
  inspirationPages: Object.values(INS).reduce((a, b) => a + b.length, 0),
  workflowStages: WF.stages.length,
  workflowRoles: new Set(WF.stages.flatMap(s => s.roles)).size,
  workflowTools: new Set(WF.stages.flatMap(s => s.tools.map(t => t[0]))).size,
  skills: 80,
};

const P = {
  bg: "0A1628", titleColor: "FFFFFF", subtitleColor: "C9D8EA", metaColor: "AFC6DC",
  accent: "5B8DB8", footerColor: "8FA6BD",
  primary: "0A1628", body: "1A2B40", secondary: "6878A0",
  surface: "F4F8FC", surface2: "EDF2F8", headerBg: "1B6B7A",
};
const NB = { style: BorderStyle.NONE, size: 0, color: "FFFFFF" };
const noBorders = { top: NB, bottom: NB, left: NB, right: NB };
const allNoBorders = { ...noBorders, insideHorizontal: NB, insideVertical: NB };
function t(text, o = {}) {
  return new TextRun({ text, font: { ascii: "Arial", hAnsi: "Arial", cs: "Tahoma", eastAsia: "Tahoma" }, ...o });
}
function rtlPara(opts, runs) { return new Paragraph({ bidirectional: true, ...opts, children: runs }); }
function h1(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_1, bidirectional: true, alignment: AlignmentType.RIGHT,
    spacing: { before: 360, after: 160, line: 340 },
    children: [t(text, { bold: true, size: 30, color: P.primary })],
  });
}
function h2(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_2, bidirectional: true, alignment: AlignmentType.RIGHT,
    spacing: { before: 260, after: 120, line: 320 },
    children: [t(text, { bold: true, size: 26, color: P.primary })],
  });
}
function body(text, o = {}) {
  return rtlPara({ alignment: AlignmentType.RIGHT, spacing: { line: 312, after: 100 } },
    [t(text, { size: 22, color: P.body, ...o })]);
}
function bullet(text) {
  return rtlPara({ alignment: AlignmentType.RIGHT, indent: { right: 340 }, spacing: { after: 40, line: 300 } },
    [t("◄ ", { size: 18, color: P.accent }), t(text, { size: 21, color: P.body })]);
}
const cellMargins = { top: 60, bottom: 60, left: 120, right: 120 };
function infoTable(rows, labelW = 26) {
  const border = { style: BorderStyle.SINGLE, size: 4, color: "C8DDE2" };
  return new Table({
    width: { size: 100, type: WidthType.PERCENTAGE },
    layout: TableLayoutType.FIXED,
    borders: { ...allNoBorders, insideHorizontal: border, insideVertical: border,
      top: border, bottom: border, left: border, right: border },
    rows: rows.map(([label, value]) => new TableRow({
      cantSplit: true,
      children: [
        new TableCell({
          width: { size: labelW, type: WidthType.PERCENTAGE }, margins: cellMargins,
          shading: { type: ShadingType.CLEAR, fill: P.surface },
          children: [rtlPara({ alignment: AlignmentType.RIGHT }, [t(label, { bold: true, size: 20, color: P.headerBg })])],
        }),
        new TableCell({
          width: { size: 100 - labelW, type: WidthType.PERCENTAGE }, margins: cellMargins,
          shading: { type: ShadingType.CLEAR, fill: "FFFFFF" },
          children: [rtlPara({ alignment: AlignmentType.RIGHT }, [t(value, { size: 20, color: P.body })])],
        }),
      ],
    })),
  });
}

// ---------- کاور (همان R1 فشرده) ----------
function buildCoverR1(config) {
  const PP = config.palette;
  const padL = 1200, padR = 800;
  // عنوان کوتاه است — یک خط در ۴۰pt (پهنای فارسی ≈ pt×12)
  const titlePt = 40, titleLines = [config.title];
  const titleSize = titlePt * 2;
  const SAFETY = 1200;
  const usable = 16838 - SAFETY;
  const contentH = titleLines.length * (titlePt * 23 + 200) + (12 * 23 + 600) + (9 * 23 + 600) + 3 * (10 * 23 + 100) + 400 + 900;
  const remaining = Math.max(usable - contentH, 400);
  const bottomSpacing = Math.max(Math.floor(remaining * 0.45), 800);
  const topSpacing = Math.max(Math.floor(remaining * 0.45), 400);
  const accentLeft = { style: BorderStyle.SINGLE, size: 8, color: PP.accent, space: 12 };
  const children = [];
  children.push(new Paragraph({ spacing: { before: topSpacing } }));
  children.push(new Paragraph({
    alignment: AlignmentType.LEFT,
    indent: { left: padL, right: padR }, spacing: { after: 500 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: PP.accent, space: 8 } },
    children: [new TextRun({ text: config.englishLabel.split("").join("  "),
      size: 18, color: PP.accent, font: { ascii: "Calibri" }, characterSpacing: 40 })],
  }));
  for (let i = 0; i < titleLines.length; i++) {
    children.push(new Paragraph({
      bidirectional: true, alignment: AlignmentType.RIGHT,
      indent: { right: padR, left: padL },
      spacing: { after: 300, line: Math.ceil(titlePt * 23), lineRule: "atLeast" },
      children: [t(titleLines[i], { size: titleSize, bold: true, color: PP.titleColor })],
    }));
  }
  children.push(new Paragraph({
    bidirectional: true, alignment: AlignmentType.RIGHT,
    indent: { right: padR, left: padL }, spacing: { after: 800, line: 340 },
    children: [t(config.subtitle, { size: 24, color: PP.subtitleColor })],
  }));
  for (const line of config.metaLines) {
    children.push(new Paragraph({
      bidirectional: true, alignment: AlignmentType.RIGHT,
      indent: { right: padR + 200, left: padL }, spacing: { after: 80 },
      border: { right: accentLeft },
      children: [t(line, { size: 24, color: PP.metaColor })],
    }));
  }
  children.push(new Paragraph({ spacing: { before: bottomSpacing } }));
  children.push(new Paragraph({
    bidirectional: true, alignment: AlignmentType.RIGHT,
    indent: { left: padL, right: padR },
    border: { top: { style: BorderStyle.SINGLE, size: 2, color: PP.accent, space: 8 } },
    spacing: { before: 200 },
    children: [
      t(config.footerRight || "", { size: 16, color: PP.footerColor }),
      t("                                        "),
      t(config.footerLeft || "", { size: 16, color: PP.footerColor }),
    ],
  }));
  return [new Table({
    width: { size: 100, type: WidthType.PERCENTAGE },
    layout: TableLayoutType.FIXED,
    borders: allNoBorders,
    rows: [new TableRow({
      height: { value: 16838, rule: "exact" },
      children: [new TableCell({
        shading: { type: ShadingType.CLEAR, fill: PP.bg }, borders: noBorders, verticalAlign: "top",
        children,
      })],
    })],
  })];
}

// ---------- بدنه ----------
const children = [];

children.push(h1("۱. کلیات و هدف"));
children.push(body("مخزن website-team-database پاسخ مستند به یک سوال بنیادی است: «ساخت یک سایت کامل دقیقاً به چه تخصص‌ها، ابزارها و مراحلی نیاز دارد؟» این ریپو آن پاسخ را در پنج لایه به‌هم‌پیوسته ارائه می‌کند: سیستم برنامه‌ریزی ۱۹ مرحله‌ای، دیتابیس ۱۸۳ ابزار متن‌باز با ستاره واقعی گیت‌هاب، شبیه‌ساز ۶۱ نقش تخصصی، ۲۶۸ صفحه الهام برای همه نقش‌ها و آرشیو ۸۰ اسکیل هوش مصنوعی. همه خروجی‌ها فارسی و راست‌به‌چپ هستند و از پنج فایل داده منفرد (منبع حقیقت) بازتولید می‌شوند."));
children.push(body("کاربرد اصلی ریپو، مبنای اولیه هر پروژه طراحی سایت — به‌خصوص پروژه‌های وایب‌کدینگ با هوش مصنوعی — است: برنامه‌ریزی می‌گوید «کِی و با چه ترتیبی»، دیتابیس می‌گوید «با چه چیزی»، شبیه‌ساز می‌گوید «چه کسی» و صفحات الهام می‌گویند «با چه الگویی»."));

children.push(h1("۲. آمار کلیدی (محاسبه‌شده از خود داده‌ها)"));
children.push(infoTable([
  ["بخش‌های تخصصی", `${stats.sections} بخش (استراتژی تا بازاریابی)`],
  ["ابزارهای آرشیوشده", `${stats.tools} ابزار متن‌باز`],
  ["ریپوهای گیت‌هاب", `${stats.repos} ریپو؛ ${stats.okRepos} مورد با ستاره واکشی موفق (تاریخ ۲۰ نوامبر ۲۰۲۶)`],
  ["کارت‌های شبیه‌ساز متخصص", `${stats.specialists} نقش در ${stats.sections} مرحله`],
  ["صفحات الهام و الگو", `${stats.inspirationPages} صفحه برای ${stats.inspirationRoles} نقش — شامل هر ۲۱ سایت راهنمای BUILD`],
  ["مراحل سیستم برنامه‌ریزی", `${stats.workflowStages} مرحله در ۶ فاز`],
  ["نقش‌های متصل به مراحل", `${stats.workflowRoles} از ${stats.specialists} نقش (پوشش کامل)`],
  ["ابزارهای ارجاع‌شده در مراحل", `${stats.workflowTools} ابزار یکتا (۷۲ ارجاع با احتساب تکرار در چند مرحله) — همه معتبر در دیتابیس`],
  ["پلتفرم‌های تمرین", "۸۲ پلتفرم برای ۲۱ تخصص"],
  ["اسکیل‌های آرشیوشده", `${stats.skills} اسکیل هوش مصنوعی`],
  ["ستاره‌دارترین ابزار", "React — بیش از ۲۵۲ هزار ستاره"],
], 32));
children.push(new Paragraph({ spacing: { after: 120 } }));

children.push(h1("۳. پنج لایه ریپو"));
children.push(h2("۳.۱. سیستم برنامه‌ریزی صفر تا صد (جدیدترین لایه)"));
children.push(body("نقشه اجرای هر پروژه سایت از ایده تا رشد: ۶ فاز (کشف، طراحی، محتوا، ساخت، تضمین کیفیت، رشد) و ۱۹ مرحله. هر مرحله هشت مشخصه دارد: هدف، ورودی‌ها، فعالیت‌ها، خروجی‌ها، مسئولان (نقش‌های شبیه‌ساز)، ابزارهای برگزیده (از دیتابیس)، معیار عبور قابل اندازه‌گیری و پرامپت آماده شروع وایب‌کدینگ. شش قانون طلایی اجرا (قرارداد تحویل، ترتیب=وابستگی، قرارداد API برای موازی‌کاری، برگشت مستند، معیار عبور عینی، وایب‌کدینگ منضبط) ستون فقرات آن است."));
children.push(bullet("WORKFLOW.md — سند اصلی ۵۳۶ خطی با جدول هر ۱۹ مرحله، چک‌لیست مدیر پروژه و دفترچه راهنمای فوری"));
children.push(bullet("data/workflow_data.json — منبع حقیقت ساختاریافته؛ اعتبارسنجی خودکار: صفر ارجاع ناشناخته به نقش یا ابزار"));
children.push(bullet("deliverables/برنامه‌ریزی-صفر-تا-صد-طراحی-سایت.docx و .pdf — سند ۱۷ صفحه‌ای با کاور، فهرست مطالب و ۱۹ جدول مرحله"));
children.push(bullet("شیت «برنامه‌ریزی صفر تا صد» در اکسل — ۱۹ ردیف × ۱۳ ستون برای فیلتر و مرور سریع"));
children.push(h2("۳.۲. دیتابیس ابزارها (اکسل ۲۳ شیتی)"));
children.push(body("۱۸۳ ابزار متن‌باز در ۱۹ بخش؛ هر ابزار با ریپوی گیت‌هاب، لینک، ستاره واقعی (واکشی مستقیم، نه حدس) و توضیح فارسی. شیت خلاصه، سه ابزار برتر هر بخش را بر اساس ستاره نشان می‌دهد؛ شیت‌های بخش‌ها ابزارها را با زیرگروه‌ها ارائه می‌کنند؛ شیت شبیه‌ساز ۸۲ پلتفرم تمرین را برای ۲۱ تخصص فهرست می‌کند و شیت تازه‌اضافه‌شده برنامه‌ریزی، مراحل را در کنار ابزارها می‌آورد."));
children.push(h2("۳.۳. شبیه‌ساز متخصصان (ورد/PDF)"));
children.push(body("۶۱ کارت متخصص در ۱۹ مرحله؛ هر کارت شامل مأموریت در تیم، مهارت‌های کلیدی، پشته فناوری با ستاره واقعی روزِ واکشی، صفحات الهام و الگو، پلتفرم تمرین، مسیر رشد و سوال مصاحبه. این سند به‌عنوان شرح شغلی مینیاتوری و برنامه آموزشی هر نقش قابل استفاده است."));
children.push(h2("۳.۴. صفحات الهام و الگو"));
children.push(body("۲۶۸ صفحه مرجع برای ۶۱ نقش؛ هر عضو تیم قبل از شروع کار، گالری‌ها و مراجع تخصصی حوزه خود را مرور می‌کند. تمام ۲۱ سایت راهنمای BUILD (نویسنده: Sanskaar Singh، ترجمه فارسی) با برچسب منشأ در نقش‌های مرتبط ادغام شده‌اند و همه لینک‌ها اعتبارسنجی HTTP شده‌اند."));
children.push(h2("۳.۵. آرشیو اسکیل‌ها"));
children.push(body("هر ۸۰ اسکیل هوش مصنوعی محیط ساخت، هرکدام با SKILL.md مستقل — قابل کپی به هر محیط agent دیگر برای استفاده مجدد. فهرست کامل در docs/SKILLS-INDEX.md آمده است."));

children.push(h1("۴. نقشه ۱۹ مرحله‌ای (خلاصه سیستم برنامه‌ریزی)"));
children.push(body("ترتیب مراحل نقشه وابستگی است نه فهرست تشریفات. خلاصه هر مرحله با معیار عبورش:"));
const stageSummary = [
  ["۱. استراتژی و مدیریت", "بریف، MVP و KPI تأیید ذی‌نفعان"],
  ["۲. تحقیق کاربر", "۳ پرسونا مبتنی بر داده + سفر کاربر"],
  ["۳. برندینگ", "برندبوک v1 + بسته کامل لوگو"],
  ["۴. طراحی UX", "وایرفریم‌ها + تست با ۵ کاربر (تکمیل جریان ≥ ۸۰٪)"],
  ["۵. طراحی UI", "طراحی نهایی + دیزاین سیستم (≥ ۱۵ کامپوننت)"],
  ["۶. تولید محتوا", "متن نهایی همه صفحات — صفر لورم‌ایپسوم"],
  ["۷. فرانت‌اند", "فرانت کامل؛ a11y ≥ ۹۰؛ صفر خطای کنسول"],
  ["۸. بک‌اند", "قرارداد API منتشرشده + endpoint های تست‌شده"],
  ["۹. دیتابیس", "مهاجرت‌های تکرارپذیر + کوئری‌های تأییدشده"],
  ["۱۰. فروشگاهی", "خرید آزمایشی سرتاسری موفق"],
  ["۱۱. امنیت", "صفر آسیب‌پذیری بحرانی/بالا"],
  ["۱۲. تست و QA", "E2E سبز + تست بار ۳ برابری پیک"],
  ["۱۳. DevOps", "استقرار زیر ۳۰ دقیقه + تمرین بازیابی"],
  ["۱۴. سئو", "Lighthouse سئو ≥ ۹۵ + sitemap بدون خطا"],
  ["۱۵. عملکرد", "Core Web Vitals سبز برای ≥ ۷۵٪ بازدیدها"],
  ["۱۶. آنالیتیکس", "رخدادها + داشبورد KPI + اولین A/B"],
  ["۱۷. حقوقی", "اسناد منطبق بر داده‌های واقعی سایت"],
  ["۱۸. پشتیبانی", "کانال فعال با SLA + ۱۰ مقاله مرکز کمک"],
  ["۱۹. بازاریابی", "۲ کانال اکتساب + توالی ایمیل + گزارش ROI"],
];
children.push(infoTable(stageSummary.map(([a, b]) => [a, b]), 30));
children.push(new Paragraph({ spacing: { after: 120 } }));
children.push(body("نکته موازی‌سازی: مراحل ۷ تا ۱۰ پس از انتشار قرارداد API همزمان پیش می‌روند؛ ۱۱ و ۱۲ موازی‌اند؛ ۱۷ باید پیش از لانچ نهایی شود؛ و فاز ۱۴ تا ۱۹ پس از لانچ چرخه همیشگی رشد است که با بازخورد بازار به مرحله ۱ برمی‌گردد."));

children.push(h1("۵. ساختار فنی و بازتولید"));
children.push(body("معماری ریپو «داده → اسکریپت → خروجی» است: پنج فایل داده در data/ منبع حقیقت‌اند و هیچ خروجی دستی ویرایش نمی‌شود. برای هر تغییر، داده یا اسکریپت مربوطه را ویرایش و بازتولید می‌کنید:"));
children.push(bullet("gh_collect.py — واکشی ستاره‌های واقعی از گیت‌هاب (resume-able؛ فقط موارد ناموفق را دوباره می‌گیرد)"));
children.push(bullet("build_specialists.py — تولید ۶۱ کارت متخصص"));
children.push(bullet("build_inspiration.py — تولید ۲۶۸ صفحه الهام (۶۱ نقش)"));
children.push(bullet("build_workflow.py — تولید داده و سند WORKFLOW.md سیستم برنامه‌ریزی"));
children.push(bullet("build_workflow_docx.js — سند ورد/PDF برنامه‌ریزی (کاور R1، فهرست مطالب، سه سکشن شماره‌گذاری‌شده)"));
children.push(bullet("workflow_sheet.py + build_xlsx.py — اکسل ۲۳ شیتی شامل شیت برنامه‌ریزی"));
children.push(bullet("check_urls.sh — اعتبارسنجی لینک‌های الهام"));
children.push(body("پیش‌نیازها: Python 3.9+ با openpyxl و Node.js 18+ با پکیج docx. راهنمای گسترش کامل در docs/EXTENDING.md و ساختار فیلدهای داده در docs/DATA-MODEL.md مستند است."));

children.push(h1("۶. کیفیت و صحت"));
children.push(bullet("ستاره‌ها واقعی‌اند: واکشی مستقیم از صفحات عمومی github.com در تاریخ ۲۰ نوامبر ۲۰۲۶ (نه برآورد یا حافظه مدل)"));
children.push(bullet("صفر ارجاع ناشناخته: همه ۶۱ نقش و ۷۲ ابزار سیستم برنامه‌ریزی با اسکریپت علیه دیتابیس موجود اعتبارسنجی شده‌اند"));
children.push(bullet("همه لینک‌های الهام با اسکریپت HTTP-چک شده‌اند؛ موارد شکننده برچسب راهنما دارند"));
children.push(bullet("اسناد Word با postcheck اسکیل docx بازبینی شده‌اند: سند برنامه‌ریزی ۹ از ۹ قانون، بدون صفحه سفید و بدون placeholder"));
children.push(bullet("تفکیک واقعیت و فرض: معیارهای عددی (Lighthouse، نرخ‌ها) به‌عنوان معیار عبور پیشنهادی سیستم‌اند، نه ادعای وضعیت فعلی پروژه‌ای خاص"));

children.push(h1("۷. تاریخچه کامیت‌ها و روند رشد"));
children.push(infoTable([
  ["c45345a", "بنیان ریپو: ۱۹ بخش، ۱۸۳ ابزار با ستاره واقعی، ۶۱ کارت متخصص، ۸۲ پلتفرم تمرین + آرشیو ۸۰ اسکیل"],
  ["53732b0", "۲۴۷ صفحه الهام برای هر ۶۱ نقش (ایده از پست «۲۱ سایت کاربردی» — farshad_frhni)"],
  ["73f962c", "ادغام کامل ۲۱ سایت راهنمای BUILD از PDF فارسی؛ ۱۷ سایت جدید اعتبارسنجی‌شده؛ مجموع ۲۶۸ صفحه"],
  ["da2e818", "سیستم برنامه‌ریزی صفر تا صد: WORKFLOW.md، داده ساختاریافته، سند Word/PDF، شیت اکسل؛ اکسل به ۲۳ شیت"],
], 18));
children.push(new Paragraph({ spacing: { after: 120 } }));
children.push(body("ریپو خصوصی است و روی شاخه main نگهداری می‌شود؛ تاریخ ستاره‌ها در هر فصل با یک اجرای gh_collect.py قابل تازه‌سازی است."));

children.push(h1("۸. راهنمای شروع استفاده"));
children.push(body("برای اینکه این ریپو را به‌عنوان اساس اولیه طراحی قرار دهید، سه مسیر پیشنهاد می‌شود. مسیر پروژه جدید: از WORKFLOW.md شروع کنید، پرامپت مرحله ۱ را به دستیار هوش مصنوعی بدهید و مرحله‌به‌مرحله با معیارهای عبور جلو بروید؛ سند هر مرحله را در پوشه docs پروژه خودتان بایگان کنید. مسیر تیم‌سازی: سند شبیه‌ساز را باز کنید تا نقش‌های لازم، شرح شغل و مسیر رشد هر کدام را ببینید و بر اساس اندازه پروژه، تیم حداقلی یا کامل بچینید. مسیر انتخاب ابزار: اکسل را باز کنید، شیت بخش مربوطه را مرور و با ستاره‌ها و توضیح فارسی مقایسه کنید."));
children.push(body("برای توسعه ریپو: ابزار جدید را به gh_collect.py اضافه و واکشی کنید؛ نقش جدید را در build_specialists.py بسازید؛ مرحله یا معیار عبور جدید را در build_workflow.py ویرایش کنید — سپس بازتولید کنید. هیچ خروجی نهایی را دستی تغییر ندهید چون بازتولید می‌شود."));

// ---------- سند ----------
function pageFooter() {
  return new Footer({
    children: [new Paragraph({
      alignment: AlignmentType.CENTER,
      children: [new TextRun({ children: [PageNumber.CURRENT], size: 18, color: P.secondary })],
    })],
  });
}
const bodyHeader = new Header({
  children: [rtlPara({ alignment: AlignmentType.RIGHT },
    [t("گزارش کامل ریپو Website Team Database", { size: 16, color: P.secondary })])],
});
const pgSize = { width: 11906, height: 16838 };
const pgMargin = { top: 1200, bottom: 1200, left: 1250, right: 1250 };

const doc = new Document({
  creator: "Z.ai",
  styles: { default: { document: {
    run: { font: { ascii: "Arial", hAnsi: "Arial", cs: "Tahoma", eastAsia: "Tahoma" }, size: 22, color: P.body },
    paragraph: { spacing: { line: 312 } },
  } } },
  sections: [
    {
      properties: { page: { size: pgSize, margin: { top: 0, bottom: 0, left: 0, right: 0 } } },
      children: buildCoverR1({
        palette: { bg: P.bg, titleColor: P.titleColor, subtitleColor: P.subtitleColor,
          metaColor: P.metaColor, accent: P.accent, footerColor: P.footerColor },
        englishLabel: "REPOSITORY REPORT",
        title: "گزارش کامل ریپو",
        subtitle: "Website Team Database — دیتابیس جامع تخصص‌های طراحی سایت به همراه سیستم برنامه‌ریزی صفر تا صد",
        metaLines: [
          "نسخه ۱.۰ — ۲۱ نوامبر ۲۰۲۶",
          "۵ لایه • ۱۹ مرحله • ۶۱ نقش • ۱۸۳ ابزار • ۲۶۸ صفحه الهام • ۸۰ اسکیل",
          "آدرس: github.com/mohammadaliaghaabbasi/website-team-database",
        ],
        footerLeft: "website-team-database",
        footerRight: "مبنای اولیه هر پروژه وایب‌کدینگ",
      }),
    },
    {
      properties: {
        type: SectionType.NEXT_PAGE,
        page: { size: pgSize, margin: pgMargin, pageNumbers: { start: 1, formatType: NumberFormat.UPPER_ROMAN } },
      },
      headers: { default: bodyHeader },
      footers: { default: pageFooter() },
      children: [
        new Paragraph({
          bidirectional: true, alignment: AlignmentType.CENTER,
          spacing: { before: 480, after: 360 },
          children: [t("فهرست مطالب", { bold: true, size: 32, color: P.primary })],
        }),
        new TableOfContents("Table of Contents", { hyperlink: true, headingStyleRange: "1-2" }),
        new Paragraph({
          spacing: { before: 200 },
          children: [t("یادآوری: این فهرست با کد فیلد ساخته شده است؛ پس از باز کردن فایل در Word روی فهرست راست‌کلیک کرده و «Update Field» را بزنید تا شماره صفحات تازه شود.", { italics: true, size: 18, color: "888888" })],
        }),
      ],
    },
    {
      properties: {
        type: SectionType.NEXT_PAGE,
        page: { size: pgSize, margin: pgMargin, pageNumbers: { start: 1, formatType: NumberFormat.DECIMAL } },
      },
      headers: { default: bodyHeader },
      footers: { default: pageFooter() },
      children,
    },
  ],
});

Packer.toBuffer(doc).then((buf) => {
  fs.writeFileSync("/home/z/my-project/download/گزارش-کامل-ریپو-دیتابیس-تیم-طراحی-سایت.docx", buf);
  console.log("SAVED report docx");
});
