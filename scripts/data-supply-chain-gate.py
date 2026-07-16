#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = REPO_ROOT / "contracts" / "fate" / "data-supply-chain" / "registry.json"
SCHEMA_PATH = REPO_ROOT / "contracts" / "fate" / "data-supply-chain" / "schemas" / "data-supply-chain.schema.json"
DATA_PRODUCTS_ROOT = REPO_ROOT / "domains" / "fate-analysis" / "data-products"
CLASSICS_DIR = DATA_PRODUCTS_ROOT / "classics"
CLASSICS_SOURCE_MANIFEST = CLASSICS_DIR / "source_manifest.tsv"
CLASSICS_COPYRIGHT_REVIEW = CLASSICS_DIR / "copyright_review.tsv"
CLASSICS_CURATION_POLICY = CLASSICS_DIR / "curation_policy.json"
CLASSICS_CURATION_SCHEMA = (
    REPO_ROOT / "contracts" / "fate" / "data-supply-chain" / "schemas" / "classics-curation-policy.schema.json"
)
SOLAR_TERMS_SOURCE_MANIFEST = DATA_PRODUCTS_ROOT / "calendar" / "solar_terms" / "source_manifest.tsv"
VENDOR_MANIFEST = REPO_ROOT / "tools" / "reference-repos" / "vendor_sources.json"
DEFAULT_OUTPUT_JSON = (
    REPO_ROOT / "infra" / "runtime" / "local-state" / "exports" / "supply-chain" / "data-supply-chain-gate.json"
)

SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")


class DataSupplyChainGateError(RuntimeError):
    """数据供应链门禁未满足预期。"""


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _append_check(checks: list[dict[str, Any]], name: str, ok: bool, details: str) -> None:
    checks.append({"name": name, "ok": ok, "details": details})


def _check(checks: list[dict[str, Any]], name: str, condition: bool, details: str) -> None:
    _append_check(checks, name, condition, details)
    if not condition:
        raise DataSupplyChainGateError(f"{name}: {details}")


def _safe_repo_path(raw_path: str) -> Path:
    path = Path(raw_path)
    if path.is_absolute() or ".." in path.parts:
        raise DataSupplyChainGateError(f"unsafe path: {raw_path}")
    return REPO_ROOT / path


def _schema_allowed(schema: dict[str, Any], key: str) -> set[str]:
    return {str(value) for value in schema.get(key, [])}


def _iter_vendor_entries(payload: dict[str, Any]):
    for scope in ("required", "optionalFutureFeatures", "legacyUnreviewedSnapshots"):
        for item in payload.get(scope, []):
            yield scope, item


