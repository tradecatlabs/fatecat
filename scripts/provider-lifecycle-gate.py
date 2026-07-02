#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
FATE_CORE_SRC = REPO_ROOT / "domains" / "fate-analysis" / "services" / "fate-core" / "src"
DEFAULT_OUTPUT_JSON = REPO_ROOT / "infra" / "runtime" / "local-state" / "exports" / "providers" / "lifecycle-gate.json"
PROVIDER_SCHEMA_PATH = REPO_ROOT / "contracts" / "fate" / "capabilities" / "schemas" / "provider.schema.json"
VENDOR_SOURCES_PATH = REPO_ROOT / "tools" / "reference-repos" / "vendor_sources.json"


class ProviderLifecycleGateError(RuntimeError):
    """provider lifecycle gate 未满足预期。"""


def _load_runtime():
    if str(FATE_CORE_SRC) not in sys.path:
        sys.path.insert(0, str(FATE_CORE_SRC))
    from fate_core.capabilities import list_capabilities, list_providers  # noqa: PLC0415

    return list_capabilities, list_providers


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _vendor_index() -> dict[str, dict[str, Any]]:
    data = _load_json(VENDOR_SOURCES_PATH)
    index: dict[str, dict[str, Any]] = {}
    for section in ("required", "optionalFutureFeatures", "legacyUnreviewedSnapshots"):
        for item in data.get(section, []):
            if isinstance(item, dict) and item.get("id"):
                index[str(item["id"])] = {**item, "_section": section}
    return index


def _check(condition: bool, name: str, details: str, checks: list[dict[str, Any]]) -> None:
    checks.append({"name": name, "ok": condition, "details": details})
    if not condition:
        raise ProviderLifecycleGateError(f"{name}: {details}")


def _resource_for_provider(provider: Any) -> dict[str, Any]:
    metadata = provider.metadata().as_dict()
    provider_id = metadata["providerId"]
    return {
        "resourceType": "Provider",
        "apiVersion": "fatecat.tradecatlabs/v1",
        "id": provider_id,
        **metadata,
        "health": provider.health().as_dict(),
        "links": {
            "self": f"/providers/{provider_id}",
            "collection": "/providers",
            "capabilities": "/capabilities",
            "errors": "/errors",
        },
        "metadata": {
            "interfaceVersion": metadata["interfaceVersion"],
            "adapterType": metadata["adapterType"],
            "healthScope": "in-process",
            "externalConnectivity": "外部连通验证待执行",
        },
    }


def _path_exists(ref: str) -> bool:
    if not ref or "#" in ref or "://" in ref:
        return True
    return (REPO_ROOT / ref).exists()


def _validate_refs(refs: list[str], name: str, checks: list[dict[str, Any]]) -> None:
    for ref in refs:
        _check(_path_exists(ref), f"{name}:{ref}", "path exists or external ref", checks)


def _validate_supply_chain(
    refs: list[str], vendor_index: dict[str, dict[str, Any]], checks: list[dict[str, Any]]
) -> None:
    for ref in refs:
        if not ref.startswith("tools/reference-repos/vendor_sources.json#"):
            continue
        vendor_id = ref.split("#", 1)[1]
        vendor = vendor_index.get(vendor_id)
        _check(vendor is not None, f"supply_chain_exists:{vendor_id}", ref, checks)
        _check(
            vendor.get("productionUseAllowed") is True,
            f"supply_chain_production_allowed:{vendor_id}",
            f"section={vendor.get('_section')} usageRole={vendor.get('usageRole')}",
            checks,
        )
        _check(
            vendor.get("licenseStatus") == "spdx",
            f"supply_chain_license_spdx:{vendor_id}",
            str(vendor.get("licenseStatus")),
            checks,
        )


