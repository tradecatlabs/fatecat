from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GATE_PATH = ROOT / "scripts" / "runtime-backend-gate.py"
DELIVERY_DIR = ROOT / "contracts" / "fate" / "delivery"
RESOURCE_SCHEMA = ROOT / "contracts" / "fate" / "capabilities" / "schemas" / "resource.schema.json"


def _load_gate_module():
    spec = importlib.util.spec_from_file_location("fatecat_runtime_backend_gate", GATE_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_runtime_backend_gate_summary(tmp_path):
    gate = _load_gate_module()
    output_json = tmp_path / "runtime-backend-gate.json"

    summary = gate.run_gate()
    gate.write_summary(summary, output_json)
    stored = _load_json(output_json)

    assert stored["schemaVersion"] == 1
    assert stored["kind"] == "fatecat.runtime_backend_gate"
    assert stored["status"] == "passed"
    assert stored["gate"] == "runtime_backend"
    assert stored["summary"]["backendCount"] == 5
    assert stored["summary"]["availableCount"] == 2
    assert stored["summary"]["plannedCount"] == 2
    assert stored["summary"]["notSelectedCount"] == 1
    assert stored["summary"]["externalCandidate"] == "backend.postgres"
    assert stored["summary"]["futureWorkflowOrchestrator"] == "backend.temporal"
    assert "DSN" in stored["privacyBoundary"]
    assert any("worker lease negative smoke baseline" in item for item in stored["limits"])
    assert any("不在 gate 内连接真实外部数据库" in item for item in stored["limits"])


def test_runtime_backend_gate_cli_writes_summary(tmp_path):
    gate = _load_gate_module()
    output_json = tmp_path / "runtime-backend-gate-cli.json"

    exit_code = gate.main(["--output-json", str(output_json)])

    assert exit_code == 0
    stored = _load_json(output_json)
    assert stored["status"] == "passed"
    assert stored["summary"]["externalCandidate"] == "backend.postgres"


def test_runtime_backend_contract_keeps_external_backends_planned():
    registry = _load_json(DELIVERY_DIR / "runtime-backends.json")
    backends = {item["id"]: item for item in registry["backends"]}

    assert registry["decision"]["selectedExternalCandidate"] == "backend.postgres"
    assert backends["backend.postgres"]["status"] == "planned"
    assert backends["backend.postgres"]["implementationStatus"] == "worker_lease_smoke_baseline"
    assert backends["backend.postgres"]["externalConnectivity"] == "requires_real_database"
    assert "production_ready" in backends["backend.postgres"]["migration"]["blockedClaims"]
    assert "exactly_once" in backends["backend.postgres"]["migration"]["blockedClaims"]
    assert "public_webhook_live" in backends["backend.postgres"]["migration"]["blockedClaims"]
    assert "external_vault_kms" in backends["backend.postgres"]["migration"]["blockedClaims"]
    assert "bash scripts/postgres-job-store-dry-run.sh" in backends["backend.postgres"]["localVerification"]
    assert (
        "bash scripts/postgres-worker-lease-smoke.sh --allow-missing"
        in backends["backend.postgres"]["localVerification"]
    )
    assert "bash scripts/postgres-job-store-live-smoke.sh" in backends["backend.postgres"]["externalVerification"]
    assert "bash scripts/postgres-worker-lease-smoke.sh" in backends["backend.postgres"]["externalVerification"]
    assert backends["backend.sqlite"]["productionEligibility"] == "single_replica_only"
    assert backends["backend.sqlite"]["capabilities"]["multiReplicaReady"] is False
    assert backends["backend.redis_queue"]["status"] == "not_selected"
    assert "source_of_truth" in backends["backend.redis_queue"]["migration"]["blockedClaims"]


def test_runtime_backend_schema_and_resource_model_are_linked():
    delivery_registry = _load_json(DELIVERY_DIR / "registry.json")
    runtime_schema = _load_json(DELIVERY_DIR / "schemas" / "runtime-backend.schema.json")
    resource_schema = _load_json(RESOURCE_SCHEMA)

    assert delivery_registry["schemas"]["runtimeBackend"] == (
        "contracts/fate/delivery/schemas/runtime-backend.schema.json"
    )
    assert delivery_registry["runtimeBackendRegistry"]["contract"] == "contracts/fate/delivery/runtime-backends.json"
    assert "RuntimeBackend" in resource_schema["resourceTypes"]
    assert "runtimeBackendResourceFields" in resource_schema
    assert "backendType" in runtime_schema["requiredRuntimeBackendFields"]
    assert runtime_schema["allowedBackendType"] == ["memory", "sqlite", "postgres", "temporal", "redis_queue"]
    assert "adapter_baseline" in runtime_schema["allowedImplementationStatus"]
    assert "live_smoke_baseline" in runtime_schema["allowedImplementationStatus"]
    assert "worker_lease_smoke_baseline" in runtime_schema["allowedImplementationStatus"]
    assert "external_connectivity_pending" in runtime_schema["allowedExternalConnectivity"]
