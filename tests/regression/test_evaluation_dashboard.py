from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DASHBOARD_PATH = ROOT / "scripts" / "evaluation-dashboard.py"


def _load_dashboard_module():
    spec = importlib.util.spec_from_file_location("fatecat_evaluation_dashboard", DASHBOARD_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _summary() -> dict:
    return {
        "schemaVersion": 1,
        "generatedAt": "2026-07-02T00:00:00Z",
        "registry": "contracts/fate/evaluations/registry.json",
        "gitCommit": "test-commit",
        "selection": {
            "runIds": ["run.local_ci_quick"],
            "allLocal": False,
            "allLocalRequired": False,
            "allowReferenceRepo": False,
        },
        "dryRun": False,
        "summary": {"total": 1, "passed": 1, "failed": 0, "skipped": 0, "planned": 0, "status": "passed"},
        "runs": [
            {
                "runId": "run.local_ci_quick<script>",
                "name": "本地 quick CI release gate",
                "runType": "release_gate",
                "gateType": "required",
                "releaseRequired": True,
                "localAvailability": "tracked_in_repo",
                "datasetIds": ["dataset.solar_terms_1900_2030"],
                "status": "passed",
                "commands": [
                    {
                        "command": "bash scripts/local-ci.sh --profile quick",
                        "exitCode": 0,
                        "durationMs": 100,
                        "stdoutTail": "should-not-render",
                        "stderrTail": "should-not-render",
                    }
                ],
            }
        ],
    }


def _diff() -> dict:
    return {
        "schemaVersion": 1,
        "summary": {
            "status": "passed",
            "runTotal": 1,
            "newFailedRuns": 0,
            "missingRuns": 0,
            "statusRegressions": 0,
            "failedCommands": 0,
            "policyViolations": [],
        },
        "runs": [
            {
                "runId": "run.local_ci_quick",
                "changeType": "unchanged",
                "baselineStatus": "passed",
                "currentStatus": "passed",
                "regression": False,
                "details": "未发现状态回退。",
            }
        ],
    }


def test_evaluation_dashboard_escapes_html_and_omits_command_tails():
    dashboard = _load_dashboard_module()

    markup = dashboard.render_dashboard(_summary(), _diff())

    assert "FateCat Evaluation Dashboard" in markup
    assert "run.local_ci_quick&lt;script&gt;" in markup
    assert "run.local_ci_quick<script>" not in markup
    assert "should-not-render" not in markup
    assert "Privacy Boundary" in markup
    assert "Diff status" in markup


def test_evaluation_dashboard_cli_writes_html_and_summary(tmp_path):
    dashboard = _load_dashboard_module()
    summary_json = tmp_path / "summary.json"
    diff_json = tmp_path / "diff.json"
    output_html = tmp_path / "dashboard.html"
    output_json = tmp_path / "dashboard-summary.json"
    summary_json.write_text(json.dumps(_summary(), ensure_ascii=False), encoding="utf-8")
    diff_json.write_text(json.dumps(_diff(), ensure_ascii=False), encoding="utf-8")

    exit_code = dashboard.main(
        [
            "--summary-json",
            str(summary_json),
            "--diff-json",
            str(diff_json),
            "--output-html",
            str(output_html),
            "--output-json",
            str(output_json),
        ]
    )

    assert exit_code == 0
    assert "Evaluation Runs" in output_html.read_text(encoding="utf-8")
    stored = json.loads(output_json.read_text(encoding="utf-8"))
    assert stored["status"] == "passed"
    assert stored["summaryStatus"] == "passed"
    assert stored["diffStatus"] == "passed"
    assert stored["runCount"] == 1
    assert "token" in stored["privacyBoundary"]
