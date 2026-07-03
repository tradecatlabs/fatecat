#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
OBSERVABILITY_DIR = REPO_ROOT / "contracts" / "fate" / "observability"
CONTRACT_PATH = OBSERVABILITY_DIR / "otel-backend-slo-evidence-contract.json"
DEFAULT_OUTPUT_JSON = (
    REPO_ROOT / "infra" / "runtime" / "local-state" / "exports" / "observability" / "otel-backend-slo-gate.json"
)

CONTROL_ID = "control.otel_backend_slo"
SENSITIVE_FRAGMENTS = {
    "BEGIN OPENSSH",
    "BEGIN RSA",
    "DATABASE_URL=",
    "DB_DSN=",
    "api_key=",
    "authorization:",
    "callback_url=",
    "password=",
    "private_key",
    "secret=",
    "token=",
    "webhook_url=",
}


class GateFailure(RuntimeError):
    """OTel backend/SLO staged evidence gate 失败。"""


def _load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as fh:
        payload = json.load(fh)
    if not isinstance(payload, dict):
        raise GateFailure(f"JSON top-level must be object: {path}")
    return payload


def _check(checks: list[dict[str, Any]], name: str, condition: bool, details: str) -> None:
    checks.append({"name": name, "ok": condition, "details": details})
    if not condition:
        raise GateFailure(f"{name}: {details}")


def _render(payload: Any) -> str:
    return json.dumps(payload, ensure_ascii=False, sort_keys=True)


def _assert_no_sensitive_fragments(checks: list[dict[str, Any]], name: str, payload: Any) -> None:
    rendered = _render(payload).lower()
    bad = sorted(fragment for fragment in SENSITIVE_FRAGMENTS if fragment.lower() in rendered)
    if re.search(r"https?://", rendered, re.I):
        bad.append("raw_url")
    _check(checks, name, not bad, ",".join(bad) or "clean")


def _scalar_values(value: Any) -> list[str]:
    if isinstance(value, dict):
        result: list[str] = []
        for item in value.values():
            result.extend(_scalar_values(item))
        return result
    if isinstance(value, list):
        result = []
        for item in value:
            result.extend(_scalar_values(item))
        return result
    return [str(value)]


def _contains_forbidden(value: Any, forbidden: list[str]) -> bool:
    text = " ".join(_scalar_values(value)).lower()
    return any(fragment.lower() in text for fragment in forbidden)


def _require_fields(area: str, payload: dict[str, Any], fields: list[str]) -> None:
    missing = [field for field in fields if field not in payload or payload[field] in ("", None, [])]
    if missing:
        raise GateFailure(f"{area}: missing fields {missing}")


def _validate_proof_refs(area: str, payload: dict[str, Any], fields: list[str], prefixes: list[str]) -> None:
    for field in fields:
        if not field.endswith("ProofRef"):
            continue
        value = str(payload.get(field) or "")
        if not value.startswith(tuple(prefixes)):
            raise GateFailure(f"{area}: {field} must use redacted proof ref prefix")


def validate_otel_backend_evidence(evidence: dict[str, Any], contract: dict[str, Any]) -> None:
    status = evidence.get("status")
    if status == "external_connectivity_pending":
        return
    if status != "external_live_passed":
        raise GateFailure(f"evidence: unsupported status {status!r}")

    backend = evidence.get("observabilityBackend")
    if not isinstance(backend, dict):
        raise GateFailure("observabilityBackend: required for external_live_passed")

    control = contract["controls"]["externalBackendSlo"]
    schema = control["liveEvidenceSchema"]
    required_fields = schema["requiredFields"]
    _require_fields("observabilityBackend", backend, required_fields)
    if backend["mode"] != control["requiredMode"]:
        raise GateFailure("observabilityBackend: mode is not external_otel_backend_slo")
    if backend["verificationStatus"] != control["requiredVerificationStatus"]:
        raise GateFailure("observabilityBackend: verificationStatus is not passed_external_otel_backend_slo_check")
    if backend["redactionBoundary"] != control["requiredRedactionBoundary"]:
        raise GateFailure("observabilityBackend: redactionBoundary must be redacted_no_secret_values")
    if backend["backendType"] in schema["forbiddenBackendValues"]:
        raise GateFailure("observabilityBackend: forbidden backendType")
    if backend["backendType"] not in control["allowedBackendTypes"]:
        raise GateFailure("observabilityBackend: unsupported backendType")
    _validate_proof_refs("observabilityBackend", backend, required_fields, schema["proofRefPrefixes"])
    if _contains_forbidden(backend, schema["forbiddenProofFragments"]):
        raise GateFailure("observabilityBackend: forbidden local, fake, placeholder, raw or payload proof")


