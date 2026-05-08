from __future__ import annotations

import json
from pathlib import Path

import pytest
from fate_core.capabilities import CapabilityExecutor, CapabilityInput, get_capability, list_capabilities

ROOT = Path(__file__).resolve().parents[1]
CAPABILITY_DIR = ROOT / "assets" / "fate" / "capabilities"


def _load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def test_capability_registry_keeps_bazi_as_only_default_production_entry():
    capabilities = list_capabilities()
    by_id = {item.capability_id: item for item in capabilities}

    assert by_id["bazi"].status == "production"
    assert by_id["bazi"].default_visibility == "default"
    assert by_id["almanac"].status == "production"
    assert by_id["almanac"].default_visibility == "standalone"
    assert [item.capability_id for item in capabilities if item.default_visibility == "default"] == ["bazi"]
    for capability_id in ["liuyao", "meihua", "qimen", "daliuren", "fengshui_nine_stars", "name_marriage"]:
        assert by_id[capability_id].status == "planned"
        assert by_id[capability_id].default_visibility == "standalone"


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
    assert schema["allowedStatus"] == ["planned", "experimental", "production"]
    assert "defaultVisibility=default 必须且只能用于 bazi" in schema["invariants"]


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
    assert result.evidence["source"] == "lunar-python"
    assert set(result.evidence["items"]) == {"2026-05-08", "2026-05-09", "2026-05-10"}
    assert result.risk["disclaimerRequired"] is True
    assert get_capability("almanac").default_visibility == "standalone"


def test_almanac_capability_hides_non_beijing_place():
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

    assert result.data["place"] == "已填写（非北京地区已隐藏）"
    assert "上海" not in json.dumps(result.data, ensure_ascii=False)


def test_bazi_capability_delegates_to_pure_analysis(monkeypatch):
    expected_data = {"analysisEvidence": {"items": {"dayMaster": {"ruleIds": ["bazi.month_command_priority"]}}}}

    monkeypatch.setattr("fate_core.capabilities.executor.calculate_pure_analysis", lambda payload: expected_data)
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
    assert result.risk["disclaimerRequired"] is True
