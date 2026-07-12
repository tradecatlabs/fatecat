#!/usr/bin/env bash
set -euo pipefail

export PYTHONDONTWRITEBYTECODE=1

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
source "${script_dir}/common.sh"

mode="pure"
do_bootstrap="0"
with_dev="0"
do_smoke="0"
pretty="0"
input_json=""
input_file=""
output_file=""

usage() {
  cat <<'EOF'
用法:
  bash scripts/preflight.sh [--mode pure|delivery] [--bootstrap] [--with-dev] [--smoke]
                            [--input-json <json> | --input-file <file>]
                            [--output-file <file>] [--pretty]

说明:
  - 统一执行 FateCat 的前置检查链路：bootstrap -> health -> (可选) pure-analysis 烟雾验证
  - 默认 mode 为 pure
  - --smoke 只允许在 pure 模式下使用
  - 若未传入 --output-file 且开启 --smoke，会自动写入 /tmp/fatecat-preflight-<timestamp>.json
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --mode)
      [[ $# -ge 2 ]] || usage_error "--mode 缺少参数"
      mode="${2:-}"
      shift 2
      ;;
    --bootstrap)
      do_bootstrap="1"
      shift
      ;;
    --with-dev)
      with_dev="1"
      shift
      ;;
    --smoke)
      do_smoke="1"
      shift
      ;;
    --input-json)
      [[ $# -ge 2 ]] || usage_error "--input-json 缺少参数"
      input_json="${2:-}"
      shift 2
      ;;
    --input-file)
      [[ $# -ge 2 ]] || usage_error "--input-file 缺少参数"
      input_file="${2:-}"
      shift 2
      ;;
    --output-file)
      [[ $# -ge 2 ]] || usage_error "--output-file 缺少参数"
      output_file="${2:-}"
      shift 2
      ;;
    --pretty)
      pretty="1"
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

case "${mode}" in
  pure|delivery)
    ;;
  *)
    usage_error "--mode 只支持 pure 或 delivery"
    ;;
esac

if [[ "${do_smoke}" == "1" && "${mode}" != "pure" ]]; then
  die "--smoke 只允许在 pure 模式下使用"
fi

if [[ -n "${input_json}" && -n "${input_file}" ]]; then
  die "--input-json 与 --input-file 不能同时使用"
fi

if [[ -n "${input_file}" && ! -f "${input_file}" ]]; then
  die "输入文件不存在：${input_file}"
fi

runtime_root="$(resolve_runtime_root)"

if [[ "${do_bootstrap}" == "1" || "${with_dev}" == "1" ]] || runtime_bootstrap_required "${runtime_root}"; then
  bootstrap_args=()
  if [[ "${with_dev}" == "1" ]]; then
    bootstrap_args+=(--with-dev)
  fi
  bash "${script_dir}/bootstrap.sh" "${bootstrap_args[@]}"
fi

echo "[preflight] health mode=${mode}"
health_args=(--mode "${mode}" --json)
if [[ "${pretty}" == "1" ]]; then
  health_args+=(--pretty)
fi
bash "${script_dir}/health.sh" "${health_args[@]}"

if [[ "${do_smoke}" == "0" ]]; then
  echo "[preflight] done: health only"
  exit 0
fi

if [[ -z "${output_file}" ]]; then
  output_file="/tmp/fatecat-preflight-$(date +%Y%m%d%H%M%S).json"
fi
ensure_parent_dir "${output_file}"

pure_args=(--output-file "${output_file}")
if [[ "${pretty}" == "1" ]]; then
  pure_args+=(--pretty)
fi

if [[ -n "${input_json}" ]]; then
  pure_args+=(--input-json "${input_json}")
elif [[ -n "${input_file}" ]]; then
  pure_args+=(--input-file "${input_file}")
else
  pure_args+=(
    --input-json
    '{"birthDateTime":"1990-01-01 08:00:00","gender":"男","longitude":116.4074,"latitude":39.9042,"birthPlace":"北京市","name":"preflight-sample"}'
  )
fi

echo "[preflight] smoke pure-analysis -> ${output_file}"
bash "${script_dir}/pure-analysis.sh" "${pure_args[@]}"
echo "[preflight] done: output=${output_file}"
