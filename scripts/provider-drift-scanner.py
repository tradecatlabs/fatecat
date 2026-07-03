#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import io
import json
import logging
import sys
from datetime import UTC, datetime
from pathlib import Path
from types import ModuleType
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
FATE_CORE_SRC = REPO_ROOT / "domains" / "fate-analysis" / "services" / "fate-core" / "src"
DEFAULT_OUTPUT_JSON = REPO_ROOT / "infra" / "runtime" / "local-state" / "exports" / "providers" / "drift-report.json"
PROVIDER_LIFECYCLE_GATE_PATH = REPO_ROOT / "scripts" / "provider-lifecycle-gate.py"
PROVIDER_DEPENDENCY_SMOKE_PATH = REPO_ROOT / "scripts" / "provider-dependency-smoke.py"
PROVIDER_DRIFT_CONTRACT_PATH = REPO_ROOT / "contracts" / "fate" / "capabilities" / "provider-drift-contract.json"
PROVIDER_SCHEMA_PATH = REPO_ROOT / "contracts" / "fate" / "capabilities" / "schemas" / "provider.schema.json"
OBSERVABILITY_REGISTRY_PATH = REPO_ROOT / "contracts" / "fate" / "observability" / "registry.json"
VENDOR_SOURCES_PATH = REPO_ROOT / "tools" / "reference-repos" / "vendor_sources.json"
TRACE_LOGGER_NAME = "fate_core.observability"


class ProviderDriftScannerError(RuntimeError):
    """provider drift scanner 发现阻断项。"""


def _load_runtime():
    if str(FATE_CORE_SRC) not in sys.path:
        sys.path.insert(0, str(FATE_CORE_SRC))
    from fate_core.capabilities import (  # noqa: PLC0415
        CapabilityExecutor,
        CapabilityInput,
        list_capabilities,
        list_providers,
    )

    return CapabilityExecutor, CapabilityInput, list_capabilities, list_providers


