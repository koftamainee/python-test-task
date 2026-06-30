#!/usr/bin/env bash
set -euo pipefail

SERVICE_URL="${1:-http://localhost:8080}"

curl -s "$SERVICE_URL/openapi.json" | python3 -c "
import sys, json
d = json.load(sys.stdin)
with open('docs.json', 'w', encoding='utf-8') as f:
    json.dump(d, f, indent=2, ensure_ascii=False)
print('docs.json generated')
"