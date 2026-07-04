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
CONTRACT_PATH = ROOT / "contracts" / "fate" / "audit" / "independent-audit-result.json"
DEFAULT_OUTPUT_JSON = (
    ROOT / "infra" / "runtime" / "local-state" / "exports" / "audit" / "independent-audit-result-gate.json"
)

INPUT_KIND = "fatecat.independent_audit_result_bundle"
OUTPUT_KIND = "fatecat.independent_audit_result_gate"
PRIVACY_BOUNDARY = "redacted_no_secret_values"
ACCEPTED_DECISIONS = {"accepted_no_findings", "accepted_with_findings"}
REJECTED_DECISIONS = {"rejected"}

COMMIT_RE = re.compile(r"^[a-f0-9]{40}$")
SHA256_RE = re.compile(r"^[a-f0-9]{64}$")
ARTIFACT_REF_RE = re.compile(r"^(?:artifact|evidence|ci-artifact|audit-artifact):[A-Za-z0-9_.:/#@=-]+$")
SENSITIVE_RE = re.compile(
    r"(token\s*=|secret\s*=|password\s*=|passwd\s*=|DATABASE_URL\s*=|DB_DSN\s*=|"
    r"api[_-]?key\s*=|private[_-]?key|BEGIN (?:RSA|OPENSSH|PRIVATE)|authorization\s*:)",
    re.IGNORECASE,
)
RAW_URL_RE = re.compile(r"https?://", re.IGNORECASE)
FORBIDDEN_TEXT = (
    "placeholder proof",
    "fake proof",
    "dummy proof",
    "localhost proof",
)


class IndependentAuditResultGateError(RuntimeError):
    """独立审计结果 intake gate 失败。"""


def _utc_now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def _load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as fh:
        payload = json.load(fh)
    if not isinstance(payload, dict):
        raise IndependentAuditResultGateError(f"JSON root must be object: {path}")
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


def _assert_no_sensitive(payload: Any, *, area: str, contract: dict[str, Any] | None = None) -> None:
    rendered = _render(payload)
    if SENSITIVE_RE.search(rendered):
        raise IndependentAuditResultGateError(f"{area}: sensitive-looking assignment detected")
    if RAW_URL_RE.search(rendered):
        raise IndependentAuditResultGateError(f"{area}: raw URL detected")
    lower = rendered.lower()
    markers = list(FORBIDDEN_TEXT)
    if contract is not None:
        markers.extend(str(item).lower() for item in contract.get("forbiddenFragments", []) if "://" not in str(item))
    for marker in markers:
        if marker and marker.lower() in lower:
            raise IndependentAuditResultGateError(f"{area}: forbidden marker detected: {marker}")


def _require_fields(payload: dict[str, Any], fields: list[str], *, area: str) -> None:
    for field in fields:
        if payload.get(field) in ("", None, []):
            raise IndependentAuditResultGateError(f"{area} missing {field}")


def _validate_contract(contract: dict[str, Any]) -> None:
    if contract.get("kind") != "fatecat.independent_audit_result_contract":
        raise IndependentAuditResultGateError("contract.kind mismatch")
    required = set(contract.get("requiredOutputFields", []))
    for field in ("independentAuditResult", "auditResultGate", "shipGate"):
        if field not in required:
            raise IndependentAuditResultGateError(f"contract missing required output field: {field}")


def _validate_artifact_ref(value: str, *, field: str) -> None:
    if not ARTIFACT_REF_RE.match(value):
        raise IndependentAuditResultGateError(f"{field} must be redacted artifact/evidence ref")


def _validate_sha256(value: str, *, field: str) -> None:
    if not SHA256_RE.match(value):
        raise IndependentAuditResultGateError(f"{field} must be sha256 hex")


def _validate_non_negative_int(value: Any, *, field: str) -> int:
    if not isinstance(value, int) or value < 0:
        raise IndependentAuditResultGateError(f"{field} must be non-negative integer")
    return value


def _validate_reviewed_artifacts(bundle: dict[str, Any]) -> list[dict[str, Any]]:
    reviewed_artifacts = bundle.get("reviewedArtifacts")
    if not isinstance(reviewed_artifacts, list) or not reviewed_artifacts:
        raise IndependentAuditResultGateError("reviewedArtifacts must be non-empty array")
    normalized: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    for index, artifact in enumerate(reviewed_artifacts):
        if not isinstance(artifact, dict):
            raise IndependentAuditResultGateError(f"reviewedArtifacts[{index}] must be object")
        _require_fields(artifact, ["id", "kind", "sha256"], area=f"reviewedArtifacts[{index}]")
        artifact_id = str(artifact["id"])
        if artifact_id in seen_ids:
            raise IndependentAuditResultGateError(f"reviewedArtifacts duplicate id: {artifact_id}")
        seen_ids.add(artifact_id)
        _validate_sha256(str(artifact["sha256"]), field=f"reviewedArtifacts[{index}].sha256")
        normalized.append(
            {
                "id": artifact_id,
                "kind": str(artifact["kind"]),
                "sha256": str(artifact["sha256"]),
            }
        )
    return normalized


