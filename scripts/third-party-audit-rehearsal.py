#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "contracts" / "fate" / "audit" / "third-party-audit-rehearsal.json"
DEFAULT_OUTPUT_JSON = (
    ROOT / "infra" / "runtime" / "local-state" / "exports" / "audit-rehearsal" / "third-party-audit-rehearsal.json"
)
DEFAULT_OUTPUT_MARKDOWN = (
    ROOT / "infra" / "runtime" / "local-state" / "exports" / "audit-rehearsal" / "THIRD_PARTY_AUDIT_REHEARSAL.md"
)

OUTPUT_KIND = "fatecat.third_party_audit_rehearsal"
SENSITIVE_RE = re.compile(
    r"(token\s*=|secret\s*=|password\s*=|passwd\s*=|DATABASE_URL\s*=|DB_DSN\s*=|"
    r"api[_-]?key\s*=|private[_-]?key|BEGIN (?:RSA|OPENSSH|PRIVATE)|authorization\s*:)",
    re.IGNORECASE,
)
RAW_URL_RE = re.compile(r"https?://", re.IGNORECASE)


class ThirdPartyAuditRehearsalError(RuntimeError):
    """第三方审计预演包生成失败。"""


def _utc_now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def _load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as fh:
        payload = json.load(fh)
    if not isinstance(payload, dict):
        raise ThirdPartyAuditRehearsalError(f"JSON root must be object: {path}")
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


def _require_file(path: Path, *, label: str) -> None:
    if not path.is_file():
        raise ThirdPartyAuditRehearsalError(f"{label} missing: {path}")


def _require_kind(payload: dict[str, Any], *, expected: str, label: str) -> None:
    if payload.get("kind") != expected:
        raise ThirdPartyAuditRehearsalError(f"{label}.kind must be {expected}")


def _gate_status(payload: dict[str, Any], gate_name: str) -> str:
    gate = payload.get(gate_name)
    if isinstance(gate, dict):
        return str(gate.get("status", "missing"))
    return "missing"


def _status(payload: dict[str, Any]) -> str:
    return str(payload.get("status", "missing"))


def _is_passed(status: str) -> bool:
    return status in {"pass", "passed"}


def _input_item(label: str, path: Path, payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": label,
        "kind": str(payload.get("kind", "")),
        "status": str(payload.get("status", "")),
        "path": str(path),
        "sha256": _sha256_file(path),
    }


def _sanitize_external_pending(closure_summary: dict[str, Any]) -> list[dict[str, Any]]:
    pending = closure_summary.get("externalPending", [])
    if not isinstance(pending, list):
        raise ThirdPartyAuditRehearsalError("closureEvidenceSummary.externalPending must be array")
    result: list[dict[str, Any]] = []
    for item in pending:
        if not isinstance(item, dict):
            continue
        result.append(
            {
                "workItemId": str(item.get("workItemId", "")),
                "domain": str(item.get("domain", "")),
                "category": str(item.get("category", "")),
                "owner": str(item.get("owner", "")),
                "blockingItems": [str(reason) for reason in item.get("blockingItems", [])],
                "nextAction": str(item.get("nextAction", "execute_category_runbook_and_submit_redacted_proof_ref")),
            }
        )
    return result


def _build_evidence_index(
    *,
    current_audit_bundle_json: Path,
    audit_dry_run_json: Path,
    current_release_proof_json: Path,
    certification_json: Path,
    closure_evidence_summary_json: Path,
    current_audit_bundle: dict[str, Any],
    audit_dry_run: dict[str, Any],
    current_release_proof: dict[str, Any],
    certification: dict[str, Any],
    closure_summary: dict[str, Any],
) -> list[dict[str, Any]]:
    release_git = current_release_proof.get("git", {})
    audit_git = current_audit_bundle.get("git", {})
    certification_gate = certification.get("certificationGate", {})
    closure_summary_counts = closure_summary.get("summary", {})
    return [
        {
            **_input_item("current_audit_bundle", current_audit_bundle_json, current_audit_bundle),
            "gate": _gate_status(current_audit_bundle, "auditGate"),
            "commit": str(audit_git.get("commit", "")) if isinstance(audit_git, dict) else "",
            "clean": bool(audit_git.get("clean", False)) if isinstance(audit_git, dict) else False,
            "pendingExternalValidationCount": int(current_audit_bundle.get("pendingExternalValidationCount") or 0),
        },
        {
            **_input_item("audit_dry_run", audit_dry_run_json, audit_dry_run),
            "gate": _gate_status(audit_dry_run, "shipGate"),
        },
        {
            **_input_item("current_release_proof", current_release_proof_json, current_release_proof),
            "gate": _gate_status(current_release_proof, "proofGate"),
            "commit": str(release_git.get("commit", "")) if isinstance(release_git, dict) else "",
            "mode": str(current_release_proof.get("mode", "")),
        },
        {
            **_input_item("measurement_infrastructure_certification", certification_json, certification),
            "gate": "passed" if certification_gate.get("canClaim100Percent") is True else "blocked",
            "canClaim100Percent": certification_gate.get("canClaim100Percent") is True,
            "domains": len(certification.get("domains", []) or []),
            "externalPending": len(certification.get("externalPending", []) or []),
            "blockingItems": len(certification.get("blockingItems", []) or []),
        },
        {
            **_input_item(
                "external_validation_closure_evidence_summary", closure_evidence_summary_json, closure_summary
            ),
            "gate": _gate_status(closure_summary, "closureGate"),
            "domains": int(closure_summary_counts.get("domains") or 0),
            "workItems": int(closure_summary_counts.get("workItems") or 0),
            "externalPending": int(closure_summary_counts.get("externalPending") or 0),
        },
    ]


