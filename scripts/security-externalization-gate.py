#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
SECURITY_DIR = REPO_ROOT / "contracts" / "fate" / "security"
CONTRACT_PATH = SECURITY_DIR / "externalization-evidence-contract.json"
DEFAULT_OUTPUT_JSON = (
    REPO_ROOT / "infra" / "runtime" / "local-state" / "exports" / "security" / "security-externalization-gate.json"
)

REQUIRED_CONTROL_IDS = {
    "control.production_identity_oidc",
    "control.external_siem_immutable_audit",
    "control.retention_cleanup_plan",
}
SENSITIVE_FRAGMENTS = {
    "BEGIN RSA",
    "BEGIN OPENSSH",
    "DATABASE_URL=",
    "DB_DSN=",
    "api_key=",
    "authorization:",
    "password=",
    "private_key",
    "secret=",
    "token=",
}
RAW_URL_PATTERN = ("http://", "https://")


class GateFailure(RuntimeError):
    """安全外部化证据门禁失败。"""


def _load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def _load_production_security_gate() -> Any:
    gate_path = REPO_ROOT / "scripts" / "production-security-gate.py"
    spec = importlib.util.spec_from_file_location("fatecat_production_security_gate", gate_path)
    if spec is None or spec.loader is None:
        raise GateFailure("production_security_gate: cannot load")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _check(checks: list[dict[str, Any]], name: str, condition: bool, details: str) -> None:
    checks.append({"name": name, "ok": condition, "details": details})
    if not condition:
        raise GateFailure(f"{name}: {details}")


def _render(payload: Any) -> str:
    return json.dumps(payload, ensure_ascii=False, sort_keys=True)


def _assert_no_sensitive_fragments(
    checks: list[dict[str, Any]], name: str, payload: Any, *, forbid_raw_url: bool = False
) -> None:
    rendered = _render(payload).lower()
    bad = sorted(fragment for fragment in SENSITIVE_FRAGMENTS if fragment.lower() in rendered)
    if forbid_raw_url and any(fragment in rendered for fragment in RAW_URL_PATTERN):
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
        if not field.endswith(("ProofRef", "SummaryRef")):
            continue
        value = str(payload.get(field) or "")
        if not value.startswith(tuple(prefixes)):
            raise GateFailure(f"{area}: {field} must use redacted proof ref prefix")


