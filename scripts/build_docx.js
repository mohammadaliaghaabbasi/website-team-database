// شبیه‌ساز متخصصان تیم طراحی سایت — سند ورد فارسی RTL
// هر متخصص: کارت کامل با معرفی، پشته فناوری، ستاره‌های واقعی، پلتفرم تمرین، مسیر رشد، سوال مصاحبه
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  Header, Footer, PageNumber, AlignmentType, HeadingLevel, WidthType,
  BorderStyle, ShadingType, PageOrientation, TableLayoutType, SectionType,
} = require("docx");
const fs = require("fs");
const path = require("path");

const GH = JSON.parse(fs.readFileSync(path.join(__dirname, "..", "data", "gh_data.json"), "utf-8"));
const stars = (r) => (GH[r] && GH[r].ok) ? GH[r].stars.toLocaleString("en-US") : "—";
const INSPIRATION = JSON.parse(fs.readFileSync(path.join(__dirname, "..", "data", "inspiration_data.json"), "utf-8"));

// ---------- رنگ‌ها (Dawn Mist Tech + بالای سفید) ----------
const P = {
  primary: "0A1628", body: "1A2B40", secondary: "6878A0",
  accent: "5B8DB8", surface: "F4F8FC", surface2: "EDF2F8",
  headerBg: "1B6B7A", cardBorder: "C8DDE2",
};

// ---------- کمکی‌ها ----------
const NB = { style: BorderStyle.NONE, size: 0, color: "FFFFFF" };
const noBorders = { top: NB, bottom: NB, left: NB, right: NB };
const allNoBorders = { ...noBorders, insideHorizontal: NB, insideVertical: NB };

function rtlPara(opts, runs) {
  return new Paragraph({
    bidirectional: true, ...opts, children: runs,
  });
}
function t(text, o = {}) {
  return new TextRun({ text, font: { ascii: "Arial", hAnsi: "Arial", cs: "Tahoma", eastAsia: "Tahoma" }, ...o });
}
// متن فارسی با اندازه پیکسل — size بر حسب half-point
function fa(text, o = {}) { return t(text, o); }

function h1(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_1, bidirectional: true,
    alignment: AlignmentType.RIGHT,
    spacing: { before: 360, after: 160, line: 340 },
    children: [t(text, { bold: true, size: 30, color: P.primary })],
  });
}
function h2(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_2, bidirectional: true,
    alignment: AlignmentType.RIGHT,
    spacing: { before: 260, after: 120, line: 320 },
    children: [t(text, { bold: true, size: 26, color: P.primary })],
  });
}
function h3(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_3, bidirectional: true,
    alignment: AlignmentType.RIGHT,
    spacing: { before: 200, after: 100, line: 312 },
    children: [t(text, { bold: true, size: 24, color: P.headerBg })],
  });
}
// پاراگراف بدنه RTL
function body(text, o = {}) {
  return rtlPara(
    { alignment: AlignmentType.RIGHT, spacing: { line: 312, after: 80 } },
    [fa(text, { size: 22, color: P.body, ...o })]
  );
}
// پاراگراف LTR برای متن انگلیسی/لینک
function bodyEn(text, o = {}) {
  return new Paragraph({
    alignment: AlignmentType.LEFT, spacing: { line: 312, after: 80 },
    children: [t(text, { size: 20, color: "0B5394", ...o })],
  });
}

