#!/usr/bin/env bash
set -euo pipefail

skill_scripts_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
skill_root="$(cd -- "${skill_scripts_dir}/.." && pwd)"
project_root="${skill_scripts_dir}/project"
lifecycle_root="${project_root}/assets/docs/lifecycle"
lifecycle_templates_dir="${lifecycle_root}/templates"
lifecycle_packs_dir="${lifecycle_root}/packs"

die() {
  echo "$*" >&2
  exit 1
}

usage_error() {
  die "参数错误：$*"
}

ensure_command() {
  local cmd="$1"
  command -v "${cmd}" >/dev/null 2>&1 || die "缺少命令：${cmd}"
}

ensure_parent_dir() {
  local target_path="$1"
  local target_dir
  target_dir="$(dirname -- "${target_path}")"
  mkdir -p "${target_dir}"
}

path_is_within() {
  local target="$1"
  local parent="$2"
  case "${target}" in
    "${parent}"|"${parent}/"*)
      return 0
      ;;
    *)
      return 1
      ;;
  esac
}

python_entrypoint_healthy() {
  local runtime_root="$1"
  local python_bin="${runtime_root}/.venv/bin/python"

  if [[ ! -x "${python_bin}" ]]; then
    return 1
  fi

  local prefix
  prefix="$("${python_bin}" -c 'import sys; print(sys.prefix)' 2>/dev/null || true)"
  [[ "${prefix}" == "${runtime_root}/.venv" ]]
}

venv_entrypoint_stale() {
  local entrypoint="$1"
  local runtime_root="$2"
  local shebang
  local interpreter

  [[ -f "${entrypoint}" ]] || return 1
  if ! grep -Iq . "${entrypoint}" 2>/dev/null; then
    return 1
  fi
  IFS= read -r shebang < "${entrypoint}" || true
  [[ "${shebang}" == '#!'/* ]] || return 1
  interpreter="${shebang#\#!}"

  case "${interpreter}" in
    */.venv/bin/*)
      ;;
    *)
      return 1
      ;;
  esac

  [[ -x "${interpreter}" ]] || return 0
  path_is_within "${interpreter}" "${runtime_root}/.venv/bin" || return 0
  return 1
}

venv_has_stale_entrypoints() {
  local runtime_root="$1"
  local bin_dir="${runtime_root}/.venv/bin"
  local entrypoint

  [[ -d "${bin_dir}" ]] || return 1

  while IFS= read -r -d '' entrypoint; do
    if venv_entrypoint_stale "${entrypoint}" "${runtime_root}"; then
      return 0
    fi
  done < <(find "${bin_dir}" -maxdepth 1 -type f -perm /111 -print0 2>/dev/null)

  return 1
}

runtime_bootstrap_required() {
  local runtime_root="$1"

  ! python_entrypoint_healthy "${runtime_root}" \
    || ! fatecat_entrypoint_healthy "${runtime_root}" \
    || venv_has_stale_entrypoints "${runtime_root}"
}

project_ready() {
  [[ -f "${project_root}/pyproject.toml" ]] && ! runtime_bootstrap_required "${project_root}"
}

project_exists() {
  [[ -f "${project_root}/pyproject.toml" ]]
}

resolve_runtime_root() {
  if project_ready; then
    printf '%s\n' "${project_root}"
    return 0
  fi

  if project_exists; then
    printf '%s\n' "${project_root}"
    return 0
  fi

  echo "无法定位 FateCat 项目根目录：缺少 ${project_root}。" >&2
  return 1
}

resolve_bootstrap_root() {
  resolve_runtime_root
}

ensure_lifecycle_dirs() {
  mkdir -p "${lifecycle_templates_dir}" "${lifecycle_packs_dir}"
}

normalize_slug() {
  local raw="$1"

  printf '%s' "${raw}" \
    | tr '[:upper:]' '[:lower:]' \
    | sed 's/[[:space:]]\+/-/g' \
    | tr -cd 'a-z0-9._-'
}

latest_lifecycle_pack() {
  if [[ ! -d "${lifecycle_packs_dir}" ]]; then
    return 1
  fi

  find "${lifecycle_packs_dir}" -mindepth 1 -maxdepth 1 -type d | sort | tail -n 1
}

fatecat_entrypoint_healthy() {
  local runtime_root="$1"
  local bin_path="${runtime_root}/.venv/bin/fatecat"

  if [[ ! -x "${bin_path}" ]]; then
    return 1
  fi

  local shebang
  local interpreter
  shebang="$(head -n 1 "${bin_path}" 2>/dev/null || true)"
  if [[ "${shebang}" == '#!'/* ]]; then
    interpreter="${shebang#\#!}"
    case "${interpreter}" in
      */.venv/bin/*)
        [[ -x "${interpreter}" ]] || return 1
        path_is_within "${interpreter}" "${runtime_root}/.venv/bin"
        return $?
        ;;
    esac
  fi

  return 0
}

resolve_fatecat_bin() {
  local runtime_root="$1"
  if fatecat_entrypoint_healthy "${runtime_root}"; then
    printf '%s\n' "${runtime_root}/.venv/bin/fatecat"
    return 0
  fi

  if [[ -x "${runtime_root}/.venv/bin/fatecat" ]]; then
    echo "检测到 ${runtime_root}/.venv/bin/fatecat 指向旧路径，请先执行 bootstrap.sh 修复虚拟环境入口。" >&2
    return 1
  fi

  echo "未找到 ${runtime_root}/.venv/bin/fatecat，请先执行 bootstrap.sh。" >&2
  return 1
}

run_fatecat() {
  local runtime_root
  runtime_root="$(resolve_runtime_root)"
  local fatecat_bin
  fatecat_bin="$(resolve_fatecat_bin "${runtime_root}")"
  "${fatecat_bin}" "$@"
}
