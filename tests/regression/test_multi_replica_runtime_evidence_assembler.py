from __future__ import annotations

import importlib.util
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ASSEMBLER_PATH = ROOT / "scripts" / "multi-replica-runtime-evidence-assembler.py"
GATE_PATH = ROOT / "scripts" / "multi-replica-runtime-gate.py"


def _load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _load_assembler():
    return _load_module(ASSEMBLER_PATH, "fatecat_multi_replica_runtime_evidence_assembler")


def _load_gate():
    return _load_module(GATE_PATH, "fatecat_multi_replica_runtime_gate_for_assembler")


def _live_args(output_json: Path) -> list[str]:
    return [
        "--external-live",
        "--ack-external-live",
        "--run-id",
        "evidence://runtime/soak-run-0081",
        "--started-at",
        "2026-07-01T00:00:00Z",
        "--finished-at",
        "2026-07-02T00:00:00Z",
        "--replica-count",
        "2",
        "--completed-job-count",
        "100",
        "--operator-attestation-ref",
        "evidence://runtime/operator-attestation-0081",
        "--concurrent-worker-proof-ref",
        "evidence://runtime/concurrent-worker-0081",
        "--lease-contention-proof-ref",
        "evidence://runtime/lease-contention-0081",
        "--restart-recovery-proof-ref",
        "evidence://runtime/restart-recovery-0081",
        "--heartbeat-continuity-proof-ref",
        "evidence://runtime/heartbeat-continuity-0081",
        "--no-duplicate-terminal-job-proof-ref",
        "evidence://runtime/no-duplicate-terminal-job-0081",
        "--public-webhook-proof-ref",
        "evidence://runtime/public-webhook-0081",
        "--external-secret-provider-proof-ref",
        "evidence://runtime/external-secret-provider-0081",
        "--metrics-proof-ref",
        "evidence://runtime/metrics-0081",
        "--output-json",
        str(output_json),
    ]


def test_multi_replica_runtime_evidence_assembler_writes_pending(tmp_path):
    assembler = _load_assembler()
    output_json = tmp_path / "multi-replica-runtime-evidence-pending.json"

    exit_code = assembler.main(["--pending", "--output-json", str(output_json)])

    assert exit_code == 0
    stored = json.loads(output_json.read_text(encoding="utf-8"))
    assert stored["schemaVersion"] == 1
    assert stored["kind"] == "fatecat.multi_replica_runtime_evidence"
    assert stored["status"] == "external_connectivity_pending"
    assert stored["externalConnectivity"] == "外部连通验证待执行"
    assert "does_not_claim_exactly_once" in stored["nonClaims"]


def test_multi_replica_runtime_evidence_assembler_live_fixture_passes_gate(tmp_path):
    assembler = _load_assembler()
    gate = _load_gate()
    evidence_json = tmp_path / "multi-replica-runtime-evidence-live.json"

    exit_code = assembler.main(_live_args(evidence_json))

    assert exit_code == 0
    stored = json.loads(evidence_json.read_text(encoding="utf-8"))
    assert stored["status"] == "external_live_passed"
    assert stored["runtime"]["durationSeconds"] == 86400
    assert stored["runtime"]["redactionBoundary"] == "redacted_no_secret_values"

    summary = gate.run_gate(evidence_json=evidence_json)
    assert summary["status"] == "passed"
    assert summary["liveEvidenceStatus"] == "external_live_passed"


def test_multi_replica_runtime_evidence_assembler_rejects_missing_ack(tmp_path):
    assembler = _load_assembler()
    args = [item for item in _live_args(tmp_path / "evidence.json") if item != "--ack-external-live"]

    exit_code = assembler.main(args)

    assert exit_code == 1


def test_multi_replica_runtime_evidence_assembler_rejects_sensitive_ref(tmp_path):
    assembler = _load_assembler()
    args = _live_args(tmp_path / "evidence.json")
    index = args.index("evidence://runtime/public-webhook-0081")
    args[index] = "evidence://runtime/token=leaked"

    exit_code = assembler.main(args)

    assert exit_code == 1


def test_multi_replica_runtime_evidence_assembler_rejects_raw_url(tmp_path):
    assembler = _load_assembler()
    args = _live_args(tmp_path / "evidence.json")
    index = args.index("evidence://runtime/metrics-0081")
    args[index] = "https://metrics.example.invalid/run"

    exit_code = assembler.main(args)

    assert exit_code == 1


def test_multi_replica_runtime_evidence_assembler_rejects_exactly_once_claim(tmp_path):
    assembler = _load_assembler()
    args = _live_args(tmp_path / "evidence.json") + ["--exactly-once-claim"]

    exit_code = assembler.main(args)

    assert exit_code == 1


def test_multi_replica_runtime_evidence_assembler_output_has_no_sensitive_values(tmp_path):
    assembler = _load_assembler()
    output_json = tmp_path / "multi-replica-runtime-evidence-live.json"

    assert assembler.main(_live_args(output_json)) == 0
    serialized = output_json.read_text(encoding="utf-8")

    assert not re.search(
        r"postgres(?:ql)?://|https?://|password\s*[:=]|token\s*[:=]|secret\s*[:=]|BEGIN (?:RSA|OPENSSH)",
        serialized,
        re.I,
    )
