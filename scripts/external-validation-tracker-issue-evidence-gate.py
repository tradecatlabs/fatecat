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
CONTRACT_PATH = ROOT / "contracts" / "fate" / "audit" / "external-validation-tracker-issue-evidence.json"
DEFAULT_OUTPUT_JSON = (
    ROOT
    / "infra"
    / "runtime"
    / "local-state"
    / "exports"
    / "audit"
    / "external-validation-tracker-issue-evidence-gate.json"
)

TRACKER_IMPORT_KIND = "fatecat.external_validation_tracker_import_package"
EVIDENCE_BUNDLE_KIND = "fatecat.external_validation_tracker_issue_evidence_bundle"
OUTPUT_KIND = "fatecat.external_validation_tracker_issue_evidence_gate"
PRIVACY_BOUNDARY = "redacted_no_secret_values"

SENSITIVE_RE = re.compile(
    r"(token\s*=|secret\s*=|password\s*=|passwd\s*=|DATABASE_URL\s*=|DB_DSN\s*=|"
    r"api[_-]?key\s*=|private[_-]?key|BEGIN (?:RSA|OPENSSH|PRIVATE)|authorization\s*:)",
    re.IGNORECASE,
)
RAW_URL_RE = re.compile(r"https?://", re.IGNORECASE)
COMMIT_RE = re.compile(r"^[a-f0-9]{40}$")
SHA256_RE = re.compile(r"^[a-f0-9]{64}$")
TRACKER_REF_RE = re.compile(r"^github:[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+#[1-9][0-9]*$")
FORBIDDEN_TEXT = ("placeholder proof", "fake proof", "dummy proof", "localhost proof")
REQUIRED_LABELS = {"external-validation", "measurement-infrastructure", "operator-action-required"}


class ExternalValidationTrackerIssueEvidenceGateError(RuntimeError):
    """外部验证 tracker issue evidence gate 失败。"""


def _utc_now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def _load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as fh:
        payload = json.load(fh)
    if not isinstance(payload, dict):
        raise ExternalValidationTrackerIssueEvidenceGateError(f"JSON root must be object: {path}")
    return payload


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


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
        raise ExternalValidationTrackerIssueEvidenceGateError(f"{area}: sensitive-looking assignment detected")
    if RAW_URL_RE.search(rendered):
        raise ExternalValidationTrackerIssueEvidenceGateError(f"{area}: raw URL detected")
    lower = rendered.lower()
    for marker in FORBIDDEN_TEXT:
        if marker in lower:
            raise ExternalValidationTrackerIssueEvidenceGateError(f"{area}: forbidden marker detected: {marker}")


def _validate_contract(contract: dict[str, Any]) -> None:
    if contract.get("kind") != "fatecat.external_validation_tracker_issue_evidence_contract":
        raise ExternalValidationTrackerIssueEvidenceGateError("contract.kind mismatch")
    required = set(contract.get("requiredOutputFields", []))
    for field in ("issueCreation", "issueEvidenceGate", "shipGate", "acceptedIssues", "rejectedIssues"):
        if field not in required:
            raise ExternalValidationTrackerIssueEvidenceGateError(f"contract missing required output field: {field}")


def _validate_tracker_import_package(package: dict[str, Any]) -> None:
    if package.get("kind") != TRACKER_IMPORT_KIND:
        raise ExternalValidationTrackerIssueEvidenceGateError(
            f"tracker import package kind must be {TRACKER_IMPORT_KIND}"
        )
    files = package.get("files")
    commands = package.get("commands")
    if not isinstance(files, list) or not isinstance(commands, list):
        raise ExternalValidationTrackerIssueEvidenceGateError("tracker import package files/commands must be arrays")
    for index, item in enumerate(files):
        if not isinstance(item, dict):
            raise ExternalValidationTrackerIssueEvidenceGateError(f"file entry {index} must be object")
        for field in ("id", "workItemId", "path", "sha256"):
            if item.get(field) in ("", None):
                raise ExternalValidationTrackerIssueEvidenceGateError(f"file entry {index} missing {field}")
        if not SHA256_RE.match(str(item["sha256"])):
            raise ExternalValidationTrackerIssueEvidenceGateError(f"file entry {index} sha256 invalid")
    for index, command in enumerate(commands):
        if not isinstance(command, dict):
            raise ExternalValidationTrackerIssueEvidenceGateError(f"command entry {index} must be object")
        for field in ("issueTemplateId", "workItemId", "bodyFile", "sha256"):
            if command.get(field) in ("", None):
                raise ExternalValidationTrackerIssueEvidenceGateError(f"command entry {index} missing {field}")


