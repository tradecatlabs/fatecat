from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT_PATH = ROOT / "scripts" / "measurement-infrastructure-certification.py"
CONTRACT_PATH = ROOT / "contracts" / "fate" / "audit" / "measurement-infrastructure-certification.json"


def _load_module():
    spec = importlib.util.spec_from_file_location("fatecat_measurement_infrastructure_certification", SCRIPT_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _write_evidence_dir(root: Path, *, blocked: bool) -> Path:
    passed = {"status": "passed"}
    for rel_path in [
        "provider-drift-trend-gate.json",
        "core-quality-corpus-gate.json",
        "mingli-bench-gate.json",
        "data-supply-chain-gate.json",
        "event-contract-gate.json",
        "production-security-gate.json",
        "observability-slo-gate.json",
        "observability-trace-slo-smoke.json",
        "otel-collector-slo-gate.json",
        "runtime-backend-gate.json",
    ]:
        _write_json(root / rel_path, passed)

    _write_json(
        root / "developer-platform-gate.json",
        {"status": "passed", "publishedSdkPackages": 1 if not blocked else 0, "liveSandboxTokenService": not blocked},
    )
    _write_json(
        root / "developer-portal-gate.json",
        {"status": "passed", "externalPortalLive": not blocked, "liveSandboxTokenService": not blocked},
    )
    _write_json(
        root / "sandbox-access-gateway-gate.json",
        {"status": "passed", "livePublicTokenService": not blocked},
    )
    _write_json(
        root / "security-externalization-gate.json",
        {"status": "passed", "liveEvidenceStatus": "外部连通验证待执行" if blocked else "passed"},
    )
    _write_json(
        root / "retention-production-cleanup-gate.json",
        {
            "status": "passed",
            "liveEvidenceStatus": "外部连通验证待执行" if blocked else "passed",
            "shipGate": "blocked" if blocked else "passed",
        },
    )
    _write_json(
        root / "external-secret-provider-gate.json",
        {"status": "passed", "liveEvidenceStatus": "外部连通验证待执行" if blocked else "passed"},
    )
    _write_json(
        root / "otel-backend-slo-gate.json",
        {"status": "passed", "liveEvidenceStatus": "外部连通验证待执行" if blocked else "passed"},
    )
    _write_json(
        root / "multi-replica-runtime-gate.json",
        {"status": "passed", "liveEvidenceStatus": "外部连通验证待执行" if blocked else "passed"},
    )
    _write_json(
        root / "runtime-proof-gate.json",
        {
            "status": "passed",
            "runtimeProofStatus": "external_connectivity_pending" if blocked else "external_live_passed",
            "shipGate": {
                "status": "blocked" if blocked else "passed",
                "blockingItems": ["public_webhook_live"] if blocked else [],
            },
        },
    )
    _write_json(
        root / "live-release-gate.json",
        {
            "status": "passed",
            "shipGate": {
                "status": "blocked" if blocked else "passed",
                "blockingItems": ["evidence.telegram_bot_live"] if blocked else [],
            },
        },
    )
    _write_json(
        root / "current-release-proof.json",
        {
            "status": "passed",
            "proofGate": {
                "status": "fail" if blocked else "passed",
                "blockingItems": ["release.git_clean"] if blocked else [],
            },
        },
    )
    _write_json(
        root / "current-audit-bundle" / "current-audit-bundle.json",
        {
            "status": "passed",
            "auditGate": {
                "status": "blocked" if blocked else "passed",
                "blockingItems": ["git.clean"] if blocked else [],
            },
            "pendingExternalValidationCount": 3 if blocked else 0,
        },
    )
    return root


def test_certification_contract_lists_required_evidence_files():
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))

    assert contract["kind"] == "fatecat.measurement_infrastructure_certification_contract"
    assert "provider-drift-trend-gate.json" in contract["requiredEvidenceFiles"]
    assert "runtime-proof-gate.json" in contract["requiredEvidenceFiles"]
    assert "current-audit-bundle/current-audit-bundle.json" in contract["requiredEvidenceFiles"]
    assert "Does not mean FateCat is 100% production infrastructure." in contract["nonClaims"]


def test_certification_aggregator_outputs_blocked_dry_run(tmp_path):
    module = _load_module()
    evidence_dir = _write_evidence_dir(tmp_path / "evidence", blocked=True)

    summary = module.run_gate(evidence_dir=evidence_dir)

    assert summary["status"] == "blocked"
    assert summary["certificationGate"]["canClaim100Percent"] is False
    assert {domain["id"]: domain["status"] for domain in summary["domains"]}["release"] == "blocked"
    assert {domain["id"]: domain["status"] for domain in summary["domains"]}["audit"] == "blocked"
    assert {domain["id"]: domain["status"] for domain in summary["domains"]}["security_privacy"] == "blocked"
    assert summary["externalPending"]


def test_certification_require_certified_rejects_blocked(tmp_path):
    module = _load_module()
    evidence_dir = _write_evidence_dir(tmp_path / "evidence", blocked=True)

    exit_code = module.main(
        ["--evidence-dir", str(evidence_dir), "--output-json", str(tmp_path / "out.json"), "--require-certified"]
    )

    assert exit_code == 1


def test_certification_rejects_missing_required_evidence(tmp_path):
    module = _load_module()
    evidence_dir = _write_evidence_dir(tmp_path / "evidence", blocked=False)
    (evidence_dir / "provider-drift-trend-gate.json").unlink()

    summary = module.run_gate(evidence_dir=evidence_dir)

    assert summary["status"] == "failed"
    assert "provider" in summary["certificationGate"]["failedDomains"]


def test_certification_accepts_synthetic_full_pass(tmp_path):
    module = _load_module()
    evidence_dir = _write_evidence_dir(tmp_path / "evidence", blocked=False)
    output_json = tmp_path / "certification.json"

    exit_code = module.main(
        ["--evidence-dir", str(evidence_dir), "--output-json", str(output_json), "--require-certified"]
    )

    assert exit_code == 0
    stored = json.loads(output_json.read_text(encoding="utf-8"))
    assert stored["status"] == "passed"
    assert stored["certificationGate"]["canClaim100Percent"] is True
