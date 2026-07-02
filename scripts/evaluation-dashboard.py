#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SUMMARY_JSON = REPO_ROOT / "infra" / "runtime" / "local-state" / "exports" / "evaluations" / "summary.json"
DEFAULT_OUTPUT_HTML = (
    REPO_ROOT / "infra" / "runtime" / "local-state" / "exports" / "evaluations" / "dashboard" / "index.html"
)
DEFAULT_OUTPUT_JSON = (
    REPO_ROOT / "infra" / "runtime" / "local-state" / "exports" / "evaluations" / "dashboard" / "summary.json"
)


class EvaluationDashboardError(ValueError):
    """Evaluation dashboard 输入不合法。"""


def utc_now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as fh:
        payload = json.load(fh)
    if not isinstance(payload, dict):
        raise EvaluationDashboardError(f"JSON 顶层必须是 object: {path}")
    return payload


def _escape(value: Any) -> str:
    return html.escape("" if value is None else str(value), quote=True)


def _status_badge(status: Any) -> str:
    normalized = str(status or "unknown")
    labels = {
        "passed": "通过",
        "failed": "失败",
        "planned": "计划",
        "skipped": "跳过",
        "unknown": "未知",
    }
    return f"{_escape(labels.get(normalized, normalized))} ({_escape(normalized)})"


def _validate_summary(summary: dict[str, Any]) -> None:
    required = {"schemaVersion", "generatedAt", "registry", "gitCommit", "summary", "runs"}
    missing = sorted(required - set(summary))
    if missing:
        raise EvaluationDashboardError(f"summary 缺少字段: {', '.join(missing)}")
    if summary.get("schemaVersion") != 1:
        raise EvaluationDashboardError("summary schemaVersion must be 1")
    if not isinstance(summary.get("runs"), list):
        raise EvaluationDashboardError("summary.runs must be list")


def _render_metadata(summary: dict[str, Any], diff: dict[str, Any] | None) -> str:
    summary_block = summary.get("summary") or {}
    rows = [
        ("生成时间", summary.get("generatedAt")),
        ("Git Commit", summary.get("gitCommit")),
        ("Registry", summary.get("registry")),
        ("Dry Run", summary.get("dryRun")),
        ("Summary Status", summary_block.get("status")),
        ("Total", summary_block.get("total")),
        ("Passed", summary_block.get("passed")),
        ("Failed", summary_block.get("failed")),
        ("Skipped", summary_block.get("skipped")),
        ("Planned", summary_block.get("planned")),
    ]
    if diff:
        diff_summary = diff.get("summary") or {}
        rows.extend(
            [
                ("Diff Status", diff_summary.get("status")),
                ("Policy Violations", ", ".join(diff_summary.get("policyViolations") or [])),
            ]
        )
    rendered = "\n".join(f"<tr><th>{_escape(key)}</th><td>{_escape(value)}</td></tr>" for key, value in rows)
    return f"<table><tbody>{rendered}</tbody></table>"


def _render_runs(summary: dict[str, Any]) -> str:
    rows: list[str] = []
    for run in summary.get("runs", []):
        command_cells = []
        for command in run.get("commands", []):
            command_cells.append(
                "<li>"
                f"<code>{_escape(command.get('command'))}</code>"
                f" exit={_escape(command.get('exitCode'))}"
                f" durationMs={_escape(command.get('durationMs'))}"
                "</li>"
            )
        if not command_cells and run.get("skipReason"):
            command_cells.append(f"<li>{_escape(run.get('skipReason'))}</li>")
        rows.append(
            "<tr>"
            f"<td><code>{_escape(run.get('runId'))}</code></td>"
            f"<td>{_escape(run.get('name'))}</td>"
            f"<td>{_status_badge(run.get('status'))}</td>"
            f"<td>{_escape(run.get('runType'))}</td>"
            f"<td>{_escape(run.get('gateType'))}</td>"
            f"<td>{_escape(run.get('releaseRequired'))}</td>"
            f"<td>{_escape(', '.join(run.get('datasetIds') or []))}</td>"
            f"<td><ul>{''.join(command_cells)}</ul></td>"
            "</tr>"
        )
    return (
        "<table>"
        "<thead><tr><th>Run</th><th>Name</th><th>Status</th><th>Type</th><th>Gate</th>"
        "<th>Release</th><th>Datasets</th><th>Commands</th></tr></thead>"
        f"<tbody>{''.join(rows)}</tbody></table>"
    )


