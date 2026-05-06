#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
source "${script_dir}/common.sh"

runtime_root="$(resolve_runtime_root)"
cd "${skill_root}"

first_party_pattern='济南|历下区|耿至宇|张三|张三丰|深圳南山|深圳市|深圳'
vendor_pattern='济南|历下区|耿至宇|深圳南山'

violations_file="$(mktemp)"
vendor_hits_file="$(mktemp)"
trap 'rm -f "${violations_file}" "${vendor_hits_file}"' EXIT

is_first_party_scan_target() {
  local path="$1"
  case "${path}" in
    README.md|SKILL.md|references/*|scripts/project/DEBUG.md)
      return 0
      ;;
    scripts/*)
      [[ "${path#scripts/}" != */* ]] && return 0
      ;;
    scripts/project/assets/docs/*|scripts/project/assets/fate/*|scripts/project/modules/telegram/scripts/*|scripts/project/modules/telegram/tests/*|scripts/project/tests/*)
      return 0
      ;;
    scripts/project/modules/telegram/src/*|scripts/project/modules/fate_core/src/*)
      return 0
      ;;
  esac
  return 1
}

is_first_party_excluded() {
  local path="$1"
  case "${path}" in
    scripts/check-privacy-fixtures.sh)
      return 0
      ;;
    scripts/project/modules/telegram/src/location.py)
      return 0
      ;;
    scripts/project/assets/docs/archive/*)
      return 0
      ;;
    scripts/project/assets/docs/vendor/*)
      return 0
      ;;
  esac
  return 1
}

while IFS= read -r path; do
  [[ -f "${path}" ]] || continue
  if ! is_first_party_scan_target "${path}"; then
    continue
  fi
  if is_first_party_excluded "${path}"; then
    continue
  fi
  if grep -n -I -E "${first_party_pattern}" "${path}" >> "${violations_file}"; then
    :
  fi
done < <(git ls-files)

if [[ -s "${violations_file}" ]]; then
  echo "隐私示例扫描失败：一线代码、文档或测试中出现真实感地点/姓名示例。" >&2
  sed 's/^/  - /' "${violations_file}" >&2
  exit 1
fi

if [[ -d "${runtime_root}/assets/vendor/web" ]]; then
  if git grep -n -I -E "${vendor_pattern}" -- scripts/project/assets/vendor/web > "${vendor_hits_file}"; then
    while IFS= read -r line; do
      path="${line%%:*}"
      case "${path}" in
        scripts/project/assets/vendor/web/lifekline-main/components/BaziForm.tsx|\
        scripts/project/assets/vendor/web/lifekline-main/mock-data.json|\
        scripts/project/assets/vendor/web/pcbz-monolith.html|\
        scripts/project/assets/vendor/web/pcbz-paipan/assets/pcbz.iwzwh.com/static/js/*.js|\
        scripts/project/assets/vendor/web/pcbz-wget/pcbz.iwzwh.com/static/js/*.js)
          ;;
        *)
          echo "vendor web 示例扫描失败：发现未登记的真实感占位数据。" >&2
          IFS=: read -r hit_path hit_line _rest <<< "${line}"
          echo "  - ${hit_path}:${hit_line}" >&2
          exit 1
          ;;
      esac
    done < "${vendor_hits_file}"
    echo "[privacy-fixtures] vendor web 存在已隔离的第三方示例占位，未作为生产入口使用。"
  fi
fi

echo "privacy fixtures ok"