def _validate_registry(
    *,
    registry: dict[str, Any],
    schema: dict[str, Any],
    checks: list[dict[str, Any]],
) -> dict[str, Any]:
    missing_registry = sorted(set(schema["requiredRegistryFields"]) - set(registry))
    _check(checks, "registry:required_fields", not missing_registry, str(missing_registry))

    assets = registry.get("assets", [])
    _check(checks, "registry:asset_count", len(assets) >= 8, str(len(assets)))
    ids = [item.get("id") for item in assets]
    _check(checks, "registry:unique_ids", len(ids) == len(set(ids)), "unique")

    allowed_asset_type = _schema_allowed(schema, "allowedAssetType")
    allowed_layer = _schema_allowed(schema, "allowedLifecycleLayer")
    allowed_usage = _schema_allowed(schema, "allowedUsageRole")
    allowed_status = _schema_allowed(schema, "allowedStatus")
    allowed_privacy = _schema_allowed(schema, "allowedPrivacyClass")
    allowed_license = _schema_allowed(schema, "allowedLicenseStatus")
    allowed_export = _schema_allowed(schema, "allowedExportStatus")
    allowed_production = _schema_allowed(schema, "allowedProductionEligibilityStatus")

    path_count = 0
    sha_checked = 0
    review_required = 0
    production_input = 0
    export_blocked = 0

    for asset in assets:
        asset_id = str(asset.get("id", "<missing>"))
        missing_asset = sorted(set(schema["requiredAssetFields"]) - set(asset))
        _check(checks, f"asset:{asset_id}:required_fields", not missing_asset, str(missing_asset))

        _check(checks, f"asset:{asset_id}:asset_type", asset["assetType"] in allowed_asset_type, asset["assetType"])
        _check(
            checks,
            f"asset:{asset_id}:lifecycle_layer",
            asset["lifecycleLayer"] in allowed_layer,
            asset["lifecycleLayer"],
        )
        _check(checks, f"asset:{asset_id}:usage_role", asset["usageRole"] in allowed_usage, asset["usageRole"])
        _check(checks, f"asset:{asset_id}:status", asset["status"] in allowed_status, asset["status"])
        _check(checks, f"asset:{asset_id}:privacy", asset["privacyClass"] in allowed_privacy, asset["privacyClass"])

        license_policy = asset["licensePolicy"]
        export_policy = asset["exportPolicy"]
        production = asset["productionEligibility"]
        missing_license = sorted(set(schema["requiredLicensePolicyFields"]) - set(license_policy))
        missing_export = sorted(set(schema["requiredExportPolicyFields"]) - set(export_policy))
        missing_production = sorted(set(schema["requiredProductionEligibilityFields"]) - set(production))
        _check(checks, f"asset:{asset_id}:license_fields", not missing_license, str(missing_license))
        _check(checks, f"asset:{asset_id}:export_fields", not missing_export, str(missing_export))
        _check(checks, f"asset:{asset_id}:production_fields", not missing_production, str(missing_production))
        _check(
            checks,
            f"asset:{asset_id}:license_status",
            license_policy["licenseStatus"] in allowed_license,
            license_policy["licenseStatus"],
        )
        _check(
            checks,
            f"asset:{asset_id}:export_status",
            export_policy["status"] in allowed_export,
            export_policy["status"],
        )
        _check(
            checks,
            f"asset:{asset_id}:production_status",
            production["status"] in allowed_production,
            production["status"],
        )

        if asset["status"] == "review_required":
            review_required += 1
            _check(
                checks,
                f"asset:{asset_id}:review_not_production_allowed",
                production["status"] != "allowed",
                production["status"],
            )
        if asset["status"] == "blocked":
            _check(
                checks,
                f"asset:{asset_id}:blocked_not_exported",
                export_policy["allowedInPublicExport"] is False,
                str(export_policy["allowedInPublicExport"]),
            )
        if asset["usageRole"] == "production_input":
            production_input += 1
            _check(
                checks,
                f"asset:{asset_id}:production_input_allowed",
                production["status"] == "allowed" and license_policy["productionUseAllowed"] is True,
                f"{production['status']} productionUseAllowed={license_policy['productionUseAllowed']}",
            )
        if export_policy["allowedInPublicExport"] is False:
            export_blocked += 1

        for path_entry in asset["paths"]:
            missing_path_fields = sorted(set(schema["requiredPathFields"]) - set(path_entry))
            _check(checks, f"asset:{asset_id}:path_fields", not missing_path_fields, str(missing_path_fields))
            path_count += 1
            path = _safe_repo_path(path_entry["path"])
            if path_entry.get("required"):
                _check(checks, f"asset:{asset_id}:path_exists:{path_entry['path']}", path.exists(), path_entry["path"])
            expected_sha = path_entry.get("sha256")
            if expected_sha:
                _check(
                    checks,
                    f"asset:{asset_id}:sha_format:{path_entry['path']}",
                    bool(SHA256_PATTERN.fullmatch(expected_sha)),
                    expected_sha,
                )
                _check(
                    checks,
                    f"asset:{asset_id}:sha_match:{path_entry['path']}",
                    path.is_file() and _sha256(path) == expected_sha,
                    path_entry["path"],
                )
                sha_checked += 1

        for manifest_path in asset["manifests"]:
            path = _safe_repo_path(manifest_path)
            _check(checks, f"asset:{asset_id}:manifest_exists:{manifest_path}", path.is_file(), manifest_path)

    return {
        "assetCount": len(assets),
        "pathCount": path_count,
        "shaChecked": sha_checked,
        "reviewRequiredAssetCount": review_required,
        "productionInputAssetCount": production_input,
        "exportBlockedAssetCount": export_blocked,
    }


