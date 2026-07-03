#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
SECURITY_DIR = REPO_ROOT / "contracts" / "fate" / "security"
CONTRACT_PATH = SECURITY_DIR / "retention-production-cleanup-staged.json"
RETENTION_CONTRACT_PATH = SECURITY_DIR / "retention-cleanup.json"
EXTERNALIZATION_CONTRACT_PATH = SECURITY_DIR / "externalization-evidence-contract.json"
POLICY_PATH = SECURITY_DIR / "production-security-policy.json"
DEFAULT_OUTPUT_JSON = (
    REPO_ROOT / "infra" / "runtime" / "local-state" / "exports" / "security" / "retention-production-cleanup-gate.json"
)


class GateFailure(RuntimeError):
    """Retention production cleanup staged gate failed."""


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _check(checks: list[dict[str, Any]], name: str, condition: bool, details: str) -> None:
    checks.append({"name": name, "ok": condition, "details": details})
    if not condition:
        raise GateFailure(f"{name}: {details}")


def _render(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True).lower()


def _assert_no_forbidden(area: str, payload: Any, contract: dict[str, Any]) -> None:
    text = _render(payload)
    for fragment in contract["forbiddenFragments"]:
        if fragment.lower() in text:
            raise GateFailure(f"{area}: forbidden proof fragment {fragment}")


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


def validate_external_evidence(evidence: dict[str, Any], contract: dict[str, Any]) -> str:
    status = evidence.get("status")
    if status in {None, "external_connectivity_pending"}:
        return "外部连通验证待执行"
    if status != "external_live_passed":
        raise GateFailure(f"evidence: unsupported status {status!r}")
    if evidence.get("kind") != "fatecat.retention_production_cleanup_evidence":
        raise GateFailure("evidence: invalid kind")
    _assert_no_forbidden("evidence", evidence, contract)

    areas = contract["requiredEvidenceAreas"]
    prefixes = contract["proofRefPrefixes"]

    scheduler = evidence.get("scheduler")
    if not isinstance(scheduler, dict):
        raise GateFailure("scheduler: required for external_live_passed")
    scheduler_schema = areas["scheduler"]
    _require_fields("scheduler", scheduler, scheduler_schema["requiredFields"])
    if scheduler["mode"] != scheduler_schema["requiredMode"]:
        raise GateFailure("scheduler: mode is not production_scheduler")
    if scheduler["verificationStatus"] != scheduler_schema["requiredVerificationStatus"]:
        raise GateFailure("scheduler: verificationStatus mismatch")
    if scheduler["auditAction"] not in scheduler_schema["requiredAuditActions"]:
        raise GateFailure("scheduler: auditAction missing")
    _validate_proof_refs("scheduler", scheduler, scheduler_schema["requiredFields"], prefixes)

    postgres = evidence.get("postgresCleanup")
    if not isinstance(postgres, dict):
        raise GateFailure("postgres: required for external_live_passed")
    postgres_schema = areas["postgresCleanup"]
    _require_fields("postgres", postgres, postgres_schema["requiredFields"])
    if postgres["mode"] != postgres_schema["requiredMode"]:
        raise GateFailure("postgres: mode mismatch")
    if postgres["verificationStatus"] != postgres_schema["requiredVerificationStatus"]:
        raise GateFailure("postgres: verificationStatus mismatch")
    if postgres["deleteMode"] not in postgres_schema["allowedDeleteModes"]:
        raise GateFailure("postgres: deleteMode unsupported")
    if postgres["auditAction"] not in postgres_schema["requiredAuditActions"]:
        raise GateFailure("postgres: auditAction missing")
    _validate_proof_refs("postgres", postgres, postgres_schema["requiredFields"], prefixes)

    siem = evidence.get("siemRetention")
    if not isinstance(siem, dict):
        raise GateFailure("siem: required for external_live_passed")
    siem_schema = areas["siemRetention"]
    _require_fields("siem", siem, siem_schema["requiredFields"])
    if siem["mode"] not in siem_schema["allowedModes"]:
        raise GateFailure("siem: mode unsupported")
    if siem["verificationStatus"] != siem_schema["requiredVerificationStatus"]:
        raise GateFailure("siem: verificationStatus mismatch")
    if siem["payloadBoundary"] != siem_schema["requiredPayloadBoundary"]:
        raise GateFailure("siem: payloadBoundary must be redacted_no_payload")
    _validate_proof_refs("siem", siem, siem_schema["requiredFields"], prefixes)
    return "external_live_passed"


