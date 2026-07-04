#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "contracts" / "fate" / "audit" / "external-validation-tracker-issue-evidence-template.json"
DEFAULT_OUTPUT_JSON = (
    ROOT
    / "infra"
    / "runtime"
    / "local-state"
    / "exports"
    / "audit"
    / "external-validation-tracker-issue-evidence-template.json"
)
DEFAULT_OUTPUT_MARKDOWN = (
    ROOT
    / "infra"
    / "runtime"
    / "local-state"
    / "exports"
    / "audit"
    / "EXTERNAL_VALIDATION_TRACKER_ISSUE_EVIDENCE_TEMPLATE.md"
)

TRACKER_IMPORT_KIND = "fatecat.external_validation_tracker_import_package"
OUTPUT_KIND = "fatecat.external_validation_tracker_issue_evidence_bundle_template"
TARGET_EVIDENCE_KIND = "fatecat.external_validation_tracker_issue_evidence_bundle"
PRIVACY_BOUNDARY = "redacted_no_secret_values"
REQUIRED_LABELS = ["external-validation", "measurement-infrastructure", "operator-action-required"]

SENSITIVE_RE = re.compile(
    r"(token\s*=|secret\s*=|password\s*=|passwd\s*=|DATABASE_URL\s*=|DB_DSN\s*=|"
    r"api[_-]?key\s*=|private[_-]?key|BEGIN (?:RSA|OPENSSH|PRIVATE)|authorization\s*:)",
    re.IGNORECASE,
)
RAW_URL_RE = re.compile(r"https?://", re.IGNORECASE)
COMMIT_RE = re.compile(r"^[a-f0-9]{40}$")
SHA256_RE = re.compile(r"^[a-f0-9]{64}$")
FORBIDDEN_TEXT = ("placeholder proof", "fake proof", "dummy proof", "localhost proof")


class ExternalValidationTrackerIssueEvidenceTemplateError(RuntimeError):
    """外部验证 tracker issue evidence template 生成失败。"""


def _utc_now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def _load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as fh:
        payload = json.load(fh)
    if not isinstance(payload, dict):
        raise ExternalValidationTrackerIssueEvidenceTemplateError(f"JSON root must be object: {path}")
    return payload


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8")


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
        raise ExternalValidationTrackerIssueEvidenceTemplateError(f"{area}: sensitive-looking assignment detected")
    if RAW_URL_RE.search(rendered):
        raise ExternalValidationTrackerIssueEvidenceTemplateError(f"{area}: raw URL detected")
    lower = rendered.lower()
    for marker in FORBIDDEN_TEXT:
        if marker in lower:
            raise ExternalValidationTrackerIssueEvidenceTemplateError(f"{area}: forbidden marker detected: {marker}")


def _validate_contract(contract: dict[str, Any]) -> None:
    if contract.get("kind") != "fatecat.external_validation_tracker_issue_evidence_template_contract":
        raise ExternalValidationTrackerIssueEvidenceTemplateError("contract.kind mismatch")
    required = set(contract.get("requiredOutputFields", []))
    for field in ("templateGate", "templatePolicy", "issueEvidenceItems", "bundleSkeleton"):
        if field not in required:
            raise ExternalValidationTrackerIssueEvidenceTemplateError(
                f"contract missing required output field: {field}"
            )


def _validate_tracker_import_package(package: dict[str, Any]) -> None:
    if package.get("kind") != TRACKER_IMPORT_KIND:
        raise ExternalValidationTrackerIssueEvidenceTemplateError(
            f"tracker import package kind must be {TRACKER_IMPORT_KIND}"
        )
    files = package.get("files")
    commands = package.get("commands")
    if not isinstance(files, list) or not isinstance(commands, list):
        raise ExternalValidationTrackerIssueEvidenceTemplateError(
            "tracker import package files/commands must be arrays"
        )
    for index, item in enumerate(files):
        if not isinstance(item, dict):
            raise ExternalValidationTrackerIssueEvidenceTemplateError(f"file entry {index} must be object")
        for field in ("id", "workItemId", "category", "owner", "path", "sha256"):
            if item.get(field) in ("", None):
                raise ExternalValidationTrackerIssueEvidenceTemplateError(f"file entry {index} missing {field}")
        if not SHA256_RE.match(str(item["sha256"])):
            raise ExternalValidationTrackerIssueEvidenceTemplateError(f"file entry {index} sha256 invalid")
    for index, command in enumerate(commands):
        if not isinstance(command, dict):
            raise ExternalValidationTrackerIssueEvidenceTemplateError(f"command entry {index} must be object")
        for field in ("issueTemplateId", "workItemId", "bodyFile", "sha256"):
            if command.get(field) in ("", None):
                raise ExternalValidationTrackerIssueEvidenceTemplateError(f"command entry {index} missing {field}")


