#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""موتور بازی «رازِ فضا» — arch-riddle-studio
فرمان‌ها: init | status | map | config | post | progress | solve | reveal | season | players | award | flashback | reset
state: data/game_state.json — منطق دروازه/XP/بج/استریک/شبِ نقض طبق references/game-design.md
flashback: منحنی فراموشی Ebbinghaus [1,2,4,7,15] طبق game-design.md §۹ب
"""
import json, os, sys, argparse, datetime

BASE = os.path.dirname(os.path.abspath(__file__))
STATE = os.path.join(BASE, "..", "data", "game_state.json")
DB = os.path.join(BASE, "..", "data", "puzzles.json")

# آستانه‌های کلید بر اساس فاز رشد (game-design.md §۴)
THRESHOLDS = {
    "آغاز": {"keys": 5, "close": 1},
    "رشد": {"keys": 20, "close": 3},
    "تثبیت": {"keys": 60, "close": 5},
}
XP = {"full": 5, "idea": 3, "mind": 2, "first": 1, "bold": 1, "code": 2}
BADGES = ["کلیددار", "سه‌ضلعی", "ذهنِ جسور", "معمارِ فصل", "مهمان‌ساز"]
REVIEW_INTERVALS = [1, 2, 4, 7, 15]  # روزهای بازگشت Ebbinghaus (game-design.md §۹ب)


def load_state():
    if not os.path.exists(STATE):
        sys.exit("بازی مقداردهی نشده — اول: game_state.py init")
    with open(STATE, encoding="utf-8") as f:
        return json.load(f)


def save_state(st):
    st["updated_at"] = str(datetime.datetime.now())
    with open(STATE, "w", encoding="utf-8") as f:
        json.dump(st, f, ensure_ascii=False, indent=2)


def load_puzzle(pid):
    with open(DB, encoding="utf-8") as f:
        db = json.load(f)
    p = next((x for x in db["puzzles"] if x["id"] == pid), None)
    if not p:
        sys.exit(f"معمای #{pid} در دیتابیس نیست")
    return p


def phase_of(st):
    return st["config"]["phase"]


def threshold_of(st):
    return THRESHOLDS[phase_of(st)]


def rank_of(pl):
    xp, streak = pl.get("xp", 0), pl.get("streak", 0)
    if pl.get("guest_designer"):
        return "هم‌بازی حرفه‌ای"
    if pl.get("season_master"):
        return "استادِ فصل"
    if xp >= 10:
        return "معمارِ معما"
    if streak >= 3:
        return "سه‌ضلعی"
    if pl.get("solves", 0) >= 1:
        return "حدس‌زننده"
    return "بیننده"


def cmd_init(args):
    if os.path.exists(STATE):
        print("بازی از قبل مقداردهی شده — برای شروع تمیز: game_state.py reset")
        return
    st = {
        "game": {"name": "رازِ فضا", "season": 1, "season_theme": "آب", "boss_puzzle": 8,
                 "current_stage": 0, "puzzles_played": 0},
        "gates": {}, "players": {},
        "config": {"phase": "آغاز", "followers": 0},
        "updated_at": None,
    }
    save_state(st)
    print("🎮 بازی «رازِ فضا» مقداردهی شد — فصل ۱ «آب»، فاز آغاز (آستانه: ۵ کلید + ۱ نزدیک)")
    print("   شروع: puzzle_db.py next → سپس game_state.py post <id>")


def cmd_reset(args):
    if os.path.exists(STATE):
        os.remove(STATE)
    cmd_init(args)


def cmd_status(args):
    st = load_state()
    g = st["game"]
    print(f"🎮 «{g['name']}» — فصل {g['season']} «{g['season_theme']}» | Boss: #{g['boss_puzzle']}")
    print(f"   فاز رشد: {phase_of(st)} (فالوور {st['config']['followers']:,}) — "
          f"آستانهٔ دروازه: {threshold_of(st)['keys']} کلید + {threshold_of(st)['close']} نزدیک")
    print(f"   مراحل بازی‌شده: {g['puzzles_played']} | مرحلهٔ جاری: {g['current_stage'] or '—'}")
    if st["gates"]:
        print("\n   دروازه‌ها:")
        for pid, gate in st["gates"].items():
            print(f"     #{pid:>2}: {gate['status']:<9} کلید={gate['keys']} نزدیک={gate['close']} "
                  f"(پاسخ: {gate.get('reveal_at', '—')})")
    if st["players"]:
        print(f"\n   بازیکنان: {len(st['players'])} — لیدربرد: game_state.py players")


def cmd_map(args):
    st = load_state()
    g = st["game"]
    with open(DB, encoding="utf-8") as f:
        db = json.load(f)
    print(f"🗺️ نقشهٔ فصل {g['season']} «{g['season_theme']}» — ۶ قفل تا راز بزرگ")
    for i, p in enumerate(db["puzzles"][:6], 1):
        gate = st["gates"].get(str(p["id"]), {})
        gs = gate.get("status", "⬜ آماده")
        icon = {"locked": "🔒", "open": "🔓", "opened": "✅", "breached": "💥"}.get(gs, "⬜")
        boss = " 👑BOSS" if p["id"] == g["boss_puzzle"] else ""
        print(f"   مرحلهٔ {i} — {icon} «{p['title']}» ({p['genre']}, سطح {p['level']}){boss}")
    print("   «۵ جوابِ مراحل، تکه‌های رمزِ فصل‌اند — کد فصل در Boss رمزگشایی می‌شود.»")


def cmd_config(args):
    st = load_state()
    if args.followers is not None:
        st["config"]["followers"] = args.followers
        st["config"]["phase"] = ("آغاز" if args.followers < 1000 else
                                 "رشد" if args.followers < 10000 else "تثبیت")
        save_state(st)
    print(f"⚙️ فاز: {phase_of(st)} | فالوور: {st['config']['followers']:,} | "
          f"آستانه: {threshold_of(st)['keys']} کلید + {threshold_of(st)['close']} نزدیک")


def cmd_post(args):
    st = load_state()
    p = load_puzzle(args.id)
    today = str(datetime.date.today())
    from datetime import timedelta
    reveal_at = str(datetime.date.today() + timedelta(days=p["reveal_days"]))
    st["gates"][str(p["id"])] = {
        "status": "locked", "keys": 0, "close": 0,
        "posted_at": today, "reveal_at": reveal_at, "opened_at": None, "solvers": []
    }
    st["game"]["current_stage"] = p["id"]
    save_state(st)
    print(f"🔒 مرحلهٔ «{p['title']}» (#{p['id']}) قفل شد — تیزر منتشر شد.")
    print(f"   روز پاسخ: {reveal_at} ({p['reveal_days']} روز) | مود: {p.get('reveal_mode', 'standalone')}")
    print(f"   آستانهٔ باز شدن زودهنگام: {threshold_of(st)['keys']} کلید + {threshold_of(st)['close']} نزدیک")
    print("   یادآوری روزانه: engagement-playbook.md §۱ — هیچ روزِ مرده‌ای نه.")


def cmd_progress(args):
    st = load_state()
    gate = st["gates"].get(str(args.id))
    if not gate:
        sys.exit(f"دروازهٔ #{args.id} باز نشده — اول: post {args.id}")
    gate["keys"] += max(0, args.keys)
    gate["close"] += max(0, args.close)
    save_state(st)
    th = threshold_of(st)
    left_k = max(0, th["keys"] - gate["keys"])
    left_c = max(0, th["close"] - gate["close"])
    print(f"🗝️ دروازهٔ #{args.id}: کلید={gate['keys']}/{th['keys']} | نزدیک={gate['close']}/{th['close']}")
    if gate["status"] == "locked" and left_k == 0 and left_c == 0:
        gate["status"] = "open"
        save_state(st)
        print("   🔓 دروازه باز شد! (جامعه حل کرد) — REVEAL تا ۲۴ ساعت دیگر جلو بیفتد.")
    elif gate["status"] == "locked":
        print(f"   مانده: {left_k} کلید + {left_c} نزدیک — «@x داره نزدیک می‌شه…» (استوری حدس نزدیک)")


def cmd_solve(args):
    st = load_state()
    gate = st["gates"].get(str(args.id))
    if not gate:
        sys.exit(f"دروازهٔ #{args.id} باز نشده — اول: post {args.id}")
    handle = args.user.lstrip("@")
    pl = st["players"].setdefault(handle, {"xp": 0, "streak": 0, "solves": 0, "badges": []})
    kind = args.kind  # full | idea | mind
    xp_gain = XP[kind]
    first_bonus = 1 if handle not in gate["solvers"] else 0
    if args.bold:
        xp_gain = XP["bold"]
    else:
        if kind == "full":
            gate["close"] = max(gate["close"], threshold_of(st)["close"])  # حل کامل = نزدیک تضمینی
        pl["solves"] = pl.get("solves", 0) + 1
        pl["streak"] = pl.get("streak", 0) + 1
        gate["solvers"].append(handle)
    pl["xp"] += xp_gain + first_bonus
    new_badges = []
    if pl["streak"] == 3 and "سه‌ضلعی" not in pl["badges"]:
        pl["badges"].append("سه‌ضلعی"); new_badges.append("🔺 سه‌ضلعی")
    if args.early and "کلیددار" not in pl["badges"] and gate["status"] == "open":
        pl["badges"].append("کلیددار"); new_badges.append("🗝️ کلیددار")
    if args.bold and "ذهنِ جسور" not in pl["badges"]:
        pl["badges"].append("ذهنِ جسور"); new_badges.append("⚡ ذهنِ جسور")
    save_state(st)
    print(f"🏅 @{handle}: +{xp_gain + first_bonus} XP (مجموع {pl['xp']}) — رتبه: {rank_of(pl)}")
    if new_badges:
        print("   بج جدید: " + "، ".join(new_badges) + " — قاعدهٔ جشن: استوری عمومی کن!")
    th = threshold_of(st)
    if gate["status"] == "locked":
        print(f"   دروازه: کلید={gate['keys']}/{th['keys']} | نزدیک={gate['close']}/{th['close']}")
        print("   (حل کامل، «نزدیک» را هم پر می‌کند — اگر کلیدها هم بس است، دروازه باز می‌شود)")


def cmd_reveal(args):
    st = load_state()
    gate = st["gates"].get(str(args.id))
    if not gate:
        sys.exit(f"دروازهٔ #{args.id} باز نشده — اول: post {args.id}")
    if gate["status"] in ("opened", "breached"):
        print(f"دروازهٔ #{args.id} قبلاً {gate['status']} شده است.")
        return
    th = threshold_of(st)
    if gate["keys"] >= th["keys"] and gate["close"] >= th["close"]:
        gate["status"] = "opened"
        print(f"✅ روز پاسخ — دروازهٔ #{args.id} طبق برنامه باز شد (کلیدها کافی بودند).")
    else:
        gate["status"] = "breached"
        print(f"💥 شبِ نقض — جامعه حل نکرد؛ دروازه را از درون باز کردیم… این‌بار.")
        print("   استوری سرنخِ قوی‌ترِ شب آخر — بازی متوقف نمی‌شود (ضد-بلاک).")
    gate["opened_at"] = str(datetime.date.today())
    st["game"]["puzzles_played"] += 1
    st["game"]["current_stage"] = None
    save_state(st)
    print("   اجرای روز پاسخ: reveal-structure.md §۶ (۱۸:۰۰ رییلز → ۱۸:۳۰ Shorts + youtube-package.md → ۱۹:۰۰ این فرمان)")


def cmd_players(args):
    st = load_state()
    if not st["players"]:
        print("هنوز بازیکنی ثبت نشده — progress/solve را پس از کامنت‌ها اجرا کن.")
        return
    print("🏆 لیدربرد «رازِ فضا»")
    rows = sorted(st["players"].items(), key=lambda kv: -kv[1]["xp"])
    for i, (h, pl) in enumerate(rows[:10], 1):
        badges = " ".join(pl.get("badges", []))
        print(f"   {i:>2}. @{h:<20} XP={pl['xp']:<3} حل={pl.get('solves', 0):<3} "
              f"استریک={pl.get('streak', 0):<2} {rank_of(pl)} {badges}")


def cmd_award(args):
    st = load_state()
    handle = args.user.lstrip("@")
    pl = st["players"].setdefault(handle, {"xp": 0, "streak": 0, "solves": 0, "badges": []})
    if args.badge not in BADGES:
        sys.exit(f"بج نامعتبر — مجاز: {', '.join(BADGES)}")
    if args.badge not in pl["badges"]:
        pl["badges"].append(args.badge)
    save_state(st)
    print(f"🎖️ @{handle} بج «{args.badge}» گرفت — جشن عمومی (استوری/کامنت) الزامی.")


def cmd_flashback(args):
    """چالش بازگشت — معماهای در آستانهٔ فراموشی (Ebbinghaus [1,2,4,7,15]) را پیشنهاد می‌دهد."""
    st = load_state()
    with open(DB, encoding="utf-8") as f:
        db = json.load(f)
    titles = {p["id"]: p["title"] for p in db["puzzles"]}
    today = datetime.date.today()
    due, upcoming = [], []
    for pid, gate in st["gates"].items():
        if gate.get("opened_at") is None or gate["status"] not in ("opened", "open", "breached"):
            continue
        opened = datetime.date.fromisoformat(gate["opened_at"])
        days = (today - opened).days
        pid_int = int(pid)
        title = titles.get(pid_int, f"معمای #{pid_int}")
        if days in REVIEW_INTERVALS:
            due.append((days, pid_int, title))
        elif days < max(REVIEW_INTERVALS):
            nxt = min((d - days) for d in REVIEW_INTERVALS if d > days)
            upcoming.append((nxt, pid_int, title, days))
    if not st["gates"]:
        print("هنوز دروازه‌ای باز نشده — flashback بعد از اولین reveal معنا دارد.")
        return
    if due:
        print("🔁 چالش بازگشتِ امروز (آستانهٔ فراموشی — همین حالا استوری/پست کن):")
        for days, pid, title in sorted(due):
            print(f"   «{title}» (#{pid}) — {days} روز از پاسخ گذشته")
            print(f"      فرمت: «یادت هست کدام ذهن بود؟» — سؤال کوتاه، جایزهٔ +۱ (بازی‌سازی، نه حل)")
    else:
        print("🔁 امروز چالش بازگشتی سررسید نیست.")
    if upcoming:
        print("\n   صف بازگشت‌های نزدیک:")
        for nxt, pid, title, days in sorted(upcoming):
            print(f"     «{title}» (#{pid}) — {days} روز گذشته، بازگشت در {nxt} روز دیگر")
    if not due and not upcoming:
        print("   همهٔ معماهای حل‌شده از پنجرهٔ ۱۵ روزه خارج‌اند — کاندیدای «جام فصل».")


def cmd_season(args):
    st = load_state()
    if args.boss:
        st["game"]["boss_puzzle"] = args.boss
    if args.theme:
        st["game"]["season_theme"] = args.theme
        st["game"]["season"] += 1
    save_state(st)
    print(f"👑 فصل {st['game']['season']} «{st['game']['season_theme']}» — Boss: #{st['game']['boss_puzzle']}")
    print("   پوستر فصل + پلی‌لیست یوتیوب جدید + اعلام «۶ قفل تا راز بزرگ»")


def main():
    parser = argparse.ArgumentParser(description="موتور بازی «رازِ فضا»")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("init")
    sub.add_parser("status")
    sub.add_parser("map")
    cp = sub.add_parser("config"); cp.add_argument("--followers", type=int, default=None)
    pp = sub.add_parser("post"); pp.add_argument("id", type=int)
    gp = sub.add_parser("progress"); gp.add_argument("id", type=int)
    gp.add_argument("--keys", type=int, default=1); gp.add_argument("--close", type=int, default=0)
    sp = sub.add_parser("solve"); sp.add_argument("id", type=int); sp.add_argument("user")
    sp.add_argument("kind", choices=["full", "idea", "mind"])
    sp.add_argument("--bold", action="store_true"); sp.add_argument("--early", action="store_true")
    rp = sub.add_parser("reveal"); rp.add_argument("id", type=int)
    sub.add_parser("players")
    ap = sub.add_parser("award"); ap.add_argument("user"); ap.add_argument("badge")
    sub.add_parser("flashback")
    sp2 = sub.add_parser("season"); sp2.add_argument("--boss", type=int); sp2.add_argument("--theme")
    sub.add_parser("reset")
    args = parser.parse_args()
    {"init": cmd_init, "status": cmd_status, "map": cmd_map, "config": cmd_config,
     "post": cmd_post, "progress": cmd_progress, "solve": cmd_solve, "reveal": cmd_reveal,
     "players": cmd_players, "award": cmd_award, "flashback": cmd_flashback,
     "season": cmd_season, "reset": cmd_reset}[args.cmd](args)


if __name__ == "__main__":
    main()
