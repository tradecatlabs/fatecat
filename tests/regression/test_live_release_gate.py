from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def _git_head() -> str:
    result = subprocess.run(
        ["git", "rev-parse", "--verify", "HEAD"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    return result.stdout.strip()


def _write_local_ci_summary(
    path: Path,
    *,
    profile: str = "quick",
    status: str = "passed",
    commit: str | None = None,
) -> None:
    payload = {
        "schemaVersion": 1,
        "kind": "fatecat.local_ci_summary",
        "profile": profile,
        "status": status,
        "exitCode": 0 if status == "passed" else 1,
        "startedAt": "2026-07-02T00:00:00+00:00",
        "finishedAt": "2026-07-02T00:01:00+00:00",
        "runtimeRoot": str(ROOT),
        "commit": commit or _git_head(),
        "git": {"branch": "main", "dirtyCount": 0, "untrackedCount": 0},
        "artifacts": {
            "releaseArtifacts": str(path.parent / "release-artifacts"),
            "liveReleaseGate": str(path.parent / "live-release-gate.json"),
        },
    }
    path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")


def test_live_release_gate_contract_declares_required_release_evidence():
    schema = _load_json(ROOT / "contracts/fate/delivery/schemas/release-gate.schema.json")
    gate = _load_json(ROOT / "contracts/fate/delivery/release-gate.json")
    registry = _load_json(ROOT / "contracts/fate/delivery/registry.json")
    resource_schema = _load_json(ROOT / "contracts/fate/capabilities/schemas/resource.schema.json")

    assert "ReleaseGate" in resource_schema["resourceTypes"]
    assert "releaseGateResourceFields" in resource_schema
    assert registry["schemas"]["releaseGate"] == "contracts/fate/delivery/schemas/release-gate.schema.json"
    assert registry["releaseGate"]["contract"] == "contracts/fate/delivery/release-gate.json"
    assert gate["resourceType"] == "ReleaseGate"
    assert gate["id"] == "gate.live_release"
    assert gate["shipGate"]["status"] == "blocked"
    assert "bash scripts/local-ci.sh --profile quick --output <dir>" in gate["localVerification"]
    assert (
        "bash scripts/live-release-gate.sh --local-ci-summary <dir>/summary.json --output-json <path>"
        in gate["localVerification"]
    )
    assert "bash scripts/release-artifacts.sh --output-dir <dir>" in gate["localVerification"]
    assert "bash scripts/rollback-drill.sh --output-json <path>" in gate["localVerification"]
    assert "bash scripts/container-release-evidence.sh --output-json <path>" in gate["localVerification"]
    assert (
        "bash scripts/live-release-gate.sh --local-ci-summary <dir>/summary.json --output-json <path>"
        in registry["releaseGate"]["localVerification"]
    )
    assert "bash scripts/rollback-drill.sh --output-json <path>" in registry["releaseGate"]["localVerification"]
    assert (
        "bash scripts/container-release-evidence.sh --output-json <path>"
        in registry["releaseGate"]["localVerification"]
    )

    required_fields = set(schema["requiredEvidenceFields"])
    evidence = {item["id"]: item for item in gate["requiredEvidence"]}
    assert required_fields <= set(next(iter(evidence.values())))
    assert set(evidence) == {
        "evidence.local_ci_quick",
        "evidence.remote_ci_current_commit",
        "evidence.production_api_live",
        "evidence.hf_space_live",
        "evidence.telegram_bot_live",
        "evidence.container_digest",
        "evidence.sbom_artifact",
        "evidence.provenance_artifact",
        "evidence.rollback_drill",
        "evidence.clean_git_state",
    }
    assert all(item["requiredForLiveRelease"] is True for item in evidence.values())
    assert "真实外部证据是否齐全" in schema["invariants"][1]


def test_public_release_gate_passes_local_ci_summary_to_live_gate():
    script = (ROOT / "scripts/public-release-gate.sh").read_text(encoding="utf-8")

    assert 'local_ci_summary="${output_dir}/local-ci-quick/summary.json"' in script
    assert 'release_gate_args+=(--local-ci-summary "${local_ci_summary}")' in script


def test_live_release_gate_local_mode_outputs_blocked_ship_gate(tmp_path):
    output_json = tmp_path / "live-release-gate.json"
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/live-release-gate.py"),
            "--output-json",
            str(output_json),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    summary = json.loads(result.stdout)
    assert summary["status"] == "passed"
    assert summary["mode"] == "local-contract"
    assert summary["shipGate"] in {"blocked", "fail"}
    assert output_json.is_file()

    payload = _load_json(output_json)
    checks = {item["id"]: item for item in payload["checks"]}
    assert payload["status"] == "passed"
    assert payload["shipGate"]["status"] in {"blocked", "fail"}
    assert checks["evidence.production_api_live"]["status"] == "pending"
    assert checks["evidence.hf_space_live"]["status"] == "pending"
    assert checks["evidence.telegram_bot_live"]["status"] == "pending"
    serialized = json.dumps(payload, ensure_ascii=False).lower()
    assert "token" + "=" not in serialized
    assert "secret" + "=" not in serialized
    assert "password" + "=" not in serialized


def test_live_release_gate_accepts_valid_local_ci_summary(tmp_path):
    summary_path = tmp_path / "summary.json"
    output_json = tmp_path / "live-release-gate.json"
    _write_local_ci_summary(summary_path)

    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/live-release-gate.py"),
            "--local-ci-summary",
            str(summary_path),
            "--output-json",
            str(output_json),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    payload = _load_json(output_json)
    checks = {item["id"]: item for item in payload["checks"]}
    assert checks["evidence.local_ci_quick"]["status"] == "pass"
    assert checks["evidence.remote_ci_current_commit"]["status"] == "pending"
    assert payload["shipGate"]["status"] == "blocked"


def test_live_release_gate_rejects_invalid_local_ci_summary(tmp_path):
    cases = [
        {"profile": "full", "status": "passed", "commit": _git_head(), "expected": "profile must be quick"},
        {"profile": "quick", "status": "failed", "commit": _git_head(), "expected": "status must be passed"},
        {"profile": "quick", "status": "passed", "commit": "0" * 40, "expected": "summary commit does not match"},
    ]

    for index, case in enumerate(cases):
        summary_path = tmp_path / f"summary-{index}.json"
        output_json = tmp_path / f"live-release-gate-{index}.json"
        _write_local_ci_summary(
            summary_path,
            profile=case["profile"],
            status=case["status"],
            commit=case["commit"],
        )

        result = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts/live-release-gate.py"),
                "--local-ci-summary",
                str(summary_path),
                "--output-json",
                str(output_json),
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

        assert result.returncode == 0, result.stderr
        payload = _load_json(output_json)
        checks = {item["id"]: item for item in payload["checks"]}
        assert checks["evidence.local_ci_quick"]["status"] == "fail"
        assert case["expected"] in checks["evidence.local_ci_quick"]["detail"]


def test_live_release_gate_required_mode_fails_without_external_evidence(tmp_path):
    output_json = tmp_path / "live-release-gate-required.json"
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/live-release-gate.py"),
            "--require-live",
            "--output-json",
            str(output_json),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 1
    summary = json.loads(result.stdout)
    assert summary["status"] == "failed"
    assert summary["shipGate"] in {"blocked", "fail"}

    payload = _load_json(output_json)
    blocking_items = set(payload["shipGate"]["blockingItems"])
    assert "evidence.production_api_live" in blocking_items
    assert "evidence.hf_space_live" in blocking_items
    assert "evidence.telegram_bot_live" in blocking_items
