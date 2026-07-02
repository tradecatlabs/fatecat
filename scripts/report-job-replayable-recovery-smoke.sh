#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
runtime_root="$(cd "${script_dir}/.." && pwd)"
python_bin="${PYTHON:-}"

if [[ -z "${python_bin}" ]]; then
  if [[ -x "${runtime_root}/.venv/bin/python" ]]; then
    python_bin="${runtime_root}/.venv/bin/python"
  else
    python_bin="python3"
  fi
fi

exec "${python_bin}" "${runtime_root}/scripts/report-job-replayable-recovery-smoke.py" "$@"
