#!/usr/bin/env python3
"""assemble.py — فاز ۵: موتور تدوین نهایی (NFP ما)

کارها:
  ۱. ساخت کلیپ Ken Burns از تصویر هر صحنه (zoom-in/out, pan)
  ۲. ساخت پلیت تیتراژ پایانی با PIL (+ شکل‌دهی فارسی)
  ۳. ساخت فایل ASS زیرنویس فارسی + عنوان روی صحنه اول
  ۴. اتصال کلیپ‌ها با کراس‌فید xfade + میکس روایت‌ها و موسیقی
  ۵. انکود نهایی H.264/AAC → output/final.mp4

استفاده: python3 assemble.py <project-dir> [--keep-work]
"""
import json
import os
import subprocess
import sys
import math

try:
    from PIL import Image, ImageDraw, ImageFont, features as PIL_features
    PIL_OK = True
except ImportError:
    PIL_OK = False

# ── ثابت‌های تایم‌لاین (باید با make_music.py همسان بماند) ──────────────
LEAD = 0.6          # فاصله شروع روایت بعد از شروع دیداری صحنه
TAIL = 0.8          # فاصله بعد از پایان روایت تا پایان صحنه
FADE = 0.8          # مدت کراس‌فید بین صحنه‌ها
FPS = 30
W, H = 1280, 720
CREDITS_DUR = 10.0  # مدت نمایش پلیت تیتراژ

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT_DIR = os.path.join(SKILL_DIR, 'assets', 'fonts')


def run(cmd, desc=''):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"ffmpeg failed ({desc}):\n{r.stderr[-800:]}")
    return r


def probe_dur(path):
    r = subprocess.run(
        ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
         '-of', 'default=noprint_wrappers=1:nokey=1', path],
        capture_output=True, text=True)
    return float(r.stdout.strip())


def ass_time(t):
    t = max(0.0, t)
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"


# ── تایم‌لاین ──────────────────────────────────────────────────────────
def compute_timeline(narr_durs):
    """مدت صحنه‌ها، شروع هر صحنه در تایم‌لاین نهایی، آفست فیدها، مدت کل"""
    durs = [LEAD + n + TAIL for n in narr_durs]
    n = len(durs)
    starts = [0.0]
    for i in range(1, n):
        starts.append(sum(durs[:i]) - i * FADE)
    # فید آخر: آخرین صحنه → تیتراژ
    credits_start = sum(durs) - n * FADE
    total = credits_start + CREDITS_DUR
    # آفست فید k (اتصال صحنه k+1؛ برای k=n اتصال به تیتراژ)
    fade_offsets = [sum(durs[:k]) - k * FADE for k in range(1, n + 1)]
    return {
        'durs': durs, 'starts': starts, 'n': n,
        'credits_start': credits_start, 'total': total, 'fade_offsets': fade_offsets,
    }


# ── Ken Burns ──────────────────────────────────────────────────────────
def ken_burns_clip(img_path, out_mp4, dur, motion):
    frames = max(2, round(dur * FPS))
    maxz = 1.22
    if motion == 'zoom-in':
        z = f"min(1+{(maxz - 1) / (frames - 1):.6f}*on,{maxz})"
        x = "iw/2-(iw/zoom/2)"
        y = "ih/2-(ih/zoom/2)"
    elif motion == 'zoom-out':
        z = f"max({maxz}-{(maxz - 1) / (frames - 1):.6f}*on,1.0)"
        x = "iw/2-(iw/zoom/2)"
        y = "ih/2-(ih/zoom/2)"
    elif motion == 'pan-right':
        z = "1.15"
        x = f"(iw-iw/zoom)*on/{frames - 1}"
        y = "ih/2-(ih/zoom/2)"
    else:  # pan-left
        z = "1.15"
        x = f"(iw-iw/zoom)*(1-on/{frames - 1})"
        y = "ih/2-(ih/zoom/2)"

    vf = (
        f"scale=2560:1440:force_original_aspect_ratio=increase,"
        f"crop=2560:1440,"
        f"zoompan=z='{z}':d={frames}:x='{x}':y='{y}':s={W}x{H}:fps={FPS},"
        f"format=yuv420p"
    )
    run(['ffmpeg', '-y', '-loglevel', 'error', '-i', img_path,
         '-vf', vf, '-frames:v', str(frames),
         '-c:v', 'libx264', '-preset', 'fast', '-crf', '18', out_mp4],
        desc=f"kenburns {os.path.basename(out_mp4)}")


# ── شکل‌دهی متن فارسی برای PIL ────────────────────────────────────────
def shape_fa(text):
    """اگر raqm موجود باشد مستقیم، وگرنه arabic_reshaper+bidi"""
    if PIL_OK and PIL_features.check('raqm'):
        return text, True  # با direction='rtl' رسم می‌شود
    try:
        import arabic_reshaper
        from bidi.algorithm import get_display
        return get_display(arabic_reshaper.reshape(text)), False
    except ImportError:
        return text, False


