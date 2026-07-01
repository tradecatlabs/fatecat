from __future__ import annotations

import json
from dataclasses import replace
from pathlib import Path

import pytest

import fate_core.capabilities.executor as capability_executor
import fate_core.capabilities.registry as capability_registry
from fate_core.capabilities import CapabilityExecutor, CapabilityInput, get_capability, list_capabilities

ROOT = Path(__file__).resolve().parents[2]
CAPABILITY_DIR = ROOT / "contracts" / "fate" / "capabilities"


def _load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def test_capability_registry_keeps_bazi_as_only_default_production_entry():
    capabilities = list_capabilities()
    by_id = {item.capability_id: item for item in capabilities}

    assert by_id["bazi"].status == "production"
    assert by_id["bazi"].default_visibility == "default"
    assert by_id["bazi"].maturity_level == "L4"
    assert by_id["bazi"].engine_version == "fate-core-bazi-v1"
    assert by_id["bazi"].deterministic is True
    assert by_id["bazi"].evidence_policy["ruleIdRequired"] is True
    assert by_id["bazi"].test_gate["status"] == "passing"
    assert by_id["almanac"].status == "production"
    assert by_id["almanac"].default_visibility == "standalone"
    assert by_id["almanac"].maturity_level == "L3"
    assert by_id["ziwei"].status == "production"
    assert by_id["ziwei"].default_visibility == "standalone"
    assert by_id["ziwei"].maturity_level == "L4"
    assert by_id["ziwei"].engine_version == "fate-core-ziwei-v1"
    assert by_id["meihua"].status == "production"
    assert by_id["meihua"].default_visibility == "standalone"
    assert by_id["meihua"].maturity_level == "L3"
    assert [item.capability_id for item in capabilities if item.default_visibility == "default"] == ["bazi"]
    for capability_id in ["liuyao", "qimen", "daliuren", "fengshui_nine_stars", "name_marriage"]:
        assert by_id[capability_id].status == "planned"
        assert by_id[capability_id].default_visibility == "standalone"
        assert by_id[capability_id].maturity_level == "L0"
        assert by_id[capability_id].engine_version == "planned-v0"
        assert by_id[capability_id].test_gate["status"] == "blocked"


def test_capability_profiles_match_registry_and_do_not_pollute_default_markdown():
    registry_ids = {item.capability_id for item in list_capabilities()}
    profile_paths = sorted((CAPABILITY_DIR / "profiles").glob("*.json"))
    profile_ids = set()

    for path in profile_paths:
        profile = _load_json(path)
        profile_ids.add(profile["capabilityId"])
        if profile["capabilityId"] == "bazi":
            assert profile["markdownDefault"] is True
            assert profile["visibility"] == "default"
        else:
            assert profile["markdownDefault"] is False
            assert profile["visibility"] == "standalone"

    assert profile_ids == registry_ids


def test_capability_schemas_define_required_protocol_boundaries():
    schema = _load_json(CAPABILITY_DIR / "schemas" / "capability.schema.json")

    assert "capabilityId" in schema["requiredCapabilityFields"]
    assert "maturity" in schema["requiredCapabilityFields"]
    assert "evidencePolicy" in schema["requiredCapabilityFields"]
    assert "testGate" in schema["requiredCapabilityFields"]
    assert schema["allowedStatus"] == ["planned", "experimental", "production"]
    assert schema["allowedMaturityLevel"] == ["L0", "L1", "L2", "L3", "L4"]
    assert "engineVersion" in schema["requiredEngineFields"]
    assert "defaultVisibility=default 必须且只能用于 bazi" in schema["invariants"]
    assert (
        "production 能力必须 testGate.status=passing 且 testGate.commands 至少包含一个本地回归入口"
        in schema["invariants"]
    )
    assert (
        "planned 能力必须 maturity.level=L0、testGate.status=blocked、provider=planned.*、engineVersion=planned-v0"
        in schema["invariants"]
    )


def test_capability_registry_enforces_infrastructure_admission_rules():
    for item in list_capabilities():
        assert item.test_gate["releaseRequired"] is True
        assert set(item.evidence_policy) >= {
            "ruleIdRequired",
            "sourceRequired",
            "calculationTraceRequired",
            "noScientificCertainty",
        }
        assert isinstance(item.evidence_policy["ruleIdRequired"], bool)

        if item.status == "production":
            assert item.test_gate["status"] == "passing"
            assert item.test_gate["commands"]
            assert item.maturity_level in {"L3", "L4"}
            assert not item.provider.startswith("planned.")
            assert item.engine_version != "planned-v0"
            continue

        if item.status == "planned":
            assert item.maturity_level == "L0"
            assert item.test_gate["status"] == "blocked"
            assert item.test_gate["commands"] == []
            assert item.provider.startswith("planned.")
            assert item.engine_version == "planned-v0"


