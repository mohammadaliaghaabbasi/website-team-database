#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ویزارد ساخت پکیج معما — arch-riddle-studio
ساخت examples/puzzle-<id>/ شامل puzzle.json + caption_fa.md + teaser_plan.md + reveal_plan.md
--from-analysis <slug>:  پیش‌پرکردن از analyses/<slug>.md (بذر معما/FACTها)
--quick + فیلدها:        اسکلت با راهنمای پرکردن برای GLM (اجرای مرحلهٔ RIDDLE)
پکیج کامل = خروجی مراحل RIDDLE + TEASER (پرامپت‌ها را GLM طبق film-studio MODE A می‌نویسد)
"""
import json, os, re, sys, argparse, datetime

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(BASE, "..")
DB = os.path.join(ROOT, "data", "puzzles.json")
ANALYSES = os.path.join(ROOT, "analyses")

GENRE_FA = {"G1": "زاویه و حرکت", "G2": "نور و زمان", "G3": "ادراک و توهم", "G4": "عملکرد پنهان",
            "G5": "ساخت و ماده", "G6": "مسیر و توالی", "G7": "شعر و معنا", "G8": "بازی هندسه"}
CAMERA_BY_GENRE = {
    "G1": "orbit مورب + کات بین زاویه‌های گیج‌کننده؛ پاسخ: تک‌شات پیوسته تا نقطهٔ قفل",
    "G2": "قاب «خاموش» در ساعت اشتباه + سایهٔ مشکوک؛ پاسخ: همان قاب در لحظهٔ نور",
    "G3": "POV بدون مرجع انسانی + موتیف صوتی؛ پاسخ: ورود مرجع (انسان/صدا/اندازه)",
    "G4": "ماکروی عنصر «بی‌گناه»؛ پاسخ: عنصر در حال کار + دیاگرام ساده",
    "G5": "ماکروی جزئیات «غلط به‌نظررسان»؛ پاسخ: زوم‌اوت + دیاگرام دقت",
    "G6": "POV گام‌برداشتن با کات‌های نیمه‌کاره؛ پاسخ: تک‌شات کل مسیر",
    "G7": "قاب‌های آرام + تکرار معنادار؛ پاسخ: جفت‌سازی فرم/نماد + موسیقی عاطفی",
    "G8": "فرم‌های مکرر «قانون‌مند»؛ پاسخ: انیمیشن شبکهٔ هندسی روی فرم",
}


def load_db():
    with open(DB, encoding="utf-8") as f:
        return json.load(f)


def save_db(db):
    db["meta"]["updated_at"] = str(datetime.date.today())
    with open(DB, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)


def parse_analysis(slug):
    path = os.path.join(ANALYSES, f"{slug}.md")
    if not os.path.exists(path):
        sys.exit(f"انالیز {slug}.md پیدا نشد — اول ANALYZE کن (idea-analysis.md)")
    with open(path, encoding="utf-8") as f:
        text = f.read()

    fa_digits = "۰۱۲۳۴۵۶۷۸۹"
    def fa2en(s):
        return "".join(str(fa_digits.index(c)) if c in fa_digits else c for c in s)

    def clean(s):
        return " ".join(line.strip() for line in s.splitlines()).strip()

    clues = []
    for label in ["سرنخ ۱ (عمومی)", "سرنخ ۲ (میانی)", "سرنخ ۳ (عمیق)"]:
        m = re.search(re.escape(label) + r":\*\*\s*(.+?)(?=\n- |\n## |\Z)", text, re.S)
        if m:
            clues.append(clean(m.group(1)))
    facts_block = re.search(r"FACT ها برای پاسخ[^\n]*\n(.+?)(?=\n- \*\*|\n##|\Z)", text, re.S)
    facts = []
    if facts_block:
        block = re.sub(r"\n\s+", " ", facts_block.group(1))  # خطوط تورفته را بچسبان
        facts = [clean(x) for x in re.findall(r"\d[.)]\s+([^0-9].+?)(?=\s*\d[.)]\s|\Z)", block)]
    facts = [f for f in facts if f and not f.startswith("**")][:5]
    core = re.search(r"## ایدهٔ هسته[^\n]*\n\s*\*\*(.+?)\*\*", text, re.S)
    genre = re.search(r"\*\*گونه/فضا/سطح:\*\*\s*(G\d)", text)
    space = re.search(r"\*\*گونه/فضا/سطح:\*\*\s*G\d\s*/\s*([^/(\n]+)", text)
    level = re.search(r"سطح[ /:]*([۰-۹0-9])", text)
    title_src = re.search(r"^#\s*انالیز:\s*(.+?)(?:\s+—|\s*$)", text, re.M)
    return {
        "raw": text,
        "source_name": clean(title_src.group(1)) if title_src else slug,
        "core_idea": clean(core.group(1)) if core else "",
        "seed_genre": genre.group(1) if genre else "",
        "seed_space": clean(space.group(1)) if space else "",
        "seed_level": fa2en(level.group(1)) if level else "",
        "clues": clues, "facts": facts[:5],
    }


def build_puzzle(db, args, seed=None):
    new_id = max(p["id"] for p in db["puzzles"]) + 1 if db["puzzles"] else 1
    genre = args.genre or (seed["seed_genre"] if seed and seed.get("seed_genre") else "G1")
    seed_level = int(seed.get("seed_level") or 3) if seed else 3
    p = {
        "id": new_id,
        "title": args.title or "«عنوان معما — از لحظهٔ آه انالیز»",
        "title_en": args.title_en or "",
        "genre": genre, "genre_fa": GENRE_FA.get(genre, ""),
        "space": args.space or ((seed or {}).get("seed_space", "").strip()) or "interior",
        "space_fa": (seed or {}).get("seed_space", "").strip(),
        "inspiration": args.inspiration or ((seed or {}).get("source_name", "")),
        "category": args.category, "level": args.level or seed_level,
        "status": "draft", "created_at": str(datetime.date.today()),
        "analysis": f"analyses/{args.from_analysis}.md" if args.from_analysis else None,
        "camera_language": CAMERA_BY_GENRE.get(genre, ""),
        "reveal_days": args.reveal_days,
        "reveal_mode": args.reveal_mode,
        "riddle_core": args.riddle_core or (seed.get("core_idea") if seed else "") or "«یک جمله: راز + شرط آشکارسازی»",
        "clues": (seed.get("clues") if seed and seed.get("clues") else None) or [
            "«سرنخ عمومی: جنبهٔ عجیبِ قابل‌لمس برای همه — بدون تفسیر»",
            "«سرنخ میانی: به مکانیزم نزدیک می‌شود ولی اسم نمی‌برد»",
            "«سرنخ عمیق: فرهنگی/شاعرانه — به ذهنیت/معنا اشاره می‌کند»",
        ],
        "answer_summary": "«ذهن + ایده: نام هنرمند/بنا + مکانیزم در ۲-۳ جمله (با جملهٔ ماندگار انالیز)»",
        "facts": (seed.get("facts") if seed else None) or ["«FACT فکت‌چک‌شده ۱ + منبع»", "«FACT ۲»", "«FACT ۳»"],
        "assets": {}, "scores_awarded": [],
        "hashtags": ["#معماری", "#معمای_معماری", "#بازی_معماری", "#فصل_" + db["meta"]["season_theme"].replace(" ", "_")],
    }
    return p, new_id


CAPTION_TMPL = """# کپشن تیزر — معمای #{id} «{title}» (مرحلهٔ بازی: {id})