def validate_external_evidence(evidence: dict[str, Any], contract: dict[str, Any]) -> None:
    status = evidence.get("status")
    if status == "external_connectivity_pending":
        return
    if status != "external_live_passed":
        raise GateFailure(f"evidence: unsupported status {status!r}")

    controls = contract["controls"]

    identity_schema = controls["identity"]["liveEvidenceSchema"]
    identity = evidence.get("identity")
    if not isinstance(identity, dict):
        raise GateFailure("identity: required for external_live_passed")
    _require_fields("identity", identity, identity_schema["requiredFields"])
    if identity["mode"] != identity_schema["requiredMode"]:
        raise GateFailure("identity: mode is not external_oidc_or_idp")
    if identity["verificationStatus"] != identity_schema["requiredVerificationStatus"]:
        raise GateFailure("identity: verificationStatus is not passed_external_oidc_check")
    if identity["provider"] in identity_schema["forbiddenProviderValues"]:
        raise GateFailure("identity: forbidden provider")
    _validate_proof_refs("identity", identity, identity_schema["requiredFields"], identity_schema["proofRefPrefixes"])
    if _contains_forbidden(identity, identity_schema["forbiddenProofFragments"]):
        raise GateFailure("identity: forbidden local token or placeholder proof")

    siem_schema = controls["siem"]["liveEvidenceSchema"]
    siem = evidence.get("siem")
    if not isinstance(siem, dict):
        raise GateFailure("siem: required for external_live_passed")
    _require_fields("siem", siem, siem_schema["requiredFields"])
    if siem["mode"] not in siem_schema["allowedModes"]:
        raise GateFailure("siem: unsupported immutability mode")
    if siem["verificationStatus"] != siem_schema["requiredVerificationStatus"]:
        raise GateFailure("siem: verificationStatus is not passed_external_siem_check")
    if siem["payloadBoundary"] != siem_schema["requiredPayloadBoundary"]:
        raise GateFailure("siem: payloadBoundary must be redacted_no_payload")
    _validate_proof_refs("siem", siem, siem_schema["requiredFields"], siem_schema["proofRefPrefixes"])
    if _contains_forbidden(siem, siem_schema["forbiddenProofFragments"]):
        raise GateFailure("siem: forbidden endpoint, payload, token or placeholder proof")

    retention_schema = controls["retentionCleaner"]["liveEvidenceSchema"]
    retention = evidence.get("retentionCleaner")
    if not isinstance(retention, dict):
        raise GateFailure("retention: required for external_live_passed")
    _require_fields("retention", retention, retention_schema["requiredFields"])
    if retention["mode"] != retention_schema["requiredMode"]:
        raise GateFailure("retention: mode is not time_based_cleanup_with_audit")
    if retention["verificationStatus"] != retention_schema["requiredVerificationStatus"]:
        raise GateFailure("retention: verificationStatus is not passed_retention_cleaner_smoke")
    if retention["deleteMode"] not in retention_schema["allowedDeleteModes"]:
        raise GateFailure("retention: unsupported deleteMode")
    if retention["auditAction"] not in retention_schema["requiredAuditActions"]:
        raise GateFailure("retention: auditAction missing")
    _validate_proof_refs(
        "retention", retention, retention_schema["requiredFields"], retention_schema["proofRefPrefixes"]
    )
    if _contains_forbidden(retention, retention_schema["forbiddenProofFragments"]):
        raise GateFailure("retention: forbidden production deletion or sensitive proof")


def _validate_negative_cases(checks: list[dict[str, Any]], contract: dict[str, Any]) -> list[str]:
    rejected: list[str] = []
    for case in contract["negativeEvidenceCases"]:
        case_id = case["id"]
        expected = case["expectedErrorContains"]
        try:
            validate_external_evidence(case["evidence"], contract)
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
        contract["contractId"] == "contract.security_externalization_evidence",
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
        {"identity", "siem", "retentionCleaner"} <= set(contract["controls"]),
        str(sorted({"identity", "siem", "retentionCleaner"} - set(contract["controls"]))),
    )
    for area, control in contract["controls"].items():
        _check(checks, f"{area}:control_id", control["controlId"] in REQUIRED_CONTROL_IDS, control["controlId"])
        _check(checks, f"{area}:dry_run_checks", bool(control.get("dryRunEvidenceChecks")), "present")
        live_schema = control.get("liveEvidenceSchema", {})
        _check(checks, f"{area}:live_schema", bool(live_schema.get("requiredFields")), "present")
        _check(
            checks,
            f"{area}:proof_ref_prefixes",
            {"evidence://", "artifact://", "ci-artifact://"} <= set(live_schema.get("proofRefPrefixes", [])),
            str(live_schema.get("proofRefPrefixes", [])),
        )
    _check(
        checks,
        "negative_cases_present",
        len(contract["negativeEvidenceCases"]) >= 3,
        str(len(contract["negativeEvidenceCases"])),
    )
    _assert_no_sensitive_fragments(checks, "contract_no_sensitive_fragments", contract)


