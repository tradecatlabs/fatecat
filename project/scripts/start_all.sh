#!/usr/bin/env bash
# 项目级兼容启动脚本（含清理旧进程）
# - 杀掉遗留 bot/api 进程
# - 使用 pyproject 生成的 fatecat CLI 后台启动 bot + API
# - 配置由模块内 dotenv 从 assets/config/.env 读取，不在 shell 中 source 执行

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_FILE="${ENV_FILE:-$ROOT/assets/config/.env}"
MODULE_DIR="$ROOT/modules/telegram"
LOG_DIR="$MODULE_DIR/output/logs"
FATE_BIN="$ROOT/.venv/bin/fatecat"

echo "==> 切换到项目根目录: $ROOT"
cd "$ROOT"

if [[ -f "$ENV_FILE" ]]; then
  echo "==> 使用配置文件: $ENV_FILE"
else
  echo "⚠️  未找到 $ENV_FILE，确保 FATE_BOT_TOKEN 已在环境中"
fi

if [[ ! -x "$FATE_BIN" ]]; then
  echo "缺少 CLI 入口: $FATE_BIN" >&2
  echo "请先在 skill 根目录执行 bash scripts/bootstrap.sh，或在 project 根目录执行 scripts/setup/bootstrap_fatecat.sh deps" >&2
  exit 1
fi

echo "==> 清理遗留进程..."
PIDS=$({
  pgrep -f "$MODULE_DIR/src/bot.py" || true
  pgrep -f "$MODULE_DIR/src/main.py" || true
  pgrep -f "fatecat serve both" || true
  # 清理旧版本调度父进程，避免多实例并存
  pgrep -f "start.py both" || true
} | sort -u | tr '\n' ' ')
if [[ -n "$PIDS" ]]; then
  echo "$PIDS" | xargs -r kill
  sleep 1
  # 如有顽固进程，再强杀
  REMAIN=$({
    pgrep -f "$MODULE_DIR/src/bot.py" || true
    pgrep -f "$MODULE_DIR/src/main.py" || true
    pgrep -f "fatecat serve both" || true
    pgrep -f "start.py both" || true
  } | sort -u | tr '\n' ' ')
  if [[ -n "$REMAIN" ]]; then
    echo "$REMAIN" | xargs -r kill -9
  fi
else
  echo "无遗留进程。"
fi

echo "==> 准备日志目录: $LOG_DIR"
mkdir -p "$LOG_DIR"

echo "==> 后台启动 Bot + API（fatecat serve both）..."
nohup "$FATE_BIN" serve both > "$LOG_DIR/nohup.out" 2>&1 &
BOT_PID=$!
echo "$BOT_PID" > "$LOG_DIR/bot.pid"

echo "✅ 启动完成，PID: $BOT_PID"
echo "日志: tail -f $LOG_DIR/bot.log"
echo "nohup: tail -f $LOG_DIR/nohup.out"
