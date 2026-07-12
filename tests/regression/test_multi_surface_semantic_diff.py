from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_multi_surface_semantic_diff_gate_outputs_hash_only_summary(tmp_path: Path):
    output_json = tmp_path / "multi-surface-semantic-diff.json"

    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "multi-surface-semantic-diff.py"),
            "--output-json",
            str(output_json),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        timeout=30,
        check=False,
    )

    assert result.returncode == 0, result.stderr or result.stdout
    payload = json.loads(output_json.read_text(encoding="utf-8"))
    assert payload["kind"] == "fatecat.multi_surface_semantic_diff"
    assert payload["status"] == "passed"
    assert payload["reportSystems"] == ["bazi", "ziwei"]
    assert payload["semanticPolicy"]["noMarkdownBodyInEvidence"] is True
    assert payload["semanticPolicy"]["requiredLocalEvidenceSurfaces"] == ["surface.cli", "surface.agent_skill"]
    assert payload["externalPending"][0]["status"] == "外部连通验证待执行"

    for comparison in payload["comparisons"]:
        assert comparison["status"] == "passed"
        assert comparison["baselineSurface"] == "surface.fastapi.direct"
        assert len(comparison["surfaces"]) == 6
        semantic_hashes = {surface["semanticSha256"] for surface in comparison["surfaces"]}
        assert len(semantic_hashes) == 1
        assert {surface["status"] for surface in comparison["surfaces"]} == {"passed"}
        assert all(surface["equalToBaseline"] is True for surface in comparison["surfaces"])

    evidence_by_surface = {item["surfaceId"]: item for item in payload["nonMarkdownSurfaceEvidence"]}
    assert evidence_by_surface["surface.cli"]["status"] == "passed"
    assert evidence_by_surface["surface.cli"]["evidenceKind"] == "fatecat.capability_cli_smoke"
    assert {item["capabilityId"] for item in evidence_by_surface["surface.cli"]["capabilities"]} == {
        "almanac",
        "bazi",
        "meihua",
        "ziwei",
    }
    assert evidence_by_surface["surface.cli"]["plannedCapabilityRejection"]["actualExitCode"] == 1
    assert evidence_by_surface["surface.agent_skill"]["status"] == "passed"
    assert set(evidence_by_surface["surface.agent_skill"]["checkedFiles"]) == {
        "SKILL.md",
        "references/commands.md",
        "references/io-contract.md",
    }

    text = json.dumps(payload, ensure_ascii=False)
    assert "# 命理排盘报告" not in text
    assert "# 紫微斗数报告" not in text
    assert "token=" not in text.lower()
    assert "secret=" not in text.lower()
    assert "password=" not in text.lower()


def test_multi_surface_semantic_diff_contract_registry_and_local_ci_wiring():
    contract = json.loads(
        (ROOT / "contracts" / "fate" / "delivery" / "multi-surface-semantic-diff.json").read_text(encoding="utf-8")
    )
    registry = json.loads((ROOT / "contracts" / "fate" / "delivery" / "registry.json").read_text(encoding="utf-8"))
    local_ci = (ROOT / "scripts" / "local-ci.sh").read_text(encoding="utf-8")
    scripts_agents = (ROOT / "scripts" / "AGENTS.md").read_text(encoding="utf-8")
    delivery_agents = (ROOT / "contracts" / "fate" / "delivery" / "AGENTS.md").read_text(encoding="utf-8")

    assert contract["resourceType"] == "DeliverySemanticDiffGate"
    assert contract["outputKind"] == "fatecat.multi_surface_semantic_diff"
    assert contract["semanticPolicy"]["rawMarkdownMustNotBeStored"] is True
    assert {item["surfaceId"] for item in contract["requiredLocalEvidenceSurfaces"]} == {
        "surface.cli",
        "surface.agent_skill",
    }
    assert {item["surfaceId"] for item in contract["nonMarkdownSurfacePolicy"]} == {
        "surface.cli",
        "surface.agent_skill",
    }
    assert "surface.telegram_bot.live" in {item["surfaceId"] for item in contract["externalPending"]}
    assert registry["multiSurfaceSemanticDiffGate"]["contract"] == (
        "contracts/fate/delivery/multi-surface-semantic-diff.json"
    )
    assert "bash scripts/multi-surface-semantic-diff.sh --output-json <path>" in json.dumps(
        registry, ensure_ascii=False
    )
    assert "multi-surface-semantic-diff.json" in local_ci
    assert "capability-cli-smoke.json" in local_ci
    assert "test_multi_surface_semantic_diff.py" in local_ci
    assert "multi-surface-semantic-diff.sh" in scripts_agents
    assert "multi-surface-semantic-diff.json" in delivery_agents


def test_standard_surfaces_use_single_capability_engine():
    main_source = (
        ROOT / "domains" / "experience-delivery" / "services" / "fatecat-delivery" / "src" / "main.py"
    ).read_text(encoding="utf-8")
    web_source = (
        ROOT / "domains" / "experience-delivery" / "services" / "fatecat-delivery" / "src" / "web_report_service.py"
    ).read_text(encoding="utf-8")
    bot_source = (
        ROOT / "domains" / "experience-delivery" / "services" / "fatecat-delivery" / "src" / "bot.py"
    ).read_text(encoding="utf-8")

    assert "bazi_engine" not in main_source
    assert "bazi_engine" not in web_source
    assert "bazi_engine" not in bot_source
    calculation_service_source = (
        ROOT / "domains" / "experience-delivery" / "services" / "fatecat-delivery" / "src" / "calculation_service.py"
    ).read_text(encoding="utf-8")
    assert "CapabilityExecutor" in calculation_service_source
    assert "bazi_engine" not in calculation_service_source
    assert "def _build_bot_report_markdown" in bot_source
    assert "_calc_and_save_report" in bot_source
