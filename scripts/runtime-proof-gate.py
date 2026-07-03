#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
DELIVERY_DIR = REPO_ROOT / "contracts" / "fate" / "delivery"
CONTRACT_PATH = DELIVERY_DIR / "runtime-proof-pack.json"
SCHEMA_PATH = DELIVERY_DIR / "schemas" / "runtime-proof.schema.json"
DELIVERY_REGISTRY_PATH = DELIVERY_DIR / "registry.json"
RUNTIME_BACKENDS_PATH = DELIVERY_DIR / "runtime-backends.json"
RUNTIME_BACKEND_GATE_PATH = REPO_ROOT / "scripts" / "runtime-backend-gate.py"
EXTERNAL_SECRET_GATE_PATH = REPO_ROOT / "scripts" / "external-secret-provider-gate.py"
MULTI_REPLICA_GATE_PATH = REPO_ROOT / "scripts" / "multi-replica-runtime-gate.py"
DEFAULT_OUTPUT_JSON = (
    REPO_ROOT / "infra" / "runtime" / "local-state" / "exports" / "delivery" / "runtime-proof-gate.json"
)

PENDING = "外部连通验证待执行"
SENSITIVE_PATTERN = re.compile(
    r"(postgres(?:ql)?://|https?://|password\s*[:=]|passwd\s*[:=]|token\s*[:=]|secret\s*[:=]|"
    r"authorization:|private[_-]?key\s*[:=]|BEGIN (?:RSA|OPENSSH|PRIVATE)|DATABASE_URL=|DB_DSN=)",
    re.I,
)


class RuntimeProofGateError(RuntimeError):
    """Runtime proof pack gate failed."""


def _load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as fh:
        payload = json.load(fh)
    if not isinstance(payload, dict):
        raise RuntimeProofGateError(f"JSON root must be object: {path}")
    return payload


