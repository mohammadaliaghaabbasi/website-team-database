// سند Word «برنامه‌ریزی صفر تا صد طراحی سایت» — RTL فارسی
// منبع داده: data/workflow_data.json | کاور: recipe R1 (Pure Paragraph, left-aligned) مطابق design-system
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  Header, Footer, PageNumber, AlignmentType, HeadingLevel, WidthType,
  BorderStyle, ShadingType, TableLayoutType, SectionType, NumberFormat,
  TableOfContents, PageBreak,
} = require("docx");
const fs = require("fs");
const path = require("path");

const WF = JSON.parse(fs.readFileSync(path.join(__dirname, "..", "data", "workflow_data.json"), "utf-8"));
const GH = JSON.parse(fs.readFileSync(path.join(__dirname, "..", "data", "gh_data.json"), "utf-8"));

// ---------- پالت Dawn Mist Tech (اسناد فنی) ----------
const P = {
  bg: "0A1628", titleColor: "FFFFFF", subtitleColor: "C9D8EA",
  metaColor: "AFC6DC", accent: "5B8DB8", footerColor: "8FA6BD",
  primary: "0A1628", body: "1A2B40", secondary: "6878A0",
  surface: "F4F8FC", surface2: "EDF2F8", headerBg: "1B6B7A",
};

// ---------- کمکی‌ها ----------
const NB = { style: BorderStyle.NONE, size: 0, color: "FFFFFF" };
const noBorders = { top: NB, bottom: NB, left: NB, right: NB };
const allNoBorders = { ...noBorders, insideHorizontal: NB, insideVertical: NB };
const FA_D = ["۰","۱","۲","۳","۴","۵","۶","۷","۸","۹"];
const fa = (n) => String(n).split("").map(c => /\d/.test(c) ? FA_D[+c] : c).join("");

function t(text, o = {}) {
  return new TextRun({ text, font: { ascii: "Arial", hAnsi: "Arial", cs: "Tahoma", eastAsia: "Tahoma" }, ...o });
}
function rtlPara(opts, runs) {
  return new Paragraph({ bidirectional: true, ...opts, children: runs });
}
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
    spacing: { before: 280, after: 120, line: 320 },
    children: [t(text, { bold: true, size: 26, color: P.primary })],
  });
}
function body(text, o = {}) {
  return rtlPara(
    { alignment: AlignmentType.RIGHT, spacing: { line: 312, after: 100 } },
    [t(text, { size: 22, color: P.body, ...o })]
  );
}
// خط متمایز هدف مرحله
function goalPara(text) {
  return rtlPara({
    alignment: AlignmentType.RIGHT,
    spacing: { before: 60, after: 140, line: 312 },
    border: { right: { style: BorderStyle.SINGLE, size: 14, color: P.accent, space: 8 } },
    indent: { right: 160 },
  }, [
    t("هدف: ", { bold: true, size: 22, color: P.headerBg }),
    t(text, { size: 22, color: P.body }),
  ]);
}
// لیست RTL با نشانگر
function bullet(text, opts = {}) {
  return rtlPara(
    { alignment: AlignmentType.RIGHT, indent: { right: 340 }, spacing: { after: 40, line: 300 } },
    [t("◄ ", { size: 18, color: P.accent }), t(text, { size: 21, color: P.body, ...opts })]
  );
}
// جدول دو ستونه RTL (برچسب | مقدار)
const cellMargins = { top: 60, bottom: 60, left: 120, right: 120 };
function infoTable(rows, labelW = 22) {
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
          width: { size: labelW, type: WidthType.PERCENTAGE },
          margins: cellMargins, shading: { type: ShadingType.CLEAR, fill: P.surface },
          children: [rtlPara({ alignment: AlignmentType.RIGHT }, [t(label, { bold: true, size: 20, color: P.headerBg })])],
        }),
        new TableCell({
          width: { size: 100 - labelW, type: WidthType.PERCENTAGE },
          margins: cellMargins, shading: { type: ShadingType.CLEAR, fill: "FFFFFF" },
          children: [rtlPara({ alignment: AlignmentType.RIGHT }, [t(value, { size: 20, color: P.body })])],
        }),
      ],
    })),
  });
}
// بلوک پرامپت AI (زمین‌مایه متمایز)
function aiPromptBox(stageId, promptText) {
  return new Table({
    width: { size: 100, type: WidthType.PERCENTAGE },
    layout: TableLayoutType.FIXED,
    borders: allNoBorders,
    rows: [new TableRow({
      cantSplit: true,
      children: [new TableCell({
        margins: { top: 100, bottom: 100, left: 160, right: 160 },
        shading: { type: ShadingType.CLEAR, fill: P.surface2 },
        borders: {
          top: NB, bottom: NB, left: NB,
          right: { style: BorderStyle.SINGLE, size: 16, color: P.headerBg, space: 4 },
        },
        children: [
          rtlPara({ alignment: AlignmentType.RIGHT, spacing: { after: 60 } },
            [t("پرامپت شروع وایب‌کدینگ این مرحله — کپی کن و به دستیار هوش مصنوعی بده:", { bold: true, size: 20, color: P.headerBg })]),
          rtlPara({ alignment: AlignmentType.RIGHT, spacing: { line: 310 } },
            [t(promptText, { size: 20, color: P.body })]),
        ],
      })],
    })],
  });
}

