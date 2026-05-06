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
import hashlib
import sys
from pathlib import Path

manifest_path = Path(sys.argv[1])
vendor_root = Path(sys.argv[2])
payload = json.loads(manifest_path.read_text(encoding="utf-8"))

REQUIRED_FIELDS = {
    "id",
    "path",
    "source",
    "purpose",
    "license",
    "licenseStatus",
    "licenseFile",
    "distributionAllowed",
    "revision",
    "retrievedAt",
    "revisionStatus",
    "snapshotSha256",
}
IGNORED_DIRS = {".git", "node_modules", "__pycache__"}


def snapshot_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    for item in sorted(path.rglob("*")):
        rel_parts = item.relative_to(path).parts
        if any(part in IGNORED_DIRS for part in rel_parts):
            continue
        if item.is_file():
            rel = item.relative_to(path).as_posix()
            digest.update(rel.encode("utf-8"))
            digest.update(b"\0")
            digest.update(item.read_bytes())
            digest.update(b"\0")
    return digest.hexdigest()


def iter_entries():
    for scope in ("required", "optionalFutureFeatures"):
        for item in payload.get(scope, []):
            yield scope, item


metadata_errors: list[str] = []
hash_errors: list[str] = []
license_audit: list[str] = []
missing: list[str] = []
hashed_count = 0

for scope, item in iter_entries():
    missing_fields = sorted(REQUIRED_FIELDS - set(item))
    if missing_fields:
        metadata_errors.append(f"{item.get('id', '<unknown>')} 缺少字段: {', '.join(missing_fields)}")
        continue

    path = vendor_root / item["path"]
    if not path.exists():
        message = f"{item['id']} -> {path}"
        if scope == "required":
            missing.append(message)
        else:
            metadata_errors.append(f"optional vendor 路径缺失: {message}")
        continue

    license_file = item.get("licenseFile")
    if license_file and not (path / license_file).exists():
        metadata_errors.append(f"{item['id']} licenseFile 不存在: {license_file}")

    if item.get("licenseStatus") == "missing_upstream_license":
        if not item.get("auditRequired"):
            metadata_errors.append(f"{item['id']} 缺少 auditRequired=true")
        license_audit.append(item["id"])
    elif item.get("licenseStatus") != "spdx":
        metadata_errors.append(f"{item['id']} licenseStatus 非法: {item.get('licenseStatus')}")

    expected_hash = item.get("snapshotSha256")
    actual_hash = snapshot_sha256(path)
    hashed_count += 1
    if actual_hash != expected_hash:
        hash_errors.append(f"{item['id']} sha256 mismatch: expected={expected_hash} actual={actual_hash}")

if missing:
    print("vendor 必需快照缺失:", file=sys.stderr)
    for item in missing:
        print(f"  - {item}", file=sys.stderr)
    raise SystemExit(1)

if metadata_errors:
    print("vendor 元数据不完整:", file=sys.stderr)
    for item in metadata_errors:
        print(f"  - {item}", file=sys.stderr)
    raise SystemExit(1)

if hash_errors:
    print("vendor 快照完整性校验失败:", file=sys.stderr)
    for item in hash_errors:
        print(f"  - {item}", file=sys.stderr)
    raise SystemExit(1)

required_count = len(payload.get("required", []))
optional_count = len(payload.get("optionalFutureFeatures", []))
print(
    "vendor health ok: "
    f"required={required_count} optionalFutureFeatures={optional_count} "
    f"hashed={hashed_count} licenseAuditRequired={len(license_audit)}"
)
PY
