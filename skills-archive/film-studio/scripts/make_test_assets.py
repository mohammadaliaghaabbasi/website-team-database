#!/usr/bin/env python3
"""make_test_assets.py — دارایی‌های تستی برای demo-test (کلیپ ویدیویی + تصاویر + صدا)"""
import os
import subprocess
import sys

PROJ = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else
                       "examples/demo-test")


def run(cmd, desc):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(f"FAIL {desc}: {r.stderr[-500:]}")
    print(f"  ✓ {desc}")


def main():
    a = os.path.join(PROJ, "assets")
    for d in ["clips", "images", "voice", "music"]:
        os.makedirs(os.path.join(a, d), exist_ok=True)

    # ۱) کلیپ ویدیویی ۸ ثانیه‌ای با صدای محیطی (شبیه‌سازی خروجی Veo)
    run(["ffmpeg", "-y", "-loglevel", "error",
         "-f", "lavfi", "-t", "8",
         "-i", "testsrc2=size=1280x720:rate=30",
         "-f", "lavfi", "-t", "8",
         "-i", "sine=frequency=220:sample_rate=48000",
         "-c:v", "libx264", "-preset", "fast", "-crf", "20",
         "-c:a", "aac", "-b:a", "128k", "-shortest",
         os.path.join(a, "clips", "S01.mp4")], "clip S01.mp4 (8s video+audio)")

    # ۲) تصاویر کی‌فریم (گرادیان گرم)
    from PIL import Image
    for sid, hue in [("S02", (34, 139, 87)), ("S03", (12, 75, 120))]:
        img = Image.new("RGB", (1344, 768))
        px = img.load()
        for y in range(768):
            for x in range(0, 1344, 2):
                t = (x / 1344 + y / 768) / 2
                px[x, y] = tuple(int(c + (255 - c) * t) for c in hue)
                if x + 1 < 1344:
                    px[x + 1, y] = px[x, y]
        img.save(os.path.join(a, "images", f"{sid}.png"))
        print(f"  ✓ image {sid}.png")

    # ۳) روایت‌های تستی (لحن سینتی کوتاه)
    for sid, f, dur in [("S01", 300, 4.2), ("S02", 330, 4.4), ("S03", 360, 3.4)]:
        run(["ffmpeg", "-y", "-loglevel", "error",
             "-f", "lavfi", "-t", f"{dur}",
             "-i", f"sine=frequency={f}:sample_rate=48000",
             "-af", "volume=0.8",
             os.path.join(a, "voice", f"{sid}.wav")], f"voice {sid}.wav ({dur}s)")

    # ۴) موسیقی بستر
    run(["ffmpeg", "-y", "-loglevel", "error",
         "-f", "lavfi", "-t", "40",
         "-i", "sine=frequency=110:sample_rate=48000",
         "-af", "tremolo=f=0.12:d=0.3,volume=0.5,lowpass=f=800",
         os.path.join(a, "music", "track.wav")], "music track.wav (40s)")

    print("ALL TEST ASSETS READY")


if __name__ == "__main__":
    main()
