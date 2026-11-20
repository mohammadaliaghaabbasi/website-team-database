#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the Excel skills database — RTL Persian, 22 sheets.
Sheet 1: dashboard/summary — top tools of every section
Sheets 2-20: one per section (19 sections)
Sheet 21: practice platforms per specialty
Sheet 22: guide (how to use, sources, date)"""
import json, sys, os
sys.path.insert(0, "skills-archive/xlsx/templates")
sys.path.insert(0, "data")
from base import *  # design tokens + helpers
from practice_data import PRACTICE
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

GH = json.load(open("data/gh_data.json", encoding="utf-8"))

def stars_of(repo):
    v = GH.get(repo, {})
    return v.get("stars")

# ============ 19 sections with their tools ============
# (category, [(group, [(repo, fa_note)])])
SECTIONS = json.load(open("data/sections_data.json", encoding="utf-8"))

wb = Workbook()
wb.properties.creator = "Z.ai"

RTL = Alignment(horizontal="right", vertical="center", wrap_text=True, readingOrder=2)
LTR = Alignment(horizontal="left", vertical="center", wrap_text=True, readingOrder=1)
CENTER = Alignment(horizontal="center", vertical="center", wrap_text=True)

def style_sheet(ws, title, headers, rows, rtl=True, num_cols=None, width_map=None):
    """Standard sheet builder: B2 title, row4 headers, data rows, no gridlines."""
    last_col = len(headers) + 1
    setup_sheet(ws, title=title, last_col=last_col)
    # headers
    for col_idx, h in enumerate(headers, start=2):
        ws.cell(row=4, column=col_idx, value=h)
    style_header_row(ws, row_num=4, col_start=2, col_end=last_col)
    # data
    for i, row_data in enumerate(rows):
        row_num = 5 + i
        for col_idx, value in enumerate(row_data, start=2):
            ws.cell(row=row_num, column=col_idx, value=value)
        style_data_row(ws, row_num=row_num, col_start=2, col_end=last_col, row_index=i)
        # per-cell alignment overrides + number formats
        for col_idx in range(2, last_col + 1):
            c = ws.cell(row=row_num, column=col_idx)
            h = headers[col_idx - 2]
            if h == "ستاره گیت‌هاب":
                c.number_format = "#,##0"
                c.alignment = CENTER
            elif h in ("لینک", "ریپو گیت‌هاب", "پلتفرم", "وب‌سایت"):
                c.alignment = LTR
                c.font = Font(name=FONT_NAME, size=10, color="0B5394")
            else:
                c.alignment = RTL if rtl else LTR
    # widths
    if width_map:
        for col_letter, w in width_map.items():
            ws.column_dimensions[col_letter].width = w
    ws.sheet_view.showGridLines = False
    ws.sheet_view.rightToLeft = True
    ws.freeze_panes = "A5"
    return 5 + len(rows) - 1  # last data row

# ---------- Sheet 1: خلاصه (dashboard) ----------
ws = wb.active
ws.title = "خلاصه"
summary_rows = []
section_totals = []
for cat, groups in SECTIONS:
    all_pairs = [p for g, items in groups for p in items]
    n_tools = len(all_pairs)
    n_gh = len([p for p in all_pairs if stars_of(p[0]) is not None])
    top = sorted([(stars_of(r) or 0, r, note) for r, note in all_pairs], reverse=True)[:3]
    section_totals.append((cat, n_tools, n_gh))
    for rank, (s, r, note) in enumerate(top, 1):
        summary_rows.append((cat, rank, r, s, note))
last = style_sheet(
    ws, "دیتابیس مهارت‌های تیم طراحی سایت — برگ برنده هر بخش",
    ["بخش", "رتبه", "ریپو گیت‌هاب", "ستاره گیت‌هاب", "توضیح فارسی"],
    summary_rows,
    width_map={"B": 24, "C": 7, "D": 34, "E": 15, "F": 46},
)
# note row
note_row = last + 2
ws.cell(row=note_row, column=2, value=f"منبع: گیت‌هاب (github.com) — تعداد ستاره‌های واقعی در تاریخ 2026-11-20. مجموع: {sum(t[1] for t in section_totals)} ابزار در {len(SECTIONS)} بخش.")
ws.cell(row=note_row, column=2).font = font_caption()
ws.cell(row=note_row, column=2).alignment = RTL
ws.merge_cells(start_row=note_row, start_column=2, end_row=note_row, end_column=6)

# ---------- Sheets 2-20: بخش‌ها ----------
for si, (cat, groups) in enumerate(SECTIONS):
    ws = wb.create_sheet(title=cat[:31])
    rows = []
    for g, items in groups:
        for repo, note in items:
            s = stars_of(repo)
            gh_link = f"github.com/{repo}"
            rows.append((g, repo, gh_link, s if s is not None else "—", note))
    last = style_sheet(
        ws, f"بخش {cat} — ابزارها و مهارت‌های برتر",
        ["زیربخش", "ریپو گیت‌هاب", "لینک", "ستاره گیت‌هاب", "توضیح فارسی"],
        rows,
        width_map={"B": 22, "C": 34, "D": 34, "E": 15, "F": 48},
    )
    # total row
    tr = last + 1
    ws.cell(row=tr, column=2, value="مجموع ابزارها")
    ws.cell(row=tr, column=5, value=len(rows))
    style_total_row(ws, row_num=tr, col_start=2, col_end=6)

# ---------- Sheet 21: پلتفرم‌های تمرین ----------
ws = wb.create_sheet(title="شبیه‌ساز و تمرین")
prow = []
for spec, items in PRACTICE.items():
    for name, url, note in items:
        prow.append((spec, name, url, note))
style_sheet(
    ws, "شبیه‌سازها و پلتفرم‌های تمرین هر تخصص",
    ["تخصص", "پلتفرم", "وب‌سایت", "توضیح"],
    prow,
    width_map={"B": 22, "C": 26, "D": 34, "E": 52},
)

# ---------- Sheet 22: راهنما ----------
ws = wb.create_sheet(title="راهنما")
guide_rows = [
    ("هدف فایل", "دیتابیس کامل مهارت‌ها، ابزارها و ریپوهای برتر گیت‌هاب برای تمام تخصص‌های طراحی سایت از صفر تا صد"),
    ("منبع ستاره‌ها", "صفحات رسمی github.com — استخراج مستقیم در تاریخ 2026-11-20"),
    ("تعداد بخش‌ها", "19 بخش تخصصی مطابق چرخه کامل ساخت سایت (استراتژی تا بازاریابی)"),
    ("شیت خلاصه", "سه ابزار برتر هر بخش بر اساس تعداد ستاره — نمای سریع کل دیتابیس"),
    ("شیت‌های بخش‌ها", "19 شیت مجزا؛ هر ابزار با ریپو، لینک، ستاره واقعی و توضیح فارسی"),
    ("شیت شبیه‌ساز", "پلتفرم‌های تمرین و شبیه‌ساز برای 21 تخصص — از CodePen تا Hack The Box"),
    ("نکته RTL", "همه شیت‌ها راست‌به‌چپ هستند؛ لینک‌ها و نام ریپوها برای خوانایی چپ‌به‌راست"),
    ("ستاره چیست؟", "تعداد کاربرانی که ریپو را Star کرده‌اند — معیار محبوبیت و اعتماد جامعه"),
    ("قدیمی و جدید", "ستاره‌ها ارزش انباشته دارند؛ برای سنجش ترند سال به رشد اخیر ریپو هم سر بزنید"),
    ("شروع سریع", "برای هر نقش ابتدا شیت بخش مربوطه، سپس شیت شبیه‌ساز برای تمرین عملی"),
]
style_sheet(
    ws, "راهنمای استفاده از دیتابیس",
    ["موضوع", "توضیح"],
    guide_rows,
    width_map={"B": 18, "C": 80},
)

OUT = "deliverables/دیتابیس-مهارت‌های-طراحی-سایت.xlsx"
wb.save(OUT)
print("SAVED:", OUT)
print("sheets:", wb.sheetnames)
