from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GATE_PATH = ROOT / "scripts" / "retention-production-cleanup-gate.py"
SECURITY_DIR = ROOT / "contracts" / "fate" / "security"


def _load_gate_module():
    spec = importlib.util.spec_from_file_location("fatecat_retention_production_cleanup_gate", GATE_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _redacted_live_evidence() -> dict:
    return {
        "schemaVersion": 1,
        "kind": "fatecat.retention_production_cleanup_evidence",
        "status": "external_live_passed",
        "scheduler": {
            "mode": "production_scheduler",
            "verificationStatus": "passed_scheduler_smoke",
            "scheduleProofRef": "evidence://retention/scheduler",
            "dryRunProofRef": "evidence://retention/scheduler-dry-run",
            "auditAction": "retention.cleanup.dry_run",
        },
        "postgresCleanup": {
            "mode": "postgres_retention_cleanup",
            "verificationStatus": "passed_postgres_cleanup_smoke",
            "smokeSummaryRef": "evidence://retention/postgres-cleanup-smoke",
            "databaseProofRef": "evidence://retention/postgres-database",
            "deleteMode": "tombstone_then_purge",
            "dryRun": True,
            "auditAction": "retention.cleanup.dry_run",
        },
        "siemRetention": {
            "mode": "worm",
            "verificationStatus": "passed_siem_retention_check",
            "retentionProofRef": "evidence://siem/retention",
            "immutabilityProofRef": "evidence://siem/immutability",
            "payloadBoundary": "redacted_no_payload",
        },
    }


def test_retention_production_cleanup_gate_defaults_to_blocked_pending(tmp_path):
    gate = _load_gate_module()
    output_json = tmp_path / "retention-production-cleanup-gate.json"

    summary = gate.run_gate()
    gate.write_summary(summary, output_json)
    stored = _load_json(output_json)

    assert stored["schemaVersion"] == 1
    assert stored["kind"] == "fatecat.retention_production_cleanup_gate_summary"
    assert stored["status"] == "passed"
    assert stored["shipGate"] == "blocked"
    assert stored["liveEvidenceStatus"] == "外部连通验证待执行"
    assert set(stored["negativeEvidenceRejected"]) == {
        "fake.retention_raw_url",
        "fake.retention_missing_postgres_smoke",
        "fake.retention_production_deleted_marker",
    }
    assert len(stored["pendingExternalValidation"]) == 3
    assert "DSN" in stored["privacyBoundary"]


def test_retention_production_cleanup_gate_cli_writes_summary(tmp_path):
    gate = _load_gate_module()
    output_json = tmp_path / "retention-production-cleanup-gate-cli.json"

    exit_code = gate.main(["--output-json", str(output_json)])

    assert exit_code == 0
    stored = _load_json(output_json)
    assert stored["status"] == "passed"
    assert stored["shipGate"] == "blocked"


def test_retention_production_cleanup_gate_accepts_redacted_staged_evidence(tmp_path):
    gate = _load_gate_module()
    evidence_json = tmp_path / "retention-live-evidence.json"
    evidence_json.write_text(json.dumps(_redacted_live_evidence(), ensure_ascii=False), encoding="utf-8")
    output_json = tmp_path / "retention-production-cleanup-live.json"

    exit_code = gate.main(["--evidence-json", str(evidence_json), "--output-json", str(output_json)])

    assert exit_code == 0
    stored = _load_json(output_json)
    assert stored["liveEvidenceStatus"] == "external_live_passed"
    assert stored["shipGate"] == "blocked"


def test_retention_production_cleanup_gate_rejects_negative_cases():
    gate = _load_gate_module()
    contract = _load_json(SECURITY_DIR / "retention-production-cleanup-staged.json")

    for case in contract["negativeEvidenceCases"]:
        try:
            gate.validate_external_evidence(case["evidence"], contract)
        except gate.GateFailure as exc:
            assert case["expectedErrorContains"] in str(exc)
        else:
            raise AssertionError(f"{case['id']} should be rejected")


def test_retention_production_cleanup_gate_is_wired_to_policy_local_ci_and_docs():
    contract = _load_json(SECURITY_DIR / "retention-production-cleanup-staged.json")
    registry = _load_json(SECURITY_DIR / "registry.json")
    policy = _load_json(SECURITY_DIR / "production-security-policy.json")
    local_ci = (ROOT / "scripts" / "local-ci.sh").read_text(encoding="utf-8")

    assert contract["resourceType"] == "RetentionProductionCleanupStagedGate"
    assert contract["status"] == "staged_contract"
    assert policy["releaseGate"]["retentionProductionCleanupStagedGate"] == (
        "bash scripts/retention-production-cleanup-gate.sh"
    )
    assert policy["releaseGate"]["retentionProductionCleanupStagedContract"] == (
        "contracts/fate/security/retention-production-cleanup-staged.json"
    )

    controls = {item["id"]: item for item in registry["controls"]}
    retention = controls["control.retention_cleanup_plan"]
    assert "contracts/fate/security/retention-production-cleanup-staged.json" in retention["implementationRefs"]
    assert "bash scripts/retention-production-cleanup-gate.sh" in retention["localVerification"]
    assert "retentionProductionCleanupStagedGateCommand" in registry["metadata"]
    assert "retention-production-cleanup-gate.sh" in local_ci
    assert "retention-production-cleanup-staged.json" in (SECURITY_DIR / "AGENTS.md").read_text(encoding="utf-8")
    assert "retention-production-cleanup-gate.py" in (ROOT / "scripts" / "AGENTS.md").read_text(encoding="utf-8")
    assert "test_retention_production_cleanup_gate.py" in (ROOT / "tests" / "AGENTS.md").read_text(encoding="utf-8")
