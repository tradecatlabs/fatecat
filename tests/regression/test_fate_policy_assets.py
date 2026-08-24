from __future__ import annotations

import json
import tomllib
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FATE_DIR = ROOT / "contracts" / "fate"
REFERENCE_MANIFEST = ROOT / "tools" / "reference-repos" / "vendor_sources.json"
FORBIDDEN_RULE_FIELDS = {"statement", "prediction", "judgement", "conclusion", "advice"}


def _load_json(name: str) -> dict:
    with (FATE_DIR / name).open("r", encoding="utf-8") as fh:
        return json.load(fh)


def _load_reference_manifest() -> dict:
    with REFERENCE_MANIFEST.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def _reference_entries() -> dict[str, dict]:
    manifest = _load_reference_manifest()
    entries = manifest["required"] + manifest["optionalFutureFeatures"] + manifest.get("legacyUnreviewedSnapshots", [])
    return {entry["id"]: entry for entry in entries}


def test_evidence_schema_declares_hidden_default_visibility():
    schema = _load_json("evidence_schema.json")

    assert schema["schemaVersion"] == 1
    assert schema["visibilityPolicy"]["default"] == "hidden"
    assert "ruleIds" in schema["itemFields"]
    assert "riskBoundary" in schema["itemFields"]


def test_weight_policy_keeps_auxiliary_and_folk_out_of_core_judgement():
    policy = _load_json("weight_policy.json")
    levels = {level["id"]: level for level in policy["levels"]}

    assert levels["core"]["rank"] > levels["auxiliary"]["rank"] > levels["folk"]["rank"]
    assert "核心喜忌" in levels["auxiliary"]["mustNotAffect"]
    assert "格局定性" in levels["folk"]["mustNotAffect"]


def test_pure_analysis_profile_declares_canonical_and_compatibility_fields():
    profile = _load_json("profiles/pure_analysis.json")
    semantics = profile["fieldSemantics"]

    assert "唯一事实源" in semantics["branchRelations"]
    assert "过渡容器" in semantics["ganzhiRelations"]
    assert "deprecatedAsSourceFields" in semantics["ganzhiRelations"]
    assert "不得独立计算或渲染" in semantics["spirits"]
    assert "不得独立计算或渲染" in semantics["spiritsExplain"]


def test_classics_rule_index_is_traceable_and_bounded():
    index = _load_json("classics_rule_index.json")
    rules = {rule["id"]: rule for rule in index["rules"]}
    policy = index["governance"]["extensionPolicy"]

    required = {
        "bazi.month_command_priority",
        "bazi.day_master_strength",
        "bazi.regulating_climate",
        "bazi.pattern_by_month_command",
        "bazi.spirits_auxiliary_only",
        "folk.bone_weight_appendix_only",
    }
    assert index["owner"] == "tradecatlabs/fate-core"
    assert set(policy["requiredRuleFields"]) >= {
        "id",
        "system",
        "topic",
        "summary",
        "sources",
        "appliesWhen",
        "doesNotApplyWhen",
    }
    assert set(policy["forbiddenRuleFields"]) == FORBIDDEN_RULE_FIELDS
    assert required <= set(rules)
    for rule in rules.values():
        assert set(policy["requiredRuleFields"]) <= set(rule)
        assert FORBIDDEN_RULE_FIELDS.isdisjoint(rule)
        assert rule["sources"]
        assert rule["appliesWhen"]
        assert rule["doesNotApplyWhen"]


def test_rule_depth_registry_declares_owner_and_extension_gate():
    registry = _load_json("rule_depth_registry.json")
    classics = {rule["id"] for rule in _load_json("classics_rule_index.json")["rules"]}
    policy = registry["governance"]["extensionPolicy"]

    assert registry["owner"] == "tradecatlabs/fate-core"
    assert policy["riskBoundaryRequired"] is True
    assert set(policy["requiredRuleFields"]) >= {
        "id",
        "system",
        "layer",
        "topic",
        "priority",
        "weight",
        "evidenceFields",
        "conditions",
        "conflictPolicy",
        "riskBoundary",
        "sourceRuleIds",
    }
    assert set(policy["forbiddenRuleFields"]) == FORBIDDEN_RULE_FIELDS

    for rule in registry["rules"]:
        assert set(policy["requiredRuleFields"]) <= set(rule)
        assert FORBIDDEN_RULE_FIELDS.isdisjoint(rule)
        assert rule["riskBoundary"]
        assert rule["conditions"]
        assert rule["evidenceFields"]
        assert set(rule["sourceRuleIds"]) <= classics


def test_rule_policy_assets_use_boundary_language_without_high_risk_suggestion_terms():
    forbidden_terms = {"医疗建议", "投资建议", "法律建议", "心理建议", "保证", "必然", "灾祸"}
    for name in ("classics_rule_index.json", "rule_depth_registry.json"):
        rendered = json.dumps(_load_json(name), ensure_ascii=False)
        assert not any(term in rendered for term in forbidden_terms), name


def test_future_features_have_owner_and_cannot_auto_return_to_standard_report():
    registry = _load_json("future_features.json")
    policy = registry["governance"]["extensionPolicy"]
    forbidden = set(policy["forbiddenFeatureFields"])

    assert registry["owner"] == "tradecatlabs/fate-core"
    assert set(policy["requiredFeatureFields"]) >= {
        "id",
        "title",
        "previousReportBlock",
        "requiredBeforeProduction",
    }
    assert "标准报告不自动恢复" in policy["productionPromotionGate"]

    for feature in registry["futureFeatures"]:
        assert set(policy["requiredFeatureFields"]) <= set(feature)
        assert forbidden.isdisjoint(feature)
        assert feature["requiredBeforeProduction"]


