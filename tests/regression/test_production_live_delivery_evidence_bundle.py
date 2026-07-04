from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT_PATH = ROOT / "scripts" / "production-live-delivery-evidence-bundle.py"
CONTRACT_PATH = ROOT / "contracts" / "fate" / "audit" / "production-live-delivery-evidence-bundle.json"
LIVE_PROOF_GATE_PATH = ROOT / "scripts" / "external-validation-live-proof-gate.py"

CATEGORIES = (
    ("release.production_api_live", "release-ops", "production_api_live_smoke"),
    ("release.hf_space_live", "release-ops", "hf_space_live_smoke"),
    ("release.telegram_bot_live", "bot-ops", "telegram_bot_live_smoke"),
    ("runtime.public_webhook_live", "runtime-ops", "public_webhook_live"),
    ("delivery.multi_surface_live", "delivery-ops", "multi_surface_live_parity"),
)


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


def _sha256(path: Path) -> str:
    import hashlib

    return hashlib.sha256(path.read_bytes()).hexdigest()


def _work_items() -> list[dict]:
    items: list[dict] = []
    for index, (category, owner, _) in enumerate(CATEGORIES, start=1):
        item_id = f"external-work.{category.replace('.', '-')}"
        items.append(
            {
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
                "credentialDependencies": ["redacted operator credential"],
                "requiredEvidence": ["redacted live proof JSON"],
                "verificationCommands": ["bash scripts/live-release-gate.sh --output-json <path>"],
                "closureCondition": "真实外部证据通过后关闭。",
                "occurrences": [
                    {
                        "id": f"external.delivery.{index}",
                        "source": {
                            "path": "docs/release.md",
                            "line": index,
                            "excerptSha256": str(index) * 64,
                        },
                        "status": "external_connectivity_pending",
                    }
                ],
            }
        )
    return items


def _work_queue() -> dict:
    items = _work_items()
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
        "summary": {"totalOccurrences": len(items), "workItems": len(items)},
        "shipGate": {"status": "blocked"},
        "workItems": items,
        "privacyBoundary": "redacted_no_secret_values",
        "nonClaims": ["Does not prove any external live validation has passed."],
    }


def _proof_ref_gate() -> dict:
    refs = []
    for item in _work_items():
        refs.append(
            {
                "id": f"proof.{item['category'].replace('.', '-')}",
                "proofRef": f"evidence://external-validation/{item['category'].replace('.', '-')}/run",
                "evidenceType": "redacted_live_smoke",
                "workItemId": item["id"],
                "owner": item["owner"],
                "category": item["category"],
                "issuer": f"operator:{item['owner']}",
                "capturedAt": "2026-07-04T00:00:00Z",
                "expiresAt": "2099-01-01T00:00:00Z",
                "artifactHash": f"sha256:{'b' * 64}",
                "verificationCommandSha256": "c" * 64,
                "occurrenceIds": [item["occurrences"][0]["id"]],
            }
        )
    return {
        "schemaVersion": 1,
        "kind": "fatecat.external_validation_proof_ref_gate_summary",
        "generatedAt": "2026-07-04T00:00:00Z",
        "status": "passed",
        "source": {
            "workQueueJson": "fixture",
            "workQueueSha256": "0" * 64,
            "workQueueKind": "fatecat.external_validation_closure_work_queue",
            "expectedCommit": "a" * 40,
        },
        "summary": {
            "workItems": len(refs),
            "acceptedProofRefs": len(refs),
            "acceptedWorkItems": len(refs),
            "pendingWorkItems": 0,
            "proofRefStatus": "schema_accepted_all_work_items",
        },
        "proofRefStatus": "schema_accepted_all_work_items",
        "proofRefGate": {"status": "schema_accepted_all_work_items"},
        "shipGate": {"status": "blocked"},
        "acceptedProofRefs": refs,
        "pendingWorkItems": [],
        "negativeEvidenceRejected": [],
        "privacyBoundary": "redacted_no_secret_values",
        "nonClaims": ["Does not prove any external live validation has passed."],
    }


def _runbooks() -> dict:
    return {
        "schemaVersion": 1,
        "kind": "fatecat.external_validation_category_runbooks",
        "generatedAt": "2026-07-04T00:00:00Z",
        "status": "passed",
        "summary": {"categories": len(CATEGORIES), "runbooks": len(CATEGORIES)},
        "runbookStatus": "operator_runbooks_ready",
        "runbookGate": {"status": "passed"},
        "shipGate": {"status": "blocked"},
        "runbooks": [
            {
                "id": f"external-runbook.{category}",
                "category": category,
                "owners": [owner],
                "priority": "P0",
                "status": "operator_action_required",
                "evidenceType": live_gate_kind,
                "requiredCredentials": ["redacted credential"],
                "operatorCommands": ["bash scripts/live-release-gate.sh --output-json <path>"],
                "proofRefArtifactPattern": f"evidence://external-validation/{category}/<run-id>",
                "redactionRule": "redact secrets",
                "expiryPolicy": "14 days",
                "failureRollback": "keep blocked",
                "closureCondition": "真实外部证据通过后关闭。",
                "verifierCommand": "bash scripts/external-validation-live-proof-gate.sh --work-queue-json <path>",
                "sourceWorkItemIds": [f"external-work.{category.replace('.', '-')}"],
                "occurrenceCount": 1,
                "nonClaims": ["Runbook readiness does not prove live evidence has passed."],
            }
            for category, owner, live_gate_kind in CATEGORIES
        ],
        "privacyBoundary": "redacted_no_secret_values",
        "nonClaims": ["Does not prove any external live validation has passed."],
    }