def _validate_negative_cases(checks: list[dict[str, Any]], contract: dict[str, Any]) -> list[str]:
    rejected: list[str] = []
    for case in contract["negativeEvidenceCases"]:
        case_id = case["id"]
        expected = case["expectedErrorContains"]
        try:
            validate_otel_backend_evidence(case["evidence"], contract)
        except GateFailure as exc:
            message = str(exc)
            _check(checks, f"negative:{case_id}", expected in message, message)
            rejected.append(case_id)
        else:
            raise GateFailure(f"negative:{case_id}: fake evidence was accepted")
    return rejected


def _validate_contract(checks: list[dict[str, Any]], contract: dict[str, Any]) -> None:
    _check(
        checks,
        "contract_id",
        contract["contractId"] == "contract.otel_backend_slo_evidence",
        contract["contractId"],
    )
    _check(checks, "contract_status", contract["status"] == "dry_run_contract", contract["status"])
    _check(
        checks,
        "contract_external_pending",
        contract["externalConnectivity"] == "external_connectivity_pending",
        contract["externalConnectivity"],
    )
    _check(
        checks,
        "contract_controls",
        {"dryRunBaseline", "externalBackendSlo"} <= set(contract["controls"]),
        str(sorted({"dryRunBaseline", "externalBackendSlo"} - set(contract["controls"]))),
    )
    local_control = contract["controls"]["dryRunBaseline"]
    _check(checks, "local_control_id", local_control["controlId"] == CONTROL_ID, local_control["controlId"])
    _check(
        checks,
        "local_baseline_not_live",
        "does_not_prove_trace_backend_live" in local_control["nonClaims"],
        str(local_control["nonClaims"]),
    )
    external_control = contract["controls"]["externalBackendSlo"]
    _check(checks, "external_control_id", external_control["controlId"] == CONTROL_ID, external_control["controlId"])
    _check(
        checks,
        "live_schema_required_fields",
        len(external_control["liveEvidenceSchema"]["requiredFields"]) >= 13,
        str(external_control["liveEvidenceSchema"]["requiredFields"]),
    )
    _check(
        checks,
        "allowed_backend_types",
        {"grafana_stack", "prometheus_tempo_loki", "datadog", "cloud_monitoring"}
        <= set(external_control["allowedBackendTypes"]),
        str(external_control["allowedBackendTypes"]),
    )
    _check(
        checks,
        "negative_cases_present",
        len(contract["negativeEvidenceCases"]) >= 4,
        str(len(contract["negativeEvidenceCases"])),
    )
    _assert_no_sensitive_fragments(checks, "contract_no_sensitive_fragments", contract)


