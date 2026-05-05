#!/usr/bin/env bash
# FateCat 项目级兼容自举脚本
# 作用：
# 1) 创建/复用 Python 虚拟环境并按 pyproject 安装 fatecat CLI
# 2) 为 Node/TS 外部仓库安装依赖并尝试构建（仅在存在 build 脚本时）
# 3) 可选通过统一 fatecat CLI 启动 Telegram Bot / FastAPI / both
#
# 用法：
#   chmod +x scripts/setup/bootstrap_fatecat.sh
#   scripts/setup/bootstrap_fatecat.sh bot   # 仅 Bot
#   scripts/setup/bootstrap_fatecat.sh api   # 仅 API
#   scripts/setup/bootstrap_fatecat.sh both  # Bot+API
#   scripts/setup/bootstrap_fatecat.sh deps  # 只装依赖不启动
#
# 依赖：python3；若要构建外部 Node 仓库，还需 node、npm
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
VENV="$ROOT/.venv"

NODE_REPOS=(
  "$ROOT/assets/vendor/github/sxwnl-master"
  "$ROOT/assets/vendor/github/iztro-main"
  "$ROOT/assets/vendor/github/fortel-ziweidoushu-main"
  "$ROOT/assets/vendor/github/js_astro-master"
)

log() { printf "\033[1;32m[BOOT]\033[0m %s\n" "$*"; }
warn() { printf "\033[1;33m[WARN]\033[0m %s\n" "$*"; }
err() { printf "\033[1;31m[ERR ]\033[0m %s\n" "$*"; }

check_bin() {
  if ! command -v "$1" >/dev/null 2>&1; then
    err "缺少依赖可执行文件：$1"
    exit 1
  fi
}

setup_python() {
  check_bin python3
  log "创建/复用虚拟环境 $VENV"
  if [ ! -d "$VENV" ]; then
    python3 -m venv "$VENV"
  fi
  # shellcheck disable=SC1090
  source "$VENV/bin/activate"
  log "升级 pip"
  pip install --upgrade pip >/dev/null
  log "按 pyproject 安装 FateCat CLI"
  pip install -e "$ROOT"
}

setup_node_repo() {
  local repo="$1"
  if [ ! -f "$repo/package.json" ]; then
    warn "跳过 Node 仓库（缺少 package.json）：$repo"
    return
  fi
  log "安装 Node 依赖：$repo"
  (cd "$repo" && npm install)
  # 如果存在 build 脚本则尝试构建
  if (cd "$repo" && npm run | grep -q "build"); then
    log "构建：$repo"
    (cd "$repo" && npm run build)
  fi
}

setup_node_all() {
  if ! command -v node >/dev/null 2>&1 || ! command -v npm >/dev/null 2>&1; then
    warn "未安装 node/npm，跳过外部 Node 仓库构建；纯 Python 与 fatecat CLI 不受影响"
    return
  fi
  for repo in "${NODE_REPOS[@]}"; do
    setup_node_repo "$repo"
  done
}

start_module() {
  local mode="$1"
  log "启动模块: $mode"
  "$VENV/bin/fatecat" serve "$mode"
}

main() {
  local action="${1:-deps}"
  log "项目根目录: $ROOT"
  setup_python
  setup_node_all

  case "$action" in
    deps)
      log "依赖安装完成（未启动模块）"
      ;;
    bot|api|both)
      start_module "$action"
      ;;
    *)
      err "未知参数：$action（可选 bot|api|both|deps）"
      exit 1
      ;;
  esac
}

main "$@"