def _checklist_item(item_id: str, title: str, status: str, evidence: str, action: str) -> dict[str, str]:
    return {
        "id": item_id,
        "title": title,
        "status": status,
        "evidence": evidence,
        "nextAction": action,
    }


def _build_checklist(
    *,
    current_audit_bundle: dict[str, Any],
    audit_dry_run: dict[str, Any],
    current_release_proof: dict[str, Any],
    certification: dict[str, Any],
    closure_summary: dict[str, Any],
    external_pending: list[dict[str, Any]],
) -> list[dict[str, str]]:
    audit_git = current_audit_bundle.get("git", {})
    clean = isinstance(audit_git, dict) and audit_git.get("clean") is True
    audit_gate = _gate_status(current_audit_bundle, "auditGate")
    dry_run_gate = _gate_status(audit_dry_run, "shipGate")
    release_gate = _gate_status(current_release_proof, "proofGate")
    certification_gate = certification.get("certificationGate", {})
    can_claim = certification_gate.get("canClaim100Percent") is True
    closure_gate = _gate_status(closure_summary, "closureGate")
    return [
        _checklist_item(
            "git.current_commit_clean",
            "当前 commit 与工作树状态",
            "passed" if clean else "blocked",
            f"commit={audit_git.get('commit', '') if isinstance(audit_git, dict) else ''}; clean={clean}",
            "提交并重新生成审计包，直到 current audit bundle 记录 clean worktree。",
        ),
        _checklist_item(
            "audit.bundle_gate",
            "当前审计包 gate",
            "passed" if audit_gate == "passed" else "blocked",
            f"auditGate={audit_gate}",
            "补齐 current audit bundle required evidence；不得把 blocked bundle 当作第三方审计通过。",
        ),
        _checklist_item(
            "audit.dry_run_gate",
            "审计 handoff dry-run",
            "passed" if _status(audit_dry_run) == "passed" else "blocked",
            f"dryRunStatus={_status(audit_dry_run)}; shipGate={dry_run_gate}",
            "dry-run 失败时先修复 handoff 结构；shipGate blocked 表示外部证据仍待执行。",
        ),
        _checklist_item(
            "release.current_proof_gate",
            "当前发布证据",
            "passed" if release_gate == "passed" else "blocked",
            f"proofGate={release_gate}",
            "为最终 commit 重跑远端 Acceptance/Container release、artifact attestation 和 release proof。",
        ),
        _checklist_item(
            "certification.aggregator_gate",
            "100% certification 聚合器",
            "passed" if can_claim else "blocked",
            f"certificationStatus={_status(certification)}; canClaim100Percent={can_claim}",
            "只有所有 domain passed 且外部 live/audit evidence 闭合后才允许 canClaim100Percent=true。",
        ),
        _checklist_item(
            "external_validation.closure_gate",
            "外部验证关闭证据",
            "passed" if closure_gate == "passed" and not external_pending else "blocked",
            f"closureGate={closure_gate}; externalPending={len(external_pending)}",
            "按 operator runbooks 执行真实外部验证并提交脱敏 proof-ref/live proof。",
        ),
        _checklist_item(
            "third_party.independent_result",
            "独立第三方审计结果",
            "blocked",
            "externalAuditorResult=missing",
            "把本预演包、证据索引和外部 pending 清单交给独立审计人员复核并获取可追溯结果。",
        ),
    ]


