#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
source "${script_dir}/common.sh"

space_id="${FATECAT_HF_SPACE_ID:-tradecatlabs/fatecat}"
bundle_dir="${FATECAT_HF_BUNDLE_DIR:-/tmp/fatecat-hf-space-$(date +%Y%m%d%H%M%S)}"
commit_message="${FATECAT_HF_COMMIT_MESSAGE:-deploy FateCat HF Space}"
create_repo="1"
upload_repo="1"
private_flag="--no-private"
allow_auth_mismatch="0"
prune_remote="0"
token_value=""

usage() {
  cat <<'EOF'
用法:
  bash scripts/hf-space-deploy.sh [--space tradecatlabs/fatecat]
                                  [--bundle-dir /tmp/fatecat-hf-space]
                                  [--commit-message <msg>]
                                  [--token <hf-token>]
                                  [--private]
                                  [--no-create]
                                  [--no-upload]
                                  [--dry-run]
                                  [--prune-remote]
                                  [--allow-auth-mismatch]

说明:
  - 构建 Hugging Face Docker Space 分发包，并用 hf CLI 上传。
  - 默认目标 Space：tradecatlabs/fatecat。
  - 默认要求当前 hf token 属于 tradecatlabs 用户或有 tradecatlabs org 权限。
  - 免费公共演示默认关闭记录存储，不需要 Bot token 或 API token。
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --space)
      [[ $# -ge 2 ]] || usage_error "--space 缺少参数"
      space_id="$2"
      shift 2
      ;;
    --bundle-dir)
      [[ $# -ge 2 ]] || usage_error "--bundle-dir 缺少参数"
      bundle_dir="$2"
      shift 2
      ;;
    --commit-message)
      [[ $# -ge 2 ]] || usage_error "--commit-message 缺少参数"
      commit_message="$2"
      shift 2
      ;;
    --token)
      [[ $# -ge 2 ]] || usage_error "--token 缺少参数"
      token_value="$2"
      shift 2
      ;;
    --private)
      private_flag="--private"
      shift
      ;;
    --no-create)
      create_repo="0"
      shift
      ;;
    --no-upload)
      upload_repo="0"
      shift
      ;;
    --dry-run)
      create_repo="0"
      upload_repo="0"
      shift
      ;;
    --prune-remote)
      prune_remote="1"
      shift
      ;;
    --allow-auth-mismatch)
      allow_auth_mismatch="1"
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

ensure_command rsync

template_dir="${enterprise_project_root}/infra/huggingface-space"
[[ -f "${template_dir}/README.md" ]] || die "缺少 HF Space README 模板: ${template_dir}/README.md"
[[ -f "${template_dir}/Dockerfile" ]] || die "缺少 HF Space Dockerfile 模板: ${template_dir}/Dockerfile"