// ---------- کاور R1 (مطابق design-system: پاراگراف خالص، چپ‌چین، فقط بوردر پاراگراف) ----------
function calcTitleLayout(title, maxWidthTwips, preferredPt = 40, minPt = 24) {
  // برای فارسی: پهنای کاراکتر ≈ pt × 12 (میانگین فارسی باریک‌تر از CJK)
  const charWidth = (pt) => pt * 12;
  const charsPerLine = (pt) => Math.floor(maxWidthTwips / charWidth(pt));
  let titlePt = preferredPt, lines;
  const split = (txt, cpl) => {
    if (txt.length <= cpl) return [txt];
    const words = txt.split(" ");
    const out = []; let cur = "";
    for (const w of words) {
      if ((cur + " " + w).trim().length > cpl && cur) { out.push(cur.trim()); cur = w; }
      else cur = (cur + " " + w).trim();
    }
    if (cur) out.push(cur.trim());
    if (out.length > 1 && out[out.length - 1].length <= 4) {
      const last = out.pop(); out[out.length - 1] += " " + last;
    }
    return out;
  };
  while (titlePt >= minPt) {
    const cpl = charsPerLine(titlePt);
    if (cpl < 4) { titlePt -= 2; continue; }
    lines = split(title, cpl);
    if (lines.length <= 3) break;
    titlePt -= 2;
  }
  if (!lines || lines.length > 3) { lines = split(title, charsPerLine(minPt)); titlePt = minPt; }
  return { titlePt, titleLines: lines };
}
function calcCoverSpacing(params) {
  const { titleLineCount = 1, titlePt = 36, hasSubtitle = false, hasEnglishLabel = false,
    metaLineCount = 0, fixedHeight = 800, pageHeight = 16838 } = params;
  const SAFETY = 1200;
  const usableHeight = pageHeight - SAFETY;
  const titleHeight = titleLineCount * (titlePt * 23 + 200);
  const subtitleHeight = hasSubtitle ? (12 * 23 + 600) : 0;
  const englishLabelHeight = hasEnglishLabel ? (9 * 23 + 600) : 0;
  const metaHeight = metaLineCount * (10 * 23 + 100);
  const implicitParaHeight = 3 * 300;
  const contentHeight = titleHeight + subtitleHeight + englishLabelHeight + metaHeight + fixedHeight + implicitParaHeight;
  const remainingSpace = usableHeight - contentHeight;
  const safeRemaining = Math.max(remainingSpace, 400);
  const FOOTER_MIN = 800;
  const rawTop = Math.floor(safeRemaining * 0.45);
  const rawBottom = Math.floor(safeRemaining * 0.45);
  const bottomSpacing = Math.max(rawBottom, FOOTER_MIN);
  const topSpacing = Math.max(rawTop - Math.max(0, FOOTER_MIN - rawBottom), 400);
  return { topSpacing, midSpacing: Math.max(safeRemaining - topSpacing - bottomSpacing, 0), bottomSpacing };
}
function buildCoverR1(config) {
  const PP = config.palette;
  const padL = 1200, padR = 800;
  const availableWidth = 11906 - padL - padR - 300;
  const { titlePt, titleLines } = calcTitleLayout(config.title, availableWidth, 40, 24);
  const titleSize = titlePt * 2;
  const spacing = calcCoverSpacing({
    titleLineCount: titleLines.length, titlePt,
    hasSubtitle: !!config.subtitle, hasEnglishLabel: !!config.englishLabel,
    metaLineCount: (config.metaLines || []).length, fixedHeight: 400,
  });
  const accentLeft = { style: BorderStyle.SINGLE, size: 8, color: PP.accent, space: 12 };
  const children = [];
  children.push(new Paragraph({ spacing: { before: spacing.topSpacing } }));
  if (config.englishLabel) {
    children.push(new Paragraph({
      alignment: AlignmentType.LEFT,
      indent: { left: padL, right: padR }, spacing: { after: 500 },
      border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: PP.accent, space: 8 } },
      children: [new TextRun({ text: config.englishLabel.split("").join("  "),
        size: 18, color: PP.accent, font: { ascii: "Calibri" }, characterSpacing: 40 })],
    }));
  }
  for (let i = 0; i < titleLines.length; i++) {
    children.push(new Paragraph({
      bidirectional: true, alignment: AlignmentType.RIGHT,
      indent: { right: padR, left: padL },
      spacing: { after: i < titleLines.length - 1 ? 100 : 300, line: Math.ceil(titlePt * 23), lineRule: "atLeast" },
      children: [t(titleLines[i], { size: titleSize, bold: true, color: PP.titleColor })],
    }));
  }
  if (config.subtitle) {
    children.push(new Paragraph({
      bidirectional: true, alignment: AlignmentType.RIGHT,
      indent: { right: padR, left: padL }, spacing: { after: 800, line: 340 },
      children: [t(config.subtitle, { size: 24, color: PP.subtitleColor })],
    }));
  }
  for (const line of (config.metaLines || [])) {
    children.push(new Paragraph({
      bidirectional: true, alignment: AlignmentType.RIGHT,
      indent: { right: padR + 200, left: padL }, spacing: { after: 80 },
      border: { right: accentLeft },
      children: [t(line, { size: 24, color: PP.metaColor })],
    }));
  }
  children.push(new Paragraph({ spacing: { before: spacing.bottomSpacing } }));
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
        shading: { type: ShadingType.CLEAR, fill: PP.bg }, borders: noBorders,
        verticalAlign: "top",
        children,
      })],
    })],
  })];
}

