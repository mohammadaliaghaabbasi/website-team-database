# -*- coding: utf-8 -*-
"""شیت «برنامه‌ریزی صفر تا صد» برای اکسل دیتابیس.
هر ردیف = یک مرحله از ۱۹ مرحله: ورودی/فعالیت/خروجی/مسئولان/ابزارها/معیار عبور/پرامپت وایب‌کدینگ.
منبع داده: data/workflow_data.json"""
import json
import os
from openpyxl.styles import Font, Alignment

WF = json.load(open(os.path.join(os.path.dirname(__file__), "..", "data", "workflow_data.json"), encoding="utf-8"))
GH = json.load(open(os.path.join(os.path.dirname(__file__), "..", "data", "gh_data.json"), encoding="utf-8"))
FA_D = "۰۱۲۳۴۵۶۷۸۹"
fa = lambda n: "".join(FA_D[int(c)] if c.isdigit() else c for c in str(n))


def build(ws, style_sheet, stars_of, LTR, RTL, CENTER, FONT_NAME):
    headers = [
        "مرحله", "عنوان", "فاز", "هدف", "ورودی‌ها (چه می‌گیرد)",
        "فعالیت‌های کلیدی", "خروجی‌ها (چه تحویل می‌دهد)", "مسئولان (۶۱ نقش)",
        "ابزارهای برگزیده (با ستاره)", "معیار عبور", "توالی", "موازی‌سازی",
        "پرامپت شروع وایب‌کدینگ",
    ]
    rows = []
    for s in WF["stages"]:
        tools = "؛ ".join(
            f"{repo}" + (f" ⭐{GH[repo]['stars']:,}" if repo in GH and GH[repo].get("ok") else "") + f" — {desc}"
            for repo, desc in s["tools"]
        )
        rows.append((
            fa(s["id"]), f"{s['title']} ({s['titleEn']})", s["phase"], s["goal"],
            "\n".join(f"• {x}" for x in s["entry"]),
            "\n".join(f"• {x}" for x in s["activities"]),
            "\n".join(f"• {x}" for x in s["exit"]),
            "، ".join(s["roles"]), tools, s["gate"],
            s["duration"], s["parallel"], s["aiBrief"],
        ))
    style_sheet(
        ws, "برنامه‌ریزی صفر تا صد طراحی سایت — ۱۹ مرحله از ایده تا رشد",
        headers, rows,
        width_map={"B": 7, "C": 26, "D": 16, "E": 46, "F": 44, "G": 46, "H": 40,
                   "I": 34, "J": 46, "K": 40, "L": 16, "M": 24, "N": 60},
    )
    # ترازهای خاص: ستون ابزارها LTR، ستون مرحله و توالی وسط‌چین
    for r in range(5, 5 + len(rows)):
        ws.cell(row=r, column=10).alignment = LTR   # ابزارها (ستون J)
        for col in (2, 12):
            ws.cell(row=r, column=col).alignment = CENTER  # مرحله (B) و توالی (L)
    # ارتفاع ردیف‌ها برای خوانایی متن چندخطی
    for r in range(5, 5 + len(rows)):
        ws.row_dimensions[r].height = 110
