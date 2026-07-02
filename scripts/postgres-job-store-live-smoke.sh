#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
runtime_root="$(cd "${script_dir}/.." && pwd)"
python_bin="${runtime_root}/.venv/bin/python"

if [[ ! -x "${python_bin}" ]]; then
  python_bin="python3"
fi

exec "${python_bin}" "${runtime_root}/scripts/postgres-job-store-live-smoke.py" "$@"
