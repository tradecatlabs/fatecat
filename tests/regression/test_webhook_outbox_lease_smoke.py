from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SMOKE_PATH = ROOT / "scripts" / "webhook-outbox-lease-smoke.py"


def _load_smoke_module():
    spec = importlib.util.spec_from_file_location("fatecat_webhook_outbox_lease_smoke", SMOKE_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_webhook_outbox_lease_smoke_checks_claim_release_and_redelivery(tmp_path):
    smoke = _load_smoke_module()
    output_json = tmp_path / "webhook-outbox-lease-smoke.json"

    summary = smoke.run_smoke()
    smoke.write_summary(summary, output_json)
    stored = json.loads(output_json.read_text(encoding="utf-8"))

    assert stored["schemaVersion"] == 1
    assert stored["kind"] == "fatecat.webhook_outbox_lease_smoke"
    assert stored["status"] == "passed"
    assert stored["redeliveryOutboxStatus"] == "succeeded"
    assert stored["encryptedConfigRemaining"] == 0
    assert "webhook.redelivery_succeeded" in stored["redeliveryEventTypes"]
    checks = {item["name"]: item for item in stored["checks"]}
    assert checks["worker_a_claims"]["ok"] is True
    assert checks["worker_b_cannot_double_claim"]["ok"] is True
    assert checks["wrong_owner_release_noop"]["ok"] is True
    assert checks["manager_redelivery_attempt_once"]["ok"] is True
    assert "external backend" in stored["boundary"]
    assert "生产级分布式 worker lease" in stored["boundary"]
    serialized = json.dumps(stored, ensure_ascii=False)
    assert "callback.example" not in serialized
    assert "lease-smoke-secret" not in serialized
    assert "worker-a" not in serialized
    assert "worker-b" not in serialized
    assert "测试样本" not in serialized
    assert "北京" not in serialized


def test_webhook_outbox_lease_smoke_cli_writes_summary(tmp_path):
    smoke = _load_smoke_module()
    output_json = tmp_path / "webhook-outbox-lease-smoke-cli.json"

    exit_code = smoke.main(["--output-json", str(output_json)])

    assert exit_code == 0
    stored = json.loads(output_json.read_text(encoding="utf-8"))
    assert stored["status"] == "passed"
    assert "webhook URL" in stored["privacyBoundary"]
    assert "exactly-once" in stored["boundary"]
