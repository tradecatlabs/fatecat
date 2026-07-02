#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
source "${script_dir}/common.sh"

profile="quick"
output_dir="/tmp/fatecat-local-ci-$(date +%Y%m%d%H%M%S)"
image="fatecat-delivery:local"
container_port="${FATECAT_CONTAINER_SMOKE_PORT:-8002}"
skip_container_build="0"
with_dev="0"
api_url=""
require_live_bot="0"

usage() {
  cat <<'EOF'
用法:
  bash scripts/local-ci.sh [--profile quick|full|container|public-service|all]
                           [--output <dir>] [--with-dev]
                           [--image <name:tag>] [--port <port>] [--skip-container-build]
                           [--api-url <url>] [--require-live-bot]

说明:
  - 本脚本是本地 CI/CD 调度入口，不调用 GitHub Actions，不 watch 远端 Acceptance。
  - quick：本地快速门禁，覆盖 shell 语法、pure smoke、vendor、数据供应链、结构/卫生/隐私、ruff、format check、mypy、关键回归测试。
  - full：本地完整验收，复用 scripts/acceptance.sh --with-dev。
  - container：真实 Docker 容器 build + smoke；--skip-container-build 可复用已有镜像。
  - public-service：公网服务静态准入门禁；可追加 --api-url 和 --require-live-bot 做外部验收。
  - all：按 quick -> full -> container -> public-service 顺序执行。
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --profile)
      [[ $# -ge 2 ]] || usage_error "--profile 缺少参数"
      profile="$2"
      shift 2
      ;;
    --output)
      [[ $# -ge 2 ]] || usage_error "--output 缺少参数"
      output_dir="$2"
      shift 2
      ;;
    --with-dev)
      with_dev="1"
      shift
      ;;
    --image)
      [[ $# -ge 2 ]] || usage_error "--image 缺少参数"
      image="$2"
      shift 2
      ;;
    --port)
      [[ $# -ge 2 ]] || usage_error "--port 缺少参数"
      container_port="$2"
      shift 2
      ;;
    --skip-container-build)
      skip_container_build="1"
      shift
      ;;
    --api-url)
      [[ $# -ge 2 ]] || usage_error "--api-url 缺少参数"
      api_url="${2%/}"
      shift 2
      ;;
    --require-live-bot)
      require_live_bot="1"
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

case "${profile}" in
  quick|full|container|public-service|all)
    ;;
  *)
    usage_error "--profile 只支持 quick、full、container、public-service 或 all"
    ;;
esac

case "${container_port}" in
  ''|*[!0-9]*)
    usage_error "--port 必须是正整数"
    ;;
esac

runtime_root="$(resolve_runtime_root)"
mkdir -p "${output_dir}"
output_dir="$(cd "${output_dir}" && pwd)"
python_bin="${runtime_root}/.venv/bin/python"
started_at="$(date -Iseconds)"
summary_finalized="0"

run_step() {
  local name="$1"
  shift
  echo "[local-ci] ${name}"
  "$@"
}

ensure_dev_runtime() {
  local dev_missing="0"
  if [[ ! -x "${python_bin}" ]]; then
    dev_missing="1"
  elif ! "${python_bin}" -m pytest --version >/dev/null 2>&1 \
    || ! "${python_bin}" -m ruff --version >/dev/null 2>&1 \
    || ! "${python_bin}" -m mypy --version >/dev/null 2>&1; then
    dev_missing="1"
  fi

  if runtime_bootstrap_required "${runtime_root}" || [[ "${with_dev}" == "1" || "${dev_missing}" == "1" ]]; then
    local bootstrap_args=()
    if [[ "${with_dev}" == "1" || "${dev_missing}" == "1" ]]; then
      bootstrap_args+=(--with-dev)
    fi
    run_step "bootstrap runtime" bash "${script_dir}/bootstrap.sh" "${bootstrap_args[@]}"
    runtime_root="$(resolve_runtime_root)"
    python_bin="${runtime_root}/.venv/bin/python"
  fi
}

