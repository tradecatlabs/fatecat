#!/usr/bin/env bash
set -euo pipefail

base_url="${FATECAT_API_URL:-http://127.0.0.1:8001}"

curl -sS -X POST "${base_url}/capabilities/almanac/calculate" \
  -H 'Content-Type: application/json' \
  -d '{
    "dateRange": {"start": "2026-05-08", "end": "2026-05-08"},
    "eventType": "出行",
    "place": "北京"
  }'
