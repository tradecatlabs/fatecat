from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from fate_core.capabilities import CapabilityExecutor, CapabilityInput
from fate_core.usecases import PureAnalysisInput, calculate_pure_analysis
from fate_core.usecases.evaluators import build_combine_transform_matrix
from main import app

ROOT = Path(__file__).resolve().parents[2]
FATE_DIR = ROOT / "contracts" / "fate"
DATA_DIR = ROOT / "domains" / "fate-analysis" / "data-products"
BAZI_RULE_DEPTH_FIXTURE = DATA_DIR / "bazi" / "golden" / "rule_depth_cases.json"
ZIWEI_RULE_DEPTH_FIXTURE = DATA_DIR / "ziwei" / "golden" / "rule_depth_cases.json"
PURE_ANALYSIS_USECASE = (
    ROOT
    / "domains"
    / "fate-analysis"
    / "services"
    / "fate-core"
    / "src"
    / "fate_core"
    / "usecases"
    / "calculate_pure_analysis.py"
)
EVALUATORS_ROOT = (
    ROOT / "domains" / "fate-analysis" / "services" / "fate-core" / "src" / "fate_core" / "usecases" / "evaluators"
)


def _rule_depth_registry() -> dict:
    return json.loads((FATE_DIR / "rule_depth_registry.json").read_text(encoding="utf-8"))


def _classics_rule_ids() -> set[str]:
    data = json.loads((FATE_DIR / "classics_rule_index.json").read_text(encoding="utf-8"))
    return {rule["id"] for rule in data["rules"]}


def _rule_depth_rules() -> dict[str, dict]:
    return {rule["id"]: rule for rule in _rule_depth_registry()["rules"]}


def _bazi_rule_depth_fixture() -> dict:
    return json.loads(BAZI_RULE_DEPTH_FIXTURE.read_text(encoding="utf-8"))


def _bazi_result() -> dict:
    return calculate_pure_analysis(
        PureAnalysisInput(
            birth_dt=datetime(1990, 1, 1, 8, 0, 0),
            gender="male",
            longitude=116.4074,
            latitude=39.9042,
            birth_place="北京",
            name="测试样本",
            use_true_solar_time=True,
        )
    )


def _run_bazi_case(case: dict) -> dict:
    payload = case["input"]
    return calculate_pure_analysis(
        PureAnalysisInput(
            birth_dt=datetime.strptime(payload["birthDateTime"], "%Y-%m-%d %H:%M:%S"),
            gender=payload["gender"],
            longitude=float(payload["longitude"]),
            latitude=float(payload["latitude"]),
            birth_place=payload.get("birthPlace", ""),
            name="测试样本",
            use_true_solar_time=True,
        )
    )


def _pillar_names(result: dict) -> dict[str, str]:
    return {name: result["fourPillars"][name]["fullName"] for name in ["year", "month", "day", "hour"]}


def test_rule_depth_registry_is_traceable_and_bounded():
    registry = _rule_depth_registry()
    classics = _classics_rule_ids()
    rules = registry["rules"]

    assert registry["copyrightBoundary"] == "summary_only_no_commercial_copy"
    assert {rule["system"] for rule in rules} == {"bazi", "ziwei"}
    assert len([rule for rule in rules if rule["system"] == "bazi"]) >= 22
    assert len([rule for rule in rules if rule["system"] == "ziwei"]) >= 22

    for rule in rules:
        assert rule["id"] in classics
        assert rule["evidenceFields"]
        assert rule["conditions"]
        assert rule["conflictPolicy"]
        assert rule["riskBoundary"]
        assert set(rule["sourceRuleIds"]) <= classics


