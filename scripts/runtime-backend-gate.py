#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
DELIVERY_DIR = REPO_ROOT / "contracts" / "fate" / "delivery"
REGISTRY_PATH = DELIVERY_DIR / "runtime-backends.json"
DELIVERY_REGISTRY_PATH = DELIVERY_DIR / "registry.json"
SCHEMA_PATH = DELIVERY_DIR / "schemas" / "runtime-backend.schema.json"
RESOURCE_SCHEMA_PATH = REPO_ROOT / "contracts" / "fate" / "capabilities" / "schemas" / "resource.schema.json"
DEFAULT_OUTPUT_JSON = REPO_ROOT / "infra" / "runtime" / "local-state" / "exports" / "runtime-backend-gate.json"

SENSITIVE_VALUE_PATTERN = re.compile(
    r"(postgres(?:ql)?://|redis://|amqp://|mysql://|mongodb://|BEGIN (?:RSA|OPENSSH|PRIVATE)|"
    r"secret\s*[:=]\s*[^,\s]+|password\s*[:=]\s*[^,\s]+|token\s*[:=]\s*[^,\s]+)",
    re.IGNORECASE,
)


class RuntimeBackendGateError(RuntimeError):
    """Runtime backend contract gate failed."""


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _append_check(checks: list[dict[str, Any]], name: str, ok: bool, details: str) -> None:
    checks.append({"name": name, "ok": ok, "details": details})


def _check(checks: list[dict[str, Any]], name: str, condition: bool, details: str) -> None:
    _append_check(checks, name, condition, details)
    if not condition:
        raise RuntimeBackendGateError(f"{name}: {details}")


def _allowed(schema: dict[str, Any], key: str) -> set[str]:
    return {str(item) for item in schema.get(key, [])}


def _contains_sensitive_value(payload: Any) -> bool:
    text = json.dumps(payload, ensure_ascii=False, sort_keys=True)
    return bool(SENSITIVE_VALUE_PATTERN.search(text))


def _validate_schema_links(
    *,
    registry: dict[str, Any],
    delivery_registry: dict[str, Any],
    resource_schema: dict[str, Any],
    checks: list[dict[str, Any]],
) -> None:
    _check(
        checks,
        "schema_links:runtime_backend_schema",
        registry.get("schemas", {}).get("runtimeBackend")
        == "contracts/fate/delivery/schemas/runtime-backend.schema.json",
        str(registry.get("schemas", {})),
    )
    _check(
        checks,
        "schema_links:resource_schema",
        registry.get("schemas", {}).get("resource") == "contracts/fate/capabilities/schemas/resource.schema.json",
        str(registry.get("schemas", {})),
    )
    _check(
        checks,
        "delivery_registry:runtime_backend_schema",
        delivery_registry.get("schemas", {}).get("runtimeBackend")
        == "contracts/fate/delivery/schemas/runtime-backend.schema.json",
        str(delivery_registry.get("schemas", {})),
    )
    _check(
        checks,
        "delivery_registry:runtime_backend_contract",
        delivery_registry.get("runtimeBackendRegistry", {}).get("contract")
        == "contracts/fate/delivery/runtime-backends.json",
        str(delivery_registry.get("runtimeBackendRegistry", {})),
    )
    _check(
        checks,
        "resource_schema:runtime_backend_resource_type",
        "RuntimeBackend" in resource_schema.get("resourceTypes", []),
        str(resource_schema.get("resourceTypes", [])),
    )
    _check(
        checks,
        "resource_schema:runtime_backend_fields",
        "runtimeBackendResourceFields" in resource_schema,
        str(resource_schema.keys()),
    )