def _validate_classics(checks: list[dict[str, Any]]) -> dict[str, Any]:
    source_rows = _read_tsv(CLASSICS_SOURCE_MANIFEST)
    copyright_rows = _read_tsv(CLASSICS_COPYRIGHT_REVIEW)
    source_by_path = {row["relative_path"]: row for row in source_rows}
    copyright_assets = {row["asset"]: row for row in copyright_rows}
    classic_files = sorted(CLASSICS_DIR.glob("*.txt"))
    missing_source: list[str] = []
    missing_copyright: list[str] = []
    hash_mismatch: list[str] = []

    for path in classic_files:
        rel = f"classics/{path.name}"
        source_row = source_by_path.get(rel)
        if not source_row:
            missing_source.append(rel)
        else:
            actual_bytes = str(path.stat().st_size)
            actual_sha = _sha256(path)
            if source_row.get("bytes") != actual_bytes or source_row.get("sha256") != actual_sha:
                hash_mismatch.append(rel)
        if rel not in copyright_assets:
            missing_copyright.append(rel)

    _check(checks, "classics:source_manifest_coverage", not missing_source, str(missing_source))
    _check(checks, "classics:copyright_review_coverage", not missing_copyright, str(missing_copyright))
    _check(checks, "classics:hash_integrity", not hash_mismatch, str(hash_mismatch))
    _check(
        checks,
        "classics:review_required_boundary",
        all(copyright_assets[f"classics/{path.name}"]["status"] == "review_required" for path in classic_files),
        "all canonical classics remain review_required",
    )
    _check(
        checks,
        "classics:no_direct_distribution_without_review",
        all(
            copyright_assets[f"classics/{path.name}"]["release_policy"] != "included_without_review"
            for path in classic_files
        ),
        "no canonical classic is marked included_without_review",
    )

    return {
        "canonicalTxtCount": len(classic_files),
        "sourceManifestRows": len(source_rows),
        "copyrightRows": len(copyright_rows),
        "hashChecked": len(classic_files),
    }


