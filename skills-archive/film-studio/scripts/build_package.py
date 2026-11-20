#!/usr/bin/env python3
"""build_package.py — از screenplay.json پکیج تولید کامل می‌سازد

خروجی در production_package/:
  00_README.md          راهنمای اجرا برای کاربر (MODE A/C)
  01_character_sheets.md پرامپت‌های Nano Banana برای Ingredient شخصیت‌ها
  02_shot_prompts.md    برای هر شات: پرامپت کی‌فریم NB + پرامپت Veo + نوت ویرایش Omni
  03_audio_plan.md      متن روایت (برای TTS) + پلان موسیقی
  timeline.json         نقشهٔ تدوین (ورودی assemble.py)

Usage: python3 build_package.py <project-dir> [--copy-scripts]
"""
import argparse
import json
import os
import sys
from datetime import datetime, timezone

LEAD, TAIL, FADE = 0.6, 0.8, 0.8
CREDITS_DUR = 10.0
VEO_STEPS = [4.0, 6.0, 8.0]          # گام‌های مدت کلیپ Veo 3.1
OMNI_MAX = 10.0

SOFT_ERRORS = []


def wpm_dur(text, wpm):
    words = len(text.split())
    return words / wpm * 60.0 if words else 0.0


def snap_veo(needed):
    """نزدیک‌ترین گام Veo که نیاز را پوشش دهد (وگرنه 8 + هشدار شکست شات)."""
    for s in VEO_STEPS:
        if needed <= s:
            return s
    SOFT_ERRORS.append(f"a video shot needs {needed:.1f}s > 8s — split it into two shots")
    return 8.0


def build_veo_prompt(shot, sp):
    v = shot.get("visual", {})
    style = v.get("style_ambiance") or sp.get("style", {}).get("style_prompt", "")
    palette = sp.get("style", {}).get("palette", "")
    parts = [
        f"[Cinematography]: {v.get('cinematography','')}",
        f"[Subject]: {v.get('subject','')}",
        f"[Action]: {v.get('action','')}",
        f"[Context]: {v.get('context','')}",
        f"[Style & Ambiance]: {style}" + (f" — palette: {palette}" if palette else ""),
    ]
    # Identity anchoring — attributes verbatim
    for ch in sp.get("characters", []):
        if ch["id"].lower() in (v.get("subject", "") + " " + v.get("action", "")).lower():
            if ch["attributes"].lower() not in v.get("subject", "").lower():
                SOFT_ERRORS.append(
                    f"{shot['id']}: character '{ch['id']}' referenced but attributes "
                    f"not verbatim in subject — add: {ch['attributes']}")
    # Audio direction
    audio_bits = []
    if shot.get("sfx"):
        audio_bits.append(f"SFX: {shot['sfx']}")
    if shot.get("ambient"):
        audio_bits.append(f"Ambient noise: {shot['ambient']}")
    if shot.get("dialogue"):
        audio_bits.append(f"Dialogue: {shot['dialogue']}")
    if audio_bits:
        parts.append("[Audio]: " + " | ".join(audio_bits))
    return "\n".join(p for p in parts if p.strip() and not p.endswith(": "))


def build_nb_prompt(shot, sp):
    v = shot.get("visual", {})
    kf = shot.get("keyframe", {}) or {}
    style = sp.get("style", {}).get("style_prompt", "")
    extra = kf.get("extra", "")
    parts = [
        f"[Subject]: {v.get('subject','')}",
        f"[Action]: {v.get('action','')}",
        f"[Location/context]: {v.get('context','')}",
        f"[Composition]: {kf.get('composition','')}",
        f"[Style]: {style}" + (f" {extra}" if extra else ""),
    ]
    return "\n".join(p for p in parts if p.strip() and not p.endswith(": "))


def build_nb_endframe(shot, sp):
    flf = shot.get("first_last_frame") or {}
    end_beat = flf.get("end_beat", "")
    if not end_beat:
        return None, None
    v = shot.get("visual", {})
    kf = shot.get("keyframe", {}) or {}
    style = sp.get("style", {}).get("style_prompt", "")
    start = (f"[Subject]: {v.get('subject','')}\n[Action]: {v.get('action','')}\n"
             f"[Location/context]: {v.get('context','')}\n"
             f"[Composition]: {kf.get('composition','')} — FIRST FRAME\n[Style]: {style}")
    end = (f"[Subject]: {v.get('subject','')}\n[Action]: {end_beat}\n"
           f"[Location/context]: {v.get('context','')}\n"
           f"[Composition]: {kf.get('composition','')} — LAST FRAME, "
           f"complementary POV to the first\n[Style]: {style}")
    return start, end


