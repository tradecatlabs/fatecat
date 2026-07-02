from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SLO_GATE_PATH = ROOT / "scripts" / "observability-slo-gate.py"
TRACE_SLO_SMOKE_PATH = ROOT / "scripts" / "observability-trace-slo-smoke.py"


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
