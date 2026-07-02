#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = REPO_ROOT / "contracts" / "fate" / "audit" / "dry-run.json"
DEFAULT_OUTPUT_DIR = REPO_ROOT / "infra" / "runtime" / "local-state" / "exports" / "audit-dry-run"
JSON_FILENAME = "audit-dry-run.json"
MARKDOWN_FILENAME = "AUDIT_DRY_RUN.md"


class AuditDryRunError(RuntimeError):
    """审计交接包 dry-run 失败。"""


@dataclass(frozen=True)
class Check:
    id: str
    status: str
    severity: str
    evidence: str


def utc_now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def load_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise AuditDryRunError(f"缺少文件: {path}") from exc
    except json.JSONDecodeError as exc:
        raise AuditDryRunError(f"JSON 格式错误: {path}: {exc}") from exc


def repo_relative(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO_ROOT.resolve()).as_posix()
    except ValueError:
        return str(path)


def check_status(condition: bool) -> str:
    return "passed" if condition else "failed"


def required_fields_check(bundle: dict[str, Any], required_fields: list[str]) -> Check:
    missing = [field for field in required_fields if field not in bundle]
    return Check(
        id="json_required_fields",
        status=check_status(not missing),
        severity="blocker",
        evidence="missing=" + json.dumps(missing, ensure_ascii=False),
    )


def markdown_sections_check(markdown: str, required_sections: list[str]) -> Check:
    missing = [section for section in required_sections if f"## {section}" not in markdown]
    return Check(
        id="markdown_required_sections",
        status=check_status(not missing),
        severity="blocker",
        evidence="missing=" + json.dumps(missing, ensure_ascii=False),
    )


def pending_count_check(bundle: dict[str, Any]) -> Check:
    declared = bundle.get("pendingExternalValidationCount")
    listed = len(bundle.get("pendingExternalValidations", []))
    return Check(
        id="pending_count_consistency",
        status=check_status(isinstance(declared, int) and declared == listed),
        severity="blocker",
        evidence=f"declared={declared} listed={listed}",
    )


def pending_risk_check(bundle: dict[str, Any]) -> Check:
    pending_count = int(bundle.get("pendingExternalValidationCount") or 0)
    risk_ids = {str(item.get("id")) for item in bundle.get("riskRegister", []) if isinstance(item, dict)}
    required = pending_count > 0
    present = "risk.external_validations_pending" in risk_ids
    return Check(
        id="pending_risk_registered",
        status=check_status((not required) or present),
        severity="blocker",
        evidence=f"pendingExternalValidationCount={pending_count} riskPresent={present}",
    )


def final_conclusion_check(markdown: str, pending_count: int) -> Check:
    conclusion = markdown.split("## Final Conclusion", 1)[-1].lower() if "## Final Conclusion" in markdown else ""
    blocks = ("remain blocked" in conclusion) or ("blocked" in conclusion and pending_count > 0)
    return Check(
        id="final_conclusion_blocks_live_claim",
        status=check_status(pending_count == 0 or blocks),
        severity="blocker",
        evidence=f"pendingExternalValidationCount={pending_count} blockedLanguage={blocks}",
    )


def sensitive_assignment_check(serialized: str, patterns: list[str]) -> Check:
    lowered = serialized.lower()
    found = [pattern for pattern in patterns if pattern.lower() in lowered]
    return Check(
        id="sensitive_assignment_absent",
        status=check_status(not found),
        severity="blocker",
        evidence="found=" + json.dumps(found, ensure_ascii=False),
    )


def false_claim_check(serialized: str, phrases: list[str]) -> Check:
    lowered = serialized.lower()
    found = [phrase for phrase in phrases if phrase.lower() in lowered]
    return Check(
        id="false_live_claim_absent",
        status=check_status(not found),
        severity="blocker",
        evidence="found=" + json.dumps(found, ensure_ascii=False),
    )


def bundle_kind_check(bundle: dict[str, Any]) -> Check:
    return Check(
        id="bundle_kind",
        status=check_status(bundle.get("kind") == "fatecat.audit_handoff_bundle"),
        severity="blocker",
        evidence=f"kind={bundle.get('kind')}",
    )


def calculate_ship_gate(bundle: dict[str, Any], checks: list[Check]) -> dict[str, Any]:
    reasons: list[str] = []
    pending_count = int(bundle.get("pendingExternalValidationCount") or 0)
    if pending_count > 0:
        reasons.append(f"pendingExternalValidationCount={pending_count}")
    repo_status = bundle.get("repository", {}).get("status", {})
    if isinstance(repo_status, dict) and not repo_status.get("clean", True):
        reasons.append(f"bundleRepositoryDirtyCount={repo_status.get('dirtyCount')}")
    failed_checks = [check.id for check in checks if check.status != "passed" and check.severity == "blocker"]
    if failed_checks:
        reasons.append("failedChecks=" + ",".join(failed_checks))
    return {
        "status": "blocked" if reasons else "passed",
        "reasons": reasons,
        "pendingExternalValidationCount": pending_count,
    }


