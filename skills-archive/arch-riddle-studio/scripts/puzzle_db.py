#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""پایگاه دادهٔ معماها — arch-riddle-studio
فرمان‌ها: list | show <id> | stats | next | add | set-status <id> <status> | export
داده: data/puzzles.json (همان پوشهٔ اسکریپت)
"""
import json, sys, os, argparse, datetime

BASE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(BASE, "..", "data", "puzzles.json")

STATUS_FLOW = ["draft", "teaser-drafted", "published", "collecting", "revealed", "deep-dived"]
GENRE_FA = {"G1": "زاویه", "G2": "نور-زمان", "G3": "ادراک", "G4": "عملکرد",
            "G5": "ساخت", "G6": "مسیر", "G7": "شعر", "G8": "هندسه"}


def load():
    with open(DB, encoding="utf-8") as f:
        return json.load(f)


def save(db):
    db["meta"]["updated_at"] = str(datetime.date.today())
    with open(DB, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)


def cmd_list(db, args):
    season = db["meta"]["season"]
    print(f"🎮 فصل {season} «{db['meta']['season_theme']}» — Boss: معمای #{db['meta']['boss_puzzle']}")
    print(f"{'ID':>3} {'عنوان':<24} {'گونه':<8} {'فضا':<10} {'الهام':<22} {'R/I':<3} {'سطح':<4} وضعیت")
    print("─" * 100)
    for p in db["puzzles"]:
        title = (p["title"] + " " * 24)[:24]
        print(f"{p['id']:>3} {title:<24} {p['genre']:<8} {p['space']:<10} "
              f"{(p['inspiration'][:20]):<22} {p['category']:<3} {p['level']:<4} {p['status']}")


def cmd_show(db, args):
    p = next((x for x in db["puzzles"] if x["id"] == args.id), None)
    if not p:
        sys.exit(f"معمای #{args.id} پیدا نشد")
    print(f"🧩 معمای #{p['id']} — «{p['title']}» ({p['title_en']})")
    print(f"   گونه: {p['genre']} ({p['genre_fa']}) | فضا: {p['space_fa']} | الهام: {p['inspiration']}")
    print(f"   نوع: {'واقعی R' if p['category']=='R' else 'تخیلی I'} | سطح: {p['level']} | وضعیت: {p['status']}")
    print(f"   پاسخ: {p['reveal_days']} روز بعد | مود REVEAL: {p.get('reveal_mode', 'standalone')}")
    print(f"   دوربین: {p['camera_language']}")
    if p.get("analysis"):
        print(f"   انالیز: {p['analysis']}")
    print("\n   راز:")
    print(f"   {p['riddle_core']}\n")
    print("   سرنخ‌ها:")
    for i, c in enumerate(p["clues"], 1):
        print(f"   {i}. {c}")
    print("\n   پاسخ کامل:")
    print(f"   {p['answer_summary']}\n")
    print("   FACTs:")
    for i, fact in enumerate(p["facts"], 1):
        print(f"   {i}. {fact}")
    print(f"\n   هشتگ: {' '.join(p.get('hashtags', []))}")
    if p.get("assets", {}).get("example_dir"):
        print(f"   پکیج نمونه: {p['assets']['example_dir']}")


def cmd_stats(db, args):
    ps = db["puzzles"]
    by_genre = {}
    by_cat = {"R": 0, "I": 0}
    by_status = {}
    for p in ps:
        by_genre[p["genre"]] = by_genre.get(p["genre"], 0) + 1
        by_cat[p["category"]] = by_cat.get(p["category"], 0) + 1
        by_status[p["status"]] = by_status.get(p["status"], 0) + 1
    print("📊 آمار دیتابیس معماها")
    print(f"   کل: {len(ps)} | فصل: {db['meta']['season']} ({db['meta']['season_theme']})")
    print(f"   واقعی (R): {by_cat['R']} | تخیلی (I): {by_cat['I']}")
    print(f"   گونه‌ها: " + ", ".join(f"{g}×{n}" for g, n in sorted(by_genre.items())))
    print(f"   وضعیت‌ها: " + ", ".join(f"{s}×{n}" for s, n in by_status.items()))
    print(f"   میانگین سطح: {sum(p['level'] for p in ps)/len(ps):.1f}")
    reveal_modes = {}
    for p in ps:
        reveal_modes[p.get("reveal_mode", "standalone")] = reveal_modes.get(p.get("reveal_mode", "standalone"), 0) + 1
    print(f"   مود REVEAL: " + ", ".join(f"{m}×{n}" for m, n in reveal_modes.items()))


def cmd_next(db, args):
    """معماهای آمادهٔ تیزر (draft/teaser-drafted) به ترتیب صف فصل"""
    ready = [p for p in db["puzzles"] if p["status"] in ("draft", "teaser-drafted")]
    if not ready:
        print("همهٔ معماها منتشر/پاسخ‌شده‌اند — معمای جدید لازم است (ANALYZE→RIDDLE)")
        return
    print("🗝️ صف انتشار (آمادهٔ تیزر):")
    for p in ready:
        print(f"   #{p['id']:>2} «{p['title']}» — {p['genre']} | سطح {p['level']} | {p['inspiration'][:40]}")


def cmd_add(db, args):
    new_id = max(p["id"] for p in db["puzzles"]) + 1 if db["puzzles"] else 1
    p = {
        "id": new_id, "title": args.title, "title_en": args.title_en or "",
        "genre": args.genre, "genre_fa": GENRE_FA.get(args.genre, ""),
        "space": args.space or "interior", "space_fa": args.space_fa or "",
        "inspiration": args.inspiration or "", "category": args.category,
        "level": args.level, "status": "draft", "created_at": str(datetime.date.today()),
        "analysis": args.analysis, "camera_language": "", "reveal_days": args.reveal_days,
        "reveal_mode": args.reveal_mode, "riddle_core": args.riddle_core,
        "clues": [], "answer_summary": "", "facts": [], "assets": {},
        "scores_awarded": [], "hashtags": ["#معماری", "#معمای_معماری", "#بازی_معماری"]
    }
    db["puzzles"].append(p)
    save(db)
    print(f"✅ معمای #{new_id} «{args.title}» به دیتابیس اضافه شد (draft)")
    print(f"   حالا کاملش کن: clues, answer_summary, facts, camera_language — یا با new_puzzle.py بازسازیش کن")


def cmd_set_status(db, args):
    p = next((x for x in db["puzzles"] if x["id"] == args.id), None)
    if not p:
        sys.exit(f"معمای #{args.id} پیدا نشد")
    old = p["status"]
    p["status"] = args.status
    save(db)
    print(f"🔄 معمای #{args.id} «{p['title']}»: {old} → {args.status}")


def cmd_export(db, args):
    p = next((x for x in db["puzzles"] if x["id"] == args.id), None)
    if not p:
        sys.exit(f"معمای #{args.id} پیدا نشد")
    out = os.path.join(os.getcwd(), f"puzzle_{p['id']:03d}.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(p, f, ensure_ascii=False, indent=2)
    print(f"📤 صادر شد: {out}")


def main():
    parser = argparse.ArgumentParser(description="پایگاه دادهٔ معماها")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list")
    sp = sub.add_parser("show"); sp.add_argument("id", type=int)
    sub.add_parser("stats")
    sub.add_parser("next")
    ap = sub.add_parser("add")
    ap.add_argument("--title", required=True)
    ap.add_argument("--title-en", dest="title_en")
    ap.add_argument("--genre", required=True, choices=list(GENRE_FA))
    ap.add_argument("--space"); ap.add_argument("--space-fa", dest="space_fa")
    ap.add_argument("--inspiration"); ap.add_argument("--category", default="I", choices=["R", "I"])
    ap.add_argument("--level", type=int, default=3)
    ap.add_argument("--analysis", default=None)
    ap.add_argument("--reveal-days", dest="reveal_days", type=int, default=4)
    ap.add_argument("--reveal-mode", dest="reveal_mode", default="standalone",
                    choices=["continuation", "standalone"])
    ap.add_argument("--riddle-core", dest="riddle_core", required=True)
    sp = sub.add_parser("set-status"); sp.add_argument("id", type=int); sp.add_argument("status")
    sp = sub.add_parser("export"); sp.add_argument("id", type=int)
    args = parser.parse_args()
    db = load()
    {"list": cmd_list, "show": cmd_show, "stats": cmd_stats, "next": cmd_next,
     "add": cmd_add, "set-status": cmd_set_status, "export": cmd_export}[args.cmd](db, args)


if __name__ == "__main__":
    main()