def _validate_contract_wiring(checks: list[dict[str, Any]], contract: dict[str, Any]) -> None:
    retention_contract = _load_json(RETENTION_CONTRACT_PATH)
    externalization_contract = _load_json(EXTERNALIZATION_CONTRACT_PATH)
    policy = _load_json(POLICY_PATH)
    _check(checks, "contract:id", contract["id"] == "contract.retention_production_cleanup_staged", contract["id"])
    _check(checks, "contract:status", contract["status"] == "staged_contract", contract["status"])
    _check(
        checks,
        "depends_on:retention_cleanup",
        "contracts/fate/security/retention-cleanup.json" in contract["dependsOn"],
        str(contract["dependsOn"]),
    )
    _check(
        checks,
        "retention_contract:local_baseline",
        retention_contract["status"] == "local_sqlite_baseline",
        retention_contract["status"],
    )
    _check(
        checks,
        "externalization_contract:retention_cleaner",
        "retentionCleaner" in externalization_contract["controls"],
        str(externalization_contract["controls"].keys()),
    )
    _check(
        checks,
        "policy:retention_cleanup_contract",
        policy["releaseGate"].get("retentionCleanupContract") == "contracts/fate/security/retention-cleanup.json",
        str(policy["releaseGate"]),
    )
    _check(
        checks,
        "policy:retention_production_staged_gate",
        policy["releaseGate"].get("retentionProductionCleanupStagedGate")
        == "bash scripts/retention-production-cleanup-gate.sh",
        str(policy["releaseGate"]),
    )
    _check(
        checks,
        "negative_cases:min_count",
        len(contract["negativeEvidenceCases"]) >= 3,
        str(len(contract["negativeEvidenceCases"])),
    )


def _validate_negative_cases(checks: list[dict[str, Any]], contract: dict[str, Any]) -> list[str]:
    rejected: list[str] = []
    for case in contract["negativeEvidenceCases"]:
        try:
            validate_external_evidence(case["evidence"], contract)
        except GateFailure as exc:
            _check(checks, f"negative:{case['id']}", case["expectedErrorContains"] in str(exc), str(exc))
            rejected.append(case["id"])
        else:
            raise GateFailure(f"negative:{case['id']}: fake evidence was accepted")
    return rejected


def run_gate(evidence_json: Path | None = None) -> dict[str, Any]:
    contract = _load_json(CONTRACT_PATH)
    checks: list[dict[str, Any]] = []
    _validate_contract_wiring(checks, contract)
    rejected = _validate_negative_cases(checks, contract)

    live_status = "外部连通验证待执行"
    if evidence_json is not None:
        evidence = _load_json(evidence_json)
        live_status = validate_external_evidence(evidence, contract)
        _check(checks, "provided_evidence:validated", True, live_status)

    return {
        "schemaVersion": 1,
        "kind": "fatecat.retention_production_cleanup_gate_summary",
        "generatedAt": datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "status": "passed",
        "shipGate": "blocked",
        "liveEvidenceStatus": live_status,
        "contract": "contracts/fate/security/retention-production-cleanup-staged.json",
        "checks": checks,
        "negativeEvidenceRejected": rejected,
        "pendingExternalValidation": contract["pendingExternalValidation"],
        "privacyBoundary": "summary 只保存脱敏 proof refs、检查名和状态；不得输出真实 DSN、endpoint、token、secret、用户输入、报告正文、生产日志或生产删除结果。",
    }


def write_summary(summary: dict[str, Any], output_json: Path) -> None:
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="验证 retention production cleanup staged evidence gate。")
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON, help="gate summary JSON 输出路径。")
    parser.add_argument("--evidence-json", type=Path, default=None, help="可选脱敏 external evidence JSON。")
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
                    "shipGate": summary["shipGate"],
                    "liveEvidenceStatus": summary["liveEvidenceStatus"],
                    "negativeEvidenceRejected": len(summary["negativeEvidenceRejected"]),
                    "checks": len(summary["checks"]),
                },
                ensure_ascii=False,
                sort_keys=True,
            )
        )
        return 0
    except GateFailure as exc:
        print(f"retention production cleanup gate error: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
