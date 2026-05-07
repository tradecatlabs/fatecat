from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FATE_DIR = ROOT / "assets" / "fate"


def _load_json(name: str) -> dict:
    with (FATE_DIR / name).open("r", encoding="utf-8") as fh:
        return json.load(fh)


def test_evidence_schema_declares_hidden_default_visibility():
    schema = _load_json("evidence_schema.json")

    assert schema["schemaVersion"] == 1
    assert schema["visibilityPolicy"]["default"] == "hidden"
    assert "ruleIds" in schema["itemFields"]


def test_weight_policy_keeps_auxiliary_and_folk_out_of_core_judgement():
    policy = _load_json("weight_policy.json")
    levels = {level["id"]: level for level in policy["levels"]}

    assert levels["core"]["rank"] > levels["auxiliary"]["rank"] > levels["folk"]["rank"]
    assert "核心喜忌" in levels["auxiliary"]["mustNotAffect"]
    assert "格局定性" in levels["folk"]["mustNotAffect"]


def test_classics_rule_index_is_traceable_and_bounded():
    index = _load_json("classics_rule_index.json")
    rules = {rule["id"]: rule for rule in index["rules"]}

    required = {
        "bazi.month_command_priority",
        "bazi.day_master_strength",
        "bazi.regulating_climate",
        "bazi.pattern_by_month_command",
        "bazi.spirits_auxiliary_only",
        "folk.bone_weight_appendix_only",
    }
    assert required <= set(rules)
    for rule in rules.values():
        assert rule["sources"]
        assert rule["appliesWhen"]
        assert rule["doesNotApplyWhen"]


def test_emitted_analysis_evidence_rule_ids_exist_in_classics_index():
    from bazi_calculator import BaziCalculator
    from report_generator import build_report_hide

    index = _load_json("classics_rule_index.json")
    indexed_rule_ids = {rule["id"] for rule in index["rules"]}
    result = BaziCalculator(
        datetime(1990, 1, 1, 8, 0, 0),
        "male",
        116.4074,
        latitude=39.9042,
        name="测试样本",
        birth_place="北京",
        use_true_solar_time=True,
    ).calculate(hide=build_report_hide("bazi"))

    emitted_rule_ids = {
        rule_id for item in result["analysisEvidence"]["items"].values() for rule_id in item.get("ruleIds", [])
    }
    assert emitted_rule_ids
    assert emitted_rule_ids <= indexed_rule_ids
