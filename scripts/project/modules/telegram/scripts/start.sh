#!/usr/bin/env bash
# FateCat Telegram 标准化启动脚本
# 用法: ./scripts/start.sh [start|stop|status|restart]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MODULE_DIR="$(dirname "$SCRIPT_DIR")"
REPO_ROOT="$(dirname "$(dirname "$MODULE_DIR")")"
CONFIG_ENV="$REPO_ROOT/assets/config/.env"
LOG_DIR="$MODULE_DIR/output/logs"
PID_FILE="$LOG_DIR/bot.pid"

# 安全加载 .env（禁止 source 执行文件内容）
RUNTIME_HELPERS="$REPO_ROOT/scripts/alternative/runtime_helpers.sh"
if [[ -f "$RUNTIME_HELPERS" ]]; then
  # shellcheck disable=SC1091
  source "$RUNTIME_HELPERS"
else
  safe_load_env_file() {
    local file="$1"
    [[ -f "$file" ]] || return 0
    while IFS= read -r line || [[ -n "$line" ]]; do
      [[ -z "$line" || "$line" =~ ^[[:space:]]*# ]] && continue
      local key=""
      local value=""
      if [[ "$line" =~ ^[[:space:]]*export[[:space:]]+([A-Za-z_][A-Za-z0-9_]*)=(.*)$ ]]; then
        key="${BASH_REMATCH[1]}"
        value="${BASH_REMATCH[2]}"
      elif [[ "$line" =~ ^[[:space:]]*([A-Za-z_][A-Za-z0-9_]*)=(.*)$ ]]; then
        key="${BASH_REMATCH[1]}"
        value="${BASH_REMATCH[2]}"
      else
        continue
      fi
      value="${value%$'\r'}"
      if [[ "$value" =~ ^\".*\"$ ]] || [[ "$value" =~ ^\'.*\'$ ]]; then
        value="${value:1:${#value}-2}"
      fi
      export "$key=$value"
    done < "$file"
  }
fi

load_env() {
  if [[ -f "$CONFIG_ENV" ]]; then
    echo "==> 加载配置: $CONFIG_ENV"
    safe_load_env_file "$CONFIG_ENV"
  else
    echo "⚠️  未找到配置文件: $CONFIG_ENV"
    echo "    请先复制 assets/config/.env.example 为 assets/config/.env"
  fi
}

get_python() {
  if [[ -x "$MODULE_DIR/.venv/bin/python" ]]; then
    echo "$MODULE_DIR/.venv/bin/python"
  elif [[ -x "$REPO_ROOT/.venv/bin/python" ]]; then
    echo "$REPO_ROOT/.venv/bin/python"
  else
    command -v python3
  fi
}

print_disclaimer() {
  python3 - <<'PY'
import json
from pathlib import Path

branding = json.loads(Path("assets/config/branding.json").read_text(encoding="utf-8"))
print(branding["disclaimerTitle"])
print(branding["disclaimerText"])
print("")
PY
}

start() {
  load_env
  mkdir -p "$LOG_DIR"

  if [[ -f "$PID_FILE" ]]; then
    OLD_PID=$(cat "$PID_FILE")
    if kill -0 "$OLD_PID" 2>/dev/null; then
      echo "后台进程已在运行 (PID: $OLD_PID)"
      return 0
    fi
  fi

  PY_BIN=$(get_python)
  cd "$REPO_ROOT"
  print_disclaimer
  echo "==> 启动 FateCat Bot..."
  cd "$MODULE_DIR"
  setsid bash -c "exec \"$PY_BIN\" start.py bot" > "$LOG_DIR/nohup.out" 2>&1 < /dev/null &
  BOT_PID=$!
  echo "$BOT_PID" > "$PID_FILE"

  echo "✅ 启动完成 (PID: $BOT_PID)"
  echo "日志: tail -f $LOG_DIR/bot.log"
}

stop() {
  if [[ -f "$PID_FILE" ]]; then
    PID=$(cat "$PID_FILE")
    if kill -0 "$PID" 2>/dev/null; then
      echo "==> 停止后台进程 (PID: $PID)..."
      kill "$PID"
      sleep 2
      if kill -0 "$PID" 2>/dev/null; then
        kill -9 "$PID"
      fi
      rm -f "$PID_FILE"
      echo "✅ 后台进程已停止"
    else
      echo "后台进程未运行"
      rm -f "$PID_FILE"
    fi
  else
    echo "后台进程未运行"
  fi
}

status() {
  if [[ -f "$PID_FILE" ]]; then
    PID=$(cat "$PID_FILE")
    if kill -0 "$PID" 2>/dev/null; then
      echo "✅ 后台进程运行中 (PID: $PID)"
      return 0
    fi
  fi
  echo "❌ 后台进程未运行"
  return 1
}

case "${1:-status}" in
  start) start ;;
  stop) stop ;;
  status) status ;;
  restart) stop; sleep 1; start ;;
  *)
    echo "用法: $0 {start|stop|status|restart}"
    exit 1
    ;;
esac
