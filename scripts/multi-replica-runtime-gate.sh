#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "${SCRIPT_DIR}/.." && pwd)"

python_bin="${REPO_ROOT}/.venv/bin/python"
if [[ ! -x "${python_bin}" ]]; then
  python_bin="python3"
fi

exec "${python_bin}" "${SCRIPT_DIR}/multi-replica-runtime-gate.py" "$@"
