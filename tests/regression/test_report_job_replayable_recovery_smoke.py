from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SMOKE_PATH = ROOT / "scripts" / "report-job-replayable-recovery-smoke.py"


def _load_smoke_module():
    spec = importlib.util.spec_from_file_location("fatecat_replayable_recovery_smoke", SMOKE_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_report_job_replayable_recovery_smoke_checks_requeue_contract(tmp_path):
    module = _load_smoke_module()
    output_json = tmp_path / "replayable-recovery-smoke.json"

    summary = module.run_smoke()
    module.write_summary(summary, output_json)

    stored = json.loads(output_json.read_text(encoding="utf-8"))
    checks = {item["name"]: item for item in stored["checks"]}
    assert stored["kind"] == "fatecat.report_job_replayable_recovery_smoke"
    assert stored["status"] == "passed"
    assert stored["replayableStatus"] == "succeeded"
    assert stored["nonReplayableStatus"] == "failed"
    assert "job.recovered_requeued" in stored["replayableEventTypes"]
    assert "job.recovered_failed" in stored["nonReplayableEventTypes"]
    assert checks["replayable_job_succeeded"]["ok"] is True
    assert checks["non_replayable_failed"]["ok"] is True
    serialized = json.dumps(stored, ensure_ascii=False)
    assert "callback.example" not in serialized
    assert "# recovered" not in serialized


def test_report_job_replayable_recovery_smoke_cli_writes_summary(tmp_path):
    output_json = tmp_path / "replayable-recovery-smoke-cli.json"
    result = subprocess.run(
        [sys.executable, str(SMOKE_PATH), "--output-json", str(output_json)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    assert '"status": "passed"' in result.stdout
    payload = json.loads(output_json.read_text(encoding="utf-8"))
    assert payload["status"] == "passed"
    assert "external backend" in payload["boundary"]