// ---------- بدنه سند ----------
const children = [];

// خلاصه اجرایی
children.push(h1("خلاصه اجرایی — چرا این سیستم؟"));
children.push(body(WF.meta.idea));
children.push(body("این سند همان ۱۹ بخش دیتابیس ابزار و ۶۱ کارت متخصص این ریپو را به یک خط تولید ترتیب‌دار تبدیل می‌کند. هر مرحله چهار چیز دارد: ورودی (چه می‌گیرد)، فعالیت (چه می‌کند)، خروجی (چه تحویل می‌دهد) و معیار عبور (کی حق دارد جلو برود). اگر فقط یک صفحه از این سند را بخوانید، همان جدول شش فاز پایین است."));
children.push(infoTable(WF.phases.map(p => [`${p.name} (مراحل ${p.stages})`, p.motto]), 34));
children.push(new Paragraph({ spacing: { after: 120 } }));

// شش قانون طلایی
children.push(h1("شش قانون طلایی اجرا"));
for (let i = 0; i < WF.rules.length; i++) {
  const r = WF.rules[i];
  children.push(rtlPara(
    { alignment: AlignmentType.RIGHT, spacing: { before: 80, after: 40, line: 312 } },
    [t(`قانون ${fa(i + 1)} — ${r.title}: `, { bold: true, size: 22, color: P.headerBg }),
     t(r.text, { size: 22, color: P.body })]
  ));
}
children.push(body("این شش قانون، تفاوت پروژه‌ای است که با برنامه جلو می‌رود و پروژه‌ای که با خوش‌بینی. قانون اول (قرارداد تحویل) مهم‌ترین است: ورودی ناقص را با حدس جلو نبرید؛ برگردید و همان مرحله را کامل کنید."));

