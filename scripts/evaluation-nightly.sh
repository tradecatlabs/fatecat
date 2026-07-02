#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
source "${script_dir}/common.sh"

runtime_root="$(resolve_runtime_root)"
python_bin="${runtime_root}/.venv/bin/python"

if [[ ! -x "${python_bin}" ]]; then
  die "缺少 Python 运行入口：${python_bin}；请先运行 bash scripts/bootstrap.sh --with-dev"
fi

timestamp="$(date -u +%Y%m%dT%H%M%SZ)"
output_dir="${runtime_root}/infra/runtime/local-state/exports/evaluations/nightly/${timestamp}"
history_dir="${runtime_root}/infra/runtime/local-state/exports/evaluations/history"
timeout_seconds="900"
allow_reference_repo="0"

usage() {
  cat <<'EOF'
用法:
  bash scripts/evaluation-nightly.sh [--output-dir <dir>] [--history-dir <dir>]
                                     [--timeout-seconds <seconds>] [--allow-reference-repo]

说明:
  执行本地 releaseRequired EvaluationRun，记录 history/latest，若存在旧 latest 则生成 diff，
  并始终尝试渲染静态 HTML dashboard。默认不执行 requires_reference_repo 的可选 benchmark。
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --output-dir)
      [[ $# -ge 2 ]] || usage_error "--output-dir 缺少参数"
      output_dir="$2"
      shift 2
      ;;
    --history-dir)
      [[ $# -ge 2 ]] || usage_error "--history-dir 缺少参数"
      history_dir="$2"
      shift 2
      ;;
    --timeout-seconds)
      [[ $# -ge 2 ]] || usage_error "--timeout-seconds 缺少参数"
      timeout_seconds="$2"
      shift 2
      ;;
    --allow-reference-repo)
      allow_reference_repo="1"
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

case "${timeout_seconds}" in
  ''|*[!0-9]*)
    usage_error "--timeout-seconds 必须是正整数"
    ;;
esac

mkdir -p "${output_dir}" "${history_dir}"
summary_json="${output_dir}/summary.json"
baseline_json="${output_dir}/baseline.json"
diff_json="${output_dir}/diff.json"
dashboard_html="${output_dir}/dashboard.html"
dashboard_json="${output_dir}/dashboard-summary.json"

has_baseline="0"
if [[ -s "${history_dir}/latest.json" ]]; then
  cp "${history_dir}/latest.json" "${baseline_json}"
  has_baseline="1"
fi

run_args=(
  --all-local-required
  --record-history
  --history-dir "${history_dir}"
  --timeout-seconds "${timeout_seconds}"
  --output-json "${summary_json}"
)
if [[ "${allow_reference_repo}" == "1" ]]; then
  run_args+=(--allow-reference-repo)
fi

set +e
bash "${script_dir}/run-evaluations.sh" "${run_args[@]}"
evaluation_status=$?
set -e

diff_status=0
dashboard_args=(--summary-json "${summary_json}" --output-html "${dashboard_html}" --output-json "${dashboard_json}")
if [[ "${has_baseline}" == "1" && -s "${summary_json}" ]]; then
  set +e
  bash "${script_dir}/compare-evaluations.sh" \
    --baseline-json "${baseline_json}" \
    --current-json "${summary_json}" \
    --output-json "${diff_json}"
  diff_status=$?
  set -e
  if [[ -s "${diff_json}" ]]; then
    dashboard_args+=(--diff-json "${diff_json}")
  fi
fi

if [[ -s "${summary_json}" ]]; then
  bash "${script_dir}/evaluation-dashboard.sh" "${dashboard_args[@]}"
fi

printf '{"evaluationStatus":%s,"diffStatus":%s,"outputDir":"%s"}\n' \
  "${evaluation_status}" "${diff_status}" "${output_dir}"

if [[ "${evaluation_status}" -ne 0 ]]; then
  exit "${evaluation_status}"
fi
exit "${diff_status}"