def _validate_classics_curation(checks: list[dict[str, Any]]) -> dict[str, Any]:
    policy = _load_json(CLASSICS_CURATION_POLICY)
    schema = _load_json(CLASSICS_CURATION_SCHEMA)
    source_rows = _read_tsv(CLASSICS_SOURCE_MANIFEST)
    source_by_path = {row["relative_path"]: row for row in source_rows}
    classic_paths = {f"classics/{path.name}" for path in CLASSICS_DIR.glob("*.txt")}
    documents = policy.get("documents", [])
    document_paths = [item.get("sourcePath") for item in documents]

    _check(
        checks,
        "classics_curation:required_policy_fields",
        not (set(schema["requiredPolicyFields"]) - set(policy)),
        str(sorted(set(schema["requiredPolicyFields"]) - set(policy))),
    )
    _check(checks, "classics_curation:document_count", len(documents) == len(classic_paths), str(len(documents)))
    _check(
        checks,
        "classics_curation:unique_source_paths",
        len(document_paths) == len(set(document_paths)),
        "unique",
    )
    _check(
        checks,
        "classics_curation:canonical_coverage",
        set(document_paths) == classic_paths,
        f"missing={sorted(classic_paths - set(document_paths))} extra={sorted(set(document_paths) - classic_paths)}",
    )

    allowed_roles = set(schema["allowedDocumentRole"])
    allowed_completeness = set(schema["allowedCompletenessStatus"])
    allowed_actions = set(schema["allowedRuleAction"])
    allowed_matches = set(schema["allowedMatchType"])
    allowed_extract_modes = set(schema["allowedExtractMode"])
    rule_sets = policy.get("ruleSets", {})
    review_items = 0
    partial_documents = 0
    for document in documents:
        source_path = str(document.get("sourcePath", "<missing>"))
        missing = sorted(set(schema["requiredDocumentFields"]) - set(document))
        _check(checks, f"classics_curation:{source_path}:required_fields", not missing, str(missing))
        source_row = source_by_path.get(source_path)
        _check(checks, f"classics_curation:{source_path}:source_manifest", source_row is not None, source_path)
        _check(
            checks,
            f"classics_curation:{source_path}:source_hash",
            source_row is not None and document["sourceSha256"] == source_row["sha256"],
            document["sourceSha256"],
        )
        _check(
            checks,
            f"classics_curation:{source_path}:document_role",
            document["documentRole"] in allowed_roles and document["roleStatus"] == "curator_assigned",
            f"{document['documentRole']} {document['roleStatus']}",
        )
        bibliography = document["bibliography"]
        _check(
            checks,
            f"classics_curation:{source_path}:bibliography_boundary",
            bibliography.get("reviewed") is None and bibliography.get("reviewStatus") == "review_required",
            str(bibliography.get("reviewStatus")),
        )
        completeness = document["completeness"]["status"]
        _check(
            checks,
            f"classics_curation:{source_path}:completeness",
            completeness in allowed_completeness,
            completeness,
        )
        partial_documents += completeness == "partial"
        selection = document["selection"]
        mode = selection.get("mode")
        ranges = selection.get("includeLineRanges", [])
        _check(
            checks,
            f"classics_curation:{source_path}:selection_mode",
            mode in set(schema["allowedSelectionMode"]) and bool(ranges) == (mode == "include_line_ranges"),
            str(mode),
        )
        references = selection.get("ruleSetRefs", [])
        _check(
            checks,
            f"classics_curation:{source_path}:rule_set_refs",
            all(reference in rule_sets for reference in references),
            str(references),
        )
        rules = [rule for reference in references for rule in rule_sets[reference]] + selection.get("lineRules", [])
        rule_ids = [rule.get("id") for rule in rules]
        _check(
            checks,
            f"classics_curation:{source_path}:rule_ids",
            len(rule_ids) == len(set(rule_ids)),
            str(rule_ids),
        )
        _check(
            checks,
            f"classics_curation:{source_path}:rule_contract",
            all(
                rule.get("action") in allowed_actions
                and rule.get("match", {}).get("type") in allowed_matches
                and bool(rule.get("match", {}).get("value"))
                and bool(rule.get("reason"))
                and (
                    rule.get("action") != "extract_and_exclude"
                    or (bool(rule.get("target")) and rule.get("extractMode") in allowed_extract_modes)
                )
                for rule in rules
            ),
            str(len(rules)),
        )
        review_items += len(document["reviewItems"])

    return {
        "policyId": policy["policyId"],
        "documentCount": len(documents),
        "familyCount": len({item["familyId"] for item in documents}),
        "partialDocumentCount": partial_documents,
        "reviewItemCount": review_items,
    }


def _validate_solar_terms_manifest(checks: list[dict[str, Any]]) -> dict[str, Any]:
    rows = _read_tsv(SOLAR_TERMS_SOURCE_MANIFEST)
    missing_columns = sorted({"system", "media_type", "relative_path", "bytes", "sha256", "source_name"} - set(rows[0]))
    _check(checks, "solar_terms:manifest_columns", not missing_columns, str(missing_columns))
    _check(checks, "solar_terms:manifest_row_count", len(rows) >= 4, str(len(rows)))
    _check(
        checks,
        "solar_terms:manifest_hash_format",
        all(SHA256_PATTERN.fullmatch(row["sha256"]) for row in rows),
        "all sha256 values are lowercase 64 hex",
    )
    return {"sourceRows": len(rows)}


