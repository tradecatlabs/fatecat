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
CONTRACT_PATH = ROOT / "contracts" / "fate" / "audit" / "external-validation-issue-export.json"
DEFAULT_OUTPUT_JSON = (
    ROOT / "infra" / "runtime" / "local-state" / "exports" / "audit" / "external-validation-issue-export.json"
)
DEFAULT_OUTPUT_MARKDOWN = (
    ROOT / "infra" / "runtime" / "local-state" / "exports" / "audit" / "EXTERNAL_VALIDATION_ISSUE_EXPORT.md"
)

WORK_QUEUE_KIND = "fatecat.external_validation_closure_work_queue"
CATEGORY_RUNBOOKS_KIND = "fatecat.external_validation_category_runbooks"
OPERATOR_PACKET_KIND = "fatecat.external_validation_operator_execution_packet"
CLOSURE_SUMMARY_KIND = "fatecat.external_validation_closure_evidence_summary"
OUTPUT_KIND = "fatecat.external_validation_issue_export"
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


class ExternalValidationIssueExportError(RuntimeError):
    """外部验证 issue export 生成失败。"""


def _utc_now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def _load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as fh:
        payload = json.load(fh)
    if not isinstance(payload, dict):
        raise ExternalValidationIssueExportError(f"JSON root must be object: {path}")
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
        raise ExternalValidationIssueExportError(f"{area}: sensitive-looking assignment detected")
    if RAW_URL_RE.search(rendered):
        raise ExternalValidationIssueExportError(f"{area}: raw URL detected")
    lower = rendered.lower()
    for marker in FORBIDDEN_TEXT:
        if marker in lower:
            raise ExternalValidationIssueExportError(f"{area}: forbidden marker detected: {marker}")


def _require_kind(payload: dict[str, Any], *, expected: str, area: str) -> None:
    if payload.get("kind") != expected:
        raise ExternalValidationIssueExportError(f"{area}.kind must be {expected}")


def _validate_contract(contract: dict[str, Any]) -> None:
    if contract.get("kind") != "fatecat.external_validation_issue_export_contract":
        raise ExternalValidationIssueExportError("contract.kind mismatch")
    required = set(contract.get("requiredOutputFields", []))
    for field in ("issueTemplates", "trackerImport", "issueGate"):
        if field not in required:
            raise ExternalValidationIssueExportError(f"contract missing required output field: {field}")


def _safe_slug(value: str) -> str:
    return re.sub(r"[^a-z0-9_.-]+", "-", value.lower()).strip("-") or "item"


def _domain_for_category(category: str) -> str:
    return category.split(".", 1)[0] if "." in category else category


def _stable_unique(values: list[str]) -> list[str]:
    return sorted({value for value in values if value})


def _work_items_by_id(work_queue: dict[str, Any]) -> dict[str, dict[str, Any]]:
    _require_kind(work_queue, expected=WORK_QUEUE_KIND, area="workQueue")
    items = work_queue.get("workItems")
    if not isinstance(items, list):
        raise ExternalValidationIssueExportError("workQueue.workItems must be array")
    result: dict[str, dict[str, Any]] = {}
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            raise ExternalValidationIssueExportError(f"workQueue.workItems[{index}] must be object")
        for field in ("id", "owner", "category", "priority", "status", "occurrences"):
            if item.get(field) in ("", None, []):
                raise ExternalValidationIssueExportError(f"work item {index} missing {field}")
        result[str(item["id"])] = item
    return result


def _runbooks_by_category(category_runbooks: dict[str, Any]) -> dict[str, dict[str, Any]]:
    _require_kind(category_runbooks, expected=CATEGORY_RUNBOOKS_KIND, area="categoryRunbooks")
    runbooks = category_runbooks.get("runbooks")
    if not isinstance(runbooks, list):
        raise ExternalValidationIssueExportError("categoryRunbooks.runbooks must be array")
    result: dict[str, dict[str, Any]] = {}
    for runbook in runbooks:
        if not isinstance(runbook, dict) or not runbook.get("category"):
            raise ExternalValidationIssueExportError("categoryRunbooks.runbook missing category")
        result[str(runbook["category"])] = runbook
    return result


