#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_DIR = REPO_ROOT / "infra" / "runtime" / "local-state" / "exports" / "current-audit-bundle"
BUNDLE_FILENAME = "current-audit-bundle.json"
MARKDOWN_FILENAME = "CURRENT_AUDIT_BUNDLE.md"
EVIDENCE_INDEX_FILENAME = "evidence-index.json"
RISK_REGISTER_FILENAME = "risk-register.json"
PENDING_EXTERNAL_FILENAME = "pending-external-validations.json"
PENDING_PHRASE = "外部连通验证待执行"
FORBIDDEN_MARKERS = ("token=", "secret=", "password=", "passwd=", "private_key=", "BEGIN RSA", "BEGIN OPENSSH")


class CurrentAuditBundleError(RuntimeError):
    """当前发布审计包生成失败。"""


@dataclass(frozen=True)
class EvidenceItem:
    id: str
    type: str
    status: str
    path: str
    required: bool
    detail: str = ""
    commit: str = ""
    digest: str = ""
    url: str = ""

    def to_json(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "type": self.type,
            "status": self.status,
            "path": self.path,
            "required": self.required,
            "detail": self.detail,
            "commit": self.commit,
            "digest": self.digest,
            "url": self.url,
        }


def utc_now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def run_capture(args: list[str], *, timeout_seconds: int = 20) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=REPO_ROOT, text=True, capture_output=True, timeout=timeout_seconds, check=False)


def git_value(*args: str) -> str:
    result = run_capture(["git", *args], timeout_seconds=15)
    if result.returncode != 0:
        return ""
    return result.stdout.strip()


def git_status_counts() -> dict[str, Any]:
    result = run_capture(["git", "status", "--porcelain"], timeout_seconds=15)
    lines = [line for line in result.stdout.splitlines() if line.strip()] if result.returncode == 0 else []
    untracked = [line for line in lines if line.startswith("??")]
    return {"clean": len(lines) == 0, "dirtyCount": len(lines), "untrackedCount": len(untracked)}