def _validate_evidence_bundle_source(
    *,
    evidence_bundle: dict[str, Any],
    package_sha256: str,
    expected_commit: str,
) -> None:
    if evidence_bundle.get("kind") != EVIDENCE_BUNDLE_KIND:
        raise ExternalValidationTrackerIssueEvidenceGateError(f"evidence bundle kind must be {EVIDENCE_BUNDLE_KIND}")
    source = evidence_bundle.get("source")
    if not isinstance(source, dict):
        raise ExternalValidationTrackerIssueEvidenceGateError("evidence bundle source must be object")
    if source.get("trackerImportPackageSha256") != package_sha256:
        raise ExternalValidationTrackerIssueEvidenceGateError("evidence bundle package sha256 mismatch")
    source_commit = str(source.get("commit", ""))
    if source_commit != expected_commit:
        raise ExternalValidationTrackerIssueEvidenceGateError(
            f"evidence bundle commit {source_commit} does not match expected commit {expected_commit}"
        )


def _issue_maps(package: dict[str, Any]) -> tuple[dict[str, dict[str, Any]], dict[str, str]]:
    file_by_work_item = {str(item["workItemId"]): item for item in package.get("files", [])}
    template_by_work_item = {
        str(command["workItemId"]): str(command["issueTemplateId"]) for command in package["commands"]
    }
    return file_by_work_item, template_by_work_item


def _reject(issue: dict[str, Any], reason: str) -> dict[str, Any]:
    return {
        "workItemId": str(issue.get("workItemId", "")),
        "issueTemplateId": str(issue.get("issueTemplateId", "")),
        "reason": reason,
    }


def _validate_issue(
    issue: dict[str, Any],
    *,
    file_by_work_item: dict[str, dict[str, Any]],
    template_by_work_item: dict[str, str],
    seen_work_items: set[str],
) -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
    for field in ("workItemId", "issueTemplateId", "trackerIssueRef", "bodySha256", "labels", "artifactSha256"):
        if issue.get(field) in ("", None, []):
            return None, _reject(issue, f"missing_{field}")

    work_item_id = str(issue["workItemId"])
    if work_item_id in seen_work_items:
        return None, _reject(issue, "duplicate_work_item")
    if work_item_id not in file_by_work_item:
        return None, _reject(issue, "unknown_work_item")
    if str(issue["issueTemplateId"]) != template_by_work_item.get(work_item_id):
        return None, _reject(issue, "issue_template_mismatch")
    if not TRACKER_REF_RE.match(str(issue["trackerIssueRef"])):
        return None, _reject(issue, "tracker_issue_ref_invalid")
    if str(issue["bodySha256"]) != str(file_by_work_item[work_item_id]["sha256"]):
        return None, _reject(issue, "body_sha256_mismatch")
    labels = issue.get("labels")
    if not isinstance(labels, list) or not REQUIRED_LABELS.issubset({str(label) for label in labels}):
        return None, _reject(issue, "required_labels_missing")
    artifact_sha256 = str(issue["artifactSha256"])
    if not SHA256_RE.match(artifact_sha256):
        return None, _reject(issue, "artifact_sha256_invalid")
    title_sha256 = str(issue.get("titleSha256", ""))
    if title_sha256 and not SHA256_RE.match(title_sha256):
        return None, _reject(issue, "title_sha256_invalid")
    if str(issue.get("redactionStatus", "")) != PRIVACY_BOUNDARY:
        return None, _reject(issue, "redaction_status_invalid")

    seen_work_items.add(work_item_id)
    accepted = {
        "workItemId": work_item_id,
        "issueTemplateId": str(issue["issueTemplateId"]),
        "trackerIssueRef": str(issue["trackerIssueRef"]),
        "bodySha256": str(issue["bodySha256"]),
        "artifactSha256": artifact_sha256,
        "titleSha256": title_sha256 or None,
        "labels": sorted({str(label) for label in labels}),
        "createdAt": str(issue.get("createdAt", "")),
        "createdByRole": str(issue.get("createdByRole", "operator")),
        "redactionStatus": str(issue["redactionStatus"]),
    }
    return accepted, None