def _operator_steps_by_category(operator_packet: dict[str, Any]) -> dict[str, dict[str, Any]]:
    _require_kind(operator_packet, expected=OPERATOR_PACKET_KIND, area="operatorPacket")
    steps = operator_packet.get("operatorSteps")
    if not isinstance(steps, list):
        raise ExternalValidationIssueExportError("operatorPacket.operatorSteps must be array")
    result: dict[str, dict[str, Any]] = {}
    for step in steps:
        if not isinstance(step, dict) or not step.get("category") or not step.get("id"):
            raise ExternalValidationIssueExportError("operatorPacket.operatorStep missing id/category")
        result[str(step["category"])] = step
    return result


def _proof_templates_by_work_item(operator_packet: dict[str, Any]) -> dict[str, dict[str, Any]]:
    proof_template = operator_packet.get("proofRefBundleTemplate")
    if not isinstance(proof_template, dict):
        raise ExternalValidationIssueExportError("operatorPacket.proofRefBundleTemplate must be object")
    proof_refs = proof_template.get("proofRefs")
    if not isinstance(proof_refs, list):
        raise ExternalValidationIssueExportError("operatorPacket.proofRefBundleTemplate.proofRefs must be array")
    result: dict[str, dict[str, Any]] = {}
    for proof_ref in proof_refs:
        if isinstance(proof_ref, dict) and proof_ref.get("workItemId"):
            result[str(proof_ref["workItemId"])] = proof_ref
    return result


def _closure_work_items_by_id(closure_summary: dict[str, Any]) -> dict[str, dict[str, Any]]:
    _require_kind(closure_summary, expected=CLOSURE_SUMMARY_KIND, area="closureEvidenceSummary")
    items = closure_summary.get("workItemSummaries")
    if not isinstance(items, list):
        raise ExternalValidationIssueExportError("closureEvidenceSummary.workItemSummaries must be array")
    result: dict[str, dict[str, Any]] = {}
    for item in items:
        if isinstance(item, dict) and item.get("id"):
            result[str(item["id"])] = item
    return result


def _pending_work_item_ids(closure_summary: dict[str, Any]) -> list[str]:
    pending = closure_summary.get("externalPending")
    if not isinstance(pending, list):
        raise ExternalValidationIssueExportError("closureEvidenceSummary.externalPending must be array")
    return sorted({str(item["workItemId"]) for item in pending if isinstance(item, dict) and item.get("workItemId")})


def _occurrence_ids(work_item: dict[str, Any]) -> list[str]:
    occurrences = work_item.get("occurrences")
    if not isinstance(occurrences, list) or not occurrences:
        raise ExternalValidationIssueExportError(f"work item {work_item['id']}: occurrences required")
    result = [str(item["id"]) for item in occurrences if isinstance(item, dict) and item.get("id")]
    if not result:
        raise ExternalValidationIssueExportError(f"work item {work_item['id']}: occurrence ids required")
    return result


def _issue_labels(*, domain: str, category: str, owner: str) -> list[str]:
    return [
        "external-validation",
        "measurement-infrastructure",
        "operator-action-required",
        f"domain.{_safe_slug(domain)}",
        f"category.{_safe_slug(category)}",
        f"owner.{_safe_slug(owner)}",
    ]


