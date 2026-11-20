#!/usr/bin/env python3
"""assemble.py — موتور تدوین استودیو (timeline-driven)

ورودی: production_package/timeline.json + دارایی‌ها در assets/
خروجی: output/final.mp4 (H.264/AAC، زیرنویس ASS چسبیده، عنوان، تیتراژ)

پشتیبانی:
  - items نوع video (کلیپ Veo/Omni با صدای خودش: keep/duck/mute) و image (Ken Burns)
  - گذارها: crossfade | cut | fade-black (xfade)
  - روایت per-shot (adelay) + موسیقی بستر (volume_db + fade) + میکس
  - زیرنویس RTL فارسی (Vazirmatn) + اورلی عنوان + پلیت تیتراژ (PIL)
  - 16:9 و 9:16، 720p/1080p

Usage: python3 assemble.py <project-dir> [--timeline path] [--keep-work]
"""
import argparse
import json
import os
import subprocess
import sys

try:
    from PIL import Image, ImageDraw, ImageFont, features as PIL_features
    PIL_OK = True
except ImportError:
    PIL_OK = False

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VP_FONTS = os.path.join(SKILL_DIR, "..", "video-producer", "assets", "fonts")
FONT_DIRS = [os.path.abspath(VP_FONTS),
             "/usr/share/fonts/truetype/chinese",
             "/usr/share/fonts"]

FADE_DEFAULT = 0.8
CREDITS_DUR = 10.0


def find_font(name):
    for d in FONT_DIRS:
        p = os.path.join(d, name)
        if os.path.exists(p):
            return p
    return name  # امید به system fontconfig


def run(cmd, desc=""):
    # -nostdin: جلوگیری از حالت تعاملی ffmpeg (علت هنگ در محیط اسکریپت)
    if cmd and cmd[0] == "ffmpeg" and "-nostdin" not in cmd:
        cmd = ["ffmpeg", "-nostdin"] + cmd[1:]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"ffmpeg failed ({desc}):\n{r.stderr[-900:]}")
    return r


def probe(path):
    """{duration, has_audio, w, h}"""
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries",
         "format=duration:stream=codec_type,width,height",
         "-of", "json", path], capture_output=True, text=True)
    d = json.loads(r.stdout or "{}")
    streams = d.get("streams", [])
    return {
        "duration": float(d.get("format", {}).get("duration", 0) or 0),
        "has_audio": any(s.get("codec_type") == "audio" for s in streams),
        "w": next((s.get("width") for s in streams if s.get("width")), 0),
        "h": next((s.get("height") for s in streams if s.get("height")), 0),
    }


