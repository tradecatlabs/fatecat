from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT_PATH = ROOT / "scripts" / "core-quality-human-review-bundle-template.py"
GATE_SCRIPT_PATH = ROOT / "scripts" / "core-quality-human-review-gate.py"
CONTRACT_PATH = ROOT / "contracts" / "fate" / "evaluations" / "core-quality-human-review-bundle-template.json"
RUBRIC_PATH = ROOT / "contracts" / "fate" / "evaluations" / "professional-quality-rubric.json"


def _load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def test_core_quality_bundle_template_contract_is_template_only() -> None:
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))

    assert contract["kind"] == "fatecat.core_quality_human_review_bundle_template_contract"
    assert contract["outputKind"] == "fatecat.core_quality_human_review_bundle_template"
    assert contract["targetEvidenceKind"] == "fatecat.core_quality_human_review_bundle"
    assert contract["targetGate"] == "fatecat.core_quality_human_review_gate"
    assert contract["templatePolicy"]["templateOnly"] is True
    assert contract["templatePolicy"]["acceptedByTargetGate"] is False
    assert "bundleSkeleton" in contract["requiredOutputFields"]
    assert "noLeakChecklist" in contract["requiredOutputFields"]
    assert "Does not mean professional review is complete." in contract["nonClaims"]


def test_core_quality_bundle_template_builds_from_rubric_and_contracts() -> None:
    module = _load_module(SCRIPT_PATH, "fatecat_core_quality_human_review_bundle_template")
    rubric = json.loads(RUBRIC_PATH.read_text(encoding="utf-8"))

    template = module.build_template(expected_commit="a" * 40)
    serialized = json.dumps(template, ensure_ascii=False, sort_keys=True)

    assert template["kind"] == "fatecat.core_quality_human_review_bundle_template"
    assert template["status"] == "operator_action_required"
    assert template["summary"]["targetBundleKind"] == "fatecat.core_quality_human_review_bundle"
    assert template["summary"]["rubricDimensions"] == len(rubric["dimensions"])
    assert template["summary"]["requiredReviewedArtifacts"] == 5
    assert template["summary"]["readyToSubmitToGate"] is False
    assert template["summary"]["templateAcceptedByTargetGate"] is False
    assert template["bundleSkeleton"]["kind"] == "fatecat.core_quality_human_review_bundle"
    assert template["bundleSkeleton"]["source"]["commit"] == "a" * 40
    assert len(template["bundleSkeleton"]["professionalReview"]["dimensions"]) == len(rubric["dimensions"])
    assert len(template["artifactHashInstructions"]) == 5
    assert template["gateExpectation"]["templateAcceptedByTargetGate"] is False
    assert "https://" not in serialized
    assert f"to{'ken'}=" not in serialized.lower()
    assert '"question"' not in serialized
    assert '"answer"' not in serialized
    assert '"markdown"' not in serialized.lower()
    assert '"content"' not in serialized.lower()


def test_core_quality_bundle_template_writes_json_and_text(tmp_path: Path) -> None:
    module = _load_module(SCRIPT_PATH, "fatecat_core_quality_human_review_bundle_template_write")
    output_json = tmp_path / "core-quality-human-review-bundle-template.json"
    output_text = tmp_path / "CORE_QUALITY_HUMAN_REVIEW_BUNDLE_TEMPLATE.md"

    template = module.build_template(expected_commit="a" * 40)
    module.write_template(template=template, output_json=output_json, output_text=output_text)

    assert output_json.is_file()
    assert output_text.is_file()
    assert json.loads(output_json.read_text(encoding="utf-8"))["kind"] == template["kind"]
    text = output_text.read_text(encoding="utf-8")
    assert "Core Quality Human Review Bundle Template" in text
    assert "Hash Instructions" in text
    assert "No-Leak Checklist" in text


def test_core_quality_bundle_template_is_rejected_by_target_gate(tmp_path: Path) -> None:
    template_module = _load_module(SCRIPT_PATH, "fatecat_core_quality_human_review_bundle_template_rejected")
    gate_module = _load_module(GATE_SCRIPT_PATH, "fatecat_core_quality_human_review_gate_from_template")
    template_json = tmp_path / "template.json"
    _write_json(template_json, template_module.build_template(expected_commit="a" * 40))

    assert gate_module.main(["--review-evidence-json", str(template_json), "--expected-commit", "a" * 40]) == 1


def test_core_quality_bundle_template_rejects_bad_commit() -> None:
    module = _load_module(SCRIPT_PATH, "fatecat_core_quality_human_review_bundle_template_bad_commit")

    try:
        module.build_template(expected_commit="not-a-commit")
    except Exception as exc:  # noqa: BLE001
        assert "expected-commit" in str(exc)
    else:
        raise AssertionError("bad commit should be rejected")


def test_core_quality_bundle_template_cli_outputs_json_and_text(tmp_path: Path) -> None:
    output_json = tmp_path / "template.json"
    output_text = tmp_path / "TEMPLATE.md"

    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT_PATH),
            "--output-json",
            str(output_json),
            "--output-markdown",
            str(output_text),
            "--expected-commit",
            "a" * 40,
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    cli_summary = json.loads(result.stdout)

    assert cli_summary["kind"] == "fatecat.core_quality_human_review_bundle_template"
    assert cli_summary["templateGate"] == "operator_action_required"
    assert cli_summary["rubricDimensions"] >= 8
    assert cli_summary["readyToSubmitToGate"] is False
    assert cli_summary["templateAcceptedByTargetGate"] is False
    assert output_json.is_file()
    assert output_text.is_file()


def test_core_quality_bundle_template_wiring_mentions_local_ci_docs_registry_and_agents() -> None:
    local_ci = (ROOT / "scripts" / "local-ci.sh").read_text(encoding="utf-8")
    scripts_agents = (ROOT / "scripts" / "AGENTS.md").read_text(encoding="utf-8")
    eval_agents = (ROOT / "contracts" / "fate" / "evaluations" / "AGENTS.md").read_text(encoding="utf-8")
    tests_agents = (ROOT / "tests" / "AGENTS.md").read_text(encoding="utf-8")
    registry = (ROOT / "contracts" / "fate" / "evaluations" / "registry.json").read_text(encoding="utf-8")
    roadmap = (ROOT / "docs" / "reference-materials" / "roadmap" / "测算基础设施100%实现计划.md").read_text(
        encoding="utf-8"
    )

    assert "core quality human review bundle template" in local_ci
    assert "FATE_LOCAL_CI_CORE_QUALITY_HUMAN_REVIEW_BUNDLE_TEMPLATE" in local_ci
    assert "core-quality-human-review-bundle-template.py" in scripts_agents
    assert "core-quality-human-review-bundle-template.json" in eval_agents
    assert "test_core_quality_human_review_bundle_template.py" in tests_agents
    assert "run.core_quality_human_review_bundle_template" in registry
    assert "Core quality evidence bundle rehearsal" in roadmap