def _blocking_items(checklist: list[dict[str, str]], external_pending: list[dict[str, Any]]) -> list[dict[str, Any]]:
    items = [
        {
            "id": item["id"],
            "reason": item["evidence"],
            "nextAction": item["nextAction"],
        }
        for item in checklist
        if item["status"] != "passed"
    ]
    if external_pending:
        items.append(
            {
                "id": "external_validation.pending_work_items",
                "reason": f"externalPending={len(external_pending)}",
                "nextAction": "execute external validation operator packet and submit redacted evidence bundle",
            }
        )
    return items


def _assert_no_forbidden(payload: dict[str, Any], markdown: str, contract: dict[str, Any]) -> None:
    rendered = json.dumps(payload, ensure_ascii=False, sort_keys=True) + markdown
    if SENSITIVE_RE.search(rendered):
        raise ThirdPartyAuditRehearsalError("sensitive-looking assignment detected in rehearsal output")
    if RAW_URL_RE.search(rendered):
        raise ThirdPartyAuditRehearsalError("raw URL detected in rehearsal output")
    lower = rendered.lower()
    found = [fragment for fragment in contract.get("forbiddenFragments", []) if fragment.lower() in lower]
    if found:
        raise ThirdPartyAuditRehearsalError("forbidden fragment detected: " + ", ".join(found))


def _table(rows: list[list[Any]]) -> str:
    if not rows:
        return ""
    lines = [
        "| " + " | ".join(str(item) for item in rows[0]) + " |",
        "| " + " | ".join("---" for _ in rows[0]) + " |",
    ]
    for row in rows[1:]:
        lines.append("| " + " | ".join(str(item).replace("\n", " ") for item in row) + " |")
    return "\n".join(lines)


def render_markdown(report: dict[str, Any]) -> str:
    evidence_rows = [["Evidence", "Status", "Gate", "Path"]]
    for item in report["evidenceIndex"]:
        evidence_rows.append([item["id"], item["status"], item.get("gate", ""), item["path"]])
    checklist_rows = [["Check", "Status", "Evidence", "Next Action"]]
    for item in report["auditorChecklist"]:
        checklist_rows.append([item["id"], item["status"], item["evidence"], item["nextAction"]])
    pending_rows = [["Work Item", "Category", "Owner", "Blocking Items"]]
    for item in report["externalPending"][:80]:
        pending_rows.append(
            [
                item["workItemId"],
                item["category"],
                item["owner"],
                ",".join(item["blockingItems"]),
            ]
        )
    return "\n".join(
        [
            "# FateCat Third-Party Audit Rehearsal",
            "",
            "## Latest Status",
            "",
            f"- Generated At: `{report['generatedAt']}`",
            f"- Status: `{report['status']}`",
            f"- Rehearsal Gate: `{report['rehearsalGate']['status']}`",
            f"- External Pending: `{report['summary']['externalPending']}`",
            f"- Blocking Items: `{report['summary']['blockingItems']}`",
            "",
            "## Evidence Index",
            "",
            _table(evidence_rows),
            "",
            "## Auditor Checklist",
            "",
            _table(checklist_rows),
            "",
            "## External Pending",
            "",
            _table(pending_rows),
            "",
            "## Non Claims",
            "",
            "- This rehearsal does not replace third-party audit.",
            "- This rehearsal does not prove production live, external connectivity, OIDC/SIEM, monitoring, Vault/KMS, developer portal or 100% readiness.",
            "- Real external evidence and independent audit result remain required.",
            "",
            "## Final Conclusion",
            "",
            "The package is ready for audit rehearsal when `status` is `passed`. It remains blocked for production 100% claims until all external pending items are closed and an independent third-party audit result is attached.",
            "",
        ]
    )


