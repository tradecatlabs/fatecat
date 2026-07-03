#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
DELIVERY_DIR = REPO_ROOT / "contracts" / "fate" / "delivery"
CONTRACT_PATH = DELIVERY_DIR / "multi-replica-runtime-contract.json"
RUNTIME_BACKENDS_PATH = DELIVERY_DIR / "runtime-backends.json"
DELIVERY_REGISTRY_PATH = DELIVERY_DIR / "registry.json"
DEFAULT_OUTPUT_JSON = (
    REPO_ROOT / "infra" / "runtime" / "local-state" / "exports" / "delivery" / "multi-replica-runtime-gate.json"
)

SENSITIVE_FRAGMENTS = {
    "BEGIN OPENSSH",
    "BEGIN RSA",
    "DATABASE_URL=",
    "DB_DSN=",
    "api_key=",
    "authorization:",
    "password=",
    "private_key",
    "secret=",
    "token=",
    "webhook_url=",
}


class GateFailure(RuntimeError):
    """长期多副本 runtime evidence gate 失败。"""


def _load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def _check(checks: list[dict[str, Any]], name: str, condition: bool, details: str) -> None:
    checks.append({"name": name, "ok": condition, "details": details})
    if not condition:
        raise GateFailure(f"{name}: {details}")


def _render(payload: Any) -> str:
    return json.dumps(payload, ensure_ascii=False, sort_keys=True)


def _assert_no_sensitive_fragments(checks: list[dict[str, Any]], name: str, payload: Any) -> None:
    rendered = _render(payload).lower()
    bad = sorted(fragment for fragment in SENSITIVE_FRAGMENTS if fragment.lower() in rendered)
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


def _require_int_at_least(area: str, payload: dict[str, Any], field: str, minimum: int) -> None:
    value = payload.get(field)
    if isinstance(value, bool) or not isinstance(value, int):
        raise GateFailure(f"{area}: {field} must be integer")
    if value < minimum:
        raise GateFailure(f"{area}: {field} {value} is lower than {minimum}")


def validate_multi_replica_evidence(evidence: dict[str, Any], contract: dict[str, Any]) -> None:
    status = evidence.get("status")
    if status == "external_connectivity_pending":
        return
    if status != "external_live_passed":
        raise GateFailure(f"evidence: unsupported status {status!r}")

    runtime = evidence.get("runtime")
    if not isinstance(runtime, dict):
        raise GateFailure("runtime: required for external_live_passed")

    control = contract["controls"]["longRunningMultiReplica"]
    schema = control["liveEvidenceSchema"]
    _require_fields("runtime", runtime, schema["requiredFields"])
    if runtime["mode"] != control["requiredMode"]:
        raise GateFailure("runtime: mode is not external_postgres_multi_replica")
    if runtime["backend"] != control["backend"]:
        raise GateFailure("runtime: backend is not backend.postgres")
    if runtime["backend"] in schema["forbiddenBackendValues"]:
        raise GateFailure("runtime: backend is forbidden")
    if runtime["verificationStatus"] != control["requiredVerificationStatus"]:
        raise GateFailure("runtime: verificationStatus is not passed_multi_replica_soak")
    if runtime["redactionBoundary"] != control["requiredRedactionBoundary"]:
        raise GateFailure("runtime: redactionBoundary must be redacted_no_secret_values")
    if runtime.get("exactlyOnceClaim") is True:
        raise GateFailure("runtime: exactlyOnceClaim is forbidden")
    _require_int_at_least("runtime", runtime, "replicaCount", int(control["minimumReplicaCount"]))
    _require_int_at_least("runtime", runtime, "durationSeconds", int(control["minimumDurationSeconds"]))
    _require_int_at_least("runtime", runtime, "completedJobCount", int(control["minimumCompletedJobCount"]))
    if _contains_forbidden(runtime, schema["forbiddenProofFragments"]):
        raise GateFailure("runtime: forbidden local, fake, placeholder or short-run proof")


def _validate_negative_cases(checks: list[dict[str, Any]], contract: dict[str, Any]) -> list[str]:
    rejected: list[str] = []
    for case in contract["negativeEvidenceCases"]:
        case_id = case["id"]
        expected = case["expectedErrorContains"]
        try:
            validate_multi_replica_evidence(case["evidence"], contract)
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
        contract["contractId"] == "contract.multi_replica_runtime_evidence",
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
        "contract_runtime_backend",
        contract["runtimeBackend"] == "backend.postgres",
        contract["runtimeBackend"],
    )
    _check(
        checks,
        "contract_controls",
        {"localPostgresWorkerBaseline", "longRunningMultiReplica"} <= set(contract["controls"]),
        str(sorted({"localPostgresWorkerBaseline", "longRunningMultiReplica"} - set(contract["controls"]))),
    )
    local_control = contract["controls"]["localPostgresWorkerBaseline"]
    _check(
        checks,
        "local_baseline_not_multi_replica",
        "does_not_prove_long_running_multi_replica" in local_control["nonClaims"],
        str(local_control["nonClaims"]),
    )
    live_control = contract["controls"]["longRunningMultiReplica"]
    _check(
        checks,
        "live_schema_required_fields",
        len(live_control["liveEvidenceSchema"]["requiredFields"]) >= 12,
        str(live_control["liveEvidenceSchema"]["requiredFields"]),
    )
    _check(
        checks,
        "minimum_replica_count",
        int(live_control["minimumReplicaCount"]) >= 2,
        str(live_control["minimumReplicaCount"]),
    )
    _check(
        checks,
        "minimum_duration_seconds",
        int(live_control["minimumDurationSeconds"]) >= 86400,
        str(live_control["minimumDurationSeconds"]),
    )
    _check(
        checks,
        "minimum_completed_jobs",
        int(live_control["minimumCompletedJobCount"]) >= 100,
        str(live_control["minimumCompletedJobCount"]),
    )
    _check(
        checks,
        "exactly_once_not_claimed",
        live_control["exactlyOncePolicy"]["claimAllowed"] is False,
        str(live_control["exactlyOncePolicy"]),
    )
    _check(
        checks,
        "negative_cases_present",
        len(contract["negativeEvidenceCases"]) >= 4,
        str(len(contract["negativeEvidenceCases"])),
    )
    _assert_no_sensitive_fragments(checks, "contract_no_sensitive_fragments", contract)