## کپشن نهایی (آمادهٔ کپی)

{hook_placeholder}
[صحنه‌آرایی — ۲-۳ جمله: چه می‌بینی؛ بدون لو دادن]

سه سرنخ:
۱️⃣ {clue1}
۲️⃣ {clue2}
۳️⃣ {clue3}

🎮 قانون بازی: هر کامنتِ حدس، یک کلید است. کلیدها دروازهٔ مرحله را باز می‌کنند —
اگر دروازه زودتر باز شود، پاسخ زودتر می‌آید. حل کامل = «ذهن + ایده» (+۵ امتیاز).
(قوانین کامل: هایلایت «قوانین بازی» 🔑)

پاسخ: {reveal_days} روز دیگر — یا هر وقت دروازه باز شود.

{hashtags}

---

## چک‌لیست پیش از انتشار (caption-formulas.md §۷)
- [ ] قلاب در ۲ خط اول (از ۱۰ قلاب caption-formulas.md §۲ — متناقض‌نما/عدد عجیب/…)
- [ ] ۳ سرنخ با ترتیب ابهام (عمومی/میانی/عمیق)
- [ ] ممنوعات: نام بنا/شهر/سبک/معمار + واژهٔ کلیدی مکانیزم
- [ ] «؟» طلایی در تیزر جاسازی شود (S2 یا S3)
- [ ] زبان بازی: مرحله + دروازه + کلید + XP
- [ ] هشتگ سه‌لایه (ثابت + گونهٔ {genre} + کمپین)
"""


TEASER_TMPL = """# پلن تولید تیزر — معمای #{id} «{title}» ({genre} / ۱۰ ثانیه / 9:16)

