#!/usr/bin/env bash
set -euo pipefail

skill_scripts_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
skill_root="$(cd -- "${skill_scripts_dir}/.." && pwd)"
enterprise_project_root="${skill_root}"
lifecycle_root="${skill_root}/docs/reference-materials/lifecycle"
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

canonical_roots_exist() {
  local root="$1"

  [[ -d "${root}/domains" ]] \
    && [[ -d "${root}/contracts" ]] \
    && [[ -d "${root}/catalog" ]] \
    && [[ -d "${root}/governance" ]]
}

enterprise_runtime_ready() {
  local root="$1"

  canonical_roots_exist "${root}" \
    && [[ -f "${root}/pyproject.toml" ]] \
    && [[ -d "${root}/domains/fate-analysis/services/fate-core/src/fate_core" ]] \
    && [[ -d "${root}/domains/experience-delivery/services/fatecat-delivery/src" ]] \
    && [[ -f "${root}/infra/environments/local/branding.json" ]] \
    && [[ -f "${root}/contracts/fate/capabilities/registry.json" ]] \
    && [[ -f "${root}/contracts/fate/profiles/pure_analysis.json" ]] \
    && [[ -f "${root}/domains/fate-analysis/data-products/locations/location_catalog.ndjson.gz" ]] \
    && [[ -f "${root}/domains/fate-analysis/data-products/locations/manifest.json" ]] \
    && [[ -f "${root}/infra/databases/bazi/schema_v2.sql" ]] \
    && [[ -d "${root}/tools/reference-repos/github/lunar-python-master" ]]
}

project_ready() {
  local root="${1:-${enterprise_project_root}}"
  [[ -f "${root}/pyproject.toml" ]] && ! runtime_bootstrap_required "${root}"
}

project_exists() {
  local root="${1:-${enterprise_project_root}}"
  [[ -f "${root}/pyproject.toml" ]]
}

resolve_explicit_runtime_root() {
  if [[ -z "${FATECAT_RUNTIME_ROOT:-}" ]]; then
    return 1
  fi

  local explicit_root="${FATECAT_RUNTIME_ROOT}"
  if [[ ! -d "${explicit_root}" ]]; then
    echo "FATECAT_RUNTIME_ROOT 指向的目录不存在：${explicit_root}" >&2
    return 1
  fi

  explicit_root="$(cd "${explicit_root}" && pwd)"
  if ! project_exists "${explicit_root}"; then
    echo "FATECAT_RUNTIME_ROOT 缺少 pyproject.toml：${explicit_root}" >&2
    return 1
  fi
  if ! enterprise_runtime_ready "${explicit_root}"; then
    echo "FATECAT_RUNTIME_ROOT 必须指向已就绪的企业根：${explicit_root}" >&2
    return 1
  fi

  printf '%s\n' "${explicit_root}"
}

resolve_runtime_root() {
  if [[ -n "${FATECAT_RUNTIME_ROOT:-}" ]]; then
    resolve_explicit_runtime_root
    return $?
  fi

  if enterprise_runtime_ready "${enterprise_project_root}" && project_exists "${enterprise_project_root}"; then
    printf '%s\n' "${enterprise_project_root}"
    return 0
  fi

  echo "无法定位 FateCat 企业运行根：${enterprise_project_root} 缺少 canonical 运行资产。" >&2
  return 1
}

resolve_bootstrap_root() {
  resolve_runtime_root
}

runtime_config_dir() {
  local root="$1"
  printf '%s\n' "${root}/infra/environments/local"
}

runtime_contract_dir() {
  local root="$1"
  printf '%s\n' "${root}/contracts/fate"
}

runtime_data_dir() {
  local root="$1"
  printf '%s\n' "${root}/domains/fate-analysis/data-products"
}

runtime_database_dir() {
  local root="$1"
  printf '%s\n' "${root}/infra/databases"
}

runtime_vendor_dir() {
  local root="$1"
  printf '%s\n' "${root}/tools/reference-repos"
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
