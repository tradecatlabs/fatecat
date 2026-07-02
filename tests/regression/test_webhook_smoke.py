from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SMOKE_PATH = ROOT / "scripts" / "webhook-smoke.py"


def _load_smoke_module():
    spec = importlib.util.spec_from_file_location("fatecat_webhook_smoke", SMOKE_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_webhook_smoke_checks_terminal_callback_contract(tmp_path):
    smoke = _load_smoke_module()
    output_json = tmp_path / "webhook-smoke.json"

    summary = smoke.run_smoke()
    smoke.write_summary(summary, output_json)
    stored = json.loads(output_json.read_text(encoding="utf-8"))

    assert stored["schemaVersion"] == 1
    assert stored["status"] == "passed"
    checks = {item["name"]: item for item in stored["checks"]}
    assert checks["job_succeeded"]["ok"] is True
    assert checks["event_type"]["ok"] is True
    assert checks["terminal_status"]["ok"] is True
    assert checks["no_markdown_body"]["ok"] is True
    assert checks["no_secret_echo"]["ok"] is True
    assert "不访问公网" in stored["privacyBoundary"]


def test_webhook_smoke_cli_writes_summary(tmp_path):
    smoke = _load_smoke_module()
    output_json = tmp_path / "webhook-smoke-cli.json"

    exit_code = smoke.main(["--output-json", str(output_json)])

    assert exit_code == 0
    stored = json.loads(output_json.read_text(encoding="utf-8"))
    assert stored["status"] == "passed"