def _body_markdown(template: dict[str, Any]) -> str:
    commands = "\n".join(f"- `{command}`" for command in template["operatorCommands"])
    credentials = "\n".join(f"- `{credential}`" for credential in template["requiredCredentials"]) or "- None"
    evidence = "\n".join(f"- {item}" for item in template["requiredEvidence"]) or "- Redacted proof-ref bundle"
    blocking = "\n".join(f"- `{item}`" for item in template["blockingItems"]) or "- None"
    occurrence_ids = ", ".join(f"`{item}`" for item in template["occurrenceIds"])
    return (
        f"## External Validation Work Item\n\n"
        f"- Work item: `{template['workItemId']}`\n"
        f"- Domain: `{template['domain']}`\n"
        f"- Category: `{template['category']}`\n"
        f"- Owner: `{template['owner']}`\n"
        f"- Priority: `{template['priority']}`\n"
        f"- Occurrences: {occurrence_ids}\n\n"
        f"## Required Credentials\n\n{credentials}\n\n"
        f"## Required Evidence\n\n{evidence}\n\n"
        f"## Operator Commands\n\n{commands}\n\n"
        f"## Proof Ref Template\n\n"
        f"- Pattern: `{template['proofRefPattern']}`\n"
        f"- Artifact hash: `{template['artifactHashInstruction']}`\n"
        f"- Verification command: `{template['verificationCommand']}`\n\n"
        f"## Blocking Items\n\n{blocking}\n\n"
        f"## Closure Condition\n\n{template['closureCondition']}\n\n"
        f"## Non-Claims\n\n"
        f"- This issue does not prove live validation has passed.\n"
        f"- Do not paste token, secret, DSN, endpoint URL, chat id, user input, report body or production logs.\n"
    )


def _build_issue_template(
    *,
    work_item: dict[str, Any],
    closure_item: dict[str, Any],
    runbook: dict[str, Any],
    operator_step: dict[str, Any],
    proof_template: dict[str, Any],
) -> dict[str, Any]:
    category = str(work_item["category"])
    domain = _domain_for_category(category)
    owner = str(work_item["owner"])
    issue_id = f"external-validation-issue.{_safe_slug(str(work_item['id']))}"
    required_credentials = _stable_unique(
        [str(value) for value in work_item.get("credentialDependencies", [])]
        + [str(value) for value in runbook.get("requiredCredentials", [])]
        + [str(value) for value in operator_step.get("requiredCredentials", [])]
    )
    operator_commands = [str(command) for command in operator_step.get("operatorCommands", [])]
    template = {
        "id": issue_id,
        "title": f"[External Validation] {domain}/{category} - {owner}",
        "labels": _issue_labels(domain=domain, category=category, owner=owner),
        "assigneeHint": str(work_item.get("assignee", "")),
        "workItemId": str(work_item["id"]),
        "domain": domain,
        "category": category,
        "owner": owner,
        "priority": str(work_item["priority"]),
        "status": "operator_action_required",
        "occurrenceIds": _occurrence_ids(work_item),
        "requiredCredentials": required_credentials,
        "requiredEvidence": [str(value) for value in work_item.get("requiredEvidence", [])],
        "runbookId": str(runbook.get("id", "")),
        "operatorStepId": str(operator_step.get("id", "")),
        "operatorCommandCount": len(operator_commands),
        "operatorCommands": operator_commands,
        "operatorCommandSha256s": [str(value) for value in operator_step.get("operatorCommandSha256s", [])],
        "proofRefPattern": str(proof_template.get("proofRef", "")),
        "artifactHashInstruction": str(proof_template.get("artifactHash", "sha256:<64 lowercase hex artifact digest>")),
        "verificationCommand": str(
            proof_template.get("verificationCommand")
            or operator_step.get("verifierCommand")
            or "bash scripts/external-validation-proof-ref-gate.sh"
        ),
        "blockingItems": [str(value) for value in closure_item.get("blockingItems", [])],
        "closureCondition": str(
            runbook.get("closureCondition")
            or work_item.get("closureCondition")
            or "Submit redacted proof-ref and live proof accepted by downstream gates."
        ),
        "sourceBinding": {
            "workItemId": str(work_item["id"]),
            "occurrenceIds": _occurrence_ids(work_item),
            "runbookId": str(runbook.get("id", "")),
            "operatorStepId": str(operator_step.get("id", "")),
        },
    }
    template["bodyMarkdown"] = _body_markdown(template)
    _assert_no_sensitive(template, area=f"issue template {issue_id}")
    return template