def _template_items(package: dict[str, Any]) -> list[dict[str, Any]]:
    command_by_work_item = {str(command["workItemId"]): command for command in package["commands"]}
    items: list[dict[str, Any]] = []
    for file_item in package["files"]:
        work_item_id = str(file_item["workItemId"])
        command = command_by_work_item.get(work_item_id)
        if command is None:
            raise ExternalValidationTrackerIssueEvidenceTemplateError(
                f"missing tracker import command for workItemId={work_item_id}"
            )
        body_file = str(command.get("bodyFile", ""))
        if body_file != str(file_item["path"]):
            raise ExternalValidationTrackerIssueEvidenceTemplateError(
                f"body file mismatch for workItemId={work_item_id}"
            )
        items.append(
            {
                "workItemId": work_item_id,
                "issueTemplateId": str(command["issueTemplateId"]),
                "category": str(file_item["category"]),
                "owner": str(file_item["owner"]),
                "bodyFile": str(file_item["path"]),
                "bodySha256": str(file_item["sha256"]),
                "requiredLabels": REQUIRED_LABELS,
                "fillableFields": {
                    "trackerIssueRef": "",
                    "titleSha256": "",
                    "artifactSha256": "",
                    "createdAt": "",
                    "createdByRole": "operator",
                },
                "redactionStatus": PRIVACY_BOUNDARY,
            }
        )
    return items


def _bundle_skeleton(
    *,
    items: list[dict[str, Any]],
    package_sha256: str,
    expected_commit: str,
) -> dict[str, Any]:
    return {
        "schemaVersion": 1,
        "kind": TARGET_EVIDENCE_KIND,
        "source": {
            "trackerImportPackageKind": TRACKER_IMPORT_KIND,
            "trackerImportPackageSha256": package_sha256,
            "commit": expected_commit,
        },
        "issues": [
            {
                "workItemId": item["workItemId"],
                "issueTemplateId": item["issueTemplateId"],
                "trackerIssueRef": "",
                "titleSha256": "",
                "bodySha256": item["bodySha256"],
                "artifactSha256": "",
                "labels": item["requiredLabels"],
                "createdAt": "",
                "createdByRole": "operator",
                "redactionStatus": PRIVACY_BOUNDARY,
            }
            for item in items
        ],
    }


