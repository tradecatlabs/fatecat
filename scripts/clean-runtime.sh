#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
source "${script_dir}/common.sh"

remove_venv="0"
dry_run="0"

usage() {
  cat <<'EOF'
用法:
  bash scripts/clean-runtime.sh [--venv] [--dry-run]

说明:
  - 清理根输出目录、本地编辑器历史与当前 runtime root 内的本地缓存
  - 默认不删除 runtime root 的 .venv；如需彻底重建环境，再加 --venv
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --venv)
      remove_venv="1"
      shift
      ;;
    --dry-run)
      dry_run="1"
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

project_root="$(resolve_runtime_root)"
delivery_output_dir="${project_root}/domains/experience-delivery/services/fatecat-delivery/output"

targets=(
  "${skill_root}/output"
  "${skill_root}/.history"
  "${skill_root}/.pytest_cache"
  "${skill_root}/.ruff_cache"
  "${skill_root}/.mypy_cache"
  "${project_root}/.pytest_cache"
  "${project_root}/.ruff_cache"
  "${project_root}/.mypy_cache"
  "${delivery_output_dir}"
  "${project_root}/infra/runtime/local-state/vendor-build"
)

if [[ "${remove_venv}" == "1" ]]; then
  targets+=("${skill_root}/.venv" "${skill_root}/venv" "${project_root}/.venv")
fi

for target in "${targets[@]}"; do
  if [[ ! -e "${target}" ]]; then
    continue
  fi

  if [[ "${dry_run}" == "1" ]]; then
    echo "[clean-runtime] would remove ${target}"
    continue
  fi

  chmod -R u+w "${target}" 2>/dev/null || true
  rm -rf "${target}"
  echo "[clean-runtime] removed ${target}"
done

python_cache_dirs_count="$(
  find "${project_root}" \
    -path "${project_root}/.venv" -prune -o \
    -type d -name '__pycache__' -print 2>/dev/null | wc -l
)"
python_bytecode_count="$(
  find "${project_root}" \
    -path "${project_root}/.venv" -prune -o \
    -type f \( -name '*.pyc' -o -name '*.pyo' \) -print 2>/dev/null | wc -l
)"

if [[ "${dry_run}" == "1" ]]; then
  echo "[clean-runtime] would remove ${python_cache_dirs_count} __pycache__ dirs under ${project_root}"
  echo "[clean-runtime] would remove ${python_bytecode_count} Python bytecode files under ${project_root}"
  exit 0
fi

if [[ "${python_cache_dirs_count}" != "0" ]]; then
  find "${project_root}" \
    -path "${project_root}/.venv" -prune -o \
    -type d -name '__pycache__' -exec rm -rf {} +
fi

if [[ "${python_bytecode_count}" != "0" ]]; then
  find "${project_root}" \
    -path "${project_root}/.venv" -prune -o \
    -type f \( -name '*.pyc' -o -name '*.pyo' \) -exec rm -f {} +
fi

runtime_state_roots=(
  "${project_root}/infra/runtime/local-state"
  "${project_root}/runtime"
)
runtime_database_count=0
for runtime_state_root in "${runtime_state_roots[@]}"; do
  [[ -d "${runtime_state_root}" ]] || continue
  count="$(
    find "${runtime_state_root}" \
      -type f \( -name '*.db' -o -name '*.sqlite' -o -name '*.sqlite3' \) -print 2>/dev/null | wc -l
  )"
  runtime_database_count=$((runtime_database_count + count))
  find "${runtime_state_root}" \
    -type f \( -name '*.db' -o -name '*.sqlite' -o -name '*.sqlite3' \) -exec rm -f {} +
done

node_modules_count=0
reference_venv_count=0
reference_pyvenv_count=0
reference_cache_dirs_count=0
reference_pollution_files_count=0
reference_repo_root="${project_root}/tools/reference-repos"
if [[ -d "${reference_repo_root}" ]]; then
  node_modules_count="$(find "${reference_repo_root}" -type d -name node_modules -print 2>/dev/null | wc -l)"
  find "${reference_repo_root}" -type d -name node_modules -prune -exec rm -rf {} +
  reference_venv_count="$(
    find "${reference_repo_root}" -type d \( -name venv -o -name .venv \) -print 2>/dev/null | wc -l
  )"
  find "${reference_repo_root}" -type d \( -name venv -o -name .venv \) -prune -exec rm -rf {} +
  reference_pyvenv_count="$(
    find "${reference_repo_root}" -type f -name pyvenv.cfg -print 2>/dev/null | wc -l
  )"
  while IFS= read -r pyvenv_file; do
    pyvenv_root="$(dirname -- "${pyvenv_file}")"
    rm -f "${pyvenv_file}"
    if [[ -f "${pyvenv_root}/bin/activate" ]]; then
      rm -rf "${pyvenv_root}/bin" "${pyvenv_root}/include" "${pyvenv_root}/lib" "${pyvenv_root}/lib64" "${pyvenv_root}/share"
    fi
  done < <(find "${reference_repo_root}" -type f -name pyvenv.cfg -print 2>/dev/null)
  reference_cache_dirs_count="$(
    find "${reference_repo_root}" -type d \( -name .pytest_cache -o -name .ruff_cache -o -name .mypy_cache \) -print 2>/dev/null | wc -l
  )"
  find "${reference_repo_root}" -type d \( -name .pytest_cache -o -name .ruff_cache -o -name .mypy_cache \) -prune -exec rm -rf {} +
  reference_pollution_files_count="$(
    find "${reference_repo_root}" \
      -type f \( -name .DS_Store -o -name Thumbs.db -o -name '*.log' -o -name '*.db' -o -name '*.sqlite' -o -name '*.sqlite3' \) \
      -print 2>/dev/null | wc -l
  )"
  find "${reference_repo_root}" \
    -type f \( -name .DS_Store -o -name Thumbs.db -o -name '*.log' -o -name '*.db' -o -name '*.sqlite' -o -name '*.sqlite3' \) \
    -exec rm -f {} +
fi

echo "[clean-runtime] removed ${python_cache_dirs_count} __pycache__ dirs"
echo "[clean-runtime] removed ${python_bytecode_count} Python bytecode files"
echo "[clean-runtime] removed ${runtime_database_count} runtime database files"
echo "[clean-runtime] removed ${node_modules_count} reference repo node_modules dirs"
echo "[clean-runtime] removed ${reference_venv_count} reference repo virtualenv dirs"
echo "[clean-runtime] removed ${reference_pyvenv_count} reference repo pyvenv roots"
echo "[clean-runtime] removed ${reference_cache_dirs_count} reference repo cache dirs"
echo "[clean-runtime] removed ${reference_pollution_files_count} reference repo pollution files"
