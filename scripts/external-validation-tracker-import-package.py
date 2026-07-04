#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shlex
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "contracts" / "fate" / "audit" / "external-validation-tracker-import-package.json"
DEFAULT_PACKAGE_DIR = (
    ROOT / "infra" / "runtime" / "local-state" / "exports" / "audit" / "external-validation-tracker-import-package"
)
DEFAULT_OUTPUT_JSON = (
    ROOT / "infra" / "runtime" / "local-state" / "exports" / "audit" / "external-validation-tracker-import-package.json"
)
DEFAULT_OUTPUT_MARKDOWN = (
    ROOT / "infra" / "runtime" / "local-state" / "exports" / "audit" / "EXTERNAL_VALIDATION_TRACKER_IMPORT_PACKAGE.md"
)

ISSUE_EXPORT_KIND = "fatecat.external_validation_issue_export"
OUTPUT_KIND = "fatecat.external_validation_tracker_import_package"
OUTPUT_STATUS = "operator_action_required"
PRIVACY_BOUNDARY = "redacted_no_secret_values"

SENSITIVE_RE = re.compile(
    r"(token\s*=|secret\s*=|password\s*=|passwd\s*=|DATABASE_URL\s*=|DB_DSN\s*=|"
    r"api[_-]?key\s*=|private[_-]?key|BEGIN (?:RSA|OPENSSH|PRIVATE)|authorization\s*:)",
    re.IGNORECASE,
)
RAW_URL_RE = re.compile(r"https?://", re.IGNORECASE)
COMMIT_RE = re.compile(r"^[a-f0-9]{40}$")
FORBIDDEN_TEXT = ("placeholder proof", "fake proof", "dummy proof", "localhost proof")


class ExternalValidationTrackerImportPackageError(RuntimeError):
    """外部验证 tracker import package 生成失败。"""


def _utc_now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def _load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as fh:
        payload = json.load(fh)
    if not isinstance(payload, dict):
        raise ExternalValidationTrackerImportPackageError(f"JSON root must be object: {path}")
    return payload


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8")


