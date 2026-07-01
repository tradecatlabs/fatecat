#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
source "${script_dir}/common.sh"

runtime_root="$(resolve_runtime_root)"
vendor_root="$(runtime_vendor_dir "${runtime_root}")"
manifest="${vendor_root}/vendor_sources.json"

[[ -f "${manifest}" ]] || die "缺少 vendor manifest: ${manifest}"

"${runtime_root}/.venv/bin/python" - "${manifest}" "${vendor_root}" <<'PY'
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
    "usageRole",
    "productionUseAllowed",
    "riskNote",
}
ENTRY_SCOPES = ("required", "optionalFutureFeatures", "legacyUnreviewedSnapshots")
VALID_LICENSE_STATUSES = {"spdx", "missing_upstream_license", "license_file_unreviewed"}
VALID_USAGE_ROLES = {
    "production_dependency",
    "oracle_only",
    "evaluation_only",
    "reference_only",
    "future_candidate",
}
IGNORED_DIRS = {
    ".git",
    "node_modules",
    "__pycache__",
    "venv",
    ".venv",
    ".pytest_cache",
    ".ruff_cache",
    ".mypy_cache",
}
IGNORED_FILE_NAMES = {".DS_Store", "Thumbs.db", "pyvenv.cfg"}
IGNORED_FILE_SUFFIXES = {".pyc", ".pyo", ".log", ".db", ".sqlite", ".sqlite3"}
RUNTIME_DIR_NAMES = IGNORED_DIRS
RUNTIME_FILE_NAMES = IGNORED_FILE_NAMES
RUNTIME_FILE_SUFFIXES = IGNORED_FILE_SUFFIXES


def snapshot_files_from_fs(path: Path) -> list[str]:
    files: list[str] = []
    for item in path.rglob("*"):
        rel_parts = item.relative_to(path).parts
        if any(part in IGNORED_DIRS for part in rel_parts):
            continue
        if item.is_symlink():
            continue
        if item.is_file():
            if item.name in IGNORED_FILE_NAMES or item.suffix in IGNORED_FILE_SUFFIXES:
                continue
            files.append(item.relative_to(path).as_posix())
    return sorted(files)


def snapshot_files(path: Path) -> list[str]:
    return snapshot_files_from_fs(path)


