#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
source "${script_dir}/common.sh"

runtime_root="$(resolve_runtime_root)"
exec "${runtime_root}/.venv/bin/python" \
  "${runtime_root}/domains/experience-delivery/services/fatecat-delivery/start.py" \
  api
