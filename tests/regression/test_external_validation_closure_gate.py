from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT_PATH = ROOT / "scripts" / "external-validation-closure-gate.py"
CONTRACT_PATH = ROOT / "contracts" / "fate" / "audit" / "external-validation-closure.json"
PENDING_PHRASE = "外部连通验证待执行"


def _load_module():
    spec = importlib.util.spec_from_file_location("fatecat_external_validation_closure_gate", SCRIPT_PATH)
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


def test_external_validation_closure_contract_lists_required_closure_fields():
    contract = _load_json(CONTRACT_PATH)

    assert contract["kind"] == "fatecat.external_validation_closure_contract"
    assert contract["generator"]["command"] == (
        "bash scripts/external-validation-closure-gate.sh --pending-external-json "
        "<pending-external-validations.json> --output-json <path>"
    )
    assert "owner" in contract["requiredFieldsPerClosureItem"]
    assert "credentialDependencies" in contract["requiredFieldsPerClosureItem"]
    assert "closureCondition" in contract["requiredFieldsPerClosureItem"]
    assert "Does not prove any external live validation has passed." in contract["nonClaims"]


def test_external_validation_closure_gate_groups_pending_items_into_actionable_plan(tmp_path):
    module = _load_module()
    pending_json = tmp_path / "pending-external-validations.json"
    _write_json(
        pending_json,
        [
            {
                "id": "p1",
                "path": "docs/release.md",
                "line": 10,
                "phrase": PENDING_PHRASE,
                "excerpt": "production API CORS 外部连通验证待执行",
            },
            {
                "id": "p2",
                "path": "docs/bot.md",
                "line": 20,
                "phrase": PENDING_PHRASE,
                "excerpt": "Telegram Bot live 外部连通验证待执行",
            },
            {
                "id": "p3",
                "path": "docs/manual.md",
                "line": 30,
                "phrase": PENDING_PHRASE,
                "excerpt": "某个未归类外部连通验证待执行",
            },
            {
                "id": "p4",
                "path": "governance/tasks/example/RESEARCH.md",
                "line": 40,
                "phrase": PENDING_PHRASE,
                "excerpt": "所有外部依赖都有真实证据或明确标记外部连通验证待执行",
            },
            {
                "id": "p5",
                "path": "contracts/fate/evaluations/registry.json",
                "line": 50,
                "phrase": PENDING_PHRASE,
                "excerpt": '"external_eval 必须标记 externalConnectivity=外部连通验证待执行"',
            },
            {
                "id": "p6",
                "path": "governance/tasks/provider/ACCEPTANCE.md",
                "line": 60,
                "phrase": PENDING_PHRASE,
                "excerpt": "生产 provider 远端依赖 外部连通验证待执行",
            },
            {
                "id": "p7",
                "path": "contracts/fate/delivery/events.json",
                "line": 70,
                "phrase": PENDING_PHRASE,
                "excerpt": '"liveEvidence": "外部连通验证待执行"',
            },
            {
                "id": "p8",
                "path": "governance/tasks/runtime/ACCEPTANCE.md",
                "line": 80,
                "phrase": PENDING_PHRASE,
                "excerpt": "multi-replica runtime gate outputs 外部连通验证待执行",
            },
        ],
    )

    summary = module.build_summary(pending_external_json=pending_json)

    assert summary["status"] == "passed"
    assert summary["kind"] == "fatecat.external_validation_closure_plan"
    assert summary["shipGate"]["status"] == "blocked"
    assert summary["summary"]["total"] == 8
    assert summary["summary"]["manualTriage"] == 1
    assert summary["summary"]["categories"]["release.production_api_live"] == 1
    assert summary["summary"]["categories"]["release.telegram_bot_live"] == 1
    assert summary["summary"]["categories"]["governance.external_validation_policy_guardrail"] == 1
    assert summary["summary"]["categories"]["quality.external_evaluation_live"] == 1
    assert summary["summary"]["categories"]["provider.external_dependency_live"] == 1
    assert summary["summary"]["categories"]["event_platform.live"] == 1
    assert summary["summary"]["categories"]["runtime.multi_replica_live"] == 1
    assert summary["summary"]["categories"]["manual_triage"] == 1
    assert all(item["owner"] for item in summary["items"])
    assert all(item["credentialDependencies"] for item in summary["items"])
    assert all(item["requiredEvidence"] for item in summary["items"])
    assert all(item["verificationCommands"] for item in summary["items"])
    assert all(item["closureCondition"] for item in summary["items"])


def test_external_validation_closure_cli_writes_redacted_summary(tmp_path):
    pending_json = tmp_path / "pending-external-validations.json"
    output_json = tmp_path / "closure.json"
    sensitive_excerpt = (
        PENDING_PHRASE + " " + "token" + "=should-not-leak " + "DATABASE_URL" + "=postgres://should-not-leak"
    )
    _write_json(
        pending_json,
        [
            {
                "id": "sensitive",
                "path": "docs/security.md",
                "line": 7,
                "phrase": PENDING_PHRASE,
                "excerpt": sensitive_excerpt,
            }
        ],
    )

    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT_PATH),
            "--pending-external-json",
            str(pending_json),
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
    assert "token" + "=should-not-leak" not in serialized
    assert "database_url" + "=postgres://should-not-leak" not in serialized
    assert "token:[redacted]" in serialized
    assert "database_url:[redacted]" in serialized
    assert summary["summary"]["total"] == 1
    assert summary["items"][0]["source"]["excerptSha256"]


def test_external_validation_closure_gate_rejects_invalid_pending_json(tmp_path):
    module = _load_module()
    pending_json = tmp_path / "pending-external-validations.json"
    _write_json(pending_json, {"not": "an array"})

    try:
        module.build_summary(pending_external_json=pending_json)
    except module.ExternalValidationClosureError as exc:
        assert "root must be an array" in str(exc)
    else:
        raise AssertionError("expected invalid pending JSON to fail")


def test_external_validation_closure_gate_is_wired_to_local_ci_and_docs():
    local_ci = (ROOT / "scripts/local-ci.sh").read_text(encoding="utf-8")
    scripts_agents = (ROOT / "scripts" / "AGENTS.md").read_text(encoding="utf-8")
    audit_agents = (ROOT / "contracts" / "fate" / "audit" / "AGENTS.md").read_text(encoding="utf-8")
    tests_agents = (ROOT / "tests" / "AGENTS.md").read_text(encoding="utf-8")

    assert "external validation closure gate" in local_ci
    assert "externalValidationClosureGate" in local_ci
    assert "external-validation-closure-gate.sh" in scripts_agents
    assert "external-validation-closure.json" in audit_agents
    assert "test_external_validation_closure_gate.py" in tests_agents