def draw_center(draw, y, text, font, fill, spacing=0, canvas_w=1344):
    """متن وسط‌چین با فاصله‌گذاری حروف اختیاری (برای انگلیسی)"""
    if spacing:
        text = ' '.join(list(text))
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    draw.text(((canvas_w - tw) / 2 - bbox[0], y), text, font=font, fill=fill)


# ── پلیت تیتراژ ───────────────────────────────────────────────────────
def make_credits_plate(sp, proj, out_png):
    img = Image.new('RGB', (1344, 768), (9, 12, 18))
    bg_path = os.path.join(proj, 'images', 'credits_bg.png')
    if os.path.exists(bg_path):
        try:
            bg = Image.open(bg_path).convert('RGB').resize((1344, 768))
            from PIL import ImageEnhance
            img = ImageEnhance.Brightness(bg).enhance(0.32)
        except Exception:
            pass
    d = ImageDraw.Draw(img)

    f_title = ImageFont.truetype('/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf', 64)
    f_fa = ImageFont.truetype(os.path.join(FONT_DIR, 'Vazirmatn-Bold.ttf'), 42)
    f_role = ImageFont.truetype('/usr/share/fonts/truetype/english/Carlito-Regular.ttf', 25)
    f_name = ImageFont.truetype('/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf', 34)

    # عنوان انگلیسی + فارسی
    draw_center(d, 130, sp.get('title', 'UNTITLED'), f_title, (243, 238, 227), spacing=1)
    fa, has_raqm = shape_fa(sp.get('title_fa', ''))
    if fa:
        bbox = d.textbbox((0, 0), fa, font=f_fa)
        d.text(((1344 - (bbox[2] - bbox[0])) / 2 - bbox[0], 215), fa,
               font=f_fa, fill=(168, 168, 175),
               direction='rtl' if has_raqm else None)

    # خط جداکننده طلایی
    d.rectangle([422, 300, 922, 302], fill=(172, 141, 86))

    # آیتم‌های تیتراژ
    y = 360
    for c in sp.get('credits', []):
        draw_center(d, y, c['role'], f_role, (140, 140, 148), spacing=1)
        draw_center(d, y + 30, c['name'], f_name, (235, 232, 225))
        y += 78

    img.save(out_png, quality=92)


# ── زیرنویس ASS ───────────────────────────────────────────────────────
def build_ass(sp, tl, narr_durs, out_path):
    header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: SubFA,Vazirmatn,37,&H00FFFFFF,&H000000FF,&H50140D0A,&H64000000,0,0,0,0,100,100,0,0,3,2,6,2,90,90,44,1
Style: TitleEN,Liberation Serif,58,&H00E6F0F5,&H000000FF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,0,0,5,0,0,0,1
Style: TitleFA,Vazirmatn,40,&H00E6F0F5,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,5,0,0,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    lines = []

    # عنوان روی صحنه اول
    if sp.get('scenes') and sp['scenes'][0].get('title_overlay'):
        t_end = min(6.5, tl['durs'][0] * 0.75)
        title = sp.get('title', '').upper()
        lines.append(
            f"Dialogue: 0,{ass_time(1.0)},{ass_time(t_end)},TitleEN,,0,0,0,,"
            f"{{\\an5\\pos({W // 2},{H // 2 - 60})\\fad(500,600)\\fsp7}}{title}")
        fa = sp.get('title_fa', '')
        if fa:
            lines.append(
                f"Dialogue: 0,{ass_time(1.0)},{ass_time(t_end)},TitleFA,,0,0,0,,"
                f"{{\\an5\\pos({W // 2},{H // 2 + 18})\\fad(500,600)}}{fa}")

    # زیرنویس فارسی هر صحنه
    for i, sc in enumerate(sp['scenes']):
        s = tl['starts'][i] + LEAD
        e = s + max(1.2, narr_durs[i])
        sub = sc.get('subtitle', '').replace('\n', ' ').strip()
        if sub:
            lines.append(f"Dialogue: 0,{ass_time(s)},{ass_time(e)},SubFA,,0,0,0,,{sub}")

    with open(out_path, 'w', encoding='utf-8-sig') as f:
        f.write(header + '\n'.join(lines) + '\n')


