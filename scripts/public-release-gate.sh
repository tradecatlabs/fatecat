#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
source "${script_dir}/common.sh"

output_dir="/tmp/fatecat-public-release-$(date +%Y%m%d%H%M%S)"
api_url=""
skip_local_ci="0"
skip_delivery_smoke="0"
smoke_port="${FATECAT_PUBLIC_RELEASE_SMOKE_PORT:-8001}"
with_container="${FATECAT_PUBLIC_RELEASE_WITH_CONTAINER:-0}"
container_image="${FATECAT_PUBLIC_RELEASE_CONTAINER_IMAGE:-fatecat-delivery:public-release}"
container_port="${FATECAT_PUBLIC_RELEASE_CONTAINER_PORT:-8021}"
container_skip_build="${FATECAT_PUBLIC_RELEASE_CONTAINER_SKIP_BUILD:-0}"

usage() {
  cat <<'EOF'
用法:
  bash scripts/public-release-gate.sh [--output <dir>] [--api-url <url>]
                                      [--skip-local-ci] [--skip-delivery-smoke]

说明:
  - 面向公开 Web 工作台发布前的本地门禁，不调用 GitHub Actions。
  - 默认执行 local-ci quick、发布策略检查、API smoke 和生产静态准入。
  - 传入 --api-url 时，会额外验证线上 /health、/ready、/metrics。
  - 可用 FATECAT_PUBLIC_RELEASE_SMOKE_PORT 覆盖本地 delivery smoke 端口。
  - 可用 FATECAT_PUBLIC_RELEASE_WITH_CONTAINER=1 生成本地 container release evidence。
  - 可用 FATECAT_PUBLIC_RELEASE_CONTAINER_SKIP_BUILD=1 复用已有镜像做 container smoke。
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --output)
      [[ $# -ge 2 ]] || usage_error "--output 缺少参数"
      output_dir="$2"
      shift 2
      ;;
    --api-url)
      [[ $# -ge 2 ]] || usage_error "--api-url 缺少参数"
      api_url="${2%/}"
      shift 2
      ;;
    --skip-local-ci)
      skip_local_ci="1"
      shift
      ;;
    --skip-delivery-smoke)
      skip_delivery_smoke="1"
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

runtime_root="$(resolve_runtime_root)"
mkdir -p "${output_dir}"
output_dir="$(cd "${output_dir}" && pwd)"
local_ci_summary=""

run_step() {
  local name="$1"
  shift
  echo "[public-release] ${name}"
  "$@"
}

if [[ "${skip_local_ci}" != "1" ]]; then
  run_step "local-ci quick" bash "${script_dir}/local-ci.sh" \
    --profile quick \
    --output "${output_dir}/local-ci-quick"
  local_ci_summary="${output_dir}/local-ci-quick/summary.json"
fi

run_step "GEO query set gate" "${python_bin}" "${script_dir}/geo-query-set-gate.py"
run_step "public release policy" bash "${script_dir}/check-public-release-policy.sh"
run_step "public client package smoke" "${python_bin}" "${script_dir}/public-client-package-smoke.py" \
  --output "${output_dir}/public-client-package-smoke"

public_skill_parent="${output_dir}/public-skill"
run_step "public skill export" bash "${script_dir}/export-runtime.sh" \
  --output-parent "${public_skill_parent}" \
  --mode lite
run_step "public skill supply-chain policy" bash "${script_dir}/check-export-hygiene.sh" \
  "${public_skill_parent}/fatecat" \
  --public

if [[ "${skip_delivery_smoke}" != "1" ]]; then
  run_step "delivery web smoke" env FATE_RECORDS_ENABLED=0 bash "${script_dir}/delivery-smoke.sh" \
    --target api \
    --port "${smoke_port}" \
    --response-file "${output_dir}/health.json" \
    --log-file "${output_dir}/delivery-smoke.log"
fi

readiness_args=(--skip-bootstrap)
if [[ -n "${api_url}" ]]; then
  readiness_args+=(--api-url "${api_url}")
  run_step "GEO discovery audit" "${python_bin}" "${script_dir}/geo-audit.py" \
    --base-url "${api_url}" \
    --output-json "${output_dir}/geo-discovery-audit.json"
fi

run_step "production readiness" env \
  FATE_CORS_ALLOW_ORIGINS="${FATE_CORS_ALLOW_ORIGINS:-https://tradecatlabs-fatecat.hf.space}" \
  FATE_RECORDS_ENABLED="${FATE_RECORDS_ENABLED:-0}" \
  FATE_DEPLOYMENT_REPLICAS="${FATE_DEPLOYMENT_REPLICAS:-1}" \
  FATE_RATE_LIMIT_BACKEND="${FATE_RATE_LIMIT_BACKEND:-gateway}" \
  FATE_EDGE_BODY_LIMIT_ENABLED="${FATE_EDGE_BODY_LIMIT_ENABLED:-1}" \
  FATE_TRUST_PROXY_HEADERS="${FATE_TRUST_PROXY_HEADERS:-1}" \
  FATE_ENABLE_HSTS="${FATE_ENABLE_HSTS:-1}" \
  bash "${script_dir}/production-readiness.sh" "${readiness_args[@]}"

run_step "release artifacts" bash "${script_dir}/release-artifacts.sh" \
  --output-dir "${output_dir}/release-artifacts" \
  --summary-json "${output_dir}/release-artifacts-summary.json"

rollback_drill_args=(
  --output-json "${output_dir}/rollback-drill.json"
  --release-artifacts-dir "${output_dir}/release-artifacts"
)
if [[ -n "${local_ci_summary}" ]]; then
  rollback_drill_args+=(--local-ci-summary "${local_ci_summary}")
fi

run_step "rollback drill evidence" bash "${script_dir}/rollback-drill.sh" "${rollback_drill_args[@]}"

container_evidence=""
if [[ "${with_container}" == "1" ]]; then
  container_evidence="${output_dir}/container-release-evidence.json"
  container_evidence_args=(--image "${container_image}" --port "${container_port}" --output-json "${container_evidence}")
  if [[ "${container_skip_build}" == "1" ]]; then
    container_evidence_args+=(--skip-build)
  fi
  run_step "container release evidence" bash "${script_dir}/container-release-evidence.sh" \
    "${container_evidence_args[@]}"
fi

release_gate_args=(--output-json "${output_dir}/live-release-gate.json")
release_gate_args+=(--sbom-path "${output_dir}/release-artifacts/sbom.cyclonedx.json")
release_gate_args+=(--provenance-path "${output_dir}/release-artifacts/provenance.slsa.json")
release_gate_args+=(--rollback-evidence-path "${output_dir}/rollback-drill.json")
if [[ -n "${container_evidence}" ]]; then
  release_gate_args+=(--container-evidence-path "${container_evidence}")
fi
if [[ -n "${local_ci_summary}" ]]; then
  release_gate_args+=(--local-ci-summary "${local_ci_summary}")
fi
if [[ -n "${api_url}" ]]; then
  release_gate_args+=(--api-url "${api_url}")
fi

run_step "live release evidence gate" bash "${script_dir}/live-release-gate.sh" "${release_gate_args[@]}"

{
  printf 'runtime_root=%s\n' "${runtime_root}"
  printf 'commit=%s\n' "$(git -C "${runtime_root}" rev-parse --verify HEAD 2>/dev/null || true)"
  printf 'api_url=%s\n' "${api_url:-not-provided}"
  printf 'smoke_port=%s\n' "${smoke_port}"
  printf 'local_ci_summary=%s\n' "${local_ci_summary:-not-provided}"
  printf 'release_artifacts=%s\n' "${output_dir}/release-artifacts"
  printf 'rollback_drill=%s\n' "${output_dir}/rollback-drill.json"
  printf 'container_evidence=%s\n' "${container_evidence:-not-provided}"
  printf 'container_skip_build=%s\n' "${container_skip_build}"
  printf 'live_release_gate=%s\n' "${output_dir}/live-release-gate.json"
  printf 'timestamp=%s\n' "$(date -Iseconds)"
} > "${output_dir}/summary.txt"

echo "[public-release] done evidence=${output_dir}"
