#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
source "${script_dir}/common.sh"

cd "${skill_root}"

failures_file="$(mktemp)"
trap 'rm -f "${failures_file}"' EXIT

record_failure() {
  printf '%s\n' "$1" >> "${failures_file}"
}

assert_manual_workflow() {
  local workflow_file="$1"
  local workflow_name="$2"

  if [[ ! -f "${workflow_file}" ]]; then
    record_failure "${workflow_name}: 缺少 ${workflow_file}"
    return
  fi
  if ! grep -q '^  workflow_dispatch:' "${workflow_file}"; then
    record_failure "${workflow_name}: 必须只通过 workflow_dispatch 手动触发"
  fi
  if grep -Eq '^  (push|pull_request|schedule):' "${workflow_file}"; then
    record_failure "${workflow_name}: 不允许 push/pull_request/schedule 自动触发"
  fi
}

assert_contains() {
  local file="$1"
  local text="$2"
  local message="$3"

  if [[ ! -f "${file}" ]]; then
    record_failure "${message}: 缺少 ${file}"
    return
  fi
  if ! grep -Fq "${text}" "${file}"; then
    record_failure "${message}: ${file} 未包含 ${text}"
  fi
}

assert_manual_workflow ".github/workflows/acceptance.yml" "FateCat Acceptance"
assert_manual_workflow ".github/workflows/container.yml" "FateCat Container"

assert_contains "infra/huggingface-space/Dockerfile" "FATE_RECORDS_ENABLED=0" "HF 免费 Space 必须默认关闭记录存储"
assert_contains "infra/huggingface-space/README.md" "免费公开 Space 默认不保存用户记录" "HF README 必须说明默认不保存"
assert_contains "docs/deployment/huggingface-space.md" "Duplicate this Space" "自助部署文档必须包含网页复制路径"
assert_contains "docs/deployment/huggingface-space.md" "GitHub + HF 云端自部署" "自助部署文档必须包含 GitHub + HF 路径"
assert_contains "README.md" "FateCat 不会自动把排盘输入或报告发送给 Gemini" "README 必须说明 Gemini 隐私边界"
assert_contains "domains/experience-delivery/services/fatecat-delivery/src/report_jobs.py" "默认仍使用单进程内存队列" "报告任务队列必须明确默认单进程边界"
assert_contains "domains/experience-delivery/services/fatecat-delivery/src/report_jobs.py" "SQLite backend 不是分布式队列" "SQLite job store 必须明确非分布式边界"

if [[ -s "${failures_file}" ]]; then
  echo "public release policy failed:" >&2
  sed 's/^/  - /' "${failures_file}" >&2
  exit 1
fi

echo "public release policy ok"