namespace="${space_id%%/*}"
if [[ "${space_id}" != */* || -z "${namespace}" ]]; then
  usage_error "--space 必须是 namespace/name，例如 tradecatlabs/fatecat"
fi

if [[ "${create_repo}" == "1" || "${upload_repo}" == "1" ]]; then
  ensure_command hf
  if [[ -n "${token_value}" ]]; then
    whoami_output="$(HF_TOKEN="${token_value}" hf auth whoami 2>&1 || true)"
  else
    whoami_output="$(hf auth whoami 2>&1 || true)"
  fi
  if ! grep -Eq "(^|[[:space:]])user(:[[:space:]]+|=)${namespace}($|[[:space:]])|(^|[[:space:]])orgs(:[[:space:]]*|=).*${namespace}" <<<"${whoami_output}"; then
    if [[ "${allow_auth_mismatch}" != "1" ]]; then
      printf '%s\n' "${whoami_output}" >&2
      die "当前 hf 认证不属于 ${namespace}，也未显示 ${namespace} org 权限；请先运行 hf auth login 使用 ${namespace} 有权限的 token，或显式传 --allow-auth-mismatch。"
    fi
  fi
fi

rm -rf -- "${bundle_dir}"
mkdir -p -- "${bundle_dir}"

cp "${template_dir}/README.md" "${bundle_dir}/README.md"
cp "${template_dir}/Dockerfile" "${bundle_dir}/Dockerfile"
cp "${template_dir}/.hfignore" "${bundle_dir}/.hfignore"

rsync_common=(
  -aR
  --exclude '.git'
  --exclude '.github/'
  --exclude '.history/'
  --exclude '.venv/'
  --exclude 'venv/'
  --exclude '__pycache__/'
  --exclude '*.py[cod]'
  --exclude '.pytest_cache/'
  --exclude '.ruff_cache/'
  --exclude '.mypy_cache/'
  --exclude '.coverage'
  --exclude 'htmlcov/'
  --exclude 'build/'
  --exclude 'dist/'
  --exclude '*.egg-info/'
  --include '.env.example'
  --include '.env.*.example'
  --exclude '.env'
  --exclude '.env.*'
  --exclude '*.log'
  --exclude 'domains/*/services/*/output/'
  --exclude 'domains/*/services/*/runtime/'
  --exclude 'infra/runtime/'
  --exclude 'tools/reference-repos/**/node_modules/'
  --exclude 'node_modules/'
)

(
  cd "${enterprise_project_root}"
  rsync "${rsync_common[@]}" \
    pyproject.toml \
    requirements.txt \
    requirements.lock.txt \
    LICENSE \
    llms.txt \
    contracts \
    domains \
    infra/databases \
    infra/docker/entrypoint.delivery.sh \
    infra/environments \
    tools/reference-repos/github/lunar-python-master \
    tools/reference-repos/github/bazi-1-master \
    tools/reference-repos/github/paipan-master \
    tools/reference-repos/github/sxwnl-master \
    tools/reference-repos/github/iztro-main \
    tools/reference-repos/github/fortel-ziweidoushu-main \
    "${bundle_dir}/"
)

private_hits_file="$(mktemp)"
if find "${bundle_dir}" \
  \( -name '.env' -o -name '*.db' -o -name '*.sqlite' -o -name '*.log' -o -path '*/output/*' -o -path '*/runtime/*' -o -path '*/node_modules/*' \) \
  -print > "${private_hits_file}" && [[ -s "${private_hits_file}" ]]; then
  cat "${private_hits_file}" >&2
  rm -f "${private_hits_file}"
  die "HF Space bundle 含运行态、数据库、日志、secret 或 node_modules，已停止。"
fi
rm -f "${private_hits_file}"

echo "[hf-space] bundle=${bundle_dir}"
du -sh "${bundle_dir}" || true

if [[ "${upload_repo}" == "1" ]]; then
  hf_executable="$(command -v hf)"
  hf_python="$(head -n 1 "${hf_executable}")"
  hf_python="${hf_python#\#!}"
  if [[ ! -x "${hf_python}" ]]; then
    ensure_command python3
    hf_python="$(command -v python3)"
  fi

  FATECAT_HF_SPACE_ID="${space_id}" \
  FATECAT_HF_BUNDLE_DIR="${bundle_dir}" \
  FATECAT_HF_COMMIT_MESSAGE="${commit_message}" \
  FATECAT_HF_CREATE_REPO="${create_repo}" \
  FATECAT_HF_PRIVATE="$([[ "${private_flag}" == "--private" ]] && printf 1 || printf 0)" \
  FATECAT_HF_PRUNE_REMOTE="${prune_remote}" \
  FATECAT_HF_EXPLICIT_TOKEN="${token_value}" \
    "${hf_python}" - <<'PY'
import os

from huggingface_hub import HfApi
from huggingface_hub.errors import RepositoryNotFoundError

space_id = os.environ["FATECAT_HF_SPACE_ID"]
bundle_dir = os.environ["FATECAT_HF_BUNDLE_DIR"]
token = os.environ.get("FATECAT_HF_EXPLICIT_TOKEN") or None
api = HfApi(token=token)

try:
    api.repo_info(repo_id=space_id, repo_type="space")
except RepositoryNotFoundError:
    if os.environ["FATECAT_HF_CREATE_REPO"] != "1":
        raise SystemExit(f"HF Space 不存在且已指定 --no-create: {space_id}")
    api.create_repo(
        repo_id=space_id,
        repo_type="space",
        space_sdk="docker",
        private=os.environ["FATECAT_HF_PRIVATE"] == "1",
    )

result = api.upload_folder(
    repo_id=space_id,
    repo_type="space",
    folder_path=bundle_dir,
    path_in_repo=".",
    commit_message=os.environ["FATECAT_HF_COMMIT_MESSAGE"],
    delete_patterns="*" if os.environ["FATECAT_HF_PRUNE_REMOTE"] == "1" else None,
)
print(result)
PY
  echo "[hf-space] uploaded https://huggingface.co/spaces/${space_id}"
  echo "[hf-space] web https://${namespace}-${space_id#*/}.hf.space/web"
else
  echo "[hf-space] upload skipped"
fi