// راهنمای وایب‌کدینگ
children.push(h1("راهنمای استفاده در پروژه‌های وایب‌کدینگ"));
children.push(body("وایب‌کدینگ یعنی ساختن محصول با هوش مصنوعی به‌جای تایپ دستی هر خط کد. مشکل رایج آن، خروجی بی‌ریشه است: مدل چیزی می‌سازد که «به‌نظر» درست می‌آید اما به بریف، کاربر و برند ربطی ندارد. راه‌حل، تغذیه مدل با سند ورودی هر مرحله است."));
children.push(bullet("قدم ۱ — بریف بساز: پرامپت مرحله ۱ (فصل مراحل) را به دستیار بده؛ خروجی PRD است و سنگ بنای همه‌چیز."));
children.push(bullet("قدم ۲ — مرحله‌به‌مرحله: پرامپت آماده هر مرحله را بده + کارت‌های متخصص همان مرحله (سند شبیه‌ساز) را به‌عنوان شرح نقش ضمیمه کن + صفحات الهام همان نقش‌ها را برای الگوبرداری باز کن."));
children.push(bullet("قدم ۳ — با معیار بسنج: خروجی را با «معیار عبور» همان مرحله مقایسه کن؛ رد نشد، جلو نرو."));
children.push(bullet("قدم ۴ — بایگان کن: سند هر مرحله را با شماره در پوشه docs پروژه‌ات ذخیره کن (01-brief.md و بعدی‌ها) — ورودی مرحله بعد همین‌ها هستند."));
children.push(body("با این چرخه، هر جلسه وایب‌کدینگ یک ورودی سند دارد، یک خروجی سند می‌سازد و قابل بازبینی است — همان چیزی که پروژه‌های دستی را قابل مدیریت می‌کرد، حالا برای پروژه‌های هوش مصنوعی هم برقرار است."));

// مراحل ۱۹گانه
children.push(h1("نوزده مرحله به تفصیل"));
children.push(body("هر مرحله با یک جدول مشخصات (ورودی/فعالیت/خروجی/مسئولان/ابزار/معیار عبور) و یک پرامپت آماده شروع ارائه می‌شود. ستاره‌های گیت‌هاب واقعی و مربوط به ۲۰ نوامبر ۲۰۲۶ هستند."));

for (const s of WF.stages) {
  children.push(h2(`مرحله ${fa(s.id)} — ${s.title} (${s.titleEn})`));
  children.push(goalPara(s.goal));
  const toolsTxt = s.tools.map(([repo, desc]) => {
    const st = GH[repo] && GH[repo].ok ? ` (⭐${GH[repo].stars.toLocaleString("en-US")})` : "";
    return `${repo}${st} — ${desc}`;
  }).join("؛ ");
  children.push(infoTable([
    ["فاز", `${s.phase} — مراحل ${s.stages}`.replace(/ — مراحل.*/, "")],
    ["ورودی‌ها", s.entry.join("؛ ")],
    ["فعالیت‌ها", s.activities.join("؛ ")],
    ["خروجی‌ها", s.exit.join("؛ ")],
    ["مسئولان", s.roles.join("، ")],
    ["ابزارهای برگزیده", toolsTxt],
    ["معیار عبور", s.gate],
    ["توالی و موازی‌سازی", `${s.duration} | ${s.parallel}`],
  ], 24));
  children.push(new Paragraph({ spacing: { after: 80 } }));
  children.push(aiPromptBox(s.id, s.aiBrief));
  children.push(new Paragraph({ spacing: { after: 160 } }));
}

