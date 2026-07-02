from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SMOKE_PATH = ROOT / "scripts" / "security-smoke.py"


def _load_smoke_module():
    spec = importlib.util.spec_from_file_location("fatecat_security_smoke", SMOKE_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_security_smoke_checks_runtime_controls_without_file_gates(tmp_path):
    smoke = _load_smoke_module()
    output_json = tmp_path / "security-smoke.json"

    summary = smoke.run_smoke(run_file_gates=False)
    smoke.write_summary(summary, output_json)
    stored = json.loads(output_json.read_text(encoding="utf-8"))

    assert stored["schemaVersion"] == 1
    assert stored["status"] == "passed"
    assert stored["fileGates"] is False
    checks = {item["name"]: item for item in stored["checks"]}
    assert checks["header_nosniff"]["ok"] is True
    assert checks["header_csp"]["ok"] is True
    assert checks["request_body_limit"]["ok"] is True
    assert checks["rate_limit_rejects_second_request"]["ok"] is True
    assert checks["records_can_be_disabled"]["ok"] is True
    assert checks["user_token_owner_boundary"]["ok"] is True
    assert checks["security_registry_smoke_command"]["ok"] is True
    assert "token" in stored["privacyBoundary"]


def test_security_smoke_cli_writes_summary_without_file_gates(tmp_path):
    smoke = _load_smoke_module()
    output_json = tmp_path / "security-smoke-cli.json"

    exit_code = smoke.main(["--skip-file-gates", "--output-json", str(output_json)])

    assert exit_code == 0
    stored = json.loads(output_json.read_text(encoding="utf-8"))
    assert stored["status"] == "passed"