def test_capability_registry_rejects_production_capability_without_passing_gate():
    bazi = get_capability("bazi")
    broken = replace(bazi, test_gate={**bazi.test_gate, "status": "blocked"})

    with pytest.raises(ValueError, match="testGate.status=passing"):
        capability_registry._validate_capability_admission(broken)


def test_capability_registry_rejects_planned_capability_with_real_provider():
    liuyao = get_capability("liuyao")
    broken = replace(liuyao, provider="fate_core.usecases.calculate_liuyao")

    with pytest.raises(ValueError, match=r"planned\.\* provider"):
        capability_registry._validate_capability_admission(broken)


def test_planned_capability_cannot_execute_as_production():
    with pytest.raises(ValueError, match="尚未生产化"):
        CapabilityExecutor().execute(
            CapabilityInput(
                capability_id="liuyao",
                payload={
                    "question": "测试问题",
                    "castMethod": "time",
                    "castTime": "2026-05-08 08:00:00",
                },
            )
        )


def test_almanac_capability_executes_as_standalone_production():
    result = CapabilityExecutor().execute(
        CapabilityInput(
            capability_id="almanac",
            payload={
                "dateRange": {"start": "2026-05-08", "end": "2026-05-10"},
                "eventType": "出行",
                "place": "北京",
            },
        )
    )

    assert result.capability_id == "almanac"
    assert result.status == "production"
    assert result.report_profile == "almanac"
    assert result.data["capabilityId"] == "almanac"
    assert result.data["dateRange"]["days"] == 3
    assert result.data["eventTerms"] == ["出行"]
    assert result.data["place"] == "北京"
    assert result.data["days"][0]["timeSlots"]
    assert len(result.data["days"][0]["timeSlots"]) == 12
    assert [slot["zhi"] for slot in result.data["days"][0]["timeSlots"]].count("子") == 1
    assert "scoreBreakdown" in result.data["days"][0]
    assert "xiu" in result.data["days"][0]
    assert result.evidence["source"] == "lunar-python"
    assert "almanac.time_yi_ji" in result.evidence["items"]["2026-05-08"]["ruleIds"]
    assert "almanac.zhi_xing_auxiliary" in result.evidence["items"]["2026-05-08"]["ruleIds"]
    assert set(result.evidence["items"]) == {"2026-05-08", "2026-05-09", "2026-05-10"}
    assert result.risk["disclaimerRequired"] is True
    assert result.metadata["maturity"]["level"] == "L3"
    assert result.metadata["engine"]["provider"] == "fate_core.usecases.calculate_almanac"
    assert result.metadata["engine"]["engineVersion"] == "fate-core-almanac-v1"
    assert result.metadata["evidencePolicy"]["ruleIdRequired"] is True
    assert result.metadata["testGate"]["status"] == "passing"
    assert get_capability("almanac").default_visibility == "standalone"


def test_almanac_capability_displays_submitted_place():
    result = CapabilityExecutor().execute(
        CapabilityInput(
            capability_id="almanac",
            payload={
                "dateRange": {"start": "2026-05-08", "end": "2026-05-08"},
                "eventType": "出行",
                "place": "上海市",
            },
        )
    )

    assert result.data["place"] == "上海市"
    assert "已填写（非北京地区已隐藏）" not in json.dumps(result.data, ensure_ascii=False)


def test_meihua_capability_executes_number_cast_as_standalone_production():
    result = CapabilityExecutor().execute(
        CapabilityInput(
            capability_id="meihua",
            payload={
                "question": "测试问题能否推进",
                "castMethod": "number",
                "castValue": "3,8,6",
            },
        )
    )

    assert result.capability_id == "meihua"
    assert result.status == "production"
    assert result.report_profile == "meihua"
    assert result.data["capabilityId"] == "meihua"
    assert result.data["castMethod"] == "数字起卦"
    assert result.data["hexagrams"]["movingLine"] == 5
    assert result.data["judgementBoundary"]
    assert "meihua.number_cast" in result.evidence["items"]["cast"]["ruleIds"]
    assert "meihua.body_use" in result.evidence["items"]["bodyUse"]["ruleIds"]


