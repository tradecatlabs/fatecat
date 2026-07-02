#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
source "${script_dir}/common.sh"

runtime_root="$(resolve_runtime_root)"
python_bin="${runtime_root}/.venv/bin/python"

if [[ ! -x "${python_bin}" ]]; then
  die "缺少 Python 运行入口：${python_bin}；请先运行 bash scripts/bootstrap.sh --with-dev"
fi

output_dir="${runtime_root}/infra/runtime/local-state/exports/evaluations/dashboard-smoke"

usage() {
  cat <<'EOF'
用法:
  bash scripts/evaluation-dashboard-smoke.sh [--output-dir <dir>]

说明:
  使用 dry-run EvaluationRun summary 验证 dashboard renderer，不执行重型评测，不访问公网。
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --output-dir)
      [[ $# -ge 2 ]] || usage_error "--output-dir 缺少参数"
      output_dir="$2"
      shift 2
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

mkdir -p "${output_dir}"
summary_json="${output_dir}/summary-dry-run.json"
dashboard_html="${output_dir}/index.html"
dashboard_json="${output_dir}/dashboard-summary.json"

bash "${script_dir}/run-evaluations.sh" \
  --all-local-required \
  --dry-run \
  --output-json "${summary_json}"

bash "${script_dir}/evaluation-dashboard.sh" \
  --summary-json "${summary_json}" \
  --output-html "${dashboard_html}" \
  --output-json "${dashboard_json}"

grep -q "FateCat Evaluation Dashboard" "${dashboard_html}"
grep -q "run.local_ci_quick" "${dashboard_html}"
grep -q "Privacy Boundary" "${dashboard_html}"

printf '{"status":"passed","summary":"%s","dashboard":"%s"}\n' "${summary_json}" "${dashboard_html}"
