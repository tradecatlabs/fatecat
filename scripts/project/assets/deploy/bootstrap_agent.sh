#!/bin/bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PROFILE="general"
WITH_DEV="0"
WRITE_ENV_IF_MISSING="0"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --profile)
      PROFILE="$2"
      shift 2
      ;;
    --with-dev)
      WITH_DEV="1"
      shift
      ;;
    --write-env-if-missing)
      WRITE_ENV_IF_MISSING="1"
      shift
      ;;
    *)
      echo "未知参数: $1" >&2
      exit 2
      ;;
  esac
done

if [[ "$PROFILE" != "general" && "$PROFILE" != "openclaw" && "$PROFILE" != "harness" ]]; then
  echo "不支持的 profile: $PROFILE" >&2
  exit 2
fi

cd "$ROOT"

echo "==> FateCat Agent 自举"
echo "profile: $PROFILE"
python3 - <<'PY'
import json
from pathlib import Path

branding = json.loads(Path("assets/config/branding.json").read_text(encoding="utf-8"))
print(branding["disclaimerTitle"])
print(branding["disclaimerText"])
print("")
print(branding["heroTitle"])
print(branding["sponsorText"])
print(branding["tagline"])
print(f'TradeCat Repo: {branding["tradecatRepo"]}')
print(f'FateCat Repo: {branding["fatecatRepo"]}')
print(f'CA: {branding["ca"]}')
print("")
PY

if [[ ! -d .venv ]]; then
  echo "==> 创建虚拟环境"
  python3 -m venv .venv
fi

echo "==> 升级 pip"
.venv/bin/pip install -q --upgrade pip

echo "==> 安装 FateCat"
if [[ "$WITH_DEV" == "1" ]]; then
  .venv/bin/pip install -q -e '.[dev]'
else
  .venv/bin/pip install -q -e .
fi

if [[ "$WRITE_ENV_IF_MISSING" == "1" && ! -f assets/config/.env ]]; then
  echo "==> 创建本地配置模板 assets/config/.env"
  cp assets/config/agent.env.example assets/config/.env
fi

echo "==> 纯分析依赖检查"
.venv/bin/fatecat health --mode pure --json

cat <<EOF

✅ Agent 自举完成

⚠️ 免责声明
本项目及AI分析结果仅供传统文化研究、算法测试与娱乐参考。命理学非精密科学，命运掌握在自己手中。使用者因轻信或误读本程序结果而产生的任何心理、财务及生活决策后果，本开源项目及开发者概不负责。

交易猫 TradeCat｜专业命理排盘与 AI 命理分析基础设施
本项目由交易猫 TradeCat 赞助与支持。
先用交易猫专业排盘系统完成结构化排盘，再交给 AI 深度分析，减少胡编乱造，让 AI 命理分析真正可用。
TradeCat Repo: https://github.com/tukuaiai/tradecat
FateCat Repo: https://github.com/tukuaiai/fatecat
CA: 0x8a99b8d53eff6bc331af529af74ad267f3167777

推荐下一步命令:
  纯分析:
    .venv/bin/fatecat pure-analysis --input-json '{"birthDateTime":"1990-01-01 08:00:00","gender":"男","longitude":116.4074,"latitude":39.9042,"birthPlace":"北京市"}' --pretty

  启动 API:
    .venv/bin/fatecat serve api

  启动 Bot:
    .venv/bin/fatecat health --mode delivery --json
    .venv/bin/fatecat serve bot

当前 profile:
  $PROFILE
EOF