def _render_markdown(export: dict[str, Any]) -> str:
    lines = [
        "# External Validation Issue Export",
        "",
        f"- Status: `{export['status']}`",
        f"- Issue gate: `{export['issueGate']['status']}`",
        f"- Issue templates: `{export['summary']['issueTemplates']}`",
        f"- Domains: `{export['summary']['domains']}`",
        f"- External pending: `{export['summary']['externalPending']}`",
        "",
        "## Tracker Import",
        "",
        f"- Creates issues: `{str(export['trackerImport']['createsIssues']).lower()}`",
        f"- Format: `{export['trackerImport']['format']}`",
        f"- Body file pattern: `{export['trackerImport']['bodyFilePattern']}`",
        "",
        "## Issue Index",
        "",
    ]
    for item in export["issueTemplates"]:
        labels = ", ".join(f"`{label}`" for label in item["labels"])
        lines.extend(
            [
                f"- `{item['id']}`: {item['title']}",
                f"  - Work item: `{item['workItemId']}`",
                f"  - Labels: {labels}",
                f"  - Blocking: {', '.join(item['blockingItems'])}",
            ]
        )
    lines.extend(["", "## Issue Bodies", ""])
    for item in export["issueTemplates"]:
        lines.extend(
            [
                f"### {item['id']}",
                "",
                item["bodyMarkdown"],
                "",
            ]
        )
    lines.extend(
        [
            "## Non-Claims",
            "",
            "- This export does not create issues.",
            "- This export does not execute external live checks.",
            "- This export does not mean FateCat is 100% production infrastructure.",
            "",
        ]
    )
    rendered = "\n".join(lines)
    _assert_no_sensitive(rendered, area="markdown")
    return rendered


