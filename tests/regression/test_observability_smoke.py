from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SMOKE_PATH = ROOT / "scripts" / "observability-smoke.py"


def _load_smoke_module():
    spec = importlib.util.spec_from_file_location("fatecat_observability_smoke", SMOKE_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_observability_smoke_checks_available_runtime_signals(tmp_path):
    smoke = _load_smoke_module()
    output_json = tmp_path / "observability-smoke.json"

    summary = smoke.run_smoke()
    smoke.write_summary(summary, output_json)
    stored = json.loads(output_json.read_text(encoding="utf-8"))

    assert stored["schemaVersion"] == 1
    assert stored["status"] == "passed"
    checks = {item["name"]: item for item in stored["checks"]}
    assert checks["health_status"]["ok"] is True
    assert checks["ready_body"]["ok"] is True
    assert checks["metric_fatecat_requests_total"]["ok"] is True
    assert checks["metric_fatecat_bot_queue_size"]["ok"] is True
    assert checks["structured_http_request_log"]["ok"] is True
    assert checks["structured_log_request_id"]["ok"] is True
    assert checks["structured_log_trace_id"]["ok"] is True
    assert "token" in stored["privacyBoundary"]


def test_observability_smoke_cli_writes_summary(tmp_path):
    smoke = _load_smoke_module()
    output_json = tmp_path / "observability-smoke-cli.json"

    exit_code = smoke.main(["--output-json", str(output_json)])

    assert exit_code == 0
    stored = json.loads(output_json.read_text(encoding="utf-8"))
    assert stored["status"] == "passed"