def test_bazi_strength_and_ten_god_evaluators_are_physically_split():
    pure_analysis = PURE_ANALYSIS_USECASE.read_text(encoding="utf-8")
    evaluator_init = (EVALUATORS_ROOT / "__init__.py").read_text(encoding="utf-8")

    assert (EVALUATORS_ROOT / "strength.py").exists()
    assert (EVALUATORS_ROOT / "ten_god.py").exists()
    assert (EVALUATORS_ROOT / "relation.py").exists()
    assert (EVALUATORS_ROOT / "regular_pattern.py").exists()
    assert (EVALUATORS_ROOT / "advanced_pattern.py").exists()
    assert (EVALUATORS_ROOT / "combine_transform.py").exists()
    assert (EVALUATORS_ROOT / "yongshen.py").exists()
    assert (EVALUATORS_ROOT / "topic_profile.py").exists()
    assert (EVALUATORS_ROOT / "constants.py").exists()
    assert "build_strength_score" in evaluator_init
    assert "build_ten_god_structure" in evaluator_init
    assert "build_relation_order" in evaluator_init
    assert "build_regular_pattern_candidates" in evaluator_init
    assert "build_special_pattern_candidates" in evaluator_init
    assert "build_combine_transform_matrix" in evaluator_init
    assert "build_yongshen_decision" in evaluator_init
    assert "build_topic_profiles" in evaluator_init
    assert "build_strength_score(" in pure_analysis
    assert "build_ten_god_structure(" in pure_analysis
    assert "_relation_order(" in pure_analysis
    assert "_build_regular_pattern_candidates(" in pure_analysis
    assert "_build_special_pattern_candidates(" in pure_analysis
    assert "_build_combine_transform_matrix(" in pure_analysis
    assert "_build_yongshen_decision(" in pure_analysis
    assert "_build_topic_profiles(" in pure_analysis
    assert "def _build_strength_score" not in pure_analysis
    assert "def _ten_god_position_evidence" not in pure_analysis
    assert "def _ten_god_values" not in pure_analysis
    assert "def _relation_order" not in pure_analysis
    assert "def _relation_blockers" not in pure_analysis
    assert "def _build_regular_pattern_candidates" not in pure_analysis
    assert "def _build_special_pattern_candidates" not in pure_analysis
    assert "def _build_combine_transform_matrix" not in pure_analysis
    assert "def _build_yongshen_decision" not in pure_analysis
    assert "def _build_topic_profiles" not in pure_analysis
    assert "def _relation_families" not in pure_analysis
    assert "def _temperature_band" not in pure_analysis


def test_bazi_rule_depth_outputs_rule_applications_and_evidence():
    result = _bazi_result()
    depth = result["baziRuleDepth"]

    assert depth["system"] == "bazi"
    assert depth["registryVersion"]
    assert len(depth["appliedRules"]) >= 22
    assert {item["ruleId"] for item in depth["appliedRules"]} >= {
        "bazi.depth.strength.month_root_transparency",
        "bazi.depth.pattern.establishment",
        "bazi.depth.pattern.regular_vs_special",
        "bazi.depth.pattern.special_pattern_checklist",
        "bazi.depth.pattern.finance_official_seal_food_matrix",
        "bazi.depth.yongshen.strategy_matrix",
        "bazi.depth.yongshen.tiaohou_priority",
        "bazi.depth.yongshen.climate_detail_matrix",
        "bazi.depth.tengod.structure_profile",
        "bazi.depth.tengod.overlap_profile",
        "bazi.depth.tengod.role_family_matrix",
        "bazi.depth.climate.seasonal_adjustment",
        "bazi.depth.relation.combine_transform_guard",
        "bazi.depth.relation.punishment_harm_break_matrix",
        "bazi.depth.fortune.trigger_chain",
        "bazi.depth.fortune.decade_year_month_order",
        "bazi.depth.fortune.month_trigger",
        "bazi.depth.statement.combination_boundary",
        "bazi.depth.statement.narrative_markdown",
        "bazi.depth.auxiliary.boundary_guard",
    }
    assert depth["conflictMatrix"]
    assert depth["conflictResolution"]["primaryRuleIds"]
    assert depth["conflictResolution"]["conflicts"]
    assert all(item["explanation"] for item in depth["conflictResolution"]["conflicts"])
    assert all(item["type"] and item["discounts"] is not None for item in depth["conflictResolution"]["conflicts"])
    assert all(item["counterEvidence"] is not None for item in depth["conflictResolution"]["conflicts"])
    assert depth["weightProfile"]["totalWeight"] > 0
    assert depth["weightProfile"]["weightedConfidence"] > 0
    assert depth["combinationStatements"]
    assert all(item["ruleIds"] and item["riskBoundary"] for item in depth["combinationStatements"])
    assert depth["narrativeSummary"]["format"] == "markdown"
    assert "依据：" in depth["narrativeSummary"]["markdown"]
    assert set(depth["sourceRuleIds"]) <= _classics_rule_ids()

    evidence = result["analysisEvidence"]["items"]["baziRuleDepth"]
    assert evidence["conclusion"]["appliedRuleCount"] == len(depth["appliedRules"])
    assert "baziRuleDepth.appliedRules" in evidence["basis"]
    assert set(evidence["ruleIds"]) <= _classics_rule_ids()


def test_bazi_core_evidence_items_have_trace_and_risk_boundary():
    result = _bazi_result()
    evidence_items = result["analysisEvidence"]["items"]
    required_items = {
        "dayMaster",
        "wuxingPreference",
        "pattern",
        "ganzhiRelations",
        "timePipeline",
        "solarTermBoundary",
        "patternUseGodTrace",
        "baziBenchmark",
        "baziRuleDepth",
    }

    assert required_items <= set(evidence_items)
    for item_id in required_items:
        item = evidence_items[item_id]
        assert item["ruleIds"], item_id
        assert item["sources"], item_id
        assert item["riskBoundary"], item_id