def _validate_bundle(
    *,
    bundle: dict[str, Any],
    bundle_sha256: str,
    expected_commit: str,
    contract: dict[str, Any],
) -> dict[str, Any]:
    if bundle.get("kind") != INPUT_KIND:
        raise IndependentAuditResultGateError(f"independent audit result bundle kind must be {INPUT_KIND}")
    if str(bundle.get("privacyBoundary", "")) != PRIVACY_BOUNDARY:
        raise IndependentAuditResultGateError("privacyBoundary must be redacted_no_secret_values")

    input_contract = contract["inputBundle"]
    _require_fields(bundle, input_contract["requiredTopLevelFields"], area="bundle")
    source = bundle.get("source")
    auditor = bundle.get("auditor")
    result = bundle.get("result")
    if not isinstance(source, dict) or not isinstance(auditor, dict) or not isinstance(result, dict):
        raise IndependentAuditResultGateError("source, auditor and result must be objects")
    _require_fields(source, input_contract["sourceRequiredFields"], area="source")
    _require_fields(auditor, input_contract["auditorRequiredFields"], area="auditor")
    _require_fields(result, input_contract["resultRequiredFields"], area="result")

    source_commit = str(source["commit"])
    if source_commit != expected_commit:
        raise IndependentAuditResultGateError(
            f"independent audit result commit {source_commit} does not match expected commit {expected_commit}"
        )

    _validate_artifact_ref(str(auditor["organizationRef"]), field="auditor.organizationRef")
    _validate_artifact_ref(str(auditor["identityProofRef"]), field="auditor.identityProofRef")
    _validate_sha256(str(auditor["signedResultArtifactSha256"]), field="auditor.signedResultArtifactSha256")
    if str(auditor.get("auditorRole", "")) not in {"independent_auditor", "third_party_auditor"}:
        raise IndependentAuditResultGateError("auditor.auditorRole must identify an independent auditor role")

    decision = str(result["decision"])
    if decision not in ACCEPTED_DECISIONS | REJECTED_DECISIONS:
        raise IndependentAuditResultGateError(f"unsupported audit decision: {decision}")
    _validate_sha256(str(result["scopeHash"]), field="result.scopeHash")
    _validate_sha256(str(result["reportArtifactSha256"]), field="result.reportArtifactSha256")
    if str(result["redactionStatus"]) != PRIVACY_BOUNDARY:
        raise IndependentAuditResultGateError("result.redactionStatus must be redacted_no_secret_values")

    finding_counts = {
        "critical": _validate_non_negative_int(result["criticalFindings"], field="result.criticalFindings"),
        "high": _validate_non_negative_int(result["highFindings"], field="result.highFindings"),
        "medium": _validate_non_negative_int(result["mediumFindings"], field="result.mediumFindings"),
        "low": _validate_non_negative_int(result["lowFindings"], field="result.lowFindings"),
    }
    reviewed_artifacts = _validate_reviewed_artifacts(bundle)

    if decision == "accepted_no_findings" and any(finding_counts.values()):
        raise IndependentAuditResultGateError("accepted_no_findings requires all finding counts to be zero")

    return {
        "bundleKind": INPUT_KIND,
        "bundleSha256": bundle_sha256,
        "commit": source_commit,
        "auditorRole": str(auditor["auditorRole"]),
        "organizationRef": str(auditor["organizationRef"]),
        "identityProofRef": str(auditor["identityProofRef"]),
        "signedAt": str(auditor["signedAt"]),
        "signedResultArtifactSha256": str(auditor["signedResultArtifactSha256"]),
        "decision": decision,
        "scopeHash": str(result["scopeHash"]),
        "reportArtifactSha256": str(result["reportArtifactSha256"]),
        "findingCounts": finding_counts,
        "reviewedArtifacts": reviewed_artifacts,
        "redactionStatus": PRIVACY_BOUNDARY,
    }


def _pending_result(expected_commit: str) -> dict[str, Any]:
    return {
        "bundleKind": None,
        "bundleSha256": None,
        "commit": expected_commit,
        "auditorRole": None,
        "organizationRef": None,
        "identityProofRef": None,
        "signedAt": None,
        "signedResultArtifactSha256": None,
        "decision": "missing",
        "scopeHash": None,
        "reportArtifactSha256": None,
        "findingCounts": {"critical": 0, "high": 0, "medium": 0, "low": 0},
        "reviewedArtifacts": [],
        "redactionStatus": PRIVACY_BOUNDARY,
    }