> {source_line}
> خط تولید: film-studio MODE A (استک گوگل: Nano Banana Pro 2 / Veo / Omni Flash) — یا MODE B داخلی

## شات‌لیست ۱۰ث (puzzle-taxonomy.md — زبان دوربین {genre})

```
S1 (0-2s):  قلاب — [اولین قاب: فضا از زاویهٔ «غلط/خاموش/بی‌مرجع» — طبق گونه]
S2 (2-5s):  جزئیات مشکوک — [کلوزآپ عنصر بی‌گناه + جاسازی «؟» طلایی]
S3 (5-8s):  تعلیق — [حرکت دوربین به سمت جواب که نیمه‌کاره کات می‌شود]
S4 (8-10s): کات به سیاه → لوگو + «مرحلهٔ {id}» + «؟»
```

**زبان دوربین {genre}:** {camera}

## پرامپت کی‌فریم (Nano Banana Pro 2 — 768×1344 عمودی)

> کی‌فریم S3 (تعلیق — مهم‌ترین فریم):

```
[STYLE BLOCK ثابت پیج — از examples/puzzle-008/teaser_plan.md کپی کن]
SCENE: [شرح دقیق صحنهٔ S3 از زاویهٔ قطع‌شده — بدون لو دادن راز]
[نور/پالت/مود — هماهنگ با STYLE BLOCK] — no people, no text, 9:16 vertical.
```

## پرامپت ویدیو (Veo — ۸ ثانیه)

```
Camera: [حرکت دقیق دوربین طبق S1→S3]
Subject: [موضوع اصلی + حالت «ناقص/در حال شدن»]
Scene: [فضا + نور + پالت]
Style: [STYLE BLOCK]
Camera motion: [یک حرکت پیوسته — قطع دقیقاً پیش از آشکارسازی]
Ambiance: [صدا/محیط]
Duration: 8s, 9:16, 1080p, no people, no text.
```

**دستور ویرایش Omni Flash (اگر اصلاح خواست):**
`Keep everything else the same. [یک تغییر جراحی — مثلاً پایین‌تر/نزدیک‌تر/محو‌تر]`
"""


REVEAL_TMPL = """# 🔓 پاسخ معمای #{id} + یوتیوب DEEP-DIVE

> مود REVEAL: **{reveal_mode}** — {reveal_mode_desc}
> {continuity_note}

## REVEAL — ریلز {reveal_len}ثانیه‌ای (منتشر: روز {reveal_days} — {reveal_date})

### بیت‌بندی (reveal-structure.md §۲)
| بیت | زمان | محتوا |
|-----|------|-------|
| A بازشناسی | 0-2s | {a_bit} |
| B افشا | 2-8s | [لحظهٔ قفل طبق گونهٔ {genre} — «دیده» شود نه «گفته»] |
| C ذهن | 8-12s | [نام ذهن/بنا + جملهٔ ماندگار روی تصویر] |
| D قلاب بعدی | 12-15s | [لوگو + «مرحلهٔ بعد» + ۱ جمله معمای بعد] |

