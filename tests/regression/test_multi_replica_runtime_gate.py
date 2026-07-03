from __future__ import annotations

import importlib.util
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GATE_PATH = ROOT / "scripts" / "multi-replica-runtime-gate.py"
DELIVERY_DIR = ROOT / "contracts" / "fate" / "delivery"


def _load_gate_module():
    spec = importlib.util.spec_from_file_location("fatecat_multi_replica_runtime_gate", GATE_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_multi_replica_runtime_gate_validates_contract_and_negative_cases(tmp_path):
    gate = _load_gate_module()
    output_json = tmp_path / "multi-replica-runtime-gate.json"

    summary = gate.run_gate()
    gate.write_summary(summary, output_json)
    stored = _load_json(output_json)

    assert stored["schemaVersion"] == 1
    assert stored["kind"] == "fatecat.multi_replica_runtime_gate_summary"
    assert stored["status"] == "passed"
    assert stored["runtimeBackend"] == "backend.postgres"
    assert stored["liveEvidenceStatus"] == "外部连通验证待执行"
    assert stored["externalConnectivity"] == "外部连通验证待执行"
    assert {
        "fake.single_replica_as_multi",
        "fake.short_run_as_soak",
        "fake.sqlite_as_external_backend",
        "fake.exactly_once_overclaim",
    } == set(stored["negativeEvidenceRejected"])
    checks = {item["name"]: item for item in stored["checks"]}
    assert checks["contract_external_pending"]["ok"] is True
    assert checks["runtime_backend_multi_replica_pending"]["ok"] is True
    assert checks["delivery_registry_gate_linked"]["ok"] is True


def test_multi_replica_runtime_gate_cli_writes_summary(tmp_path):
    gate = _load_gate_module()
    output_json = tmp_path / "multi-replica-runtime-gate-cli.json"

    exit_code = gate.main(["--output-json", str(output_json)])

    assert exit_code == 0
    stored = _load_json(output_json)
    assert stored["status"] == "passed"
    assert len(stored["negativeEvidenceRejected"]) == 4


def test_multi_replica_runtime_gate_rejects_short_or_fake_evidence():
    gate = _load_gate_module()
    contract = _load_json(DELIVERY_DIR / "multi-replica-runtime-contract.json")

    for case in contract["negativeEvidenceCases"]:
        try:
            gate.validate_multi_replica_evidence(case["evidence"], contract)
        except gate.GateFailure as exc:
            assert case["expectedErrorContains"] in str(exc)
        else:
            raise AssertionError(f"{case['id']} must be rejected")


def test_multi_replica_runtime_gate_accepts_redacted_live_evidence(tmp_path):
    gate = _load_gate_module()
    evidence_json = tmp_path / "multi-replica-runtime-evidence.json"
    evidence_json.write_text(
        json.dumps(
            {
                "schemaVersion": 1,
                "kind": "fatecat.multi_replica_runtime_evidence",
                "status": "external_live_passed",
                "runtime": {
                    "mode": "external_postgres_multi_replica",
                    "backend": "backend.postgres",
                    "verificationStatus": "passed_multi_replica_soak",
                    "replicaCount": 2,
                    "durationSeconds": 86400,
                    "completedJobCount": 100,
                    "concurrentWorkerProofRef": "evidence://runtime/concurrent-worker",
                    "leaseContentionProofRef": "evidence://runtime/lease-contention",
                    "restartRecoveryProofRef": "evidence://runtime/restart-recovery",
                    "heartbeatContinuityProofRef": "evidence://runtime/heartbeat",
                    "noDuplicateTerminalJobProofRef": "evidence://runtime/no-duplicate-terminal",
                    "publicWebhookProofRef": "evidence://runtime/public-webhook",
                    "externalSecretProviderProofRef": "evidence://runtime/external-secret-provider",
                    "metricsProofRef": "evidence://runtime/metrics",
                    "redactionBoundary": "redacted_no_secret_values",
                },
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    output_json = tmp_path / "multi-replica-runtime-live.json"

    exit_code = gate.main(["--evidence-json", str(evidence_json), "--output-json", str(output_json)])

    assert exit_code == 0
    stored = _load_json(output_json)
    assert stored["liveEvidenceStatus"] == "external_live_passed"


def test_multi_replica_runtime_gate_summary_does_not_expose_sensitive_values(tmp_path):
    gate = _load_gate_module()
    output_json = tmp_path / "multi-replica-runtime-gate.json"

    gate.write_summary(gate.run_gate(), output_json)
    serialized = output_json.read_text(encoding="utf-8")

    assert not re.search(
        r"postgres(?:ql)?://|https?://|password\s*[:=]|token\s*[:=]|secret\s*[:=]|BEGIN (?:RSA|OPENSSH)",
        serialized,
        re.I,
    )
