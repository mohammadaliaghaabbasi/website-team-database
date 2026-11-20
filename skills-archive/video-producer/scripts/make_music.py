#!/usr/bin/env python3
"""make_music.py — فاز ۴: پد آمبیانت هم‌مدت ویدیو با سینتز ffmpeg

ساختار پد: سه موج سینوسی (root + fifth + octave) با detune خفیف،
tremolo آهسته (0.08Hz) و lowpass نرم — حس مستند آرام می‌دهد.
ولوم پیش‌فرض -23dB زیر روایت می‌نشیند.

استفاده: python3 make_music.py <project-dir> [--duration N]
اگر duration ندهد: از مدت روایت‌ها + پدینگ‌ها محاسبه می‌شود (همان منطق assemble.py).
"""
import json
import subprocess
import sys
import os
import glob


def scene_durations(proj):
    """مدت هر صحنه = 0.6 lead + dur(wav) + 0.8 tail — همان فرمول assemble.py"""
    durs = []
    for wav in sorted(glob.glob(os.path.join(proj, 'voice', 'scene_*.wav'))):
        r = subprocess.run(
            ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
             '-of', 'default=noprint_wrappers=1:nokey=1', wav],
            capture_output=True, text=True)
        durs.append(0.6 + float(r.stdout.strip()) + 0.8)
    return durs


def total_duration(proj):
    durs = scene_durations(proj)
    if not durs:
        return 30.0
    n = len(durs)
    fade = 0.8
    # n کراس‌فید: بین صحنه‌ها + فید به تیتراژ (همان فرمول assemble.py)
    return sum(durs) - n * fade + 10.0


def main():
    proj = sys.argv[1] if len(sys.argv) > 1 else ''
    if not proj or not os.path.isfile(os.path.join(proj, 'screenplay.json')):
        print("Usage: python3 make_music.py <project-dir>")
        sys.exit(1)

    with open(os.path.join(proj, 'screenplay.json')) as f:
        sp = json.load(f)
    music = sp.get('music', {})
    if not music.get('enabled', True):
        print("Music disabled in screenplay.")
        sys.exit(0)

    duration = total_duration(proj)
    if '--duration' in sys.argv:
        duration = float(sys.argv[sys.argv.index('--duration') + 1])

    root = music.get('root_hz', 110)
    vol_db = music.get('volume_db', -23)

    os.makedirs(os.path.join(proj, 'music'), exist_ok=True)
    out = os.path.join(proj, 'music', 'ambient.wav')

    fifth = root * 1.5
    octave = root * 2.0
    # detune خفیف برای گرمی
    d1, d2 = root * 1.003, root * 0.997

    fc = (
        f"sine=frequency={d1}:duration={duration},"
        f"volume=0.6[a];"
        f"sine=frequency={d2}:duration={duration},"
        f"volume=0.6[b];"
        f"sine=frequency={fifth}:duration={duration},"
        f"volume=0.35[c];"
        f"sine=frequency={octave}:duration={duration},"
        f"volume=0.22[d];"
        f"[a][b][c][d]amix=inputs=4:duration=longest,"
        f"tremolo=f=0.12:d=0.6,"
        f"lowpass=f=900,"
        f"afade=t=in:st=0:d=3,"
        f"afade=t=out:st={max(0, duration-4)}:d=4,"
        f"volume={vol_db}dB[out]"
    )

    cmd = ['ffmpeg', '-y', '-loglevel', 'error',
           '-filter_complex', fc, '-map', '[out]',
           '-ar', '48000', '-ac', '2', out]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("ffmpeg music failed:", r.stderr[-500:])
        sys.exit(1)

    rr = subprocess.run(
        ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
         '-of', 'default=noprint_wrappers=1:nokey=1', out],
        capture_output=True, text=True)
    print(f"✓ ambient pad ready: {out} ({float(rr.stdout.strip()):.1f}s, root={root}Hz)")


if __name__ == '__main__':
    main()
