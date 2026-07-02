from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SMOKE_PATH = ROOT / "scripts" / "webhook-outbox-smoke.py"


def _load_smoke_module():
    spec = importlib.util.spec_from_file_location("fatecat_webhook_outbox_smoke", SMOKE_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_webhook_outbox_smoke_checks_sqlite_persistent_outbox(tmp_path):
    smoke = _load_smoke_module()
    output_json = tmp_path / "webhook-outbox-smoke.json"

    summary = smoke.run_smoke()
    smoke.write_summary(summary, output_json)
    stored = json.loads(output_json.read_text(encoding="utf-8"))

    assert stored["schemaVersion"] == 1
    assert stored["kind"] == "fatecat.webhook_outbox_smoke"
    assert stored["status"] == "passed"
    assert stored["outboxStatuses"] == {"success": "succeeded", "failure": "failed"}
    checks = {item["name"]: item for item in stored["checks"]}
    assert checks["success_outbox_persisted_after_rebuild"]["ok"] is True
    assert checks["failure_outbox_persisted_after_rebuild"]["ok"] is True
    assert "跨进程自动重投" in stored["boundary"]
    serialized = json.dumps(stored, ensure_ascii=False)
    assert "callback.example" not in serialized
    assert "outbox-secret" not in serialized
    assert "测试样本" not in serialized
    assert "北京" not in serialized


def test_webhook_outbox_smoke_cli_writes_summary(tmp_path):
    smoke = _load_smoke_module()
    output_json = tmp_path / "webhook-outbox-smoke-cli.json"

    exit_code = smoke.main(["--output-json", str(output_json)])

    assert exit_code == 0
    stored = json.loads(output_json.read_text(encoding="utf-8"))
    assert stored["status"] == "passed"
    assert "webhook URL" in stored["privacyBoundary"]