// ---------- کارت متخصص ----------
// spec = { id, role, roleEn, section, mission, skills: [..], stack: [{name, repo}], practice: [{name, url, note}], path: [..], interview: [...] }
function specialistCard(spec, index) {
  const children = [];
  // خط موضوع کارت (نه هدرینگ — عنوان نقش بالای کارت در H2 آمده)
  children.push(new Paragraph({
    bidirectional: true, alignment: AlignmentType.RIGHT,
    spacing: { before: index === 0 ? 60 : 340, after: 40, line: 320 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 12, color: P.accent, space: 6 } },
    children: [
      fa("مأموریت در تیم: ", { bold: true, size: 24, color: P.headerBg }),
      fa(spec.mission, { size: 24, color: P.body }),
    ],
  }));

  // جدول مهارت‌های کلیدی — دو ستونه RTL
  const skillRows = spec.skills.map((s) =>
    new TableRow({
      cantSplit: true,
      children: [
        new TableCell({
          width: { size: 50, type: WidthType.PERCENTAGE }, borders: noBorders,
          margins: { top: 30, bottom: 30, left: 100, right: 100 },
          shading: { type: ShadingType.CLEAR, fill: "FFFFFF" },
          children: [rtlPara({ alignment: AlignmentType.RIGHT }, [fa("• " + s, { size: 20, color: P.body })])],
        }),
        new TableCell({
          width: { size: 50, type: WidthType.PERCENTAGE }, borders: noBorders,
          margins: { top: 30, bottom: 30, left: 100, right: 100 },
          shading: { type: ShadingType.CLEAR, fill: "FFFFFF" },
          children: [rtlPara({ alignment: AlignmentType.RIGHT }, [fa("", { size: 20 })])],
        }),
      ].length === 2 ? [
        new TableCell({
          width: { size: 50, type: WidthType.PERCENTAGE }, borders: noBorders,
          margins: { top: 30, bottom: 30, left: 100, right: 100 },
          children: [rtlPara({ alignment: AlignmentType.RIGHT }, [fa("• " + s, { size: 20, color: P.body })])],
        }),
      ] : [],
    })
  );
  // مهارت‌ها ساده‌تر: تک‌ستون با بولت — جدول لازم نیست
  children.push(h3("مهارت‌های کلیدی"));
  for (const s of spec.skills) {
    children.push(rtlPara(
      { alignment: AlignmentType.RIGHT, indent: { right: 280 }, spacing: { after: 40, line: 300 } },
      [fa("◄ ", { size: 18, color: P.accent }), fa(s, { size: 21, color: P.body })]
    ));
  }

  // پشته فناوری + ستاره واقعی
  children.push(h3("پشته فناوری برگزیده (با ستاره واقعی گیت‌هاب)"));
  const stackRows = [
    new TableRow({
      tableHeader: true, cantSplit: true,
      children: [
        new TableCell({
          width: { size: 40, type: WidthType.PERCENTAGE },
          shading: { type: ShadingType.CLEAR, fill: P.headerBg },
          margins: { top: 40, bottom: 40, left: 100, right: 100 },
          children: [rtlPara({ alignment: AlignmentType.RIGHT }, [fa("ابزار / فناوری", { bold: true, size: 20, color: "FFFFFF" })])],
        }),
        new TableCell({
          width: { size: 34, type: WidthType.PERCENTAGE },
          shading: { type: ShadingType.CLEAR, fill: P.headerBg },
          margins: { top: 40, bottom: 40, left: 100, right: 100 },
          children: [new Paragraph({ alignment: AlignmentType.LEFT }, [t("GitHub repo", { bold: true, size: 18, color: "FFFFFF" })])],
        }),
        new TableCell({
          width: { size: 26, type: WidthType.PERCENTAGE },
          shading: { type: ShadingType.CLEAR, fill: P.headerBg },
          margins: { top: 40, bottom: 40, left: 100, right: 100 },
          children: [rtlPara({ alignment: AlignmentType.CENTER }, [fa("ستاره واقعی", { bold: true, size: 20, color: "FFFFFF" })])],
        }),
      ],
    }),
    ...spec.stack.map((s, i) =>
      new TableRow({
        cantSplit: true,
        children: [
          new TableCell({
            width: { size: 40, type: WidthType.PERCENTAGE },
            shading: { type: ShadingType.CLEAR, fill: i % 2 === 0 ? P.surface : "FFFFFF" },
            margins: { top: 30, bottom: 30, left: 100, right: 100 },
            children: [rtlPara({ alignment: AlignmentType.RIGHT }, [fa(s.name, { size: 20, color: P.body })])],
          }),
          new TableCell({
            width: { size: 34, type: WidthType.PERCENTAGE },
            shading: { type: ShadingType.CLEAR, fill: i % 2 === 0 ? P.surface : "FFFFFF" },
            margins: { top: 30, bottom: 30, left: 100, right: 100 },
            children: [new Paragraph({ alignment: AlignmentType.LEFT }, [t(s.repo, { size: 17, color: "0B5394" })])],
          }),
          new TableCell({
            width: { size: 26, type: WidthType.PERCENTAGE },
            shading: { type: ShadingType.CLEAR, fill: i % 2 === 0 ? P.surface : "FFFFFF" },
            margins: { top: 30, bottom: 30, left: 100, right: 100 },
            children: [rtlPara({ alignment: AlignmentType.CENTER }, [fa(stars(s.repo), { size: 20, color: P.headerBg, bold: true })])],
          }),
        ],
      })
    ),
  ];
  children.push(new Table({
    width: { size: 100, type: WidthType.PERCENTAGE },
    layout: TableLayoutType.FIXED, borders: {
      top: { style: BorderStyle.SINGLE, size: 4, color: P.cardBorder },
      bottom: { style: BorderStyle.SINGLE, size: 4, color: P.cardBorder },
      left: NB, right: NB, insideHorizontal: { style: BorderStyle.SINGLE, size: 2, color: "D8E4EC" }, insideVertical: NB,
    },
    rows: stackRows,
  }));

  // شبیه‌ساز / پلتفرم تمرین
  children.push(h3("شبیه‌ساز و پلتفرم تمرین"));
  for (const p of spec.practice) {
    children.push(rtlPara(
      { alignment: AlignmentType.RIGHT, indent: { right: 280 }, spacing: { after: 40, line: 300 } },
      [
        fa("◄ ", { size: 18, color: P.accent }),
        fa(p.name + " — ", { bold: true, size: 21, color: P.body }),
        fa(p.note + "  ", { size: 21, color: P.body }),
      ]
    ));
    children.push(new Paragraph({
      alignment: AlignmentType.LEFT, indent: { left: 600 }, spacing: { after: 60 },
      children: [t(p.url, { size: 17, color: "0B5394" })],
    }));
  }

  // صفحات الهام و الگو — قبل از شروع کار از این‌ها ایده/الگو بگیر
  const insp = INSPIRATION[spec.role] || [];
  if (insp.length > 0) {
    children.push(h3("صفحات الهام و الگو (قبل از شروع کار مرور شود)"));
    for (const p of insp) {
      children.push(rtlPara(
        { alignment: AlignmentType.RIGHT, indent: { right: 280 }, spacing: { after: 40, line: 300 } },
        [
          fa("◄ ", { size: 18, color: P.accent }),
          fa(p.name + " — ", { bold: true, size: 21, color: P.body }),
          fa(p.note, { size: 21, color: P.body }),
        ]
      ));
      children.push(new Paragraph({
        alignment: AlignmentType.LEFT, indent: { left: 600 }, spacing: { after: 60 },
        children: [t(p.url, { size: 17, color: "0B5394" })],
      }));
    }
  }

  // مسیر رشد
  children.push(h3("مسیر رشد پیشنهادی"));
  spec.path.forEach((step, i) => {
    children.push(rtlPara(
      { alignment: AlignmentType.RIGHT, indent: { right: 280 }, spacing: { after: 40, line: 300 } },
      [
        fa(`${i + 1}. `, { bold: true, size: 21, color: P.headerBg }),
        fa(step, { size: 21, color: P.body }),
      ]
    ));
  });

  // سوال مصاحبه
  children.push(h3("سوال مصاحبه شبیه‌ساز"));
  children.push(rtlPara(
    { alignment: AlignmentType.RIGHT, spacing: { after: 120, line: 300 } },
    [
      fa("«", { size: 21, color: P.secondary }),
      fa(spec.interview, { size: 21, color: P.body, italics: true }),
      fa("»", { size: 21, color: P.secondary }),
    ]
  ));

  return children;
}