def build_gate(
    *,
    tracker_import_package_json: Path,
    issue_evidence_json: Path | None = None,
    expected_commit: str | None = None,
) -> dict[str, Any]:
    if not tracker_import_package_json.is_file():
        raise ExternalValidationTrackerIssueEvidenceGateError(
            f"tracker import package json missing: {tracker_import_package_json}"
        )
    expected_commit = expected_commit or _current_commit()
    if not COMMIT_RE.match(expected_commit):
        raise ExternalValidationTrackerIssueEvidenceGateError("--expected-commit must be 40 lowercase hex chars")

    contract = _load_json(CONTRACT_PATH)
    _validate_contract(contract)
    package = _load_json(tracker_import_package_json)
    _assert_no_sensitive(package, area="tracker import package")
    _validate_tracker_import_package(package)
    package_commit = str(package.get("source", {}).get("commit", ""))
    if package_commit and package_commit != expected_commit:
        raise ExternalValidationTrackerIssueEvidenceGateError(
            f"tracker import package commit {package_commit} does not match expected commit {expected_commit}"
        )

    file_by_work_item, template_by_work_item = _issue_maps(package)
    package_sha256 = _sha256_file(tracker_import_package_json)
    accepted_issues: list[dict[str, Any]] = []
    rejected_issues: list[dict[str, Any]] = []
    evidence_supplied = issue_evidence_json is not None
    evidence_sha256 = None
    evidence_kind = None

    if issue_evidence_json is not None:
        if not issue_evidence_json.is_file():
            raise ExternalValidationTrackerIssueEvidenceGateError(f"issue evidence json missing: {issue_evidence_json}")
        evidence_sha256 = _sha256_file(issue_evidence_json)
        evidence_bundle = _load_json(issue_evidence_json)
        _assert_no_sensitive(evidence_bundle, area="issue evidence bundle")
        _validate_evidence_bundle_source(
            evidence_bundle=evidence_bundle,
            package_sha256=package_sha256,
            expected_commit=expected_commit,
        )
        evidence_kind = str(evidence_bundle["kind"])
        issues = evidence_bundle.get("issues")
        if not isinstance(issues, list):
            raise ExternalValidationTrackerIssueEvidenceGateError("evidence bundle issues must be array")
        seen_work_items: set[str] = set()
        for issue in issues:
            if not isinstance(issue, dict):
                raise ExternalValidationTrackerIssueEvidenceGateError("evidence bundle issue entry must be object")
            accepted, rejected = _validate_issue(
                issue,
                file_by_work_item=file_by_work_item,
                template_by_work_item=template_by_work_item,
                seen_work_items=seen_work_items,
            )
            if accepted is not None:
                accepted_issues.append(accepted)
            if rejected is not None:
                rejected_issues.append(rejected)

    accepted_work_items = {issue["workItemId"] for issue in accepted_issues}
    pending_work_items = sorted(
        work_item_id for work_item_id in file_by_work_item if work_item_id not in accepted_work_items
    )
    issue_evidence_gate_status = (
        "passed" if evidence_supplied and not pending_work_items and not rejected_issues else "blocked"
    )
    if not evidence_supplied:
        issue_creation_status = "external_connectivity_pending"
    elif issue_evidence_gate_status == "passed":
        issue_creation_status = "accepted"
    else:
        issue_creation_status = "partial_evidence_pending"

    gate = {
        "schemaVersion": 1,
        "kind": OUTPUT_KIND,
        "status": issue_creation_status,
        "generatedAt": _utc_now(),
        "source": {
            "trackerImportPackageKind": TRACKER_IMPORT_KIND,
            "trackerImportPackageSha256": package_sha256,
            "trackerImportPackageCommit": package_commit or expected_commit,
            "issueEvidenceBundleKind": evidence_kind,
            "issueEvidenceBundleSha256": evidence_sha256,
            "commit": expected_commit,
        },
        "summary": {
            "workItems": len(file_by_work_item),
            "requiredIssueEvidence": len(file_by_work_item),
            "acceptedIssues": len(accepted_issues),
            "rejectedIssues": len(rejected_issues),
            "pendingIssues": len(pending_work_items),
            "issueCreationStatus": issue_creation_status,
        },
        "issueCreation": {
            "tracker": "github_issues",
            "createsIssues": False,
            "executesCommands": False,
            "evidenceSupplied": evidence_supplied,
            "status": issue_creation_status,
            "requiredAction": (
                "Operator must create tracker issues from the import package and submit a redacted "
                "tracker issue evidence bundle."
                if not evidence_supplied
                else "Resolve rejected or pending tracker issue evidence before live proof closure."
            ),
        },
        "issueEvidenceGate": {
            "status": issue_evidence_gate_status,
            "blockingItems": (
                []
                if issue_evidence_gate_status == "passed"
                else [
                    "tracker_issue_creation_evidence_required",
                    "all_work_items_must_bind_to_tracker_issue_refs",
                    "body_hash_binding_required",
                ]
            ),
            "reason": (
                "all tracker issue evidence is structurally accepted"
                if issue_evidence_gate_status == "passed"
                else "tracker issue creation evidence is missing, partial or rejected"
            ),
        },
        "shipGate": {
            "status": "blocked",
            "blockingItems": [
                "external_validation_live_proof_gate_required",
                "measurement_infrastructure_certification_required",
                "third_party_audit_result_required",
            ],
            "reason": "tracker issue evidence does not prove external live validation or independent audit closure",
        },
        "acceptedIssues": accepted_issues,
        "rejectedIssues": rejected_issues,
        "pendingWorkItems": pending_work_items,
        "privacyBoundary": contract["privacyBoundary"],
        "nonClaims": contract["nonClaims"],
    }
    _assert_no_sensitive(gate, area="tracker issue evidence gate")
    return gate


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate redacted external validation tracker issue evidence.")
    parser.add_argument("--tracker-import-package-json", type=Path, required=True)
    parser.add_argument("--issue-evidence-json", type=Path)
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON)
    parser.add_argument("--expected-commit")
    return parser.parse_args(argv)


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    gate = build_gate(
        tracker_import_package_json=_resolve(args.tracker_import_package_json),
        issue_evidence_json=_resolve(args.issue_evidence_json) if args.issue_evidence_json else None,
        expected_commit=args.expected_commit,
    )
    output_json = _resolve(args.output_json)
    _write_json(output_json, gate)
    print(
        json.dumps(
            {
                "status": gate["status"],
                "kind": gate["kind"],
                "issueEvidenceGate": gate["issueEvidenceGate"]["status"],
                "shipGate": gate["shipGate"]["status"],
                "acceptedIssues": gate["summary"]["acceptedIssues"],
                "pendingIssues": gate["summary"]["pendingIssues"],
                "rejectedIssues": gate["summary"]["rejectedIssues"],
                "outputJson": str(output_json),
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