def test_bazi_gap_closure_benchmark_fields_are_structured():
    result = _bazi_result()
    benchmark = result["baziBenchmark"]

    strength = benchmark["strengthScore"]
    assert strength["score"] == strength["strongScore"]
    assert strength["sourceRuleId"] == "bazi.day_master_strength"
    assert strength["basis"]
    assert strength["conflicts"]
    assert all(item["factor"] and item["evidenceField"] for item in strength["basis"])
    assert all(item["type"] and item["explanation"] for item in strength["conflicts"])

    ten_god = benchmark["tenGodStructure"]
    assert ten_god["sourceRuleId"] == "bazi.ten_god_structure"
    assert ten_god["basisEvidence"]
    assert ten_god["families"]
    assert ten_god["dominant"]
    assert all(item["pillar"] and item["source"] and item["evidenceField"] for item in ten_god["basisEvidence"])

    combine = benchmark["combineTransformMatrix"]
    assert combine["schemaVersion"] == 1
    assert combine["conditionCatalog"] == [
        "paired_stems_present",
        "month_command_supports_transform_element",
        "transform_element_transparent",
        "transform_element_rooted",
        "no_direct_blocker",
    ]
    assert combine["riskBoundary"]
    for candidate in combine["candidates"]:
        assert candidate["conditions"]
        assert all("met" in condition and "evidence" in condition for condition in candidate["conditions"])
        assert candidate["status"] in {"formed_candidate", "guarded_candidate", "weak_candidate"}

    special = benchmark["patternRegistry"]["specialPatternCandidates"]
    assert {candidate["name"] for candidate in special["candidates"]} >= {
        "从格",
        "化气",
        "专旺",
        "假从",
        "从杀",
        "从财",
    }
    assert all(candidate["conditions"] and candidate["boundary"] for candidate in special["candidates"])
    assert all(candidate["status"] in {"candidate", "guarded", "not_supported"} for candidate in special["candidates"])
    assert all(candidate["maturity"]["basis"] == "condition_chain" for candidate in special["candidates"])
    assert all(candidate["appliesWhen"] and candidate["breaksWhen"] for candidate in special["candidates"])
    assert all(candidate["sourceRuleId"] in _classics_rule_ids() for candidate in special["candidates"])
    assert all(candidate["lifecycle"] == "beta" and candidate["lifecycleGate"] for candidate in special["candidates"])
    assert all("counterEvidence" in candidate for candidate in special["candidates"])
    assert all(
        candidate["maturity"]["metConditions"] <= candidate["maturity"]["totalConditions"]
        for candidate in special["candidates"]
    )

    regular = benchmark["patternRegistry"]["regularPatternCandidates"]
    assert regular["schemaVersion"] == 1
    assert regular["uncertaintyPolicy"]
    assert regular["riskBoundary"]
    assert regular["candidates"]
    assert any(candidate["status"] in {"candidate", "uncertain", "established"} for candidate in regular["candidates"])
    for candidate in regular["candidates"]:
        assert candidate["sourceRuleId"] == "bazi.pattern_by_month_command"
        assert candidate["conditions"]
        assert candidate["breaksWhen"]
        assert candidate["riskBoundary"]
        if candidate["status"] != "established":
            assert candidate["uncertainty"]

    decision = benchmark["yongShenDecision"]
    assert decision["primaryStrategy"]
    assert len(decision["scoredStrategies"]) == 4
    assert [item["score"] for item in decision["scoredStrategies"]] == sorted(
        [item["score"] for item in decision["scoredStrategies"]],
        reverse=True,
    )
    assert all(item["evidenceFields"] for item in decision["scoredStrategies"])
    assert {item["strategy"] for item in decision["scoredStrategies"]} == {"调候", "扶抑", "通关", "病药"}
    assert all(item["appliesWhen"] and item["doesNotApplyWhen"] for item in decision["scoredStrategies"])
    assert all(item["conflictPolicy"] for item in decision["scoredStrategies"])
    assert all(item["basis"] and item["scoreBasis"] for item in decision["scoredStrategies"])
    assert all(
        all(score_item["factor"] and score_item["evidenceField"] for score_item in item["scoreBasis"])
        for item in decision["scoredStrategies"]
    )
    assert decision["noAbsoluteConclusion"] is True
    assert len(decision["ranking"]) == len(decision["scoredStrategies"])
    assert [item["score"] for item in decision["ranking"]] == sorted(
        [item["score"] for item in decision["ranking"]],
        reverse=True,
    )
    assert decision["selectedCandidates"]
    assert any(item["tier"] == "parallel_review" for item in decision["selectedCandidates"])
    assert decision["conflicts"]
    assert all(
        item["type"] and item["explanation"] and item["counterEvidence"] is not None for item in decision["conflicts"]
    )
    assert [item["step"] for item in decision["decisionTrace"]] == [
        "score_strategies",
        "rank_by_score",
        "select_parallel_candidates",
        "attach_conflicts",
    ]

    topics = benchmark["topicProfiles"]
    assert {item["topic"] for item in topics} >= {"事业", "财运", "婚姻", "健康", "学业", "迁移", "家庭"}
    assert all(item["status"] == "evidence_seed" for item in topics)
    assert all(0 <= item["score"] <= 100 and item["riskBoundary"] for item in topics)
    assert all(item["lifecycle"] in {"beta", "production"} for item in topics)
    assert all(item["lifecycleGate"] for item in topics)
    assert all(item["basis"] and item["scoreBasis"] and item["evidenceFields"] for item in topics)
    assert all(item["jointScoreInputs"] and item["scoreTrace"] and item["productionGate"] for item in topics)
    assert all(item["riskPolicy"]["disclaimerRequired"] is True for item in topics)
    assert all(item["riskPolicy"]["riskLevel"] == "high_topic_boundary" for item in topics)
    assert all(
        set(item["riskPolicy"]["forbiddenClaims"])
        >= {"deterministic_future", "professional_replacement", "guarantee", "fear_claim"}
        for item in topics
    )
    assert all(item["lifecycle"] == "beta" and item["productionGate"]["status"] == "blocked" for item in topics)
    assert all(
        all(score_item["factor"] and score_item["evidenceField"] for score_item in item["scoreBasis"])
        for item in topics
    )
    for item in topics:
        assert item["scoreTrace"]["cappedScore"] == item["score"]
        assert item["scoreTrace"]["jointInputs"] == item["jointScoreInputs"]
        assert "baziBenchmark.yongShenDecision" in item["evidenceFields"]
        assert "baziBenchmark.fortuneTriggerMatrix" in item["evidenceFields"]
        assert set(item["productionGate"]["requiredEvidence"]) >= {
            "topic golden",
            "MingLi 分类回归",
            "高风险输出 policy regression",
        }
    forbidden_profile_fields = {"statement", "prediction", "judgement", "conclusion", "advice"}
    forbidden_profile_terms = {"必然", "一定", "保证", "灾祸", "疾病", "投资建议", "医疗建议"}
    for item in topics:
        assert not (forbidden_profile_fields & set(item))
        rendered = json.dumps(item, ensure_ascii=False)
        assert not any(term in rendered for term in forbidden_profile_terms)

    fortune_triggers = benchmark["fortuneTriggers"]
    assert fortune_triggers
    for trigger in fortune_triggers:
        assert trigger["triggerTypes"]
        assert trigger["reasons"]
        assert trigger["riskBoundary"]
        rendered = json.dumps(trigger, ensure_ascii=False)
        assert not any(term in rendered for term in {"必然", "一定", "保证", "灾祸"})
    fortune_matrix = benchmark["fortuneTriggerMatrix"]
    assert fortune_matrix["schemaVersion"] == 1
    assert fortune_matrix["layerOrder"] == ["original_chart", "major_stage", "annual_trigger", "monthly_refinement"]
    assert fortune_matrix["riskBoundary"]
    assert fortune_matrix["conflictPolicy"]
    matrix_by_type = {item["type"]: item for item in fortune_matrix["matrix"]}
    assert set(matrix_by_type) >= {
        "major_stage",
        "annual_trigger",
        "monthly_refinement",
        "fu_yin",
        "fan_yin",
        "sui_yun_bing_lin",
        "tian_ke_di_chong",
    }
    for item in fortune_matrix["matrix"]:
        assert item["status"] in {"available", "missing", "blocked", "triggered", "not_triggered"}
        assert item["evidenceFields"]
        assert item["appliesWhen"]
        assert item["doesNotApplyWhen"]
        assert item["riskBoundary"]
        rendered = json.dumps(item, ensure_ascii=False)
        assert not any(term in rendered for term in {"必然", "一定", "保证", "灾祸"})
    assert matrix_by_type["monthly_refinement"]["riskBoundary"] == "流月只能细化窗口，不反向覆盖大运流年。"


