#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_HISTORY_DIR = REPO_ROOT / "infra" / "runtime" / "local-state" / "exports" / "evaluations" / "history"
DEFAULT_POLICY = REPO_ROOT / "contracts" / "fate" / "evaluations" / "trend-policy.json"
DEFAULT_OUTPUT_JSON = REPO_ROOT / "infra" / "runtime" / "local-state" / "exports" / "evaluations" / "trend-gate.json"


class EvaluationTrendGateError(ValueError):
    """Evaluation trend gate 输入不合法。"""


def utc_now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as fh:
        payload = json.load(fh)
    if not isinstance(payload, dict):
        raise EvaluationTrendGateError(f"JSON root must be object: {path}")
    return payload


def _rel(path: Path) -> str:
    try:
        return path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return str(path)


def _summary_status(summary: dict[str, Any]) -> str:
    return str((summary.get("summary") or {}).get("status") or "unknown")


def _failed_runs(summary: dict[str, Any]) -> list[str]:
    return [str(item.get("runId")) for item in summary.get("runs", []) if item.get("status") == "failed"]


def _failed_commands(summary: dict[str, Any]) -> int:
    count = 0
    for run in summary.get("runs", []):
        for command in run.get("commands", []):
            if command.get("exitCode") not in {0, None}:
                count += 1
    return count


def _required_runs(summary: dict[str, Any]) -> set[str]:
    return {str(item.get("runId")) for item in summary.get("runs", []) if item.get("releaseRequired") is True}


def _history_files(history_dir: Path) -> list[Path]:
    if not history_dir.is_dir():
        return []
    return sorted(path for path in history_dir.glob("*.json") if path.name != "latest.json" and path.is_file())


def load_history(history_dir: Path, window: int) -> list[dict[str, Any]]:
    files = _history_files(history_dir)
    selected = files[-window:] if window > 0 else files
    summaries: list[dict[str, Any]] = []
    for path in selected:
        payload = load_json(path)
        summaries.append({"path": _rel(path), "payload": payload})
    latest_path = history_dir / "latest.json"
    if latest_path.is_file():
        latest = load_json(latest_path)
        if not summaries or summaries[-1]["payload"].get("generatedAt") != latest.get("generatedAt"):
            summaries.append({"path": _rel(latest_path), "payload": latest})
    return summaries


def _consecutive_failed(summaries: list[dict[str, Any]]) -> int:
    count = 0
    for item in reversed(summaries):
        if _summary_status(item["payload"]) == "failed":
            count += 1
            continue
        break
    return count


def append_finding(findings: list[dict[str, Any]], *, metric: str, actual: Any, expected: Any) -> None:
    findings.append({"metric": metric, "actual": actual, "expected": expected})


def build_trend_report(
    *, history_dir: Path = DEFAULT_HISTORY_DIR, policy_path: Path = DEFAULT_POLICY
) -> dict[str, Any]:
    policy = load_json(policy_path)
    history_policy = policy.get("history") or {}
    window = int(history_policy.get("defaultWindow", 10))
    summaries = load_history(history_dir, window)
    findings: list[dict[str, Any]] = []

    min_summaries = int(history_policy.get("minSummaries", 1))
    if len(summaries) < min_summaries:
        append_finding(findings, metric="minSummaries", actual=len(summaries), expected=min_summaries)

    latest = summaries[-1]["payload"] if summaries else {}
    latest_status = _summary_status(latest) if latest else "missing"
    if history_policy.get("latestMustPass") is True and latest_status != "passed":
        append_finding(findings, metric="latestStatus", actual=latest_status, expected="passed")

    consecutive_failed = _consecutive_failed(summaries)
    max_consecutive = int(history_policy.get("maxConsecutiveFailedSummaries", 0))
    if consecutive_failed > max_consecutive:
        append_finding(
            findings,
            metric="consecutiveFailedSummaries",
            actual=consecutive_failed,
            expected=max_consecutive,
        )

    latest_failed_runs = _failed_runs(latest)
    max_failed_runs = int(history_policy.get("maxLatestFailedRuns", 0))
    if len(latest_failed_runs) > max_failed_runs:
        append_finding(findings, metric="latestFailedRuns", actual=latest_failed_runs, expected=max_failed_runs)

    latest_failed_commands = _failed_commands(latest)
    max_failed_commands = int(history_policy.get("maxLatestFailedCommands", 0))
    if latest_failed_commands > max_failed_commands:
        append_finding(
            findings,
            metric="latestFailedCommands",
            actual=latest_failed_commands,
            expected=max_failed_commands,
        )

    expected_required_runs = set()
    for item in summaries[:-1]:
        expected_required_runs.update(_required_runs(item["payload"]))
    latest_required_runs = _required_runs(latest)
    missing_required = sorted(expected_required_runs - latest_required_runs)
    max_missing_required = int(history_policy.get("maxLatestMissingRequiredRuns", 0))
    if len(missing_required) > max_missing_required:
        append_finding(
            findings,
            metric="latestMissingRequiredRuns",
            actual=missing_required,
            expected=max_missing_required,
        )

    status_counts: dict[str, int] = {}
    history_entries = []
    for item in summaries:
        payload = item["payload"]
        status = _summary_status(payload)
        status_counts[status] = status_counts.get(status, 0) + 1
        history_entries.append(
            {
                "path": item["path"],
                "generatedAt": payload.get("generatedAt"),
                "gitCommit": payload.get("gitCommit"),
                "status": status,
                "total": (payload.get("summary") or {}).get("total"),
                "passed": (payload.get("summary") or {}).get("passed"),
                "failed": (payload.get("summary") or {}).get("failed"),
                "failedRuns": _failed_runs(payload),
                "failedCommands": _failed_commands(payload),
            }
        )

    return {
        "schemaVersion": 1,
        "kind": "fatecat.evaluation_trend_gate",
        "generatedAt": utc_now(),
        "status": "failed" if findings else "passed",
        "policy": _rel(policy_path),
        "historyDir": _rel(history_dir),
        "window": window,
        "summaryCount": len(summaries),
        "latest": history_entries[-1] if history_entries else None,
        "statusCounts": status_counts,
        "consecutiveFailedSummaries": consecutive_failed,
        "trendFindings": findings,
        "history": history_entries,
        "privacyBoundary": policy["privacyBoundary"],
        "productionBoundary": policy["productionBoundary"],
    }


def write_report(report: dict[str, Any], output_json: Path) -> None:
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="执行 EvaluationRun 历史趋势门禁。")
    parser.add_argument(
        "--history-dir", type=Path, default=DEFAULT_HISTORY_DIR, help="Evaluation summary history 目录。"
    )
    parser.add_argument("--policy", type=Path, default=DEFAULT_POLICY, help="Evaluation trend policy JSON。")
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON, help="trend gate JSON 输出路径。")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        report = build_trend_report(history_dir=args.history_dir, policy_path=args.policy)
        write_report(report, args.output_json)
        print(
            json.dumps(
                {
                    "status": report["status"],
                    "summaryCount": report["summaryCount"],
                    "latestStatus": (report.get("latest") or {}).get("status"),
                    "trendFindings": len(report["trendFindings"]),
                },
                ensure_ascii=False,
                sort_keys=True,
            )
        )
        return 1 if report["status"] == "failed" else 0
    except (EvaluationTrendGateError, OSError, json.JSONDecodeError, KeyError) as exc:
        print(f"evaluation trend gate error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
