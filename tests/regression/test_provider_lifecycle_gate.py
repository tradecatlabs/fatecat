from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GATE_PATH = ROOT / "scripts" / "provider-lifecycle-gate.py"


def _load_gate_module():
    spec = importlib.util.spec_from_file_location("fatecat_provider_lifecycle_gate", GATE_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_provider_lifecycle_gate_checks_registered_providers(tmp_path):
    gate = _load_gate_module()
    output_json = tmp_path / "provider-lifecycle-gate.json"

    summary = gate.run_gate()
    gate.write_summary(summary, output_json)
    stored = json.loads(output_json.read_text(encoding="utf-8"))

    assert stored["schemaVersion"] == 1
    assert stored["status"] == "passed"
    assert stored["providerCount"] == 4
    checks = {item["name"]: item for item in stored["checks"]}
    assert checks["available_provider_coverage"]["ok"] is True
    assert checks["supply_chain_production_allowed:lunar-python"]["ok"] is True
    assert checks["supply_chain_production_allowed:iztro"]["ok"] is True
    assert "token" in stored["privacyBoundary"]


def test_provider_lifecycle_gate_cli_writes_summary(tmp_path):
    gate = _load_gate_module()
    output_json = tmp_path / "provider-lifecycle-gate-cli.json"

    exit_code = gate.main(["--output-json", str(output_json)])

    assert exit_code == 0
    stored = json.loads(output_json.read_text(encoding="utf-8"))
    assert stored["status"] == "passed"
