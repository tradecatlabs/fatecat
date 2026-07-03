#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
source "${script_dir}/common.sh"

usage() {
  cat <<'EOF'
用法:
  bash scripts/capability-cli.sh <capability_id> [fatecat capability 参数...]

示例:
  bash scripts/capability-cli.sh bazi --input-json '{"birthDateTime":"1990-01-01 08:00:00","gender":"male","longitude":116.4074,"latitude":39.9042,"birthPlace":"北京市"}' --pretty

说明:
  - 该脚本是根级 capability CLI 入口，只转发到 fate_core.cli capability。
  - 测算逻辑必须继续由 CapabilityExecutor 和 provider registry 执行。
EOF
}

if [[ $# -lt 1 ]]; then
  usage >&2
  exit 2
fi

runtime_root="$(resolve_runtime_root)"
python_bin="${runtime_root}/.venv/bin/python"

if [[ ! -x "${python_bin}" ]]; then
  die "缺少 Python 运行入口：${python_bin}；请先运行 bash scripts/bootstrap.sh --with-dev"
fi

export PYTHONPATH="${runtime_root}/domains/fate-analysis/services/fate-core/src${PYTHONPATH:+:${PYTHONPATH}}"
cd "${runtime_root}"
exec "${python_bin}" -m fate_core.cli capability "$@"
