#!/bin/bash
# generate_images.sh — فاز ۲: تولید تصویر هر صحنه + پلیت تیتراژ
# استفاده: bash generate_images.sh <project-dir>
# idempotent: فایل موجود را دوباره نمی‌سازد (برای ریجنرایت: rm images/scene_XX.png)
set -u

PROJ="${1:-}"
if [ -z "$PROJ" ] || [ ! -f "$PROJ/screenplay.json" ]; then
  echo "Usage: bash generate_images.sh <project-dir-with-screenplay.json>"
  exit 1
fi

cd "$PROJ"
mkdir -p images

# استخراج style_prompt و صحنه‌ها با python
python3 - << 'EOF' > /tmp/img_tasks.json
import json, sys
with open('screenplay.json') as f:
    sp = json.load(f)
tasks = []
for i, sc in enumerate(sp['scenes'], 1):
    prompt = f"{sp['style_prompt']}, {sc['visual_prompt']}"
    tasks.append({"idx": i, "prompt": prompt, "out": f"images/scene_{i:02d}.png"})
# پلیت تیتراژ: همان سبک، زمینه تیره سینمایی
title = sp.get('title', 'UNTITLED')
tasks.append({"idx": 0, "prompt": f"{sp['style_prompt']}, dark cinematic abstract background for end credits, deep shadows, subtle texture, moody atmosphere", "out": "images/credits_bg.png"})
json.dump(tasks, sys.stdout, ensure_ascii=False)
EOF

python3 - << 'EOF'
import json, subprocess, os, sys, time

with open('/tmp/img_tasks.json') as f:
    tasks = json.load(f)

failed = []
for t in tasks:
    out = t['out']
    if os.path.exists(out) and os.path.getsize(out) > 10000:
        print(f"✓ exists: {out}")
        continue
    print(f"→ generating {out} ...")
    ok = False
    for attempt in range(1, 4):
        r = subprocess.run(
            ['z-ai', 'image', '-p', t['prompt'], '-o', out, '-s', '1344x768'],
            capture_output=True, text=True, timeout=180
        )
        if r.returncode == 0 and os.path.exists(out) and os.path.getsize(out) > 10000:
            print(f"  ✓ done (attempt {attempt})")
            ok = True
            break
        print(f"  ✗ attempt {attempt} failed: {(r.stderr or r.stdout)[-200:]}")
        time.sleep(15)
    if not ok:
        failed.append(t['out'])

if failed:
    print(f"\nFAILED: {failed}")
    sys.exit(1)
print("\nAll images ready.")
EOF
