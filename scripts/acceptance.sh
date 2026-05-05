#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
source "${script_dir}/common.sh"

with_dev="0"
skip_strict="0"
skip_delivery="0"
skip_export="0"
delivery_target="both"
output_dir="/tmp/fatecat-acceptance"
strict_validator="${HOME}/.codex/skills/auto-skill/scripts/validate-skill.sh"

usage() {
  cat <<'EOF'
用法:
  bash scripts/acceptance.sh [--with-dev] [--skip-strict] [--skip-delivery] [--skip-export]
                             [--delivery-target api|bot|both] [--output <dir>]

说明:
  - 统一执行单-skill 仓库的验收链：shell 语法 -> strict skill 校验 -> pure preflight -> 全量 pytest -> 静态门禁 -> API/Bot delivery smoke -> 导出包 smoke
  - 默认输出目录为 /tmp/fatecat-acceptance
  - 默认 --delivery-target both，同时验证 API 与 Bot dry-run；本地快速循环可显式指定 api 或 bot
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --with-dev)
      with_dev="1"
      shift
      ;;
    --skip-strict)
      skip_strict="1"
      shift
      ;;
    --skip-delivery)
      skip_delivery="1"
      shift
      ;;
    --skip-export)
      skip_export="1"
      shift
      ;;
    --delivery-target)
      [[ $# -ge 2 ]] || usage_error "--delivery-target 缺少参数"
      delivery_target="$2"
      shift 2
      ;;
    --output)
      [[ $# -ge 2 ]] || usage_error "--output 缺少参数"
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

case "${delivery_target}" in
  api|bot|both)
    ;;
  *)
    usage_error "--delivery-target 只支持 api、bot 或 both"
    ;;
esac

runtime_root="$(resolve_runtime_root)"
mkdir -p "${output_dir}"
output_dir="$(cd "${output_dir}" && pwd)"

bootstrap_args=()
if [[ "${with_dev}" == "1" ]]; then
  bootstrap_args+=(--with-dev)
fi

echo "[acceptance] bootstrap"
bash "${script_dir}/bootstrap.sh" "${bootstrap_args[@]}"

echo "[acceptance] shell syntax"
bash -n "${script_dir}"/*.sh

if [[ "${skip_strict}" != "1" ]]; then
  if [[ -x "${strict_validator}" ]]; then
    echo "[acceptance] strict skill validate"
    "${strict_validator}" "${skill_root}" --strict
  else
    echo "[acceptance] skip strict: 未找到 ${strict_validator}"
  fi
fi

echo "[acceptance] pure preflight smoke"
bash "${script_dir}/preflight.sh" \
  --mode pure \
  --bootstrap \
  --smoke \
  --output-file "${output_dir}/preflight-pure.json" \
  --pretty

echo "[acceptance] pytest"
"${runtime_root}/.venv/bin/python" -m pytest -q \
  "${runtime_root}/tests" \
  "${runtime_root}/modules/telegram/tests"

echo "[acceptance] ruff"
RUFF_CACHE_DIR="${RUFF_CACHE_DIR:-/tmp/fatecat-ruff-cache}" \
  "${runtime_root}/.venv/bin/python" -m ruff check "${runtime_root}"
RUFF_CACHE_DIR="${RUFF_CACHE_DIR:-/tmp/fatecat-ruff-cache}" \
  "${runtime_root}/.venv/bin/python" -m ruff format --check "${runtime_root}"

echo "[acceptance] mypy fate_core"
(
  cd "${runtime_root}"
  .venv/bin/python -m mypy -p fate_core
)

if [[ "${skip_delivery}" == "1" ]]; then
  echo "[acceptance] skip delivery: 用户显式要求跳过"
else
  delivery_targets=()
  if [[ "${delivery_target}" == "both" ]]; then
    delivery_targets=(api bot)
  else
    delivery_targets=("${delivery_target}")
  fi

  for target in "${delivery_targets[@]}"; do
    echo "[acceptance] delivery smoke (${target})"
    bash "${script_dir}/delivery-smoke.sh" \
      --target "${target}" \
      --response-file "${output_dir}/delivery-${target}.json"
  done
fi

if [[ "${skip_export}" == "1" ]]; then
  echo "[acceptance] skip export: 用户显式要求跳过"
else
  export_parent="${output_dir}/export"
  export_skill_root="${export_parent}/fatecat"
  echo "[acceptance] export lite"
  rm -rf "${export_parent}"
  bash "${script_dir}/export-runtime.sh" --output-parent "${export_parent}" --mode lite

  if [[ "${skip_strict}" != "1" && -x "${strict_validator}" ]]; then
    echo "[acceptance] strict skill validate exported bundle"
    "${strict_validator}" "${export_skill_root}" --strict
  fi

  echo "[acceptance] exported pure preflight smoke"
  (
    cd "${export_skill_root}"
    bash scripts/preflight.sh \
      --mode pure \
      --bootstrap \
      --smoke \
      --output-file "${output_dir}/export-preflight-pure.json" \
      --pretty
  )
fi

echo "[acceptance] done: ${output_dir}"
