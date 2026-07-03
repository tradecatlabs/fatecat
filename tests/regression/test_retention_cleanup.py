from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SMOKE_SCRIPT = ROOT / "scripts" / "retention-cleanup-smoke.py"
CLEANUP_SCRIPT = ROOT / "scripts" / "retention-cleanup.py"
SECURITY_DIR = ROOT / "contracts" / "fate" / "security"


def _run_script(script: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(script), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def _target(summary: dict, name: str) -> dict:
    for item in summary["targets"]:
        if item["target"] == name:
            return item
    raise AssertionError(f"missing target: {name}")


def test_retention_cleanup_smoke_removes_only_expired_terminal_fixture(tmp_path):
    output_json = tmp_path / "retention-cleanup-smoke.json"

    result = _run_script(SMOKE_SCRIPT, "--output-json", str(output_json), "--pretty")

    assert result.returncode == 0, result.stderr or result.stdout
    summary = json.loads(output_json.read_text(encoding="utf-8"))
    assert summary["schemaVersion"] == 1
    assert summary["kind"] == "fatecat.retention_cleanup_smoke"
    assert summary["status"] == "passed"
    assert {item["name"] for item in summary["checks"]} >= {
        "dry_run_passed",
        "execute_passed",
        "old_record_removed",
        "old_terminal_job_removed",
        "fresh_terminal_job_kept",
        "old_running_job_kept",
        "related_event_removed",
        "related_outbox_removed",
        "related_delivery_config_removed",
    }
    assert all(item["ok"] is True for item in summary["checks"])

    dry_run_records = _target(summary["dryRun"], "records")
    execute_records = _target(summary["execute"], "records")
    assert dry_run_records["candidateCount"] == 1
    assert dry_run_records["deletedCount"] == 0
    assert execute_records["candidateCount"] == 1
    assert execute_records["deletedCount"] == 1

    dry_run_jobs = _target(summary["dryRun"], "reportJobs")
    execute_jobs = _target(summary["execute"], "reportJobs")
    assert dry_run_jobs["candidateCount"] == 1
    assert dry_run_jobs["deletedRows"]["jobs"] == 0
    assert execute_jobs["candidateCount"] == 1
    assert execute_jobs["deletedRows"] == {
        "events": 1,
        "jobs": 1,
        "webhookDeliveryConfigs": 1,
        "webhookOutbox": 1,
    }
    assert _target(summary["execute"], "auditEvents")["status"] == "external_connectivity_pending"

    rendered = json.dumps(summary, ensure_ascii=False)
    for forbidden in (
        "old-terminal",
        "fresh-terminal",
        "old-running",
        "old-user",
        "fresh-user",
        "旧样本",
        "新样本",
        "token=",
        "secret=",
        "password=",
    ):
        assert forbidden not in rendered


def test_retention_cleanup_cli_dry_run_skips_missing_local_databases(tmp_path):
    output_json = tmp_path / "retention-cleanup.json"
    missing_records = tmp_path / "missing-records.sqlite"
    missing_jobs = tmp_path / "missing-report-jobs.sqlite"

    result = _run_script(
        CLEANUP_SCRIPT,
        "--record-db",
        str(missing_records),
        "--report-job-db",
        str(missing_jobs),
        "--record-retention-days",
        "30",
        "--output-json",
        str(output_json),
    )

    assert result.returncode == 0, result.stderr or result.stdout
    summary = json.loads(output_json.read_text(encoding="utf-8"))
    assert summary["kind"] == "fatecat.retention_cleanup_summary"
    assert summary["status"] == "passed"
    assert summary["dryRun"] is True
    assert _target(summary, "records")["status"] == "skipped"
    assert _target(summary, "reportJobs")["status"] == "skipped"
    assert _target(summary, "auditEvents")["status"] == "external_connectivity_pending"


def test_retention_cleanup_contract_registry_and_local_ci_are_wired():
    contract = json.loads((SECURITY_DIR / "retention-cleanup.json").read_text(encoding="utf-8"))
    registry = json.loads((SECURITY_DIR / "registry.json").read_text(encoding="utf-8"))
    policy = json.loads((SECURITY_DIR / "production-security-policy.json").read_text(encoding="utf-8"))
    local_ci = (ROOT / "scripts" / "local-ci.sh").read_text(encoding="utf-8")

    assert contract["resourceType"] == "RetentionCleanupContract"
    assert contract["requiredSmoke"]["kind"] == "fatecat.retention_cleanup_smoke"
    assert contract["commands"]["smoke"] == "bash scripts/retention-cleanup-smoke.sh --output-json <path>"

    controls = {item["id"]: item for item in registry["controls"]}
    retention = controls["control.retention_cleanup_plan"]
    assert "contracts/fate/security/retention-cleanup.json" in retention["implementationRefs"]
    assert (
        "domains/experience-delivery/services/fatecat-delivery/src/retention_cleanup.py"
        in retention["implementationRefs"]
    )
    assert "bash scripts/retention-cleanup-smoke.sh --output-json <path>" in retention["localVerification"]
    assert retention["metadata"]["localCleanerStatus"] == "available"

    assert policy["retention"]["localCleanerMode"] == "sqlite_records_and_report_jobs_smoke"
    assert policy["releaseGate"]["retentionCleanupContract"] == "contracts/fate/security/retention-cleanup.json"
    assert "retention-cleanup-smoke.sh" in local_ci
    assert "FATE_LOCAL_CI_RETENTION_CLEANUP_SMOKE" in local_ci

    assert "retention_cleanup.py" in (
        ROOT / "domains" / "experience-delivery" / "services" / "fatecat-delivery" / "AGENTS.md"
    ).read_text(encoding="utf-8")
    assert "retention-cleanup.json" in (SECURITY_DIR / "AGENTS.md").read_text(encoding="utf-8")
    assert "retention-cleanup-smoke.py" in (ROOT / "scripts" / "AGENTS.md").read_text(encoding="utf-8")
    assert "test_retention_cleanup.py" in (ROOT / "tests" / "AGENTS.md").read_text(encoding="utf-8")
