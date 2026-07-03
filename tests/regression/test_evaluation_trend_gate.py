from __future__ import annotations

import importlib.util
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TREND_PATH = ROOT / "scripts" / "evaluation-trend-gate.py"
POLICY_PATH = ROOT / "contracts" / "fate" / "evaluations" / "trend-policy.json"


def _load_module():
    spec = importlib.util.spec_from_file_location("fatecat_evaluation_trend_gate", TREND_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _summary(*, status: str = "passed", run_status: str = "passed", exit_code: int = 0, run_id: str = "run.a"):
    return {
        "schemaVersion": 1,
        "generatedAt": "2026-07-03T00:00:00Z",
        "registry": "contracts/fate/evaluations/registry.json",
        "gitCommit": "synthetic",
        "selection": {"runIds": [], "allLocal": False, "allLocalRequired": True, "allowReferenceRepo": False},
        "dryRun": False,
        "summary": {
            "total": 1,
            "passed": 1 if status == "passed" else 0,
            "failed": 1 if status == "failed" else 0,
            "skipped": 0,
            "planned": 0,
            "status": status,
        },
        "runs": [
            {
                "runId": run_id,
                "name": "synthetic",
                "runType": "golden_regression",
                "gateType": "required",
                "releaseRequired": True,
                "localAvailability": "tracked_in_repo",
                "datasetIds": ["dataset.synthetic"],
                "status": run_status,
                "commands": [
                    {
                        "command": ".venv/bin/python -m pytest -q tests/regression/test_solar_terms_golden.py",
                        "exitCode": exit_code,
                        "durationMs": 1,
                        "stdoutTail": "must not be copied",
                        "stderrTail": "must not be copied",
                    }
                ],
            }
        ],
    }


def _write_history(history_dir: Path, *summaries: dict):
    history_dir.mkdir(parents=True)
    for index, summary in enumerate(summaries):
        path = history_dir / f"20260703T0{index}0000Z-{summary['summary']['status']}.json"
        path.write_text(json.dumps(summary, ensure_ascii=False), encoding="utf-8")
    (history_dir / "latest.json").write_text(json.dumps(summaries[-1], ensure_ascii=False), encoding="utf-8")


def test_evaluation_trend_gate_passes_clean_history(tmp_path):
    module = _load_module()
    history_dir = tmp_path / "history"
    _write_history(history_dir, _summary(), _summary())

    report = module.build_trend_report(history_dir=history_dir)

    assert report["status"] == "passed"
    assert report["summaryCount"] == 2
    assert report["trendFindings"] == []
    serialized = json.dumps(report, ensure_ascii=False)
    assert "must not be copied" not in serialized


def test_evaluation_trend_gate_fails_latest_regression(tmp_path):
    module = _load_module()
    history_dir = tmp_path / "history"
    _write_history(history_dir, _summary(), _summary(status="failed", run_status="failed", exit_code=1))

    report = module.build_trend_report(history_dir=history_dir)

    assert report["status"] == "failed"
    metrics = {item["metric"] for item in report["trendFindings"]}
    assert {"latestStatus", "consecutiveFailedSummaries", "latestFailedRuns", "latestFailedCommands"} <= metrics


def test_evaluation_trend_gate_detects_missing_required_run(tmp_path):
    module = _load_module()
    history_dir = tmp_path / "history"
    _write_history(history_dir, _summary(run_id="run.a"), _summary(run_id="run.b"))

    report = module.build_trend_report(history_dir=history_dir)

    assert report["status"] == "failed"
    assert any(item["metric"] == "latestMissingRequiredRuns" for item in report["trendFindings"])


def test_evaluation_trend_gate_contract_and_smoke_are_wired(tmp_path):
    policy = json.loads(POLICY_PATH.read_text(encoding="utf-8"))
    local_ci = (ROOT / "scripts" / "local-ci.sh").read_text(encoding="utf-8")
    registry = json.loads((ROOT / "contracts" / "fate" / "evaluations" / "registry.json").read_text(encoding="utf-8"))

    assert policy["kind"] == "fatecat.evaluation_trend_policy"
    assert policy["history"]["latestMustPass"] is True
    assert "evaluation-trend-gate-smoke" in local_ci
    assert registry["metadata"]["trendPolicy"] == "contracts/fate/evaluations/trend-policy.json"
    assert registry["metadata"]["trendCommand"] == "bash scripts/evaluation-trend-gate.sh"

    result = subprocess.run(
        ["bash", "scripts/evaluation-trend-gate-smoke.sh", "--output-dir", str(tmp_path / "smoke")],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert '"status": "passed"' in result.stdout or '"status":"passed"' in result.stdout
