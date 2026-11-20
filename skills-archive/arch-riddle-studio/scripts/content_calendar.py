#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""تقویم محتوا — arch-riddle-studio
--week        برنامهٔ ۷ روز آینده (۳ معما/هفته، چرخهٔ ۴ روزه + روز استراحت/مهمان)
--plan <id>   نقشهٔ ۴+۱ روزهٔ یک معما (تیزر→انتظار→پاسخ→یوتیوب)
--month       نمای ماه (فصل) + کوتاه‌سازی گپ صف
"""
import json, os, sys, argparse, datetime
from datetime import timedelta

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(BASE, "..")
DB = os.path.join(ROOT, "data", "puzzles.json")
STATE = os.path.join(ROOT, "data", "game_state.json")

PERSIAN_DAYS = ["دوشنبه", "سه‌شنبه", "چهارشنبه", "پنج‌شنبه", "جمعه", "شنبه", "یک‌شنبه"]


def load():
    with open(DB, encoding="utf-8") as f:
        return json.load(f)


def load_state():
    if os.path.exists(STATE):
        with open(STATE, encoding="utf-8") as f:
            return json.load(f)
    return None


def cmd_plan(db, args):
    p = next((x for x in db["puzzles"] if x["id"] == args.id), None)
    if not p:
        sys.exit(f"معمای #{args.id} نیست")
    st = load_state()
    gate = (st or {}).get("gates", {}).get(str(p["id"]), {})
    start = datetime.date.fromisoformat(gate["posted_at"]) if gate.get("posted_at") else datetime.date.today()
    reveal = start + timedelta(days=p["reveal_days"])
    print(f"🗓️ نقشهٔ معمای #{p['id']} «{p['title']}» ({p['genre']} — مود {p['reveal_mode']})")
    for d in range(p["reveal_days"] + 1):
        day = start + timedelta(days=d)
        if d == 0:
            act = "🔒 تیزر ۱۰ث ریلز + کپشن معما (TEASER) — game_state.py post"
        elif d < p["reveal_days"]:
            acts = {1: "📱 استوری «؟» طلایی + بهترین حدس — progress", 2: "📱 استوری سرنخ میانی + نظرسنجی", 3: "📱 شب آخر: شمارش معکوس (+سرنخ قوی‌تر اگر شبِ نقض پیدا)"}
            act = acts.get(d, "📱 استوری روزِ مرده نباشد — engagement-playbook §۱")
        else:
            act = ("🔓 REVEAL ریلز ۱۵ث + Shorts یوتیوب + بستهٔ متن + game_state.py reveal — "
                   "۲۱:۰۰ استوری برترین حدس‌ها + تیزر ۳ث معمای بعد")
        wd = PERSIAN_DAYS[day.weekday()]
        print(f"   روز {d} ({day} {wd}): {act}")
    print(f"   حلقه کامل: {p['reveal_days'] + 1} روز — بعد از آن معمای بعدی post می‌شود (هم‌پوشانی ۱ روزه مجاز)")


def cmd_week(db, args):
    st = load_state() or {}
    today = datetime.date.today()
    print(f"🗓️ هفتهٔ {today} تا {today + timedelta(days=6)} — فصل {db['meta']['season']} «{db['meta']['season_theme']}»")
    active = []
    for pid, gate in st.get("gates", {}).items():
        if gate["status"] in ("locked", "open"):
            p = next((x for x in db["puzzles"] if x["id"] == int(pid)), None)
            if p:
                active.append((p, gate))
    if active:
        print("\n🔒 در جریان:")
        for p, gate in active:
            print(f"   #{p['id']} «{p['title']}» — دروازه {gate['status']} | پاسخ: {gate['reveal_at']}")
    ready = [p for p in db["puzzles"] if p["status"] in ("draft", "teaser-drafted")]
    print(f"\n🗝️ صف انتشار آماده ({len(ready)}):")
    for p in ready[:5]:
        print(f"   #{p['id']:>2} «{p['title']}» — {p['genre']} سطح {p['level']}")
    print("\n📝 ریتم استاندارد: ۳ معما/هفته (شنبه/دوشنبه/چهارشنبه تیزر) — پاسخ‌ها ۳-۴ روز بعد")
    print("   هر روز حداقل ۱ استوری — هیچ روزِ مرده‌ای نه (engagement-playbook §۱)")
    if len(ready) < 3:
        print(f"\n⚠️ صف کم است ({len(ready)}) — ANALYZE تازه لازم است: idea-analysis.md → new_puzzle.py --from-analysis")


def cmd_month(db, args):
    st = load_state()
    ps = db["puzzles"]
    done = [p for p in ps if p["status"] in ("revealed", "deep-dived")]
    ready = [p for p in ps if p["status"] in ("draft", "teaser-drafted")]
    active = [p for p in ps if p["status"] in ("published", "collecting")]
    print(f"📆 نمای ماه — فصل {db['meta']['season']} «{db['meta']['season_theme']}» (Boss: #{db['meta']['boss_puzzle']})")
    print(f"   تمام‌شده: {len(done)} | در جریان: {len(active)} | آماده: {len(ready)}")
    weeks_needed = -(-len(ready) // 3) if ready else 0
    print(f"   با ۳ معما/هفته: صف فعلی {weeks_needed} هفته جواب می‌دهد")
    for i, p in enumerate(ready):
        week = i // 3 + 1
        slot = ["تیزر شنبه", "تیزر دوشنبه", "تیزر چهارشنبه"][i % 3]
        print(f"   هفتهٔ {week} {slot}: #{p['id']} «{p['title']}» ({p['genre']}, سطح {p['level']})")
    if db["meta"]["boss_puzzle"] in [p["id"] for p in ready]:
        print(f"\n👑 Boss فصل #{db['meta']['boss_puzzle']} در صف است — در هفتهٔ آخر فصل قرار بگیرد")
    print("\n📊 تله‌متری هفتگی را فراموش نکن: engagement-playbook §۸")
    if st:
        print("   وضعیت بازی: game_state.py status")


def main():
    parser = argparse.ArgumentParser(description="تقویم محتوای پیج")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("week", aliases=["--week"])
    sp = sub.add_parser("plan", aliases=["--plan"]); sp.add_argument("id", type=int)
    sub.add_parser("month", aliases=["--month"])
    args = parser.parse_args()
    db = load()
    {"week": cmd_week, "plan": cmd_plan, "month": cmd_month}[args.cmd](db, args)


if __name__ == "__main__":
    main()
