from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT_PATH = ROOT / "scripts" / "evidence-coverage-trend-gate.py"
BASELINE_PATH = ROOT / "contracts" / "fate" / "evidence-coverage-baseline.json"
CONTRACT_PATH = ROOT / "contracts" / "fate" / "evidence-coverage-trend-contract.json"


def _load_module():
    spec = importlib.util.spec_from_file_location("fatecat_evidence_coverage_trend_gate", SCRIPT_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_evidence_coverage_contract_and_baseline_are_traceable():
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    baseline = json.loads(BASELINE_PATH.read_text(encoding="utf-8"))

    assert contract["kind"] == "fatecat.evidence_coverage_trend_contract"
    assert "bash scripts/evidence-coverage-trend-gate.sh" in contract["generator"]["command"]
    assert "命理排盘报告：" in contract["forbiddenReportFragments"]
    assert baseline["kind"] == "fatecat.evidence_coverage_baseline"
    assert baseline["registryMinimums"]["rulesBySystem"] == {"bazi": 22, "ziwei": 22}
    assert baseline["capabilityMinimums"]["bazi"]["minAppliedRules"] >= 22
    assert baseline["capabilityMinimums"]["bazi"]["minReportEvidenceRefCompletenessRatio"] == 1.0
    assert baseline["capabilityMinimums"]["ziwei"]["minReportEvidenceRefs"] >= 6


def test_evidence_coverage_trend_gate_passes_current_baseline(tmp_path):
    module = _load_module()
    summary = module.run_gate()

    assert summary["status"] == "passed"
    assert summary["summary"]["totalEvidenceItems"] >= 18
    assert summary["summary"]["totalReportEvidenceRefs"] >= 18
    assert summary["summary"]["totalBrokenRuleRefs"] == 0
    assert summary["trendFindings"] == []
    assert summary["capabilities"]["bazi"]["reportEvidenceRefs"]["completeRatio"] == 1.0
    assert summary["capabilities"]["bazi"]["ruleDepth"]["conflictCounterEvidenceRatio"] == 1.0
    assert summary["capabilities"]["ziwei"]["evidenceItems"]["completeRatio"] == 1.0
    assert "baziRuleDepth" in summary["capabilities"]["bazi"]["evidenceItems"]["evidenceItemIds"]

    output_json = tmp_path / "evidence-coverage-trend.json"
    module.write_summary(summary, output_json)
    stored = json.loads(output_json.read_text(encoding="utf-8"))
    assert stored["status"] == "passed"


def test_evidence_coverage_trend_gate_fails_on_regression_baseline(tmp_path):
    module = _load_module()
    baseline = json.loads(BASELINE_PATH.read_text(encoding="utf-8"))
    baseline["capabilityMinimums"]["bazi"]["minEvidenceItems"] = 999
    baseline_path = tmp_path / "strict-baseline.json"
    baseline_path.write_text(json.dumps(baseline, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    summary = module.run_gate(baseline_path=baseline_path)

    assert summary["status"] == "failed"
    assert any(item["scope"] == "bazi" and item["metric"] == "minEvidenceItems" for item in summary["trendFindings"])


def test_evidence_coverage_trend_gate_detects_broken_classics_refs(tmp_path):
    module = _load_module()
    original_path = module.CLASSICS_RULE_INDEX
    try:
        broken_classics = tmp_path / "classics_rule_index.json"
        broken_classics.write_text(
            json.dumps({"schemaVersion": 1, "rules": [{"id": "only.one.rule"}]}, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        module.CLASSICS_RULE_INDEX = broken_classics

        summary = module.run_gate()
    finally:
        module.CLASSICS_RULE_INDEX = original_path

    assert summary["status"] == "failed"
    assert summary["brokenRuleRefs"]
    assert any(item["metric"] == "brokenRuleRefs" for item in summary["trendFindings"])


def test_evidence_coverage_trend_gate_cli_writes_summary(tmp_path):
    module = _load_module()
    output_json = tmp_path / "evidence-coverage-trend-cli.json"

    exit_code = module.main(["--output-json", str(output_json)])

    assert exit_code == 0
    stored = json.loads(output_json.read_text(encoding="utf-8"))
    assert stored["status"] == "passed"
    assert stored["summary"]["totalBrokenRuleRefs"] == 0
