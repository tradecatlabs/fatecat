#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_POLICY = REPO_ROOT / "contracts" / "fate" / "evaluations" / "diff-policy.json"
DEFAULT_OUTPUT_JSON = REPO_ROOT / "infra" / "runtime" / "local-state" / "exports" / "evaluations" / "diff.json"


class EvaluationDiffError(ValueError):
    """Evaluation summary diff 输入不合法。"""


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def load_policy(path: Path = DEFAULT_POLICY) -> dict[str, Any]:
    return load_json(path)


def _runs_by_id(summary: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {item["runId"]: item for item in summary.get("runs", [])}


def _command_failures(run: dict[str, Any]) -> int:
    return sum(1 for item in run.get("commands", []) if item.get("exitCode") not in {0, None})


def compare_summaries(
    baseline: dict[str, Any],
    current: dict[str, Any],
    policy: dict[str, Any],
) -> dict[str, Any]:
    baseline_runs = _runs_by_id(baseline)
    current_runs = _runs_by_id(current)
    run_ids = sorted(set(baseline_runs) | set(current_runs))
    run_diffs: list[dict[str, Any]] = []

    new_failures = 0
    missing_runs = 0
    status_regressions = 0
    command_failures = 0

    for run_id in run_ids:
        before = baseline_runs.get(run_id)
        after = current_runs.get(run_id)
        if before is None:
            run_diffs.append(
                {
                    "runId": run_id,
                    "changeType": "added",
                    "baselineStatus": None,
                    "currentStatus": after.get("status") if after else None,
                    "regression": False,
                    "details": "current summary 新增 run。",
                }
            )
            continue
        if after is None:
            missing_runs += 1
            run_diffs.append(
                {
                    "runId": run_id,
                    "changeType": "removed",
                    "baselineStatus": before.get("status"),
                    "currentStatus": None,
                    "regression": True,
                    "details": "baseline 中存在的 run 在 current summary 中缺失。",
                }
            )
            continue

        before_status = before.get("status")
        after_status = after.get("status")
        after_command_failures = _command_failures(after)
        regression = False
        details: list[str] = []

        if before_status == "passed" and after_status != "passed":
            status_regressions += 1
            regression = True
            details.append("run 状态从 passed 退化。")
        if after_status == "failed" and before_status != "failed":
            new_failures += 1
            regression = True
            details.append("current 新增 failed run。")
        if after_command_failures:
            command_failures += after_command_failures
            regression = True
            details.append(f"current 存在 {after_command_failures} 个失败命令。")

        run_diffs.append(
            {
                "runId": run_id,
                "changeType": "changed" if before_status != after_status else "unchanged",
                "baselineStatus": before_status,
                "currentStatus": after_status,
                "regression": regression,
                "baselineCommandFailures": _command_failures(before),
                "currentCommandFailures": after_command_failures,
                "details": " ".join(details) if details else "未发现状态回退。",
            }
        )

    thresholds = policy.get("thresholds") or {}
    allowed_new_failures = int(thresholds.get("maxNewFailedRuns", 0))
    allowed_missing_runs = int(thresholds.get("maxMissingRuns", 0))
    allowed_command_failures = int(thresholds.get("maxFailedCommands", 0))
    policy_violations: list[str] = []
    if new_failures > allowed_new_failures:
        policy_violations.append(f"newFailedRuns={new_failures} > {allowed_new_failures}")
    if missing_runs > allowed_missing_runs:
        policy_violations.append(f"missingRuns={missing_runs} > {allowed_missing_runs}")
    if command_failures > allowed_command_failures:
        policy_violations.append(f"failedCommands={command_failures} > {allowed_command_failures}")

    status = "failed" if policy_violations or status_regressions else "passed"
    return {
        "schemaVersion": 1,
        "policy": {
            "path": str(policy.get("path") or DEFAULT_POLICY.relative_to(REPO_ROOT)),
            "version": policy.get("version"),
            "thresholds": thresholds,
        },
        "baseline": {
            "generatedAt": baseline.get("generatedAt"),
            "gitCommit": baseline.get("gitCommit"),
            "status": (baseline.get("summary") or {}).get("status"),
        },
        "current": {
            "generatedAt": current.get("generatedAt"),
            "gitCommit": current.get("gitCommit"),
            "status": (current.get("summary") or {}).get("status"),
        },
        "summary": {
            "status": status,
            "runTotal": len(run_diffs),
            "newFailedRuns": new_failures,
            "missingRuns": missing_runs,
            "statusRegressions": status_regressions,
            "failedCommands": command_failures,
            "policyViolations": policy_violations,
        },
        "runs": run_diffs,
    }


def write_diff(diff: dict[str, Any], output_json: Path) -> None:
    output_json.parent.mkdir(parents=True, exist_ok=True)
    with output_json.open("w", encoding="utf-8") as fh:
        json.dump(diff, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="比较两个 EvaluationRun summary JSON，并按 diff policy 判定是否回归。")
    parser.add_argument("--baseline-json", type=Path, required=True, help="baseline Evaluation summary JSON。")
    parser.add_argument("--current-json", type=Path, required=True, help="current Evaluation summary JSON。")
    parser.add_argument("--policy", type=Path, default=DEFAULT_POLICY, help="diff policy JSON。")
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON, help="diff JSON 输出路径。")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        diff = compare_summaries(
            load_json(args.baseline_json),
            load_json(args.current_json),
            load_policy(args.policy),
        )
        write_diff(diff, args.output_json)
        print(json.dumps(diff["summary"], ensure_ascii=False, sort_keys=True))
        return 1 if diff["summary"]["status"] == "failed" else 0
    except (EvaluationDiffError, OSError, json.JSONDecodeError) as exc:
        print(f"evaluation diff error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