def _render_diff(diff: dict[str, Any] | None) -> str:
    if not diff:
        return "<p>本次没有提供 baseline diff；首次运行或本地未保留 previous latest 时属于预期。</p>"

    diff_summary = diff.get("summary") or {}
    rows = []
    for item in diff.get("runs", []):
        rows.append(
            "<tr>"
            f"<td><code>{_escape(item.get('runId'))}</code></td>"
            f"<td>{_escape(item.get('changeType'))}</td>"
            f"<td>{_escape(item.get('baselineStatus'))}</td>"
            f"<td>{_escape(item.get('currentStatus'))}</td>"
            f"<td>{_escape(item.get('regression'))}</td>"
            f"<td>{_escape(item.get('details'))}</td>"
            "</tr>"
        )
    return (
        f"<p>Diff status: {_status_badge(diff_summary.get('status'))}</p>"
        f"<p>Policy violations: {_escape(', '.join(diff_summary.get('policyViolations') or []))}</p>"
        "<table><thead><tr><th>Run</th><th>Change</th><th>Baseline</th><th>Current</th>"
        f"<th>Regression</th><th>Details</th></tr></thead><tbody>{''.join(rows)}</tbody></table>"
    )


def render_dashboard(summary: dict[str, Any], diff: dict[str, Any] | None = None) -> str:
    _validate_summary(summary)
    generated_at = utc_now()
    status = (summary.get("summary") or {}).get("status")
    return (
        "<!doctype html>\n"
        '<html lang="zh-CN">\n'
        "<head>\n"
        '<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        "<title>FateCat Evaluation Dashboard</title>\n"
        "</head>\n"
        "<body>\n"
        "<main>\n"
        "<h1>FateCat Evaluation Dashboard</h1>\n"
        f"<p>Generated: {_escape(generated_at)}</p>\n"
        f"<p>Overall status: {_status_badge(status)}</p>\n"
        "<section>\n"
        "<h2>Metadata</h2>\n"
        f"{_render_metadata(summary, diff)}\n"
        "</section>\n"
        "<section>\n"
        "<h2>Evaluation Runs</h2>\n"
        f"{_render_runs(summary)}\n"
        "</section>\n"
        "<section>\n"
        "<h2>Diff</h2>\n"
        f"{_render_diff(diff)}\n"
        "</section>\n"
        "<section>\n"
        "<h2>Privacy Boundary</h2>\n"
        "<p>Dashboard 只展示 evaluation summary、命令、exit code、duration 和 diff 摘要；"
        "不展示 stdout/stderr tail、benchmark 标准答案、报告正文、真实 token、secret、DSN 或真实用户输入。</p>\n"
        "</section>\n"
        "</main>\n"
        "</body>\n"
        "</html>\n"
    )


def write_dashboard(markup: str, output_html: Path) -> None:
    output_html.parent.mkdir(parents=True, exist_ok=True)
    output_html.write_text(markup, encoding="utf-8")


def write_summary(summary: dict[str, Any], output_json: Path) -> None:
    output_json.parent.mkdir(parents=True, exist_ok=True)
    with output_json.open("w", encoding="utf-8") as fh:
        json.dump(summary, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


def build_dashboard(
    *,
    summary_json: Path = DEFAULT_SUMMARY_JSON,
    diff_json: Path | None = None,
    output_html: Path = DEFAULT_OUTPUT_HTML,
) -> dict[str, Any]:
    summary = load_json(summary_json)
    diff = load_json(diff_json) if diff_json else None
    markup = render_dashboard(summary, diff)
    write_dashboard(markup, output_html)
    rendered = {
        "schemaVersion": 1,
        "generatedAt": utc_now(),
        "status": "passed",
        "summaryJson": str(summary_json),
        "diffJson": str(diff_json) if diff_json else None,
        "outputHtml": str(output_html),
        "summaryStatus": (summary.get("summary") or {}).get("status"),
        "diffStatus": (diff.get("summary") or {}).get("status") if diff else None,
        "runCount": len(summary.get("runs") or []),
        "privacyBoundary": (
            "不渲染 stdout/stderr tail、benchmark 标准答案、报告正文、真实 token、secret、DSN 或真实用户输入。"
        ),
    }
    return rendered


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="把 EvaluationRun summary/diff 渲染为静态 HTML dashboard。")
    parser.add_argument("--summary-json", type=Path, default=DEFAULT_SUMMARY_JSON, help="Evaluation summary JSON。")
    parser.add_argument("--diff-json", type=Path, default=None, help="可选 Evaluation diff JSON。")
    parser.add_argument("--output-html", type=Path, default=DEFAULT_OUTPUT_HTML, help="HTML dashboard 输出路径。")
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON, help="dashboard render summary JSON。")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        result = build_dashboard(
            summary_json=args.summary_json,
            diff_json=args.diff_json,
            output_html=args.output_html,
        )
        write_summary(result, args.output_json)
        print(json.dumps({"status": result["status"], "runCount": result["runCount"]}, ensure_ascii=False))
        return 0
    except (EvaluationDashboardError, OSError, json.JSONDecodeError) as exc:
        print(f"evaluation dashboard error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
