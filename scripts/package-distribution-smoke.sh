#!/usr/bin/env bash
set -euo pipefail

export PYTHONDONTWRITEBYTECODE=1

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
source "${script_dir}/common.sh"

runtime_root="$(resolve_runtime_root)"
python_bin="${runtime_root}/.venv/bin/python"
output_root="${1:-/tmp/fatecat-package-distribution-smoke}"
wheel_limit_bytes="${FATECAT_WHEEL_MAX_BYTES:-1048576}"
sdist_limit_bytes="${FATECAT_SDIST_MAX_BYTES:-2097152}"

[[ -x "${python_bin}" ]] || die "缺少开发 Python：${python_bin}"
rm -rf "${output_root}"
mkdir -p "${output_root}/dist"

(
  cd "${runtime_root}"
  "${python_bin}" -m build --sdist --wheel --outdir "${output_root}/dist"
)

wheel_path="$(find "${output_root}/dist" -maxdepth 1 -type f -name '*.whl' -print -quit)"
sdist_path="$(find "${output_root}/dist" -maxdepth 1 -type f -name '*.tar.gz' -print -quit)"
[[ -n "${wheel_path}" && -n "${sdist_path}" ]] || die "构建产物不完整"

wheel_size="$(stat -c '%s' "${wheel_path}")"
sdist_size="$(stat -c '%s' "${sdist_path}")"
(( wheel_size <= wheel_limit_bytes )) || die "wheel 超出预算：${wheel_size} > ${wheel_limit_bytes}"
(( sdist_size <= sdist_limit_bytes )) || die "sdist 超出预算：${sdist_size} > ${sdist_limit_bytes}"

mkdir -p "${output_root}/sdist-source" "${output_root}/sdist-wheel"
tar -xzf "${sdist_path}" -C "${output_root}/sdist-source"
sdist_source_root="$(find "${output_root}/sdist-source" -mindepth 1 -maxdepth 1 -type d -print -quit)"
[[ -n "${sdist_source_root}" ]] || die "无法解压 sdist"
"${python_bin}" -m build --wheel --no-isolation --outdir "${output_root}/sdist-wheel" "${sdist_source_root}"
sdist_wheel_path="$(find "${output_root}/sdist-wheel" -maxdepth 1 -type f -name '*.whl' -print -quit)"
[[ -n "${sdist_wheel_path}" ]] || die "无法从 sdist 重建 wheel"

python3 -m venv "${output_root}/venv"
"${output_root}/venv/bin/python" -m pip install -q --no-deps "${sdist_wheel_path}"
(
  cd "${output_root}"
  "${output_root}/venv/bin/fatecat" capabilities --pretty > capabilities.json
)

"${output_root}/venv/bin/python" - "${output_root}/capabilities.json" <<'PY'
from __future__ import annotations

import json
import sys
from pathlib import Path

payload = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
if payload.get("success") is not True:
    raise SystemExit("clean-room capabilities smoke failed")
capability_ids = {item.get("capabilityId") for item in payload.get("capabilities", [])}
if not {"bazi", "ziwei"}.issubset(capability_ids):
    raise SystemExit(f"missing required capabilities: {sorted(capability_ids)}")
runtime = payload.get("runtime", {})
if runtime.get("distributionMode") != "wheel":
    raise SystemExit(f"unexpected distribution mode: {runtime}")
if runtime.get("providerAssetsAvailable") is not False:
    raise SystemExit("protocol wheel must not claim bundled provider assets")
PY

printf 'package distribution smoke ok: wheel=%s bytes sdist=%s bytes output=%s\n' \
  "${wheel_size}" "${sdist_size}" "${output_root}"
