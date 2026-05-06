#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
source "${script_dir}/common.sh"

bundle_root="${1:-}"

usage() {
  cat <<'EOF'
用法:
  bash scripts/check-export-hygiene.sh <exported-skill-root>

说明:
  - 检查导出 skill 包中是否混入本地运行态、缓存、字节码、secret 或 Git 元数据。
EOF
}

if [[ -z "${bundle_root}" ]]; then
  usage >&2
  exit 2
fi

[[ -d "${bundle_root}" ]] || die "导出目录不存在: ${bundle_root}"
bundle_root="$(cd "${bundle_root}" && pwd)"

violations_file="$(mktemp)"
trap 'rm -f "${violations_file}"' EXIT

find "${bundle_root}" \
  \( \
    -path "${bundle_root}/.git" -o \
    -path "${bundle_root}/.history" -o \
    -path "${bundle_root}/.venv" -o \
    -path "${bundle_root}/venv" -o \
    -path "${bundle_root}/.pytest_cache" -o \
    -path "${bundle_root}/.ruff_cache" -o \
    -path "${bundle_root}/.mypy_cache" -o \
    -path "${bundle_root}/output" -o \
    -path "${bundle_root}/scripts/project/.venv" -o \
    -path "${bundle_root}/scripts/project/.pytest_cache" -o \
    -path "${bundle_root}/scripts/project/.ruff_cache" -o \
    -path "${bundle_root}/scripts/project/.mypy_cache" -o \
    -path "${bundle_root}/scripts/project/assets/config/.env" -o \
    -path "${bundle_root}/scripts/project/assets/data/classics/raw" -o \
    -path "${bundle_root}/scripts/project/assets/data/calendar/solar_terms/raw" -o \
    -path "${bundle_root}/scripts/project/modules/telegram/output" -o \
    -name '.env' -o \
    -name '.env.local' -o \
    -name '*.local' -o \
    -name '*.log' -o \
    -name '.DS_Store' -o \
    -name 'node_modules' -o \
    -name '__pycache__' -o \
    -name '*.pyc' -o \
    -name '*.pyo' -o \
    -name '*.db' -o \
    -name '*.sqlite' -o \
    -name '*.sqlite3' \
  \) -print > "${violations_file}"

if [[ -s "${violations_file}" ]]; then
  echo "导出包卫生检查失败，发现不应分发的文件或目录:" >&2
  sed 's/^/  - /' "${violations_file}" >&2
  exit 1
fi

echo "export hygiene ok: ${bundle_root}"
