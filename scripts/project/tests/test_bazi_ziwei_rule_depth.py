from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from fate_core.capabilities import CapabilityExecutor, CapabilityInput
from fate_core.usecases import PureAnalysisInput, calculate_pure_analysis
from main import app

ROOT = Path(__file__).resolve().parents[1]
FATE_DIR = ROOT / "assets" / "fate"
BAZI_RULE_DEPTH_FIXTURE = ROOT / "assets" / "data" / "bazi" / "golden" / "rule_depth_cases.json"
ZIWEI_RULE_DEPTH_FIXTURE = ROOT / "assets" / "data" / "ziwei" / "golden" / "rule_depth_cases.json"


def _rule_depth_registry() -> dict:
    return json.loads((FATE_DIR / "rule_depth_registry.json").read_text(encoding="utf-8"))


def _classics_rule_ids() -> set[str]:
    data = json.loads((FATE_DIR / "classics_rule_index.json").read_text(encoding="utf-8"))
    return {rule["id"] for rule in data["rules"]}


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
    assert len([rule for rule in rules if rule["system"] == "bazi"]) >= 12
    assert len([rule for rule in rules if rule["system"] == "ziwei"]) >= 12

    for rule in rules:
        assert rule["id"] in classics
        assert rule["evidenceFields"]
        assert rule["conditions"]
        assert rule["conflictPolicy"]
        assert rule["riskBoundary"]
        assert set(rule["sourceRuleIds"]) <= classics


def test_bazi_rule_depth_outputs_rule_applications_and_evidence():
    result = _bazi_result()
    depth = result["baziRuleDepth"]

    assert depth["system"] == "bazi"
    assert depth["registryVersion"]
    assert len(depth["appliedRules"]) >= 12
    assert {item["ruleId"] for item in depth["appliedRules"]} >= {
        "bazi.depth.strength.month_root_transparency",
        "bazi.depth.pattern.establishment",
        "bazi.depth.pattern.regular_vs_special",
        "bazi.depth.yongshen.strategy_matrix",
        "bazi.depth.yongshen.tiaohou_priority",
        "bazi.depth.tengod.structure_profile",
        "bazi.depth.climate.seasonal_adjustment",
        "bazi.depth.fortune.trigger_chain",
        "bazi.depth.fortune.month_trigger",
        "bazi.depth.auxiliary.boundary_guard",
    }
    assert depth["conflictMatrix"]
    assert depth["conflictResolution"]["primaryRuleIds"]
    assert depth["conflictResolution"]["conflicts"]
    assert set(depth["sourceRuleIds"]) <= _classics_rule_ids()

    evidence = result["analysisEvidence"]["items"]["baziRuleDepth"]
    assert evidence["conclusion"]["appliedRuleCount"] == len(depth["appliedRules"])
    assert "baziRuleDepth.appliedRules" in evidence["basis"]
    assert set(evidence["ruleIds"]) <= _classics_rule_ids()


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
    assert len(depth["appliedRules"]) >= 12
    assert {item["ruleId"] for item in depth["appliedRules"]} >= {
        "ziwei.depth.star.brightness_weight",
        "ziwei.depth.palace.triad_focus",
        "ziwei.depth.mutagen.scope_chain",
        "ziwei.depth.pattern.condition_matrix",
        "ziwei.depth.pattern.sha_po_lang",
        "ziwei.depth.pattern.ji_yue_tong_liang",
        "ziwei.depth.star.encyclopedia_condition",
        "ziwei.depth.mutagen.opposition_guard",
        "ziwei.depth.palace.topic_risk_boundary",
        "ziwei.depth.fortune.linkage_chain",
    }
    assert depth["conflictResolution"]["primaryRuleIds"]
    assert depth["conflictResolution"]["conflicts"]
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
    for rule_id in expected["requiredRuleIds"]:
        assert rule_id in emitted


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
    assert "规则深度 / 冲突策略" in ziwei_web.text
    assert "ziwei.depth.mutagen.scope_chain" in ziwei_web.text
    assert "上海" not in ziwei_web.text
