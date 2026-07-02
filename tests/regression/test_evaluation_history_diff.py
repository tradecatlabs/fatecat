from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUNNER_PATH = ROOT / "scripts" / "run-evaluations.py"
DIFF_PATH = ROOT / "scripts" / "compare-evaluations.py"


def _load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _summary(status: str = "passed", run_status: str = "passed", exit_code: int = 0) -> dict:
    return {
        "schemaVersion": 1,
        "generatedAt": "2026-07-02T00:00:00Z",
        "registry": "contracts/fate/evaluations/registry.json",
        "gitCommit": "test-commit",
        "selection": {
            "runIds": ["run.solar_terms_golden"],
            "allLocal": False,
            "allLocalRequired": False,
            "allowReferenceRepo": False,
        },
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
                "runId": "run.solar_terms_golden",
                "name": "节气与历法边界 golden regression",
                "runType": "golden_regression",
                "gateType": "required",
                "releaseRequired": True,
                "localAvailability": "tracked_in_repo",
                "datasetIds": ["dataset.solar_terms_1900_2030"],
                "status": run_status,
                "commands": [
                    {
                        "command": ".venv/bin/python -m pytest -q tests/regression/test_solar_terms_golden.py",
                        "exitCode": exit_code,
                        "durationMs": 100,
                        "stdoutTail": "",
                        "stderrTail": "",
                    }
                ],
            }
        ],
    }


def test_evaluation_runner_records_history_and_latest_pointer(tmp_path):
    runner = _load_module(RUNNER_PATH, "fatecat_evaluation_runner_history")
    summary = _summary()

    history = runner.record_history(summary, tmp_path)
    history_path = Path(history["historyPath"])
    latest_path = Path(history["latestPath"])

    assert history_path.exists()
    assert latest_path.exists()
    assert history_path.name.endswith("-passed.json")
    assert json.loads(history_path.read_text(encoding="utf-8"))["summary"]["status"] == "passed"
    assert json.loads(latest_path.read_text(encoding="utf-8"))["summary"]["status"] == "passed"


def test_evaluation_diff_passes_when_current_matches_baseline():
    diff_module = _load_module(DIFF_PATH, "fatecat_evaluation_diff_pass")
    policy = diff_module.load_policy()

    diff = diff_module.compare_summaries(_summary(), _summary(), policy)

    assert diff["summary"]["status"] == "passed"
    assert diff["summary"]["policyViolations"] == []
    assert diff["runs"][0]["regression"] is False


def test_evaluation_diff_fails_on_new_failed_run_and_failed_command():
    diff_module = _load_module(DIFF_PATH, "fatecat_evaluation_diff_fail")
    policy = diff_module.load_policy()

    diff = diff_module.compare_summaries(
        _summary(), _summary(status="failed", run_status="failed", exit_code=1), policy
    )

    assert diff["summary"]["status"] == "failed"
    assert diff["summary"]["newFailedRuns"] == 1
    assert diff["summary"]["failedCommands"] == 1
    assert diff["summary"]["policyViolations"]
    assert diff["runs"][0]["regression"] is True


def test_evaluation_diff_cli_writes_machine_readable_output(tmp_path):
    diff_module = _load_module(DIFF_PATH, "fatecat_evaluation_diff_cli")
    baseline = tmp_path / "baseline.json"
    current = tmp_path / "current.json"
    output = tmp_path / "diff.json"
    baseline.write_text(json.dumps(_summary(), ensure_ascii=False), encoding="utf-8")
    current.write_text(json.dumps(_summary(), ensure_ascii=False), encoding="utf-8")

    exit_code = diff_module.main(
        [
            "--baseline-json",
            str(baseline),
            "--current-json",
            str(current),
            "--output-json",
            str(output),
        ]
    )

    assert exit_code == 0
    stored = json.loads(output.read_text(encoding="utf-8"))
    assert stored["schemaVersion"] == 1
    assert stored["summary"]["status"] == "passed"
