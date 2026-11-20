#!/bin/bash
# generate_voice.sh — فاز ۳: روایت انگلیسی هر صحنه با TTS
# استفاده: bash generate_voice.sh <project-dir>
# idempotent: فایل موجود را دوباره نمی‌سازد
set -u

PROJ="${1:-}"
if [ -z "$PROJ" ] || [ ! -f "$PROJ/screenplay.json" ]; then
  echo "Usage: bash generate_voice.sh <project-dir-with-screenplay.json>"
  exit 1
fi

cd "$PROJ"
mkdir -p voice

python3 - << 'EOF'
import json, subprocess, os, sys, time

with open('screenplay.json') as f:
    sp = json.load(f)

voice = sp.get('voice', 'jam')
speed = sp.get('speed', 0.95)

failed = []
for i, sc in enumerate(sp['scenes'], 1):
    text = sc['narration'].strip()
    out = f'voice/scene_{i:02d}.wav'
    if len(text) > 900:
        print(f"✗ scene {i}: narration longer than 900 chars ({len(text)}) — shorten it!")
        failed.append(out)
        continue
    if os.path.exists(out) and os.path.getsize(out) > 100000:
        print(f"✓ exists: {out}")
        continue
    print(f"→ TTS scene {i} ({len(text)} chars) ...")
    ok = False
    for attempt in range(1, 4):
        r = subprocess.run(
            ['z-ai', 'tts', '-i', text, '-o', out, '--voice', voice,
             '--speed', str(speed), '--format', 'wav'],
            capture_output=True, text=True, timeout=120
        )
        if r.returncode == 0 and os.path.exists(out) and os.path.getsize(out) > 10000:
            print(f"  ✓ done (attempt {attempt})")
            ok = True
            break
        print(f"  ✗ attempt {attempt}: {(r.stderr or r.stdout)[-200:]}")
        time.sleep(20)  # rate-limit backoff
    if not ok:
        failed.append(out)

if failed:
    print(f"\nFAILED: {failed}")
    sys.exit(1)
print("\nAll narration audio ready.")
EOF