def build_export(
    *,
    work_queue_json: Path,
    category_runbooks_json: Path,
    operator_packet_json: Path,
    closure_evidence_summary_json: Path,
    expected_commit: str | None = None,
) -> dict[str, Any]:
    for path in (work_queue_json, category_runbooks_json, operator_packet_json, closure_evidence_summary_json):
        if not path.is_file():
            raise ExternalValidationIssueExportError(f"input json missing: {path}")

    expected_commit = expected_commit or _current_commit()
    if not COMMIT_RE.match(expected_commit):
        raise ExternalValidationIssueExportError("--expected-commit must be 40 lowercase hex chars")

    contract = _load_json(CONTRACT_PATH)
    _validate_contract(contract)
    work_queue = _load_json(work_queue_json)
    category_runbooks = _load_json(category_runbooks_json)
    operator_packet = _load_json(operator_packet_json)
    closure_summary = _load_json(closure_evidence_summary_json)
    _assert_no_sensitive(work_queue, area="workQueue")
    _assert_no_sensitive(category_runbooks, area="categoryRunbooks")
    _assert_no_sensitive(operator_packet, area="operatorPacket")
    _assert_no_sensitive(closure_summary, area="closureEvidenceSummary")

    work_items = _work_items_by_id(work_queue)
    runbooks = _runbooks_by_category(category_runbooks)
    operator_steps = _operator_steps_by_category(operator_packet)
    proof_templates = _proof_templates_by_work_item(operator_packet)
    closure_items = _closure_work_items_by_id(closure_summary)
    pending_ids = _pending_work_item_ids(closure_summary)

    missing = [
        item_id
        for item_id in pending_ids
        if item_id not in work_items
        or str(work_items[item_id]["category"]) not in runbooks
        or str(work_items[item_id]["category"]) not in operator_steps
        or item_id not in closure_items
        or item_id not in proof_templates
    ]
    if missing:
        raise ExternalValidationIssueExportError(f"issue export missing source binding for work items: {missing}")

    issue_templates = [
        _build_issue_template(
            work_item=work_items[item_id],
            closure_item=closure_items[item_id],
            runbook=runbooks[str(work_items[item_id]["category"])],
            operator_step=operator_steps[str(work_items[item_id]["category"])],
            proof_template=proof_templates[item_id],
        )
        for item_id in pending_ids
    ]
    issue_gate_status = "blocked" if issue_templates else "passed"
    required_credentials = _stable_unique(
        [credential for template in issue_templates for credential in template["requiredCredentials"]]
    )
    output = {
        "schemaVersion": 1,
        "kind": OUTPUT_KIND,
        "status": OUTPUT_STATUS if issue_templates else "passed",
        "generatedAt": _utc_now(),
        "source": {
            "workQueueKind": WORK_QUEUE_KIND,
            "workQueueSha256": _sha256_file(work_queue_json),
            "categoryRunbooksKind": CATEGORY_RUNBOOKS_KIND,
            "categoryRunbooksSha256": _sha256_file(category_runbooks_json),
            "operatorPacketKind": OPERATOR_PACKET_KIND,
            "operatorPacketSha256": _sha256_file(operator_packet_json),
            "closureEvidenceSummaryKind": CLOSURE_SUMMARY_KIND,
            "closureEvidenceSummarySha256": _sha256_file(closure_evidence_summary_json),
            "commit": expected_commit,
        },
        "summary": {
            "domains": len({template["domain"] for template in issue_templates}),
            "categories": len({template["category"] for template in issue_templates}),
            "workItems": len(work_items),
            "externalPending": len(pending_ids),
            "issueTemplates": len(issue_templates),
            "requiredCredentials": len(required_credentials),
            "operatorCommands": sum(int(template["operatorCommandCount"]) for template in issue_templates),
        },
        "issueGate": {
            "status": issue_gate_status,
            "blockingItems": (
                [
                    "tracker_issue_creation_required",
                    "operator_external_credentials_required",
                    "proof_ref_bundle_required",
                    "live_proof_gate_required",
                    "third_party_audit_result_required",
                ]
                if issue_templates
                else []
            ),
            "reason": "issue export is ready, but real tracker creation, live execution and proof gates are still pending",
        },
        "trackerImport": {
            "format": "github_issue_markdown_copy_paste",
            "createsIssues": False,
            "bodyFilePattern": "external-validation-issues/{issueTemplateId}.md",
            "requiredLabels": contract["trackerPolicy"]["requiredLabels"],
            "operatorInstruction": (
                "Review each issue body, create tracker entries manually, execute runbooks with real external "
                "credentials, then submit redacted proof-ref/live proof bundles."
            ),
        },
        "issueTemplates": issue_templates,
        "privacyBoundary": contract["privacyBoundary"],
        "nonClaims": contract["nonClaims"],
    }
    _assert_no_sensitive(output, area="output")
    return output


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build redacted external validation issue export.")
    parser.add_argument("--work-queue-json", type=Path, required=True)
    parser.add_argument("--category-runbooks-json", type=Path, required=True)
    parser.add_argument("--operator-packet-json", type=Path, required=True)
    parser.add_argument("--closure-evidence-summary-json", type=Path, required=True)
    parser.add_argument("--expected-commit")
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON)
    parser.add_argument("--output-markdown", type=Path, default=DEFAULT_OUTPUT_MARKDOWN)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    export = build_export(
        work_queue_json=args.work_queue_json,
        category_runbooks_json=args.category_runbooks_json,
        operator_packet_json=args.operator_packet_json,
        closure_evidence_summary_json=args.closure_evidence_summary_json,
        expected_commit=args.expected_commit,
    )
    output_json = args.output_json
    output_markdown = args.output_markdown
    if not output_json.is_absolute():
        output_json = ROOT / output_json
    if not output_markdown.is_absolute():
        output_markdown = ROOT / output_markdown
    _write_json(output_json, export)
    _write_text(output_markdown, _render_markdown(export))
    print(
        json.dumps(
            {
                "status": export["status"],
                "kind": export["kind"],
                "issueGate": export["issueGate"]["status"],
                "issueTemplates": export["summary"]["issueTemplates"],
                "externalPending": export["summary"]["externalPending"],
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