# ── تدوین نهایی ───────────────────────────────────────────────────────
def main():
    proj = sys.argv[1] if len(sys.argv) > 1 else ''
    if not proj or not os.path.isfile(os.path.join(proj, 'screenplay.json')):
        print("Usage: python3 assemble.py <project-dir>")
        sys.exit(1)
    proj = os.path.abspath(proj)

    with open(os.path.join(proj, 'screenplay.json')) as f:
        sp = json.load(f)

    work = os.path.join(proj, 'work')
    os.makedirs(work, exist_ok=True)
    os.makedirs(os.path.join(proj, 'output'), exist_ok=True)

    scenes = sp['scenes']
    n = len(scenes)

    # ۱) مدت روایت‌ها
    narr_durs, narr_files = [], []
    for i in range(1, n + 1):
        wav = os.path.join(proj, 'voice', f'scene_{i:02d}.wav')
        if not os.path.isfile(wav):
            raise SystemExit(f"✗ missing {wav} — run generate_voice.sh first")
        narr_durs.append(probe_dur(wav))
        narr_files.append(wav)

    tl = compute_timeline(narr_durs)
    print(f"· timeline: {n} scenes, credits @ {tl['credits_start']:.1f}s, "
          f"total {tl['total']:.1f}s")

    # ۲) کلیپ‌های صحنه (Ken Burns)
    scene_clips = []
    for i, sc in enumerate(scenes, 1):
        clip = os.path.join(work, f'scene_{i:02d}.mp4')
        img = os.path.join(proj, 'images', f'scene_{i:02d}.png')
        if not os.path.isfile(img):
            raise SystemExit(f"✗ missing {img} — run generate_images.sh first")
        if os.path.isfile(clip) and abs(probe_dur(clip) - tl['durs'][i - 1]) < 0.15:
            print(f"✓ cached clip {i}")
        else:
            ken_burns_clip(img, clip, tl['durs'][i - 1], sc.get('motion', 'zoom-in'))
            print(f"✓ clip {i}/{n} ({tl['durs'][i - 1]:.1f}s, {sc.get('motion', 'zoom-in')})")
        scene_clips.append(clip)

    # ۳) پلیت + کلیپ تیتراژ
    credits_clip = os.path.join(work, 'credits.mp4')
    plate = os.path.join(work, 'credits_plate.png')
    make_credits_plate(sp, proj, plate)
    ken_burns_clip(plate, credits_clip, CREDITS_DUR, 'zoom-in')
    print(f"✓ credits clip ({CREDITS_DUR}s)")

    # ۴) زیرنویس ASS
    ass_path = os.path.join(work, 'subtitles.ass')
    build_ass(sp, tl, narr_durs, ass_path)
    print(f"✓ subtitles: {ass_path}")

    # ۵) گراف فیلتر بزرگ
    inputs = []
    for c in scene_clips:
        inputs += ['-i', c]
    inputs += ['-i', credits_clip]           # input index n
    for w in narr_files:
        inputs += ['-i', w]                  # indices n+1 .. 2n
    music_path = os.path.join(proj, 'music', 'ambient.wav')
    has_music = os.path.isfile(music_path)
    if has_music:
        inputs += ['-i', music_path]          # index 2n+1
    music_idx = 2 * n + 1

    parts = []
    # زنجیره xfade ویدیو
    prev = '[0]'
    for k in range(1, n + 1):
        outlbl = f'[x{k}]' if k < n else '[vcat]'
        parts.append(
            f"{prev}[{k}]xfade=transition=fade:duration={FADE}:"
            f"offset={tl['fade_offsets'][k - 1]:.3f}{outlbl}")
        prev = outlbl
    total = tl['total']
    parts.append(
        f"[vcat]subtitles=filename='{ass_path}',"
        f"fade=t=in:st=0:d=1.0,fade=t=out:st={total - 1.3:.2f}:d=1.3[vout]")

    # زنجیره صدا: adelay هر روایت → amix → + موسیقی
    for i in range(n):
        t_ms = int(round((tl['starts'][i] + LEAD) * 1000))
        parts.append(
            f"[{n + 1 + i}]aresample=48000,adelay={t_ms}:all=1[a{i}]")
    amix_in = ''.join(f'[a{i}]' for i in range(n))
    if has_music:
        parts.append(f"{amix_in}amix=inputs={n}:duration=longest:normalize=0[nm]")
        parts.append(
            f"[nm][{music_idx}]amix=inputs=2:duration=longest:normalize=0[mx]")
        parts.append(f"[mx]atrim=0:{total:.3f}[aout]")
    else:
        parts.append(f"{amix_in}amix=inputs={n}:duration=longest:normalize=0[nm]")
        parts.append(f"[nm]atrim=0:{total:.3f}[aout]")

    fc = ';'.join(parts)

    final = os.path.join(proj, 'output', 'final.mp4')
    cmd = (['ffmpeg', '-y', '-loglevel', 'error', '-stats'] + inputs +
           ['-filter_complex', fc,
            '-map', '[vout]', '-map', '[aout]',
            '-c:v', 'libx264', '-preset', 'medium', '-crf', '20',
            '-pix_fmt', 'yuv420p',
            '-c:a', 'aac', '-b:a', '160k',
            '-movflags', '+faststart',
            '-t', f'{total:.3f}', final])
    run(cmd, desc='final assembly')
    print(f"\n🎬 FINAL: {final} ({probe_dur(final):.1f}s, {os.path.getsize(final) / 1e6:.1f} MB)")


if __name__ == '__main__':
    main()