def _live_release_gate() -> dict:
    return {
        "schemaVersion": 1,
        "generatedAt": "2026-07-04T00:00:00Z",
        "status": "passed",
        "mode": "live-required",
        "git": {"commit": "a" * 40, "clean": True},
        "summary": {"requiredBlocking": []},
        "shipGate": {"status": "pass", "blockingItems": []},
        "checks": [
            {
                "id": "evidence.production_api_live",
                "name": "Production API live",
                "category": "external_live",
                "status": "pass",
                "requiredForLiveRelease": True,
                "evidence": "https://api.example.invalid",
                "externalConnectivity": "required",
                "detail": "status=200",
            },
            {
                "id": "evidence.hf_space_live",
                "name": "HF Space live",
                "category": "external_live",
                "status": "pass",
                "requiredForLiveRelease": True,
                "evidence": "https://fatecat.example.hf.space/web",
                "externalConnectivity": "required",
                "detail": "status=200",
            },
            {
                "id": "evidence.telegram_bot_live",
                "name": "Telegram Bot live",
                "category": "external_live",
                "status": "pass",
                "requiredForLiveRelease": True,
                "evidence": "scripts/live-bot-smoke.sh",
                "externalConnectivity": "required",
                "detail": "live bot smoke ok: id=123 username=@redacted",
            },
        ],
        "privacyBoundary": "input may contain URLs; assembler output must not copy them",
    }


def _public_webhook() -> dict:
    return {
        "schemaVersion": 1,
        "kind": "fatecat.postgres_public_webhook_live_smoke",
        "generatedAt": "2026-07-04T00:00:00Z",
        "status": "passed",
        "liveEvidence": {
            "jobStatus": "succeeded",
            "outboxStatus": "succeeded",
            "publicWebhookLiveDelivery": True,
        },
        "shipGate": {"status": "blocked"},
        "privacyBoundary": "redacted",
        "nonClaims": ["does_not_prove_production_ready"],
    }


def _multi_surface() -> dict:
    return {
        "schemaVersion": 1,
        "kind": "fatecat.multi_surface_semantic_diff",
        "status": "passed",
        "generatedAt": "2026-07-04T00:00:00Z",
        "comparisons": [{"reportSystem": "bazi", "status": "passed"}],
        "privacyBoundary": "hash only",
    }


def _write_inputs(tmp_path: Path) -> tuple[Path, Path, Path]:
    work_queue_json = tmp_path / "work-queue.json"
    proof_ref_gate_json = tmp_path / "proof-ref-gate.json"
    category_runbooks_json = tmp_path / "category-runbooks.json"
    _write_json(work_queue_json, _work_queue())
    _write_json(proof_ref_gate_json, _proof_ref_gate())
    _write_json(category_runbooks_json, _runbooks())
    return work_queue_json, proof_ref_gate_json, category_runbooks_json


def test_production_live_delivery_contract_lists_supported_categories():
    module = _load_module(SCRIPT_PATH, "fatecat_production_live_delivery_evidence_bundle")
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))

    assert contract["kind"] == "fatecat.production_live_delivery_evidence_bundle_contract"
    assert contract["outputKind"] == "fatecat.external_validation_live_evidence_bundle"
    assert set(contract["supportedCategories"]) == set(module.CATEGORY_RULES)
    assert "Does not execute production API/HF/Bot/Postgres/webhook checks." in contract["nonClaims"]


def test_production_live_delivery_bundle_pending_without_live_summaries(tmp_path):
    module = _load_module(SCRIPT_PATH, "fatecat_production_live_delivery_evidence_bundle_pending")
    work_queue_json, proof_ref_gate_json, category_runbooks_json = _write_inputs(tmp_path)

    bundle = module.build_bundle(
        work_queue_json=work_queue_json,
        proof_ref_gate_json=proof_ref_gate_json,
        category_runbooks_json=category_runbooks_json,
        expected_commit="a" * 40,
    )

    assert bundle["kind"] == "fatecat.external_validation_live_evidence_bundle"
    assert bundle["status"] == "external_connectivity_pending"
    assert bundle["liveProofs"] == []
    assert "https://" not in json.dumps(bundle, ensure_ascii=False)