def test_bazi_pattern_matrix_declares_conditions_counterevidence_and_boundaries():
    rules = _rule_depth_rules()
    matrix = rules["bazi.depth.pattern.regular_vs_special"]["patternMatrix"]
    classics = _classics_rule_ids()

    assert {item["name"] for item in matrix} >= {"正格", "变格", "从格", "假从", "专旺", "化气"}
    for item in matrix:
        assert item["sourceRuleId"] in classics
        assert item["lifecycle"]
        assert item["lifecycleGate"]
        assert item["appliesWhen"]
        assert item["doesNotApplyWhen"]
        assert item["breaksWhen"]
        assert item["riskBoundary"]

    assert rules["bazi.depth.pattern.follow_transform_guard"]["patternMatrixRef"]
    assert rules["bazi.depth.pattern.special_pattern_checklist"]["patternMatrixRef"]


def test_bazi_advanced_pattern_golden_matrix_covers_lifecycle_boundaries():
    fixture = _bazi_rule_depth_fixture()
    matrix = fixture["advancedPatternGoldenMatrix"]
    case_by_id = {case["id"]: case for case in fixture["cases"]}
    pattern_contract = {
        item["name"]: item for item in _rule_depth_rules()["bazi.depth.pattern.regular_vs_special"]["patternMatrix"]
    }

    assert {item["name"] for item in matrix} >= {"正格", "变格", "从格", "假从", "专旺", "化气"}
    for item in matrix:
        contract = pattern_contract[item["name"]]
        assert item["lifecycle"] == contract["lifecycle"]
        assert item["riskBoundary"]
        assert {sample["kind"] for sample in item["samples"]} == {"positive", "negative", "boundary"}

        missing_samples = [sample for sample in item["samples"] if sample["caseId"] is None]
        if missing_samples:
            assert item["promotionBlocked"] is True
            assert item["lifecycle"] in {"beta", "beta_hitl"}
        else:
            assert item["promotionBlocked"] in {False, True}

        for sample in item["samples"]:
            assert sample["expectedStatus"]
            assert sample["evidencePath"]
            assert sample["failureExplanation"]
            if sample["caseId"] is None:
                assert sample["expectedStatus"] == "missing"
                assert sample["evidencePath"] == "future_golden_required"
                continue
            assert sample["caseId"] in case_by_id
            if sample["evidencePath"].startswith("expected.specialPatternStatuses."):
                pattern_name = sample["evidencePath"].split(".")[-1]
                observed = case_by_id[sample["caseId"]]["expected"]["specialPatternStatuses"][pattern_name]
                assert observed["status"] == sample["expectedStatus"]


