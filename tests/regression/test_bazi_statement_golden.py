from __future__ import annotations

import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import pytest

from fate_core.kernel.bazi_calculator import BaziCalculator
from fate_core.usecases import PureAnalysisInput, calculate_pure_analysis

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "domains" / "fate-analysis" / "data-products" / "bazi" / "golden" / "statement_cases.json"


def _load_fixture() -> dict:
    with FIXTURE.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def _run_case(case: dict) -> dict:
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


def _relation_pillars(branches: tuple[str, str, str, str]) -> dict[str, dict[str, str]]:
    return {
        position: {"stem": stem, "branch": branch}
        for position, stem, branch in zip(
            ("year", "month", "day", "hour"),
            ("甲", "乙", "丙", "丁"),
            branches,
            strict=True,
        )
    }


def _branch_relations(branches: tuple[str, str, str, str]) -> dict:
    calculator = object.__new__(BaziCalculator)
    return calculator._calc_zhi_relations(_relation_pillars(branches))


def _canonical_relation_violations(relations: list[dict]) -> list[str]:
    violations = []
    keys = [item.get("key") for item in relations]
    if len(keys) != len(set(keys)):
        violations.append("duplicate_key")
    if any(len(item.get("positions", [])) != len(set(item.get("positions", []))) for item in relations):
        violations.append("same_position_instance")
    return violations


@pytest.mark.parametrize("branch", ("辰", "午", "酉", "亥"))
def test_single_branch_instance_does_not_create_self_punishment(branch: str):
    fillers = tuple(value for value in ("子", "寅", "巳", "未") if value != branch)[:3]
    relations = _branch_relations((branch, *fillers))

    self_punishments = [
        item for item in relations["canonical"] if item["relation"] == "刑" and item["branches"] == [branch, branch]
    ]
    assert self_punishments == []


@pytest.mark.parametrize("branch", ("辰", "午", "酉", "亥"))
def test_two_distinct_branch_instances_create_one_self_punishment(branch: str):
    fillers = tuple(value for value in ("子", "寅", "巳", "未") if value != branch)[:2]
    relations = _branch_relations((branch, branch, *fillers))

    self_punishments = [
        item for item in relations["canonical"] if item["relation"] == "刑" and item["branches"] == [branch, branch]
    ]
    assert len(self_punishments) == 1
    assert set(self_punishments[0]["positions"]) == {"year", "month"}
    assert self_punishments[0]["source"] == "bazi-1.zhi_atts"


def test_symmetric_and_directional_branch_relations_have_stable_unique_keys():
    relations = _branch_relations(("巳", "子", "寅", "辰"))
    canonical = relations["canonical"]

    assert _canonical_relation_violations(canonical) == []
    assert len({item["key"] for item in canonical}) == len(canonical)
    assert sum(item["relation"] == "害" and set(item["branches"]) == {"巳", "寅"} for item in canonical) == 1
    assert sum(item["relation"] == "合" and set(item["branches"]) == {"子", "辰"} for item in canonical) == 1
    punishments = [item for item in canonical if item["relation"] == "刑" and set(item["branches"]) == {"巳", "寅"}]
    assert len(punishments) == 1
    assert punishments[0]["directional"] is True
    assert punishments[0]["positions"] == ["day", "year"]


def test_relation_uniqueness_gate_detects_injected_invalid_records():
    invalid = [
        {"key": "branch:刑:year-year", "positions": ["year", "year"]},
        {"key": "branch:刑:year-year", "positions": ["year", "month"]},
    ]

    assert _canonical_relation_violations(invalid) == ["duplicate_key", "same_position_instance"]


def test_canonical_relation_order_is_stable_across_hash_seeds():
    script = """
import json
from fate_core.kernel.bazi_calculator import BaziCalculator

pillars = {
    position: {"stem": stem, "branch": branch}
    for position, stem, branch in zip(
        ("year", "month", "day", "hour"),
        ("甲", "乙", "丙", "丁"),
        ("丑", "戌", "未", "辰"),
        strict=True,
    )
}
calculator = object.__new__(BaziCalculator)
relations = calculator._calc_zhi_relations(pillars)
print(json.dumps([item["key"] for item in relations["canonical"]], ensure_ascii=False))
"""
    outputs = []
    for seed in ("1", "2", "3"):
        env = os.environ.copy()
        env["PYTHONHASHSEED"] = seed
        result = subprocess.run(
            [sys.executable, "-c", script],
            cwd=ROOT,
            env=env,
            check=True,
            capture_output=True,
            text=True,
        )
        outputs.append(result.stdout.strip())

    assert len(set(outputs)) == 1


@pytest.mark.parametrize("case", _load_fixture()["cases"], ids=lambda case: case["id"])
def test_bazi_statement_cases_lock_core_judgement_boundaries(case: dict):
    result = _run_case(case)
    expected = case["expected"]

    assert _pillar_names(result) == expected["fourPillars"]
    assert result["dayMaster"]["stem"] == expected["dayMaster"]["stem"]
    assert result["dayMaster"]["strength"] == expected["dayMaster"]["strength"]
    assert result["geju"]["main"] == expected["gejuMain"]

    yong_shen = result["yongShen"]
    assert yong_shen.get("note", "") == expected["yongShen"]["note"]
    assert yong_shen.get("basisSource", "") == expected["yongShen"]["basisSource"]
    assert yong_shen.get("tiaohouRaw", "") == expected["yongShen"]["tiaohouRaw"]

    assert result["ganzhiRelations"]["tianGan"] == expected["ganzhiRelations"]["tianGan"]
    assert len(result["branchRelations"]["canonical"]) == expected["ganzhiRelations"]["canonicalRelationCount"]
    assert result["ganzhiRelations"]["projectionOf"]["diZhi"] == "branchRelations.canonical"
    assert result["ganzhiRelations"]["deprecatedAsSourceFields"] == ["diZhi"]
    assert len(result["ganzhiRelations"]["diZhi"]) == len(set(result["ganzhiRelations"]["diZhi"]))
    assert result["jiaoYun"]["startDate"] == expected["fortuneStart"]["startDate"]
    assert result["jiaoYun"]["jiaoJieQi"] == expected["fortuneStart"]["anchorTerm"]

    emitted_rule_ids = {
        rule_id for item in result["analysisEvidence"]["items"].values() for rule_id in item.get("ruleIds", [])
    }
    for rule_id in expected["accuracyRuleIds"]:
        assert rule_id in emitted_rule_ids

    forbidden_topic_terms = {
        "必然",
        "一定",
        "保证",
        "灾祸",
        "疾病",
        "医疗建议",
        "投资建议",
        "法律建议",
        "心理建议",
        "必破产",
        "必离婚",
    }
    forbidden_topic_fields = {"statement", "prediction", "judgement", "conclusion", "advice"}
    topic_profiles = result["baziBenchmark"]["topicProfiles"]
    assert topic_profiles
    for profile in topic_profiles:
        assert profile["lifecycle"] == "beta"
        assert profile["productionGate"]["status"] == "blocked"
        assert profile["riskPolicy"]["disclaimerRequired"] is True
        assert forbidden_topic_fields.isdisjoint(profile)
        rendered = json.dumps(profile, ensure_ascii=False)
        assert not any(term in rendered for term in forbidden_topic_terms)
