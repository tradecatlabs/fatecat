from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from fastapi.testclient import TestClient
from fate_core.capabilities import CapabilityExecutor, CapabilityInput
from fate_core.usecases import PureAnalysisInput, calculate_pure_analysis
from main import app

ROOT = Path(__file__).resolve().parents[1]
ZIWEI_GOLDEN = ROOT / "assets" / "data" / "ziwei" / "golden" / "cases.json"


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


def test_tp01_benchmark_docs_are_landed():
    source_doc = ROOT / "assets" / "docs" / "vendor" / "八字紫微标杆来源登记.md"
    baseline_doc = ROOT / "assets" / "docs" / "reference" / "八字紫微能力基线与缺口矩阵.md"
    roadmap_doc = ROOT / "assets" / "docs" / "roadmap" / "八字紫微标杆对标路线图.md"

    for path in [source_doc, baseline_doc, roadmap_doc]:
        assert path.exists(), path
        text = path.read_text(encoding="utf-8")
        assert "八字" in text
        assert "紫微" in text

    baseline = baseline_doc.read_text(encoding="utf-8")
    for task_id in ["TP-02.01", "TP-03.02", "TP-04.05", "TP-06.03"]:
        assert task_id in baseline


def test_bazi_benchmark_hardening_fields_cover_tp02_tp03():
    result = _bazi_result()
    benchmark = result["baziBenchmark"]

    assert benchmark["timeBoundaryGolden"]["ziTimeAnalysis"]
    assert "bazi.zi_time_boundary" in benchmark["timeBoundaryGolden"]["ruleIds"]
    assert benchmark["renYuanSiling"]["siling"]["current"]
    assert "bazi.renyuan_siling_weight" in benchmark["renYuanSiling"]["ruleIds"]
    assert benchmark["strengthScore"]["label"] in {"身弱", "中和偏弱", "中和", "中和偏强", "身强"}
    assert "bazi.strength_score_golden" in benchmark["strengthScore"]["ruleIds"]
    assert [item["key"] for item in benchmark["ganzhiPriority"]] == [
        "hehua",
        "sanHui",
        "sanHe",
        "liuHe",
        "conflict",
        "ku",
    ]
    assert len(benchmark["yongShenStrategies"]) == 4
    assert benchmark["tenGodStructure"]["counts"]
    assert {item["topic"] for item in benchmark["topicProfiles"]} >= {"事业", "财运", "婚姻", "健康"}

    rule_ids = set(result["analysisEvidence"]["items"]["baziBenchmark"]["ruleIds"])
    for required in [
        "bazi.renyuan_siling_weight",
        "bazi.ganzhi_priority",
        "bazi.fortune_trigger_boundary",
        "bazi.yongshen_strategy",
        "bazi.ten_god_structure",
        "bazi.topic_profile_boundary",
    ]:
        assert required in rule_ids


def test_ziwei_benchmark_hardening_fields_cover_tp04_tp05():
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

    assert data["ziweiStarTaxonomy"]["categoryCounts"]
    assert data["ziweiStarTaxonomy"]["brightnessCounts"]
    assert len(data["ziweiPalaceRelations"]["relations"]) == 12
    assert data["ziweiMutagenFlow"]["placements"]
    assert data["ziweiStarEncyclopedia"]["entries"]
    assert len(data["ziweiPalaceTopics"]) == 12
    assert data["ziweiPatternMatches"]
    assert data["ziweiGoldenGuards"]["palaceCount"] == 12
    assert result.evidence["coverage"]["hasBenchmarkHardening"] is True

    rule_ids = set(result.evidence["items"]["benchmarkHardening"]["ruleIds"])
    for required in [
        "ziwei.star_taxonomy",
        "ziwei.brightness_state",
        "ziwei.palace_relations",
        "ziwei.mutagen_flow",
        "ziwei.golden_case_guard",
        "ziwei.star_encyclopedia_seed",
        "ziwei.pattern_match_seed",
        "ziwei.palace_topic",
    ]:
        assert required in rule_ids


def test_ziwei_golden_case_locks_core_chart_fields():
    fixture = json.loads(ZIWEI_GOLDEN.read_text(encoding="utf-8"))
    case = fixture["cases"][0]
    result = CapabilityExecutor().execute(CapabilityInput(capability_id="ziwei", payload=case["input"])).data
    expected = case["expected"]
    guards = result["ziweiGoldenGuards"]

    assert guards["palaceCount"] == expected["palaceCount"]
    assert guards["lifePalace"] == expected["lifePalace"]
    assert guards["bodyPalace"] == expected["bodyPalace"]
    assert guards["mutagenPlacementCount"] == expected["mutagenPlacementCount"]
    assert guards["fortuneLinkCount"] == expected["fortuneLinkCount"]
    emitted = set(result["analysisEvidence"]["items"]["benchmarkHardening"]["ruleIds"])
    for rule_id in expected["requiredRuleIds"]:
        assert rule_id in emitted


def test_web_workbench_is_backend_structured_and_keeps_privacy():
    client = TestClient(app)
    bazi_response = client.get(
        "/web",
        params={
            "birthDate": "1990-01-01",
            "birthTime": "08:00",
            "birthPlace": "北京",
            "gender": "male",
            "name": "测试样本",
        },
    )
    assert bazi_response.status_code == 200
    assert '<section id="bazi-workbench">' in bazi_response.text
    assert "八字工作台" in bazi_response.text
    assert "四柱 / 十神 / 藏干" in bazi_response.text
    assert "格局与用神策略" in bazi_response.text
    assert "复制 Markdown" in bazi_response.text

    ziwei_response = client.get(
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
    assert ziwei_response.status_code == 200
    assert '<section id="ziwei-workbench">' in ziwei_response.text
    assert "紫微工作台" in ziwei_response.text
    assert "十二宫 / 星曜" in ziwei_response.text
    assert "四化飞入 / 运限" in ziwei_response.text
    assert "上海" not in ziwei_response.text
    assert "已填写（非北京地区已隐藏）" in ziwei_response.text


def test_api_and_web_share_benchmark_contract_fields():
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
    assert bazi_api.json()["data"]["baziBenchmark"]["strengthScore"]

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
    ziwei_data = ziwei_api.json()["data"]
    assert ziwei_data["ziweiStarTaxonomy"]["categoryCounts"]
    assert ziwei_data["ziweiGoldenGuards"]["palaceCount"] == 12