def omni_note(shot):
    flf = shot.get("first_last_frame") or {}
    notes = []
    if flf.get("omni_fix"):
        notes.append(f"{flf['omni_fix']} Keep everything else the same.")
    if shot.get("source") == "video" and shot.get("keep_clip_audio") == "mute":
        notes.append("Remove all audio. Keep everything else the same.")
    return notes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project_dir")
    args = ap.parse_args()
    proj = os.path.abspath(args.project_dir)

    sp_path = os.path.join(proj, "artifacts", "screenplay.json")
    if not os.path.isfile(sp_path):
        sp_path = os.path.join(proj, "screenplay.json")
    if not os.path.isfile(sp_path):
        sys.exit(f"✗ screenplay.json not found under {proj}")
    with open(sp_path, encoding="utf-8") as f:
        sp = json.load(f)

    pkg = os.path.join(proj, "production_package")
    os.makedirs(pkg, exist_ok=True)
    mode = sp.get("mode", "google-suite")
    wpm = sp.get("audio", {}).get("narration_wpm", 140)
    chars = sp.get("characters", [])
    shots = sp.get("shots", [])

    # ── تایم‌لاین ─────────────────────────────────────────────
    items, t_cursor = [], 0.0
    for i, shot in enumerate(shots):
        narr = shot.get("narration", "")
        narr_dur = wpm_dur(narr, wpm) if narr else 0.0
        if shot.get("source") == "video":
            needed = LEAD + narr_dur + TAIL + shot.get("silence_after", 0.0)
            dur = snap_veo(needed) if mode != "in-house" else needed
            if narr_dur and needed > dur:
                SOFT_ERRORS.append(
                    f"{shot['id']}: narration {narr_dur:.1f}s doesn't fit {dur:.0f}s clip "
                    f"(need {needed:.1f}s) — trim narration or split shot")
        else:
            dur = LEAD + narr_dur + TAIL + shot.get("silence_after", 0.0)
        start = 0.0 if i == 0 else t_cursor
        t_cursor = start + dur - (FADE if i < len(shots) - 1 else 0.0)
        items.append({
            "id": shot["id"],
            "type": shot.get("source", "image"),
            "src": (f"assets/clips/{shot['id']}.mp4" if shot.get("source") == "video"
                    else f"assets/images/{shot['id']}.png"),
            "narration_src": f"assets/voice/{shot['id']}.wav" if narr else None,
            "duration": round(dur, 2),
            "start": round(start, 2),
            "motion": shot.get("motion", "zoom-in"),
            "keep_clip_audio": shot.get("keep_clip_audio", "duck"),
            "transition_out": shot.get("transition_out",
                                       "crossfade" if i < len(shots) - 1 else "fade-black"),
            "subtitle": shot.get("subtitle", ""),
            "subtitle_dur": round(max(1.2, narr_dur), 2),
            "silence_after": shot.get("silence_after", 0.0),
            "title_overlay": bool(shot.get("title_overlay")),
        })
    total_body = t_cursor
    credits_start = t_cursor
    total = credits_start + CREDITS_DUR

    timeline = {
        "project": sp.get("project", os.path.basename(proj)),
        "title": sp.get("title", "UNTITLED"),
        "title_fa": sp.get("title_fa", ""),
        "mode": mode,
        "fps": sp.get("target", {}).get("fps", 30),
        "resolution": sp.get("target", {}).get("resolution", "1080p"),
        "aspect": sp.get("target", {}).get("aspect", "16:9"),
        "lead": LEAD, "tail": TAIL, "fade": FADE,
        "items": items,
        "credits": sp.get("credits", []),
        "credits_start": round(credits_start, 2),
        "total": round(total, 2),
        "music": sp.get("audio", {}).get("music", {}),
    }
    with open(os.path.join(pkg, "timeline.json"), "w", encoding="utf-8") as f:
        json.dump(timeline, f, ensure_ascii=False, indent=2)

    # ── 00_README.md ─────────────────────────────────────────
    readme = f"""# 🎬 پکیج تولید — {sp.get('title')} ({sp.get('title_fa','')})

**Mode:** {mode} | **Pipeline:** {sp.get('pipeline','documentary')} |
**هدف:** ~{sp.get('target',{}).get('duration_s',90)}s، {sp.get('target',{}).get('aspect','16:9')} |
**مدت پلان‌شده:** {total:.0f}s (بدنه {total_body:.0f}s + تیتراژ {CREDITS_DUR:.0f}s)

## ترتیب اجرا (در ابزارهای خودت)

1. **شیت‌های شخصیت** → `01_character_sheets.md` — هر پرامپت را در Nano Banana اجرا کن؛
   خروجی را در `assets/images/char_<id>.png` ذخیره کن (Ingredient).
2. **کی‌فریم هر شات** → `02_shot_prompts.md` بخش NB — خروجی در
   `assets/images/<SHOT_ID>.png` (در صورت داشتن فریم آخر: `assets/images/<SHOT_ID>_end.png`).
3. **شات‌های متحرک** → همان فایل، بخش Veo — در Flow/Veo با «Frames to Video» (کی‌فریم
   = فریم اول) یا «Ingredients to Video» (شخصیت‌ها) اجرا کن؛ خروجی در
   `assets/clips/<SHOT_ID>.mp4`.
4. **ویرایش جراحی (اختیاری)** → همان فایل، بخش Omni — جمله‌های کوتاه +
   «Keep everything else the same.»
5. **روایت** → `03_audio_plan.md` را به TTS دلخواه بده (یا از من بخواه)؛
   فایل‌ها در `assets/voice/<SHOT_ID>.wav`.
6. **موسیقی** → طبق پلان؛ در `assets/music/track.wav`.
7. **بازگشت به من** → بگو «دارایی‌ها آماده‌ست» تا `assemble.py` را اجرا کنم:
   `python3 <skill>/scripts/assemble.py {proj}`

## یادآوری consistency
- بلاک Style در همهٔ پرامپت‌ها ثابت است — تغییرش نکن.
- ویژگی‌های شخصیت verbatim تکرار می‌شوند — paraphrase نکن.
- اگر شاتی جواب نداد: اول دوربین را ساده کن، بعد اکشن، بعد سبک.
"""
    with open(os.path.join(pkg, "00_README.md"), "w", encoding="utf-8") as f:
        f.write(readme)

    # ── 01_character_sheets.md ───────────────────────────────
    if chars:
        lines = [f"# شیت‌های شخصیت (Nano Banana Ingredients)\n"]
        lines.append("هر پرامپت را جدا اجرا کن؛ خروجی = `assets/images/char_<id>.png`\n")
        lines.append("سپس در Flow به‌عنوان Ingredient اضافه کن (حداکثر ۳ در هر پرامپت).\n")
        for ch in chars:
            lines.append(f"\n## {ch['id']} — {ch.get('name','')}\n")
            lines.append(f"**Attributes (verbatim در همهٔ شات‌ها):**\n> {ch['attributes']}\n")
            lines.append(f"**پرامپت شیت:**\n```\n{ch['sheet_prompt']}\n```\n")
        with open(os.path.join(pkg, "01_character_sheets.md"), "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

    # ── 02_shot_prompts.md ───────────────────────────────────
    lines = ["# پرامپت‌های شات (به‌ترتیب)\n"]
    for shot in shots:
        sid = shot["id"]
        lines.append(f"\n---\n\n## {sid} — {shot.get('act','')} · {shot.get('beat','')}\n")
        lines.append(f"**Source:** {shot.get('source','image')} · "
                     f"**Duration:** {[i for i in items if i['id']==sid][0]['duration']}s · "
                     f"**Transition out:** {shot.get('transition_out','crossfade')}\n")
        if shot.get("source") == "video":
            lines.append(f"\n### 🎥 Veo 3.1 prompt (Flow: Frames-to-Video با کی‌فریم)\n```text\n{build_veo_prompt(shot, sp)}\n```")
        flf_start, flf_end = build_nb_endframe(shot, sp)
        if flf_start:
            lines.append(f"\n### 🔁 First & Last Frame (دو کی‌فریم + گذار)\n")
            lines.append(f"**NB — FIRST FRAME**\n```text\n{flf_start}\n```")
            lines.append(f"\n**NB — LAST FRAME**\n```text\n{flf_end}\n```")
            lines.append(f"\n**Veo — انتقال:**\n```text\n{build_veo_prompt(shot, sp)}\n(the camera transitions smoothly from the FIRST FRAME composition to the LAST FRAME composition)\n```")
        else:
            lines.append(f"\n### 🖼 Nano Banana keyframe\n```text\n{build_nb_prompt(shot, sp)}\n```")
        on = omni_note(shot)
        if on:
            lines.append("\n### ✂️ Omni Flash edits (جراحی، لایه‌لایه)\n")
            for n_ in on:
                lines.append(f"- `{n_}`")
    with open(os.path.join(pkg, "02_shot_prompts.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    # ── 03_audio_plan.md ─────────────────────────────────────
    aud = sp.get("audio", {})
    mus = aud.get("music", {})
    lines = ["# پلان صدا\n", f"- WPM: {wpm} | Voice: {aud.get('voice','—')} | Speed: {aud.get('speed',1)}\n"]
    lines.append(f"- موسیقی: {mus.get('plan','none')} | mood: {mus.get('mood','—')} | "
                 f"volume: {mus.get('volume_db',-23)}dB\n")
    lines.append("\n## متن روایت (per shot — خروجی: assets/voice/<SHOT_ID>.wav)\n")
    for shot in shots:
        if shot.get("narration"):
            lines.append(f"\n**{shot['id']}**\n> {shot['narration']}\n")
            if shot.get("subtitle"):
                lines.append(f"*زیرنویس:* {shot['subtitle']}\n")
    with open(os.path.join(pkg, "03_audio_plan.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    # ── گزارش ────────────────────────────────────────────────
    print(f"✓ package → {pkg}")
    print(f"  shots: {len(items)} | body: {total_body:.1f}s | credits: {CREDITS_DUR}s | total: {total:.1f}s")
    for i in items:
        print(f"   {i['id']:>5} {i['type']:>5} {i['duration']:>5.1f}s  → {i['src']}")
    if SOFT_ERRORS:
        print("\n⚠ FIX BEFORE GENERATION:")
        for e in SOFT_ERRORS:
            print(f"   - {e}")
    return 0 if not SOFT_ERRORS else 1


if __name__ == "__main__":
    sys.exit(main())
