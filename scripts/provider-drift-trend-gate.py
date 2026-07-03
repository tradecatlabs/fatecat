#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from types import ModuleType
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_JSON = REPO_ROOT / "infra" / "runtime" / "local-state" / "exports" / "providers" / "drift-trend.json"
CONTRACT_PATH = REPO_ROOT / "contracts" / "fate" / "capabilities" / "provider-drift-trend-contract.json"
BASELINE_PATH = REPO_ROOT / "contracts" / "fate" / "capabilities" / "provider-drift-baseline.json"
SCANNER_PATH = REPO_ROOT / "scripts" / "provider-drift-scanner.py"


class ProviderDriftTrendGateError(RuntimeError):
    """provider/source/license 趋势门禁发现阻断项。"""


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_script_module(path: Path, module_name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise ProviderDriftTrendGateError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _canonical(payload: Any) -> str:
    return json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _fingerprint(payload: Any) -> str:
    return "sha256:" + hashlib.sha256(_canonical(payload).encode("utf-8")).hexdigest()


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
        finding: dict[str, Any] = {"severity": severity, "name": name, "details": details}
        if provider_id:
            finding["providerId"] = provider_id
        findings.append(finding)


def _provider_identity(provider: dict[str, Any]) -> dict[str, Any]:
    return {
        "providerId": provider["providerId"],
        "capabilityIds": sorted(provider.get("capabilityIds", [])),
        "engineVersion": provider["engineVersion"],
        "lifecycleStage": provider["lifecycleStage"],
    }


def _source_snapshot(provider: dict[str, Any]) -> dict[str, Any]:
    source = provider.get("source") or {}
    return {
        "sourceRefs": sorted(provider.get("sourceRefs", source.get("sourceRefs", []))),
        "supplyChainRefs": sorted(provider.get("supplyChainRefs", source.get("supplyChainRefs", []))),
    }


def _license_snapshot(provider: dict[str, Any]) -> dict[str, Any]:
    license_policy = provider["license"]
    return {
        "license": license_policy.get("license"),
        "licenseStatus": license_policy.get("licenseStatus"),
        "productionUseAllowed": license_policy.get("productionUseAllowed"),
        "distributionAllowed": license_policy.get("distributionAllowed"),
        "evidence": sorted(license_policy.get("evidence", [])),
    }


def _vendor_snapshot(provider: dict[str, Any]) -> list[dict[str, Any]]:
    vendor_rows = provider.get("vendorSupplyChain", provider.get("supplyChain", []))
    normalized: list[dict[str, Any]] = []
    for vendor in vendor_rows:
        normalized.append(
            {
                "id": vendor.get("id"),
                "usageRole": vendor.get("usageRole"),
                "license": vendor.get("license"),
                "licenseStatus": vendor.get("licenseStatus"),
                "productionUseAllowed": vendor.get("productionUseAllowed"),
                "snapshotSha256": vendor.get("snapshotSha256"),
            }
        )
    return sorted(normalized, key=lambda item: str(item.get("id")))


def _provider_snapshot(provider: dict[str, Any]) -> dict[str, Any]:
    identity = _provider_identity(provider)
    source = _source_snapshot(provider)
    license_policy = _license_snapshot(provider)
    vendor = _vendor_snapshot(provider)
    fingerprints = {
        "sourceFingerprint": _fingerprint(source),
        "licenseFingerprint": _fingerprint(license_policy),
        "vendorFingerprint": _fingerprint(vendor),
        "providerFingerprint": _fingerprint(
            {"identity": identity, "source": source, "license": license_policy, "vendor": vendor}
        ),
    }
    return {
        **identity,
        "source": source,
        "license": license_policy,
        "vendorSupplyChain": vendor,
        "fingerprints": fingerprints,
    }


def _snapshot_from_drift_report(report: dict[str, Any]) -> dict[str, Any]:
    providers = [_provider_snapshot(provider) for provider in report.get("providers", [])]
    providers.sort(key=lambda item: item["providerId"])
    return {
        "providerCount": report.get("providerCount"),
        "capabilityCount": report.get("capabilityCount"),
        "providers": providers,
    }


def _assert_privacy(summary: dict[str, Any], contract: dict[str, Any]) -> None:
    rendered = _canonical(summary)
    forbidden = [fragment for fragment in contract.get("forbiddenReportFragments", []) if str(fragment) in rendered]
    if forbidden:
        joined = ", ".join(forbidden)
        raise ProviderDriftTrendGateError(f"provider drift trend report contains forbidden fragments: {joined}")


def _validate_baseline(
    baseline: dict[str, Any],
    contract: dict[str, Any],
    checks: list[dict[str, Any]],
    findings: list[dict[str, Any]],
) -> None:
    _append_check(
        checks,
        findings,
        "baseline_kind",
        baseline.get("kind") == contract["baselineKind"],
        str(baseline.get("kind")),
    )
    missing = sorted(set(contract["requiredBaselineFields"]) - set(baseline))
    _append_check(checks, findings, "baseline_required_fields", not missing, str(missing))
    _append_check(
        checks,
        findings,
        "baseline_source_report_kind",
        baseline.get("sourceReportKind") == contract["driftReportKind"],
        str(baseline.get("sourceReportKind")),
    )
    for provider in baseline.get("providers", []):
        provider_id = str(provider.get("providerId", "<missing>"))
        missing_provider_fields = sorted(set(contract["requiredProviderFields"]) - set(provider))
        _append_check(
            checks,
            findings,
            f"baseline_provider_required_fields:{provider_id}",
            not missing_provider_fields,
            str(missing_provider_fields),
            provider_id=provider_id,
        )
        missing_fingerprints = sorted(
            set(contract["requiredFingerprintFields"]) - set(provider.get("fingerprints", {}))
        )
        _append_check(
            checks,
            findings,
            f"baseline_provider_fingerprints:{provider_id}",
            not missing_fingerprints,
            str(missing_fingerprints),
            provider_id=provider_id,
        )


def _compare_snapshots(
    baseline: dict[str, Any],
    current: dict[str, Any],
    checks: list[dict[str, Any]],
    findings: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    baseline_by_provider = {provider["providerId"]: provider for provider in baseline.get("providers", [])}
    current_by_provider = {provider["providerId"]: provider for provider in current.get("providers", [])}
    baseline_ids = set(baseline_by_provider)
    current_ids = set(current_by_provider)
    _append_check(
        checks,
        findings,
        "provider_set_matches_baseline",
        baseline_ids == current_ids,
        f"baseline={sorted(baseline_ids)} current={sorted(current_ids)}",
    )
    _append_check(
        checks,
        findings,
        "provider_count_matches_baseline",
        baseline.get("providerCount") == current.get("providerCount"),
        f"{baseline.get('providerCount')} == {current.get('providerCount')}",
    )
    _append_check(
        checks,
        findings,
        "capability_count_matches_baseline",
        baseline.get("capabilityCount") == current.get("capabilityCount"),
        f"{baseline.get('capabilityCount')} == {current.get('capabilityCount')}",
    )

    trend_rows: list[dict[str, Any]] = []
    for provider_id in sorted(current_ids & baseline_ids):
        base = baseline_by_provider[provider_id]
        now = current_by_provider[provider_id]
        provider_findings_before = len(findings)
        for field_name in ("capabilityIds", "engineVersion", "lifecycleStage"):
            _append_check(
                checks,
                findings,
                f"{provider_id}:identity:{field_name}",
                base.get(field_name) == now.get(field_name),
                f"{base.get(field_name)} == {now.get(field_name)}",
                provider_id=provider_id,
            )
        for fingerprint_name in ("sourceFingerprint", "licenseFingerprint", "vendorFingerprint", "providerFingerprint"):
            _append_check(
                checks,
                findings,
                f"{provider_id}:fingerprint:{fingerprint_name}",
                base["fingerprints"].get(fingerprint_name) == now["fingerprints"].get(fingerprint_name),
                f"{base['fingerprints'].get(fingerprint_name)} == {now['fingerprints'].get(fingerprint_name)}",
                provider_id=provider_id,
            )
        license_policy = now["license"]
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
        for vendor in now["vendorSupplyChain"]:
            vendor_id = str(vendor.get("id"))
            _append_check(
                checks,
                findings,
                f"{provider_id}:vendor_production_allowed:{vendor_id}",
                vendor.get("productionUseAllowed") is True,
                str(vendor.get("productionUseAllowed")),
                provider_id=provider_id,
            )
            _append_check(
                checks,
                findings,
                f"{provider_id}:vendor_license_spdx:{vendor_id}",
                vendor.get("licenseStatus") == "spdx",
                str(vendor.get("licenseStatus")),
                provider_id=provider_id,
            )
        trend_rows.append(
            {
                "providerId": provider_id,
                "status": "passed" if len(findings) == provider_findings_before else "failed",
                "fingerprints": now["fingerprints"],
            }
        )
    return trend_rows


def _load_drift_report(scanner_report_path: Path | None) -> dict[str, Any]:
    if scanner_report_path is not None:
        return _load_json(scanner_report_path)
    scanner = _load_script_module(SCANNER_PATH, "fatecat_provider_drift_scanner_for_trend")
    return scanner.run_scanner()


def run_gate(*, baseline_path: Path = BASELINE_PATH, scanner_report_path: Path | None = None) -> dict[str, Any]:
    contract = _load_json(CONTRACT_PATH)
    baseline = _load_json(baseline_path)
    drift_report = _load_drift_report(scanner_report_path)
    current = _snapshot_from_drift_report(drift_report)
    checks: list[dict[str, Any]] = []
    findings: list[dict[str, Any]] = []

    _append_check(
        checks,
        findings,
        "contract_kind",
        contract.get("reportKind") == "fatecat.provider_drift_trend_report",
        str(contract.get("reportKind")),
    )
    _append_check(
        checks,
        findings,
        "scanner_report_kind",
        drift_report.get("kind") == contract["driftReportKind"],
        str(drift_report.get("kind")),
    )
    _append_check(
        checks,
        findings,
        "scanner_report_passed",
        drift_report.get("status") == "passed" and drift_report.get("findingCount") == 0,
        f"status={drift_report.get('status')} findings={drift_report.get('findingCount')}",
    )
    _validate_baseline(baseline, contract, checks, findings)
    trend_rows = _compare_snapshots(baseline, current, checks, findings)

    summary: dict[str, Any] = {
        "schemaVersion": 1,
        "generatedAt": datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "kind": contract["reportKind"],
        "status": "passed" if not findings else "failed",
        "baseline": {
            "path": str(baseline_path.relative_to(REPO_ROOT))
            if baseline_path.is_relative_to(REPO_ROOT)
            else str(baseline_path),
            "baselineId": baseline.get("baselineId"),
            "providerCount": baseline.get("providerCount"),
            "capabilityCount": baseline.get("capabilityCount"),
        },
        "current": {
            "sourceReportKind": drift_report.get("kind"),
            "providerCount": current.get("providerCount"),
            "capabilityCount": current.get("capabilityCount"),
            "scannerFindingCount": drift_report.get("findingCount"),
            "scannerSpanCount": drift_report.get("spanCount"),
        },
        "providerTrend": trend_rows,
        "checkCount": len(checks),
        "findingCount": len(findings),
        "findings": findings,
        "checks": checks,
        "externalConnectivity": "外部连通验证待执行",
        "privacyBoundary": contract["privacyBoundary"],
        "releaseBoundary": contract["releaseBoundary"],
    }
    _assert_privacy(summary, contract)
    return summary


def write_summary(summary: dict[str, Any], output_json: Path) -> None:
    output_json.parent.mkdir(parents=True, exist_ok=True)
    with output_json.open("w", encoding="utf-8") as fh:
        json.dump(summary, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="验证 provider/source/license/vendor 长期趋势 baseline。")
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON, help="趋势门禁 JSON 输出路径。")
    parser.add_argument("--baseline-json", type=Path, default=BASELINE_PATH, help="tracked baseline JSON。")
    parser.add_argument(
        "--scanner-report-json",
        type=Path,
        default=None,
        help="可选：复用已生成的 provider drift report；默认重新运行 provider drift scanner。",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        summary = run_gate(baseline_path=args.baseline_json, scanner_report_path=args.scanner_report_json)
        write_summary(summary, args.output_json)
        print(
            json.dumps(
                {
                    "status": summary["status"],
                    "providers": summary["current"]["providerCount"],
                    "findings": summary["findingCount"],
                    "baseline": summary["baseline"]["baselineId"],
                },
                ensure_ascii=False,
            )
        )
        return 0 if summary["status"] == "passed" else 1
    except (ProviderDriftTrendGateError, KeyError, OSError, json.JSONDecodeError) as exc:
        print(f"provider drift trend gate error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
