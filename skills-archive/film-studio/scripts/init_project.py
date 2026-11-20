#!/usr/bin/env python3
"""init_project.py — ساخت workspace پروژه فیلم + project.json

Usage:
  python3 init_project.py <slug> --mode google-suite --pipeline documentary \
      --title "THE SILENT MILLENNIA" --title-fa "هزاره‌های خاموش" [--dir projects]

Creates:
  projects/<slug>/
  ├── project.json
  ├── artifacts/  production_package/  assets/{clips,images,voice,music}
  ├── work/  output/
"""
import argparse
import json
import os
import sys
from datetime import datetime, timezone

STAGES = ["intake", "research", "concept", "screenplay", "shot_list",
          "assets", "assembly", "qc", "deliver"]

MODES = ["google-suite", "in-house", "hybrid"]
PIPELINES = ["documentary", "cinematic", "explainer", "short-form", "montage"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slug")
    ap.add_argument("--mode", default="google-suite", choices=MODES)
    ap.add_argument("--pipeline", default="documentary", choices=PIPELINES)
    ap.add_argument("--title", default="")
    ap.add_argument("--title-fa", default="")
    ap.add_argument("--duration", type=int, default=90)
    ap.add_argument("--aspect", default="16:9", choices=["16:9", "9:16"])
    ap.add_argument("--dir", default=os.path.join("projects"))
    args = ap.parse_args()

    slug = "".join(c if c.isalnum() or c == "-" else "-" for c in args.slug.lower()).strip("-")
    root = os.path.abspath(os.path.join(args.dir, slug))
    if os.path.exists(root):
        print(f"⚠ project exists: {root} (keeping it)")
    else:
        for sub in ["artifacts", "production_package",
                    "assets/clips", "assets/images", "assets/voice", "assets/music",
                    "work", "output"]:
            os.makedirs(os.path.join(root, sub), exist_ok=True)

    now = datetime.now(timezone.utc).isoformat()
    project = {
        "project": slug,
        "title": args.title or slug.upper(),
        "title_fa": args.title_fa,
        "mode": args.mode,
        "pipeline": args.pipeline,
        "target": {"duration_s": args.duration, "aspect": args.aspect},
        "created_at": now,
        "updated_at": now,
        "stages": {s: ("completed" if s == "intake" else "pending") for s in STAGES},
        "decision_log": [
            {
                "category": "mode_selection",
                "subject": "Execution mode",
                "options_considered": MODES,
                "selected": args.mode,
                "rejected_because": "user tool stack / request routing",
                "confidence": 0.8,
                "at": now,
            },
            {
                "category": "pipeline_selection",
                "subject": "Production pipeline",
                "options_considered": PIPELINES,
                "selected": args.pipeline,
                "rejected_because": "genre fit",
                "confidence": 0.8,
                "at": now,
            },
        ],
    }
    pj = os.path.join(root, "project.json")
    if not os.path.exists(pj):
        with open(pj, "w", encoding="utf-8") as f:
            json.dump(project, f, ensure_ascii=False, indent=2)

    print(f"✓ project ready: {root}")
    print(f"  mode={args.mode} pipeline={args.pipeline} target={args.duration}s {args.aspect}")
    print(f"  next: research → artifacts/research_brief.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
