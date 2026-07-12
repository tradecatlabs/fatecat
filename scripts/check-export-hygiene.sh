#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
source "${script_dir}/common.sh"

bundle_root=""
require_public_vendor_policy="0"
max_bytes="${FATECAT_EXPORT_MAX_BYTES:-83886080}"
max_files="${FATECAT_EXPORT_MAX_FILES:-6000}"

usage() {
  cat <<'EOF'
用法:
  bash scripts/check-export-hygiene.sh <exported-skill-root> [--public]

说明:
  - 检查导出 skill 包中是否混入本地运行态、缓存、字节码、secret 或 Git 元数据。
  - --public 额外拒绝 vendor manifest 中 distributionAllowed=false 的已包含快照。
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --public)
      require_public_vendor_policy="1"
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      if [[ -n "${bundle_root}" ]]; then
        usage_error "只能提供一个导出目录"
      fi
      bundle_root="$1"
      shift
      ;;
  esac
done

if [[ -z "${bundle_root}" ]]; then
  usage >&2
  exit 2
fi

[[ -d "${bundle_root}" ]] || die "导出目录不存在: ${bundle_root}"
bundle_root="$(cd "${bundle_root}" && pwd)"

violations_file="$(mktemp)"
trap 'rm -f "${violations_file}"' EXIT

find "${bundle_root}" \
  \( \
    -path "${bundle_root}/.git" -o \
    -path "${bundle_root}/.history" -o \
    -path "${bundle_root}/.venv" -o \
    -path "${bundle_root}/venv" -o \
    -path "${bundle_root}/.pytest_cache" -o \
    -path "${bundle_root}/.ruff_cache" -o \
    -path "${bundle_root}/.mypy_cache" -o \
    -path "${bundle_root}/infra/runtime/local-state/exports" -o \
    -path "${bundle_root}/infra/runtime/local-state/vendor-build" -o \
    -path "${bundle_root}/output" -o \
    -path "${bundle_root}/domains/fate-analysis/services/fate-core/output" -o \
    -path "${bundle_root}/domains/fate-analysis/services/fate-core/runtime" -o \
    -path "${bundle_root}/domains/experience-delivery/services/fatecat-delivery/output" -o \
    -path "${bundle_root}/domains/experience-delivery/services/fatecat-delivery/runtime" -o \
    -name '.env' -o \
    -name '.env.local' -o \
    -name '*.local' -o \
    -name '*.log' -o \
    -name '.DS_Store' -o \
    -name 'node_modules' -o \
    -name '__pycache__' -o \
    -name '*.pyc' -o \
    -name '*.pyo' -o \
    -name '*.db' -o \
    -name '*.sqlite' -o \
    -name '*.sqlite3' \
  \) -print > "${violations_file}"

find "${bundle_root}/tools/reference-repos" -type f \
  \( -name '*.zip' -o -name '*.7z' -o -name '*.rar' -o -name '*.mp4' -o -name '*.mov' -o \
     -name '*.avi' -o -name '*.ttf' -o -name '*.otf' -o -name '*.woff' -o -name '*.woff2' \) \
  -print >> "${violations_file}" 2>/dev/null || true

if [[ -s "${violations_file}" ]]; then
  echo "导出包卫生检查失败，发现不应分发的文件或目录:" >&2
  sed 's/^/  - /' "${violations_file}" >&2
  exit 1
fi

if [[ "${require_public_vendor_policy}" == "1" ]]; then
  manifest="${bundle_root}/tools/reference-repos/vendor_sources.json"
  [[ -f "${manifest}" ]] || die "公开导出缺少 vendor manifest: ${manifest}"
  python3 - "${bundle_root}" "${manifest}" <<'PY'
from __future__ import annotations

import json
import sys
from pathlib import Path

bundle_root = Path(sys.argv[1])
manifest = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
blocked: list[str] = []
for scope in ("required", "optionalFutureFeatures", "legacyUnreviewedSnapshots"):
    for item in manifest.get(scope, []):
        path = bundle_root / "tools" / "reference-repos" / str(item.get("path", ""))
        if path.exists() and item.get("distributionAllowed") is not True:
            blocked.append(
                f"{item.get('id', '<unknown>')} ({item.get('licenseStatus', 'unknown')}, {path.relative_to(bundle_root)})"
            )
if blocked:
    print("公开导出供应链检查失败，包含未获准分发的 vendor:", file=sys.stderr)
    for item in blocked:
        print(f"  - {item}", file=sys.stderr)
    raise SystemExit(1)
print("public vendor distribution policy ok")
PY
fi

case "${max_bytes}" in
  ''|*[!0-9]*) die "FATECAT_EXPORT_MAX_BYTES 必须是非负整数" ;;
esac
case "${max_files}" in
  ''|*[!0-9]*) die "FATECAT_EXPORT_MAX_FILES 必须是非负整数" ;;
esac

bundle_bytes="$(du -sb "${bundle_root}" | awk '{print $1}')"
bundle_files="$(find "${bundle_root}" -type f | wc -l)"
if (( bundle_bytes > max_bytes )); then
  die "导出包超出体积预算: ${bundle_bytes} > ${max_bytes} bytes"
fi
if (( bundle_files > max_files )); then
  die "导出包超出文件数预算: ${bundle_files} > ${max_files}"
fi

echo "export hygiene ok: ${bundle_root} (${bundle_bytes} bytes, ${bundle_files} files)"
