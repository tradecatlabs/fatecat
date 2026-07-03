from __future__ import annotations

import importlib.util
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DELIVERY_DIR = ROOT / "contracts" / "fate" / "delivery"
GATE_PATH = ROOT / "scripts" / "runtime-proof-gate.py"


def _load_gate_module():
    spec = importlib.util.spec_from_file_location("fatecat_runtime_proof_gate", GATE_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_runtime_proof_contract_defines_required_components():
    contract = _load_json(DELIVERY_DIR / "runtime-proof-pack.json")
    schema = _load_json(DELIVERY_DIR / "schemas" / "runtime-proof.schema.json")
    components = {item["id"]: item for item in contract["requiredComponents"]}

    assert contract["contractId"] == "contract.runtime_proof_pack"
    assert contract["status"] == "dry_run_contract"
    assert contract["externalConnectivity"] == "external_connectivity_pending"
    assert set(schema["requiredComponentIds"]) == set(components)
    assert components["runtime_backend_contract"]["localGate"] == "bash scripts/runtime-backend-gate.sh"
    assert components["public_webhook_live"]["liveEvidenceKind"] == "fatecat.postgres_public_webhook_live_smoke"
    assert components["external_secret_provider"]["liveEvidenceKind"] == "fatecat.external_secret_provider_evidence"
    assert components["multi_replica_runtime"]["liveEvidenceKind"] == "fatecat.multi_replica_runtime_evidence"
    assert "does_not_claim_exactly_once" in contract["nonClaims"]


def test_runtime_proof_gate_defaults_to_external_pending(tmp_path):
    gate = _load_gate_module()
    output_json = tmp_path / "runtime-proof-gate.json"

    summary = gate.run_gate()
    gate.write_summary(summary, output_json)
    stored = _load_json(output_json)

    assert stored["schemaVersion"] == 1
    assert stored["kind"] == "fatecat.runtime_proof_gate_summary"
    assert stored["status"] == "passed"
    assert stored["runtimeProofStatus"] == "external_connectivity_pending"
    assert stored["shipGate"]["status"] == "blocked"
    assert set(stored["shipGate"]["blockingItems"]) == {
        "public_webhook_live",
        "external_secret_provider",
        "multi_replica_runtime",
    }
    assert stored["components"]["runtime_backend_contract"] == "contract_passed"
    assert stored["components"]["exactly_once_boundary"] == "non_claim_boundary_enforced"
    assert {
        "fake.public_webhook_blocked_as_live",
        "fake.local_secret_as_external",
        "fake.single_replica_as_runtime_proof",
        "fake.exactly_once_overclaim",
    } == set(stored["negativeEvidenceRejected"])


def test_runtime_proof_gate_accepts_redacted_live_evidence_pack(tmp_path):
    gate = _load_gate_module()
    public_webhook = tmp_path / "public-webhook.json"
    secret_evidence = tmp_path / "secret-provider.json"
    multi_evidence = tmp_path / "multi-replica.json"

    public_webhook.write_text(
        json.dumps(
            {
                "schemaVersion": 1,
                "kind": "fatecat.postgres_public_webhook_live_smoke",
                "status": "passed",
                "liveEvidence": {
                    "jobStatus": "succeeded",
                    "outboxStatus": "succeeded",
                    "publicWebhookLiveDelivery": True,
                },
                "privacyBoundary": "redacted summary only",
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    secret_evidence.write_text(
        json.dumps(
            {
                "schemaVersion": 1,
                "kind": "fatecat.external_secret_provider_evidence",
                "status": "external_live_passed",
                "secretProvider": {
                    "mode": "external_secret_provider",
                    "providerType": "hashicorp_vault",
                    "verificationStatus": "passed_external_secret_provider_check",
                    "keyReferenceProofRef": "evidence://secret-provider/key-reference",
                    "rotationProofRef": "evidence://secret-provider/rotation",
                    "accessAuditProofRef": "evidence://secret-provider/access-audit",
                    "applicationInjectionProofRef": "evidence://secret-provider/application-injection",
                    "redactionBoundary": "redacted_no_secret_values",
                },
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    multi_evidence.write_text(
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

    summary = gate.run_gate(
        webhook_evidence_path=public_webhook,
        provider_evidence_path=secret_evidence,
        replica_evidence_path=multi_evidence,
    )

    assert summary["runtimeProofStatus"] == "external_live_passed"
    assert summary["shipGate"]["status"] == "passed"
    assert summary["shipGate"]["blockingItems"] == []


def test_runtime_proof_gate_rejects_sensitive_or_raw_public_webhook_summary(tmp_path):
    gate = _load_gate_module()
    public_webhook = tmp_path / "public-webhook.json"
    public_webhook.write_text(
        json.dumps(
            {
                "schemaVersion": 1,
                "kind": "fatecat.postgres_public_webhook_live_smoke",
                "status": "passed",
                "webhook": {"raw": "https://example.invalid/callback"},
                "liveEvidence": {"publicWebhookLiveDelivery": True},
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    try:
        gate.run_gate(webhook_evidence_path=public_webhook)
    except gate.RuntimeProofGateError as exc:
        assert "sensitive" in str(exc)
    else:
        raise AssertionError("raw public webhook URL must be rejected")


def test_runtime_proof_gate_cli_writes_summary(tmp_path):
    gate = _load_gate_module()
    output_json = tmp_path / "runtime-proof-gate-cli.json"

    exit_code = gate.main(["--output-json", str(output_json)])

    assert exit_code == 0
    stored = _load_json(output_json)
    assert stored["status"] == "passed"
    assert stored["shipGate"]["status"] == "blocked"
    assert not re.search(r"https?://|postgres(?:ql)?://|token\\s*[:=]|secret\\s*[:=]", output_json.read_text())