def _validate_runtime_registry(
    checks: list[dict[str, Any]], runtime_backends: dict[str, Any], delivery_registry: dict[str, Any]
) -> None:
    postgres = {item["id"]: item for item in runtime_backends["backends"]}["backend.postgres"]
    _check(
        checks,
        "runtime_backend_postgres_still_planned",
        postgres["status"] == "planned",
        postgres["status"],
    )
    _check(
        checks,
        "runtime_backend_multi_replica_pending",
        postgres["capabilities"].get("multiReplicaReady") == "evidence_contract_gate_ready_evidence_pending",
        str(postgres["capabilities"].get("multiReplicaReady")),
    )
    _check(
        checks,
        "runtime_backend_exactly_once_false",
        postgres["capabilities"].get("exactlyOnceClaim") is False,
        str(postgres["capabilities"].get("exactlyOnceClaim")),
    )
    _check(
        checks,
        "runtime_backend_blocks_claims",
        {"multi_replica_ready", "exactly_once", "public_webhook_live", "external_vault_kms"}
        <= set(postgres["migration"]["blockedClaims"]),
        str(postgres["migration"]["blockedClaims"]),
    )
    _check(
        checks,
        "runtime_backend_required_evidence_linked",
        "multi-replica runtime evidence gate: bash scripts/multi-replica-runtime-gate.sh"
        in postgres["requiredEvidence"],
        str(postgres["requiredEvidence"]),
    )
    _check(
        checks,
        "runtime_backend_local_gate_linked",
        "bash scripts/multi-replica-runtime-gate.sh" in postgres["localVerification"],
        str(postgres["localVerification"]),
    )
    _check(
        checks,
        "runtime_backend_external_evidence_linked",
        any("multi-replica runtime live evidence" in item for item in postgres["externalVerification"]),
        str(postgres["externalVerification"]),
    )

    runtime_registry = delivery_registry["runtimeBackendRegistry"]
    _check(
        checks,
        "delivery_registry_contract_linked",
        runtime_registry.get("multiReplicaRuntimeEvidenceContract")
        == "contracts/fate/delivery/multi-replica-runtime-contract.json",
        str(runtime_registry),
    )
    _check(
        checks,
        "delivery_registry_gate_linked",
        runtime_registry.get("multiReplicaRuntimeGateCommand") == "bash scripts/multi-replica-runtime-gate.sh",
        str(runtime_registry),
    )
    _check(
        checks,
        "delivery_registry_local_verification",
        "bash scripts/multi-replica-runtime-gate.sh" in runtime_registry["localVerification"],
        str(runtime_registry["localVerification"]),
    )


def run_gate(evidence_json: Path | None = None) -> dict[str, Any]:
    contract = _load_json(CONTRACT_PATH)
    runtime_backends = _load_json(RUNTIME_BACKENDS_PATH)
    delivery_registry = _load_json(DELIVERY_REGISTRY_PATH)
    checks: list[dict[str, Any]] = []

    _validate_contract(checks, contract)
    _validate_runtime_registry(checks, runtime_backends, delivery_registry)
    rejected_negative_cases = _validate_negative_cases(checks, contract)

    live_evidence_status = "外部连通验证待执行"
    if evidence_json is not None:
        evidence = _load_json(evidence_json)
        _assert_no_sensitive_fragments(checks, "evidence_no_sensitive_fragments", evidence)
        validate_multi_replica_evidence(evidence, contract)
        live_evidence_status = (
            "external_live_passed" if evidence.get("status") == "external_live_passed" else live_evidence_status
        )

    return {
        "schemaVersion": 1,
        "kind": "fatecat.multi_replica_runtime_gate_summary",
        "generatedAt": datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "status": "passed",
        "checks": checks,
        "contract": "contracts/fate/delivery/multi-replica-runtime-contract.json",
        "runtimeBackend": "backend.postgres",
        "negativeEvidenceRejected": rejected_negative_cases,
        "liveEvidenceStatus": live_evidence_status,
        "externalConnectivity": "外部连通验证待执行",
        "privacyBoundary": (
            "multi-replica runtime gate 只读取 tracked contract metadata 和可选脱敏 evidence JSON；"
            "不读取或输出真实 DSN、webhook URL、secret、token、报告正文、用户输入或生产日志。"
        ),
        "nonClaims": [
            "does_not_connect_real_database",
            "does_not_prove_public_webhook_live_passed",
            "does_not_prove_external_secret_provider_live",
            "does_not_claim_exactly_once",
        ],
    }


def write_summary(summary: dict[str, Any], output_json: Path) -> None:
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="执行 FateCat long-running multi-replica runtime evidence gate。")
    parser.add_argument("--evidence-json", type=Path, help="可选：真实外部多副本运行脱敏 evidence JSON。")
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON, help="gate summary JSON 输出路径。")
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
                    "runtimeBackend": summary["runtimeBackend"],
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
        print(f"multi-replica runtime gate error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
