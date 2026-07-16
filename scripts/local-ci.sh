#!/usr/bin/env bash
set -euo pipefail

export PYTHONDONTWRITEBYTECODE=1

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
  run_step "security externalization gate" bash "${script_dir}/security-externalization-gate.sh" \
    --output-json "${output_dir}/security-externalization-gate.json"
  run_step "retention cleanup smoke" bash "${script_dir}/retention-cleanup-smoke.sh" \
    --output-json "${output_dir}/retention-cleanup-smoke.json"
  run_step "retention production cleanup staged gate" bash "${script_dir}/retention-production-cleanup-gate.sh" \
    --output-json "${output_dir}/retention-production-cleanup-gate.json"
  run_step "external secret provider gate" bash "${script_dir}/external-secret-provider-gate.sh" \
    --output-json "${output_dir}/external-secret-provider-gate.json"
  run_step "privacy fixtures" bash "${script_dir}/check-privacy-fixtures.sh"
  run_step "public release policy" bash "${script_dir}/check-public-release-policy.sh"
  run_step "developer docs smoke" bash "${script_dir}/developer-docs-smoke.sh" \
    --output-json "${output_dir}/developer-docs-smoke.json" \
    --openapi-json "${output_dir}/openapi.json"
  run_step "developer platform gate" bash "${script_dir}/developer-platform-gate.sh" \
    --output-json "${output_dir}/developer-platform-gate.json"
  run_step "developer portal gate" bash "${script_dir}/developer-portal-gate.sh" \
    --output-json "${output_dir}/developer-portal-gate.json"
  run_step "sandbox access gateway gate" bash "${script_dir}/sandbox-access-gateway-gate.sh" \
    --output-json "${output_dir}/sandbox-access-gateway-gate.json"
  run_step "CLI capability smoke" bash "${script_dir}/capability-cli-smoke.sh" \
    --output-json "${output_dir}/capability-cli-smoke.json"
  run_step "package distribution smoke" bash "${script_dir}/package-distribution-smoke.sh" \
    "${output_dir}/package-distribution-smoke"
  run_step "public client package smoke" "${python_bin}" "${script_dir}/public-client-package-smoke.py" \
    --output "${output_dir}/public-client-package-smoke"
  run_step "control plane gate" bash "${script_dir}/control-plane-gate.sh" \
    --output-json "${output_dir}/control-plane-gate.json"
  run_step "multi-surface semantic diff" bash "${script_dir}/multi-surface-semantic-diff.sh" \
    --output-json "${output_dir}/multi-surface-semantic-diff.json"
  run_step "provider lifecycle gate" bash "${script_dir}/provider-lifecycle-gate.sh" \
    --output-json "${output_dir}/provider-lifecycle-gate.json"
  run_step "provider dependency smoke" bash "${script_dir}/provider-dependency-smoke.sh" \
    --output-json "${output_dir}/provider-dependency-smoke.json"
  run_step "provider drift scanner" bash "${script_dir}/provider-drift-scanner.sh" \
    --output-json "${output_dir}/provider-drift-scanner.json"
  run_step "provider drift trend gate" bash "${script_dir}/provider-drift-trend-gate.sh" \
    --scanner-report-json "${output_dir}/provider-drift-scanner.json" \
    --output-json "${output_dir}/provider-drift-trend-gate.json"
  run_step "observability SLO gate" bash "${script_dir}/observability-slo-gate.sh" \
    --output-json "${output_dir}/observability-slo-gate.json"
  run_step "observability trace SLO smoke" bash "${script_dir}/observability-trace-slo-smoke.sh" \
    --output-json "${output_dir}/observability-trace-slo-smoke.json"
  run_step "OTel collector SLO gate" bash "${script_dir}/otel-collector-slo-gate.sh" \
    --output-json "${output_dir}/otel-collector-slo-gate.json"
  run_step "OTel backend SLO staged gate" bash "${script_dir}/otel-backend-slo-gate.sh" \
    --output-json "${output_dir}/otel-backend-slo-gate.json"
  run_step "bazi ziwei L4 golden smoke" bash "${script_dir}/bazi-ziwei-l4-golden-smoke.sh" \
    --profile quick \
    --output-json "${output_dir}/bazi-ziwei-l4-golden-smoke.json"
  run_step "core performance smoke" bash "${script_dir}/core-performance-smoke.sh" \
    --samples 3 \
    --output-json "${output_dir}/core-performance-smoke.json"
  run_step "evidence coverage trend gate" bash "${script_dir}/evidence-coverage-trend-gate.sh" \
    --output-json "${output_dir}/evidence-coverage-trend-gate.json"
  run_step "core quality corpus gate" bash "${script_dir}/core-quality-corpus-gate.sh" \
    --output-json "${output_dir}/core-quality-corpus-gate.json"
  run_step "MingLi-Bench aggregate gate" bash "${script_dir}/mingli-bench-gate.sh" \
    --year 2025 \
    --sample 5 \
    --output-json "${output_dir}/mingli-bench-gate.json"
  run_step "core quality human review gate" bash "${script_dir}/core-quality-human-review-gate.sh" \
    --output-json "${output_dir}/core-quality-human-review-gate.json"
  run_step "core quality human review bundle template" bash "${script_dir}/core-quality-human-review-bundle-template.sh" \
    --output-json "${output_dir}/core-quality-human-review-bundle-template.json" \
    --output-markdown "${output_dir}/CORE_QUALITY_HUMAN_REVIEW_BUNDLE_TEMPLATE.md"
  run_step "data supply chain gate" bash "${script_dir}/data-supply-chain-gate.sh" \
    --output-json "${output_dir}/data-supply-chain-gate.json"
  run_step "runtime backend gate" bash "${script_dir}/runtime-backend-gate.sh" \
    --output-json "${output_dir}/runtime-backend-gate.json"
  run_step "multi-replica runtime evidence assembler" bash "${script_dir}/multi-replica-runtime-evidence-assembler.sh" \
    --pending \
    --output-json "${output_dir}/multi-replica-runtime-evidence.json"
  run_step "multi-replica runtime gate" bash "${script_dir}/multi-replica-runtime-gate.sh" \
    --output-json "${output_dir}/multi-replica-runtime-gate.json"
  run_step "postgres job store dry-run" bash "${script_dir}/postgres-job-store-dry-run.sh" \
    --output-json "${output_dir}/postgres-job-store-dry-run.json"
  run_step "postgres job store live-smoke preflight" bash "${script_dir}/postgres-job-store-live-smoke.sh" \
    --allow-missing \
    --output-json "${output_dir}/postgres-job-store-live-smoke.json"
  run_step "postgres worker lease smoke preflight" bash "${script_dir}/postgres-worker-lease-smoke.sh" \
    --allow-missing \
    --output-json "${output_dir}/postgres-worker-lease-smoke.json"
  run_step "postgres job worker lease smoke preflight" bash "${script_dir}/postgres-job-worker-lease-smoke.sh" \
    --allow-missing \
    --output-json "${output_dir}/postgres-job-worker-lease-smoke.json"
  run_step "postgres external worker restart smoke preflight" bash "${script_dir}/postgres-external-worker-restart-smoke.sh" \
    --allow-missing \
    --output-json "${output_dir}/postgres-external-worker-restart-smoke.json"
  run_step "postgres worker heartbeat polling smoke preflight" bash "${script_dir}/postgres-worker-heartbeat-polling-smoke.sh" \
    --allow-missing \
    --output-json "${output_dir}/postgres-worker-heartbeat-polling-smoke.json"
  run_step "postgres public webhook live smoke preflight" bash "${script_dir}/postgres-public-webhook-live-smoke.sh" \
    --allow-missing \
    --output-json "${output_dir}/postgres-public-webhook-live-smoke.json"
  run_step "runtime proof gate" bash "${script_dir}/runtime-proof-gate.sh" \
    --public-webhook-summary "${output_dir}/postgres-public-webhook-live-smoke.json" \
    --output-json "${output_dir}/runtime-proof-gate.json"
  run_step "event contract gate" bash "${script_dir}/event-contract-gate.sh" \
    --output-json "${output_dir}/event-contract-gate.json"
  run_step "release artifacts" bash "${script_dir}/release-artifacts.sh" \
    --output-dir "${output_dir}/release-artifacts" \
    --summary-json "${output_dir}/release-artifacts-summary.json"
  run_step "rollback drill" bash "${script_dir}/rollback-drill.sh" \
    --output-json "${output_dir}/rollback-drill.json" \
    --release-artifacts-dir "${output_dir}/release-artifacts"
  run_step "current release proof local contract" bash "${script_dir}/current-release-proof.sh" \
    --skip-remote \
    --rollback-evidence-path "${output_dir}/rollback-drill.json" \
    --output-json "${output_dir}/current-release-proof.json"
  run_step "evaluation dashboard smoke" bash "${script_dir}/evaluation-dashboard-smoke.sh" \
    --output-dir "${output_dir}/evaluation-dashboard-smoke"
  run_step "evaluation trend gate smoke" bash "${script_dir}/evaluation-trend-gate-smoke.sh" \
    --output-dir "${output_dir}/evaluation-trend-gate-smoke"
  run_step "webhook smoke" bash "${script_dir}/webhook-smoke.sh" \
    --output-json "${output_dir}/webhook-smoke.json"
  run_step "webhook outbox smoke" bash "${script_dir}/webhook-outbox-smoke.sh" \
    --output-json "${output_dir}/webhook-outbox-smoke.json"
  run_step "webhook outbox redelivery smoke" bash "${script_dir}/webhook-outbox-redelivery-smoke.sh" \
    --output-json "${output_dir}/webhook-outbox-redelivery-smoke.json"
  run_step "webhook config vault smoke" bash "${script_dir}/webhook-config-vault-smoke.sh" \
    --output-json "${output_dir}/webhook-config-vault-smoke.json"
  run_step "webhook outbox lease smoke" bash "${script_dir}/webhook-outbox-lease-smoke.sh" \
    --output-json "${output_dir}/webhook-outbox-lease-smoke.json"
  run_step "report job replayable recovery smoke" bash "${script_dir}/report-job-replayable-recovery-smoke.sh" \
    --output-json "${output_dir}/report-job-replayable-recovery-smoke.json"
  run_step "report job restart recovery smoke" bash "${script_dir}/report-job-restart-recovery-smoke.sh" \
    --output-json "${output_dir}/report-job-restart-recovery-smoke.json"
  run_step "live release gate contract" bash "${script_dir}/live-release-gate.sh" \
    --sbom-path "${output_dir}/release-artifacts/sbom.cyclonedx.json" \
    --provenance-path "${output_dir}/release-artifacts/provenance.slsa.json" \
    --output-json "${output_dir}/live-release-gate.json"
  run_step "audit handoff" bash "${script_dir}/audit-handoff.sh" \
    --output-dir "${output_dir}/audit-handoff"
  run_step "audit handoff dry-run" bash "${script_dir}/audit-handoff-dry-run.sh" \
    --bundle-json "${output_dir}/audit-handoff/audit-handoff.json" \
    --bundle-markdown "${output_dir}/audit-handoff/AUDIT_HANDOFF.md" \
    --output-dir "${output_dir}/audit-dry-run"
  run_step "current audit bundle" bash "${script_dir}/current-audit-bundle.sh" \
    --output-dir "${output_dir}/current-audit-bundle" \
    --audit-handoff-json "${output_dir}/audit-handoff/audit-handoff.json" \
    --audit-handoff-markdown "${output_dir}/audit-handoff/AUDIT_HANDOFF.md" \
    --audit-dry-run-json "${output_dir}/audit-dry-run/audit-dry-run.json" \
    --current-release-proof "${output_dir}/current-release-proof.json" \
    --rollback-evidence-path "${output_dir}/rollback-drill.json" \
    --release-artifacts-dir "${output_dir}/release-artifacts" \
    --local-ci-output-dir "${output_dir}"
  run_step "external validation closure gate" bash "${script_dir}/external-validation-closure-gate.sh" \
    --pending-external-json "${output_dir}/current-audit-bundle/pending-external-validations.json" \
    --output-json "${output_dir}/external-validation-closure-gate.json"
  run_step "external validation closure work queue" bash "${script_dir}/external-validation-closure-work-queue.sh" \
    --closure-plan-json "${output_dir}/external-validation-closure-gate.json" \
    --output-json "${output_dir}/external-validation-closure-work-queue.json"
  run_step "external validation proof-ref gate" bash "${script_dir}/external-validation-proof-ref-gate.sh" \
    --work-queue-json "${output_dir}/external-validation-closure-work-queue.json" \
    --output-json "${output_dir}/external-validation-proof-ref-gate.json"
  run_step "external validation category runbooks" bash "${script_dir}/external-validation-category-runbooks.sh" \
    --work-queue-json "${output_dir}/external-validation-closure-work-queue.json" \
    --output-json "${output_dir}/external-validation-category-runbooks.json"
  run_step "external validation operator execution packet" bash "${script_dir}/external-validation-operator-execution-packet.sh" \
    --work-queue-json "${output_dir}/external-validation-closure-work-queue.json" \
    --proof-ref-gate-json "${output_dir}/external-validation-proof-ref-gate.json" \
    --category-runbooks-json "${output_dir}/external-validation-category-runbooks.json" \
    --output-json "${output_dir}/external-validation-operator-execution-packet.json"
  run_step "production live operator execution packet" bash "${script_dir}/production-live-operator-execution-packet.sh" \
    --work-queue-json "${output_dir}/external-validation-closure-work-queue.json" \
    --proof-ref-gate-json "${output_dir}/external-validation-proof-ref-gate.json" \
    --category-runbooks-json "${output_dir}/external-validation-category-runbooks.json" \
    --output-json "${output_dir}/production-live-operator-execution-packet.json"
  run_step "production live delivery evidence bundle" bash "${script_dir}/production-live-delivery-evidence-bundle.sh" \
    --work-queue-json "${output_dir}/external-validation-closure-work-queue.json" \
    --proof-ref-gate-json "${output_dir}/external-validation-proof-ref-gate.json" \
    --category-runbooks-json "${output_dir}/external-validation-category-runbooks.json" \
    --live-release-gate-json "${output_dir}/live-release-gate.json" \
    --public-webhook-json "${output_dir}/postgres-public-webhook-live-smoke.json" \
    --multi-surface-json "${output_dir}/multi-surface-semantic-diff.json" \
    --output-json "${output_dir}/production-live-delivery-evidence-bundle.json"
  run_step "external validation live proof gate" bash "${script_dir}/external-validation-live-proof-gate.sh" \
    --work-queue-json "${output_dir}/external-validation-closure-work-queue.json" \
    --proof-ref-gate-json "${output_dir}/external-validation-proof-ref-gate.json" \
    --category-runbooks-json "${output_dir}/external-validation-category-runbooks.json" \
    --live-evidence-json "${output_dir}/production-live-delivery-evidence-bundle.json" \
    --output-json "${output_dir}/external-validation-live-proof-gate.json"
  run_step "external validation closure trend dashboard" bash "${script_dir}/external-validation-closure-trend-dashboard.sh" \
    --closure-plan-json "${output_dir}/external-validation-closure-gate.json" \
    --work-queue-json "${output_dir}/external-validation-closure-work-queue.json" \
    --proof-ref-gate-json "${output_dir}/external-validation-proof-ref-gate.json" \
    --category-runbooks-json "${output_dir}/external-validation-category-runbooks.json" \
    --live-proof-gate-json "${output_dir}/external-validation-live-proof-gate.json" \
    --output-json "${output_dir}/external-validation-closure-trend-dashboard.json"
  run_step "external validation closure evidence summary" bash "${script_dir}/external-validation-closure-evidence-summary.sh" \
    --work-queue-json "${output_dir}/external-validation-closure-work-queue.json" \
    --proof-ref-gate-json "${output_dir}/external-validation-proof-ref-gate.json" \
    --category-runbooks-json "${output_dir}/external-validation-category-runbooks.json" \
    --operator-packet-json "${output_dir}/external-validation-operator-execution-packet.json" \
    --live-proof-gate-json "${output_dir}/external-validation-live-proof-gate.json" \
    --closure-trend-dashboard-json "${output_dir}/external-validation-closure-trend-dashboard.json" \
    --output-json "${output_dir}/external-validation-closure-evidence-summary.json"
  run_step "external validation issue export" bash "${script_dir}/external-validation-issue-export.sh" \
    --work-queue-json "${output_dir}/external-validation-closure-work-queue.json" \
    --category-runbooks-json "${output_dir}/external-validation-category-runbooks.json" \
    --operator-packet-json "${output_dir}/external-validation-operator-execution-packet.json" \
    --closure-evidence-summary-json "${output_dir}/external-validation-closure-evidence-summary.json" \
    --output-json "${output_dir}/external-validation-issue-export.json" \
    --output-markdown "${output_dir}/EXTERNAL_VALIDATION_ISSUE_EXPORT.md"
  run_step "external validation tracker import package" bash "${script_dir}/external-validation-tracker-import-package.sh" \
    --issue-export-json "${output_dir}/external-validation-issue-export.json" \
    --package-dir "${output_dir}/external-validation-tracker-import-package" \
    --output-json "${output_dir}/external-validation-tracker-import-package.json" \
    --output-markdown "${output_dir}/EXTERNAL_VALIDATION_TRACKER_IMPORT_PACKAGE.md"
  run_step "external validation tracker issue evidence template" bash "${script_dir}/external-validation-tracker-issue-evidence-template.sh" \
    --tracker-import-package-json "${output_dir}/external-validation-tracker-import-package.json" \
    --output-json "${output_dir}/external-validation-tracker-issue-evidence-template.json" \
    --output-markdown "${output_dir}/EXTERNAL_VALIDATION_TRACKER_ISSUE_EVIDENCE_TEMPLATE.md"
  run_step "external validation tracker issue evidence gate" bash "${script_dir}/external-validation-tracker-issue-evidence-gate.sh" \
    --tracker-import-package-json "${output_dir}/external-validation-tracker-import-package.json" \
    --output-json "${output_dir}/external-validation-tracker-issue-evidence-gate.json"
  run_step "independent audit result gate" bash "${script_dir}/independent-audit-result-gate.sh" \
    --output-json "${output_dir}/independent-audit-result-gate.json"
  run_step "measurement infrastructure certification dry-run" bash "${script_dir}/measurement-infrastructure-certification.sh" \
    --evidence-dir "${output_dir}" \
    --output-json "${output_dir}/measurement-infrastructure-certification.json"
  run_step "third-party audit rehearsal" bash "${script_dir}/third-party-audit-rehearsal.sh" \
    --current-audit-bundle-json "${output_dir}/current-audit-bundle/current-audit-bundle.json" \
    --audit-dry-run-json "${output_dir}/audit-dry-run/audit-dry-run.json" \
    --current-release-proof-json "${output_dir}/current-release-proof.json" \
    --certification-json "${output_dir}/measurement-infrastructure-certification.json" \
    --closure-evidence-summary-json "${output_dir}/external-validation-closure-evidence-summary.json" \
    --tracker-import-package-json "${output_dir}/external-validation-tracker-import-package.json" \
    --tracker-issue-evidence-template-json "${output_dir}/external-validation-tracker-issue-evidence-template.json" \
    --tracker-issue-evidence-gate-json "${output_dir}/external-validation-tracker-issue-evidence-gate.json" \
    --independent-audit-result-gate-json "${output_dir}/independent-audit-result-gate.json" \
    --output-json "${output_dir}/third-party-audit-rehearsal.json" \
    --output-markdown "${output_dir}/THIRD_PARTY_AUDIT_REHEARSAL.md"
  run_step "external evidence submission readiness audit" bash "${script_dir}/external-evidence-submission-readiness-audit.sh" \
    --work-queue-json "${output_dir}/external-validation-closure-work-queue.json" \
    --proof-ref-gate-json "${output_dir}/external-validation-proof-ref-gate.json" \
    --live-proof-gate-json "${output_dir}/external-validation-live-proof-gate.json" \
    --operator-packet-json "${output_dir}/external-validation-operator-execution-packet.json" \
    --core-quality-human-review-json "${output_dir}/core-quality-human-review-gate.json" \
    --third-party-audit-rehearsal-json "${output_dir}/third-party-audit-rehearsal.json" \
    --certification-json "${output_dir}/measurement-infrastructure-certification.json" \
    --output-json "${output_dir}/external-evidence-submission-readiness-audit.json" \
    --output-markdown "${output_dir}/EXTERNAL_EVIDENCE_SUBMISSION_READINESS_AUDIT.md"
  run_step "GEO query set gate" "${python_bin}" "${script_dir}/geo-query-set-gate.py"
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
      tests/regression/test_audit_handoff.py \
      tests/regression/test_audit_handoff_dry_run.py \
      tests/regression/test_bazi_ziwei_l4_golden_smoke.py \
      tests/regression/test_branding_support.py \
      tests/regression/test_core_quality_corpus_gate.py \
      tests/regression/test_data_supply_chain_gate.py \
      tests/regression/test_location.py \
      tests/regression/test_location_catalog.py \
      tests/regression/test_developer_docs_smoke.py \
      tests/regression/test_developer_platform_gate.py \
      tests/regression/test_developer_portal_gate.py \
      tests/regression/test_sandbox_access_gateway_gate.py \
      tests/regression/test_capability_cli_smoke.py \
      tests/regression/test_capability_protocol.py \
      tests/regression/test_monthly_performance_equivalence.py \
      tests/regression/test_multi_surface_semantic_diff.py \
      tests/regression/test_public_client_distribution.py \
      tests/regression/test_public_report_visibility.py \
      tests/regression/test_retention_cleanup.py \
      tests/regression/test_retention_production_cleanup_gate.py \
      tests/regression/test_evaluation_dashboard.py \
      tests/regression/test_evaluation_history_diff.py \
      tests/regression/test_evaluation_runner.py \
      tests/regression/test_evaluation_trend_gate.py \
      tests/regression/test_geo_discovery.py \
      tests/regression/test_external_secret_provider_gate.py \
      tests/regression/test_mingli_bench_aggregate_gate.py \
      tests/regression/test_mingli_bench_gate.py \
      tests/regression/test_core_quality_human_review_gate.py \
      tests/regression/test_observability_smoke.py \
      tests/regression/test_observability_trace_slo.py \
      tests/regression/test_otel_backend_slo_gate.py \
      tests/regression/test_evidence_coverage_trend_gate.py \
      tests/regression/test_provider_dependency_smoke.py \
      tests/regression/test_provider_lifecycle_gate.py \
      tests/regression/test_production_security_gate.py \
      tests/regression/test_runtime_backend_gate.py \
      tests/regression/test_multi_replica_runtime_evidence_assembler.py \
      tests/regression/test_multi_replica_runtime_gate.py \
      tests/regression/test_postgres_job_store_adapter.py \
      tests/regression/test_postgres_job_store_live_smoke.py \
      tests/regression/test_postgres_worker_lease_smoke.py \
      tests/regression/test_postgres_job_worker_lease_smoke.py \
      tests/regression/test_postgres_external_worker_restart_smoke.py \
      tests/regression/test_postgres_worker_heartbeat_polling_smoke.py \
      tests/regression/test_postgres_public_webhook_live_smoke.py \
      tests/regression/test_event_contract_gate.py \
      tests/regression/test_secret_scan.py \
      tests/regression/test_security_smoke.py \
      tests/regression/test_telegram_webhook.py \
      tests/regression/test_web_html.py \
      tests/regression/test_webhook_smoke.py \
      tests/regression/test_webhook_outbox_smoke.py \
      tests/regression/test_webhook_outbox_redelivery_smoke.py \
      tests/regression/test_webhook_config_vault_smoke.py \
      tests/regression/test_webhook_outbox_lease_smoke.py \
      tests/regression/test_report_job_replayable_recovery_smoke.py \
      tests/regression/test_report_job_restart_recovery_smoke.py \
      tests/regression/test_current_audit_bundle.py \
      tests/regression/test_external_validation_closure_gate.py \
      tests/regression/test_external_validation_closure_work_queue.py \
      tests/regression/test_external_validation_proof_ref_gate.py \
      tests/regression/test_external_validation_category_runbooks.py \
      tests/regression/test_external_validation_operator_execution_packet.py \
      tests/regression/test_production_live_operator_execution_packet.py \
      tests/regression/test_production_live_delivery_evidence_bundle.py \
      tests/regression/test_external_validation_live_proof_gate.py \
      tests/regression/test_external_validation_closure_trend_dashboard.py \
      tests/regression/test_external_validation_closure_evidence_summary.py \
      tests/regression/test_external_validation_issue_export.py \
      tests/regression/test_external_validation_tracker_import_package.py \
      tests/regression/test_external_validation_tracker_issue_evidence_template.py \
      tests/regression/test_external_validation_tracker_issue_evidence_gate.py \
      tests/regression/test_independent_audit_result_gate.py \
      tests/regression/test_measurement_infrastructure_certification.py \
      tests/regression/test_third_party_audit_rehearsal.py \
      tests/regression/test_external_evidence_submission_readiness_audit.py \
      tests/regression/test_current_release_proof.py \
      tests/regression/test_live_release_gate.py \
      tests/regression/test_container_release_evidence.py \
      tests/regression/test_release_artifacts.py \
      tests/regression/test_rollback_drill.py
  )
  run_step "vendor health after tests" bash "${script_dir}/vendor-health.sh"
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
  FATE_LOCAL_CI_SECURITY_EXTERNALIZATION_GATE="${output_dir}/security-externalization-gate.json" \
  FATE_LOCAL_CI_RETENTION_CLEANUP_SMOKE="${output_dir}/retention-cleanup-smoke.json" \
  FATE_LOCAL_CI_RETENTION_PRODUCTION_CLEANUP_GATE="${output_dir}/retention-production-cleanup-gate.json" \
  FATE_LOCAL_CI_EXTERNAL_SECRET_PROVIDER_GATE="${output_dir}/external-secret-provider-gate.json" \
  FATE_LOCAL_CI_DEVELOPER_DOCS_SMOKE="${output_dir}/developer-docs-smoke.json" \
  FATE_LOCAL_CI_DEVELOPER_PLATFORM_GATE="${output_dir}/developer-platform-gate.json" \
  FATE_LOCAL_CI_DEVELOPER_PORTAL_GATE="${output_dir}/developer-portal-gate.json" \
  FATE_LOCAL_CI_SANDBOX_ACCESS_GATEWAY_GATE="${output_dir}/sandbox-access-gateway-gate.json" \
  FATE_LOCAL_CI_CAPABILITY_CLI_SMOKE="${output_dir}/capability-cli-smoke.json" \
  FATE_LOCAL_CI_PACKAGE_DISTRIBUTION_SMOKE="${output_dir}/package-distribution-smoke" \
  FATE_LOCAL_CI_MULTI_SURFACE_SEMANTIC_DIFF="${output_dir}/multi-surface-semantic-diff.json" \
  FATE_LOCAL_CI_OPENAPI="${output_dir}/openapi.json" \
  FATE_LOCAL_CI_PROVIDER_LIFECYCLE_GATE="${output_dir}/provider-lifecycle-gate.json" \
  FATE_LOCAL_CI_PROVIDER_DEPENDENCY_SMOKE="${output_dir}/provider-dependency-smoke.json" \
  FATE_LOCAL_CI_PROVIDER_DRIFT_SCANNER="${output_dir}/provider-drift-scanner.json" \
  FATE_LOCAL_CI_PROVIDER_DRIFT_TREND_GATE="${output_dir}/provider-drift-trend-gate.json" \
  FATE_LOCAL_CI_OBSERVABILITY_SLO_GATE="${output_dir}/observability-slo-gate.json" \
  FATE_LOCAL_CI_OBSERVABILITY_TRACE_SLO_SMOKE="${output_dir}/observability-trace-slo-smoke.json" \
  FATE_LOCAL_CI_OTEL_COLLECTOR_SLO_GATE="${output_dir}/otel-collector-slo-gate.json" \
  FATE_LOCAL_CI_OTEL_BACKEND_SLO_GATE="${output_dir}/otel-backend-slo-gate.json" \
  FATE_LOCAL_CI_BAZI_ZIWEI_L4_GOLDEN_SMOKE="${output_dir}/bazi-ziwei-l4-golden-smoke.json" \
  FATE_LOCAL_CI_CORE_PERFORMANCE_SMOKE="${output_dir}/core-performance-smoke.json" \
  FATE_LOCAL_CI_EVIDENCE_COVERAGE_TREND_GATE="${output_dir}/evidence-coverage-trend-gate.json" \
  FATE_LOCAL_CI_CORE_QUALITY_CORPUS_GATE="${output_dir}/core-quality-corpus-gate.json" \
  FATE_LOCAL_CI_MINGLI_BENCH_GATE="${output_dir}/mingli-bench-gate.json" \
  FATE_LOCAL_CI_CORE_QUALITY_HUMAN_REVIEW_GATE="${output_dir}/core-quality-human-review-gate.json" \
  FATE_LOCAL_CI_CORE_QUALITY_HUMAN_REVIEW_BUNDLE_TEMPLATE="${output_dir}/core-quality-human-review-bundle-template.json" \
  FATE_LOCAL_CI_CORE_QUALITY_HUMAN_REVIEW_BUNDLE_TEMPLATE_MARKDOWN="${output_dir}/CORE_QUALITY_HUMAN_REVIEW_BUNDLE_TEMPLATE.md" \
  FATE_LOCAL_CI_DATA_SUPPLY_CHAIN_GATE="${output_dir}/data-supply-chain-gate.json" \
  FATE_LOCAL_CI_RUNTIME_BACKEND_GATE="${output_dir}/runtime-backend-gate.json" \
  FATE_LOCAL_CI_MULTI_REPLICA_RUNTIME_EVIDENCE="${output_dir}/multi-replica-runtime-evidence.json" \
  FATE_LOCAL_CI_MULTI_REPLICA_RUNTIME_GATE="${output_dir}/multi-replica-runtime-gate.json" \
  FATE_LOCAL_CI_POSTGRES_JOB_STORE_DRY_RUN="${output_dir}/postgres-job-store-dry-run.json" \
  FATE_LOCAL_CI_POSTGRES_JOB_STORE_LIVE_SMOKE="${output_dir}/postgres-job-store-live-smoke.json" \
  FATE_LOCAL_CI_POSTGRES_WORKER_LEASE_SMOKE="${output_dir}/postgres-worker-lease-smoke.json" \
  FATE_LOCAL_CI_POSTGRES_JOB_WORKER_LEASE_SMOKE="${output_dir}/postgres-job-worker-lease-smoke.json" \
  FATE_LOCAL_CI_POSTGRES_EXTERNAL_WORKER_RESTART_SMOKE="${output_dir}/postgres-external-worker-restart-smoke.json" \
  FATE_LOCAL_CI_POSTGRES_WORKER_HEARTBEAT_POLLING_SMOKE="${output_dir}/postgres-worker-heartbeat-polling-smoke.json" \
  FATE_LOCAL_CI_POSTGRES_PUBLIC_WEBHOOK_LIVE_SMOKE="${output_dir}/postgres-public-webhook-live-smoke.json" \
  FATE_LOCAL_CI_RUNTIME_PROOF_GATE="${output_dir}/runtime-proof-gate.json" \
  FATE_LOCAL_CI_EVENT_CONTRACT_GATE="${output_dir}/event-contract-gate.json" \
  FATE_LOCAL_CI_RELEASE_ARTIFACTS="${output_dir}/release-artifacts" \
  FATE_LOCAL_CI_RELEASE_ARTIFACTS_SUMMARY="${output_dir}/release-artifacts-summary.json" \
  FATE_LOCAL_CI_ROLLBACK_DRILL="${output_dir}/rollback-drill.json" \
  FATE_LOCAL_CI_CURRENT_RELEASE_PROOF="${output_dir}/current-release-proof.json" \
  FATE_LOCAL_CI_EVALUATION_DASHBOARD_SMOKE="${output_dir}/evaluation-dashboard-smoke" \
  FATE_LOCAL_CI_EVALUATION_TREND_GATE_SMOKE="${output_dir}/evaluation-trend-gate-smoke" \
  FATE_LOCAL_CI_WEBHOOK_SMOKE="${output_dir}/webhook-smoke.json" \
  FATE_LOCAL_CI_WEBHOOK_OUTBOX_SMOKE="${output_dir}/webhook-outbox-smoke.json" \
  FATE_LOCAL_CI_WEBHOOK_OUTBOX_REDELIVERY_SMOKE="${output_dir}/webhook-outbox-redelivery-smoke.json" \
  FATE_LOCAL_CI_WEBHOOK_CONFIG_VAULT_SMOKE="${output_dir}/webhook-config-vault-smoke.json" \
  FATE_LOCAL_CI_WEBHOOK_OUTBOX_LEASE_SMOKE="${output_dir}/webhook-outbox-lease-smoke.json" \
  FATE_LOCAL_CI_REPORT_JOB_REPLAYABLE_RECOVERY_SMOKE="${output_dir}/report-job-replayable-recovery-smoke.json" \
  FATE_LOCAL_CI_REPORT_JOB_RESTART_RECOVERY_SMOKE="${output_dir}/report-job-restart-recovery-smoke.json" \
  FATE_LOCAL_CI_LIVE_RELEASE_GATE="${output_dir}/live-release-gate.json" \
  FATE_LOCAL_CI_AUDIT_HANDOFF="${output_dir}/audit-handoff" \
  FATE_LOCAL_CI_AUDIT_DRY_RUN="${output_dir}/audit-dry-run" \
  FATE_LOCAL_CI_CURRENT_AUDIT_BUNDLE="${output_dir}/current-audit-bundle" \
  FATE_LOCAL_CI_EXTERNAL_VALIDATION_CLOSURE_GATE="${output_dir}/external-validation-closure-gate.json" \
  FATE_LOCAL_CI_EXTERNAL_VALIDATION_CLOSURE_WORK_QUEUE="${output_dir}/external-validation-closure-work-queue.json" \
  FATE_LOCAL_CI_EXTERNAL_VALIDATION_PROOF_REF_GATE="${output_dir}/external-validation-proof-ref-gate.json" \
  FATE_LOCAL_CI_EXTERNAL_VALIDATION_CATEGORY_RUNBOOKS="${output_dir}/external-validation-category-runbooks.json" \
  FATE_LOCAL_CI_EXTERNAL_VALIDATION_OPERATOR_EXECUTION_PACKET="${output_dir}/external-validation-operator-execution-packet.json" \
  FATE_LOCAL_CI_PRODUCTION_LIVE_OPERATOR_EXECUTION_PACKET="${output_dir}/production-live-operator-execution-packet.json" \
  FATE_LOCAL_CI_PRODUCTION_LIVE_DELIVERY_EVIDENCE_BUNDLE="${output_dir}/production-live-delivery-evidence-bundle.json" \
  FATE_LOCAL_CI_EXTERNAL_VALIDATION_LIVE_PROOF_GATE="${output_dir}/external-validation-live-proof-gate.json" \
  FATE_LOCAL_CI_EXTERNAL_VALIDATION_CLOSURE_TREND_DASHBOARD="${output_dir}/external-validation-closure-trend-dashboard.json" \
  FATE_LOCAL_CI_EXTERNAL_VALIDATION_CLOSURE_EVIDENCE_SUMMARY="${output_dir}/external-validation-closure-evidence-summary.json" \
  FATE_LOCAL_CI_EXTERNAL_VALIDATION_ISSUE_EXPORT="${output_dir}/external-validation-issue-export.json" \
  FATE_LOCAL_CI_EXTERNAL_VALIDATION_ISSUE_EXPORT_MARKDOWN="${output_dir}/EXTERNAL_VALIDATION_ISSUE_EXPORT.md" \
  FATE_LOCAL_CI_EXTERNAL_VALIDATION_TRACKER_IMPORT_PACKAGE="${output_dir}/external-validation-tracker-import-package.json" \
  FATE_LOCAL_CI_EXTERNAL_VALIDATION_TRACKER_IMPORT_PACKAGE_DIR="${output_dir}/external-validation-tracker-import-package" \
  FATE_LOCAL_CI_EXTERNAL_VALIDATION_TRACKER_IMPORT_PACKAGE_MARKDOWN="${output_dir}/EXTERNAL_VALIDATION_TRACKER_IMPORT_PACKAGE.md" \
  FATE_LOCAL_CI_EXTERNAL_VALIDATION_TRACKER_ISSUE_EVIDENCE_TEMPLATE="${output_dir}/external-validation-tracker-issue-evidence-template.json" \
  FATE_LOCAL_CI_EXTERNAL_VALIDATION_TRACKER_ISSUE_EVIDENCE_TEMPLATE_MARKDOWN="${output_dir}/EXTERNAL_VALIDATION_TRACKER_ISSUE_EVIDENCE_TEMPLATE.md" \
  FATE_LOCAL_CI_EXTERNAL_VALIDATION_TRACKER_ISSUE_EVIDENCE_GATE="${output_dir}/external-validation-tracker-issue-evidence-gate.json" \
  FATE_LOCAL_CI_INDEPENDENT_AUDIT_RESULT_GATE="${output_dir}/independent-audit-result-gate.json" \
  FATE_LOCAL_CI_MEASUREMENT_INFRASTRUCTURE_CERTIFICATION="${output_dir}/measurement-infrastructure-certification.json" \
  FATE_LOCAL_CI_THIRD_PARTY_AUDIT_REHEARSAL="${output_dir}/third-party-audit-rehearsal.json" \
  FATE_LOCAL_CI_THIRD_PARTY_AUDIT_REHEARSAL_MARKDOWN="${output_dir}/THIRD_PARTY_AUDIT_REHEARSAL.md" \
  FATE_LOCAL_CI_EXTERNAL_EVIDENCE_SUBMISSION_READINESS_AUDIT="${output_dir}/external-evidence-submission-readiness-audit.json" \
  FATE_LOCAL_CI_EXTERNAL_EVIDENCE_SUBMISSION_READINESS_AUDIT_MARKDOWN="${output_dir}/EXTERNAL_EVIDENCE_SUBMISSION_READINESS_AUDIT.md" \
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
        "securityExternalizationGate": env("FATE_LOCAL_CI_SECURITY_EXTERNALIZATION_GATE"),
        "retentionCleanupSmoke": env("FATE_LOCAL_CI_RETENTION_CLEANUP_SMOKE"),
        "retentionProductionCleanupGate": env("FATE_LOCAL_CI_RETENTION_PRODUCTION_CLEANUP_GATE"),
        "externalSecretProviderGate": env("FATE_LOCAL_CI_EXTERNAL_SECRET_PROVIDER_GATE"),
        "developerDocsSmoke": env("FATE_LOCAL_CI_DEVELOPER_DOCS_SMOKE"),
        "developerPlatformGate": env("FATE_LOCAL_CI_DEVELOPER_PLATFORM_GATE"),
        "developerPortalGate": env("FATE_LOCAL_CI_DEVELOPER_PORTAL_GATE"),
        "sandboxAccessGatewayGate": env("FATE_LOCAL_CI_SANDBOX_ACCESS_GATEWAY_GATE"),
        "capabilityCliSmoke": env("FATE_LOCAL_CI_CAPABILITY_CLI_SMOKE"),
        "packageDistributionSmoke": env("FATE_LOCAL_CI_PACKAGE_DISTRIBUTION_SMOKE"),
        "multiSurfaceSemanticDiff": env("FATE_LOCAL_CI_MULTI_SURFACE_SEMANTIC_DIFF"),
        "openapi": env("FATE_LOCAL_CI_OPENAPI"),
        "providerLifecycleGate": env("FATE_LOCAL_CI_PROVIDER_LIFECYCLE_GATE"),
        "providerDependencySmoke": env("FATE_LOCAL_CI_PROVIDER_DEPENDENCY_SMOKE"),
        "providerDriftScanner": env("FATE_LOCAL_CI_PROVIDER_DRIFT_SCANNER"),
        "providerDriftTrendGate": env("FATE_LOCAL_CI_PROVIDER_DRIFT_TREND_GATE"),
        "observabilitySloGate": env("FATE_LOCAL_CI_OBSERVABILITY_SLO_GATE"),
        "observabilityTraceSloSmoke": env("FATE_LOCAL_CI_OBSERVABILITY_TRACE_SLO_SMOKE"),
        "otelCollectorSloGate": env("FATE_LOCAL_CI_OTEL_COLLECTOR_SLO_GATE"),
        "otelBackendSloGate": env("FATE_LOCAL_CI_OTEL_BACKEND_SLO_GATE"),
        "baziZiweiL4GoldenSmoke": env("FATE_LOCAL_CI_BAZI_ZIWEI_L4_GOLDEN_SMOKE"),
        "corePerformanceSmoke": env("FATE_LOCAL_CI_CORE_PERFORMANCE_SMOKE"),
        "evidenceCoverageTrendGate": env("FATE_LOCAL_CI_EVIDENCE_COVERAGE_TREND_GATE"),
        "coreQualityCorpusGate": env("FATE_LOCAL_CI_CORE_QUALITY_CORPUS_GATE"),
        "mingliBenchGate": env("FATE_LOCAL_CI_MINGLI_BENCH_GATE"),
        "coreQualityHumanReviewGate": env("FATE_LOCAL_CI_CORE_QUALITY_HUMAN_REVIEW_GATE"),
        "coreQualityHumanReviewBundleTemplate": env("FATE_LOCAL_CI_CORE_QUALITY_HUMAN_REVIEW_BUNDLE_TEMPLATE"),
        "coreQualityHumanReviewBundleTemplateMarkdown": env(
            "FATE_LOCAL_CI_CORE_QUALITY_HUMAN_REVIEW_BUNDLE_TEMPLATE_MARKDOWN"
        ),
        "dataSupplyChainGate": env("FATE_LOCAL_CI_DATA_SUPPLY_CHAIN_GATE"),
        "runtimeBackendGate": env("FATE_LOCAL_CI_RUNTIME_BACKEND_GATE"),
        "multiReplicaRuntimeEvidence": env("FATE_LOCAL_CI_MULTI_REPLICA_RUNTIME_EVIDENCE"),
        "multiReplicaRuntimeGate": env("FATE_LOCAL_CI_MULTI_REPLICA_RUNTIME_GATE"),
        "postgresJobStoreDryRun": env("FATE_LOCAL_CI_POSTGRES_JOB_STORE_DRY_RUN"),
        "postgresJobStoreLiveSmoke": env("FATE_LOCAL_CI_POSTGRES_JOB_STORE_LIVE_SMOKE"),
        "postgresWorkerLeaseSmoke": env("FATE_LOCAL_CI_POSTGRES_WORKER_LEASE_SMOKE"),
        "postgresJobWorkerLeaseSmoke": env("FATE_LOCAL_CI_POSTGRES_JOB_WORKER_LEASE_SMOKE"),
        "postgresExternalWorkerRestartSmoke": env("FATE_LOCAL_CI_POSTGRES_EXTERNAL_WORKER_RESTART_SMOKE"),
        "postgresWorkerHeartbeatPollingSmoke": env("FATE_LOCAL_CI_POSTGRES_WORKER_HEARTBEAT_POLLING_SMOKE"),
        "postgresPublicWebhookLiveSmoke": env("FATE_LOCAL_CI_POSTGRES_PUBLIC_WEBHOOK_LIVE_SMOKE"),
        "eventContractGate": env("FATE_LOCAL_CI_EVENT_CONTRACT_GATE"),
        "releaseArtifacts": env("FATE_LOCAL_CI_RELEASE_ARTIFACTS"),
        "releaseArtifactsSummary": env("FATE_LOCAL_CI_RELEASE_ARTIFACTS_SUMMARY"),
        "rollbackDrill": env("FATE_LOCAL_CI_ROLLBACK_DRILL"),
        "currentReleaseProof": env("FATE_LOCAL_CI_CURRENT_RELEASE_PROOF"),
        "evaluationDashboardSmoke": env("FATE_LOCAL_CI_EVALUATION_DASHBOARD_SMOKE"),
        "evaluationTrendGateSmoke": env("FATE_LOCAL_CI_EVALUATION_TREND_GATE_SMOKE"),
        "webhookSmoke": env("FATE_LOCAL_CI_WEBHOOK_SMOKE"),
        "webhookOutboxSmoke": env("FATE_LOCAL_CI_WEBHOOK_OUTBOX_SMOKE"),
        "webhookOutboxRedeliverySmoke": env("FATE_LOCAL_CI_WEBHOOK_OUTBOX_REDELIVERY_SMOKE"),
        "webhookConfigVaultSmoke": env("FATE_LOCAL_CI_WEBHOOK_CONFIG_VAULT_SMOKE"),
        "webhookOutboxLeaseSmoke": env("FATE_LOCAL_CI_WEBHOOK_OUTBOX_LEASE_SMOKE"),
        "reportJobReplayableRecoverySmoke": env("FATE_LOCAL_CI_REPORT_JOB_REPLAYABLE_RECOVERY_SMOKE"),
        "reportJobRestartRecoverySmoke": env("FATE_LOCAL_CI_REPORT_JOB_RESTART_RECOVERY_SMOKE"),
        "liveReleaseGate": env("FATE_LOCAL_CI_LIVE_RELEASE_GATE"),
        "auditHandoff": env("FATE_LOCAL_CI_AUDIT_HANDOFF"),
        "auditDryRun": env("FATE_LOCAL_CI_AUDIT_DRY_RUN"),
        "currentAuditBundle": env("FATE_LOCAL_CI_CURRENT_AUDIT_BUNDLE"),
        "externalValidationClosureGate": env("FATE_LOCAL_CI_EXTERNAL_VALIDATION_CLOSURE_GATE"),
        "externalValidationClosureWorkQueue": env("FATE_LOCAL_CI_EXTERNAL_VALIDATION_CLOSURE_WORK_QUEUE"),
        "externalValidationProofRefGate": env("FATE_LOCAL_CI_EXTERNAL_VALIDATION_PROOF_REF_GATE"),
        "externalValidationCategoryRunbooks": env("FATE_LOCAL_CI_EXTERNAL_VALIDATION_CATEGORY_RUNBOOKS"),
        "externalValidationOperatorExecutionPacket": env("FATE_LOCAL_CI_EXTERNAL_VALIDATION_OPERATOR_EXECUTION_PACKET"),
        "productionLiveOperatorExecutionPacket": env("FATE_LOCAL_CI_PRODUCTION_LIVE_OPERATOR_EXECUTION_PACKET"),
        "productionLiveDeliveryEvidenceBundle": env("FATE_LOCAL_CI_PRODUCTION_LIVE_DELIVERY_EVIDENCE_BUNDLE"),
        "externalValidationLiveProofGate": env("FATE_LOCAL_CI_EXTERNAL_VALIDATION_LIVE_PROOF_GATE"),
        "externalValidationClosureTrendDashboard": env("FATE_LOCAL_CI_EXTERNAL_VALIDATION_CLOSURE_TREND_DASHBOARD"),
        "externalValidationClosureEvidenceSummary": env(
            "FATE_LOCAL_CI_EXTERNAL_VALIDATION_CLOSURE_EVIDENCE_SUMMARY"
        ),
        "externalValidationIssueExport": env("FATE_LOCAL_CI_EXTERNAL_VALIDATION_ISSUE_EXPORT"),
        "externalValidationIssueExportMarkdown": env("FATE_LOCAL_CI_EXTERNAL_VALIDATION_ISSUE_EXPORT_MARKDOWN"),
        "externalValidationTrackerImportPackage": env(
            "FATE_LOCAL_CI_EXTERNAL_VALIDATION_TRACKER_IMPORT_PACKAGE"
        ),
        "externalValidationTrackerImportPackageDir": env(
            "FATE_LOCAL_CI_EXTERNAL_VALIDATION_TRACKER_IMPORT_PACKAGE_DIR"
        ),
        "externalValidationTrackerImportPackageMarkdown": env(
            "FATE_LOCAL_CI_EXTERNAL_VALIDATION_TRACKER_IMPORT_PACKAGE_MARKDOWN"
        ),
        "externalValidationTrackerIssueEvidenceTemplate": env(
            "FATE_LOCAL_CI_EXTERNAL_VALIDATION_TRACKER_ISSUE_EVIDENCE_TEMPLATE"
        ),
        "externalValidationTrackerIssueEvidenceTemplateMarkdown": env(
            "FATE_LOCAL_CI_EXTERNAL_VALIDATION_TRACKER_ISSUE_EVIDENCE_TEMPLATE_MARKDOWN"
        ),
        "externalValidationTrackerIssueEvidenceGate": env(
            "FATE_LOCAL_CI_EXTERNAL_VALIDATION_TRACKER_ISSUE_EVIDENCE_GATE"
        ),
        "independentAuditResultGate": env("FATE_LOCAL_CI_INDEPENDENT_AUDIT_RESULT_GATE"),
        "measurementInfrastructureCertification": env("FATE_LOCAL_CI_MEASUREMENT_INFRASTRUCTURE_CERTIFICATION"),
        "thirdPartyAuditRehearsal": env("FATE_LOCAL_CI_THIRD_PARTY_AUDIT_REHEARSAL"),
        "thirdPartyAuditRehearsalMarkdown": env("FATE_LOCAL_CI_THIRD_PARTY_AUDIT_REHEARSAL_MARKDOWN"),
        "externalEvidenceSubmissionReadinessAudit": env(
            "FATE_LOCAL_CI_EXTERNAL_EVIDENCE_SUBMISSION_READINESS_AUDIT"
        ),
        "externalEvidenceSubmissionReadinessAuditMarkdown": env(
            "FATE_LOCAL_CI_EXTERNAL_EVIDENCE_SUBMISSION_READINESS_AUDIT_MARKDOWN"
        ),
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