// ---------- داده ۵۲ متخصص ----------
// هر کارت: نقش، بخش، مأموریت، مهارت‌ها، پشته (با ریپو برای ستاره واقعی)، تمرین، مسیر، مصاحبه
const SPECIALISTS = require(path.join(__dirname, "..", "data", "specialists_data.json"));

// ---------- مونتاژ سند ----------
const children = [];

// مقدمه (بدون جلد جدا — سند مرجع کاربردی)
children.push(rtlPara(
  { alignment: AlignmentType.RIGHT, spacing: { after: 120, line: 340 } },
  [fa("شبیه‌ساز متخصصان تیم طراحی سایت", { bold: true, size: 40, color: P.primary })]
));
children.push(rtlPara(
  { alignment: AlignmentType.RIGHT, spacing: { after: 200, line: 300 } },
  [fa("۶۱ نقش تخصصی در ۱۹ مرحله از صفر تا صد — همراه پشته فناوری با ستاره‌های واقعی گیت‌هاب، صفحات الهام و الگو، پلتفرم تمرین و مسیر رشد", { size: 22, color: P.secondary })]
));
children.push(rtlPara(
  { alignment: AlignmentType.RIGHT, spacing: { after: 240, line: 300 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: P.accent, space: 10 } } },
  [fa("تاریخ گردآوری ستاره‌ها: ۲۰ نوامبر ۲۰۲۶ — منبع: github.com", { size: 18, color: P.secondary })]
));
children.push(body("این سند نقشه کامل یک تیم طراحی سایت است؛ برای هر نقش، کارتی شامل مأموریت، مهارت‌های کلیدی، پشته فناوری برگزیده (با تعداد ستاره واقعی گیت‌هاب به‌عنوان معیار محبوبیت)، صفحات الهام و الگو، شبیه‌ساز یا پلتفرم تمرین، مسیر رشد گام‌به‌گام و یک سوال مصاحبه شبیه‌ساز آمده است. ترتیب نقش‌ها از استراتژی و مدیریت تا بازاریابی پس از راه‌اندازی چیده شده تا مسیر طبیعی ساخت یک سایت را از صفر تا صد دنبال کند."));
children.push(body("بخش «صفحات الهام و الگو» در هر کارت بر اساس این ایده ساخته شده که پیش از شروع هر کار باید از گالری‌ها و مراجع تخصصی همان حوزه بازدید کرد: نمونه واقعی دیدن، الگوی آماده گرفتن و ترند روز را شنیدن، بعد دست به کار شد. این رویکرد با الهام از پست «۲۱ سایت کاربردی برای ساخت سایت با هوش مصنوعی» در اینستاگرام (farshad_frhni، نوامبر ۲۰۲۵) گسترش یافته و به همه ۶۱ نقش تیم تعمیم داده شده است؛ برای هر نقش ۴ تا ۵ صفحه مرجع انتخاب شده تا هر عضو تیم قبل از شروع کارش، از بهترین نمونه‌های همان حوزه الگو بگیرد."));