def repo_path(value: str | Path) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path
    return REPO_ROOT / path


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as fh:
        payload = json.load(fh)
    if not isinstance(payload, dict):
        raise CurrentAuditBundleError(f"JSON root must be object: {path}")
    return payload


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_text_safe(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


def path_evidence_missing(item_id: str, item_type: str, path_text: str, *, required: bool, detail: str) -> EvidenceItem:
    return EvidenceItem(
        id=item_id,
        type=item_type,
        status="missing" if path_text else "pending",
        path=path_text or "not provided",
        required=required,
        detail=detail,
    )


def status_from_errors(errors: list[str]) -> str:
    return "pass" if not errors else "fail"


def local_ci_evidence(path_text: str, current_commit: str, *, required: bool) -> EvidenceItem:
    if not path_text:
        return path_evidence_missing(
            "evidence.local_ci_summary",
            "local_ci",
            "",
            required=required,
            detail="local-ci summary not provided",
        )
    path = repo_path(path_text)
    if not path.is_file():
        return path_evidence_missing(
            "evidence.local_ci_summary",
            "local_ci",
            str(path),
            required=required,
            detail="file missing",
        )
    payload = load_json(path)
    errors: list[str] = []
    if payload.get("kind") != "fatecat.local_ci_summary":
        errors.append("kind must be fatecat.local_ci_summary")
    if payload.get("status") != "passed":
        errors.append("status must be passed")
    if payload.get("commit") != current_commit:
        errors.append("commit must match current HEAD")
    git_payload = payload.get("git", {})
    if isinstance(git_payload, dict) and (git_payload.get("dirtyCount") or git_payload.get("untrackedCount")):
        errors.append("local-ci summary must be clean")
    return EvidenceItem(
        id="evidence.local_ci_summary",
        type="local_ci",
        status=status_from_errors(errors),
        path=str(path),
        required=required,
        detail="; ".join(errors) if errors else f"profile={payload.get('profile')}",
        commit=str(payload.get("commit", "")),
    )


def current_release_proof_evidence(path_text: str, current_commit: str, *, required: bool) -> EvidenceItem:
    if not path_text:
        return path_evidence_missing(
            "evidence.current_release_proof",
            "current_release_proof",
            "",
            required=required,
            detail="current release proof not provided",
        )
    path = repo_path(path_text)
    if not path.is_file():
        return path_evidence_missing(
            "evidence.current_release_proof",
            "current_release_proof",
            str(path),
            required=required,
            detail="file missing",
        )
    payload = load_json(path)
    errors: list[str] = []
    if payload.get("kind") != "fatecat.current_release_proof":
        errors.append("kind must be fatecat.current_release_proof")
    if payload.get("status") != "passed":
        errors.append("status must be passed")
    proof_gate = payload.get("proofGate", {})
    if not isinstance(proof_gate, dict) or proof_gate.get("status") != "passed":
        errors.append("proofGate.status must be passed")
    git_payload = payload.get("git", {})
    if not isinstance(git_payload, dict) or git_payload.get("commit") != current_commit:
        errors.append("proof commit must match current HEAD")
    if isinstance(git_payload, dict) and git_payload.get("dirtyCount") not in {0, None}:
        errors.append("proof must have dirtyCount=0")
    container = payload.get("container", {}) if isinstance(payload.get("container"), dict) else {}
    github = payload.get("github", {}) if isinstance(payload.get("github"), dict) else {}
    return EvidenceItem(
        id="evidence.current_release_proof",
        type="current_release_proof",
        status=status_from_errors(errors),
        path=str(path),
        required=required,
        detail="; ".join(errors) if errors else "current release proof accepted",
        commit=str(git_payload.get("commit", "")) if isinstance(git_payload, dict) else "",
        digest=str(container.get("digest", "")),
        url=f"acceptance={github.get('acceptanceRunId')}; container={github.get('containerRunId')}",
    )


def audit_handoff_evidence(path_text: str, current_commit: str) -> tuple[EvidenceItem, dict[str, Any]]:
    if not path_text:
        return (
            path_evidence_missing(
                "evidence.audit_handoff_json",
                "audit_handoff",
                "",
                required=True,
                detail="audit handoff json not provided",
            ),
            {},
        )
    path = repo_path(path_text)
    if not path.is_file():
        return (
            path_evidence_missing(
                "evidence.audit_handoff_json",
                "audit_handoff",
                str(path),
                required=True,
                detail="file missing",
            ),
            {},
        )
    payload = load_json(path)
    errors: list[str] = []
    if payload.get("kind") != "fatecat.audit_handoff_bundle":
        errors.append("kind must be fatecat.audit_handoff_bundle")
    if payload.get("status") != "passed":
        errors.append("status must be passed")
    commit = ""
    repository = payload.get("repository", {})
    if isinstance(repository, dict):
        commit = str(repository.get("commit", ""))
        if commit != current_commit:
            errors.append("audit handoff commit must match current HEAD")
    return (
        EvidenceItem(
            id="evidence.audit_handoff_json",
            type="audit_handoff",
            status=status_from_errors(errors),
            path=str(path),
            required=True,
            detail="; ".join(errors) if errors else "audit handoff json accepted",
            commit=commit,
        ),
        payload,
    )


def markdown_evidence(item_id: str, path_text: str, required_section: str) -> EvidenceItem:
    if not path_text:
        return path_evidence_missing(item_id, "markdown", "", required=True, detail="markdown path not provided")
    path = repo_path(path_text)
    if not path.is_file():
        return path_evidence_missing(item_id, "markdown", str(path), required=True, detail="file missing")
    text = read_text_safe(path)
    errors = [] if f"## {required_section}" in text else [f"missing section: {required_section}"]
    return EvidenceItem(
        id=item_id,
        type="markdown",
        status=status_from_errors(errors),
        path=str(path),
        required=True,
        detail="; ".join(errors) if errors else "markdown accepted",
    )


def audit_dry_run_evidence(path_text: str, current_commit: str) -> EvidenceItem:
    if not path_text:
        return path_evidence_missing(
            "evidence.audit_dry_run",
            "audit_dry_run",
            "",
            required=True,
            detail="audit dry-run json not provided",
        )
    path = repo_path(path_text)
    if not path.is_file():
        return path_evidence_missing(
            "evidence.audit_dry_run",
            "audit_dry_run",
            str(path),
            required=True,
            detail="file missing",
        )
    payload = load_json(path)
    errors: list[str] = []
    if payload.get("kind") != "fatecat.audit_handoff_dry_run":
        errors.append("kind must be fatecat.audit_handoff_dry_run")
    if payload.get("status") != "passed":
        errors.append("status must be passed")
    inputs = payload.get("inputs", {})
    commit = str(inputs.get("bundleCommit", "")) if isinstance(inputs, dict) else ""
    if commit and commit != current_commit:
        errors.append("dry-run bundleCommit must match current HEAD")
    return EvidenceItem(
        id="evidence.audit_dry_run",
        type="audit_dry_run",
        status=status_from_errors(errors),
        path=str(path),
        required=True,
        detail="; ".join(errors) if errors else f"shipGate={payload.get('shipGate', {}).get('status')}",
        commit=commit,
    )


def release_artifacts_evidence(path_text: str, current_commit: str) -> list[EvidenceItem]:
    if not path_text:
        return [
            path_evidence_missing(
                "evidence.release_artifacts",
                "release_artifacts",
                "",
                required=True,
                detail="release artifacts directory not provided",
            )
        ]
    directory = repo_path(path_text)
    if not directory.is_dir():
        return [
            path_evidence_missing(
                "evidence.release_artifacts",
                "release_artifacts",
                str(directory),
                required=True,
                detail="directory missing",
            )
        ]
    manifest_path = directory / "release-artifacts-manifest.json"
    sbom_path = directory / "sbom.cyclonedx.json"
    provenance_path = directory / "provenance.slsa.json"
    items: list[EvidenceItem] = []
    errors: list[str] = []
    manifest: dict[str, Any] = {}
    if manifest_path.is_file():
        manifest = load_json(manifest_path)
        if manifest.get("resourceType") != "ReleaseArtifactManifest":
            errors.append("manifest resourceType mismatch")
        git_payload = manifest.get("git", {})
        if not isinstance(git_payload, dict) or git_payload.get("commit") != current_commit:
            errors.append("manifest commit must match current HEAD")
        for artifact in manifest.get("artifacts", []):
            if not isinstance(artifact, dict):
                continue
            artifact_path = Path(str(artifact.get("path", "")))
            if not artifact_path.is_absolute():
                artifact_path = repo_path(artifact_path)
            if not artifact_path.is_file():
                errors.append(f"artifact missing: {artifact_path}")
                continue
            if artifact.get("sha256") != sha256_file(artifact_path):
                errors.append(f"artifact sha256 mismatch: {artifact_path}")
    else:
        errors.append("manifest missing")
    items.append(
        EvidenceItem(
            id="evidence.release_artifacts_manifest",
            type="release_artifacts",
            status=status_from_errors(errors),
            path=str(manifest_path),
            required=True,
            detail="; ".join(errors) if errors else "manifest and hashes accepted",
            commit=str(manifest.get("git", {}).get("commit", "")) if isinstance(manifest.get("git"), dict) else "",
            digest=sha256_file(manifest_path) if manifest_path.is_file() else "",
        )
    )
    for item_id, artifact_type, artifact_path in (
        ("evidence.release_sbom", "sbom", sbom_path),
        ("evidence.release_provenance", "provenance", provenance_path),
    ):
        if not artifact_path.is_file():
            items.append(
                path_evidence_missing(
                    item_id,
                    artifact_type,
                    str(artifact_path),
                    required=True,
                    detail="file missing",
                )
            )
            continue
        items.append(
            EvidenceItem(
                id=item_id,
                type=artifact_type,
                status="pass",
                path=str(artifact_path),
                required=True,
                detail="artifact present",
                digest=sha256_file(artifact_path),
            )
        )
    return items


def rollback_evidence(path_text: str, current_commit: str) -> EvidenceItem:
    if not path_text:
        return path_evidence_missing(
            "evidence.rollback_drill",
            "rollback",
            "",
            required=True,
            detail="rollback evidence not provided",
        )
    path = repo_path(path_text)
    if not path.is_file():
        return path_evidence_missing(
            "evidence.rollback_drill",
            "rollback",
            str(path),
            required=True,
            detail="file missing",
        )
    payload = load_json(path)
    errors: list[str] = []
    if payload.get("kind") != "fatecat.rollback_drill_evidence":
        errors.append("kind must be fatecat.rollback_drill_evidence")
    if payload.get("status") != "passed":
        errors.append("status must be passed")
    if payload.get("productionRollbackExecuted") is not False:
        errors.append("productionRollbackExecuted must be false")
    git_payload = payload.get("git", {})
    if not isinstance(git_payload, dict) or git_payload.get("commit") != current_commit:
        errors.append("rollback commit must match current HEAD")
    return EvidenceItem(
        id="evidence.rollback_drill",
        type="rollback",
        status=status_from_errors(errors),
        path=str(path),
        required=True,
        detail="; ".join(errors) if errors else "dry-run rollback accepted",
        commit=str(git_payload.get("commit", "")) if isinstance(git_payload, dict) else "",
    )


def pending_external_from_handoff(handoff: dict[str, Any]) -> list[dict[str, Any]]:
    items = handoff.get("pendingExternalValidations")
    if isinstance(items, list):
        return [item for item in items if isinstance(item, dict)]
    return []


def build_risk_register(
    *,
    evidence: list[EvidenceItem],
    pending_external_count: int,
    require_current_release: bool,
) -> list[dict[str, Any]]:
    failed_required = [item.id for item in evidence if item.required and item.status == "fail"]
    missing_required = [item.id for item in evidence if item.required and item.status == "missing"]
    pending_required = [item.id for item in evidence if item.required and item.status == "pending"]
    risks: list[dict[str, Any]] = []
    if failed_required or missing_required:
        risks.append(
            {
                "id": "risk.current_audit_required_evidence_incomplete",
                "severity": "blocking_for_audit_bundle_claim",
                "status": "open",
                "evidence": json.dumps({"failed": failed_required, "missing": missing_required}, ensure_ascii=False),
                "mitigation": "Regenerate the missing/failed evidence from the current HEAD before handoff.",
            }
        )
    if pending_required:
        risks.append(
            {
                "id": "risk.current_audit_evidence_pending",
                "severity": "blocking_when_require_current_release",
                "status": "open" if require_current_release else "accepted_local_contract",
                "evidence": ",".join(pending_required),
                "mitigation": "Run external release proof and pass --require-current-release for final audit bundle.",
            }
        )
    if pending_external_count > 0:
        risks.append(
            {
                "id": "risk.external_validations_pending",
                "severity": "blocking_for_100_percent_live_claim",
                "status": "open",
                "evidence": f"pendingExternalValidationCount={pending_external_count}",
                "mitigation": "Keep production live claims blocked until each external validation has real evidence.",
            }
        )
    risks.append(
        {
            "id": "risk.third_party_audit_not_performed_by_script",
            "severity": "non_blocking_for_bundle_generation",
            "status": "open",
            "evidence": "Bundle is generated by repository tooling and still needs independent auditor review.",
            "mitigation": "Send JSON/Markdown and evidence index to third-party auditor.",
        }
    )
    return risks


def audit_gate_status(evidence: list[EvidenceItem], *, require_current_release: bool) -> tuple[str, list[str]]:
    blocking = [item.id for item in evidence if item.required and item.status in {"fail", "missing"}]
    pending = [item.id for item in evidence if item.required and item.status == "pending"]
    if blocking:
        return "failed", blocking
    if pending or not require_current_release:
        return "blocked", pending
    return "passed", []


def markdown_table(rows: list[list[Any]]) -> str:
    if not rows:
        return ""
    lines = [
        "| " + " | ".join(str(item) for item in rows[0]) + " |",
        "| " + " | ".join("---" for _ in rows[0]) + " |",
    ]
    for row in rows[1:]:
        lines.append("| " + " | ".join(str(item).replace("\n", " ") for item in row) + " |")
    return "\n".join(lines)


def render_markdown(bundle: dict[str, Any]) -> str:
    evidence_rows = [["ID", "Type", "Status", "Required", "Detail"]]
    for item in bundle["evidenceIndex"]:
        evidence_rows.append([item["id"], item["type"], item["status"], item["required"], item["detail"]])
    risk_rows = [["ID", "Severity", "Status", "Evidence"]]
    for item in bundle["riskRegister"]:
        risk_rows.append([item["id"], item["severity"], item["status"], item["evidence"]])
    pending_rows = [["Path", "Line", "Excerpt"]]
    for item in bundle["pendingExternalValidations"][:80]:
        pending_rows.append([item.get("path", ""), item.get("line", ""), item.get("excerpt", "")])
    container = bundle["releaseProof"].get("container", {})
    github = bundle["releaseProof"].get("github", {})
    sections = [
        "# FateCat Current Audit Bundle",
        "",
        "## Latest Status",
        "",
        f"- Generated At: `{bundle['generatedAt']}`",
        f"- Branch: `{bundle['git']['branch']}`",
        f"- Commit: `{bundle['git']['commit']}`",
        f"- Clean Worktree: `{bundle['git']['clean']}`",
        f"- Audit Gate: `{bundle['auditGate']['status']}`",
        "",
        "## Evidence Index",
        "",
        markdown_table(evidence_rows),
        "",
        "## Release Proof",
        "",
        f"- Mode: `{bundle['releaseProof'].get('mode', '')}`",
        f"- Proof Gate: `{bundle['releaseProof'].get('proofGate', {}).get('status', '')}`",
        f"- Acceptance Run: `{github.get('acceptanceRunId', '')}`",
        f"- Container Run: `{github.get('containerRunId', '')}`",
        f"- Container Digest: `{container.get('digest', '')}`",
        "",
        "## Pending External Validations",
        "",
        f"- Phrase: `{PENDING_PHRASE}`",
        f"- Count: `{bundle['pendingExternalValidationCount']}`",
        "",
        markdown_table(pending_rows),
        "",
        "## Risk Register",
        "",
        markdown_table(risk_rows),
        "",
        "## Verification",
        "",
        f"- Required current release: `{bundle['requireCurrentRelease']}`",
        f"- Output JSON: `{bundle['outputs']['bundleJson']}`",
        f"- Evidence Index JSON: `{bundle['outputs']['evidenceIndexJson']}`",
        f"- Risk Register JSON: `{bundle['outputs']['riskRegisterJson']}`",
        f"- Pending External JSON: `{bundle['outputs']['pendingExternalJson']}`",
        "",
        "## Final Conclusion",
        "",
        "This bundle is ready for current-commit audit review only when `auditGate.status` is `passed`. It does not prove production API/HF/Bot live status, real production rollback, or third-party audit completion.",
        "",
    ]
    return "\n".join(sections)


def assert_no_sensitive_markers(payload: dict[str, Any], markdown: str) -> None:
    serialized = json.dumps(payload, ensure_ascii=False).lower() + markdown.lower()
    found = [marker for marker in FORBIDDEN_MARKERS if marker.lower() in serialized]
    if found:
        raise CurrentAuditBundleError("current audit bundle contains forbidden sensitive marker: " + ",".join(found))


def build_bundle(args: argparse.Namespace) -> dict[str, Any]:
    current_commit = git_value("rev-parse", "--verify", "HEAD")
    branch = git_value("rev-parse", "--abbrev-ref", "HEAD")
    git_status = git_status_counts()
    evidence: list[EvidenceItem] = []
    local_ci_required = bool(args.require_current_release)
    evidence.append(local_ci_evidence(args.local_ci_summary, current_commit, required=local_ci_required))
    handoff_item, handoff_payload = audit_handoff_evidence(args.audit_handoff_json, current_commit)
    evidence.append(handoff_item)
    evidence.append(
        markdown_evidence("evidence.audit_handoff_markdown", args.audit_handoff_markdown, "Final Conclusion")
    )
    evidence.append(audit_dry_run_evidence(args.audit_dry_run_json, current_commit))
    evidence.extend(release_artifacts_evidence(args.release_artifacts_dir, current_commit))
    evidence.append(rollback_evidence(args.rollback_evidence_path, current_commit))
    current_proof_item = current_release_proof_evidence(
        args.current_release_proof,
        current_commit,
        required=bool(args.require_current_release),
    )
    evidence.append(current_proof_item)

    current_proof_path = repo_path(args.current_release_proof) if args.current_release_proof else None
    current_proof_payload = load_json(current_proof_path) if current_proof_path and current_proof_path.is_file() else {}
    pending_external = pending_external_from_handoff(handoff_payload)
    gate, blockers = audit_gate_status(evidence, require_current_release=bool(args.require_current_release))
    if not git_status["clean"]:
        blockers = [*blockers, "git.clean"]
        gate = "failed" if args.require_current_release else "blocked"
    if args.require_current_release and current_proof_item.status != "pass":
        gate = "failed"
        blockers = [*blockers, current_proof_item.id]
    risk_register = build_risk_register(
        evidence=evidence,
        pending_external_count=len(pending_external),
        require_current_release=bool(args.require_current_release),
    )

    output_dir = repo_path(args.output_dir)
    outputs = {
        "bundleJson": str(output_dir / BUNDLE_FILENAME),
        "bundleMarkdown": str(output_dir / MARKDOWN_FILENAME),
        "evidenceIndexJson": str(output_dir / EVIDENCE_INDEX_FILENAME),
        "riskRegisterJson": str(output_dir / RISK_REGISTER_FILENAME),
        "pendingExternalJson": str(output_dir / PENDING_EXTERNAL_FILENAME),
    }
    bundle = {
        "schemaVersion": 1,
        "kind": "fatecat.current_audit_bundle",
        "generatedAt": utc_now(),
        "status": "passed" if gate in {"passed", "blocked"} else "failed",
        "requireCurrentRelease": bool(args.require_current_release),
        "git": {
            "branch": branch,
            "commit": current_commit,
            **git_status,
        },
        "auditGate": {
            "status": gate,
            "blockingItems": sorted(set(blockers)),
            "policy": "required mode passes only when all current-commit local and remote release evidence is accepted",
        },
        "releaseProof": {
            "path": str(repo_path(args.current_release_proof)) if args.current_release_proof else "",
            "mode": current_proof_payload.get("mode", ""),
            "proofGate": current_proof_payload.get("proofGate", {}),
            "github": current_proof_payload.get("github", {}),
            "container": current_proof_payload.get("container", {}),
        },
        "evidenceIndex": [item.to_json() for item in evidence],
        "pendingExternalValidationCount": len(pending_external),
        "pendingExternalValidations": pending_external,
        "riskRegister": risk_register,
        "outputs": outputs,
        "privacyBoundary": "不复制 token、secret、DSN、私钥、用户报告正文、真实生产日志正文或真实用户输入。",
        "nonClaims": [
            "Current audit bundle does not mean third-party audit passed.",
            "Current audit bundle does not prove production API/HF/Bot live unless separate live evidence exists.",
            "Rollback evidence is dry-run unless productionRollbackExecuted is explicitly true in a separate authorized artifact.",
        ],
    }
    markdown = render_markdown(bundle)
    assert_no_sensitive_markers(bundle, markdown)
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / BUNDLE_FILENAME).write_text(
        json.dumps(bundle, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (output_dir / MARKDOWN_FILENAME).write_text(markdown, encoding="utf-8")
    (output_dir / EVIDENCE_INDEX_FILENAME).write_text(
        json.dumps(bundle["evidenceIndex"], ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (output_dir / RISK_REGISTER_FILENAME).write_text(
        json.dumps(bundle["riskRegister"], ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (output_dir / PENDING_EXTERNAL_FILENAME).write_text(
        json.dumps(bundle["pendingExternalValidations"], ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return bundle


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Assemble current commit audit evidence bundle.")
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR), help="current audit bundle output dir")
    parser.add_argument("--local-ci-summary", default="", help="local-ci summary.json")
    parser.add_argument("--audit-handoff-json", default="", help="audit-handoff.json")
    parser.add_argument("--audit-handoff-markdown", default="", help="AUDIT_HANDOFF.md")
    parser.add_argument("--audit-dry-run-json", default="", help="audit-dry-run.json")
    parser.add_argument("--current-release-proof", default="", help="current-release-proof JSON")
    parser.add_argument("--rollback-evidence-path", default="", help="rollback drill evidence JSON")
    parser.add_argument("--release-artifacts-dir", default="", help="release artifacts directory")
    parser.add_argument("--require-current-release", action="store_true", help="fail unless current audit gate passes")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        bundle = build_bundle(args)
    except (CurrentAuditBundleError, OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"current audit bundle error: {exc}", file=sys.stderr)
        return 1
    print(
        json.dumps(
            {
                "status": bundle["status"],
                "auditGate": bundle["auditGate"]["status"],
                "evidence": len(bundle["evidenceIndex"]),
                "pendingExternalValidationCount": bundle["pendingExternalValidationCount"],
                "outputJson": bundle["outputs"]["bundleJson"],
                "outputMarkdown": bundle["outputs"]["bundleMarkdown"],
            },
            ensure_ascii=False,
        )
    )
    return 1 if args.require_current_release and bundle["auditGate"]["status"] != "passed" else 0


if __name__ == "__main__":
    raise SystemExit(main())
