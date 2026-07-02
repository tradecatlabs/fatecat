from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SMOKE_PATH = ROOT / "scripts" / "bazi-ziwei-l4-golden-smoke.py"


def _load_smoke_module():
    spec = importlib.util.spec_from_file_location("fatecat_bazi_ziwei_l4_golden_smoke", SMOKE_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_bazi_ziwei_l4_golden_smoke_summary(tmp_path):
    smoke = _load_smoke_module()
    output_json = tmp_path / "bazi-ziwei-l4.json"

    summary = smoke.run_smoke()
    smoke.write_summary(summary, output_json)
    stored = json.loads(output_json.read_text(encoding="utf-8"))

    assert stored["schemaVersion"] == 1
    assert stored["status"] == "passed"
    assert stored["profile"] == "quick"
    assert stored["smokeScope"] == "bazi_ziwei_l4_golden_evidence_baseline"
    assert stored["summary"]["baziMatrix"]["caseCount"] >= 300
    assert stored["summary"]["baziMatrix"]["executedCaseCount"] >= 3
    assert stored["summary"]["baziMatrix"]["requiredTagCount"] >= 15
    assert stored["summary"]["baziRuleDepth"]["caseCount"] >= 3
    assert stored["summary"]["baziRuleDepth"]["executedCaseCount"] == 2
    assert stored["summary"]["ziweiCases"]["caseCount"] >= 1
    assert stored["summary"]["ziweiCases"]["executedCaseCount"] == 1
    assert stored["summary"]["ziweiRuleDepth"]["caseCount"] >= 3
    assert stored["summary"]["ziweiRuleDepth"]["executedCaseCount"] == 2
    assert stored["summary"]["markdownProfiles"]["bazi"]["policyGate"] == "pass"
    assert stored["summary"]["markdownProfiles"]["ziwei"]["snapshotGate"] == "pass"
    assert "真实非北京地区" in stored["privacyBoundary"]
    assert any("不锁定完整断语正文" in item for item in stored["limits"])


def test_bazi_ziwei_l4_golden_smoke_cli_writes_summary(tmp_path):
    smoke = _load_smoke_module()
    output_json = tmp_path / "bazi-ziwei-l4-cli.json"

    exit_code = smoke.main(["--profile", "quick", "--output-json", str(output_json)])

    assert exit_code == 0
    stored = json.loads(output_json.read_text(encoding="utf-8"))
    assert stored["status"] == "passed"
    assert stored["profile"] == "quick"