def _load_script_module(path: Path, module_name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise ProviderDriftScannerError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _render(payload: Any) -> str:
    return json.dumps(payload, ensure_ascii=False, sort_keys=True)


def _append_check(
    checks: list[dict[str, Any]],
    findings: list[dict[str, Any]],
    name: str,
    ok: bool,
    details: str,
    *,
    provider_id: str | None = None,
    severity: str = "block",
) -> None:
    checks.append({"name": name, "ok": ok, "details": details})
    if not ok:
        finding: dict[str, Any] = {
            "severity": severity,
            "name": name,
            "details": details,
        }
        if provider_id:
            finding["providerId"] = provider_id
        findings.append(finding)


def _path_exists(ref: str) -> bool:
    if not ref or "#" in ref or "://" in ref:
        return True
    return (REPO_ROOT / ref).exists()


def _vendor_index() -> dict[str, dict[str, Any]]:
    data = _load_json(VENDOR_SOURCES_PATH)
    index: dict[str, dict[str, Any]] = {}
    for section in ("required", "optionalFutureFeatures", "legacyUnreviewedSnapshots"):
        for item in data.get(section, []):
            if isinstance(item, dict) and item.get("id"):
                index[str(item["id"])] = {**item, "_section": section}
    return index


def _vendor_id(ref: str) -> str | None:
    prefix = "tools/reference-repos/vendor_sources.json#"
    if not ref.startswith(prefix):
        return None
    return ref.split("#", 1)[1]


def _span_events(log_text: str) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    for line in log_text.splitlines():
        try:
            payload = json.loads(line)
        except json.JSONDecodeError:
            continue
        if payload.get("event") == "trace_span":
            events.append(payload)
    return events


def _capture_provider_spans(sample_payloads: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    CapabilityExecutor, CapabilityInput, list_capabilities, _list_providers = _load_runtime()
    executor = CapabilityExecutor()
    production_capabilities = [item for item in list_capabilities() if item.status == "production"]

    log_stream = io.StringIO()
    handler = logging.StreamHandler(log_stream)
    trace_logger = logging.getLogger(TRACE_LOGGER_NAME)
    previous_level = trace_logger.level
    trace_logger.addHandler(handler)
    trace_logger.setLevel(logging.INFO)

    try:
        for capability in production_capabilities:
            payload = sample_payloads.get(capability.capability_id)
            if payload is None:
                continue
            executor.execute(CapabilityInput(capability_id=capability.capability_id, payload=payload))
        return _span_events(log_stream.getvalue())
    finally:
        trace_logger.removeHandler(handler)
        trace_logger.setLevel(previous_level)


def _trace_status(provider_id: str, capability_id: str, spans: list[dict[str, Any]]) -> dict[str, Any]:
    matched = [
        span
        for span in spans
        if span.get("attributes", {}).get("providerId") == provider_id
        and span.get("attributes", {}).get("capabilityId") == capability_id
    ]
    span_names = sorted({str(span.get("spanName")) for span in matched if span.get("spanName")})
    return {
        "spanCount": len(matched),
        "spanNames": span_names,
        "hasValidate": "provider.validate" in span_names,
        "hasCalculate": "provider.calculate" in span_names,
    }


def _observability_trace_signal() -> dict[str, Any] | None:
    registry = _load_json(OBSERVABILITY_REGISTRY_PATH)
    for signal in registry.get("signals", []):
        if signal.get("id") == "signal.provider_report_traces":
            return signal
    return None


def _validate_contract(
    contract: dict[str, Any],
    checks: list[dict[str, Any]],
    findings: list[dict[str, Any]],
) -> None:
    _append_check(
        checks,
        findings,
        "contract_kind",
        contract.get("reportKind") == "fatecat.provider_drift_report",
        str(contract.get("reportKind")),
    )
    _append_check(
        checks,
        findings,
        "contract_required_spans",
        {"provider.validate", "provider.calculate"} <= set(contract.get("requiredTraceSpanNames", [])),
        str(contract.get("requiredTraceSpanNames", [])),
    )
    for ref in contract.get("requiredLocalSources", []):
        _append_check(checks, findings, f"contract_source:{ref}", _path_exists(str(ref)), "path exists")


def _validate_observability_signal(checks: list[dict[str, Any]], findings: list[dict[str, Any]]) -> None:
    signal = _observability_trace_signal()
    _append_check(checks, findings, "trace_signal_exists", signal is not None, "signal.provider_report_traces")
    if signal is None:
        return
    _append_check(
        checks, findings, "trace_signal_available", signal.get("status") == "available", str(signal.get("status"))
    )
    _append_check(
        checks,
        findings,
        "trace_signal_verification",
        any("observability-trace-slo-smoke.sh" in item for item in signal.get("localVerification", [])),
        str(signal.get("localVerification", [])),
    )


def _validate_provider(
    provider_metadata: dict[str, Any],
    capability_by_provider: dict[str, list[Any]],
    dependency_by_capability: dict[str, dict[str, Any]],
    vendor_index: dict[str, dict[str, Any]],
    spans: list[dict[str, Any]],
    checks: list[dict[str, Any]],
    findings: list[dict[str, Any]],
) -> dict[str, Any]:
    provider_id = provider_metadata["providerId"]
    capabilities = capability_by_provider.get(provider_id, [])
    source_policy = provider_metadata["sourcePolicy"]
    license_policy = provider_metadata["licensePolicy"]
    resource_manifest = provider_metadata["resourceManifest"]
    supply_chain_refs = list(source_policy.get("supplyChainRefs", []))

    provider_checks_before = len(findings)
    capability_ids = [capability.capability_id for capability in capabilities]
    trace_summaries: dict[str, dict[str, Any]] = {}
    dependency_summaries: dict[str, dict[str, Any]] = {}

    _append_check(
        checks,
        findings,
        f"{provider_id}:capability_coverage",
        bool(capability_ids),
        str(capability_ids),
        provider_id=provider_id,
    )
    for capability in capabilities:
        _append_check(
            checks,
            findings,
            f"{provider_id}:{capability.capability_id}:engine_version",
            capability.engine_version == provider_metadata["engineVersion"],
            f"{capability.engine_version} == {provider_metadata['engineVersion']}",
            provider_id=provider_id,
        )
        dependency = dependency_by_capability.get(capability.capability_id)
        _append_check(
            checks,
            findings,
            f"{provider_id}:{capability.capability_id}:dependency_smoke",
            dependency is not None,
            "dependency smoke result present",
            provider_id=provider_id,
        )
        if dependency is not None:
            dependency_summaries[capability.capability_id] = {
                "engineVersion": dependency.get("engineVersion"),
                "healthStatus": dependency.get("healthStatus"),
                "dependencyRefs": dependency.get("dependencyRefs", []),
            }
            _append_check(
                checks,
                findings,
                f"{provider_id}:{capability.capability_id}:dependency_engine",
                dependency.get("engineVersion") == provider_metadata["engineVersion"],
                str(dependency.get("engineVersion")),
                provider_id=provider_id,
            )
            _append_check(
                checks,
                findings,
                f"{provider_id}:{capability.capability_id}:dependency_refs",
                set(dependency.get("dependencyRefs", [])) == set(supply_chain_refs),
                f"{dependency.get('dependencyRefs', [])}",
                provider_id=provider_id,
            )

        trace_summary = _trace_status(provider_id, capability.capability_id, spans)
        trace_summaries[capability.capability_id] = trace_summary
        _append_check(
            checks,
            findings,
            f"{provider_id}:{capability.capability_id}:trace_validate",
            trace_summary["hasValidate"],
            str(trace_summary["spanNames"]),
            provider_id=provider_id,
        )
        _append_check(
            checks,
            findings,
            f"{provider_id}:{capability.capability_id}:trace_calculate",
            trace_summary["hasCalculate"],
            str(trace_summary["spanNames"]),
            provider_id=provider_id,
        )

    for ref_group, refs in (
        ("source_ref", source_policy.get("sourceRefs", [])),
        ("runtime_ref", resource_manifest.get("runtimeRefs", [])),
        ("contract_ref", resource_manifest.get("contractRefs", [])),
        ("test_ref", resource_manifest.get("testRefs", [])),
        ("license_evidence", license_policy.get("evidence", [])),
    ):
        for ref in refs:
            _append_check(
                checks,
                findings,
                f"{provider_id}:{ref_group}:{ref}",
                _path_exists(str(ref)),
                "path exists",
                provider_id=provider_id,
            )

    _append_check(
        checks,
        findings,
        f"{provider_id}:resource_supply_chain_matches_source",
        set(resource_manifest.get("supplyChainRefs", [])) == set(supply_chain_refs),
        str(resource_manifest.get("supplyChainRefs", [])),
        provider_id=provider_id,
    )
    _append_check(
        checks,
        findings,
        f"{provider_id}:license_production_allowed",
        license_policy.get("productionUseAllowed") is True,
        str(license_policy.get("productionUseAllowed")),
        provider_id=provider_id,
    )
    _append_check(
        checks,
        findings,
        f"{provider_id}:license_distribution_allowed",
        license_policy.get("distributionAllowed") is True,
        str(license_policy.get("distributionAllowed")),
        provider_id=provider_id,
    )

    supply_chain_summary: list[dict[str, Any]] = []
    for ref in supply_chain_refs:
        vendor_id = _vendor_id(str(ref))
        vendor = vendor_index.get(vendor_id or "")
        _append_check(
            checks,
            findings,
            f"{provider_id}:vendor_exists:{vendor_id}",
            vendor is not None,
            str(ref),
            provider_id=provider_id,
        )
        if vendor is None:
            continue
        supply_chain_summary.append(
            {
                "id": vendor["id"],
                "usageRole": vendor.get("usageRole"),
                "license": vendor.get("license"),
                "licenseStatus": vendor.get("licenseStatus"),
                "productionUseAllowed": vendor.get("productionUseAllowed"),
                "snapshotSha256": vendor.get("snapshotSha256"),
            }
        )
        _append_check(
            checks,
            findings,
            f"{provider_id}:vendor_production_allowed:{vendor['id']}",
            vendor.get("productionUseAllowed") is True,
            str(vendor.get("productionUseAllowed")),
            provider_id=provider_id,
        )
        _append_check(
            checks,
            findings,
            f"{provider_id}:vendor_license_spdx:{vendor['id']}",
            vendor.get("licenseStatus") == "spdx",
            str(vendor.get("licenseStatus")),
            provider_id=provider_id,
        )

    drift_status = "passed" if len(findings) == provider_checks_before else "failed"
    return {
        "providerId": provider_id,
        "capabilityIds": capability_ids,
        "engineVersion": provider_metadata["engineVersion"],
        "lifecycleStage": provider_metadata["lifecycle"]["stage"],
        "sourceRefs": list(source_policy.get("sourceRefs", [])),
        "supplyChainRefs": supply_chain_refs,
        "license": {
            "license": license_policy.get("license"),
            "licenseStatus": license_policy.get("licenseStatus"),
            "productionUseAllowed": license_policy.get("productionUseAllowed"),
            "distributionAllowed": license_policy.get("distributionAllowed"),
            "evidence": list(license_policy.get("evidence", [])),
        },
        "dependencySmoke": dependency_summaries,
        "traceSpans": trace_summaries,
        "supplyChain": supply_chain_summary,
        "driftStatus": drift_status,
    }


def _assert_report_privacy(summary: dict[str, Any], contract: dict[str, Any]) -> None:
    rendered = _render(summary)
    forbidden = [fragment for fragment in contract.get("forbiddenReportFragments", []) if str(fragment) in rendered]
    if forbidden:
        raise ProviderDriftScannerError(f"provider drift report contains forbidden fragments: {', '.join(forbidden)}")


def run_scanner() -> dict[str, Any]:
    CapabilityExecutor, _CapabilityInput, list_capabilities, list_providers = _load_runtime()
    _ = CapabilityExecutor
    lifecycle_gate = _load_script_module(PROVIDER_LIFECYCLE_GATE_PATH, "fatecat_provider_lifecycle_gate_for_drift")
    dependency_smoke = _load_script_module(
        PROVIDER_DEPENDENCY_SMOKE_PATH, "fatecat_provider_dependency_smoke_for_drift"
    )

    contract = _load_json(PROVIDER_DRIFT_CONTRACT_PATH)
    _load_json(PROVIDER_SCHEMA_PATH)
    vendor_index = _vendor_index()
    checks: list[dict[str, Any]] = []
    findings: list[dict[str, Any]] = []

    _validate_contract(contract, checks, findings)
    _validate_observability_signal(checks, findings)

    lifecycle_summary = lifecycle_gate.run_gate()
    dependency_summary = dependency_smoke.run_smoke()
    spans = _capture_provider_spans(dependency_smoke.SAMPLE_PAYLOADS)

    _append_check(
        checks,
        findings,
        "lifecycle_gate_status",
        lifecycle_summary.get("status") == "passed",
        str(lifecycle_summary.get("status")),
    )
    _append_check(
        checks,
        findings,
        "dependency_smoke_status",
        dependency_summary.get("status") == "passed",
        str(dependency_summary.get("status")),
    )
    _append_check(checks, findings, "provider_span_count", len(spans) >= 8, str(len(spans)))

    production_capabilities = [item for item in list_capabilities() if item.status == "production"]
    providers = [provider.metadata().as_dict() for provider in list_providers()]
    capability_by_provider: dict[str, list[Any]] = {}
    for capability in production_capabilities:
        capability_by_provider.setdefault(capability.provider, []).append(capability)
    dependency_by_capability = {
        item["capabilityId"]: item for item in dependency_summary.get("providers", []) if isinstance(item, dict)
    }

    provider_reports = [
        _validate_provider(
            provider_metadata,
            capability_by_provider,
            dependency_by_capability,
            vendor_index,
            spans,
            checks,
            findings,
        )
        for provider_metadata in providers
    ]
    status = "passed" if not findings else "failed"
    summary: dict[str, Any] = {
        "schemaVersion": 1,
        "generatedAt": datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "kind": "fatecat.provider_drift_report",
        "status": status,
        "providerCount": len(providers),
        "capabilityCount": len(production_capabilities),
        "spanCount": len(spans),
        "findingCount": len(findings),
        "providers": provider_reports,
        "findings": findings,
        "checks": checks,
        "externalConnectivity": "外部连通验证待执行",
        "privacyBoundary": "provider drift scanner 只使用脱敏固定样例和本地 provider span 聚合属性；不读取真实 .env、token、secret、DSN、用户报告正文或生产外部账号。",
    }
    _assert_report_privacy(summary, contract)
    return summary


def write_summary(summary: dict[str, Any], output_json: Path) -> None:
    output_json.parent.mkdir(parents=True, exist_ok=True)
    with output_json.open("w", encoding="utf-8") as fh:
        json.dump(summary, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="执行 production provider drift scanner，并输出机器可读 JSON。")
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON, help="drift report JSON 输出路径。")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        summary = run_scanner()
        write_summary(summary, args.output_json)
        print(
            json.dumps(
                {
                    "status": summary["status"],
                    "providers": summary["providerCount"],
                    "findings": summary["findingCount"],
                    "spans": summary["spanCount"],
                },
                ensure_ascii=False,
            )
        )
        return 0 if summary["status"] == "passed" else 1
    except (ProviderDriftScannerError, OSError, json.JSONDecodeError) as exc:
        print(f"provider drift scanner error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