run_quick() {
  ensure_dev_runtime

  run_step "shell syntax" bash -n "${script_dir}"/*.sh
  run_step "pure preflight smoke" bash "${script_dir}/preflight.sh" \
    --mode pure \
    --bootstrap \
    --smoke \
    --output-file "${output_dir}/preflight-pure.json" \
    --pretty
  run_step "clean runtime before vendor health" bash "${script_dir}/clean-runtime.sh"
  run_step "vendor health" bash "${script_dir}/vendor-health.sh"
  run_step "structure gate" bash "${script_dir}/check-structure.sh"
  run_step "source hygiene" bash "${script_dir}/check-source-hygiene.sh"
  run_step "secret scan" bash "${script_dir}/secret-scan.sh" --output-json "${output_dir}/secret-scan.json"
  run_step "production security gate" bash "${script_dir}/production-security-gate.sh" \
    --output-json "${output_dir}/production-security-gate.json"
  run_step "privacy fixtures" bash "${script_dir}/check-privacy-fixtures.sh"
  run_step "public release policy" bash "${script_dir}/check-public-release-policy.sh"
  run_step "developer docs smoke" bash "${script_dir}/developer-docs-smoke.sh" \
    --output-json "${output_dir}/developer-docs-smoke.json" \
    --openapi-json "${output_dir}/openapi.json"
  run_step "provider lifecycle gate" bash "${script_dir}/provider-lifecycle-gate.sh" \
    --output-json "${output_dir}/provider-lifecycle-gate.json"
  run_step "provider dependency smoke" bash "${script_dir}/provider-dependency-smoke.sh" \
    --output-json "${output_dir}/provider-dependency-smoke.json"
  run_step "observability SLO gate" bash "${script_dir}/observability-slo-gate.sh" \
    --output-json "${output_dir}/observability-slo-gate.json"
  run_step "observability trace SLO smoke" bash "${script_dir}/observability-trace-slo-smoke.sh" \
    --output-json "${output_dir}/observability-trace-slo-smoke.json"
  run_step "bazi ziwei L4 golden smoke" bash "${script_dir}/bazi-ziwei-l4-golden-smoke.sh" \
    --profile quick \
    --output-json "${output_dir}/bazi-ziwei-l4-golden-smoke.json"
  run_step "data supply chain gate" bash "${script_dir}/data-supply-chain-gate.sh" \
    --output-json "${output_dir}/data-supply-chain-gate.json"
  run_step "release artifacts" bash "${script_dir}/release-artifacts.sh" \
    --output-dir "${output_dir}/release-artifacts" \
    --summary-json "${output_dir}/release-artifacts-summary.json"
  run_step "evaluation dashboard smoke" bash "${script_dir}/evaluation-dashboard-smoke.sh" \
    --output-dir "${output_dir}/evaluation-dashboard-smoke"
  run_step "webhook smoke" bash "${script_dir}/webhook-smoke.sh" \
    --output-json "${output_dir}/webhook-smoke.json"
  run_step "webhook outbox smoke" bash "${script_dir}/webhook-outbox-smoke.sh" \
    --output-json "${output_dir}/webhook-outbox-smoke.json"
  run_step "report job restart recovery smoke" bash "${script_dir}/report-job-restart-recovery-smoke.sh" \
    --output-json "${output_dir}/report-job-restart-recovery-smoke.json"
  run_step "live release gate contract" bash "${script_dir}/live-release-gate.sh" \
    --sbom-path "${output_dir}/release-artifacts/sbom.cyclonedx.json" \
    --provenance-path "${output_dir}/release-artifacts/provenance.slsa.json" \
    --output-json "${output_dir}/live-release-gate.json"
  run_step "ruff check" env RUFF_CACHE_DIR="${RUFF_CACHE_DIR:-/tmp/fatecat-ruff-cache}" \
    "${python_bin}" -m ruff check "${runtime_root}"
  run_step "ruff format check" env RUFF_CACHE_DIR="${RUFF_CACHE_DIR:-/tmp/fatecat-ruff-cache}" \
    "${python_bin}" -m ruff format --check "${runtime_root}"
  echo "[local-ci] mypy fate_core"
  (
    cd "${runtime_root}"
    "${python_bin}" -m mypy -p fate_core
  )
  echo "[local-ci] focused regression tests"
  (
    cd "${runtime_root}"
    "${python_bin}" -m pytest -q \
      tests/regression/test_api_contracts.py \
      tests/regression/test_bazi_ziwei_l4_golden_smoke.py \
      tests/regression/test_branding_support.py \
      tests/regression/test_data_supply_chain_gate.py \
      tests/regression/test_developer_docs_smoke.py \
      tests/regression/test_evaluation_dashboard.py \
      tests/regression/test_evaluation_history_diff.py \
      tests/regression/test_evaluation_runner.py \
      tests/regression/test_observability_smoke.py \
      tests/regression/test_observability_trace_slo.py \
      tests/regression/test_provider_dependency_smoke.py \
      tests/regression/test_provider_lifecycle_gate.py \
      tests/regression/test_production_security_gate.py \
      tests/regression/test_secret_scan.py \
      tests/regression/test_security_smoke.py \
      tests/regression/test_web_html.py \
      tests/regression/test_webhook_smoke.py \
      tests/regression/test_webhook_outbox_smoke.py \
      tests/regression/test_report_job_restart_recovery_smoke.py \
      tests/regression/test_live_release_gate.py \
      tests/regression/test_container_release_evidence.py \
      tests/regression/test_release_artifacts.py \
      tests/regression/test_rollback_drill.py
  )
  run_step "git whitespace check" git -C "${runtime_root}" diff --check
}

run_full() {
  run_step "local full acceptance" bash "${script_dir}/acceptance.sh" \
    --with-dev \
    --output "${output_dir}/acceptance"
}

run_container() {
  local container_args=(--image "${image}" --port "${container_port}")
  if [[ "${skip_container_build}" == "1" ]]; then
    container_args+=(--skip-build)
  fi
  run_step "container smoke" bash "${script_dir}/container-smoke.sh" "${container_args[@]}"
}

run_public_service() {
  local readiness_args=(--skip-bootstrap)
  if [[ -n "${api_url}" ]]; then
    readiness_args+=(--api-url "${api_url}")
  fi
  if [[ "${require_live_bot}" == "1" ]]; then
    readiness_args+=(--require-live-bot)
  fi

  echo "[local-ci] public-service readiness"
  (
    export FATE_CORS_ALLOW_ORIGINS="${FATE_CORS_ALLOW_ORIGINS:-https://fatecat.tradecatlabs.example}"
    export FATE_RECORDS_ENABLED="${FATE_RECORDS_ENABLED:-0}"
    export FATE_DEPLOYMENT_REPLICAS="${FATE_DEPLOYMENT_REPLICAS:-1}"
    export FATE_RATE_LIMIT_BACKEND="${FATE_RATE_LIMIT_BACKEND:-gateway}"
    export FATE_EDGE_BODY_LIMIT_ENABLED="${FATE_EDGE_BODY_LIMIT_ENABLED:-1}"
    export FATE_TRUST_PROXY_HEADERS="${FATE_TRUST_PROXY_HEADERS:-1}"
    export FATE_ENABLE_HSTS="${FATE_ENABLE_HSTS:-1}"
    bash "${script_dir}/production-readiness.sh" "${readiness_args[@]}"
  )
}

write_summary() {
  local exit_code="${1:-0}"
  if [[ "${summary_finalized}" == "1" ]]; then
    return 0
  fi
  summary_finalized="1"
  set +e

  local status="failed"
  if [[ "${exit_code}" == "0" ]]; then
    status="passed"
  fi

  local summary_file="${output_dir}/summary.txt"
  local summary_json="${output_dir}/summary.json"
  local finished_at
  finished_at="$(date -Iseconds)"
  local commit
  commit="$(git -C "${runtime_root}" rev-parse --verify HEAD 2>/dev/null || true)"
  local branch
  branch="$(git -C "${runtime_root}" rev-parse --abbrev-ref HEAD 2>/dev/null || true)"
  local dirty_count
  dirty_count="$(git -C "${runtime_root}" status --porcelain 2>/dev/null | wc -l | tr -d ' ')"
  local untracked_count
  untracked_count="$(git -C "${runtime_root}" status --porcelain 2>/dev/null | grep -c '^??' || true)"

  {
    printf 'profile=%s\n' "${profile}"
    printf 'status=%s\n' "${status}"
    printf 'exit_code=%s\n' "${exit_code}"
    printf 'runtime_root=%s\n' "${runtime_root}"
    printf 'commit=%s\n' "${commit}"
    printf 'started_at=%s\n' "${started_at}"
    printf 'finished_at=%s\n' "${finished_at}"
    printf 'summary_json=%s\n' "${summary_json}"
  } > "${summary_file}"

  local summary_python="${python_bin}"
  if [[ ! -x "${summary_python}" ]]; then
    summary_python="python3"
  fi

  FATE_LOCAL_CI_SUMMARY_JSON="${summary_json}" \
  FATE_LOCAL_CI_SCHEMA_VERSION="1" \
  FATE_LOCAL_CI_KIND="fatecat.local_ci_summary" \
  FATE_LOCAL_CI_PROFILE="${profile}" \
  FATE_LOCAL_CI_STATUS="${status}" \
  FATE_LOCAL_CI_EXIT_CODE="${exit_code}" \
  FATE_LOCAL_CI_STARTED_AT="${started_at}" \
  FATE_LOCAL_CI_FINISHED_AT="${finished_at}" \
  FATE_LOCAL_CI_RUNTIME_ROOT="${runtime_root}" \
  FATE_LOCAL_CI_COMMIT="${commit}" \
  FATE_LOCAL_CI_BRANCH="${branch}" \
  FATE_LOCAL_CI_DIRTY_COUNT="${dirty_count}" \
  FATE_LOCAL_CI_UNTRACKED_COUNT="${untracked_count}" \
  FATE_LOCAL_CI_SUMMARY_TEXT="${summary_file}" \
  FATE_LOCAL_CI_PREFLIGHT_PURE="${output_dir}/preflight-pure.json" \
  FATE_LOCAL_CI_SECRET_SCAN="${output_dir}/secret-scan.json" \
  FATE_LOCAL_CI_PRODUCTION_SECURITY_GATE="${output_dir}/production-security-gate.json" \
  FATE_LOCAL_CI_DEVELOPER_DOCS_SMOKE="${output_dir}/developer-docs-smoke.json" \
  FATE_LOCAL_CI_OPENAPI="${output_dir}/openapi.json" \
  FATE_LOCAL_CI_PROVIDER_LIFECYCLE_GATE="${output_dir}/provider-lifecycle-gate.json" \
  FATE_LOCAL_CI_PROVIDER_DEPENDENCY_SMOKE="${output_dir}/provider-dependency-smoke.json" \
  FATE_LOCAL_CI_OBSERVABILITY_SLO_GATE="${output_dir}/observability-slo-gate.json" \
  FATE_LOCAL_CI_OBSERVABILITY_TRACE_SLO_SMOKE="${output_dir}/observability-trace-slo-smoke.json" \
  FATE_LOCAL_CI_BAZI_ZIWEI_L4_GOLDEN_SMOKE="${output_dir}/bazi-ziwei-l4-golden-smoke.json" \
  FATE_LOCAL_CI_DATA_SUPPLY_CHAIN_GATE="${output_dir}/data-supply-chain-gate.json" \
  FATE_LOCAL_CI_RELEASE_ARTIFACTS="${output_dir}/release-artifacts" \
  FATE_LOCAL_CI_RELEASE_ARTIFACTS_SUMMARY="${output_dir}/release-artifacts-summary.json" \
  FATE_LOCAL_CI_EVALUATION_DASHBOARD_SMOKE="${output_dir}/evaluation-dashboard-smoke" \
  FATE_LOCAL_CI_WEBHOOK_SMOKE="${output_dir}/webhook-smoke.json" \
  FATE_LOCAL_CI_WEBHOOK_OUTBOX_SMOKE="${output_dir}/webhook-outbox-smoke.json" \
  FATE_LOCAL_CI_REPORT_JOB_RESTART_RECOVERY_SMOKE="${output_dir}/report-job-restart-recovery-smoke.json" \
  FATE_LOCAL_CI_LIVE_RELEASE_GATE="${output_dir}/live-release-gate.json" \
  "${summary_python}" - <<'PY'
import json
import os
from pathlib import Path


def env(name: str) -> str:
    return os.environ.get(name, "")


payload = {
    "schemaVersion": int(env("FATE_LOCAL_CI_SCHEMA_VERSION") or "1"),
    "kind": env("FATE_LOCAL_CI_KIND"),
    "profile": env("FATE_LOCAL_CI_PROFILE"),
    "status": env("FATE_LOCAL_CI_STATUS"),
    "exitCode": int(env("FATE_LOCAL_CI_EXIT_CODE") or "1"),
    "startedAt": env("FATE_LOCAL_CI_STARTED_AT"),
    "finishedAt": env("FATE_LOCAL_CI_FINISHED_AT"),
    "runtimeRoot": env("FATE_LOCAL_CI_RUNTIME_ROOT"),
    "commit": env("FATE_LOCAL_CI_COMMIT"),
    "git": {
        "branch": env("FATE_LOCAL_CI_BRANCH"),
        "dirtyCount": int(env("FATE_LOCAL_CI_DIRTY_COUNT") or "0"),
        "untrackedCount": int(env("FATE_LOCAL_CI_UNTRACKED_COUNT") or "0"),
    },
    "artifacts": {
        "summaryText": env("FATE_LOCAL_CI_SUMMARY_TEXT"),
        "preflightPure": env("FATE_LOCAL_CI_PREFLIGHT_PURE"),
        "secretScan": env("FATE_LOCAL_CI_SECRET_SCAN"),
        "productionSecurityGate": env("FATE_LOCAL_CI_PRODUCTION_SECURITY_GATE"),
        "developerDocsSmoke": env("FATE_LOCAL_CI_DEVELOPER_DOCS_SMOKE"),
        "openapi": env("FATE_LOCAL_CI_OPENAPI"),
        "providerLifecycleGate": env("FATE_LOCAL_CI_PROVIDER_LIFECYCLE_GATE"),
        "providerDependencySmoke": env("FATE_LOCAL_CI_PROVIDER_DEPENDENCY_SMOKE"),
        "observabilitySloGate": env("FATE_LOCAL_CI_OBSERVABILITY_SLO_GATE"),
        "observabilityTraceSloSmoke": env("FATE_LOCAL_CI_OBSERVABILITY_TRACE_SLO_SMOKE"),
        "baziZiweiL4GoldenSmoke": env("FATE_LOCAL_CI_BAZI_ZIWEI_L4_GOLDEN_SMOKE"),
        "dataSupplyChainGate": env("FATE_LOCAL_CI_DATA_SUPPLY_CHAIN_GATE"),
        "releaseArtifacts": env("FATE_LOCAL_CI_RELEASE_ARTIFACTS"),
        "releaseArtifactsSummary": env("FATE_LOCAL_CI_RELEASE_ARTIFACTS_SUMMARY"),
        "evaluationDashboardSmoke": env("FATE_LOCAL_CI_EVALUATION_DASHBOARD_SMOKE"),
        "webhookSmoke": env("FATE_LOCAL_CI_WEBHOOK_SMOKE"),
        "webhookOutboxSmoke": env("FATE_LOCAL_CI_WEBHOOK_OUTBOX_SMOKE"),
        "reportJobRestartRecoverySmoke": env("FATE_LOCAL_CI_REPORT_JOB_RESTART_RECOVERY_SMOKE"),
        "liveReleaseGate": env("FATE_LOCAL_CI_LIVE_RELEASE_GATE"),
    },
    "privacyBoundary": "只记录命令产物路径、commit 和状态，不复制测试日志全文或用户报告内容。",
    "limitations": [
        "该 summary 只证明本地 local-ci profile 执行结果，不代表远端 GitHub Actions 通过。",
        "该 summary 不证明真实生产 API、HF Space、Telegram Bot、container digest 或 rollback drill 已完成。",
    ],
}

Path(env("FATE_LOCAL_CI_SUMMARY_JSON")).write_text(
    json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
)
PY

  if [[ "${status}" == "passed" ]]; then
    echo "[local-ci] done profile=${profile} evidence=${output_dir}"
  else
    echo "[local-ci] failed profile=${profile} evidence=${output_dir} exit_code=${exit_code}" >&2
  fi
}

trap 'rc=$?; write_summary "${rc}"' EXIT

case "${profile}" in
  quick)
    run_quick
    ;;
  full)
    run_full
    ;;
  container)
    run_container
    ;;
  public-service)
    run_public_service
    ;;
  all)
    run_quick
    run_full
    run_container
    run_public_service
    ;;
esac
