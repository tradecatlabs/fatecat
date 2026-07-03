#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
source "${script_dir}/common.sh"

runtime_root="$(resolve_runtime_root)"
python_bin="${runtime_root}/.venv/bin/python"

if [[ ! -x "${python_bin}" ]]; then
  python_bin="python3"
fi

exec "${python_bin}" "${script_dir}/measurement-infrastructure-certification.py" "$@"