### پرامپت‌های کلیدی (MODE A)
- **کی‌فریم لحظهٔ قفل (Nano Banana):** [همان پرامپت S3 تیزر + حرکت کامل‌شده + راز نمایان]
- **Veo (بیت B):** [تک‌شات حرکت قفل — Camera/Subject/Scene/Style/Ambiance کامل]
- **Omni (اصلاح):** `Keep everything else the same. [یک اصلاح جراحی]`

### کپشن REVEAL (caption-formulas.md §۵)
```
[اعتراف ۱ جمله‌ای — جوابِ قلاب تیزر]
جواب: [ذهن + ایده]
[مکانیزم در ۳-۴ جمله]
[۲-۳ FACT]
🏆 بهترین حدس‌ها: @[کاربر۱] +۵ (کامل!) | …
توضیحِ کامل + داستان واقعی: لینک یوتیوب در بایو ▶️
معمای بعدی، [روز]: «[قلاب معمای بعد]»
#هشتگ‌ها
```

---

## DEEP-DIVE — یوتیوب {yt_len} (Shorts عمودی 9:16 — هم‌روز با REVEAL)

### عنوان (youtube-package.md §۳)
`معمای معماری {id:03d} — [قلاب ≤۶۰ کاراکتر] | [ذهن/بنا]`

### فیلمنامه روایت (۵ پرده — reveal-structure.md §۵)
| پرده | زمان | محتوا |
|------|------|-------|
| ۱ فشردهٔ معما | 0-8s | [همان تیزر + «چرا کار می‌کند؟»] |
| ۲ مسئله | 8-20s | [مسئله/وسواس پشت طراحی — از انالیز] |
| ۳ مکانیزم | 20-40s | [دیاگرام + ۲-۳ FACT عددی] |
| ۴ درس طراحی | 40-50s | [۳ بولت عملی برای معمارها — youtube-package.md §۲] |
| ۵ جملهٔ ماندگار + CTA | 50-60s | [جملهٔ هسته + «مرحلهٔ بعد در اینستاگرام قفل است»] |

### بستهٔ متن یوتیوب (youtube-package.md — ۶ قطعه)
- [ ] عنوان + کاور (قاب لحظهٔ قفل + عدد قاتل)
- [ ] توضیحات: ۵ بلوک (قلاب/تایم‌استمپ/درس طراحی ۳ بولتی/منابع/FAQ از حدس‌های واقعی)
- [ ] پین‌کامنت (سؤال تعاملی + لینک اینستاگرام)
- [ ] کارت پایان + تگ‌ها + پلی‌لیست فصل