def test_production_live_delivery_bundle_accepts_redacted_live_summaries_and_chains_gate(tmp_path):
    module = _load_module(SCRIPT_PATH, "fatecat_production_live_delivery_evidence_bundle_live")
    live_gate = _load_module(LIVE_PROOF_GATE_PATH, "fatecat_external_validation_live_proof_gate_for_bundle")
    work_queue_json, proof_ref_gate_json, category_runbooks_json = _write_inputs(tmp_path)
    live_release_gate_json = tmp_path / "live-release-gate.json"
    public_hook_json = tmp_path / "public-webhook.json"
    multi_surface_json = tmp_path / "multi-surface.json"
    bundle_json = tmp_path / "production-live-delivery-evidence-bundle.json"
    _write_json(live_release_gate_json, _live_release_gate())
    _write_json(public_hook_json, _public_webhook())
    _write_json(multi_surface_json, _multi_surface())

    bundle = module.build_bundle(
        work_queue_json=work_queue_json,
        proof_ref_gate_json=proof_ref_gate_json,
        category_runbooks_json=category_runbooks_json,
        live_release_gate_json=live_release_gate_json,
        public_hook_json=public_hook_json,
        multi_surface_json=multi_surface_json,
        expected_commit="a" * 40,
    )
    _write_json(bundle_json, bundle)
    serialized = json.dumps(bundle, ensure_ascii=False, sort_keys=True)

    assert bundle["status"] == "external_live_evidence_supplied_by_operator"
    assert len(bundle["liveProofs"]) == len(CATEGORIES)
    assert {item["category"] for item in bundle["liveProofs"]} == {category for category, _, _ in CATEGORIES}
    assert "https://api.example.invalid" not in serialized
    assert "https://fatecat.example.hf.space" not in serialized
    assert "token=" not in serialized

    live_proof_summary = live_gate.build_summary(
        work_queue_json=work_queue_json,
        proof_ref_gate_json=proof_ref_gate_json,
        category_runbooks_json=category_runbooks_json,
        live_evidence_json=bundle_json,
        expected_commit="a" * 40,
    )
    assert live_proof_summary["liveProofStatus"] == "live_gate_accepted_all_work_items"
    assert live_proof_summary["summary"]["acceptedLiveProofs"] == len(CATEGORIES)
    assert live_proof_summary["shipGate"]["status"] == "blocked"


def test_production_live_delivery_bundle_rejects_sensitive_summary_input(tmp_path):
    module = _load_module(SCRIPT_PATH, "fatecat_production_live_delivery_evidence_bundle_sensitive")
    work_queue_json, proof_ref_gate_json, category_runbooks_json = _write_inputs(tmp_path)
    live_release_gate_json = tmp_path / "live-release-gate.json"
    payload = _live_release_gate()
    payload["checks"][0]["detail"] = "token=should-not-appear"
    _write_json(live_release_gate_json, payload)

    with pytest.raises(module.ProductionLiveDeliveryEvidenceBundleError, match="sensitive-looking"):
        module.build_bundle(
            work_queue_json=work_queue_json,
            proof_ref_gate_json=proof_ref_gate_json,
            category_runbooks_json=category_runbooks_json,
            live_release_gate_json=live_release_gate_json,
            expected_commit="a" * 40,
        )


def test_production_live_delivery_bundle_cli_writes_pending_bundle(tmp_path):
    work_queue_json, proof_ref_gate_json, category_runbooks_json = _write_inputs(tmp_path)
    output_json = tmp_path / "bundle.json"

    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT_PATH),
            "--work-queue-json",
            str(work_queue_json),
            "--proof-ref-gate-json",
            str(proof_ref_gate_json),
            "--category-runbooks-json",
            str(category_runbooks_json),
            "--expected-commit",
            "a" * 40,
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
    assert summary["status"] == "external_connectivity_pending"
    assert summary["source"]["workQueueSha256"] == _sha256(work_queue_json)


def test_production_live_delivery_bundle_wiring_is_registered():
    local_ci = (ROOT / "scripts" / "local-ci.sh").read_text(encoding="utf-8")
    scripts_agents = (ROOT / "scripts" / "AGENTS.md").read_text(encoding="utf-8")
    audit_agents = (ROOT / "contracts" / "fate" / "audit" / "AGENTS.md").read_text(encoding="utf-8")
    tests_agents = (ROOT / "tests" / "AGENTS.md").read_text(encoding="utf-8")

    assert "production live delivery evidence bundle" in local_ci
    assert "productionLiveDeliveryEvidenceBundle" in local_ci
    assert "production-live-delivery-evidence-bundle.py" in scripts_agents
    assert "production-live-delivery-evidence-bundle.json" in audit_agents
    assert "test_production_live_delivery_evidence_bundle.py" in tests_agents