def test_bazi_combine_transform_matrix_declares_states_and_counter_conditions():
    matrix = _rule_depth_rules()["bazi.depth.relation.combine_transform_guard"]["transformStateMatrix"]

    assert {item["state"] for item in matrix} >= {
        "structural_relation",
        "transform_candidate",
        "transform_success",
        "transform_broken",
        "contested_transform",
    }
    assert {item["label"] for item in matrix} >= {"成化成立", "破化/阻隔", "争合"}
    for item in matrix:
        assert item["evidenceFields"]
        assert item["requiredEvidenceFields"]
        assert item["appliesWhen"]
        assert item["doesNotApplyWhen"]
        assert item["counterConditions"]
        assert item["riskBoundary"]

    result = _bazi_result()
    emitted = result["baziBenchmark"]["combineTransformMatrix"]
    assert set(emitted["stateCatalog"]) == {
        "structural_relation",
        "transform_candidate",
        "transform_success",
        "transform_broken",
        "contested_transform",
    }
    assert set(emitted["stateContracts"]) >= set(emitted["stateCatalog"])
    for state in emitted["stateCatalog"]:
        contract = emitted["stateContracts"][state]
        assert contract["evidenceFields"]
        assert contract["requiredEvidenceFields"]
        assert contract["doesNotApplyWhen"]
        assert contract["counterConditions"]
        assert contract["riskBoundary"]
    for candidate in emitted["candidates"]:
        assert candidate["state"] in emitted["stateCatalog"]


def test_bazi_combine_transform_counterexample_matrix_covers_failure_conditions():
    fixture = _bazi_rule_depth_fixture()
    matrix = fixture["combineTransformCounterexampleMatrix"]
    evaluator_cases = {case["id"]: case for case in fixture["evaluatorStateCases"]["combineTransform"]}
    state_contracts = {
        item["state"]
        for item in _rule_depth_rules()["bazi.depth.relation.combine_transform_guard"]["transformStateMatrix"]
    }

    assert {item["scenario"] for item in matrix} >= {"破化", "争合", "阻隔", "冲破"}
    for item in matrix:
        assert item["state"] in state_contracts
        assert item["conditionChainField"] in {
            "month_command",
            "transparent_stems",
            "rooted_branches",
            "blockers",
            "counter_conditions",
        }
        assert item["failedCondition"]
        assert item["failureExplanation"]
        if item["evaluatorCaseId"] is None:
            assert item["state"] == "contested_transform"
            assert item["promotionBlocked"] is True
            continue
        assert item["evaluatorCaseId"] in evaluator_cases
        assert evaluator_cases[item["evaluatorCaseId"]]["expected"]["state"] == item["state"]