def _validate_registry(
    *,
    registry: dict[str, Any],
    schema: dict[str, Any],
    checks: list[dict[str, Any]],
) -> dict[str, Any]:
    missing_registry = sorted(set(schema["requiredRegistryFields"]) - set(registry))
    _check(checks, "registry:required_fields", not missing_registry, str(missing_registry))
    _check(
        checks, "registry:resource_type", registry["resourceType"] == "RuntimeBackendRegistry", registry["resourceType"]
    )
    _check(checks, "registry:schema_version", registry["schemaVersion"] == 1, str(registry["schemaVersion"]))

    decision = registry["decision"]
    missing_decision = sorted(set(schema["requiredDecisionFields"]) - set(decision))
    _check(checks, "decision:required_fields", not missing_decision, str(missing_decision))
    _check(
        checks,
        "decision:selected_external_candidate",
        decision["selectedExternalCandidate"] == "backend.postgres",
        decision["selectedExternalCandidate"],
    )
    _check(
        checks,
        "decision:future_workflow_orchestrator",
        decision["futureWorkflowOrchestrator"] == "backend.temporal",
        decision["futureWorkflowOrchestrator"],
    )
    _check(
        checks,
        "decision:redis_not_source_of_truth",
        "backend.redis_queue" in decision["notSelectedAsSourceOfTruth"],
        str(decision["notSelectedAsSourceOfTruth"]),
    )

    backends = registry.get("backends", [])
    ids = [str(item.get("id")) for item in backends]
    _check(checks, "backends:unique_ids", len(ids) == len(set(ids)), str(ids))
    required_ids = {"backend.memory", "backend.sqlite", "backend.postgres", "backend.temporal", "backend.redis_queue"}
    _check(checks, "backends:required_ids", required_ids <= set(ids), str(sorted(set(ids))))

    allowed_backend_type = _allowed(schema, "allowedBackendType")
    allowed_status = _allowed(schema, "allowedStatus")
    allowed_maturity = _allowed(schema, "allowedMaturity")
    allowed_deployment = _allowed(schema, "allowedDeploymentScope")
    allowed_implementation = _allowed(schema, "allowedImplementationStatus")
    allowed_production = _allowed(schema, "allowedProductionEligibility")
    allowed_connectivity = _allowed(schema, "allowedExternalConnectivity")

    summary: dict[str, Any] = {
        "backendCount": len(backends),
        "availableCount": 0,
        "plannedCount": 0,
        "notSelectedCount": 0,
        "externalCandidate": decision["selectedExternalCandidate"],
        "futureWorkflowOrchestrator": decision["futureWorkflowOrchestrator"],
    }

    by_id = {item["id"]: item for item in backends}
    for backend in backends:
        backend_id = str(backend.get("id", "<missing>"))
        missing_backend = sorted(set(schema["requiredRuntimeBackendFields"]) - set(backend))
        _check(checks, f"{backend_id}:required_fields", not missing_backend, str(missing_backend))
        _check(
            checks, f"{backend_id}:resource_type", backend["resourceType"] == "RuntimeBackend", backend["resourceType"]
        )
        _check(
            checks, f"{backend_id}:backend_type", backend["backendType"] in allowed_backend_type, backend["backendType"]
        )
        _check(checks, f"{backend_id}:status", backend["status"] in allowed_status, backend["status"])
        _check(checks, f"{backend_id}:maturity", backend["maturity"] in allowed_maturity, backend["maturity"])
        _check(
            checks,
            f"{backend_id}:deployment_scope",
            backend["deploymentScope"] in allowed_deployment,
            backend["deploymentScope"],
        )
        _check(
            checks,
            f"{backend_id}:implementation_status",
            backend["implementationStatus"] in allowed_implementation,
            backend["implementationStatus"],
        )
        _check(
            checks,
            f"{backend_id}:production_eligibility",
            backend["productionEligibility"] in allowed_production,
            backend["productionEligibility"],
        )
        _check(
            checks,
            f"{backend_id}:external_connectivity",
            backend["externalConnectivity"] in allowed_connectivity,
            backend["externalConnectivity"],
        )
        missing_capability = sorted(set(schema["requiredCapabilityFields"]) - set(backend["capabilities"]))
        _check(checks, f"{backend_id}:capability_fields", not missing_capability, str(missing_capability))
        missing_metadata = sorted(set(schema["requiredMetadataFields"]) - set(backend["metadata"]))
        _check(checks, f"{backend_id}:metadata_fields", not missing_metadata, str(missing_metadata))
        _check(
            checks,
            f"{backend_id}:local_verification",
            bool(backend["localVerification"]),
            str(backend["localVerification"]),
        )
        privacy_boundary = backend["privacyBoundary"].lower()
        privacy_terms = ("secret", "token", "dsn", "password", "credential")
        _check(
            checks,
            f"{backend_id}:privacy_boundary",
            any(term in privacy_boundary for term in privacy_terms),
            backend["privacyBoundary"],
        )

        status = backend["status"]
        if status == "available":
            summary["availableCount"] += 1
        elif status == "planned":
            summary["plannedCount"] += 1
        elif status == "not_selected":
            summary["notSelectedCount"] += 1

    memory = by_id["backend.memory"]
    sqlite = by_id["backend.sqlite"]
    postgres = by_id["backend.postgres"]
    temporal = by_id["backend.temporal"]
    redis_queue = by_id["backend.redis_queue"]

    _check(
        checks,
        "memory:not_production",
        memory["productionEligibility"] == "not_allowed",
        memory["productionEligibility"],
    )
    _check(checks, "memory:no_durability", memory["capabilities"]["jobStatePersistence"] is False, "memory is volatile")
    _check(
        checks,
        "sqlite:single_replica_only",
        sqlite["productionEligibility"] == "single_replica_only"
        and sqlite["capabilities"]["multiReplicaReady"] is False,
        f"{sqlite['productionEligibility']} multiReplicaReady={sqlite['capabilities']['multiReplicaReady']}",
    )
    _check(
        checks,
        "sqlite:no_external_backend_claim",
        "external_backend" in sqlite["migration"]["blockedClaims"],
        str(sqlite["migration"]["blockedClaims"]),
    )
    _check(checks, "postgres:planned", postgres["status"] == "planned", postgres["status"])
    _check(
        checks,
        "postgres:contract_baseline",
        postgres["implementationStatus"] == "contract_baseline",
        postgres["implementationStatus"],
    )
    _check(
        checks,
        "postgres:requires_real_database",
        postgres["externalConnectivity"] == "requires_real_database",
        postgres["externalConnectivity"],
    )
    _check(
        checks,
        "postgres:blocks_production_claim",
        {"implemented", "production_ready", "external_live_verified"} <= set(postgres["migration"]["blockedClaims"]),
        str(postgres["migration"]["blockedClaims"]),
    )
    _check(
        checks,
        "temporal:future_orchestrator",
        temporal["productionEligibility"] == "future_orchestrator" and temporal["status"] == "planned",
        f"{temporal['productionEligibility']} {temporal['status']}",
    )
    _check(
        checks,
        "redis_queue:not_source_of_truth",
        redis_queue["status"] == "not_selected"
        and redis_queue["productionEligibility"] == "auxiliary_only"
        and "source_of_truth" in redis_queue["migration"]["blockedClaims"],
        f"{redis_queue['status']} {redis_queue['productionEligibility']} {redis_queue['migration']['blockedClaims']}",
    )
    _check(
        checks, "privacy:no_sensitive_inline_values", not _contains_sensitive_value(registry), "no DSN/secret values"
    )
    return summary