def build_gate(
    *,
    independent_audit_result_json: Path | None = None,
    expected_commit: str | None = None,
) -> dict[str, Any]:
    expected_commit = expected_commit or _current_commit()
    if not COMMIT_RE.match(expected_commit):
        raise IndependentAuditResultGateError("--expected-commit must be 40 lowercase hex chars")

    contract = _load_json(CONTRACT_PATH)
    _validate_contract(contract)
    bundle_supplied = independent_audit_result_json is not None
    result_summary = _pending_result(expected_commit)

    if independent_audit_result_json is not None:
        if not independent_audit_result_json.is_file():
            raise IndependentAuditResultGateError(
                f"independent audit result json missing: {independent_audit_result_json}"
            )
        bundle_sha256 = _sha256_file(independent_audit_result_json)
        bundle = _load_json(independent_audit_result_json)
        _assert_no_sensitive(bundle, area="independent audit result bundle", contract=contract)
        result_summary = _validate_bundle(
            bundle=bundle,
            bundle_sha256=bundle_sha256,
            expected_commit=expected_commit,
            contract=contract,
        )

    decision = str(result_summary["decision"])
    if not bundle_supplied:
        status = "external_audit_result_pending"
    elif decision in ACCEPTED_DECISIONS:
        status = "accepted"
    else:
        status = "rejected"

    audit_result_gate_status = "passed" if status == "accepted" else "blocked"
    gate = {
        "schemaVersion": 1,
        "kind": OUTPUT_KIND,
        "status": status,
        "generatedAt": _utc_now(),
        "source": {
            "independentAuditResultBundleKind": result_summary["bundleKind"],
            "independentAuditResultBundleSha256": result_summary["bundleSha256"],
            "commit": expected_commit,
        },
        "summary": {
            "resultSupplied": bundle_supplied,
            "acceptedResults": 1 if status == "accepted" else 0,
            "pendingResults": 1 if not bundle_supplied else 0,
            "rejectedResults": 1 if status == "rejected" else 0,
            "decision": decision,
            "reviewedArtifacts": len(result_summary["reviewedArtifacts"]),
        },
        "independentAuditResult": result_summary,
        "auditResultGate": {
            "status": audit_result_gate_status,
            "blockingItems": []
            if audit_result_gate_status == "passed"
            else [
                "independent_audit_result_required" if not bundle_supplied else "independent_auditor_rejected_release",
                "signed_redacted_auditor_result_required",
                "current_commit_binding_required",
            ],
            "reason": (
                "independent auditor result is structurally accepted for the current commit"
                if audit_result_gate_status == "passed"
                else "independent auditor result is missing or did not accept the current release"
            ),
        },
        "shipGate": {
            "status": "blocked",
            "blockingItems": [
                "release_aggregate_gate_required",
                "measurement_infrastructure_certification_required",
                "third_party_audit_rehearsal_gate_required",
            ],
            "reason": "independent audit result intake does not by itself prove production 100% readiness",
        },
        "privacyBoundary": contract["privacyBoundary"],
        "nonClaims": contract["nonClaims"],
    }
    _assert_no_sensitive(gate, area="independent audit result gate", contract=contract)
    return gate


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate redacted independent audit result bundle.")
    parser.add_argument("--independent-audit-result-json", type=Path)
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON)
    parser.add_argument("--expected-commit")
    return parser.parse_args(argv)


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        gate = build_gate(
            independent_audit_result_json=_resolve(args.independent_audit_result_json)
            if args.independent_audit_result_json
            else None,
            expected_commit=args.expected_commit,
        )
        output_json = _resolve(args.output_json)
        _write_json(output_json, gate)
        print(
            json.dumps(
                {
                    "status": gate["status"],
                    "kind": gate["kind"],
                    "auditResultGate": gate["auditResultGate"]["status"],
                    "shipGate": gate["shipGate"]["status"],
                    "acceptedResults": gate["summary"]["acceptedResults"],
                    "pendingResults": gate["summary"]["pendingResults"],
                    "rejectedResults": gate["summary"]["rejectedResults"],
                    "outputJson": str(output_json),
                },
                ensure_ascii=False,
                sort_keys=True,
            )
        )
        return 0
    except (IndependentAuditResultGateError, OSError, json.JSONDecodeError, subprocess.CalledProcessError) as exc:
        print(f"independent audit result gate error: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