def _validate_registry_and_policy(
    checks: list[dict[str, Any]], registry: dict[str, Any], policy: dict[str, Any]
) -> None:
    controls = {item["id"]: item for item in registry["controls"]}
    _check(checks, "required_controls_present", REQUIRED_CONTROL_IDS <= set(controls), "present")
    for control_id in sorted(REQUIRED_CONTROL_IDS):
        control = controls[control_id]
        _check(checks, f"{control_id}:manual", control["status"] == "manual", control["status"])
        _check(
            checks,
            f"{control_id}:external_pending",
            control["externalConnectivity"] == "external_connectivity_pending",
            control["externalConnectivity"],
        )
        _check(
            checks,
            f"{control_id}:gate_linked",
            "bash scripts/security-externalization-gate.sh" in control["localVerification"],
            str(control.get("localVerification", [])),
        )
    metadata = registry["metadata"]
    _check(
        checks,
        "registry_externalization_gate_command",
        metadata.get("securityExternalizationGateCommand") == "bash scripts/security-externalization-gate.sh",
        metadata.get("securityExternalizationGateCommand", ""),
    )
    _check(
        checks,
        "registry_externalization_contract",
        metadata.get("securityExternalizationEvidenceContract")
        == "contracts/fate/security/externalization-evidence-contract.json",
        metadata.get("securityExternalizationEvidenceContract", ""),
    )
    _check(
        checks,
        "policy_externalization_contract",
        policy["releaseGate"].get("externalizationEvidenceContract")
        == "contracts/fate/security/externalization-evidence-contract.json",
        policy["releaseGate"].get("externalizationEvidenceContract", ""),
    )
    _check(
        checks,
        "policy_externalization_gate",
        policy["releaseGate"].get("externalizationGateCommand") == "bash scripts/security-externalization-gate.sh",
        policy["releaseGate"].get("externalizationGateCommand", ""),
    )


def run_gate(evidence_json: Path | None = None) -> dict[str, Any]:
    production_security_gate = _load_production_security_gate()
    production_summary = production_security_gate.run_gate()
    contract = _load_json(CONTRACT_PATH)
    registry = _load_json(SECURITY_DIR / "registry.json")
    policy = _load_json(SECURITY_DIR / "production-security-policy.json")
    checks: list[dict[str, Any]] = []

    _check(checks, "production_security_gate", production_summary["status"] == "passed", production_summary["status"])
    _validate_contract(checks, contract)
    _validate_registry_and_policy(checks, registry, policy)
    rejected_negative_cases = _validate_negative_cases(checks, contract)

    live_evidence_status = "外部连通验证待执行"
    if evidence_json is not None:
        evidence = _load_json(evidence_json)
        _assert_no_sensitive_fragments(checks, "evidence_no_sensitive_fragments", evidence, forbid_raw_url=True)
        validate_external_evidence(evidence, contract)
        live_evidence_status = (
            "external_live_passed" if evidence.get("status") == "external_live_passed" else live_evidence_status
        )

    return {
        "schemaVersion": 1,
        "kind": "fatecat.security_externalization_gate_summary",
        "generatedAt": datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "status": "passed",
        "checks": checks,
        "contract": "contracts/fate/security/externalization-evidence-contract.json",
        "controls": sorted(REQUIRED_CONTROL_IDS),
        "negativeEvidenceRejected": rejected_negative_cases,
        "liveEvidenceStatus": live_evidence_status,
        "externalConnectivity": "外部连通验证待执行",
        "privacyBoundary": "summary 只保存检查名、状态和脱敏摘要；不得输出真实 token、secret、DSN、OIDC issuer、JWKS、SIEM endpoint、请求体、用户输入、审计 payload 或报告正文。",
    }


def write_summary(summary: dict[str, Any], output_json: Path) -> None:
    output_json.parent.mkdir(parents=True, exist_ok=True)
    with output_json.open("w", encoding="utf-8") as fh:
        json.dump(summary, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="验证 OIDC/SIEM/retention cleaner 外部化证据契约和反伪造边界。")
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON, help="gate summary JSON 输出路径。")
    parser.add_argument(
        "--evidence-json", type=Path, default=None, help="可选外部 live evidence JSON；默认只验证 pending contract。"
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        summary = run_gate(args.evidence_json)
        write_summary(summary, args.output_json)
        print(
            json.dumps(
                {
                    "status": summary["status"],
                    "controls": len(summary["controls"]),
                    "negativeEvidenceRejected": len(summary["negativeEvidenceRejected"]),
                    "liveEvidenceStatus": summary["liveEvidenceStatus"],
                    "checks": len(summary["checks"]),
                },
                ensure_ascii=False,
            )
        )
        return 0
    except GateFailure as exc:
        print(f"security externalization gate error: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
