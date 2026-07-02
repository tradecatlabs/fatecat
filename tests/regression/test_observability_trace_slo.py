from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[2]
SLO_GATE_PATH = ROOT / "scripts" / "observability-slo-gate.py"
TRACE_SLO_SMOKE_PATH = ROOT / "scripts" / "observability-trace-slo-smoke.py"
OTEL_COLLECTOR_SLO_GATE_PATH = ROOT / "scripts" / "otel-collector-slo-gate.py"
OTEL_COLLECTOR_CONFIG_PATH = ROOT / "contracts" / "fate" / "observability" / "otel-collector.dry-run.yaml"


def _load_module(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_observability_slo_gate_validates_policy_and_alert_rules(tmp_path):
    gate = _load_module("fatecat_observability_slo_gate_test", SLO_GATE_PATH)
    output_json = tmp_path / "slo-gate.json"

    summary = gate.run_gate()
    gate.write_summary(summary, output_json)
    stored = json.loads(output_json.read_text(encoding="utf-8"))

    assert stored["status"] == "passed"
    assert stored["objectives"] >= 4
    assert stored["alertRules"] >= 5
    checks = {item["name"]: item for item in stored["checks"]}
    assert checks["trace_signal_available"]["ok"] is True
    assert checks["slo_signal_available"]["ok"] is True
    assert checks["required_slo_ids"]["ok"] is True
    assert checks["required_alert_ids"]["ok"] is True
    assert stored["externalConnectivity"] == "外部连通验证待执行"


def test_observability_trace_slo_smoke_captures_local_spans(tmp_path):
    smoke = _load_module("fatecat_observability_trace_slo_smoke_test", TRACE_SLO_SMOKE_PATH)
    output_json = tmp_path / "trace-slo-smoke.json"

    summary = smoke.run_smoke()
    smoke.write_summary(summary, output_json)
    stored = json.loads(output_json.read_text(encoding="utf-8"))

    assert stored["status"] == "passed"
    assert stored["spanCount"] >= 6
    assert {
        "capability.execute",
        "http.request",
        "provider.calculate",
        "provider.validate",
        "report.calculate",
        "report.render_markdown",
    } <= set(stored["spanNames"])
    checks = {item["name"]: item for item in stored["checks"]}
    assert checks["trace_id_propagated"]["ok"] is True
    assert checks["no_birth_place_in_spans"]["ok"] is True
    assert checks["no_name_in_spans"]["ok"] is True
    assert checks["no_report_title_in_spans"]["ok"] is True
    assert checks["no_report_body_in_spans"]["ok"] is True
    assert "token" in stored["privacyBoundary"]


def test_observability_trace_slo_smoke_cli_writes_summary(tmp_path):
    smoke = _load_module("fatecat_observability_trace_slo_smoke_cli_test", TRACE_SLO_SMOKE_PATH)
    output_json = tmp_path / "trace-slo-smoke-cli.json"

    exit_code = smoke.main(["--output-json", str(output_json)])

    assert exit_code == 0
    stored = json.loads(output_json.read_text(encoding="utf-8"))
    assert stored["status"] == "passed"
    assert stored["alertRules"] >= 5


def test_otel_collector_slo_gate_validates_dry_run_contract(tmp_path):
    gate = _load_module("fatecat_otel_collector_slo_gate_test", OTEL_COLLECTOR_SLO_GATE_PATH)
    output_json = tmp_path / "otel-collector-slo-gate.json"

    summary = gate.run_gate()
    gate.write_summary(summary, output_json)
    stored = json.loads(output_json.read_text(encoding="utf-8"))

    assert stored["status"] == "passed"
    assert stored["collectorMode"] == "dry-run-contract"
    assert stored["pipelines"] >= 3
    assert stored["dryRunEvidenceChecks"] >= 3
    assert stored["liveEvidenceStatus"] == "external_connectivity_pending"
    checks = {item["name"]: item for item in stored["checks"]}
    assert checks["collector_required_receivers"]["ok"] is True
    assert checks["collector_required_pipelines"]["ok"] is True
    assert checks["slo_required_live_evidence"]["ok"] is True
    assert checks["registry_signal_signal.otel_collector_dry_run"]["ok"] is True
    assert checks["schema_otel_invariant"]["ok"] is True
    assert stored["externalConnectivity"] == "外部连通验证待执行"
    assert "token" in stored["privacyBoundary"]


def test_otel_collector_slo_gate_cli_writes_summary(tmp_path):
    gate = _load_module("fatecat_otel_collector_slo_gate_cli_test", OTEL_COLLECTOR_SLO_GATE_PATH)
    output_json = tmp_path / "otel-collector-slo-gate-cli.json"

    exit_code = gate.main(["--output-json", str(output_json)])

    assert exit_code == 0
    stored = json.loads(output_json.read_text(encoding="utf-8"))
    assert stored["status"] == "passed"
    assert stored["pipelines"] >= 3


def test_otel_collector_slo_gate_rejects_external_backend_endpoint(tmp_path):
    gate = _load_module("fatecat_otel_collector_slo_gate_negative_test", OTEL_COLLECTOR_SLO_GATE_PATH)
    config = yaml.safe_load(OTEL_COLLECTOR_CONFIG_PATH.read_text(encoding="utf-8"))
    config["exporters"]["otlp"] = {"endpoint": "https://tempo.example.invalid"}
    config["service"]["pipelines"]["traces"]["exporters"] = ["debug", "otlp"]
    config_path = tmp_path / "bad-collector.yaml"
    config_path.write_text(yaml.safe_dump(config, allow_unicode=True), encoding="utf-8")

    with pytest.raises(gate.OTelCollectorSloGateError):
        gate.run_gate(collector_config_path=config_path)
