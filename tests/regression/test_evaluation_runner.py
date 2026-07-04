from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
RUNNER_PATH = ROOT / "scripts" / "run-evaluations.py"


def _load_runner():
    spec = importlib.util.spec_from_file_location("fatecat_evaluation_runner", RUNNER_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_evaluation_runner_defaults_to_local_required_dry_run(tmp_path):
    runner = _load_runner()
    output_json = tmp_path / "summary.json"

    summary = runner.run_evaluations(dry_run=True)
    runner.write_summary(summary, output_json)
    stored = json.loads(output_json.read_text(encoding="utf-8"))

    assert stored["schemaVersion"] == 1
    assert stored["dryRun"] is True
    assert stored["selection"]["allLocalRequired"] is True
    assert stored["summary"]["status"] == "planned"
    run_ids = {item["runId"] for item in stored["runs"]}
    assert run_ids == {
        "run.core_quality_corpus_gate",
        "run.core_quality_human_review_gate",
        "run.evaluation_dashboard_smoke",
        "run.local_ci_quick",
        "run.solar_terms_golden",
    }
    assert all(item["status"] == "planned" for item in stored["runs"])
    assert all(command["exitCode"] is None for item in stored["runs"] for command in item["commands"])


def test_evaluation_runner_rejects_unknown_run_id():
    runner = _load_runner()

    with pytest.raises(runner.EvaluationRunnerError, match="未知 EvaluationRun"):
        runner.run_evaluations(run_ids=["run.not_found"], dry_run=True)


def test_evaluation_runner_skips_reference_repo_run_without_explicit_allowance():
    runner = _load_runner()

    summary = runner.run_evaluations(run_ids=["run.mingli_bench_offline"], dry_run=False)

    assert summary["summary"]["status"] == "skipped"
    assert summary["summary"]["skipped"] == 1
    assert summary["runs"][0]["status"] == "skipped"
    assert "requires_reference_repo" in summary["runs"][0]["localAvailability"]


def test_evaluation_runner_command_whitelist_blocks_shell_escape():
    runner = _load_runner()

    with pytest.raises(runner.EvaluationRunnerError, match="bash 只允许执行 scripts"):
        runner.validate_command("bash -c 'echo unsafe'", ROOT)

    with pytest.raises(runner.EvaluationRunnerError, match="不允许的 shell 语法"):
        runner.validate_command(
            ".venv/bin/python -m pytest -q tests/regression/test_solar_terms_golden.py ';' rm -rf /", ROOT
        )

    assert runner.validate_command(
        ".venv/bin/python -m pytest -q tests/regression/test_solar_terms_golden.py",
        ROOT,
    ) == [".venv/bin/python", "-m", "pytest", "-q", "tests/regression/test_solar_terms_golden.py"]


def test_evaluation_runner_cli_list_exposes_registered_runs(capsys):
    runner = _load_runner()

    assert runner.main(["--list"]) == 0
    captured = capsys.readouterr()

    assert "run.local_ci_quick" in captured.out
    assert "run.solar_terms_golden" in captured.out
    assert "run.evaluation_dashboard_smoke" in captured.out
    assert "run.mingli_bench_offline" in captured.out
    assert "run.core_quality_human_review_gate" in captured.out