def snapshot_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    for rel in snapshot_files(path):
        item = path / rel
        digest.update(rel.encode("utf-8"))
        digest.update(b"\0")
        digest.update(item.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def iter_entries():
    for scope in ENTRY_SCOPES:
        for item in payload.get(scope, []):
            yield scope, item


def find_runtime_pollution(path: Path) -> list[str]:
    pollution: list[str] = []
    if not path.exists():
        return pollution
    for item in path.rglob("*"):
        rel = item.relative_to(vendor_root).as_posix()
        if item.is_symlink():
            pollution.append(rel)
        elif item.is_dir() and item.name in RUNTIME_DIR_NAMES:
            pollution.append(rel + "/")
        elif item.is_file() and (item.name in RUNTIME_FILE_NAMES or item.suffix in RUNTIME_FILE_SUFFIXES):
            pollution.append(rel)
    return sorted(pollution)


metadata_errors: list[str] = []
hash_errors: list[str] = []
license_audit: list[str] = []
missing: list[str] = []
pollution_errors: list[str] = []
duplicate_errors: list[str] = []
seen_ids: set[str] = set()
seen_paths: set[str] = set()
hashed_count = 0

for scope, item in iter_entries():
    item_id = item.get("id", "<unknown>")
    missing_fields = sorted(REQUIRED_FIELDS - set(item))
    if missing_fields:
        metadata_errors.append(f"{item_id} 缺少字段: {', '.join(missing_fields)}")
        continue

    if item["id"] in seen_ids:
        duplicate_errors.append(f"重复 id: {item['id']}")
    seen_ids.add(item["id"])
    if item["path"] in seen_paths:
        duplicate_errors.append(f"重复 path: {item['path']}")
    seen_paths.add(item["path"])

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

    if item.get("usageRole") not in VALID_USAGE_ROLES:
        metadata_errors.append(f"{item['id']} usageRole 非法: {item.get('usageRole')}")

    if item.get("licenseStatus") not in VALID_LICENSE_STATUSES:
        metadata_errors.append(f"{item['id']} licenseStatus 非法: {item.get('licenseStatus')}")
    elif item.get("licenseStatus") == "missing_upstream_license":
        if not item.get("auditRequired"):
            metadata_errors.append(f"{item['id']} 缺少 auditRequired=true")
        license_audit.append(item["id"])
    elif item.get("licenseStatus") == "license_file_unreviewed":
        if not item.get("auditRequired"):
            metadata_errors.append(f"{item['id']} license_file_unreviewed 必须 auditRequired=true")
        if item.get("distributionAllowed"):
            metadata_errors.append(f"{item['id']} license_file_unreviewed 不得 distributionAllowed=true")
        license_audit.append(item["id"])

    if item.get("usageRole") == "production_dependency":
        if item.get("licenseStatus") != "spdx" or item.get("productionUseAllowed") is not True:
            metadata_errors.append(f"{item['id']} production_dependency 必须 spdx 且 productionUseAllowed=true")
    elif item.get("productionUseAllowed") is not False:
        metadata_errors.append(f"{item['id']} 非 production_dependency 不得 productionUseAllowed=true")

    if scope == "legacyUnreviewedSnapshots":
        if item.get("usageRole") != "reference_only":
            metadata_errors.append(f"{item['id']} legacyUnreviewedSnapshots 只能 reference_only")
        if item.get("distributionAllowed"):
            metadata_errors.append(f"{item['id']} legacyUnreviewedSnapshots 不得 distributionAllowed=true")
        if not item.get("auditRequired"):
            metadata_errors.append(f"{item['id']} legacyUnreviewedSnapshots 必须 auditRequired=true")

    expected_hash = item.get("snapshotSha256")
    actual_hash = snapshot_sha256(path)
    hashed_count += 1
    if actual_hash != expected_hash:
        hash_errors.append(f"{item['id']} sha256 mismatch: expected={expected_hash} actual={actual_hash}")

manifest_github_paths = {item["path"] for _, item in iter_entries() if item.get("path", "").startswith("github/")}
actual_github_paths = {
    f"github/{item.name}"
    for item in (vendor_root / "github").iterdir()
    if item.is_dir()
}
unmanifested_paths = sorted(actual_github_paths - manifest_github_paths)
stale_paths = sorted(manifest_github_paths - actual_github_paths)
if unmanifested_paths:
    metadata_errors.append("github 快照未登记到 vendor_sources.json: " + ", ".join(unmanifested_paths))
if stale_paths:
    metadata_errors.append("vendor_sources.json 指向不存在的 github 快照: " + ", ".join(stale_paths))

pollution_errors = find_runtime_pollution(vendor_root)

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

if duplicate_errors:
    print("vendor manifest 存在重复条目:", file=sys.stderr)
    for item in duplicate_errors:
        print(f"  - {item}", file=sys.stderr)
    raise SystemExit(1)

if pollution_errors:
    print("vendor 快照存在运行态或本机污染文件:", file=sys.stderr)
    for item in pollution_errors[:80]:
        print(f"  - {item}", file=sys.stderr)
    if len(pollution_errors) > 80:
        print(f"  ... 还有 {len(pollution_errors) - 80} 项", file=sys.stderr)
    raise SystemExit(1)

if hash_errors:
    print("vendor 快照完整性校验失败:", file=sys.stderr)
    for item in hash_errors:
        print(f"  - {item}", file=sys.stderr)
    raise SystemExit(1)

required_count = len(payload.get("required", []))
optional_count = len(payload.get("optionalFutureFeatures", []))
legacy_count = len(payload.get("legacyUnreviewedSnapshots", []))
print(
    "vendor health ok: "
    f"required={required_count} optionalFutureFeatures={optional_count} "
    f"legacyUnreviewedSnapshots={legacy_count} hashed={hashed_count} "
    f"licenseAuditRequired={len(license_audit)}"
)
PY
