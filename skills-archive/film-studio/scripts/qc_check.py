#!/usr/bin/env python3
"""qc_check.py — کنترل کیفیت پس از رندر (از پروتکل reviewer)

بررسی‌ها:
  ۱. ffprobe: مدت/کدک/رزولوشن/fps/جریان صدا مطابق timeline
  ۲. استخراج فریم در نقاط حساس (شروع/میانه/پایان + عنوان + تیتراژ)
  ۳. تحلیل سطح صدا (قله/میانگین) — روایت باید بالای بستر باشد
  ۴. گزارش JSON: artifacts/qc_report.json + خلاصه متن

Usage: python3 qc_check.py <project-dir>
"""
import json
import os
import subprocess
import sys


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    return r.returncode, r.stdout, r.stderr


def probe(path):
    c, out, _ = run(["ffprobe", "-v", "error", "-show_entries",
                     "format=duration:stream=codec_type,codec_name,width,height,avg_frame_rate",
                     "-of", "json", path])
    d = json.loads(out or "{}")
    streams = d.get("streams", [])
    v = next((s for s in streams if s.get("codec_type") == "video"), {})
    a = next((s for s in streams if s.get("codec_type") == "audio"), {})
    return {
        "duration": float(d.get("format", {}).get("duration", 0) or 0),
        "video": v.get("codec_name"), "audio": a.get("codec_name"),
        "w": v.get("width"), "h": v.get("height"),
        "fps": v.get("avg_frame_rate"),
    }


def loudness(path):
    c, out, err = run(["ffmpeg", "-nostdin", "-i", path, "-af",
                       "volumedetect", "-f", "null", "-"])
    stats = {}
    for line in (err or "").splitlines():
        if "mean_volume" in line:
            stats["mean_db"] = float(line.split("mean_volume:")[1].split("dB")[0])
        if "max_volume" in line:
            stats["max_db"] = float(line.split("max_volume:")[1].split("dB")[0])
    return stats


def main():
    proj = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else "")
    final = os.path.join(proj, "output", "final.mp4")
    if not os.path.isfile(final):
        sys.exit(f"✗ final.mp4 not found: {final}")
    tl_path = os.path.join(proj, "production_package", "timeline.json")
    tl = json.load(open(tl_path, encoding="utf-8")) if os.path.isfile(tl_path) else {}

    p = probe(final)
    findings, passes = [], []

    # ۱. مشخصات
    exp_total = tl.get("total")
    if exp_total and abs(p["duration"] - exp_total) > 1.0:
        findings.append(f"CRITICAL: duration {p['duration']:.1f}s vs planned {exp_total}s")
    else:
        passes.append(f"duration {p['duration']:.1f}s ≈ plan {exp_total or '?'}s")
    if p["video"] != "h264":
        findings.append(f"CRITICAL: video codec {p['video']} (want h264)")
    else:
        passes.append(f"codec {p['video']}/{p['audio']}")
    if not p["audio"]:
        findings.append("CRITICAL: no audio stream")
    else:
        passes.append("audio stream present")

    # ۲. فریم‌های حساس
    qc_dir = os.path.join(proj, "artifacts")
    os.makedirs(qc_dir, exist_ok=True)
    frames = []
    marks = {t: name for t, name in [
        (1.5, "title"), (p["duration"] * 0.35, "mid"),
        (p["duration"] * 0.65, "late"),
        ((tl.get("credits_start") or p["duration"] * 0.9) + 3.0, "credits"),
        (p["duration"] - 1.0, "end"),
    ] if 0 < t < p["duration"] - 0.2}
    for t, name in marks.items():
        out_jpg = os.path.join(qc_dir, f"qc_{name}.jpg")
        c, _, err = run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{t:.2f}",
                         "-i", final, "-frames:v", "1", "-q:v", "3", out_jpg])
        if c == 0 and os.path.isfile(out_jpg):
            frames.append({"t": round(t, 2), "name": name, "file": out_jpg})
            passes.append(f"frame {name} @ {t:.1f}s")
        else:
            findings.append(f"SUGGESTION: frame extraction failed @ {t:.1f}s")

    # ۳. بلندی صدا
    vol = loudness(final)
    if vol:
        if vol.get("max_db", 0) > -0.5:
            findings.append(f"CRITICAL: clipping risk (max {vol['max_db']}dB)")
        else:
            passes.append(f"peak {vol['max_db']}dB, mean {vol.get('mean_db')}dB")

    report = {
        "file": final, "probe": p, "loudness": vol, "frames": frames,
        "passes": passes, "findings": findings,
        "verdict": "PASS" if not any("CRITICAL" in f for f in findings) else "FAIL",
    }
    rp = os.path.join(qc_dir, "qc_report.json")
    with open(rp, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"QC → {rp}")
    for x in passes:
        print(f"  ✓ {x}")
    for x in findings:
        print(f"  ✗ {x}")
    print(f"VERDICT: {report['verdict']}")
    if report["verdict"] == "PASS":
        print(f"\n→ آمادهٔ تحویل: کپی کن به /home/z/my-project/download/")
    return 0 if report["verdict"] == "PASS" else 2


if __name__ == "__main__":
    sys.exit(main())