def ass_time(t):
    t = max(0.0, t)
    h, m, s = int(t // 3600), int((t % 3600) // 60), t % 60
    return f"{h}:{m:02d}:{s:05.2f}"


def fade_for(transition):
    return {"crossfade": FADE_DEFAULT, "fade-black": FADE_DEFAULT, "cut": 0.05}.get(
        transition, FADE_DEFAULT)


# ── نرمال‌سازی هر آیتم به کلیپ استاندارد W×H/FPS با صدای همیشه‌موجود ──
def normalize_video(src, out, W, H, FPS, dur, audio_mode):
    p = probe(src)
    vf = [f"scale={W}:{H}:force_original_aspect_ratio=increase",
          f"crop={W}:{H}", f"fps={FPS}", "format=yuv420p"]
    real = p["duration"]
    if real + 0.05 < dur:  # کلیپ کوتاه‌تر از پلان → فریم آخر را نگه دار
        vf.append(f"tpad=stop_mode=clone:stop_duration={dur - real:.3f}")
    inputs = ["-i", src]
    if p["has_audio"] and audio_mode != "mute":
        vol = 1.0 if audio_mode == "keep" else 0.25
        af = [f"aresample=48000", f"volume={vol}"]
        if real + 0.05 < dur:
            af.append(f"apad=whole_dur={dur:.3f}")
        cmd = ["ffmpeg", "-y", "-loglevel", "error"] + inputs + [
            "-vf", ",".join(vf), "-af", ",".join(af), "-t", f"{dur:.3f}",
            "-c:v", "libx264", "-preset", "fast", "-crf", "18",
            "-c:a", "aac", "-b:a", "160k", out]
    else:  # بدون صدا یا mute → صدای سکوت
        cmd = ["ffmpeg", "-y", "-loglevel", "error"] + inputs + [
            "-f", "lavfi", "-t", f"{dur:.3f}", "-i", "anullsrc=r=48000:cl=stereo",
            "-vf", ",".join(vf), "-t", f"{dur:.3f}",
            "-map", "0:v:0", "-map", "1:a:0",
            "-c:v", "libx264", "-preset", "fast", "-crf", "18",
            "-c:a", "aac", "-b:a", "160k", "-shortest", out]
    run(cmd, desc=f"normalize {os.path.basename(out)}")


def ken_burns(src_img, out, W, H, FPS, dur, motion):
    frames = max(2, round(dur * FPS))
    SW, SH = W * 2, H * 2  # فضای بزرگ برای کیفیت زوم
    maxz = 1.22
    if motion == "zoom-in":
        z = f"min(1+{(maxz - 1) / (frames - 1):.6f}*on,{maxz})"
        x, y = "iw/2-(iw/zoom/2)", "ih/2-(ih/zoom/2)"
    elif motion == "zoom-out":
        z = f"max({maxz}-{(maxz - 1) / (frames - 1):.6f}*on,1.0)"
        x, y = "iw/2-(iw/zoom/2)", "ih/2-(ih/zoom/2)"
    elif motion == "pan-right":
        z, x, y = "1.15", f"(iw-iw/zoom)*on/{frames - 1}", "ih/2-(ih/zoom/2)"
    else:  # pan-left
        z, x, y = "1.15", f"(iw-iw/zoom)*(1-on/{frames - 1})", "ih/2-(ih/zoom/2)"
    vf = (f"scale={SW}:{SH}:force_original_aspect_ratio=increase,crop={SW}:{SH},"
          f"zoompan=z='{z}':d={frames}:x='{x}':y='{y}':s={W}x{H}:fps={FPS},"
          f"format=yuv420p")
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", src_img,
           "-f", "lavfi", "-t", f"{dur:.3f}", "-i", "anullsrc=r=48000:cl=stereo",
           "-vf", vf, "-frames:v", str(frames),
           "-map", "0:v:0", "-map", "1:a:0",
           "-c:v", "libx264", "-preset", "fast", "-crf", "18",
           "-c:a", "aac", "-b:a", "160k", "-shortest", out]
    run(cmd, desc=f"kenburns {os.path.basename(out)}")


# ── پلیت تیتراژ ──────────────────────────────────────────────
def shape_fa(text):
    if PIL_OK and PIL_features.check("raqm"):
        return text, True
    try:
        import arabic_reshaper
        from bidi.algorithm import get_display
        return get_display(arabic_reshaper.reshape(text)), False
    except ImportError:
        return text, False


def draw_center(d, y, text, font, fill, spacing=0, cw=1920):
    if spacing:
        text = " ".join(list(text))
    b = d.textbbox((0, 0), text, font=font)
    d.text(((cw - (b[2] - b[0])) / 2 - b[0], y), text, font=font, fill=fill)


