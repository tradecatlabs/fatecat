from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SMOKE_PATH = ROOT / "scripts" / "webhook-config-vault-smoke.py"


def _load_smoke_module():
    spec = importlib.util.spec_from_file_location("fatecat_webhook_config_vault_smoke", SMOKE_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_webhook_config_vault_smoke_checks_encrypted_redelivery_and_rotation(tmp_path):
    smoke = _load_smoke_module()
    output_json = tmp_path / "webhook-config-vault-smoke.json"

    summary = smoke.run_smoke()
    smoke.write_summary(summary, output_json)
    stored = json.loads(output_json.read_text(encoding="utf-8"))

    assert stored["schemaVersion"] == 1
    assert stored["kind"] == "fatecat.webhook_config_vault_smoke"
    assert stored["status"] == "passed"
    assert stored["redeliveryOutboxStatus"] == "succeeded"
    assert stored["encryptedConfigRemaining"] == 0
    assert stored["rotation"] == {"fromKey": "old", "toKey": "new", "rotated": 1}
    assert "webhook.redelivery_succeeded" in stored["redeliveryEventTypes"]
    checks = {item["name"]: item for item in stored["checks"]}
    assert checks["encrypted_config_record_exists"]["ok"] is True
    assert checks["encrypted_config_deleted_after_success"]["ok"] is True
    assert checks["rotation_count"]["ok"] is True
    assert "external backend" in stored["boundary"]
    serialized = json.dumps(stored, ensure_ascii=False)
    assert "callback.example" not in serialized
    assert "vault-smoke-secret" not in serialized
    assert "测试样本" not in serialized
    assert "北京" not in serialized
    assert "# 命理排盘报告" not in serialized


def test_webhook_config_vault_smoke_cli_writes_summary(tmp_path):
    smoke = _load_smoke_module()
    output_json = tmp_path / "webhook-config-vault-smoke-cli.json"

    exit_code = smoke.main(["--output-json", str(output_json)])

    assert exit_code == 0
    stored = json.loads(output_json.read_text(encoding="utf-8"))
    assert stored["status"] == "passed"
    assert "Fernet keys" in stored["privacyBoundary"]
