#!/usr/bin/env bash
# اعتبارسنجی همه URLهای inspiration_data.json — خروجی: dead/redirect/report
set -u
cd "$(dirname "$0")/.."
IN=data/inspiration_data.json
OUT=scripts/inspiration_url_report.txt

python3 - <<'PY' > /tmp/urls.txt
import json
data = json.load(open('data/inspiration_data.json', encoding='utf-8'))
for role, items in data.items():
    for it in items:
        print(role + '\t' + it['name'] + '\t' + it['url'])
PY

TOTAL=$(wc -l < /tmp/urls.txt)
echo "checking $TOTAL urls..." >&2
> "$OUT"
i=0
while IFS=$'\t' read -r role name url; do
  i=$((i+1))
  code=$(curl -s -o /dev/null -w "%{http_code}" -L --max-time 15 -A "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36" "$url" 2>/dev/null)
  echo -e "$code\t$role\t$name\t$url" >> "$OUT"
  [ $((i % 25)) -eq 0 ] && echo "  $i/$TOTAL..." >&2
done < /tmp/urls.txt

echo "=== SUMMARY ===" >&2
awk -F'\t' '{print $1}' "$OUT" | sort | uniq -c | sort -rn
echo "--- non-2xx/3xx ---" >&2
grep -vE '^[23]' "$OUT" | head -40