def test_ziwei_capability_delegates_to_ziwei_usecase(monkeypatch):
    expected_data = {
        "capabilityId": "ziwei",
        "ziweiChart": {"palaces": []},
        "analysisEvidence": {"items": {"ziweiChart": {"ruleIds": ["ziwei.iztro_chart"]}}},
    }

    monkeypatch.setattr(capability_executor, "calculate_ziwei", lambda payload: expected_data)
    result = CapabilityExecutor().execute(
        CapabilityInput(
            capability_id="ziwei",
            payload={
                "birthDateTime": "1990-01-01 08:00:00",
                "gender": "男",
                "longitude": 116.4074,
                "latitude": 39.9042,
                "birthPlace": "北京",
            },
        )
    )

    assert result.capability_id == "ziwei"
    assert result.status == "production"
    assert result.report_profile == "ziwei"
    assert result.data == expected_data
    assert result.evidence == expected_data["analysisEvidence"]
    assert result.metadata["maturity"]["level"] == "L4"
    assert result.metadata["engine"]["provider"] == "fate_core.usecases.calculate_ziwei"
    assert result.metadata["testGate"]["status"] == "passing"


def test_ziwei_capability_preserves_complete_iztro_palace_schema():
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
    assert data["capabilityId"] == "ziwei"
    assert data["meta"]["legacyZiweiBasic"] == "disabled"
    assert "ziweiBasic" not in data
    assert data["inputTrace"]["originalTime"] == "1990-01-01 08:00:00"
    assert data["inputTrace"]["trueSolarTime"]
    assert data["inputTrace"]["fixLeap"] is True
    assert data["fiveElementsClass"]
    assert data["starInfluence"] == data["fiveElementsClass"]
    interpretation = data["ziweiInterpretation"]
    assert interpretation["interpretationBoundary"]
    assert interpretation["mainStarCombinations"]
    assert interpretation["lifeBody"]
    assert interpretation["surroundedPalaces"]["life"]
    assert interpretation["mutagenPlacements"]
    assert len(interpretation["fortuneLinks"]) == 5

    palaces = data["palaceAnalysis"]
    assert len(palaces) == 12
    for palace in palaces:
        for field in [
            "index",
            "name",
            "heavenlyStem",
            "earthlyBranch",
            "isBodyPalace",
            "isOriginalPalace",
            "changsheng12",
            "boshi12",
            "jiangqian12",
            "suiqian12",
            "decadal",
            "ages",
        ]:
            assert field in palace
        assert isinstance(palace["majorStars"], list)
        assert isinstance(palace["minorStars"], list)
        assert isinstance(palace["adjectiveStars"], list)

    assert len(data["starPositions"]) == 12
    assert result.evidence["coverage"]["palaceCount"] == 12
    assert result.evidence["coverage"]["hasInterpretation"] is True
    assert "ziwei.palace_metadata" in result.evidence["items"]["ziweiChart"]["ruleIds"]
    assert "ziwei.time_index" in result.evidence["items"]["timePipeline"]["ruleIds"]
    assert "ziwei.surrounded_palaces" in result.evidence["items"]["interpretation"]["ruleIds"]


def test_bazi_capability_delegates_to_pure_analysis(monkeypatch):
    expected_data = {"analysisEvidence": {"items": {"dayMaster": {"ruleIds": ["bazi.month_command_priority"]}}}}

    monkeypatch.setattr(capability_executor, "calculate_pure_analysis", lambda payload: expected_data)
    result = CapabilityExecutor().execute(
        CapabilityInput(
            capability_id="bazi",
            payload={
                "birthDateTime": "1990-01-01 08:00:00",
                "gender": "男",
                "longitude": 116.4074,
                "latitude": 39.9042,
                "birthPlace": "北京",
            },
        )
    )

    assert result.capability_id == "bazi"
    assert result.status == "production"
    assert result.report_profile == get_capability("bazi").report_profile
    assert result.data == expected_data
    assert result.evidence == expected_data["analysisEvidence"]
    assert result.metadata["maturity"]["level"] == "L4"
    assert result.metadata["engine"]["provider"] == "fate_core.usecases.calculate_pure_analysis"
    assert result.metadata["testGate"]["status"] == "passing"
    assert result.risk["disclaimerRequired"] is True
