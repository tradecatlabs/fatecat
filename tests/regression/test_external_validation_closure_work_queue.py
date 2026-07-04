from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT_PATH = ROOT / "scripts" / "external-validation-closure-work-queue.py"
CONTRACT_PATH = ROOT / "contracts" / "fate" / "audit" / "external-validation-closure-work-queue.json"


def _load_module():
    spec = importlib.util.spec_from_file_location("fatecat_external_validation_closure_work_queue", SCRIPT_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _write_json(path: Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def _closure_item(
    *,
    item_id: str,
    owner: str,
    category: str,
    line: int,
    path: str = "docs/release.md",
    status: str = "external_connectivity_pending",
) -> dict:
    return {
        "id": item_id,
        "source": {
            "id": item_id,
            "path": path,
            "line": line,
            "excerpt": "外部连通验证待执行 token:[redacted]",
            "excerptSha256": f"hash-{item_id}",
        },
        "category": category,
        "owner": owner,
        "status": status,
        "credentialDependencies": ["production token"],
        "requiredEvidence": ["redacted live proof JSON"],
        "verificationCommands": ["bash scripts/live-release-gate.sh --require-live"],
        "closureCondition": "真实外部证据通过后关闭。",
        "privacyBoundary": "不得输出真实 token、secret、DSN、私钥、生产日志正文、用户报告正文或外部账号数据。",
    }


def _closure_plan(items: list[dict]) -> dict:
    return {
        "schemaVersion": 1,
        "kind": "fatecat.external_validation_closure_plan",
        "generatedAt": "2026-07-04T00:00:00Z",
        "status": "passed",
        "source": {"pendingExternalJson": "fixture", "itemCount": len(items)},
        "summary": {"total": len(items)},
        "shipGate": {"status": "blocked"},
        "items": items,
        "privacyBoundary": "fixture privacy",
        "nonClaims": ["Does not prove any external live validation has passed."],
    }


def test_external_validation_closure_work_queue_contract_lists_required_fields():
    contract = _load_json(CONTRACT_PATH)

    assert contract["kind"] == "fatecat.external_validation_closure_work_queue_contract"
    assert contract["generator"]["command"] == (
        "bash scripts/external-validation-closure-work-queue.sh --closure-plan-json "
        "<external-validation-closure-gate.json> --output-json <path>"
    )
    assert "assignee" in contract["requiredFieldsPerWorkItem"]
    assert "proofRef" in contract["requiredFieldsPerWorkItem"]
    assert "closeConditionResult" in contract["requiredFieldsPerWorkItem"]
    assert contract["workQueuePolicy"]["proofRefInitialValue"] == ""
    assert "Does not prove any external live validation has passed." in contract["nonClaims"]


def test_external_validation_closure_work_queue_groups_by_owner_and_category(tmp_path):
    module = _load_module()
    closure_plan_json = tmp_path / "closure-plan.json"
    _write_json(
        closure_plan_json,
        _closure_plan(
            [
                _closure_item(
                    item_id="api-1",
                    owner="release-engineering",
                    category="release.production_api_live",
                    line=10,
                ),
                _closure_item(
                    item_id="api-2",
                    owner="release-engineering",
                    category="release.production_api_live",
                    line=11,
                ),
                _closure_item(
                    item_id="policy-1",
                    owner="governance",
                    category="governance.external_validation_policy_guardrail",
                    line=20,
                    path="governance/tasks/example/README.md",
                ),
                _closure_item(
                    item_id="manual-1",
                    owner="engineering-audit",
                    category="manual_triage",
                    line=30,
                    path="docs/manual.md",
                    status="manual_triage_required",
                ),
            ]
        ),
    )

    summary = module.build_summary(closure_plan_json=closure_plan_json)

    assert summary["kind"] == "fatecat.external_validation_closure_work_queue"
    assert summary["status"] == "passed"
    assert summary["shipGate"]["status"] == "blocked"
    assert summary["summary"]["totalOccurrences"] == 4
    assert summary["summary"]["workItems"] == 3
    assert summary["summary"]["byOwner"]["release-engineering"] == 2
    assert summary["summary"]["byStatus"]["pending_external_evidence"] == 1
    assert summary["summary"]["byStatus"]["policy_guardrail_review_required"] == 1
    assert summary["summary"]["byStatus"]["manual_triage_required"] == 1

    api_item = next(item for item in summary["workItems"] if item["category"] == "release.production_api_live")
    assert api_item["assignee"] == "unassigned:release-engineering"
    assert api_item["proofRef"] == ""
    assert api_item["lastCheckedAt"].endswith("Z")
    assert api_item["staleReason"] == "proof_ref_missing"
    assert api_item["closeConditionResult"] == "not_evaluated_no_proof_ref"
    assert len(api_item["occurrences"]) == 2
    assert "excerpt" not in api_item["occurrences"][0]["source"]

    manual_item = next(item for item in summary["workItems"] if item["category"] == "manual_triage")
    assert manual_item["status"] == "manual_triage_required"
    assert manual_item["staleReason"] == "manual_classification_required"


def test_external_validation_closure_work_queue_cli_does_not_copy_pending_excerpt_or_secret_markers(tmp_path):
    closure_plan_json = tmp_path / "closure-plan.json"
    output_json = tmp_path / "work-queue.json"
    _write_json(
        closure_plan_json,
        _closure_plan(
            [
                _closure_item(
                    item_id="sensitive",
                    owner="release-engineering",
                    category="release.production_api_live",
                    line=7,
                )
            ]
        ),
    )

    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT_PATH),
            "--closure-plan-json",
            str(closure_plan_json),
            "--output-json",
            str(output_json),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    summary = _load_json(output_json)
    serialized = json.dumps(summary, ensure_ascii=False).lower()
    assert "token:[redacted]" not in serialized
    assert "token=" not in serialized
    assert "database_url=" not in serialized
    assert summary["summary"]["workItems"] == 1


def test_external_validation_closure_work_queue_rejects_invalid_closure_plan(tmp_path):
    module = _load_module()
    closure_plan_json = tmp_path / "closure-plan.json"
    _write_json(closure_plan_json, {"kind": "wrong", "items": []})

    try:
        module.build_summary(closure_plan_json=closure_plan_json)
    except module.ExternalValidationClosureWorkQueueError as exc:
        assert "kind must be fatecat.external_validation_closure_plan" in str(exc)
    else:
        raise AssertionError("expected invalid closure plan to fail")


def test_external_validation_closure_work_queue_is_wired_to_local_ci_and_docs():
    local_ci = (ROOT / "scripts/local-ci.sh").read_text(encoding="utf-8")
    scripts_agents = (ROOT / "scripts" / "AGENTS.md").read_text(encoding="utf-8")
    audit_agents = (ROOT / "contracts" / "fate" / "audit" / "AGENTS.md").read_text(encoding="utf-8")
    tests_agents = (ROOT / "tests" / "AGENTS.md").read_text(encoding="utf-8")

    assert "external validation closure work queue" in local_ci
    assert "externalValidationClosureWorkQueue" in local_ci
    assert "external-validation-closure-work-queue.sh" in scripts_agents
    assert "external-validation-closure-work-queue.json" in audit_agents
    assert "test_external_validation_closure_work_queue.py" in tests_agents
