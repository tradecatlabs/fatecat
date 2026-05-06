#!/usr/bin/env bash
# 项目级兼容排盘脚本：通过统一 fatecat CLI 输出 JSON
# 用法: ./generate_bazi.sh "2004-02-21" "19:30" "male" "北京" 116.4 39.9 "测试用户"

set -euo pipefail

# 参数
BIRTH_DATE="${1:-2004-02-21}"
BIRTH_TIME="${2:-19:30}"
GENDER="${3:-male}"
BIRTH_PLACE="${4:-北京}"
LONGITUDE="${5:-116.4}"
LATITUDE="${6:-39.9}"
NAME="${7:-}"

# 输出文件名
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
OUTPUT_BASE="output_${TIMESTAMP}"
BIRTH_DATETIME="${BIRTH_DATE} ${BIRTH_TIME}"
if [[ "$BIRTH_TIME" != *:*:* ]]; then
  BIRTH_DATETIME="${BIRTH_DATE} ${BIRTH_TIME}:00"
fi

# 项目路径
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUTPUT_DIR="${PROJECT_DIR}/modules/telegram/output"
FATE_BIN="${PROJECT_DIR}/.venv/bin/fatecat"

# 创建输出目录
mkdir -p "$OUTPUT_DIR"

if [[ ! -x "$FATE_BIN" ]]; then
  echo "缺少 CLI 入口: $FATE_BIN" >&2
  echo "请先在 skill 根目录执行 bash scripts/bootstrap.sh，或在 scripts/project 根目录执行 scripts/setup/bootstrap_fatecat.sh deps" >&2
  exit 1
fi

OUTPUT_FILE="${OUTPUT_DIR}/${OUTPUT_BASE}.json"
"$FATE_BIN" pure-analysis \
  --birth-datetime "$BIRTH_DATETIME" \
  --gender "$GENDER" \
  --longitude "$LONGITUDE" \
  --latitude "$LATITUDE" \
  --birth-place "$BIRTH_PLACE" \
  --name "$NAME" \
  --output-file "$OUTPUT_FILE" \
  --pretty

echo "JSON: $OUTPUT_FILE"

echo ""
echo "完成！"
