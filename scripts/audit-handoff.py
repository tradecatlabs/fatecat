#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = REPO_ROOT / "contracts" / "fate" / "audit" / "handoff.json"
DEFAULT_OUTPUT_DIR = REPO_ROOT / "infra" / "runtime" / "local-state" / "exports" / "audit-handoff"
PENDING_PHRASE = "外部连通验证待执行"
JSON_FILENAME = "audit-handoff.json"
MARKDOWN_FILENAME = "AUDIT_HANDOFF.md"
REDACTED_REMOTE = "[redacted-remote]"


class AuditHandoffError(RuntimeError):
    """审计交接包生成失败。"""


def utc_now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def run_capture(args: list[str], *, timeout_seconds: int = 30) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        timeout=timeout_seconds,
        check=False,
    )


def git_value(*args: str) -> str:
    result = run_capture(["git", *args], timeout_seconds=10)
    if result.returncode != 0:
        return ""
    return result.stdout.strip()


def load_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise AuditHandoffError(f"缺少文件: {path}") from exc
    except json.JSONDecodeError as exc:
        raise AuditHandoffError(f"JSON 格式错误: {path}: {exc}") from exc


def repo_relative(path: Path) -> str:
    return path.resolve().relative_to(REPO_ROOT.resolve()).as_posix()


def safe_remote(value: str) -> str:
    if not value:
        return ""
    lowered = value.lower()
    if "@" in value.split("://", 1)[-1] or "credential" in lowered:
        return REDACTED_REMOTE
    return value


def git_status() -> dict[str, Any]:
    result = run_capture(["git", "status", "--porcelain"], timeout_seconds=10)
    lines = [line for line in result.stdout.splitlines() if line.strip()] if result.returncode == 0 else []
    untracked = [line for line in lines if line.startswith("??")]
    return {
        "clean": len(lines) == 0,
        "dirtyCount": len(lines),
        "untrackedCount": len(untracked),
    }


def collect_repository_state() -> dict[str, Any]:
    return {
        "branch": git_value("rev-parse", "--abbrev-ref", "HEAD"),
        "commit": git_value("rev-parse", "--verify", "HEAD"),
        "shortCommit": git_value("rev-parse", "--short", "HEAD"),
        "lastCommit": git_value("log", "-1", "--oneline"),
        "remote": safe_remote(git_value("remote", "get-url", "origin")),
        "status": git_status(),
    }


