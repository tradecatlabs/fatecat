from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT_PATH = ROOT / "scripts" / "external-validation-category-runbooks.py"
CONTRACT_PATH = ROOT / "contracts" / "fate" / "audit" / "external-validation-category-runbooks.json"


def _load_module():
    spec = importlib.util.spec_from_file_location("fatecat_external_validation_category_runbooks", SCRIPT_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _work_item(*, category: str, item_id: str | None = None, owner: str = "release-ops") -> dict:
    item_id = item_id or f"external-work.{category.replace('.', '-')}"
    return {
        "id": item_id,
        "owner": owner,
        "assignee": f"unassigned:{owner}",
        "category": category,
        "priority": "P0",
        "status": "pending_external_evidence",
        "proofRef": "",
        "lastCheckedAt": "2026-07-04T00:00:00Z",
        "staleReason": "proof_ref_missing",
        "closeConditionResult": "not_evaluated_no_proof_ref",
        "credentialDependencies": ["category operator credential"],
        "requiredEvidence": ["redacted category live proof JSON"],
        "verificationCommands": ["bash scripts/external-validation-proof-ref-gate.sh --work-queue-json <path>"],
        "closureCondition": "真实外部证据通过后关闭。",
        "occurrences": [
            {
                "id": f"external.{category.replace('.', '-')}",
                "source": {
                    "path": "docs/release.md",
                    "line": 1,
                    "excerptSha256": "1" * 64,
                },
                "status": "external_connectivity_pending",
            }
        ],
    }


def _work_queue(items: list[dict]) -> dict:
    return {
        "schemaVersion": 1,
        "kind": "fatecat.external_validation_closure_work_queue",
        "generatedAt": "2026-07-04T00:00:00Z",
        "status": "passed",
        "source": {
            "closurePlanJson": "fixture",
            "closurePlanSha256": "0" * 64,
            "closurePlanKind": "fatecat.external_validation_closure_plan",
            "closureItemCount": len(items),
        },
        "summary": {
            "totalOccurrences": len(items),
            "workItems": len(items),
        },
        "shipGate": {
            "status": "blocked",
        },
        "workItems": items,
        "privacyBoundary": "redacted_no_secret_values",
        "nonClaims": ["Does not prove any external live validation has passed."],
    }


def test_external_validation_category_runbooks_contract_lists_required_fields():
    module = _load_module()
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))

    assert contract["kind"] == "fatecat.external_validation_category_runbooks_contract"
    assert contract["generator"]["command"] == (
        "bash scripts/external-validation-category-runbooks.sh --work-queue-json "
        "<external-validation-closure-work-queue.json> --output-json <path>"
    )
    assert "proofRefArtifactPattern" in contract["requiredFieldsPerRunbook"]
    assert "failureRollback" in contract["requiredFieldsPerRunbook"]
    assert set(contract["knownCategories"]) == set(module.CATEGORY_PROFILES)
    assert "Does not prove any external live validation has passed." in contract["nonClaims"]


