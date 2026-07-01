#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PYTHON_BIN="${PYTHON_BIN:-python3}"

run_case() {
  local mode="$1"
  local question="$2"
  local context="$3"
  echo "===== $mode ====="
  "$PYTHON_BIN" "$ROOT/scripts/render_reading.py" \
    --mode "$mode" \
    --question "$question" \
    --context "$context" \
    --date "2026-03-16" \
    --style standard
  echo
}

career_output="$($PYTHON_BIN "$ROOT/scripts/render_reading.py" \
  --mode career \
  --question "我要不要辞职做自己的项目" \
  --context "现在工作稳定但很消耗，手里有一个想做半年的产品方向，还没验证过付费。" \
  --date "2026-03-16" \
  --style standard)"

echo "===== career ====="
printf '%s\n\n' "$career_output"

printf '%s' "$career_output" | grep -Eq "这不是立刻翻桌的局，更像边搭新盘边等时机成熟。|短期仍偏迟滞，硬催只会把风险提前显形。|眼下更像补盘期，不是猛跳期；中势好不好，要看你现在肯不肯先做笨功。"
career_advice_count=$(printf '%s' "$career_output" | grep -o '这类局面更适合先做副线验证，而不是把退路一次压没。' | wc -l | tr -d ' ')
[ "$career_advice_count" = "1" ]

run_case "relationship" "我该不该主动联系他" "之前聊得不错，但最近冷下来了。我怕不联系就断掉，联系又怕显得太主动。"
run_case "fortune" "为什么我最近做什么都不顺" "事情很多，睡眠一般，开了很多线但都推进不快。"
run_case "personality" "我是不是那种容易自我消耗的人" "常常一开始很猛，后面就乱，想很多，也容易同时开很多线。"

relationship_output="$($PYTHON_BIN "$ROOT/scripts/render_reading.py" \
  --mode relationship \
  --question "我该不该主动联系他" \
  --context "之前聊得不错，但最近冷下来了。我怕不联系就断掉，联系又怕显得太主动。" \
  --date "2026-03-16" \
  --style standard)"

relationship_advice_count=$(printf '%s' "$relationship_output" | grep -o '现在更适合先守住分寸，不要拿追问去换安全感。' | wc -l | tr -d ' ')
[ "$relationship_advice_count" = "1" ]

relationship_deep_output="$($PYTHON_BIN "$ROOT/scripts/render_reading.py" \
  --mode relationship \
  --question "我该不该主动联系他" \
  --context "之前聊得不错，但最近冷下来了。我怕不联系就断掉，联系又怕显得太主动。" \
  --date "2026-03-16" \
  --style deep)"

printf '%s' "$relationship_deep_output" | grep -q '命中场景：该不该主动联系'
if printf '%s' "$relationship_deep_output" | grep -q '。；'; then
  echo 'punctuation regression: found 。； in deep output' >&2
  exit 1
fi

reconcile_output="$($PYTHON_BIN "$ROOT/scripts/render_reading.py" \
  --mode relationship \
  --question "我要不要主动联系前任" \
  --context "我们断联一阵了，我想知道还有没有复合可能。" \
  --date "2026-03-16" \
  --style deep)"

printf '%s' "$reconcile_output" | grep -q '命中场景：复合 / 旧人回头'

contact_output="$($PYTHON_BIN "$ROOT/scripts/render_reading.py" \
  --mode relationship \
  --question "我要不要主动联系他" \
  --context "之前聊得不错，但最近冷下来了。" \
  --date "2026-03-16" \
  --style deep)"

printf '%s' "$contact_output" | grep -q '命中场景：该不该主动联系'

echo "Smoke test passed."