def _load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeProofGateError(f"cannot load module: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _utc_now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def _render(payload: Any) -> str:
    return json.dumps(payload, ensure_ascii=False, sort_keys=True)


def _assert_no_sensitive(name: str, payload: Any) -> None:
    rendered = _render(payload)
    if SENSITIVE_PATTERN.search(rendered):
        raise RuntimeProofGateError(f"{name}: sensitive value or raw URL detected")


def _check(checks: list[dict[str, Any]], name: str, condition: bool, details: str) -> None:
    checks.append({"name": name, "ok": condition, "details": details})
    if not condition:
        raise RuntimeProofGateError(f"{name}: {details}")


def _validate_contract_shape(checks: list[dict[str, Any]], contract: dict[str, Any], schema: dict[str, Any]) -> None:
    for field_name in schema["requiredTopLevelFields"]:
        _check(checks, f"contract.required.{field_name}", field_name in contract, "present")
    _check(checks, "contract_id", contract["contractId"] == "contract.runtime_proof_pack", contract["contractId"])
    _check(checks, "contract_kind", contract["kind"] == "RuntimeProofPackContract", contract["kind"])
    _check(checks, "contract_status", contract["status"] in schema["allowedContractStatus"], contract["status"])
    _check(
        checks,
        "contract_external_pending",
        contract["externalConnectivity"] == "external_connectivity_pending",
        contract["externalConnectivity"],
    )

    components = {item["id"]: item for item in contract["requiredComponents"]}
    _check(
        checks,
        "contract.required_components",
        set(schema["requiredComponentIds"]) == set(components),
        ",".join(sorted(components)),
    )
    for component_id, component in components.items():
        for field_name in schema["requiredComponentFields"]:
            _check(checks, f"{component_id}.required.{field_name}", field_name in component, "present")
        _check(
            checks,
            f"{component_id}.required_for_production",
            component["requiredForProduction"] is True,
            str(component["requiredForProduction"]),
        )

    negative_ids = {item["id"] for item in contract["negativeEvidenceCases"]}
    _check(
        checks,
        "contract.negative_cases",
        set(schema["requiredNegativeCaseIds"]) <= negative_ids,
        ",".join(sorted(negative_ids)),
    )
    _check(
        checks,
        "contract.no_exactly_once_claim",
        "does_not_claim_exactly_once" in contract["nonClaims"],
        str(contract["nonClaims"]),
    )
    _assert_no_sensitive("contract", contract)


def _validate_registry_links(
    checks: list[dict[str, Any]],
    contract: dict[str, Any],
    delivery_registry: dict[str, Any],
    runtime_backends: dict[str, Any],
) -> None:
    runtime_registry = delivery_registry["runtimeBackendRegistry"]
    _check(
        checks,
        "delivery.runtime_proof_contract_link",
        runtime_registry.get("runtimeProofPackContract") == "contracts/fate/delivery/runtime-proof-pack.json",
        str(runtime_registry.get("runtimeProofPackContract")),
    )
    _check(
        checks,
        "delivery.runtime_proof_gate_link",
        runtime_registry.get("runtimeProofGateCommand") == "bash scripts/runtime-proof-gate.sh",
        str(runtime_registry.get("runtimeProofGateCommand")),
    )
    _check(
        checks,
        "delivery.runtime_proof_local_verification",
        "bash scripts/runtime-proof-gate.sh" in runtime_registry["localVerification"],
        str(runtime_registry["localVerification"]),
    )

    postgres = {item["id"]: item for item in runtime_backends["backends"]}["backend.postgres"]
    _check(checks, "postgres.status.planned", postgres["status"] == "planned", postgres["status"])
    _check(
        checks,
        "postgres.no_exactly_once",
        postgres["capabilities"].get("exactlyOnceClaim") is False,
        str(postgres["capabilities"].get("exactlyOnceClaim")),
    )
    _check(
        checks,
        "postgres.blocks_live_claims",
        {"multi_replica_ready", "exactly_once", "public_webhook_live", "external_vault_kms"}
        <= set(postgres["migration"]["blockedClaims"]),
        str(postgres["migration"]["blockedClaims"]),
    )
    _check(
        checks,
        "contract.source.runtime_backends",
        contract["sourceOfTruth"]["runtimeBackends"] == "contracts/fate/delivery/runtime-backends.json",
        contract["sourceOfTruth"]["runtimeBackends"],
    )


def _runtime_backend_status(checks: list[dict[str, Any]]) -> str:
    module = _load_module(RUNTIME_BACKEND_GATE_PATH, "fatecat_runtime_backend_gate")
    summary = module.run_gate()
    _assert_no_sensitive("runtime_backend_gate_summary", summary)
    _check(checks, "runtime_backend_gate.status", summary["status"] == "passed", summary["status"])
    return "contract_passed"


def _public_webhook_status(checks: list[dict[str, Any]], summary_path: Path | None) -> str:
    if summary_path is None:
        _check(checks, "public_webhook.summary", True, "not supplied")
        return "external_connectivity_pending"
    summary = _load_json(summary_path)
    _assert_no_sensitive("public_webhook_summary", summary)
    _check(
        checks,
        "public_webhook.kind",
        summary.get("kind") == "fatecat.postgres_public_webhook_live_smoke",
        str(summary.get("kind")),
    )
    status = summary.get("status")
    if status == "passed":
        live = summary.get("liveEvidence", {})
        _check(
            checks,
            "public_webhook.live_delivery",
            isinstance(live, dict) and live.get("publicWebhookLiveDelivery") is True,
            str(live),
        )
        return "external_live_passed"
    if status == "blocked":
        _check(checks, "public_webhook.blocked_pending", True, "blocked allow-missing summary")
        return "external_connectivity_pending"
    raise RuntimeProofGateError(f"public webhook summary status is not acceptable: {status}")


def _external_secret_status(checks: list[dict[str, Any]], evidence_path: Path | None) -> str:
    module = _load_module(EXTERNAL_SECRET_GATE_PATH, "fatecat_external_secret_provider_gate")
    summary = module.run_gate(evidence_path)
    _assert_no_sensitive("external_secret_provider_gate_summary", summary)
    _check(checks, "external_secret_provider_gate.status", summary["status"] == "passed", summary["status"])
    return (
        "external_live_passed"
        if summary.get("liveEvidenceStatus") == "external_live_passed"
        else "external_connectivity_pending"
    )


def _multi_replica_status(checks: list[dict[str, Any]], evidence_path: Path | None) -> str:
    module = _load_module(MULTI_REPLICA_GATE_PATH, "fatecat_multi_replica_runtime_gate")
    summary = module.run_gate(evidence_path)
    _assert_no_sensitive("multi_replica_runtime_gate_summary", summary)
    _check(checks, "multi_replica_runtime_gate.status", summary["status"] == "passed", summary["status"])
    _check(
        checks,
        "multi_replica.no_exactly_once_nonclaim",
        "does_not_claim_exactly_once" in summary.get("nonClaims", []),
        str(summary.get("nonClaims")),
    )
    return (
        "external_live_passed"
        if summary.get("liveEvidenceStatus") == "external_live_passed"
        else "external_connectivity_pending"
    )


def _validate_negative_cases(checks: list[dict[str, Any]], contract: dict[str, Any]) -> list[str]:
    rejected: list[str] = []
    external_secret_gate = _load_module(EXTERNAL_SECRET_GATE_PATH, "fatecat_external_secret_provider_gate_negative")
    multi_replica_gate = _load_module(MULTI_REPLICA_GATE_PATH, "fatecat_multi_replica_runtime_gate_negative")
    secret_contract = external_secret_gate._load_json(external_secret_gate.CONTRACT_PATH)
    multi_contract = multi_replica_gate._load_json(multi_replica_gate.CONTRACT_PATH)

    for case in contract["negativeEvidenceCases"]:
        case_id = case["id"]
        expected = case["expectedErrorContains"]
        evidence = case["evidence"]
        try:
            if case_id == "fake.public_webhook_blocked_as_live":
                if evidence.get("status") != "passed":
                    raise RuntimeProofGateError("public webhook summary is blocked")
            elif case_id == "fake.local_secret_as_external":
                external_secret_gate.validate_external_secret_evidence(evidence, secret_contract)
            elif case_id == "fake.single_replica_as_runtime_proof":
                multi_replica_gate.validate_multi_replica_evidence(evidence, multi_contract)
            elif case_id == "fake.exactly_once_overclaim":
                if evidence.get("exactlyOnceClaim") is True:
                    raise RuntimeProofGateError("exactly-once claim is forbidden")
            else:
                raise RuntimeProofGateError(f"unknown negative case {case_id}")
        except Exception as exc:  # noqa: BLE001 - negative case must be rejected by any relevant gate.
            message = str(exc)
            _check(checks, f"negative:{case_id}", expected in message, message)
            rejected.append(case_id)
        else:
            raise RuntimeProofGateError(f"negative:{case_id}: fake evidence was accepted")
    return rejected


def run_gate(
    webhook_evidence_path: Path | None = None,
    provider_evidence_path: Path | None = None,
    replica_evidence_path: Path | None = None,
) -> dict[str, Any]:
    contract = _load_json(CONTRACT_PATH)
    schema = _load_json(SCHEMA_PATH)
    delivery_registry = _load_json(DELIVERY_REGISTRY_PATH)
    runtime_backends = _load_json(RUNTIME_BACKENDS_PATH)
    checks: list[dict[str, Any]] = []

    _validate_contract_shape(checks, contract, schema)
    _validate_registry_links(checks, contract, delivery_registry, runtime_backends)
    negative_rejected = _validate_negative_cases(checks, contract)

    components = {
        "runtime_backend_contract": _runtime_backend_status(checks),
        "public_webhook_live": _public_webhook_status(checks, webhook_evidence_path),
        "external_secret_provider": _external_secret_status(checks, provider_evidence_path),
        "multi_replica_runtime": _multi_replica_status(checks, replica_evidence_path),
        "exactly_once_boundary": "non_claim_boundary_enforced",
    }
    live_required = [
        "public_webhook_live",
        "external_secret_provider",
        "multi_replica_runtime",
    ]
    pending_items = [
        component_id for component_id in live_required if components[component_id] != "external_live_passed"
    ]
    ship_gate_status = "passed" if not pending_items else "blocked"

    return {
        "schemaVersion": 1,
        "kind": "fatecat.runtime_proof_gate_summary",
        "generatedAt": _utc_now(),
        "status": "passed",
        "contract": "contracts/fate/delivery/runtime-proof-pack.json",
        "components": components,
        "negativeEvidenceRejected": negative_rejected,
        "runtimeProofStatus": "external_live_passed"
        if ship_gate_status == "passed"
        else "external_connectivity_pending",
        "externalConnectivity": "external_live_passed" if ship_gate_status == "passed" else PENDING,
        "shipGate": {
            "status": ship_gate_status,
            "blockingItems": pending_items,
            "policy": contract["shipGate"]["policy"],
        },
        "checks": checks,
        "privacyBoundary": contract["privacyBoundary"],
        "nonClaims": contract["nonClaims"],
    }


def write_summary(summary: dict[str, Any], output_json: Path) -> None:
    _assert_no_sensitive("runtime_proof_summary", summary)
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="聚合 FateCat W2 runtime proof pack。")
    parser.add_argument(
        "--public-webhook-summary", type=Path, help="可选：postgres public webhook live smoke summary。"
    )
    parser.add_argument("--external-secret-evidence-json", type=Path, help="可选：外部 secret provider live evidence。")
    parser.add_argument("--multi-replica-evidence-json", type=Path, help="可选：长期多副本 runtime live evidence。")
    parser.add_argument(
        "--output-json", type=Path, default=DEFAULT_OUTPUT_JSON, help="runtime proof summary 输出路径。"
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        summary = run_gate(
            args.public_webhook_summary,
            args.external_secret_evidence_json,
            args.multi_replica_evidence_json,
        )
        write_summary(summary, args.output_json)
        print(
            json.dumps(
                {
                    "status": summary["status"],
                    "runtimeProofStatus": summary["runtimeProofStatus"],
                    "shipGate": summary["shipGate"]["status"],
                    "pending": len(summary["shipGate"]["blockingItems"]),
                    "checks": len(summary["checks"]),
                    "outputJson": str(args.output_json),
                },
                ensure_ascii=False,
                sort_keys=True,
            )
        )
        return 0
    except RuntimeProofGateError as exc:
        print(f"runtime proof gate error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