def test_bazi_yongshen_strategy_scoring_matrix_has_conflict_policy():
    matrix = _rule_depth_rules()["bazi.depth.yongshen.strategy_matrix"]["strategyScoringMatrix"]

    assert {item["strategy"] for item in matrix} >= {"调候", "扶抑", "通关", "病药", "格局用神"}
    for item in matrix:
        assert item["appliesWhen"]
        assert item["doesNotApplyWhen"]
        assert item["scoreBasis"]
        assert item["conflictPolicy"]


def test_bazi_yongshen_counterexamples_and_report_boundaries_are_declared():
    fixture = _bazi_rule_depth_fixture()
    matrix = fixture["yongShenCounterexampleMatrix"]
    case_by_id = {case["id"]: case for case in fixture["cases"]}

    assert {item["scenario"] for item in matrix} >= {
        "single_absolute_conclusion_forbidden",
        "climate_vs_strength_conflict",
        "relationship_or_imbalance_overlay",
        "topic_report_boundary",
    }
    for item in matrix:
        assert item["caseId"] in case_by_id
        assert item["expectedNoAbsoluteConclusion"] is True
        assert item["failureExplanation"]
        expected = case_by_id[item["caseId"]]["expected"]
        assert expected["yongShenNoAbsoluteConclusion"] is True
        if "requiredSelectedCandidateMin" in item:
            assert len(expected["yongShenSelectedCandidates"]) >= item["requiredSelectedCandidateMin"]
        if "requiredConflictType" in item:
            observed_types = {conflict["type"] for conflict in expected["yongShenConflictMatrix"]}
            assert item["requiredConflictType"] in observed_types
        if item["scenario"] == "topic_report_boundary":
            assert item["expectedTopicLifecycle"] == "beta"
            assert item["expectedProductionGateStatus"] == "blocked"
            assert item["forbiddenTerms"]


def test_bazi_fortune_trigger_matrix_declares_dynamic_boundaries():
    matrix = _rule_depth_rules()["bazi.depth.fortune.trigger_chain"]["triggerMatrix"]

    assert {item["type"] for item in matrix} >= {
        "major_stage",
        "annual_trigger",
        "monthly_refinement",
        "fu_yin",
        "fan_yin",
        "sui_yun_bing_lin",
        "tian_ke_di_chong",
    }
    for item in matrix:
        assert item["evidenceFields"]
        assert item["appliesWhen"]
        assert item["doesNotApplyWhen"]
        assert item["riskBoundary"]
        rendered = json.dumps(item, ensure_ascii=False)
        assert not any(term in rendered for term in {"必然", "一定", "保证"})