def run_gate() -> dict[str, Any]:
    list_capabilities, list_providers = _load_runtime()
    provider_schema = _load_json(PROVIDER_SCHEMA_PATH)
    vendor_index = _vendor_index()
    checks: list[dict[str, Any]] = []

    production_capabilities = [item for item in list_capabilities() if item.status == "production"]
    providers = list_providers()
    provider_resources = [_resource_for_provider(provider) for provider in providers]
    providers_by_id = {item["providerId"]: item for item in provider_resources}

    _check(
        set(providers_by_id) == {item.provider for item in production_capabilities},
        "production_provider_coverage",
        f"providers={sorted(providers_by_id)}",
        checks,
    )

    for provider in provider_resources:
        provider_id = provider["providerId"]
        for field_name in provider_schema["requiredProviderFields"]:
            _check(field_name in provider, f"{provider_id}:required:{field_name}", "present", checks)

        for field_name in provider_schema["requiredLifecycleFields"]:
            _check(field_name in provider["lifecycle"], f"{provider_id}:lifecycle:{field_name}", "present", checks)
        _check(
            provider["lifecycle"]["stage"] in provider_schema["allowedLifecycleStage"],
            f"{provider_id}:lifecycle_stage",
            provider["lifecycle"]["stage"],
            checks,
        )
        _check(
            provider["lifecycle"]["status"] in provider_schema["allowedLifecycleStatus"],
            f"{provider_id}:lifecycle_status",
            provider["lifecycle"]["status"],
            checks,
        )

        for field_name in provider_schema["requiredSourcePolicyFields"]:
            _check(
                field_name in provider["sourcePolicy"], f"{provider_id}:source_policy:{field_name}", "present", checks
            )
        _validate_refs(provider["sourcePolicy"]["sourceRefs"], f"{provider_id}:source_ref", checks)
        _validate_supply_chain(provider["sourcePolicy"]["supplyChainRefs"], vendor_index, checks)

        for field_name in provider_schema["requiredLicensePolicyFields"]:
            _check(
                field_name in provider["licensePolicy"], f"{provider_id}:license_policy:{field_name}", "present", checks
            )
        _check(
            provider["licensePolicy"]["productionUseAllowed"] is True,
            f"{provider_id}:license_production_use_allowed",
            str(provider["licensePolicy"].get("productionUseAllowed")),
            checks,
        )
        _check(
            provider["licensePolicy"]["distributionAllowed"] is True,
            f"{provider_id}:license_distribution_allowed",
            str(provider["licensePolicy"].get("distributionAllowed")),
            checks,
        )
        _validate_refs(provider["licensePolicy"]["evidence"], f"{provider_id}:license_evidence", checks)

        for field_name in provider_schema["requiredResourceManifestFields"]:
            _check(
                field_name in provider["resourceManifest"],
                f"{provider_id}:resource_manifest:{field_name}",
                "present",
                checks,
            )
        _validate_refs(provider["resourceManifest"]["runtimeRefs"], f"{provider_id}:runtime_ref", checks)
        _validate_refs(provider["resourceManifest"]["contractRefs"], f"{provider_id}:contract_ref", checks)
        _validate_refs(provider["resourceManifest"]["testRefs"], f"{provider_id}:test_ref", checks)
        _validate_supply_chain(provider["resourceManifest"]["supplyChainRefs"], vendor_index, checks)

        for field_name in provider_schema["requiredPromotionGateFields"]:
            _check(
                field_name in provider["promotionGate"], f"{provider_id}:promotion_gate:{field_name}", "present", checks
            )
        _check(
            provider["promotionGate"]["status"] in provider_schema["allowedPromotionGateStatus"],
            f"{provider_id}:promotion_gate_status",
            provider["promotionGate"]["status"],
            checks,
        )
        _check(provider["promotionGate"]["commands"], f"{provider_id}:promotion_gate_commands", "non-empty", checks)

        for field_name in provider_schema["requiredDeprecationFields"]:
            _check(field_name in provider["deprecation"], f"{provider_id}:deprecation:{field_name}", "present", checks)
        _check(
            provider["deprecation"]["status"] in provider_schema["allowedDeprecationStatus"],
            f"{provider_id}:deprecation_status",
            provider["deprecation"]["status"],
            checks,
        )
        if provider["deprecation"]["status"] == "deprecated":
            _check(
                bool(provider["deprecation"]["replacementProvider"] or provider["deprecation"]["removalNotBefore"]),
                f"{provider_id}:deprecation_exit_plan",
                "replacementProvider or removalNotBefore required",
                checks,
            )

        _check(
            provider["versionLock"]["engineVersion"] == provider["engineVersion"],
            f"{provider_id}:version_lock_engine",
            provider["versionLock"]["engineVersion"],
            checks,
        )
        _check(
            provider["versionLock"]["interfaceVersion"] == provider["interfaceVersion"],
            f"{provider_id}:version_lock_interface",
            provider["versionLock"]["interfaceVersion"],
            checks,
        )

    return {
        "schemaVersion": 1,
        "generatedAt": datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "status": "passed",
        "providerCount": len(provider_resources),
        "checks": checks,
        "privacyBoundary": "provider lifecycle gate 只读取 registry、provider metadata 和 vendor manifest，不读取用户输入、报告正文、token、secret、DSN 或生产环境。",
    }


def write_summary(summary: dict[str, Any], output_json: Path) -> None:
    output_json.parent.mkdir(parents=True, exist_ok=True)
    with output_json.open("w", encoding="utf-8") as fh:
        json.dump(summary, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="执行 production provider lifecycle gate，并输出机器可读 JSON。")
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON, help="gate summary JSON 输出路径。")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        summary = run_gate()
        write_summary(summary, args.output_json)
        print(json.dumps({"status": summary["status"], "providers": summary["providerCount"]}, ensure_ascii=False))
        return 0
    except ProviderLifecycleGateError as exc:
        print(f"provider lifecycle gate error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