## برنامهٔ روز پاسخ (reveal-structure.md §۶)
- ۱۸:۰۰ REVEAL ریلز + پین‌کامنت امتیازها → ۱۸:۳۰ Shorts + بستهٔ متن → ۱۹:۰۰ `game_state.py reveal {id}` → ۲۱:۰۰ استوری «برترین حدس‌ها» + تیزر معمای بعد
"""


def main():
    parser = argparse.ArgumentParser(description="ویزارد پکیج معما")
    parser.add_argument("--from-analysis", dest="from_analysis", help="analyses/<slug>.md")
    parser.add_argument("--quick", action="store_true", help="اسکلت با placeholder")
    parser.add_argument("--title"); parser.add_argument("--title-en", dest="title_en")
    parser.add_argument("--genre", choices=list(GENRE_FA))
    parser.add_argument("--space"); parser.add_argument("--space-fa", dest="space_fa")
    parser.add_argument("--inspiration"); parser.add_argument("--category", default="I", choices=["R", "I"])
    parser.add_argument("--level", type=int)
    parser.add_argument("--reveal-days", dest="reveal_days", type=int, default=4)
    parser.add_argument("--reveal-mode", dest="reveal_mode", default="standalone",
                        choices=["continuation", "standalone"])
    parser.add_argument("--riddle-core", dest="riddle_core")
    args = parser.parse_args()

    seed = parse_analysis(args.from_analysis) if args.from_analysis else None
    db = load_db()
    p, new_id = build_puzzle(db, args, seed)

    if args.from_analysis:
        p["inspiration"] = p["inspiration"] or args.from_analysis
        if seed and seed.get("facts"):
            p["facts"] = seed["facts"][:4]
        if seed and seed.get("clues"):
            p["clues"] = seed["clues"]

    db["puzzles"].append(p)
    save_db(db)

    outdir = os.path.join(ROOT, "examples", f"puzzle-{new_id:03d}")
    os.makedirs(outdir, exist_ok=True)

    with open(os.path.join(outdir, "puzzle.json"), "w", encoding="utf-8") as f:
        json.dump(p, f, ensure_ascii=False, indent=2)

    hooks = "«[قلاب — از ۱۰ قلاب caption-formulas.md — متناقض‌نما/عدد عجیب/وصیت معمار/…]»"
    caption = CAPTION_TMPL.format(
        id=new_id, title=p["title"], hook_placeholder=hooks,
        clue1=p["clues"][0] if p["clues"] else "…", clue2=p["clues"][1] if len(p["clues"]) > 1 else "…",
        clue3=p["clues"][2] if len(p["clues"]) > 2 else "…",
        reveal_days=p["reveal_days"], hashtags=" ".join(p["hashtags"]), genre=p["genre"])
    with open(os.path.join(outdir, "caption_fa.md"), "w", encoding="utf-8") as f:
        f.write(caption)

    teaser = TEASER_TMPL.format(
        id=new_id, title=p["title"], genre=p["genre"], camera=p["camera_language"],
        source_line=(f"منبع فکری: analyses/{args.from_analysis}.md" if args.from_analysis
                     else "منبع فکری: [ذهنیت/بذر معما — از inspiration-matrix یا انالیز تازه]"))
    with open(os.path.join(outdir, "teaser_plan.md"), "w", encoding="utf-8") as f:
        f.write(teaser)

    mode_desc = {
        "continuation": "ویدیوی پاسخ از دقیقاً همان قاب آخرِ تیزر شروع می‌شود و حرکتِ قطع‌شده را کامل می‌کند",
        "standalone": "کلیپ مستقل — با freeze ۰.۵ث روی قاب معروف تیزر شروع می‌شود",
    }[p["reveal_mode"]]
    cont_note = ("پیوستگی قاب: فریم آخر تیزر = کی‌فریم اول پاسخ (Veo First-Frame / Omni: "
                 "«Continue exactly from this frame…»)" if p["reveal_mode"] == "continuation"
                 else "قاب شروع باید در ثانیهٔ اول قابل‌بازشناسی باشد (freeze ۰.۵ث)")
    from datetime import timedelta
    reveal_date = str(datetime.date.today() + timedelta(days=p["reveal_days"]))
    reveal = REVEAL_TMPL.format(
        id=new_id, reveal_mode=p["reveal_mode"], reveal_mode_desc=mode_desc,
        continuity_note=cont_note, reveal_days=p["reveal_days"], reveal_date=reveal_date,
        reveal_len=15, yt_len="۴۵-۶۰ثانیه", genre=p["genre"],
        a_bit=("همان قاب آخر تیزر — freeze ۰.۵ث" if p["reveal_mode"] == "continuation"
               else "freeze روی قاب معروف تیزر + «همان روز، ادامهٔ داستان…»"))
    with open(os.path.join(outdir, "reveal_plan.md"), "w", encoding="utf-8") as f:
        f.write(reveal)

    print(f"🧩 پکیج معمای #{new_id} ساخته شد: examples/puzzle-{new_id:03d}/")
    print("   فایل‌ها: puzzle.json (ثبت در دیتابیس) + caption_fa.md + teaser_plan.md + reveal_plan.md")
    if seed:
        print(f"   پیش‌پر از انالیز «{args.from_analysis}»: {len(seed.get('facts', []))} فکت، "
              f"{len(seed.get('clues', []))} سرنخ، هسته: «{seed.get('core_idea', '')[:60]}…»")
    print("   قدم بعد: placeholder های «…» را با کیفیت RIDDLE پر کن + پرامپت‌های NB/Veo طبق film-studio")


if __name__ == "__main__":
    main()