def test_lunar_python_is_declared_as_runtime_dependency():
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    dependencies = set(pyproject["project"]["dependencies"])
    requirements = (ROOT / "requirements.txt").read_text(encoding="utf-8").splitlines()
    locked = (ROOT / "requirements.lock.txt").read_text(encoding="utf-8").splitlines()

    assert "lunar-python>=1.4.8" in dependencies
    assert "lunar-python>=1.4.8" in requirements
    assert "lunar-python==1.4.8" in locked


def test_tabulate_wide_character_support_is_declared_as_runtime_dependency():
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    dependencies = set(pyproject["project"]["dependencies"])
    requirements = (ROOT / "requirements.txt").read_text(encoding="utf-8").splitlines()
    locked = (ROOT / "requirements.lock.txt").read_text(encoding="utf-8").splitlines()

    assert "tabulate[widechars]>=0.9.0" in dependencies
    assert "tabulate[widechars]>=0.9.0" in requirements
    assert "wcwidth==0.8.1" in locked


def test_project_classifier_matches_independent_deployment_beta_status():
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))

    assert "Development Status :: 4 - Beta" in pyproject["project"]["classifiers"]
    assert "Development Status :: 3 - Alpha" not in pyproject["project"]["classifiers"]
    assert "Development Status :: 5 - Production/Stable" not in pyproject["project"]["classifiers"]


def test_lunar_calendar_adapter_prefers_declared_dependency_over_vendor_path():
    adapter = ROOT / "domains/fate-analysis/services/fate-core/src/fate_core/adapters/lunar_calendar.py"
    source = adapter.read_text(encoding="utf-8")

    assert "from lunar_python import Solar" in source
    assert "except ModuleNotFoundError" in source
    assert "sys.path.insert(0, str(LUNAR_PYTHON_DIR))" in source
    assert source.index("from lunar_python import Solar") < source.index("except ModuleNotFoundError")


def test_bazi_kernel_prefers_declared_lunar_python_dependency_over_vendor_path():
    kernel = ROOT / "domains/fate-analysis/services/fate-core/src/fate_core/kernel/bazi_calculator.py"
    source = kernel.read_text(encoding="utf-8")

    assert "from lunar_python import Solar" in source
    assert "except ModuleNotFoundError" in source
    assert "sys.path.insert(0, str(LUNAR_PYTHON_DIR))" in source
    assert source.index("from lunar_python import Solar") < source.index("except ModuleNotFoundError")


def test_reference_manifest_declares_bazi_source_roles_and_risks():
    entries = _reference_entries()
    required_ids = {
        "lunar-python",
        "bazi-1",
        "sxwnl",
        "iztro",
        "MingLi-Bench",
        "bazica",
        "bazi-calculator-by-alvamind",
        "dantalion",
    }

    assert required_ids <= set(entries)
    assert entries["lunar-python"]["usageRole"] == "production_dependency"
    assert entries["lunar-python"]["productionUseAllowed"] is True
    assert entries["MingLi-Bench"]["usageRole"] == "evaluation_only"
    assert entries["bazica"]["usageRole"] == "oracle_only"
    assert entries["bazi-calculator-by-alvamind"]["usageRole"] == "reference_only"


def test_reference_manifest_entries_have_usage_contract_fields():
    for entry in _reference_entries().values():
        assert entry["usageRole"] in {
            "production_dependency",
            "oracle_only",
            "evaluation_only",
            "reference_only",
            "future_candidate",
        }
        assert isinstance(entry["productionUseAllowed"], bool)
        assert "riskNote" in entry


def test_reference_manifest_blocks_missing_license_materials_from_production_role():
    distribution_decision = _load_json("developer/public-server-distribution.json")
    approved_assets = {item["id"]: item for item in distribution_decision["approvedAssets"]}

    for entry in _reference_entries().values():
        non_production_license = entry["licenseStatus"] in {
            "missing_upstream_license",
            "license_file_unreviewed",
        }
        if non_production_license:
            assert entry.get("auditRequired") is True
            assert entry["usageRole"] != "production_dependency"
            assert entry["productionUseAllowed"] is False
            if entry["distributionAllowed"] is True:
                approved = approved_assets[entry["id"]]
                assert entry["license"] == approved["license"] == "NOASSERTION"
                assert entry["licenseStatus"] == approved["licenseStatus"]
                assert entry["distributionExceptionRef"].endswith(f"#approvedAssets/{entry['id']}")
                assert set(entry["distributionExceptionScopes"]) <= set(approved["scopes"])
            else:
                assert "distributionExceptionRef" not in entry
        if entry["id"] == "bazi-calculator-by-alvamind":
            assert entry.get("auditRequired") is True
            assert entry["usageRole"] == "reference_only"
            assert entry["productionUseAllowed"] is False


def test_reference_manifest_covers_every_github_snapshot_directory():
    manifest = _load_reference_manifest()
    declared_paths = {
        entry["path"]
        for scope in ("required", "optionalFutureFeatures", "legacyUnreviewedSnapshots")
        for entry in manifest.get(scope, [])
        if entry["path"].startswith("github/")
    }
    actual_paths = {
        f"github/{path.name}" for path in (ROOT / "tools" / "reference-repos" / "github").iterdir() if path.is_dir()
    }

    assert actual_paths == declared_paths


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