def build_template(
    *,
    tracker_import_package_json: Path,
    expected_commit: str | None = None,
) -> dict[str, Any]:
    if not tracker_import_package_json.is_file():
        raise ExternalValidationTrackerIssueEvidenceTemplateError(
            f"tracker import package json missing: {tracker_import_package_json}"
        )
    expected_commit = expected_commit or _current_commit()
    if not COMMIT_RE.match(expected_commit):
        raise ExternalValidationTrackerIssueEvidenceTemplateError("--expected-commit must be 40 lowercase hex chars")

    contract = _load_json(CONTRACT_PATH)
    _validate_contract(contract)
    package = _load_json(tracker_import_package_json)
    _assert_no_sensitive(package, area="tracker import package")
    _validate_tracker_import_package(package)
    package_commit = str(package.get("source", {}).get("commit", ""))
    if package_commit and package_commit != expected_commit:
        raise ExternalValidationTrackerIssueEvidenceTemplateError(
            f"tracker import package commit {package_commit} does not match expected commit {expected_commit}"
        )
    package_sha256 = _sha256_file(tracker_import_package_json)
    items = _template_items(package)
    bundle_skeleton = _bundle_skeleton(
        items=items,
        package_sha256=package_sha256,
        expected_commit=expected_commit,
    )
    template = {
        "schemaVersion": 1,
        "kind": OUTPUT_KIND,
        "status": "operator_action_required",
        "generatedAt": _utc_now(),
        "source": {
            "trackerImportPackageKind": TRACKER_IMPORT_KIND,
            "trackerImportPackageSha256": package_sha256,
            "trackerImportPackageCommit": package_commit or expected_commit,
            "commit": expected_commit,
        },
        "summary": {
            "workItems": len(items),
            "requiredIssueRefs": len(items),
            "requiredArtifactHashes": len(items),
            "readyToSubmitToGate": False,
        },
        "templateGate": {
            "status": "operator_action_required",
            "blockingItems": [
                "tracker_issue_creation_required",
                "tracker_issue_ref_fill_required",
                "artifact_sha256_fill_required",
            ],
            "reason": "template is ready, but operator must create tracker issues and fill redacted evidence values",
        },
        "templatePolicy": contract["templatePolicy"],
        "issueEvidenceItems": items,
        "bundleSkeleton": bundle_skeleton,
        "privacyBoundary": contract["privacyBoundary"],
        "nonClaims": contract["nonClaims"],
    }
    _assert_no_sensitive(template, area="tracker issue evidence template")
    return template


def _render_markdown(template: dict[str, Any]) -> str:
    lines = [
        "# External Validation Tracker Issue Evidence Template",
        "",
        f"- Status: `{template['status']}`",
        f"- Template gate: `{template['templateGate']['status']}`",
        f"- Work items: `{template['summary']['workItems']}`",
        f"- Ready to submit to gate: `{str(template['summary']['readyToSubmitToGate']).lower()}`",
        "",
        "## Operator Fill Fields",
        "",
        "- `trackerIssueRef`: sanitized format `github:owner/repo#123`.",
        "- `artifactSha256`: sha256 digest of the redacted issue creation evidence artifact.",
        "- `titleSha256`: sha256 digest of the created issue title when available.",
        "- `createdAt`: issue creation timestamp from the authorized tracker session.",
        "- `createdByRole`: role name only, normally `operator`.",
        "",
        "## Work Items",
        "",
    ]
    for item in template["issueEvidenceItems"]:
        lines.extend(
            [
                f"### {item['workItemId']}",
                "",
                f"- Issue template: `{item['issueTemplateId']}`",
                f"- Category: `{item['category']}`",
                f"- Owner: `{item['owner']}`",
                f"- Body sha256: `{item['bodySha256']}`",
                "",
            ]
        )
    lines.extend(
        [
            "## Bundle Skeleton",
            "",
            "```json",
            json.dumps(template["bundleSkeleton"], ensure_ascii=False, indent=2, sort_keys=True),
            "```",
            "",
            "## Non-Claims",
            "",
        ]
    )
    for claim in template["nonClaims"]:
        lines.append(f"- {claim}")
    rendered = "\n".join(lines) + "\n"
    _assert_no_sensitive(rendered, area="markdown")
    return rendered


def write_template(*, template: dict[str, Any], output_json: Path, output_markdown: Path) -> None:
    _write_json(output_json, template)
    _write_text(output_markdown, _render_markdown(template))


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build redacted tracker issue evidence bundle template.")
    parser.add_argument("--tracker-import-package-json", type=Path, required=True)
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON)
    parser.add_argument("--output-markdown", type=Path, default=DEFAULT_OUTPUT_MARKDOWN)
    parser.add_argument("--expected-commit")
    return parser.parse_args(argv)


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    template = build_template(
        tracker_import_package_json=_resolve(args.tracker_import_package_json),
        expected_commit=args.expected_commit,
    )
    output_json = _resolve(args.output_json)
    output_markdown = _resolve(args.output_markdown)
    write_template(template=template, output_json=output_json, output_markdown=output_markdown)
    print(
        json.dumps(
            {
                "status": template["status"],
                "kind": template["kind"],
                "templateGate": template["templateGate"]["status"],
                "workItems": template["summary"]["workItems"],
                "readyToSubmitToGate": template["summary"]["readyToSubmitToGate"],
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