def _validate_vendor_manifest(checks: list[dict[str, Any]]) -> dict[str, Any]:
    payload = _load_json(VENDOR_MANIFEST)
    production: list[str] = []
    audit_required: list[str] = []
    missing_license: list[str] = []
    for _, item in _iter_vendor_entries(payload):
        item_id = item.get("id", "<unknown>")
        if item.get("usageRole") == "production_dependency":
            production.append(item_id)
            if item.get("licenseStatus") != "spdx" or item.get("productionUseAllowed") is not True:
                missing_license.append(item_id)
        elif item.get("productionUseAllowed") is not False:
            missing_license.append(item_id)
        if item.get("auditRequired"):
            audit_required.append(item_id)

    _check(checks, "vendor:production_dependency_policy", not missing_license, str(missing_license))
    _check(checks, "vendor:has_production_dependencies", len(production) >= 2, str(production))
    _check(checks, "vendor:audit_required_tracked", len(audit_required) >= 1, str(len(audit_required)))

    return {
        "requiredCount": len(payload.get("required", [])),
        "optionalFutureFeatureCount": len(payload.get("optionalFutureFeatures", [])),
        "legacyUnreviewedSnapshotCount": len(payload.get("legacyUnreviewedSnapshots", [])),
        "productionDependencyIds": production,
        "auditRequiredCount": len(audit_required),
    }


def run_gate() -> dict[str, Any]:
    registry = _load_json(REGISTRY_PATH)
    schema = _load_json(SCHEMA_PATH)
    checks: list[dict[str, Any]] = []
    started = time.perf_counter()

    registry_summary = _validate_registry(registry=registry, schema=schema, checks=checks)
    classics_summary = _validate_classics(checks)
    classics_curation_summary = _validate_classics_curation(checks)
    solar_terms_summary = _validate_solar_terms_manifest(checks)
    vendor_summary = _validate_vendor_manifest(checks)

    return {
        "schemaVersion": 1,
        "generatedAt": datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "status": "passed",
        "gate": "data_supply_chain",
        "elapsedMs": round((time.perf_counter() - started) * 1000, 3),
        "summary": {
            "registry": registry_summary,
            "classics": classics_summary,
            "classicsCuration": classics_curation_summary,
            "solarTerms": solar_terms_summary,
            "vendor": vendor_summary,
        },
        "checks": checks,
        "privacyBoundary": "Data supply chain gate 只读取 tracked manifest、hash、license/status metadata，不读取真实用户、真实 token、secret、DSN、生产账号或 raw 私有资料。",
        "limits": [
            "不提供法律意见。",
            "不生成 SBOM/provenance artifact。",
            "不证明外部 raw 资料可公开分发。",
            "不改变 production provider 算法或运行时依赖。",
        ],
    }


def write_summary(summary: dict[str, Any], output_json: Path) -> None:
    output_json.parent.mkdir(parents=True, exist_ok=True)
    with output_json.open("w", encoding="utf-8") as fh:
        json.dump(summary, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="执行 FateCat data supply chain gate，并输出机器可读 JSON。")
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON, help="gate summary JSON 输出路径。")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        summary = run_gate()
        write_summary(summary, args.output_json)
        print(
            json.dumps(
                {
                    "status": summary["status"],
                    "assets": summary["summary"]["registry"]["assetCount"],
                    "classics": summary["summary"]["classics"]["canonicalTxtCount"],
                    "checks": len(summary["checks"]),
                    "elapsedMs": summary["elapsedMs"],
                },
                ensure_ascii=False,
            )
        )
        return 0
    except DataSupplyChainGateError as exc:
        print(f"data supply chain gate error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