def test_ziwei_rule_depth_outputs_rule_applications_and_evidence():
    result = CapabilityExecutor().execute(
        CapabilityInput(
            capability_id="ziwei",
            payload={
                "birthDateTime": "1990-01-01 08:00:00",
                "gender": "男",
                "longitude": 116.4074,
                "latitude": 39.9042,
                "birthPlace": "北京",
                "name": "测试样本",
            },
        )
    )
    data = result.data
    depth = data["ziweiRuleDepth"]

    assert depth["system"] == "ziwei"
    assert depth["registryVersion"]
    assert len(depth["appliedRules"]) >= 22
    assert {item["ruleId"] for item in depth["appliedRules"]} >= {
        "ziwei.depth.star.brightness_weight",
        "ziwei.depth.star.fourteen_major_coverage",
        "ziwei.depth.star.support_malefic_balance",
        "ziwei.depth.palace.triad_focus",
        "ziwei.depth.palace.life_body_triad_bridge",
        "ziwei.depth.mutagen.scope_chain",
        "ziwei.depth.mutagen.flying_layer_guard",
        "ziwei.depth.pattern.condition_matrix",
        "ziwei.depth.pattern.sha_po_lang",
        "ziwei.depth.pattern.ji_yue_tong_liang",
        "ziwei.depth.combination.major_star_context",
        "ziwei.depth.star.encyclopedia_condition",
        "ziwei.depth.mutagen.opposition_guard",
        "ziwei.depth.mutagen.lu_quan_ke_ji_balance",
        "ziwei.depth.combination.palace_mutagen_bridge",
        "ziwei.depth.palace.topic_risk_boundary",
        "ziwei.depth.fortune.linkage_chain",
        "ziwei.depth.fortune.year_month_day_hour_order",
        "ziwei.depth.statement.combination_boundary",
        "ziwei.depth.statement.narrative_markdown",
    }
    assert depth["conflictResolution"]["primaryRuleIds"]
    assert depth["conflictResolution"]["conflicts"]
    assert all(item["explanation"] for item in depth["conflictResolution"]["conflicts"])
    assert all(item["type"] and item["discounts"] is not None for item in depth["conflictResolution"]["conflicts"])
    assert all(item["counterEvidence"] is not None for item in depth["conflictResolution"]["conflicts"])
    assert depth["weightProfile"]["totalWeight"] > 0
    assert depth["weightProfile"]["weightedConfidence"] > 0
    assert depth["combinationStatements"]
    assert all(item["ruleIds"] and item["riskBoundary"] for item in depth["combinationStatements"])
    assert depth["narrativeSummary"]["format"] == "markdown"
    assert "依据：" in depth["narrativeSummary"]["markdown"]
    assert result.evidence["coverage"]["hasRuleDepth"] is True
    assert set(result.evidence["items"]["ruleDepth"]["ruleIds"]) <= _classics_rule_ids()


@pytest.mark.parametrize(
    "case",
    json.loads(BAZI_RULE_DEPTH_FIXTURE.read_text(encoding="utf-8"))["cases"],
    ids=lambda case: case["id"],
)
def test_bazi_rule_depth_golden_cases(case: dict):
    result = _run_bazi_case(case)
    expected = case["expected"]
    depth = result["baziRuleDepth"]
    emitted = {item["ruleId"] for item in depth["appliedRules"]}

    assert _pillar_names(result) == expected["fourPillars"]
    assert result["dayMaster"]["strength"] == expected["dayMasterStrength"]
    assert result["geju"]["main"] == expected["gejuMain"]
    assert len(depth["appliedRules"]) >= expected["appliedRuleCountMin"]
    assert depth["conflictResolution"]["primaryRuleIds"] == expected["primaryRuleIds"]
    assert depth["weightProfile"]["weightedConfidence"] >= expected["weightedConfidenceMin"]
    assert {item["topic"] for item in depth["combinationStatements"]} >= set(expected["combinationTopics"])
    for rule_id in expected["requiredRuleIds"]:
        assert rule_id in emitted
    benchmark = result["baziBenchmark"]
    special = {
        item["name"]: {
            "status": item["status"],
            "score": item["score"],
            "metConditions": item["maturity"]["metConditions"],
            "totalConditions": item["maturity"]["totalConditions"],
        }
        for item in benchmark["patternRegistry"]["specialPatternCandidates"]["candidates"]
    }
    assert special == expected["specialPatternStatuses"]
    assert (
        benchmark["patternRegistry"]["specialPatternCandidates"]["riskBoundary"]
        == expected["specialPatternRiskBoundary"]
    )
    combine_states = [
        {"pair": item.get("pair"), "state": item.get("state"), "status": item.get("status"), "score": item.get("score")}
        for item in benchmark["combineTransformMatrix"]["candidates"]
    ]
    assert combine_states == expected["combineTransformStates"]
    assert [item["strategy"] for item in benchmark["yongShenDecision"]["scoredStrategies"]] == expected[
        "yongShenStrategyOrder"
    ]
    assert [
        {"strategy": item["strategy"], "score": item["score"]} for item in benchmark["yongShenDecision"]["ranking"]
    ] == expected["yongShenRanking"]
    assert [
        {
            "strategy": item["strategy"],
            "tier": item["tier"],
            "selectionReason": item["selectionReason"],
        }
        for item in benchmark["yongShenDecision"]["selectedCandidates"]
    ] == expected["yongShenSelectedCandidates"]
    assert [
        {
            "type": item["type"],
            "severity": item["severity"],
            "delta": item["delta"],
            "strategies": item["strategies"],
        }
        for item in benchmark["yongShenDecision"]["conflicts"]
    ] == expected["yongShenConflictMatrix"]
    assert [item["step"] for item in benchmark["yongShenDecision"]["decisionTrace"]] == expected[
        "yongShenDecisionTraceSteps"
    ]
    assert benchmark["yongShenDecision"]["noAbsoluteConclusion"] is expected["yongShenNoAbsoluteConclusion"]
    assert benchmark["yongShenDecision"]["riskBoundary"] == expected["yongShenRiskBoundary"]
    assert expected["failureExplanation"]["specialPatternStatuses"]
    assert expected["failureExplanation"]["combineTransformStates"]
    assert expected["failureExplanation"]["yongShenStrategyOrder"]
    assert expected["failureExplanation"]["yongShenRanking"]
    assert expected["failureExplanation"]["yongShenSelectedCandidates"]
    assert expected["failureExplanation"]["yongShenConflictMatrix"]


