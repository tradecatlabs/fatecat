#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
source "${script_dir}/common.sh"

cd "${skill_root}"

violations_file="$(mktemp)"
personal_hits_file="$(mktemp)"
trap 'rm -f "${violations_file}" "${personal_hits_file}"' EXIT

while IFS= read -r path; do
  case "${path}" in
    scripts/project/assets/data/classics/raw/*|\
    scripts/project/assets/data/calendar/solar_terms/raw/*|\
    scripts/project/assets/config/.env|\
    scripts/project/modules/telegram/output/*|\
    output/*|\
    *.pyc|\
    *.pyo|\
    *.db|\
    *.sqlite|\
    *.sqlite3|\
    *.log)
      printf '%s\n' "${path}" >> "${violations_file}"
      ;;
  esac
done < <(git ls-files)

if [[ -s "${violations_file}" ]]; then
  echo "源仓卫生检查失败：发现不应进入 Git 的 raw、运行态、缓存或数据库文件。" >&2
  sed 's/^/  - /' "${violations_file}" >&2
  exit 1
fi

for pattern in '13208' '/mnt/c/Users' 'C:\Users'; do
  if git grep -n -I -F "${pattern}" -- \
    ':!scripts/check-source-hygiene.sh' \
    ':!scripts/project/assets/vendor' \
    ':!scripts/project/assets/data/classics/raw' \
    ':!scripts/project/assets/data/calendar/solar_terms/raw' \
    >> "${personal_hits_file}"; then
    :
  fi
done

if [[ -s "${personal_hits_file}" ]]; then
  echo "源仓卫生检查失败：发现本机个人绝对路径或账号痕迹。" >&2
  sed 's/^/  - /' "${personal_hits_file}" >&2
  exit 1
fi

echo "source hygiene ok"
