#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
source "${script_dir}/common.sh"

remove_venv="0"
dry_run="0"

usage() {
  cat <<'EOF'
用法:
  bash scripts/clean-runtime.sh [--venv] [--dry-run]

说明:
  - 清理根 skill 输出目录、本地编辑器历史与 scripts/project 内的本地缓存
  - 默认不删除 scripts/project/.venv；如需彻底重建环境，再加 --venv
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --venv)
      remove_venv="1"
      shift
      ;;
    --dry-run)
      dry_run="1"
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      usage_error "未知参数: $1"
      ;;
  esac
done

targets=(
  "${skill_root}/output"
  "${skill_root}/.history"
  "${skill_root}/.pytest_cache"
  "${skill_root}/.ruff_cache"
  "${skill_root}/.mypy_cache"
  "${project_root}/.pytest_cache"
  "${project_root}/.ruff_cache"
  "${project_root}/.mypy_cache"
  "${project_root}/modules/telegram/output"
)

if [[ "${remove_venv}" == "1" ]]; then
  targets+=("${skill_root}/.venv" "${skill_root}/venv" "${project_root}/.venv")
fi

for target in "${targets[@]}"; do
  if [[ ! -e "${target}" ]]; then
    continue
  fi

  if [[ "${dry_run}" == "1" ]]; then
    echo "[clean-runtime] would remove ${target}"
    continue
  fi

  chmod -R u+w "${target}" 2>/dev/null || true
  rm -rf "${target}"
  echo "[clean-runtime] removed ${target}"
done

python_cache_dirs_count="$(
  find "${project_root}" \
    -path "${project_root}/.venv" -prune -o \
    -type d -name '__pycache__' -print 2>/dev/null | wc -l
)"
python_bytecode_count="$(
  find "${project_root}" \
    -path "${project_root}/.venv" -prune -o \
    -type f \( -name '*.pyc' -o -name '*.pyo' \) -print 2>/dev/null | wc -l
)"

if [[ "${dry_run}" == "1" ]]; then
  echo "[clean-runtime] would remove ${python_cache_dirs_count} __pycache__ dirs under ${project_root}"
  echo "[clean-runtime] would remove ${python_bytecode_count} Python bytecode files under ${project_root}"
  exit 0
fi

if [[ "${python_cache_dirs_count}" != "0" ]]; then
  find "${project_root}" \
    -path "${project_root}/.venv" -prune -o \
    -type d -name '__pycache__' -exec rm -rf {} +
fi

if [[ "${python_bytecode_count}" != "0" ]]; then
  find "${project_root}" \
    -path "${project_root}/.venv" -prune -o \
    -type f \( -name '*.pyc' -o -name '*.pyo' \) -exec rm -f {} +
fi

echo "[clean-runtime] removed ${python_cache_dirs_count} __pycache__ dirs"
echo "[clean-runtime] removed ${python_bytecode_count} Python bytecode files"