def parse_task_index() -> dict[str, Any]:
    path = REPO_ROOT / "governance" / "tasks" / "INDEX.md"
    rows: list[dict[str, str]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("| ") or "---" in line or "Task ID" in line:
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 6 or not cells[0].isdigit():
            continue
        rows.append(
            {
                "id": cells[0],
                "slug": cells[1],
                "status": cells[2],
                "priority": cells[3],
                "objective": cells[4],
                "path": cells[5],
            }
        )
    status_counts: dict[str, int] = {}
    for row in rows:
        status_counts[row["status"]] = status_counts.get(row["status"], 0) + 1
    return {
        "path": "governance/tasks/INDEX.md",
        "total": len(rows),
        "statusCounts": status_counts,
        "latest": rows[-8:],
    }


def pending_occurrence_id(path: str, line: int, excerpt: str) -> str:
    raw = f"{path}:{line}:{excerpt}".encode()
    return hashlib.sha256(raw).hexdigest()[:16]


def collect_pending_external_validations() -> list[dict[str, Any]]:
    result = run_capture(["git", "grep", "-n", "-I", PENDING_PHRASE], timeout_seconds=30)
    if result.returncode not in {0, 1}:
        raise AuditHandoffError(f"git grep failed: {result.stderr.strip()}")
    items: list[dict[str, Any]] = []
    seen: set[tuple[str, int, str]] = set()
    for raw_line in result.stdout.splitlines():
        parts = raw_line.split(":", 2)
        if len(parts) != 3:
            continue
        path, line_text, excerpt = parts
        try:
            line_no = int(line_text)
        except ValueError:
            continue
        key = (path, line_no, excerpt.strip())
        seen.add(key)
        items.append(
            {
                "id": pending_occurrence_id(path, line_no, excerpt.strip()),
                "path": path,
                "line": line_no,
                "phrase": PENDING_PHRASE,
                "excerpt": excerpt.strip(),
            }
        )
    for item in collect_untracked_pending_occurrences(seen):
        items.append(item)
    return items


def collect_untracked_pending_occurrences(seen: set[tuple[str, int, str]]) -> list[dict[str, Any]]:
    result = run_capture(["git", "ls-files", "--others", "--exclude-standard"], timeout_seconds=30)
    if result.returncode != 0:
        raise AuditHandoffError(f"git ls-files failed: {result.stderr.strip()}")
    items: list[dict[str, Any]] = []
    for path_text in result.stdout.splitlines():
        if not path_text or path_text.startswith(("infra/runtime/", ".venv/", "tools/reference-repos/")):
            continue
        path = REPO_ROOT / path_text
        if not path.is_file() or path.stat().st_size > 1_000_000:
            continue
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            continue
        for index, line in enumerate(lines, start=1):
            if PENDING_PHRASE not in line:
                continue
            excerpt = line.strip()
            key = (path_text, index, excerpt)
            if key in seen:
                continue
            seen.add(key)
            items.append(
                {
                    "id": pending_occurrence_id(path_text, index, excerpt),
                    "path": path_text,
                    "line": index,
                    "phrase": PENDING_PHRASE,
                    "excerpt": excerpt,
                    "source": "untracked_non_ignored",
                }
            )
    return items


def read_optional_local_ci_summary(path_text: str | None, current_commit: str) -> dict[str, Any]:
    if not path_text:
        return {
            "provided": False,
            "status": "not_supplied",
            "message": "local-ci summary not supplied to audit handoff generator",
        }
    path = Path(path_text)
    if not path.is_absolute():
        path = REPO_ROOT / path
    payload = load_json(path)
    checks: list[str] = []
    if payload.get("kind") != "fatecat.local_ci_summary":
        checks.append("kind must be fatecat.local_ci_summary")
    if payload.get("status") != "passed":
        checks.append("status must be passed")
    if payload.get("commit") != current_commit:
        checks.append("summary commit must match current HEAD")
    return {
        "provided": True,
        "path": str(path),
        "status": "passed" if not checks else "failed",
        "profile": payload.get("profile"),
        "commit": payload.get("commit"),
        "finishedAt": payload.get("finishedAt"),
        "artifacts": payload.get("artifacts", {}),
        "errors": checks,
    }


def collect_remote_acceptance(current_commit: str) -> dict[str, Any]:
    if shutil.which("gh") is None:
        return {"checked": False, "status": "gh_unavailable", "message": "GitHub CLI not available"}
    result = run_capture(
        [
            "gh",
            "run",
            "list",
            "--workflow",
            "acceptance.yml",
            "--limit",
            "20",
            "--json",
            "databaseId,headSha,status,conclusion,url,createdAt",
        ],
        timeout_seconds=30,
    )
    if result.returncode != 0:
        return {"checked": False, "status": "gh_failed", "message": result.stderr.strip()[:300]}
    runs = json.loads(result.stdout or "[]")
    for item in runs:
        if item.get("headSha") == current_commit:
            return {
                "checked": True,
                "status": item.get("status"),
                "conclusion": item.get("conclusion") or "",
                "url": item.get("url"),
                "databaseId": item.get("databaseId"),
                "createdAt": item.get("createdAt"),
            }
    return {
        "checked": True,
        "status": "not_found",
        "message": "No acceptance.yml run found for current commit in latest 20 runs",
    }


def contract_paths() -> list[str]:
    return [
        "contracts/fate/audit/handoff.json",
        "contracts/fate/delivery/release-gate.json",
        "contracts/fate/delivery/registry.json",
        "contracts/fate/security/registry.json",
        "contracts/fate/security/externalization-evidence-contract.json",
        "contracts/fate/observability/registry.json",
        "contracts/fate/observability/slo-evidence-contract.json",
        "contracts/fate/developer/developer-platform.json",
        "contracts/fate/evaluations/registry.json",
    ]


def collect_code_asset_index() -> list[dict[str, Any]]:
    assets: list[dict[str, Any]] = []
    for path_text in contract_paths():
        path = REPO_ROOT / path_text
        assets.append({"path": path_text, "exists": path.is_file(), "type": "contract"})
    for path_text in [
        "scripts/audit-handoff.py",
        "scripts/audit-handoff.sh",
        "scripts/local-ci.sh",
        "tests/regression/test_audit_handoff.py",
        "docs/reference-materials/roadmap/测算基础设施100%实现计划.md",
    ]:
        path = REPO_ROOT / path_text
        assets.append({"path": path_text, "exists": path.is_file(), "type": "implementation"})
    return assets


def build_risk_register(
    pending_count: int, repo_state: dict[str, Any], remote_acceptance: dict[str, Any]
) -> list[dict[str, Any]]:
    risks = [
        {
            "id": "risk.external_validations_pending",
            "severity": "blocking_for_100_percent_live_claim",
            "status": "open",
            "evidence": f"{pending_count} tracked + untracked non-ignored occurrences of {PENDING_PHRASE}",
            "mitigation": "Keep live claims blocked until each external validation has real evidence.",
        },
        {
            "id": "risk.audit_bundle_not_third_party_review",
            "severity": "non_blocking_for_local_baseline",
            "status": "open",
            "evidence": "Generator produces handoff evidence; it does not replace third-party audit.",
            "mitigation": "Give generated Markdown/JSON to external auditor for independent review.",
        },
    ]
    if not repo_state["status"]["clean"]:
        risks.append(
            {
                "id": "risk.worktree_dirty",
                "severity": "blocking_for_ship_claim",
                "status": "open",
                "evidence": f"dirtyCount={repo_state['status']['dirtyCount']}",
                "mitigation": "Commit or intentionally exclude local changes before final ship evidence.",
            }
        )
    if remote_acceptance.get("conclusion") != "success":
        risks.append(
            {
                "id": "risk.remote_acceptance_not_success",
                "severity": "blocking_for_remote_ci_claim",
                "status": "open",
                "evidence": json.dumps(remote_acceptance, ensure_ascii=False),
                "mitigation": "Run GitHub Actions acceptance for current commit and record success URL.",
            }
        )
    return risks


def validate_contract(contract: dict[str, Any]) -> None:
    if contract.get("schemaVersion") != 1:
        raise AuditHandoffError("handoff contract schemaVersion must be 1")
    if contract.get("kind") != "fatecat.audit_handoff_contract":
        raise AuditHandoffError("handoff contract kind mismatch")
    policy = contract.get("pendingExternalValidationPolicy", {})
    if policy.get("requiredPhrase") != PENDING_PHRASE:
        raise AuditHandoffError("handoff contract pending phrase mismatch")


def build_bundle(*, output_dir: Path, local_ci_summary: str | None, include_github: bool) -> dict[str, Any]:
    contract = load_json(CONTRACT_PATH)
    validate_contract(contract)
    repo_state = collect_repository_state()
    pending_items = collect_pending_external_validations()
    remote_acceptance = (
        collect_remote_acceptance(repo_state["commit"])
        if include_github
        else {"checked": False, "status": "not_requested", "message": "Run with --include-github to query gh."}
    )
    local_ci = read_optional_local_ci_summary(local_ci_summary, repo_state["commit"])
    markdown_path = output_dir / MARKDOWN_FILENAME
    json_path = output_dir / JSON_FILENAME
    bundle = {
        "schemaVersion": 1,
        "kind": "fatecat.audit_handoff_bundle",
        "generatedAt": utc_now(),
        "status": "passed",
        "contract": repo_relative(CONTRACT_PATH),
        "repository": repo_state,
        "taskIndex": parse_task_index(),
        "evidence": {
            "localCiSummary": local_ci,
            "remoteAcceptance": remote_acceptance,
            "codeAndAssetIndex": collect_code_asset_index(),
            "markdownPath": str(markdown_path),
            "jsonPath": str(json_path),
        },
        "pendingExternalValidationPolicy": contract["pendingExternalValidationPolicy"],
        "pendingExternalValidationCount": len(pending_items),
        "pendingExternalValidations": pending_items,
        "riskRegister": build_risk_register(len(pending_items), repo_state, remote_acceptance),
        "verification": {
            "pendingCoverage": "complete",
            "pendingCoverageCommand": f"git grep -n -I {PENDING_PHRASE} && git ls-files --others --exclude-standard",
            "requiredMarkdownSections": contract["requiredMarkdownSections"],
            "privacyBoundary": contract["privacyBoundary"],
            "nonClaims": contract["nonClaims"],
        },
    }
    markdown = render_markdown(bundle)
    validate_bundle(bundle, markdown)
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(bundle, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    markdown_path.write_text(markdown, encoding="utf-8")
    return bundle


def markdown_table(rows: list[list[Any]]) -> str:
    if not rows:
        return ""
    header = rows[0]
    body = rows[1:]
    lines = [
        "| " + " | ".join(str(item) for item in header) + " |",
        "| " + " | ".join("---" for _ in header) + " |",
    ]
    for row in body:
        lines.append("| " + " | ".join(str(item).replace("\n", " ") for item in row) + " |")
    return "\n".join(lines)


def render_markdown(bundle: dict[str, Any]) -> str:
    repo = bundle["repository"]
    task_index = bundle["taskIndex"]
    evidence = bundle["evidence"]
    pending = bundle["pendingExternalValidations"]
    risks = bundle["riskRegister"]

    task_rows = [["ID", "Slug", "Status", "Priority"]]
    for item in task_index["latest"]:
        task_rows.append([item["id"], item["slug"], item["status"], item["priority"]])

    asset_rows = [["Path", "Type", "Exists"]]
    for item in evidence["codeAndAssetIndex"]:
        asset_rows.append([item["path"], item["type"], item["exists"]])

    pending_rows = [["Path", "Line", "Excerpt"]]
    for item in pending[:80]:
        pending_rows.append([item["path"], item["line"], item["excerpt"]])

    risk_rows = [["ID", "Severity", "Status", "Evidence"]]
    for item in risks:
        risk_rows.append([item["id"], item["severity"], item["status"], item["evidence"]])

    sections = [
        "# FateCat Audit Handoff",
        "",
        "## Latest Status",
        "",
        f"- Generated At: `{bundle['generatedAt']}`",
        f"- Branch: `{repo['branch']}`",
        f"- Commit: `{repo['commit']}`",
        f"- Clean Worktree: `{repo['status']['clean']}`",
        f"- Task Total: `{task_index['total']}`",
        f"- Task Status Counts: `{json.dumps(task_index['statusCounts'], ensure_ascii=False)}`",
        "",
        "## Delivery Evidence",
        "",
        f"- Local CI Summary: `{evidence['localCiSummary']['status']}`",
        f"- Remote Acceptance: `{json.dumps(evidence['remoteAcceptance'], ensure_ascii=False)}`",
        f"- JSON Bundle: `{evidence['jsonPath']}`",
        f"- Markdown Bundle: `{evidence['markdownPath']}`",
        "",
        "## Code And Asset Index",
        "",
        markdown_table(asset_rows),
        "",
        "## Pending External Validations",
        "",
        f"- Required phrase: `{PENDING_PHRASE}`",
        f"- Count: `{bundle['pendingExternalValidationCount']}`",
        "- Policy: every tracked and untracked non-ignored occurrence is listed in JSON with path, line and excerpt.",
        "",
        markdown_table(pending_rows),
        "",
        "## Risk Register",
        "",
        markdown_table(risk_rows),
        "",
        "## Verification",
        "",
        f"- Pending coverage command: `{bundle['verification']['pendingCoverageCommand']}`",
        "- This bundle proves repository-local audit handoff generation only.",
        "- It does not prove production API, Bot, OIDC, SIEM, monitoring, developer portal or sandbox live connectivity.",
        "",
        "## Final Conclusion",
        "",
        "Current branch has a reproducible audit handoff bundle. Production reuse and 100% infrastructure claims remain blocked until all pending external validations have real evidence.",
        "",
        "## Recent Task Index",
        "",
        markdown_table(task_rows),
        "",
    ]
    return "\n".join(sections)


def validate_bundle(bundle: dict[str, Any], markdown: str) -> None:
    if bundle.get("kind") != "fatecat.audit_handoff_bundle":
        raise AuditHandoffError("bundle kind mismatch")
    if bundle.get("pendingExternalValidationCount") != len(bundle.get("pendingExternalValidations", [])):
        raise AuditHandoffError("pending external validation count mismatch")
    contract = load_json(CONTRACT_PATH)
    for section in contract["requiredMarkdownSections"]:
        if f"## {section}" not in markdown:
            raise AuditHandoffError(f"Markdown missing section: {section}")
    serialized = json.dumps(bundle, ensure_ascii=False).lower() + markdown.lower()
    for forbidden in ("token=", "secret=", "password=", "passwd=", "private_key="):
        if forbidden in serialized:
            raise AuditHandoffError(f"audit handoff contains forbidden sensitive assignment pattern: {forbidden}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="生成 FateCat 第三方审计交接包。")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR, help="audit handoff output directory")
    parser.add_argument("--local-ci-summary", default=None, help="optional local-ci summary.json for evidence linking")
    parser.add_argument("--include-github", action="store_true", help="query gh for current commit acceptance run")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        bundle = build_bundle(
            output_dir=args.output_dir,
            local_ci_summary=args.local_ci_summary,
            include_github=args.include_github,
        )
        print(
            json.dumps(
                {
                    "status": bundle["status"],
                    "pendingExternalValidationCount": bundle["pendingExternalValidationCount"],
                    "jsonPath": bundle["evidence"]["jsonPath"],
                    "markdownPath": bundle["evidence"]["markdownPath"],
                },
                ensure_ascii=False,
            )
        )
        return 0
    except AuditHandoffError as exc:
        print(f"audit handoff error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
