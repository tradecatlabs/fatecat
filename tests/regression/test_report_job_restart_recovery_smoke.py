from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SMOKE_PATH = ROOT / "scripts" / "report-job-restart-recovery-smoke.py"


def _load_smoke_module():
    spec = importlib.util.spec_from_file_location("fatecat_restart_recovery_smoke", SMOKE_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_report_job_restart_recovery_smoke_checks_rebuild_contract(tmp_path):
    smoke = _load_smoke_module()
    output_json = tmp_path / "restart-recovery-smoke.json"

    summary = smoke.run_smoke()
    smoke.write_summary(summary, output_json)
    stored = json.loads(output_json.read_text(encoding="utf-8"))

    assert stored["schemaVersion"] == 1
    assert stored["kind"] == "fatecat.report_job_restart_recovery_smoke"
    assert stored["status"] == "passed"
    assert "job.recovered_failed" in stored["eventTypes"]
    checks = {item["name"]: item for item in stored["checks"]}
    assert checks["job_running_before_rebuild"]["ok"] is True
    assert checks["job_failed_after_rebuild"]["ok"] is True
    assert checks["recovered_failed_event"]["ok"] is True
    assert checks["idempotency_reuses_recovered_job"]["ok"] is True
    serialized = json.dumps(stored, ensure_ascii=False)
    assert "测试样本" not in serialized
    assert "北京" not in serialized
    assert "should-not-run" not in serialized
    assert "不证明任务跨进程继续执行" in stored["boundary"]


def test_report_job_restart_recovery_smoke_cli_writes_summary(tmp_path):
    smoke = _load_smoke_module()
    output_json = tmp_path / "restart-recovery-smoke-cli.json"

    exit_code = smoke.main(["--output-json", str(output_json)])

    assert exit_code == 0
    stored = json.loads(output_json.read_text(encoding="utf-8"))
    assert stored["status"] == "passed"
    assert "token" in stored["privacyBoundary"]