def _sha256_bytes(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _current_commit() -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    return result.stdout.strip()


def _render(payload: Any) -> str:
    return json.dumps(payload, ensure_ascii=False, sort_keys=True) if not isinstance(payload, str) else payload


def _assert_no_sensitive(payload: Any, *, area: str) -> None:
    rendered = _render(payload)
    if SENSITIVE_RE.search(rendered):
        raise ExternalValidationTrackerImportPackageError(f"{area}: sensitive-looking assignment detected")
    if RAW_URL_RE.search(rendered):
        raise ExternalValidationTrackerImportPackageError(f"{area}: raw URL detected")
    lower = rendered.lower()
    for marker in FORBIDDEN_TEXT:
        if marker in lower:
            raise ExternalValidationTrackerImportPackageError(f"{area}: forbidden marker detected: {marker}")


def _validate_contract(contract: dict[str, Any]) -> None:
    if contract.get("kind") != "fatecat.external_validation_tracker_import_package_contract":
        raise ExternalValidationTrackerImportPackageError("contract.kind mismatch")
    required = set(contract.get("requiredOutputFields", []))
    for field in ("files", "commands", "trackerImport", "packageGate"):
        if field not in required:
            raise ExternalValidationTrackerImportPackageError(f"contract missing required output field: {field}")


def _safe_slug(value: str) -> str:
    return re.sub(r"[^a-z0-9_.-]+", "-", value.lower()).strip("-") or "item"


def _quote_labels(labels: list[str]) -> str:
    return " ".join(f"--label {shlex.quote(label)}" for label in labels)


def _body_file_for(template: dict[str, Any]) -> str:
    return f"issues/{_safe_slug(str(template['id']))}.md"


def _command_for(template: dict[str, Any], *, body_file: str) -> str:
    labels = [str(label) for label in template.get("labels", [])]
    label_args = _quote_labels(labels)
    return (
        f"gh issue create --title {shlex.quote(str(template['title']))} "
        f"--body-file {shlex.quote(body_file)} {label_args}"
    ).strip()


def _issue_templates(issue_export: dict[str, Any]) -> list[dict[str, Any]]:
    if issue_export.get("kind") != ISSUE_EXPORT_KIND:
        raise ExternalValidationTrackerImportPackageError(f"issueExport.kind must be {ISSUE_EXPORT_KIND}")
    templates = issue_export.get("issueTemplates")
    if not isinstance(templates, list):
        raise ExternalValidationTrackerImportPackageError("issueExport.issueTemplates must be array")
    result: list[dict[str, Any]] = []
    for index, template in enumerate(templates):
        if not isinstance(template, dict):
            raise ExternalValidationTrackerImportPackageError(f"issue template {index} must be object")
        for field in ("id", "title", "labels", "workItemId", "category", "owner", "bodyMarkdown"):
            if template.get(field) in ("", None, []):
                raise ExternalValidationTrackerImportPackageError(f"issue template {index} missing {field}")
        labels = template.get("labels")
        if not isinstance(labels, list) or "external-validation" not in labels:
            raise ExternalValidationTrackerImportPackageError(
                f"issue template {index} missing external-validation label"
            )
        result.append(template)
    return result


def _prepare_package_dir(package_dir: Path) -> None:
    issues_dir = package_dir / "issues"
    issues_dir.mkdir(parents=True, exist_ok=True)
    for stale in issues_dir.glob("*.md"):
        stale.unlink()


def _render_commands(commands: list[dict[str, Any]]) -> str:
    lines = [
        "# External Validation Tracker Import Commands",
        "",
        "# Dry-run command text only. Review each issue body before executing manually.",
        "# This file is generated as evidence; this generator does not run gh or create issues.",
        "",
    ]
    for command in commands:
        lines.extend(
            [
                f"# {command['id']}",
                f"# workItemId: {command['workItemId']}",
                str(command["command"]),
                "",
            ]
        )
    rendered = "\n".join(lines)
    _assert_no_sensitive(rendered, area="command file")
    return rendered


def _render_markdown(package: dict[str, Any]) -> str:
    lines = [
        "# External Validation Tracker Import Package",
        "",
        f"- Status: `{package['status']}`",
        f"- Package gate: `{package['packageGate']['status']}`",
        f"- Issue files: `{package['summary']['issueFiles']}`",
        f"- Command count: `{package['summary']['commands']}`",
        f"- Creates issues: `{str(package['trackerImport']['createsIssues']).lower()}`",
        f"- Executes commands: `{str(package['trackerImport']['executesCommands']).lower()}`",
        "",
        "## Files",
        "",
    ]
    for item in package["files"]:
        lines.append(f"- `{item['path']}` sha256 `{item['sha256']}`")
    lines.extend(["", "## Commands", ""])
    for command in package["commands"]:
        lines.extend(
            [
                f"### {command['id']}",
                "",
                f"- Work item: `{command['workItemId']}`",
                f"- Body file: `{command['bodyFile']}`",
                f"- Command sha256: `{command['sha256']}`",
                "",
                "```bash",
                command["command"],
                "```",
                "",
            ]
        )
    lines.extend(
        [
            "## Non-Claims",
            "",
            "- This package does not create issues.",
            "- This package does not execute external live checks.",
            "- This package does not mean FateCat is 100% production infrastructure.",
            "",
        ]
    )
    rendered = "\n".join(lines)
    _assert_no_sensitive(rendered, area="markdown")
    return rendered


def build_package(
    *,
    issue_export_json: Path,
    package_dir: Path,
    expected_commit: str | None = None,
) -> dict[str, Any]:
    if not issue_export_json.is_file():
        raise ExternalValidationTrackerImportPackageError(f"issue export json missing: {issue_export_json}")
    expected_commit = expected_commit or _current_commit()
    if not COMMIT_RE.match(expected_commit):
        raise ExternalValidationTrackerImportPackageError("--expected-commit must be 40 lowercase hex chars")

    contract = _load_json(CONTRACT_PATH)
    _validate_contract(contract)
    issue_export = _load_json(issue_export_json)
    _assert_no_sensitive(issue_export, area="issueExport")
    templates = _issue_templates(issue_export)
    issue_export_commit = str(issue_export.get("source", {}).get("commit", ""))
    if issue_export_commit and issue_export_commit != expected_commit:
        raise ExternalValidationTrackerImportPackageError(
            f"issue export commit {issue_export_commit} does not match expected commit {expected_commit}"
        )

    _prepare_package_dir(package_dir)
    files: list[dict[str, Any]] = []
    commands: list[dict[str, Any]] = []
    for template in templates:
        body = str(template["bodyMarkdown"])
        _assert_no_sensitive(body, area=f"issue body {template['id']}")
        body_file = _body_file_for(template)
        body_path = package_dir / body_file
        _write_text(body_path, body)
        file_sha256 = _sha256_file(body_path)
        command = _command_for(template, body_file=body_file)
        _assert_no_sensitive(command, area=f"tracker command {template['id']}")
        files.append(
            {
                "id": str(template["id"]),
                "workItemId": str(template["workItemId"]),
                "category": str(template["category"]),
                "owner": str(template["owner"]),
                "path": body_file,
                "sha256": file_sha256,
            }
        )
        commands.append(
            {
                "id": f"tracker-import-command.{_safe_slug(str(template['id']))}",
                "issueTemplateId": str(template["id"]),
                "workItemId": str(template["workItemId"]),
                "bodyFile": body_file,
                "command": command,
                "sha256": _sha256_bytes(command),
                "execution": "manual_review_required",
            }
        )

    command_file = "gh-issue-create-commands.txt"
    _write_text(package_dir / command_file, _render_commands(commands))
    command_file_sha256 = _sha256_file(package_dir / command_file)
    issue_gate_status = "blocked" if templates else "passed"
    package = {
        "schemaVersion": 1,
        "kind": OUTPUT_KIND,
        "status": OUTPUT_STATUS if templates else "passed",
        "generatedAt": _utc_now(),
        "source": {
            "issueExportKind": ISSUE_EXPORT_KIND,
            "issueExportSha256": _sha256_file(issue_export_json),
            "issueExportCommit": issue_export_commit or expected_commit,
            "commit": expected_commit,
        },
        "summary": {
            "issueTemplates": len(templates),
            "issueFiles": len(files),
            "commands": len(commands),
            "externalPending": int(issue_export.get("summary", {}).get("externalPending", len(templates))),
        },
        "packageGate": {
            "status": issue_gate_status,
            "blockingItems": (
                [
                    "tracker_issue_creation_required",
                    "operator_external_credentials_required",
                    "proof_ref_bundle_required",
                    "live_proof_gate_required",
                    "third_party_audit_result_required",
                ]
                if templates
                else []
            ),
            "reason": "tracker import package is ready, but real issue creation and live proof closure are still pending",
        },
        "trackerImport": {
            "tracker": "github_issues",
            "format": "github_cli_command_text_and_markdown_body_files",
            "createsIssues": False,
            "executesCommands": False,
            "packageDir": str(package_dir),
            "commandFile": command_file,
            "commandFileSha256": command_file_sha256,
            "operatorInstruction": (
                "Review issue bodies and command text, then manually create tracker issues in an approved session. "
                "After real external validation, submit redacted proof-ref/live proof bundles."
            ),
        },
        "files": files,
        "commands": commands,
        "privacyBoundary": contract["privacyBoundary"],
        "nonClaims": contract["nonClaims"],
    }
    _assert_no_sensitive(package, area="package")
    return package


def write_package(
    *,
    package: dict[str, Any],
    package_dir: Path,
    output_json: Path,
    output_markdown: Path,
) -> None:
    markdown = _render_markdown(package)
    _write_json(package_dir / "import-manifest.json", package)
    _write_text(package_dir / "README.md", markdown)
    _write_json(output_json, package)
    _write_text(output_markdown, markdown)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build redacted external validation tracker import package.")
    parser.add_argument("--issue-export-json", type=Path, required=True)
    parser.add_argument("--package-dir", type=Path, default=DEFAULT_PACKAGE_DIR)
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON)
    parser.add_argument("--output-markdown", type=Path, default=DEFAULT_OUTPUT_MARKDOWN)
    parser.add_argument("--expected-commit")
    return parser.parse_args(argv)


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    package_dir = _resolve(args.package_dir)
    output_json = _resolve(args.output_json)
    output_markdown = _resolve(args.output_markdown)
    package = build_package(
        issue_export_json=_resolve(args.issue_export_json),
        package_dir=package_dir,
        expected_commit=args.expected_commit,
    )
    write_package(
        package=package,
        package_dir=package_dir,
        output_json=output_json,
        output_markdown=output_markdown,
    )
    print(
        json.dumps(
            {
                "status": package["status"],
                "kind": package["kind"],
                "packageGate": package["packageGate"]["status"],
                "issueFiles": package["summary"]["issueFiles"],
                "commands": package["summary"]["commands"],
                "packageDir": str(package_dir),
                "outputJson": str(output_json),
                "outputMarkdown": str(output_markdown),
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
