# Production Methodology — مراحل، آرتیفکت‌ها، گیت‌های کیفیت

> منبع: OpenMontage `AGENT_GUIDE.md` + `pipeline_defs/*.yaml` + `skills/meta/reviewer.md`
> + `checkpoint-protocol.md` — اقتباس‌شده برای استودیو.

## ماشین حالت تولید

```
intake → research → concept → screenplay → shot_list → assets → assembly → qc → deliver
```

هر مرحله: **ورودی‌های الزامی → خروجی canonical → معیار قبولی → گیت انسانی؟**

| مرحله | ورودی | خروجی canonical | معیار قبولی | Gate |
|-------|-------|-----------------|-------------|------|
| intake | پیام کاربر | `project.json` (mode+pipeline+target) | mode/pipeline/duration/زبان مشخص | ✋ اگر مبهم |
| research | موضوع | `artifacts/research_brief.md` | ≥۸ جستجو؛ ≥۵ واقعیت با منبع؛ مراجع بصری با URL؛ ۳ زاویهٔ روایی | خیر |
| concept | research_brief | `artifacts/concepts.md` (۲-۳ کانسپت متمایز) | کانسپت‌ها واقعاً متفاوت (نه رنگ‌عوضی)؛ هرکدام: logline + سبک + مسیر ابزار + برآورد هزینه/زمان | **بله** |
| screenplay | کانسپت انتخابی | `artifacts/screenplay.json` | اسکیمای screenplay معتبر؛ قوس کامل؛ wpm درست؛ بدون صفت ذهنی | **بله** |
| shot_list | screenplay | `production_package/` | هر شات: پرامپت NB کامل + پرامپت Veo (فرمول ۵بخشی) + notes ویرایش Omni + زمان‌بندی | **بله** |
| assets | پکیج | `assets/clips|images|voice|music` | همهٔ فایل‌های ارجاع‌شده موجود | **بله** (پیش از رندر) |
| assembly | assets + timeline | `work/*.mp4` → `output/final.mp4` | ffprobe سالم؛ بدون اسلایدشو | خیر |
| qc | final.mp4 | گزارش QC | چک‌لیست پایین PASS | خیر |
| deliver | QC PASS | کپی در `/home/z/my-project/download/` | مسیر به کاربر اعلام شد | خیر |

## پروتکل Checkpoint (داخل project.json)

```json
"stages": {
  "research":   {"status": "completed", "at": "..."},
  "concept":    {"status": "awaiting_user", "at": "..."},
  ...
}
```
- status ∈ `pending | in_progress | completed | awaiting_user | failed`
- قبل از ورود به هر مرحله → `in_progress`؛ بعد از خروجی → `completed` یا `awaiting_user`.
- اگر مرحله gate دارد: پس از ارائهٔ خلاصه **نوبتت را تمام کن** و منتظر کاربر بمان.
  کار بیشتر در همان پاسخ = تخلف از گیت.
- تأییدِ زودهنگام گیت‌های بعدی را پوشش نمی‌دهد؛ پیش‌اجازهٔ کل مسیر باید به‌صورت
  decision (`approval_policy`) ثبت شود.

## Decision Log (append-only)

```json
"decision_log": [
  {
    "category": "pipeline_selection",
    "subject": "Production pipeline",
    "options_considered": ["documentary", "cinematic", "explainer"],
    "selected": "documentary",
    "rejected_because": "...",
    "confidence": 0.85,
    "at": "..."
  }
]
```
- هر تغییرِ انتخابِ قبلاً-ثبت‌شده = **مدخل جدید** با همان (category, subject)؛
  گزینهٔ قدیمی → options_considered با rejected_because: "changed mid-run".
- ویرایشِ خاموشِ مدخل قبلی = نقص.

دسته‌های استاندارد: `pipeline_selection`, `mode_selection`, `concept_selection`,
`style_selection`, `music_plan`, `voice_selection`, `shot_treatment`, `approval_policy`.

## Quality Gates پیش از رندر (Pre-compose Validation)

1. **Delivery Promise:** چیزی که در concept قول داده‌ای باید در timeline قابل اثبات باشد —
   «ویدیوی متحرک» = کلیپ‌های واقعیِ متحرک، نه تصویر ثابت + Ken Burns (مگر آنکه صریحاً
   animatic بخواهند). سقوط پنهان به اسلایدشو = CRITICAL.
2. **پوشش کامل:** هر جملهٔ روایت حداقل یک شات دارد؛ هیچ شاتی بدون روایتِ منطقی نماند
   (مگر montage).
3. **پلان زمان‌بندی:** مجموع (LEAD + narration + TAIL + فیدها) با مدت هدف ±۱۰٪.
4. **consistency:** style block یکسان verbatim در همهٔ پرامپت‌ها؛ attributes شخصیت در
   هر شاتِ حاوی شخصیت.

## Self-Review پس از هر مرحله (پیش از checkpoint)

- حداکثر ۲ دور بازبینی؛ بعد: pass با warning و ادامه.
- یافته‌ها: `critical` (باید اصلاح شود) / `suggestion` (ثبت کن و ادامه) / `nitpick`.
- برای هر مرحله review_focus مشخص: مثلاً screenplay → «beat map صعودی است؟ دیالوگ کم
  و هدفمند است؟ reveal/landing واضح‌اند؟»

## QC پس از رندر (اجباری — از OpenMontage reviewer)

1. **ffprobe:** duration/codec/resolution/fps/audio-stream مطابق پلان.
2. **استخراج فریم:** ≥۳ فریم (شروع/میانه/پایان) + فریم‌های حساس (تایتل، تیتراژ،
   گذار سخت) → بررسی بصری.
3. **سطح صدا:** قله‌ها نرم؛ روایت ≥ ۸dB بالاتر از موسیقی؛ بدون کلیپ.
4. **زیرنویس:** RTL درست، بدون هم‌پوشانی، خوانا (کنتراست با باکس).
5. **Delivery promise:** متحرک‌بودن شات‌های قول‌داده‌شده.
6. **مقیاس زمانی:** خطای هم‌گامی صدا/تصویر < ۰٫۳s.

فقط اگر QC پاس شد، فایل به download/ می‌رود و اعلام تحویل داده می‌شود.

## بودجه و هزینه (برای MODE A)

تخمین قبل از تولید به کاربر اعلام شود:
- Veo 3.1: کلیپ ۸s مرجع ~$۰٫۳-۰٫۶ (بسته به سرویس/اشتراک)
- Omni Flash: ~$۰٫۱/ثانیه خروجی (۵,۷۹۲ توکن/s @ $۱۷٫۵/۱M)
- Nano Banana: تصویر 1K/2K/4K — ارزان؛ Ingredients به صرفه
- قانون: نمونه (sample) قبل از批量 — اول ۱ شات تست، بعد تولید کامل.

## اصول Executive Producer

1. **هرگز تولید مستقیم/بدون خط تولید نکن** — همه‌چیز از pipeline می‌گذرد.
2. **اعلام قبل از اجرای هر تولید پرهزینه.**
3. **بدون جایگزینی یک‌جانبه** — مسیر تأییدشده مسدود شد → blocker ساخت‌یافته:
   چه امتحان شد / چه شکست خورد / علت (auth? provider? پرامپت؟) / گزینه‌ها / پیشنهاد.
4. **ارائهٔ تصمیم با پیشنهاد:** شورت‌لیست + tradeoffها + یک پیشنهاد + انتظار.
5. **Musique plan اجباری در concept:** کتابخانهٔ شخصی / تولید / بدون — انتخاب کاربر.