def _validate_registry_and_schema(
    checks: list[dict[str, Any]], registry: dict[str, Any], schema: dict[str, Any]
) -> None:
    _check(
        checks,
        "schema_allows_backend_slo_fields",
        "otelBackendSloEvidenceFields" in schema,
        str(schema.keys()),
    )
    _check(
        checks,
        "schema_backend_slo_invariant",
        "OTel backend/SLO staged evidence 不得被解释为真实 collector runtime、trace backend、metrics backend、production SLO、alert live 或 incident drill 已完成"
        in schema["invariants"],
        "present",
    )
    _check(
        checks,
        "registry_contract_link",
        registry["schemas"].get("otelBackendSloEvidenceContract")
        == "contracts/fate/observability/otel-backend-slo-evidence-contract.json",
        str(registry["schemas"].get("otelBackendSloEvidenceContract")),
    )
    signals = {item["id"]: item for item in registry["signals"]}
    _check(checks, "registry_signal_present", "signal.otel_backend_slo_evidence" in signals, str(sorted(signals)))
    signal = signals["signal.otel_backend_slo_evidence"]
    _check(checks, "registry_signal_available", signal["status"] == "available", signal["status"])
    _check(checks, "registry_signal_type", signal["signalType"] == "slo", signal["signalType"])
    _check(
        checks,
        "registry_signal_external_pending",
        signal["externalConnectivity"] == "external_connectivity_pending",
        signal["externalConnectivity"],
    )
    _check(
        checks,
        "registry_signal_gate_linked",
        any("bash scripts/otel-backend-slo-gate.sh" in item for item in signal["localVerification"]),
        str(signal["localVerification"]),
    )
    metadata = registry["metadata"]
    _check(
        checks,
        "registry_backend_gate_command",
        metadata.get("otelBackendSloGateCommand") == "bash scripts/otel-backend-slo-gate.sh",
        str(metadata.get("otelBackendSloGateCommand")),
    )
    _check(
        checks,
        "registry_backend_contract",
        metadata.get("otelBackendSloEvidenceContract")
        == "contracts/fate/observability/otel-backend-slo-evidence-contract.json",
        str(metadata.get("otelBackendSloEvidenceContract")),
    )


def run_gate(evidence_json: Path | None = None) -> dict[str, Any]:
    contract = _load_json(CONTRACT_PATH)
    registry = _load_json(OBSERVABILITY_DIR / "registry.json")
    schema = _load_json(OBSERVABILITY_DIR / "schemas" / "observability-signal.schema.json")
    checks: list[dict[str, Any]] = []

    _validate_contract(checks, contract)
    _validate_registry_and_schema(checks, registry, schema)
    rejected_negative_cases = _validate_negative_cases(checks, contract)

    live_evidence_status = "外部连通验证待执行"
    if evidence_json is not None:
        evidence = _load_json(evidence_json)
        _assert_no_sensitive_fragments(checks, "evidence_no_sensitive_fragments", evidence)
        validate_otel_backend_evidence(evidence, contract)
        if evidence.get("status") == "external_live_passed":
            live_evidence_status = "external_live_passed"

    return {
        "schemaVersion": 1,
        "kind": "fatecat.otel_backend_slo_gate_summary",
        "generatedAt": datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "status": "passed",
        "contract": "contracts/fate/observability/otel-backend-slo-evidence-contract.json",
        "controls": [CONTROL_ID],
        "checks": checks,
        "negativeEvidenceRejected": rejected_negative_cases,
        "liveEvidenceStatus": live_evidence_status,
        "externalConnectivity": "外部连通验证待执行",
        "privacyBoundary": "gate 只读取 contract、registry、schema 和可选脱敏 proof refs；不读取真实 logs、metrics、traces、dashboard URL、用户输入、token、secret、DSN 或报告正文。",
    }


def write_summary(summary: dict[str, Any], output_json: Path) -> None:
    output_json.parent.mkdir(parents=True, exist_ok=True)
    with output_json.open("w", encoding="utf-8") as fh:
        json.dump(summary, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="校验 OTel backend/SLO staged evidence contract。")
    parser.add_argument("--evidence-json", type=Path, help="可选脱敏 external live evidence JSON。")
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON, help="gate summary 输出路径。")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        summary = run_gate(evidence_json=args.evidence_json)
        write_summary(summary, args.output_json)
        print(
            json.dumps(
                {
                    "status": summary["status"],
                    "liveEvidenceStatus": summary["liveEvidenceStatus"],
                    "negativeEvidenceRejected": len(summary["negativeEvidenceRejected"]),
                    "checks": len(summary["checks"]),
                },
                ensure_ascii=False,
                sort_keys=True,
            )
        )
        return 0
    except (GateFailure, OSError, json.JSONDecodeError) as exc:
        print(f"otel backend slo gate error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