def make_credits_plate(tl, proj, out_png, W, H):
    bg_src = None
    last_img_dir = os.path.join(proj, "assets", "images")
    if os.path.isdir(last_img_dir):
        cands = sorted(f for f in os.listdir(last_img_dir) if f.endswith(".png"))
        if cands:
            bg_src = os.path.join(last_img_dir, cands[-1])
    img = Image.new("RGB", (W, int(W * 9 / 16)) if H > W else (W, H), (9, 12, 18))
    if bg_src and PIL_OK:
        try:
            bg = Image.open(bg_src).convert("RGB").resize(img.size)
            from PIL import ImageEnhance
            img = ImageEnhance.Brightness(bg).enhance(0.32)
        except Exception:
            pass
    d = ImageDraw.Draw(img)
    CW = img.size[0]
    f_title = ImageFont.truetype(
        "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
        max(44, CW // 26))
    f_fa = ImageFont.truetype(find_font("Vazirmatn-Bold.ttf"), max(28, CW // 42))
    f_role = ImageFont.truetype(
        "/usr/share/fonts/truetype/english/Carlito-Regular.ttf", max(20, CW // 70))
    f_name = ImageFont.truetype(
        "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
        max(26, CW // 52))
    y0 = int(img.size[1] * 0.17)
    draw_center(d, y0, tl.get("title", "UNTITLED"), f_title, (243, 238, 227), spacing=1, cw=CW)
    fa, has_raqm = shape_fa(tl.get("title_fa", ""))
    if fa:
        b = d.textbbox((0, 0), fa, font=f_fa)
        d.text(((CW - (b[2] - b[0])) / 2 - b[0], y0 + int(img.size[1] * 0.075)), fa,
               font=f_fa, fill=(168, 168, 175),
               direction="rtl" if has_raqm else None)
    d.rectangle([CW * 0.31, y0 + int(img.size[1] * 0.16),
                 CW * 0.69, y0 + int(img.size[1] * 0.162)], fill=(172, 141, 86))
    y = y0 + int(img.size[1] * 0.22)
    for c in tl.get("credits", []):
        draw_center(d, y, c["role"], f_role, (140, 140, 148), spacing=1, cw=CW)
        draw_center(d, y + int(img.size[1] * 0.035), c["name"], f_name, (235, 232, 225), cw=CW)
        y += int(img.size[1] * 0.09)
    img.save(out_png, quality=92)


# ── زیرنویس ASS ──────────────────────────────────────────────
def build_ass(tl, starts, durs, W, H, out_path, fa_font):
    header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: SubFA,{fa_font},{max(34, H // 26)},&H00FFFFFF,&H000000FF,&H50140D0A,&H64000000,0,0,0,0,100,100,0,0,3,2,6,2,90,90,{H // 16},1
Style: TitleEN,Liberation Serif,{max(54, H // 17)},&H00E6F0F5,&H000000FF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,0,0,5,0,0,0,1
Style: TitleFA,{fa_font},{max(38, H // 24)},&H00E6F0F5,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,5,0,0,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    lines = []
    LEAD = tl.get("lead", 0.6)
    # عنوان روی آیتم اول
    if tl.get("items") and tl["items"][0].get("title_overlay"):
        t_end = min(6.5, durs[0] * 0.75)
        lines.append(f"Dialogue: 0,{ass_time(1.0)},{ass_time(t_end)},TitleEN,,0,0,0,,"
                     f"{{\\an5\\pos({W // 2},{H // 2 - 60})\\fad(500,600)\\fsp7}}"
                     f"{tl.get('title', '').upper()}")
        if tl.get("title_fa"):
            lines.append(f"Dialogue: 0,{ass_time(1.0)},{ass_time(t_end)},TitleFA,,0,0,0,,"
                         f"{{\\an5\\pos({W // 2},{H // 2 + 18})\\fad(500,600)}}{tl['title_fa']}")
    for i, it in enumerate(tl["items"]):
        s = starts[i] + LEAD
        e = s + it.get("subtitle_dur", 1.2)
        sub = (it.get("subtitle") or "").replace("\n", " ").strip()
        if sub:
            lines.append(f"Dialogue: 0,{ass_time(s)},{ass_time(e)},SubFA,,0,0,0,,{sub}")
    with open(out_path, "w", encoding="utf-8-sig") as f:
        f.write(header + "\n".join(lines) + "\n")


# ── اصلی ─────────────────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project_dir")
    ap.add_argument("--timeline")
    ap.add_argument("--keep-work", action="store_true")
    args = ap.parse_args()
    proj = os.path.abspath(args.project_dir)

    tl_path = args.timeline or os.path.join(proj, "production_package", "timeline.json")
    if not os.path.isfile(tl_path):
        sys.exit(f"✗ timeline not found: {tl_path} — run build_package.py first")
    with open(tl_path, encoding="utf-8") as f:
        tl = json.load(f)

    W, H = (1920, 1080) if tl.get("resolution") == "1080p" else (1280, 720)
    if tl.get("aspect") == "9:16":
        W, H = (1080, 1920) if tl.get("resolution") == "1080p" else (720, 1280)
    FPS = tl.get("fps", 30)
    LEAD = tl.get("lead", 0.6)
    items = tl["items"]
    n = len(items)
    if n == 0:
        sys.exit("✗ timeline has no items")

    work = os.path.join(proj, "work")
    os.makedirs(work, exist_ok=True)
    os.makedirs(os.path.join(proj, "output"), exist_ok=True)

    # ۱) نرمال‌سازی همهٔ آیتم‌ها
    clips, missing = [], []
    for it in items:
        src = os.path.join(proj, it["src"])
        out = os.path.join(work, f"{it['id']}.mp4")
        if not os.path.exists(src):
            missing.append(src)
            continue
        clips.append((it, out))
    if missing:
        print("✗ missing assets (put them where shown, then re-run):")
        for m in missing:
            print(f"   - {m}")
        sys.exit(1)

    for it, out in clips:
        if os.path.isfile(out) and abs(probe(out)["duration"] - it["duration"]) < 0.15:
            print(f"✓ cached {it['id']}")
            continue
        if it["type"] == "video":
            normalize_video(os.path.join(proj, it["src"]), out, W, H, FPS,
                            it["duration"], it.get("keep_clip_audio", "duck"))
        else:
            ken_burns(os.path.join(proj, it["src"]), out, W, H, FPS,
                      it["duration"], it.get("motion", "zoom-in"))
        print(f"✓ {it['id']} ({it['duration']:.1f}s, {it['type']})")

    # ۲) تیتراژ
    credits_clip = os.path.join(work, "credits.mp4")
    plate = os.path.join(work, "credits_plate.png")
    if not os.path.isfile(credits_clip):
        if PIL_OK:
            make_credits_plate(tl, proj, plate, W, H)
            ken_burns(plate, credits_clip, W, H, FPS, CREDITS_DUR, "zoom-in")
        else:
            sys.exit("✗ PIL not available for credits plate")
    print(f"✓ credits ({CREDITS_DUR}s)")

    # ۳) تایم‌لاین (با fade واقعی هر گذار)
    starts, durs = [], []
    t = 0.0
    for i, (it, _) in enumerate(clips):
        starts.append(round(t, 3))
        durs.append(it["duration"])
        f = fade_for(it.get("transition_out", "crossfade")) if i < n - 1 else FADE_DEFAULT
        t += it["duration"] - f
    credits_start = t
    total = credits_start + CREDITS_DUR
    # آفست‌های xfade (انباشت cumulative)
    fade_offsets = []
    acc = 0.0
    for i in range(1, n + 1):
        trans = clips[i - 1][0].get("transition_out", "crossfade") if i <= n - 1 else "fade-black"
        f = fade_for(trans)
        acc += durs[i - 1] - f
        fade_offsets.append(round(acc, 3))
    print(f"· timeline: {n} items, credits @ {credits_start:.1f}s, total {total:.1f}s")

    # ۴) ASS
    ass_path = os.path.join(work, "subtitles.ass")
    fa_font = "Vazirmatn"
    build_ass(tl, starts, durs, W, H, ass_path, fa_font)
    print(f"✓ subtitles → {ass_path}")

    # ۵) گراف نهایی
    inputs = []
    for _, out in clips:
        inputs += ["-i", out]
    inputs += ["-i", credits_clip]                       # index n
    narr_idx = {}
    k = n + 1
    for i, (it, _) in enumerate(clips):
        if it.get("narration_src"):
            p = os.path.join(proj, it["narration_src"])
            if os.path.isfile(p):
                inputs += ["-i", p]
                narr_idx[i] = k
                k += 1
            else:
                print(f"⚠ narration missing for {it['id']}: {p} (continuing without)")
    music_path = None
    mus = tl.get("music", {})
    if mus.get("enabled") or mus.get("plan") not in (None, "none"):
        for cand in ["track.wav", "track.mp3", "ambient.wav", "ambient.mp3"]:
            p = os.path.join(proj, "assets", "music", cand)
            if os.path.isfile(p):
                music_path = p
                break
    if music_path:
        inputs += ["-i", music_path]
        music_idx = k
        k += 1

    parts = []
    # ویدیو: زنجیرهٔ xfade (ورودی‌های ویدیویی — هر ورودی فقط یک‌بار مصرف می‌شود)
    prev = "[0:v]"
    for i in range(1, n + 1):
        trans = clips[i - 1][0].get("transition_out", "crossfade") if i <= n - 1 else "fade-black"
        xtrans = {"crossfade": "fade", "fade-black": "fadeblack", "cut": "fade"}[trans]
        f = fade_for(trans)
        lbl = f"[x{i}]" if i < n else "[vcat]"
        parts.append(f"{prev}[{i}:v]xfade=transition={xtrans}:duration={f:.3f}:"
                     f"offset={fade_offsets[i - 1]:.3f}{lbl}")
        prev = lbl
    parts.append(f"[vcat]subtitles=filename='{ass_path}',"
                 f"fade=t=in:st=0:d=1.0,fade=t=out:st={total - 1.3:.2f}:d=1.3[vout]")

    # صدا: صدای هر کلیپ (adelay) + روایت‌ها + موسیقی
    audio_labels = []
    for i, (it, _) in enumerate(clips):
        parts.append(f"[{i}:a]aresample=48000,adelay={int(starts[i] * 1000)}:all=1[ca{i}]")
        audio_labels.append(f"[ca{i}]")
    for i, idx in narr_idx.items():
        parts.append(f"[{idx}:a]aresample=48000,adelay={int((starts[i] + LEAD) * 1000)}:all=1[na{i}]")
        audio_labels.append(f"[na{i}]")
    if music_path:
        vol = 10 ** (mus.get("volume_db", -23) / 20)
        parts.append(f"[{music_idx}:a]aresample=48000,volume={vol:.4f},"
                     f"afade=t=in:d=2,afade=t=out:st={total - 2:.2f}:d=2,"
                     f"atrim=0:{total:.3f}[mus]")
        audio_labels.append("[mus]")
    if audio_labels:
        parts.append("".join(audio_labels) +
                     f"amix=inputs={len(audio_labels)}:duration=longest:normalize=0"
                     f"[amx]")
        parts.append(f"[amx]atrim=0:{total:.3f},alimiter=limit=0.95:level=false[aout]")

    fc = ";".join(parts)
    final = os.path.join(proj, "output", "final.mp4")
    maps = ["-map", "[vout]"]
    if audio_labels:
        maps += ["-map", "[aout]"]
    cmd = (["ffmpeg", "-y", "-loglevel", "error"] + inputs +
           ["-filter_complex", fc] + maps +
           ["-c:v", "libx264", "-preset", "medium", "-crf", "20",
            "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
            "-movflags", "+faststart", "-t", f"{total:.3f}", final])
    run(cmd, desc="final assembly")

    d = probe(final)
    print(f"\n🎬 FINAL: {final} ({d['duration']:.1f}s, "
          f"{os.path.getsize(final) / 1e6:.1f} MB, {W}x{H}@{FPS})")
    if not args.keep_work:
        print("(work files kept for QC; re-run with --keep-work to force keep note)")


if __name__ == "__main__":
    main()
