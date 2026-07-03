from __future__ import annotations

import importlib.util
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GATE_PATH = ROOT / "scripts" / "otel-backend-slo-gate.py"
OBSERVABILITY_DIR = ROOT / "contracts" / "fate" / "observability"


def _load_gate_module():
    spec = importlib.util.spec_from_file_location("fatecat_otel_backend_slo_gate", GATE_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _live_evidence() -> dict:
    return {
        "schemaVersion": 1,
        "kind": "fatecat.otel_backend_slo_evidence",
        "status": "external_live_passed",
        "observabilityBackend": {
            "mode": "external_otel_backend_slo",
            "backendType": "grafana_stack",
            "verificationStatus": "passed_external_otel_backend_slo_check",
            "releaseCommitProofRef": "evidence://observability/release-commit-0082",
            "collectorRuntimeProofRef": "evidence://observability/collector-runtime-0082",
            "traceBackendProofRef": "evidence://observability/trace-backend-0082",
            "metricsBackendProofRef": "evidence://observability/metrics-backend-0082",
            "sloDashboardProofRef": "evidence://observability/slo-dashboard-0082",
            "alertRouteProofRef": "evidence://observability/alert-route-0082",
            "productionTrafficWindowProofRef": "evidence://observability/traffic-window-0082",
            "errorBudgetProofRef": "evidence://observability/error-budget-0082",
            "incidentDrillProofRef": "evidence://observability/incident-drill-0082",
            "redactionBoundary": "redacted_no_secret_values",
        },
    }


def test_otel_backend_slo_gate_validates_contract_registry_and_negative_cases(tmp_path):
    gate = _load_gate_module()
    output_json = tmp_path / "otel-backend-slo-gate.json"

    summary = gate.run_gate()
    gate.write_summary(summary, output_json)
    stored = json.loads(output_json.read_text(encoding="utf-8"))

    assert stored["schemaVersion"] == 1
    assert stored["kind"] == "fatecat.otel_backend_slo_gate_summary"
    assert stored["status"] == "passed"
    assert stored["liveEvidenceStatus"] == "外部连通验证待执行"
    assert stored["externalConnectivity"] == "外部连通验证待执行"
    assert stored["controls"] == ["control.otel_backend_slo"]
    assert {
        "fake.local_collector_as_backend",
        "fake.placeholder_dashboard",
        "fake.missing_error_budget",
        "fake.incident_drill_overclaim_without_alert",
    } == set(stored["negativeEvidenceRejected"])
    checks = {item["name"]: item for item in stored["checks"]}
    assert checks["contract_external_pending"]["ok"] is True
    assert checks["registry_backend_gate_command"]["ok"] is True
    assert checks["schema_backend_slo_invariant"]["ok"] is True


def test_otel_backend_slo_gate_cli_writes_pending_summary(tmp_path):
    gate = _load_gate_module()
    output_json = tmp_path / "otel-backend-slo-gate-cli.json"

    exit_code = gate.main(["--output-json", str(output_json)])

    assert exit_code == 0
    stored = json.loads(output_json.read_text(encoding="utf-8"))
    assert stored["status"] == "passed"
    assert stored["liveEvidenceStatus"] == "外部连通验证待执行"
    assert len(stored["negativeEvidenceRejected"]) == 4


def test_otel_backend_slo_gate_accepts_redacted_live_evidence(tmp_path):
    gate = _load_gate_module()
    evidence_json = tmp_path / "otel-backend-slo-evidence.json"
    evidence_json.write_text(json.dumps(_live_evidence(), ensure_ascii=False), encoding="utf-8")
    output_json = tmp_path / "otel-backend-slo-live.json"

    exit_code = gate.main(["--evidence-json", str(evidence_json), "--output-json", str(output_json)])

    assert exit_code == 0
    stored = json.loads(output_json.read_text(encoding="utf-8"))
    assert stored["liveEvidenceStatus"] == "external_live_passed"


def test_otel_backend_slo_gate_rejects_placeholder_dashboard():
    gate = _load_gate_module()
    contract = json.loads((OBSERVABILITY_DIR / "otel-backend-slo-evidence-contract.json").read_text(encoding="utf-8"))
    fake_case = next(case for case in contract["negativeEvidenceCases"] if case["id"] == "fake.placeholder_dashboard")

    try:
        gate.validate_otel_backend_evidence(fake_case["evidence"], contract)
    except gate.GateFailure as exc:
        assert "forbidden" in str(exc)
    else:
        raise AssertionError("placeholder dashboard evidence must be rejected")


def test_otel_backend_slo_gate_rejects_raw_url(tmp_path):
    gate = _load_gate_module()
    evidence = _live_evidence()
    evidence["observabilityBackend"]["sloDashboardProofRef"] = "https://grafana.example.invalid/d/abc"
    evidence_json = tmp_path / "otel-backend-slo-url-evidence.json"
    evidence_json.write_text(json.dumps(evidence, ensure_ascii=False), encoding="utf-8")

    exit_code = gate.main(["--evidence-json", str(evidence_json), "--output-json", str(tmp_path / "out.json")])

    assert exit_code == 1


def test_otel_backend_slo_gate_summary_does_not_expose_sensitive_values(tmp_path):
    gate = _load_gate_module()
    output_json = tmp_path / "otel-backend-slo-gate.json"

    gate.write_summary(gate.run_gate(), output_json)
    serialized = output_json.read_text(encoding="utf-8")

    assert not re.search(
        r"postgres(?:ql)?://|https?://|password\s*[:=]|token\s*[:=]|secret\s*[:=]|BEGIN (?:RSA|OPENSSH)",
        serialized,
        re.I,
    )
