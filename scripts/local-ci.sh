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
  - quick：本地快速门禁，覆盖 shell 语法、pure smoke、vendor、结构/卫生/隐私、ruff、format check、mypy、关键回归测试。
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
  run_step "privacy fixtures" bash "${script_dir}/check-privacy-fixtures.sh"
  run_step "public release policy" bash "${script_dir}/check-public-release-policy.sh"
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
      tests/regression/test_branding_support.py \
      tests/regression/test_web_html.py
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
  local summary_file="${output_dir}/summary.txt"
  {
    printf 'profile=%s\n' "${profile}"
    printf 'runtime_root=%s\n' "${runtime_root}"
    printf 'commit=%s\n' "$(git -C "${runtime_root}" rev-parse --verify HEAD 2>/dev/null || true)"
    printf 'timestamp=%s\n' "$(date -Iseconds)"
  } > "${summary_file}"
  echo "[local-ci] done profile=${profile} evidence=${output_dir}"
}

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

write_summary
