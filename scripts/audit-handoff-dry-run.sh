#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
source "${script_dir}/common.sh"

runtime_root="$(resolve_runtime_root)"
python_bin="${runtime_root}/.venv/bin/python"

if [[ ! -x "${python_bin}" ]]; then
  die "缺少 Python 运行入口：${python_bin}；请先运行 bash scripts/bootstrap.sh --with-dev"
fi

cd "${runtime_root}"
exec "${python_bin}" "${runtime_root}/scripts/audit-handoff-dry-run.py" "$@"