def run_gate() -> dict[str, Any]:
    registry = _load_json(REGISTRY_PATH)
    schema = _load_json(SCHEMA_PATH)
    delivery_registry = _load_json(DELIVERY_REGISTRY_PATH)
    resource_schema = _load_json(RESOURCE_SCHEMA_PATH)
    checks: list[dict[str, Any]] = []
    started = time.perf_counter()

    _validate_schema_links(
        registry=registry,
        delivery_registry=delivery_registry,
        resource_schema=resource_schema,
        checks=checks,
    )
    registry_summary = _validate_registry(registry=registry, schema=schema, checks=checks)

    return {
        "schemaVersion": 1,
        "kind": "fatecat.runtime_backend_gate",
        "generatedAt": datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "status": "passed",
        "gate": "runtime_backend",
        "elapsedMs": round((time.perf_counter() - started) * 1000, 3),
        "summary": registry_summary,
        "checks": checks,
        "privacyBoundary": "Runtime backend gate 只读取 tracked contract metadata，不读取真实用户、报告正文、webhook URL、webhook secret、token、DSN、数据库密码或生产日志。",
        "limits": [
            "不实现 Postgres、Temporal 或 Redis adapter。",
            "不连接真实外部数据库或服务。",
            "不证明生产级分布式 worker lease、exactly-once 或公网 webhook live delivery。",
            "不把 SQLite local lease 解释为 external backend。",
        ],
    }


def write_summary(summary: dict[str, Any], output_json: Path) -> None:
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="执行 FateCat runtime backend contract gate，并输出机器可读 JSON。")
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
                    "backends": summary["summary"]["backendCount"],
                    "externalCandidate": summary["summary"]["externalCandidate"],
                    "checks": len(summary["checks"]),
                    "elapsedMs": summary["elapsedMs"],
                },
                ensure_ascii=False,
                sort_keys=True,
            )
        )
        return 0
    except RuntimeBackendGateError as exc:
        print(f"runtime backend gate error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