// چک‌لیست و دفترچه
children.push(h1("چک‌لیست سریع مدیر پروژه"));
children.push(body("این چک‌لیست خلاصه معیارهای عبور همه مراحل است؛ اولین خانه خام از بالا، همان مرحله‌ای است که پروژه در آن گیر کرده. برای هر پروژه جدید، از همین فهرست شروع کنید."));
const checklist = [
  "مرحله ۱: بریف + MVP + KPI تأیید ذی‌نفعان",
  "مرحله ۲: ۳ پرسونا + سفر کاربر + تحلیل رقبا",
  "مرحله ۳: برندبوک v1 + بسته لوگو",
  "مرحله ۴: وایرفریم همه صفحات + تست با ۵ کاربر (تکمیل جریان ≥ ۸۰٪)",
  "مرحله ۵: طراحی نهایی + دیزاین سیستم (حداقل ۱۵ کامپوننت)",
  "مرحله ۶: متن نهایی همه صفحات (صفر لورم‌ایپسوم)",
  "مرحله ۹ و ۸: مدل داده + قرارداد API منتشر شد",
  "مرحله ۷: فرانت کامل (a11y ≥ ۹۰، صفر خطای کنسول)",
  "مرحله ۱۰: خرید آزمایشی سرتاسری موفق",
  "مرحله ۱۱: صفر آسیب‌پذیری بحرانی/بالا",
  "مرحله ۱۲: تست E2E سبز + تست بار ۳ برابری",
  "مرحله ۱۳: استقرار زیر ۳۰ دقیقه + آپ‌تایم + تمرین بازیابی",
  "مرحله ۱۴ و ۱۵: سئو ≥ ۹۵ + Core Web Vitals سبز",
  "مرحله ۱۶: رخدادها + داشبورد KPI + اولین A/B",
  "مرحله ۱۷: اسناد حقوقی منطبق بر داده‌های واقعی",
  "مرحله ۱۸: کانال پشتیبانی + ۱۰ مقاله مرکز کمک",
  "مرحله ۱۹: ۲ کانال اکتساب + توالی ایمیل + گزارش ROI",
];
for (const c of checklist) children.push(bullet(c));
children.push(new Paragraph({ spacing: { after: 100 } }));

children.push(h1("دفترچه راهنمای فوری"));
children.push(body("شش موقعیت پرتکرار هر پروژه و فرمول پاسخ سیستم. این جدول را در دسترس نگه دارید؛ پاسخ هر سوال «کدام مرحله» است، نه شروع دوباره از صفر."));
children.push(infoTable([
  ["«می‌خواهم سایتی بسازم، از کجا شروع کنم؟»", "مرحله ۱ — پرامپت بریف را بده؛ تا PRD تأیید نشده سراغ چیز دیگری نرو"],
  ["«طرح قشنگی دیدم، مثلش بساز»", "اول مرحله ۲ (پرسونا) و ۴ (وایرفریم)؛ زیبایی کار مرحله ۵ است"],
  ["«هوش مصنوعی کد را خراب می‌کند»", "ورودی سند نبود؛ خروجی مرحله قبل را کامل تحویل بده (قانون ۱)"],
  ["«فرانت منتظر بک‌اند است»", "قرارداد API هنوز منتشر نشده (قانون ۳)"],
  ["«پروژه لنگ است و نمی‌دانم کجاست»", "چک‌لیست بالا را چک کن؛ اولین خانه خام، مرحله گیرکرده است"],
  ["«سایت لانچ شد، حالا چی؟»", "فاز رشد: ۱۴ و ۱۵ موازی، سپس ۱۶، ۱۷، ۱۸ و ۱۹"],
], 38));
children.push(new Paragraph({ spacing: { after: 120 } }));

