from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GATE_PATH = ROOT / "scripts" / "data-supply-chain-gate.py"


def _load_gate_module():
    spec = importlib.util.spec_from_file_location("fatecat_data_supply_chain_gate", GATE_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_data_supply_chain_gate_summary(tmp_path):
    gate = _load_gate_module()
    output_json = tmp_path / "data-supply-chain-gate.json"

    summary = gate.run_gate()
    gate.write_summary(summary, output_json)
    stored = json.loads(output_json.read_text(encoding="utf-8"))

    assert stored["schemaVersion"] == 1
    assert stored["status"] == "passed"
    assert stored["gate"] == "data_supply_chain"
    assert stored["summary"]["registry"]["assetCount"] >= 8
    assert stored["summary"]["registry"]["productionInputAssetCount"] == 1
    assert stored["summary"]["classics"]["canonicalTxtCount"] == 14
    assert stored["summary"]["classics"]["hashChecked"] == 14
    assert "lunar-python" in stored["summary"]["vendor"]["productionDependencyIds"]
    assert "iztro" in stored["summary"]["vendor"]["productionDependencyIds"]
    assert "token" in stored["privacyBoundary"]
    assert any("不提供法律意见" in item for item in stored["limits"])


def test_data_supply_chain_gate_cli_writes_summary(tmp_path):
    gate = _load_gate_module()
    output_json = tmp_path / "data-supply-chain-gate-cli.json"

    exit_code = gate.main(["--output-json", str(output_json)])

    assert exit_code == 0
    stored = json.loads(output_json.read_text(encoding="utf-8"))
    assert stored["status"] == "passed"