// فهرست بخش‌ها — هر بخش H1، هر متخصص کارت
const sectionsMap = {};
for (const s of SPECIALISTS) {
  (sectionsMap[s.section] = sectionsMap[s.section] || []).push(s);
}
let idx = 0;
for (const [section, specs] of Object.entries(sectionsMap)) {
  children.push(h1(section));
  children.push(body(`${specs.length} نقش تخصصی در این مرحله از پروژه فعال‌اند. هر کارت را می‌توانید به‌عنوان شرح شغلی مینیاتوری و برنامه آموزشی همان نقش استفاده کنید.`));
  for (const spec of specs) {
    children.push(h2(`${spec.role} (${spec.roleEn})`));
    children.push(...specialistCard(spec, idx));
    idx++;
  }
}

// جمع‌بندی
children.push(h1("جمع‌بندی و ترکیب تیم"));
children.push(body("برای یک سایت استارتاپی کوچک، شش نقش هسته‌ای کافی است: مدیر پروژه (یا مدیر محصول)، طراح UI/UX، توسعه‌دهنده فرانت‌اند، توسعه‌دهنده بک‌اند، متخصص سئو/محتوا و متخصص DevOps پاره‌وقت. با رشد پروژه، نقش‌های امنیت، تست، آنالیتیکس و بازاریابی به تیم اضافه می‌شوند و در بلندمدت، نقش‌های پشتیبانی و تولید محتوای مستمر تداام حیات سایت را تضمین می‌کنند."));
children.push(body("ستاره‌های گیت‌هاب در این سند واقعی و مربوط به تاریخ ۲۰ نوامبر ۲۰۲۶ هستند؛ با این حال پیش از انتخاب فناوری، به رشد اخیر ریپو، آخرین کامیت‌ها و سلامت جامعه نیز سر بزنید چون ستاره ارزش انباشته است و همیشه معیار تازگی نیست."));

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
  sections: [{
    properties: {
      page: {
        size: { width: 11906, height: 16838 },
        margin: { top: 1200, bottom: 1200, left: 1250, right: 1250 },
      },
    },
    headers: {
      default: new Header({
        children: [rtlPara({ alignment: AlignmentType.RIGHT }, [fa("شبیه‌ساز متخصصان تیم طراحی سایت", { size: 16, color: P.secondary })])],
      }),
    },
    footers: {
      default: new Footer({
        children: [new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [new TextRun({ children: [PageNumber.CURRENT], size: 18, color: P.secondary })],
        })],
      }),
    },
    children,
  }],
});

Packer.toBuffer(doc).then((buf) => {
  fs.writeFileSync(path.join(__dirname, "..", "deliverables", "شبیه‌ساز-متخصصان-تیم-طراحی-سایت.docx"), buf);
  console.log("SAVED docx,", SPECIALISTS.length, "specialists");
});
