#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shlex
import subprocess
import sys
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REGISTRY = REPO_ROOT / "contracts" / "fate" / "evaluations" / "registry.json"
DEFAULT_OUTPUT_JSON = REPO_ROOT / "infra" / "runtime" / "local-state" / "exports" / "evaluations" / "summary.json"
DEFAULT_HISTORY_DIR = REPO_ROOT / "infra" / "runtime" / "local-state" / "exports" / "evaluations" / "history"
TAIL_LIMIT = 4000
PYTHON_COMMANDS = {".venv/bin/python", "python", "python3"}
FORBIDDEN_TOKEN_FRAGMENTS = (";", "&", "|", ">", "<", "`", "$(", "\n", "\r")


class EvaluationRunnerError(ValueError):
    """评测执行器输入或 registry 命令不满足安全约束。"""


def utc_now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def load_registry(path: Path = DEFAULT_REGISTRY) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def evaluation_runs(registry: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {item["id"]: item for item in registry.get("resources", []) if item.get("resourceType") == "EvaluationRun"}


def select_evaluation_runs(
    registry: dict[str, Any],
    *,
    run_ids: list[str],
    all_local: bool,
    all_local_required: bool,
) -> list[dict[str, Any]]:
    runs = evaluation_runs(registry)
    selected_ids: list[str] = []

    if not run_ids and not all_local and not all_local_required:
        all_local_required = True

    for run_id in run_ids:
        if run_id not in runs:
            raise EvaluationRunnerError(f"未知 EvaluationRun: {run_id}")
        selected_ids.append(run_id)

    if all_local:
        selected_ids.extend(
            run_id for run_id, item in runs.items() if item.get("localAvailability") == "tracked_in_repo"
        )

    if all_local_required:
        selected_ids.extend(
            run_id
            for run_id, item in runs.items()
            if item.get("localAvailability") == "tracked_in_repo" and item.get("releaseRequired") is True
        )

    deduped_ids = list(dict.fromkeys(selected_ids))
    return [runs[run_id] for run_id in deduped_ids]


def _has_forbidden_shell_syntax(token: str) -> bool:
    return any(fragment in token for fragment in FORBIDDEN_TOKEN_FRAGMENTS)


def _resolve_repo_relative_path(root: Path, raw_path: str) -> Path:
    path = Path(raw_path)
    if path.is_absolute():
        raise EvaluationRunnerError(f"命令路径必须是仓库相对路径: {raw_path}")
    if ".." in path.parts:
        raise EvaluationRunnerError(f"命令路径不得越过仓库根: {raw_path}")
    resolved = (root / path).resolve()
    try:
        resolved.relative_to(root.resolve())
    except ValueError as exc:
        raise EvaluationRunnerError(f"命令路径不在仓库内: {raw_path}") from exc
    return resolved


def _validate_bash_command(parts: list[str], root: Path) -> None:
    if len(parts) < 2:
        raise EvaluationRunnerError("bash 命令必须指定 scripts/ 下的脚本")
    script_path = parts[1]
    if not script_path.startswith("scripts/") or not script_path.endswith(".sh"):
        raise EvaluationRunnerError(f"bash 只允许执行 scripts/*.sh: {script_path}")
    resolved = _resolve_repo_relative_path(root, script_path)
    if not resolved.exists():
        raise EvaluationRunnerError(f"bash 脚本不存在: {script_path}")


def _validate_python_command(parts: list[str], root: Path) -> None:
    if len(parts) < 3 or parts[1:3] != ["-m", "pytest"]:
        raise EvaluationRunnerError("Python 评测命令只允许 `.venv/bin/python -m pytest ...` 形式")
    for token in parts[3:]:
        if token.startswith("-"):
            continue
        if "/" in token or token.endswith(".py"):
            resolved = _resolve_repo_relative_path(root, token)
            if token.endswith(".py") and not resolved.exists():
                raise EvaluationRunnerError(f"pytest 目标不存在: {token}")


def validate_command(command: str, root: Path = REPO_ROOT) -> list[str]:
    parts = shlex.split(command)
    if not parts:
        raise EvaluationRunnerError("EvaluationRun command 不能为空")
    for token in parts:
        if _has_forbidden_shell_syntax(token):
            raise EvaluationRunnerError(f"命令含不允许的 shell 语法: {command}")

    executable = parts[0]
    if executable == "bash":
        _validate_bash_command(parts, root)
        return parts
    if executable in PYTHON_COMMANDS:
        _validate_python_command(parts, root)
        return parts
    raise EvaluationRunnerError(f"EvaluationRun command 不在白名单内: {executable}")


def _tail(text: str, limit: int = TAIL_LIMIT) -> str:
    if len(text) <= limit:
        return text
    return text[-limit:]


def _git_commit(root: Path) -> str:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=root,
            check=False,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (OSError, subprocess.TimeoutExpired):
        return "unknown"
    if result.returncode != 0:
        return "unknown"
    return result.stdout.strip() or "unknown"


def _run_command(parts: list[str], root: Path, timeout_seconds: int) -> dict[str, Any]:
    started = time.monotonic()
    try:
        result = subprocess.run(
            parts,
            cwd=root,
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
        )
        duration_ms = int((time.monotonic() - started) * 1000)
        return {
            "command": shlex.join(parts),
            "exitCode": result.returncode,
            "durationMs": duration_ms,
            "stdoutTail": _tail(result.stdout),
            "stderrTail": _tail(result.stderr),
        }
    except subprocess.TimeoutExpired as exc:
        duration_ms = int((time.monotonic() - started) * 1000)
        return {
            "command": shlex.join(parts),
            "exitCode": 124,
            "durationMs": duration_ms,
            "stdoutTail": _tail(exc.stdout or ""),
            "stderrTail": _tail(exc.stderr or f"命令超时：{timeout_seconds}s"),
        }


def _run_status(command_results: list[dict[str, Any]]) -> str:
    if any(item["exitCode"] != 0 for item in command_results):
        return "failed"
    return "passed"


def run_evaluations(
    *,
    registry_path: Path = DEFAULT_REGISTRY,
    run_ids: list[str] | None = None,
    all_local: bool = False,
    all_local_required: bool = False,
    allow_reference_repo: bool = False,
    dry_run: bool = False,
    timeout_seconds: int = 900,
) -> dict[str, Any]:
    run_ids = run_ids or []
    registry = load_registry(registry_path)
    root = registry_path.resolve().parents[3]
    selected_runs = select_evaluation_runs(
        registry,
        run_ids=run_ids,
        all_local=all_local,
        all_local_required=all_local_required,
    )

    run_results: list[dict[str, Any]] = []
    for item in selected_runs:
        local_availability = item["localAvailability"]
        command_results: list[dict[str, Any]] = []
        if local_availability != "tracked_in_repo" and not allow_reference_repo:
            run_results.append(
                {
                    "runId": item["id"],
                    "name": item["name"],
                    "runType": item["runType"],
                    "gateType": item["gateType"],
                    "releaseRequired": item["releaseRequired"],
                    "localAvailability": local_availability,
                    "datasetIds": item["datasetIds"],
                    "status": "skipped",
                    "skipReason": "localAvailability 不是 tracked_in_repo；如需执行 reference repo 评测，显式追加 --allow-reference-repo。",
                    "commands": [],
                }
            )
            continue

        for command in item["commands"]:
            parts = validate_command(command, root)
            if dry_run:
                command_results.append(
                    {
                        "command": shlex.join(parts),
                        "exitCode": None,
                        "durationMs": 0,
                        "stdoutTail": "",
                        "stderrTail": "",
                    }
                )
                continue
            command_results.append(_run_command(parts, root, timeout_seconds))

        run_results.append(
            {
                "runId": item["id"],
                "name": item["name"],
                "runType": item["runType"],
                "gateType": item["gateType"],
                "releaseRequired": item["releaseRequired"],
                "localAvailability": local_availability,
                "datasetIds": item["datasetIds"],
                "status": "planned" if dry_run else _run_status(command_results),
                "commands": command_results,
            }
        )

    passed = sum(1 for item in run_results if item["status"] == "passed")
    failed = sum(1 for item in run_results if item["status"] == "failed")
    skipped = sum(1 for item in run_results if item["status"] == "skipped")
    planned = sum(1 for item in run_results if item["status"] == "planned")
    summary_status = "failed" if failed else "passed"
    if not failed and skipped and not passed and not planned:
        summary_status = "skipped"
    if dry_run:
        summary_status = "planned"

    return {
        "schemaVersion": 1,
        "generatedAt": utc_now(),
        "registry": str(registry_path.relative_to(root)),
        "gitCommit": _git_commit(root),
        "selection": {
            "runIds": run_ids,
            "allLocal": all_local,
            "allLocalRequired": all_local_required or (not run_ids and not all_local),
            "allowReferenceRepo": allow_reference_repo,
        },
        "dryRun": dry_run,
        "summary": {
            "total": len(run_results),
            "passed": passed,
            "failed": failed,
            "skipped": skipped,
            "planned": planned,
            "status": summary_status,
        },
        "runs": run_results,
    }


def write_summary(summary: dict[str, Any], output_json: Path) -> None:
    output_json.parent.mkdir(parents=True, exist_ok=True)
    with output_json.open("w", encoding="utf-8") as fh:
        json.dump(summary, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


def record_history(summary: dict[str, Any], history_dir: Path = DEFAULT_HISTORY_DIR) -> dict[str, str]:
    history_dir.mkdir(parents=True, exist_ok=True)
    generated_at = str(summary.get("generatedAt") or utc_now())
    timestamp = generated_at.replace(":", "").replace("-", "").replace("Z", "Z")
    status = str((summary.get("summary") or {}).get("status") or "unknown")
    history_path = history_dir / f"{timestamp}-{status}.json"
    latest_path = history_dir / "latest.json"
    with history_path.open("w", encoding="utf-8") as fh:
        json.dump(summary, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    with latest_path.open("w", encoding="utf-8") as fh:
        json.dump(summary, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    return {"historyPath": str(history_path), "latestPath": str(latest_path)}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="执行 contracts/fate/evaluations/registry.json 中登记的 EvaluationRun。"
    )
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY, help="Evaluation registry JSON 路径。")
    parser.add_argument("--run-id", action="append", default=[], help="指定 EvaluationRun id，可重复。")
    parser.add_argument("--all-local", action="store_true", help="执行所有 tracked_in_repo 的 EvaluationRun。")
    parser.add_argument(
        "--all-local-required",
        action="store_true",
        help="执行所有 tracked_in_repo 且 releaseRequired=true 的 EvaluationRun。",
    )
    parser.add_argument(
        "--allow-reference-repo", action="store_true", help="允许执行 requires_reference_repo 的可选离线评测。"
    )
    parser.add_argument("--dry-run", action="store_true", help="只校验选择和命令白名单，不实际执行命令。")
    parser.add_argument("--timeout-seconds", type=int, default=900, help="单条命令超时时间。")
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON, help="summary JSON 输出路径。")
    parser.add_argument(
        "--record-history", action="store_true", help="把本次 summary 复制到 history 目录并更新 latest.json。"
    )
    parser.add_argument(
        "--history-dir", type=Path, default=DEFAULT_HISTORY_DIR, help="Evaluation summary history 目录。"
    )
    parser.add_argument("--list", action="store_true", help="列出 EvaluationRun id 后退出。")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.list:
            registry = load_registry(args.registry)
            for run_id in evaluation_runs(registry):
                print(run_id)
            return 0

        summary = run_evaluations(
            registry_path=args.registry,
            run_ids=args.run_id,
            all_local=args.all_local,
            all_local_required=args.all_local_required,
            allow_reference_repo=args.allow_reference_repo,
            dry_run=args.dry_run,
            timeout_seconds=args.timeout_seconds,
        )
        if args.record_history:
            summary["history"] = record_history(summary, args.history_dir)
        write_summary(summary, args.output_json)
        print(json.dumps(summary["summary"], ensure_ascii=False, sort_keys=True))
        return 1 if summary["summary"]["failed"] else 0
    except EvaluationRunnerError as exc:
        print(f"evaluation runner error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
