from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GATE_PATH = ROOT / "scripts" / "core-quality-corpus-gate.py"
MANIFEST_PATH = ROOT / "contracts" / "fate" / "evaluations" / "core-quality-corpus.json"
POLICY_PATH = ROOT / "contracts" / "fate" / "evaluations" / "report-diff-policy.json"
RUBRIC_PATH = ROOT / "contracts" / "fate" / "evaluations" / "professional-quality-rubric.json"
REGISTRY_PATH = ROOT / "contracts" / "fate" / "evaluations" / "registry.json"


def _load_gate():
    spec = importlib.util.spec_from_file_location("fatecat_core_quality_corpus_gate", GATE_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_core_quality_corpus_gate_passes_and_writes_summary(tmp_path):
    gate = _load_gate()
    output_json = tmp_path / "core-quality-corpus-gate.json"

    exit_code = gate.main(["--output-json", str(output_json)])

    assert exit_code == 0
    stored = json.loads(output_json.read_text(encoding="utf-8"))
    assert stored["schemaVersion"] == 1
    assert stored["kind"] == "fatecat.core_quality_corpus_gate"
    assert stored["status"] == "passed"
    assert stored["summary"]["corpusCount"] == 5
    assert stored["summary"]["totalCaseCount"] >= 340
    assert stored["professionalQualityRubric"] == "contracts/fate/evaluations/professional-quality-rubric.json"
    assert stored["professionalRubric"]["dimensionCount"] >= 8
    assert stored["professionalRubric"]["requiredCapabilityCount"] == 2
    assert stored["professionalRubric"]["requiredEvidenceKindCount"] == 5
    bazi_statements = next(item for item in stored["corpora"] if item["id"] == "corpus.bazi.statement_cases")
    assert bazi_statements["caseCount"] >= 8
    ziwei_basic = next(item for item in stored["corpora"] if item["id"] == "corpus.ziwei.basic_cases")
    assert ziwei_basic["caseCount"] >= 12
    assert ziwei_basic["coverageTagCount"] >= 31
    ziwei_depth = next(item for item in stored["corpora"] if item["id"] == "corpus.ziwei.rule_depth")
    assert ziwei_depth["caseCount"] >= 12
    assert "真实非北京地区" in stored["privacyBoundary"]
    assert any("不新增真实命例" in item for item in stored["limits"])


def test_core_quality_corpus_manifest_and_report_diff_policy_are_registered():
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    policy = json.loads(POLICY_PATH.read_text(encoding="utf-8"))
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))

    assert registry["metadata"]["coreQualityCorpusManifest"] == "contracts/fate/evaluations/core-quality-corpus.json"
    assert registry["metadata"]["reportDiffPolicy"] == "contracts/fate/evaluations/report-diff-policy.json"
    assert (
        registry["metadata"]["professionalQualityRubric"]
        == "contracts/fate/evaluations/professional-quality-rubric.json"
    )
    assert registry["metadata"]["coreQualityCorpusGateCommand"] == "bash scripts/core-quality-corpus-gate.sh"
    assert manifest["releaseGate"]["required"] is True
    assert manifest["professionalQualityRubric"]["minimumDimensionCount"] >= 8
    assert policy["thresholds"]["minBaziGoldenCases"] >= 300
    assert policy["thresholds"]["minZiweiGoldenCases"] >= 12
    assert policy["thresholds"]["minProfessionalRubricDimensions"] >= 8
    assert policy["structuralDiff"]["summaryOnly"] is True
    assert "fullReport" in policy["structuralDiff"]["forbiddenStoredFields"]
    assert "紫微斗数" in policy["profiles"]["bazi"]["structurePolicy"]["forbiddenDefaultBlocks"]
    assert "八字排盘详情" in policy["profiles"]["ziwei"]["structurePolicy"]["forbiddenDefaultBlocks"]


def test_core_quality_corpus_fixture_privacy_boundary():
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

    for corpus in manifest["corpora"]:
        data = json.loads((ROOT / corpus["path"]).read_text(encoding="utf-8"))
        assert data["source"] == "synthetic_anonymous_fixture"
        assert len(data["cases"]) >= corpus["minCaseCount"]
        for case in data["cases"]:
            assert case["input"]["birthPlace"] == "北京"
            assert case["input"].get("name", "测试样本") == "测试样本"
            if corpus["id"] == "corpus.ziwei.basic_cases":
                assert case["coverageTags"]


def test_professional_quality_rubric_enforces_review_boundary_and_forbidden_claims():
    rubric = json.loads(RUBRIC_PATH.read_text(encoding="utf-8"))

    assert rubric["kind"] == "fatecat.professional_quality_rubric"
    assert rubric["scope"]["usageRole"] == "evaluation_only"
    assert rubric["minimums"]["dimensionCount"] >= 8
    assert set(rubric["minimums"]["requiredCapabilities"]) == {"bazi", "ziwei"}
    assert {
        "golden_fixture",
        "report_diff_summary",
        "evidence_ref",
        "privacy_scan",
        "human_review_note",
    } <= set(rubric["minimums"]["requiredEvidenceKinds"])
    assert len(rubric["dimensions"]) >= rubric["minimums"]["dimensionCount"]
    assert {item["id"] for item in rubric["dimensions"]} >= {
        "rubric.calendar_boundary",
        "rubric.bazi_pattern_yongshen",
        "rubric.ziwei_chart_integrity",
        "rubric.report_structure",
        "rubric.privacy_and_non_claim",
    }
    assert rubric["humanReview"]["status"] == "required_before_external_claim"
    assert {"预测准确率 100%", "专业能力 100% 已证明", "确定未来"} <= set(rubric["forbiddenClaims"])
    assert any("不等于真实命例准确率证明" in item for item in rubric["limitations"])