@pytest.mark.parametrize(
    "case",
    json.loads(BAZI_RULE_DEPTH_FIXTURE.read_text(encoding="utf-8"))["evaluatorStateCases"]["combineTransform"],
    ids=lambda case: case["id"],
)
def test_bazi_combine_transform_state_golden_cases(case: dict):
    result = build_combine_transform_matrix(case["raw"])
    expected = case["expected"]
    assert case["source"]["privacy"] == "no_real_person_data"
    assert case["source"]["productionUse"] == "test_only_not_runtime_oracle"
    assert expected["failureExplanation"]
    assert result["candidates"], case["id"]
    assert result["candidates"][0]["state"] == expected["state"]
    assert result["candidates"][0]["status"] == expected["status"]


@pytest.mark.parametrize(
    "case",
    json.loads(ZIWEI_RULE_DEPTH_FIXTURE.read_text(encoding="utf-8"))["cases"],
    ids=lambda case: case["id"],
)
def test_ziwei_rule_depth_golden_cases(case: dict):
    result = CapabilityExecutor().execute(CapabilityInput(capability_id="ziwei", payload=case["input"])).data
    expected = case["expected"]
    depth = result["ziweiRuleDepth"]
    guards = result["ziweiGoldenGuards"]
    emitted = {item["ruleId"] for item in depth["appliedRules"]}

    assert guards["lifePalace"] == expected["lifePalace"]
    assert guards["bodyPalace"] == expected["bodyPalace"]
    assert len(depth["appliedRules"]) >= expected["appliedRuleCountMin"]
    assert depth["conflictResolution"]["primaryRuleIds"] == expected["primaryRuleIds"]
    assert depth["weightProfile"]["weightedConfidence"] >= expected["weightedConfidenceMin"]
    assert {item["topic"] for item in depth["combinationStatements"]} >= set(expected["combinationTopics"])
    for rule_id in expected["requiredRuleIds"]:
        assert rule_id in emitted


def test_rule_depth_is_available_from_api_and_web_without_frontend_recalculation():
    client = TestClient(app)
    bazi_api = client.post(
        "/api/v1/capabilities/bazi",
        json={
            "birthDateTime": "1990-01-01 08:00:00",
            "gender": "男",
            "longitude": 116.4074,
            "latitude": 39.9042,
            "birthPlace": "北京",
            "name": "测试样本",
        },
    )
    assert bazi_api.status_code == 200
    assert bazi_api.json()["data"]["baziRuleDepth"]["appliedRules"]

    ziwei_api = client.post(
        "/api/v1/capabilities/ziwei",
        json={
            "birthDateTime": "1990-01-01 08:00:00",
            "gender": "男",
            "longitude": 116.4074,
            "latitude": 39.9042,
            "birthPlace": "北京",
            "name": "测试样本",
        },
    )
    assert ziwei_api.status_code == 200
    assert ziwei_api.json()["data"]["ziweiRuleDepth"]["appliedRules"]

    bazi_web = client.get(
        "/web",
        params={
            "birthDate": "1990-01-01",
            "birthTime": "08:00",
            "birthPlace": "北京",
            "gender": "male",
            "name": "测试样本",
        },
    )
    assert bazi_web.status_code == 200
    assert "综合八字规则摘要" in bazi_web.text
    assert "特殊格局边界" in bazi_web.text
    assert "规则深度 / 冲突策略" in bazi_web.text
    assert "bazi.depth.yongshen.strategy_matrix" in bazi_web.text

    ziwei_web = client.get(
        "/web",
        params={
            "birthDate": "1990-01-01",
            "birthTime": "08:00",
            "birthPlace": "上海",
            "gender": "male",
            "name": "测试样本",
            "reportSystem": "ziwei",
        },
    )
    assert ziwei_web.status_code == 200
    assert "紫微斗数规则摘要" in ziwei_web.text
    assert "命身宫-三方四正" in ziwei_web.text
    assert "规则深度 / 冲突策略" in ziwei_web.text
    assert "ziwei.depth.mutagen.scope_chain" in ziwei_web.text
    assert "上海" in ziwei_web.text
    assert "已填写（非北京地区已隐藏）" not in ziwei_web.text