def build_report(
    *,
    current_audit_bundle_json: Path,
    audit_dry_run_json: Path,
    current_release_proof_json: Path,
    certification_json: Path,
    closure_evidence_summary_json: Path,
    output_json: Path,
    output_markdown: Path,
) -> tuple[dict[str, Any], str]:
    contract = _load_json(CONTRACT_PATH)
    if contract.get("kind") != "fatecat.third_party_audit_rehearsal_contract":
        raise ThirdPartyAuditRehearsalError("contract.kind mismatch")

    for label, path in (
        ("currentAuditBundle", current_audit_bundle_json),
        ("auditDryRun", audit_dry_run_json),
        ("currentReleaseProof", current_release_proof_json),
        ("certification", certification_json),
        ("closureEvidenceSummary", closure_evidence_summary_json),
    ):
        _require_file(path, label=label)

    current_audit_bundle = _load_json(current_audit_bundle_json)
    audit_dry_run = _load_json(audit_dry_run_json)
    current_release_proof = _load_json(current_release_proof_json)
    certification = _load_json(certification_json)
    closure_summary = _load_json(closure_evidence_summary_json)

    required_kinds = contract["requiredKinds"]
    _require_kind(current_audit_bundle, expected=required_kinds["currentAuditBundle"], label="currentAuditBundle")
    _require_kind(audit_dry_run, expected=required_kinds["auditDryRun"], label="auditDryRun")
    _require_kind(current_release_proof, expected=required_kinds["currentReleaseProof"], label="currentReleaseProof")
    _require_kind(certification, expected=required_kinds["certification"], label="certification")
    _require_kind(
        closure_summary,
        expected=required_kinds["closureEvidenceSummary"],
        label="closureEvidenceSummary",
    )

    external_pending = _sanitize_external_pending(closure_summary)
    evidence_index = _build_evidence_index(
        current_audit_bundle_json=current_audit_bundle_json,
        audit_dry_run_json=audit_dry_run_json,
        current_release_proof_json=current_release_proof_json,
        certification_json=certification_json,
        closure_evidence_summary_json=closure_evidence_summary_json,
        current_audit_bundle=current_audit_bundle,
        audit_dry_run=audit_dry_run,
        current_release_proof=current_release_proof,
        certification=certification,
        closure_summary=closure_summary,
    )
    checklist = _build_checklist(
        current_audit_bundle=current_audit_bundle,
        audit_dry_run=audit_dry_run,
        current_release_proof=current_release_proof,
        certification=certification,
        closure_summary=closure_summary,
        external_pending=external_pending,
    )
    blocking = _blocking_items(checklist, external_pending)
    report = {
        "schemaVersion": 1,
        "kind": OUTPUT_KIND,
        "generatedAt": _utc_now(),
        "status": "passed",
        "inputs": {
            "currentAuditBundleJson": str(current_audit_bundle_json),
            "auditDryRunJson": str(audit_dry_run_json),
            "currentReleaseProofJson": str(current_release_proof_json),
            "certificationJson": str(certification_json),
            "closureEvidenceSummaryJson": str(closure_evidence_summary_json),
        },
        "summary": {
            "evidenceInputs": len(evidence_index),
            "checklistItems": len(checklist),
            "passedChecklistItems": sum(1 for item in checklist if item["status"] == "passed"),
            "blockedChecklistItems": sum(1 for item in checklist if item["status"] != "passed"),
            "externalPending": len(external_pending),
            "blockingItems": len(blocking),
        },
        "evidenceIndex": evidence_index,
        "auditorChecklist": checklist,
        "externalPending": external_pending,
        "blockingItems": blocking,
        "rehearsalGate": {
            "status": "passed" if not blocking and not external_pending else "blocked",
            "policy": contract["rehearsalGatePolicy"],
        },
        "outputs": {
            "jsonPath": str(output_json),
            "markdownPath": str(output_markdown),
        },
        "privacyBoundary": contract["privacyBoundary"],
        "nonClaims": contract["nonClaims"],
    }
    markdown = render_markdown(report)
    _assert_no_forbidden(report, markdown, contract)
    return report, markdown


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build third-party audit rehearsal package.")
    parser.add_argument("--current-audit-bundle-json", type=Path, required=True)
    parser.add_argument("--audit-dry-run-json", type=Path, required=True)
    parser.add_argument("--current-release-proof-json", type=Path, required=True)
    parser.add_argument("--certification-json", type=Path, required=True)
    parser.add_argument("--closure-evidence-summary-json", type=Path, required=True)
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON)
    parser.add_argument("--output-markdown", type=Path, default=DEFAULT_OUTPUT_MARKDOWN)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        report, markdown = build_report(
            current_audit_bundle_json=args.current_audit_bundle_json,
            audit_dry_run_json=args.audit_dry_run_json,
            current_release_proof_json=args.current_release_proof_json,
            certification_json=args.certification_json,
            closure_evidence_summary_json=args.closure_evidence_summary_json,
            output_json=args.output_json,
            output_markdown=args.output_markdown,
        )
        _write_json(args.output_json, report)
        args.output_markdown.parent.mkdir(parents=True, exist_ok=True)
        args.output_markdown.write_text(markdown, encoding="utf-8")
        print(
            json.dumps(
                {
                    "status": report["status"],
                    "rehearsalGate": report["rehearsalGate"]["status"],
                    "evidenceInputs": report["summary"]["evidenceInputs"],
                    "externalPending": report["summary"]["externalPending"],
                    "blockingItems": report["summary"]["blockingItems"],
                    "outputJson": str(args.output_json),
                    "outputMarkdown": str(args.output_markdown),
                },
                ensure_ascii=False,
                sort_keys=True,
            )
        )
        return 0
    except (ThirdPartyAuditRehearsalError, OSError, json.JSONDecodeError) as exc:
        print(f"third-party audit rehearsal error: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