def markdown_table(rows: list[list[Any]]) -> str:
    if not rows:
        return ""
    header = rows[0]
    lines = [
        "| " + " | ".join(str(item) for item in header) + " |",
        "| " + " | ".join("---" for _ in header) + " |",
    ]
    for row in rows[1:]:
        lines.append("| " + " | ".join(str(item).replace("\n", " ") for item in row) + " |")
    return "\n".join(lines)


def render_markdown(report: dict[str, Any]) -> str:
    check_rows = [["Check", "Status", "Severity", "Evidence"]]
    for item in report["checks"]:
        check_rows.append([item["id"], item["status"], item["severity"], item["evidence"]])
    reason_rows = [["Reason"]]
    for reason in report["shipGate"]["reasons"] or ["-"]:
        reason_rows.append([reason])
    sections = [
        "# FateCat Audit Dry Run",
        "",
        "## Summary",
        "",
        f"- Generated At: `{report['generatedAt']}`",
        f"- Status: `{report['status']}`",
        f"- Ship Gate: `{report['shipGate']['status']}`",
        f"- Bundle JSON: `{report['inputs']['bundleJson']}`",
        f"- Bundle Markdown: `{report['inputs']['bundleMarkdown']}`",
        "",
        "## Checks",
        "",
        markdown_table(check_rows),
        "",
        "## Ship Gate",
        "",
        markdown_table(reason_rows),
        "",
        "## Non Claims",
        "",
        "- Dry-run passed does not mean third-party audit passed.",
        "- Dry-run passed does not prove production API, Bot, OIDC, SIEM, monitoring, developer portal or sandbox live status.",
        "- Ship gate remains blocked while external validations are pending.",
        "",
        "## Final Conclusion",
        "",
        "The audit handoff bundle is ready for local dry-run review when status is passed. Production, live and third-party audit claims remain blocked until external evidence exists.",
        "",
    ]
    return "\n".join(sections)


def build_report(*, bundle_json: Path, bundle_markdown: Path, output_dir: Path) -> dict[str, Any]:
    contract = load_json(CONTRACT_PATH)
    bundle = load_json(bundle_json)
    try:
        markdown = bundle_markdown.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise AuditDryRunError(f"缺少文件: {bundle_markdown}") from exc
    checks = [
        bundle_kind_check(bundle),
        required_fields_check(bundle, contract["requiredBundleJsonFields"]),
        markdown_sections_check(markdown, contract["requiredBundleMarkdownSections"]),
        pending_count_check(bundle),
        pending_risk_check(bundle),
        final_conclusion_check(markdown, int(bundle.get("pendingExternalValidationCount") or 0)),
    ]
    serialized = json.dumps(bundle, ensure_ascii=False).lower() + markdown.lower()
    checks.append(sensitive_assignment_check(serialized, contract["forbiddenSensitiveAssignmentPatterns"]))
    checks.append(false_claim_check(serialized, contract["forbiddenFalseClaimPhrases"]))
    check_payloads = [check.__dict__ for check in checks]
    failed = [check for check in checks if check.status != "passed" and check.severity == "blocker"]
    json_path = output_dir / JSON_FILENAME
    markdown_path = output_dir / MARKDOWN_FILENAME
    report = {
        "schemaVersion": 1,
        "kind": "fatecat.audit_handoff_dry_run",
        "generatedAt": utc_now(),
        "status": "failed" if failed else "passed",
        "contract": repo_relative(CONTRACT_PATH),
        "inputs": {
            "bundleJson": str(bundle_json),
            "bundleMarkdown": str(bundle_markdown),
            "bundleKind": bundle.get("kind"),
            "bundleCommit": bundle.get("repository", {}).get("commit"),
        },
        "checks": check_payloads,
        "summary": {
            "passed": len([check for check in checks if check.status == "passed"]),
            "failed": len(failed),
            "total": len(checks),
        },
        "shipGate": calculate_ship_gate(bundle, checks),
        "outputs": {
            "jsonPath": str(json_path),
            "markdownPath": str(markdown_path),
        },
        "privacyBoundary": contract["privacyBoundary"],
        "nonClaims": contract["nonClaims"],
    }
    dry_run_markdown = render_markdown(report)
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    markdown_path.write_text(dry_run_markdown, encoding="utf-8")
    return report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="执行 FateCat 审计交接包 dry-run 预检。")
    parser.add_argument("--bundle-json", type=Path, required=True, help="audit-handoff.json path")
    parser.add_argument("--bundle-markdown", type=Path, required=True, help="AUDIT_HANDOFF.md path")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR, help="audit dry-run output directory")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        report = build_report(
            bundle_json=args.bundle_json,
            bundle_markdown=args.bundle_markdown,
            output_dir=args.output_dir,
        )
        print(
            json.dumps(
                {
                    "status": report["status"],
                    "shipGate": report["shipGate"]["status"],
                    "jsonPath": report["outputs"]["jsonPath"],
                    "markdownPath": report["outputs"]["markdownPath"],
                },
                ensure_ascii=False,
            )
        )
        return 0 if report["status"] == "passed" else 1
    except AuditDryRunError as exc:
        print(f"audit dry-run error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