children.push(h1("جمع‌بندی"));
children.push(body("این سیستم عمداً روی همان ۱۹ بخش و ۶۱ نقش دیتابیس سوار شده است تا سه سند این ریپو یک زبان مشترک داشته باشند: دیتابیس ابزار می‌گوید «با چه چیزی»، شبیه‌ساز متخصصان می‌گوید «چه کسی» و این سند می‌گوید «کِی و با چه ترتیبی». هر پروژه طراحی سایت — از لندینگ تک‌صفحه‌ای تا فروشگاه کامل — از همین نقطه صفر شروع می‌شود و با همان چرخه رشد، تازه می‌ماند. برای هر پروژه جدید، فقط بریف عوض می‌شود؛ نقشه، ثابت است."));

// ---------- فوتر شماره صفحه ----------
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
    [t("برنامه‌ریزی صفر تا صد طراحی سایت", { size: 16, color: P.secondary })])],
});

const pgSize = { width: 11906, height: 16838 };
const pgMargin = { top: 1200, bottom: 1200, left: 1250, right: 1250 };

const doc = new Document({
  creator: "Z.ai",
  styles: {
    default: {
      document: {
        run: { font: { ascii: "Arial", hAnsi: "Arial", cs: "Tahoma", eastAsia: "Tahoma" }, size: 22, color: P.body },
        paragraph: { spacing: { line: 312 } },
      },
    },
  },
  sections: [
    { // سکشن ۱: کاور — بدون شماره صفحه
      properties: { page: { size: pgSize, margin: { top: 0, bottom: 0, left: 0, right: 0 } } },
      children: buildCoverR1({
        palette: { bg: P.bg, titleColor: P.titleColor, subtitleColor: P.subtitleColor,
          metaColor: P.metaColor, accent: P.accent, footerColor: P.footerColor },
        englishLabel: "ZERO TO LAUNCH SYSTEM",
        title: "برنامه‌ریزی صفر تا صد طراحی سایت",
        subtitle: "سیستم اجرای دقیق از ایده تا لانچ و رشد — مبتنی بر ۱۹ مرحله، ۶۱ نقش تخصصی و ۱۸۳ ابزار متن‌باز",
        metaLines: [
          "نسخه ۱.۰ — ۲۱ نوامبر ۲۰۲۶",
          "شش فاز • نوزده مرحله • شصت‌ویک نقش • صدوهشتادوسه ابزار",
          "همراه: شبیه‌ساز متخصصان + دیتابیس ابزار + صفحات الهام",
        ],
        footerLeft: "website-team-database",
        footerRight: "مبنای اولیه هر پروژه وایب‌کدینگ",
      }),
    },
    { // سکشن ۲: فهرست مطالب — اعداد رومی
      properties: {
        type: SectionType.NEXT_PAGE,
        page: { size: pgSize, margin: pgMargin,
          pageNumbers: { start: 1, formatType: NumberFormat.UPPER_ROMAN } },
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
        // بدون PageBreak: سکشن بعدی NEXT_PAGE است و خودش صفحه عوض می‌کند (قانون ضد صفحه سفید)
      ],
    },
    { // سکشن ۳: بدنه — اعداد عربی از ۱
      properties: {
        type: SectionType.NEXT_PAGE,
        page: { size: pgSize, margin: pgMargin,
          pageNumbers: { start: 1, formatType: NumberFormat.DECIMAL } },
      },
      headers: { default: bodyHeader },
      footers: { default: pageFooter() },
      children,
    },
  ],
});

Packer.toBuffer(doc).then((buf) => {
  fs.writeFileSync(path.join(__dirname, "..", "deliverables", "برنامه‌ریزی-صفر-تا-صد-طراحی-سایت.docx"), buf);
  console.log("SAVED docx,", WF.stages.length, "stages");
});