def test_external_validation_category_runbooks_builds_per_category_runbook(tmp_path):
    module = _load_module()
    work_queue_json = tmp_path / "work-queue.json"
    _write_json(
        work_queue_json,
        _work_queue(
            [
                _work_item(category="release.production_api_live", item_id="api-1", owner="release-ops"),
                _work_item(category="release.production_api_live", item_id="api-2", owner="release-ops"),
                _work_item(category="security.identity_oidc", owner="security-ops"),
                _work_item(category="manual_triage", owner="engineering-audit"),
            ]
        ),
    )

    summary = module.build_summary(work_queue_json=work_queue_json)
    serialized = json.dumps(summary, ensure_ascii=False, sort_keys=True)

    assert summary["kind"] == "fatecat.external_validation_category_runbooks"
    assert summary["status"] == "passed"
    assert summary["runbookStatus"] == "operator_runbooks_ready"
    assert summary["shipGate"]["status"] == "blocked"
    assert summary["shipGate"]["blockingItems"] == ["category_live_execution_pending", "proof_ref_evidence_pending"]
    assert summary["summary"]["categories"] == 3
    assert summary["summary"]["runbooks"] == 3

    api_runbook = next(item for item in summary["runbooks"] if item["category"] == "release.production_api_live")
    assert api_runbook["owners"] == ["release-ops"]
    assert api_runbook["evidenceType"] == "production_api_live_smoke"
    assert api_runbook["occurrenceCount"] == 2
    assert api_runbook["proofRefArtifactPattern"].startswith(
        "evidence://external-validation/release-production-api-live/"
    )
    assert api_runbook["failureRollback"]
    assert api_runbook["closureCondition"]
    assert any("production-readiness.sh" in command for command in api_runbook["operatorCommands"])
    assert any("external-validation-proof-ref-gate.sh" in command for command in api_runbook["operatorCommands"])

    manual_runbook = next(item for item in summary["runbooks"] if item["category"] == "manual_triage")
    assert manual_runbook["priority"] == "P1"
    assert manual_runbook["status"] == "manual_triage_required"
    assert "https://" not in serialized
    assert "token=" not in serialized
    assert "secret=" not in serialized


def test_external_validation_category_runbooks_covers_all_known_categories(tmp_path):
    module = _load_module()
    work_queue_json = tmp_path / "all-categories-work-queue.json"
    items = [
        _work_item(category=category, owner=f"owner-{index:02d}")
        for index, category in enumerate(sorted(module.CATEGORY_PROFILES), start=1)
    ]
    _write_json(work_queue_json, _work_queue(items))

    summary = module.build_summary(work_queue_json=work_queue_json)

    assert summary["summary"]["knownCategoryProfiles"] == len(module.CATEGORY_PROFILES)
    assert summary["summary"]["categories"] == len(module.CATEGORY_PROFILES)
    assert {item["category"] for item in summary["runbooks"]} == set(module.CATEGORY_PROFILES)


def test_external_validation_category_runbooks_rejects_unknown_category(tmp_path):
    module = _load_module()
    work_queue_json = tmp_path / "work-queue.json"
    _write_json(work_queue_json, _work_queue([_work_item(category="unknown.live")]))

    with pytest.raises(module.ExternalValidationCategoryRunbooksError, match="runbook profile missing"):
        module.build_summary(work_queue_json=work_queue_json)


def test_external_validation_category_runbooks_cli_writes_blocked_summary(tmp_path):
    work_queue_json = tmp_path / "work-queue.json"
    output_json = tmp_path / "runbooks.json"
    _write_json(work_queue_json, _work_queue([_work_item(category="release.telegram_bot_live")]))

    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT_PATH),
            "--work-queue-json",
            str(work_queue_json),
            "--output-json",
            str(output_json),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    summary = json.loads(output_json.read_text(encoding="utf-8"))
    assert summary["runbookStatus"] == "operator_runbooks_ready"
    assert summary["shipGate"]["status"] == "blocked"
    assert summary["summary"]["runbooks"] == 1


def test_external_validation_category_runbooks_wiring_is_registered():
    local_ci = (ROOT / "scripts" / "local-ci.sh").read_text(encoding="utf-8")
    scripts_agents = (ROOT / "scripts" / "AGENTS.md").read_text(encoding="utf-8")
    audit_agents = (ROOT / "contracts" / "fate" / "audit" / "AGENTS.md").read_text(encoding="utf-8")
    tests_agents = (ROOT / "tests" / "AGENTS.md").read_text(encoding="utf-8")
    certification_contract = (
        ROOT / "contracts" / "fate" / "audit" / "measurement-infrastructure-certification.json"
    ).read_text(encoding="utf-8")

    assert "external validation category runbooks" in local_ci
    assert "externalValidationCategoryRunbooks" in local_ci
    assert "external-validation-category-runbooks.py" in scripts_agents
    assert "external-validation-category-runbooks.json" in audit_agents
    assert "test_external_validation_category_runbooks.py" in tests_agents
    assert "external-validation-category-runbooks.json" in certification_contract
