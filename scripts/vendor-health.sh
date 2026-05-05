#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
source "${script_dir}/common.sh"

runtime_root="$(resolve_runtime_root)"
manifest="${runtime_root}/assets/vendor/vendor_sources.json"

[[ -f "${manifest}" ]] || die "缺少 vendor manifest: ${manifest}"

"${runtime_root}/.venv/bin/python" - "${manifest}" "${runtime_root}/assets/vendor" <<'PY'
from __future__ import annotations

import json
import sys
from pathlib import Path

manifest_path = Path(sys.argv[1])
vendor_root = Path(sys.argv[2])
payload = json.loads(manifest_path.read_text(encoding="utf-8"))

missing: list[str] = []
for item in payload.get("required", []):
    path = vendor_root / item["path"]
    if not path.exists():
        missing.append(f"{item['id']} -> {path}")

if missing:
    print("vendor 必需快照缺失:", file=sys.stderr)
    for item in missing:
        print(f"  - {item}", file=sys.stderr)
    raise SystemExit(1)

required_count = len(payload.get("required", []))
optional_count = len(payload.get("optionalFutureFeatures", []))
print(f"vendor health ok: required={required_count} optionalFutureFeatures={optional_count}")
PY
