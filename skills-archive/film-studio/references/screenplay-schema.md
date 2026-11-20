# Screenplay Schema — ساختار screenplay.json (قلب سیستم)

> فیلمنامهٔ استودیو. همهٔ ابزارهای بعدی (پکیج پرامپت، تدوین) از این فایل تغذیه می‌شوند.

```jsonc
{
  // ── شناسنامه ─────────────────────────────────────────────
  "project": "silent-millennia",            // slug = نام پوشه projects/
  "title": "THE SILENT MILLENNIA",
  "title_fa": "هزاره‌های خاموش",
  "logline": "پیش از هر شهر و هر خط، ...) — یک جمله",
  "mode": "google-suite",                   // google-suite | in-house | hybrid
  "pipeline": "documentary",                // documentary|cinematic|explainer|short-form|montage
  "target": {
    "duration_s": 90,                       // هدف نهایی (±۱۰٪)
    "aspect": "16:9",                       // 16:9 | 9:16
    "resolution": "1080p",                  // 1080p | 720p
    "fps": 30
  },
  "language": { "narration": "en", "subtitle": "fa" },

  // ── سبک (بلاک ثابت — در هر پرامپت verbatim تکرار می‌شود) ──
  "style": {
    "style_prompt": "hand-painted cinematic documentary style, visible impasto brushwork, warm ochre and amber palette, soft golden hour light, volumetric dust rays, painterly texture, no text, no watermark",
    "palette": "ochre-amber / cold blue-grey for tension",
    "grade": "warm filmic, lifted blacks"
  },

  // ── بانک شخصیت (MovieAgent) ─────────────────────────────
  "characters": [
    {
      "id": "narrator-figure",
      "name": "The Wanderer",
      "attributes": "weathered man in his 50s, salt-and-pepper beard, indigo wool cloak, leather satchel",  // ← verbatim در هر پرامپت
      "sheet_prompt": "character reference sheet, front and side view, neutral studio light — …(style_prompt)"
    }
  ],

  // ── شات‌ها ───────────────────────────────────────────────
  "shots": [
    {
      "id": "S01",
      "act": "COLD OPEN",
      "beat": "hook — پرسش قلاب",
      "narration": "Every story you know about the past was written down by someone.",
      "subtitle": "هر داستانی که از گذشته می‌شناسی، کسی آن را نوشته است.",
      "silence_after": 0.0,                  // سکوت عمدی بعد از این شات (ثانیه)
      "visual": {                            // فرمول ۵بخشی — به Veo prompt تبدیل می‌شود
        "cinematography": "slow aerial establishing shot, gentle drift forward",
        "subject": "sun-scorched plain with scattered stone pillars",
        "action": "dust drifts across ancient carved stones",
        "context": "pre-dawn haze, distant hills",
        "style_ambiance": "…"                 // اگر خالی → از style.style_prompt
      },
      "keyframe": {                          // Nano Banana (کی‌فریم/فریم اول)
        "composition": "wide establishing composition, horizon on lower third",
        "extra": ""                           // جزئیات مخصوص کی‌فریم
      },
      "source": "video",                     // video (Veo/Omni) | image (KenBurns)
      "motion": "zoom-in",                   // برای image: zoom-in|zoom-out|pan-left|pan-right
      "keep_clip_audio": "duck",             // برای video: keep | duck | mute
      "transition_out": "crossfade",         // crossfade | cut | fade-black
      "first_last_frame": null,              // یا { "end_beat": "…" } → جفت NB می‌سازد
      "title_overlay": true                  // عنوان روی این شات
    }
  ],

  // ── صدا ─────────────────────────────────────────────────
  "audio": {
    "voice": "jam",                          // MODE B: z-ai tts
    "speed": 0.95,
    "narration_wpm": 135,                    // documentary سینمایی: 130-140 | explainer: 155
    "music": {
      "enabled": true,
      "plan": "generated",                   // library | generated | none | user
      "mood": "ambient pad, root+fifth, slow swell in act 3",
      "volume_db": -23
    }
  },

  // ── تیتراژ ───────────────────────────────────────────────
  "credits": [
    { "role": "WRITTEN & DIRECTED BY", "name": "GLM + Gemini Pro" },
    { "role": "PRODUCTION DESIGN BY", "name": "Nano Banana" },
    { "role": "CINEMATOGRAPHY BY", "name": "Veo 3.1 · Google Flow" },
    { "role": "EDITED WITH", "name": "Gemini Omni Flash" },
    { "role": "VOICE BY", "name": "Z-AI TTS" },
    { "role": "MADE WITH", "name": "Film Studio Skill" }
  ]
}
```

## قواعد اعتبارسنجی

1. `shots` حداقل ۶، حداکثر ۱۶ (برای ۶۰-۱۲۰s).
2. شات‌های `source: video` → منطق مدت: کلیپ Veo = ۴/۶/۸s (نزدیک‌ترین به
   `LEAD+narr+TAIL` انتخاب و روایت در پکیج هم‌اندازه می‌شود). Omni = ۳-۱۰s.
3. هر `narration` ≤ ۹۰۰ کاراکتر (سقف TTS داخلی).
4. `subtitle` ترجمهٔ وفادار-به-معنا، بدون newline.
5. `style.style_prompt` غیرخالی و در build_package به‌صورت خودکار به همهٔ پرامپت‌ها
   چسبانده می‌شود — در خود پرامپت‌ها تکرارش نکن.
6. `attributes` هر شخصیت باید در `visual.subject` هر شاتِ حاوی آن شخصیت verbatim آمده
   باشد (Identity Anchoring) — build_package هشدار می‌دهد اگر نبود.
7. `title_overlay` فقط روی شات اول (یا شات دوم اگر اول cold-open خیلی کوتاه است).
8. فقط یک شات `transition_out: fade-black` — آخرین شات قبل از تیتراژ (خودکار).

## تبدیل‌های خودکار (در build_package.py)

- `visual` + `style` → **پرامپت Veo** (فرمول [Cinematography]+[Subject]+[Action]+[Context]+[Style & Ambiance] + صدا)
- `keyframe` + `visual` + `style` → **پرامپت Nano Banana** (فرمول [Subject]+[Action]+[Location]+[Composition]+[Style])
- `characters[].sheet_prompt` → **شیت شخصیت NB** (Ingredient)
- `first_last_frame` → **جفت پرامپت NB + پرامپت گذار Veo**
- `narration`/`subtitle` → فایل روایت/زیرنویس
- تخمین زمان: `dur ≈ 0.6 + words/wpm*60 + 0.8 + silence_after`
- خروجی تایم‌لاین → `production_package/timeline.json` (ورودی assemble.py)
