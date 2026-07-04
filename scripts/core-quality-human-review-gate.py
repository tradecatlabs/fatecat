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
CONTRACT_PATH = ROOT / "contracts" / "fate" / "evaluations" / "core-quality-human-review-gate.json"
RUBRIC_PATH = ROOT / "contracts" / "fate" / "evaluations" / "professional-quality-rubric.json"
DEFAULT_OUTPUT_JSON = (
    ROOT / "infra" / "runtime" / "local-state" / "exports" / "quality" / "core-quality-human-review-gate.json"
)

INPUT_KIND = "fatecat.core_quality_human_review_bundle"
OUTPUT_KIND = "fatecat.core_quality_human_review_gate"
PRIVACY_BOUNDARY = "redacted_no_secret_values"
ACCEPTED_REVIEW_DECISIONS = {"accepted_no_blockers", "accepted_with_findings"}
DIMENSION_PASS_DECISIONS = {"pass", "pass_with_findings"}

COMMIT_RE = re.compile(r"^[a-f0-9]{40}$")
SHA256_RE = re.compile(r"^[a-f0-9]{64}$")
ARTIFACT_REF_RE = re.compile(
    r"^(?:artifact|evidence|review-artifact|benchmark-artifact|ci-artifact):[A-Za-z0-9_.:/#@=-]+$"
)
SENSITIVE_RE = re.compile(
    r"(token\s*=|secret\s*=|password\s*=|passwd\s*=|DATABASE_URL\s*=|DB_DSN\s*=|"
    r"api[_-]?key\s*=|private[_-]?key|BEGIN (?:RSA|OPENSSH|PRIVATE)|authorization\s*:)",
    re.IGNORECASE,
)
RAW_URL_RE = re.compile(r"https?://", re.IGNORECASE)


class CoreQualityHumanReviewGateError(RuntimeError):
    """八字/紫微外部专家评审 intake gate 失败。"""


def _utc_now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def _load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as fh:
        payload = json.load(fh)
    if not isinstance(payload, dict):
        raise CoreQualityHumanReviewGateError(f"JSON root must be object: {path}")
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


def _assert_no_sensitive(payload: Any, *, area: str, contract: dict[str, Any]) -> None:
    rendered = _render(payload)
    if SENSITIVE_RE.search(rendered):
        raise CoreQualityHumanReviewGateError(f"{area}: sensitive-looking assignment detected")
    if RAW_URL_RE.search(rendered):
        raise CoreQualityHumanReviewGateError(f"{area}: raw URL detected")
    lower = rendered.lower()
    for marker in contract.get("forbiddenReportFragments", []):
        marker_text = str(marker).lower()
        if marker_text and marker_text in lower:
            raise CoreQualityHumanReviewGateError(f"{area}: forbidden marker detected: {marker}")


def _require_fields(payload: dict[str, Any], fields: list[str], *, area: str) -> None:
    for field in fields:
        if payload.get(field) in ("", None, []):
            raise CoreQualityHumanReviewGateError(f"{area} missing {field}")


def _validate_contract(contract: dict[str, Any]) -> None:
    if contract.get("kind") != "fatecat.core_quality_human_review_contract":
        raise CoreQualityHumanReviewGateError("contract.kind mismatch")
    required = set(contract.get("requiredOutputFields", []))
    for field in ("coreQualityHumanReview", "humanReviewGate", "externalBenchmarkGate", "noLeakGate"):
        if field not in required:
            raise CoreQualityHumanReviewGateError(f"contract missing output field: {field}")


def _validate_artifact_ref(value: str, *, field: str) -> None:
    if not ARTIFACT_REF_RE.match(value):
        raise CoreQualityHumanReviewGateError(f"{field} must be redacted artifact/evidence ref")


def _validate_sha256(value: str, *, field: str) -> None:
    if not SHA256_RE.match(value):
        raise CoreQualityHumanReviewGateError(f"{field} must be sha256 hex")


def _validate_non_negative_int(value: Any, *, field: str) -> int:
    if not isinstance(value, int) or value < 0:
        raise CoreQualityHumanReviewGateError(f"{field} must be non-negative integer")
    return value


def _validate_accuracy(value: Any, *, field: str) -> float:
    if not isinstance(value, int | float):
        raise CoreQualityHumanReviewGateError(f"{field} must be number")
    accuracy = float(value)
    if accuracy < 0 or accuracy > 1:
        raise CoreQualityHumanReviewGateError(f"{field} must be between 0 and 1")
    return accuracy


def _rubric_dimensions() -> set[str]:
    rubric = _load_json(RUBRIC_PATH)
    dimensions = rubric.get("dimensions")
    if not isinstance(dimensions, list) or not dimensions:
        raise CoreQualityHumanReviewGateError("professional rubric dimensions missing")
    return {str(item.get("id")) for item in dimensions if isinstance(item, dict) and item.get("id")}


def _validate_reviewed_artifacts(bundle: dict[str, Any], contract: dict[str, Any]) -> list[dict[str, Any]]:
    artifacts = bundle.get("reviewedArtifacts")
    if not isinstance(artifacts, list) or not artifacts:
        raise CoreQualityHumanReviewGateError("reviewedArtifacts must be non-empty array")
    required = set(contract.get("requiredArtifacts", []))
    seen_ids: set[str] = set()
    normalized: list[dict[str, Any]] = []
    for index, artifact in enumerate(artifacts):
        if not isinstance(artifact, dict):
            raise CoreQualityHumanReviewGateError(f"reviewedArtifacts[{index}] must be object")
        _require_fields(artifact, ["id", "kind", "sha256"], area=f"reviewedArtifacts[{index}]")
        artifact_id = str(artifact["id"])
        if artifact_id in seen_ids:
            raise CoreQualityHumanReviewGateError(f"reviewedArtifacts duplicate id: {artifact_id}")
        seen_ids.add(artifact_id)
        _validate_sha256(str(artifact["sha256"]), field=f"reviewedArtifacts[{index}].sha256")
        normalized.append({"id": artifact_id, "kind": str(artifact["kind"]), "sha256": str(artifact["sha256"])})
    missing = sorted(required - seen_ids)
    if missing:
        raise CoreQualityHumanReviewGateError(f"reviewedArtifacts missing required artifacts: {', '.join(missing)}")
    return normalized


def _validate_dimensions(
    professional_review: dict[str, Any], contract: dict[str, Any]
) -> tuple[list[dict[str, Any]], int]:
    dimensions = professional_review.get("dimensions")
    if not isinstance(dimensions, list) or not dimensions:
        raise CoreQualityHumanReviewGateError("professionalReview.dimensions must be non-empty array")
    required_ids = _rubric_dimensions()
    seen_ids: set[str] = set()
    normalized: list[dict[str, Any]] = []
    total_findings = 0
    for index, item in enumerate(dimensions):
        if not isinstance(item, dict):
            raise CoreQualityHumanReviewGateError(f"professionalReview.dimensions[{index}] must be object")
        _require_fields(item, contract["inputBundle"]["dimensionRequiredFields"], area=f"dimension[{index}]")
        dimension_id = str(item["id"])
        if dimension_id in seen_ids:
            raise CoreQualityHumanReviewGateError(f"duplicate dimension id: {dimension_id}")
        seen_ids.add(dimension_id)
        decision = str(item["decision"])
        if decision not in DIMENSION_PASS_DECISIONS:
            raise CoreQualityHumanReviewGateError(f"dimension {dimension_id} decision is not accepted: {decision}")
        _validate_artifact_ref(str(item["evidenceRef"]), field=f"dimension[{index}].evidenceRef")
        _validate_sha256(str(item["artifactSha256"]), field=f"dimension[{index}].artifactSha256")
        finding_count = _validate_non_negative_int(item["findingCount"], field=f"dimension[{index}].findingCount")
        total_findings += finding_count
        normalized.append(
            {
                "id": dimension_id,
                "decision": decision,
                "evidenceRef": str(item["evidenceRef"]),
                "artifactSha256": str(item["artifactSha256"]),
                "findingCount": finding_count,
            }
        )
    missing = sorted(required_ids - seen_ids)
    if missing:
        raise CoreQualityHumanReviewGateError(
            f"professionalReview.dimensions missing rubric dimensions: {', '.join(missing)}"
        )
    return normalized, total_findings


def _validate_bundle(
    *,
    bundle: dict[str, Any],
    bundle_sha256: str,
    expected_commit: str,
    contract: dict[str, Any],
) -> dict[str, Any]:
    if bundle.get("kind") != INPUT_KIND:
        raise CoreQualityHumanReviewGateError(f"core quality review bundle kind must be {INPUT_KIND}")
    if str(bundle.get("privacyBoundary", "")) != PRIVACY_BOUNDARY:
        raise CoreQualityHumanReviewGateError("privacyBoundary must be redacted_no_secret_values")

    input_contract = contract["inputBundle"]
    _require_fields(bundle, input_contract["requiredTopLevelFields"], area="bundle")
    source = bundle.get("source")
    reviewer = bundle.get("reviewer")
    professional_review = bundle.get("professionalReview")
    external_benchmark = bundle.get("externalBenchmark")
    no_leak_review = bundle.get("noLeakReview")
    if not all(
        isinstance(item, dict) for item in (source, reviewer, professional_review, external_benchmark, no_leak_review)
    ):
        raise CoreQualityHumanReviewGateError(
            "source, reviewer, professionalReview, externalBenchmark and noLeakReview must be objects"
        )
    assert isinstance(source, dict)
    assert isinstance(reviewer, dict)
    assert isinstance(professional_review, dict)
    assert isinstance(external_benchmark, dict)
    assert isinstance(no_leak_review, dict)
    _require_fields(source, input_contract["sourceRequiredFields"], area="source")
    _require_fields(reviewer, input_contract["reviewerRequiredFields"], area="reviewer")
    _require_fields(professional_review, input_contract["professionalReviewRequiredFields"], area="professionalReview")
    _require_fields(external_benchmark, input_contract["externalBenchmarkRequiredFields"], area="externalBenchmark")
    _require_fields(no_leak_review, input_contract["noLeakReviewRequiredFields"], area="noLeakReview")

    source_commit = str(source["commit"])
    if source_commit != expected_commit:
        raise CoreQualityHumanReviewGateError(
            f"core quality review commit {source_commit} does not match expected commit {expected_commit}"
        )
    if str(source["rubricVersion"]) != "professional-quality-rubric.v1":
        raise CoreQualityHumanReviewGateError("source.rubricVersion mismatch")
    if str(source["coreQualityCorpusManifest"]) != "contracts/fate/evaluations/core-quality-corpus.json":
        raise CoreQualityHumanReviewGateError("source.coreQualityCorpusManifest mismatch")
    _validate_artifact_ref(str(source["mingliBenchGateReportRef"]), field="source.mingliBenchGateReportRef")

    if str(reviewer["reviewerRole"]) not in {"professional_reviewer", "domain_expert", "external_quality_reviewer"}:
        raise CoreQualityHumanReviewGateError("reviewer.reviewerRole is not allowed")
    _validate_artifact_ref(str(reviewer["reviewerRef"]), field="reviewer.reviewerRef")
    _validate_sha256(str(reviewer["signedReviewArtifactSha256"]), field="reviewer.signedReviewArtifactSha256")

    review_decision = str(professional_review["decision"])
    if review_decision not in ACCEPTED_REVIEW_DECISIONS | {"rejected"}:
        raise CoreQualityHumanReviewGateError(f"unsupported professionalReview.decision: {review_decision}")
    if review_decision == "rejected":
        raise CoreQualityHumanReviewGateError("professionalReview.decision rejected")
    dimensions, total_findings = _validate_dimensions(professional_review, contract)

    if str(external_benchmark["decision"]) != contract["requiredExternalBenchmarkDecision"]:
        raise CoreQualityHumanReviewGateError("externalBenchmark.decision must be accepted")
    _validate_artifact_ref(str(external_benchmark["benchmarkRef"]), field="externalBenchmark.benchmarkRef")
    _validate_sha256(
        str(external_benchmark["aggregateArtifactSha256"]), field="externalBenchmark.aggregateArtifactSha256"
    )
    sample_count = _validate_non_negative_int(external_benchmark["sampleCount"], field="externalBenchmark.sampleCount")
    if sample_count <= 0:
        raise CoreQualityHumanReviewGateError("externalBenchmark.sampleCount must be positive")
    accuracy = _validate_accuracy(external_benchmark["accuracy"], field="externalBenchmark.accuracy")
    if external_benchmark.get("noPerQuestionLeak") is not True:
        raise CoreQualityHumanReviewGateError("externalBenchmark.noPerQuestionLeak must be true")

    if str(no_leak_review["decision"]) != contract["requiredNoLeakDecision"]:
        raise CoreQualityHumanReviewGateError("noLeakReview.decision must be passed")
    _validate_sha256(str(no_leak_review["privacyScanArtifactSha256"]), field="noLeakReview.privacyScanArtifactSha256")
    forbidden_found = _validate_non_negative_int(
        no_leak_review["forbiddenFragmentsFound"], field="noLeakReview.forbiddenFragmentsFound"
    )
    if forbidden_found != 0:
        raise CoreQualityHumanReviewGateError("noLeakReview.forbiddenFragmentsFound must be 0")
    if str(no_leak_review["redactionStatus"]) != PRIVACY_BOUNDARY:
        raise CoreQualityHumanReviewGateError("noLeakReview.redactionStatus must be redacted_no_secret_values")

    artifacts = _validate_reviewed_artifacts(bundle, contract)
    return {
        "bundleKind": INPUT_KIND,
        "bundleSha256": bundle_sha256,
        "commit": source_commit,
        "reviewerRole": str(reviewer["reviewerRole"]),
        "reviewerRef": str(reviewer["reviewerRef"]),
        "signedAt": str(reviewer["signedAt"]),
        "signedReviewArtifactSha256": str(reviewer["signedReviewArtifactSha256"]),
        "professionalReviewDecision": review_decision,
        "reviewedDimensions": dimensions,
        "dimensionCount": len(dimensions),
        "findingCount": total_findings,
        "externalBenchmark": {
            "decision": str(external_benchmark["decision"]),
            "benchmarkRef": str(external_benchmark["benchmarkRef"]),
            "aggregateArtifactSha256": str(external_benchmark["aggregateArtifactSha256"]),
            "sampleCount": sample_count,
            "accuracy": round(accuracy, 6),
            "noPerQuestionLeak": True,
        },
        "noLeakReview": {
            "decision": str(no_leak_review["decision"]),
            "privacyScanArtifactSha256": str(no_leak_review["privacyScanArtifactSha256"]),
            "forbiddenFragmentsFound": forbidden_found,
            "redactionStatus": PRIVACY_BOUNDARY,
        },
        "reviewedArtifacts": artifacts,
        "redactionStatus": PRIVACY_BOUNDARY,
    }


def _pending_result(expected_commit: str) -> dict[str, Any]:
    return {
        "bundleKind": None,
        "bundleSha256": None,
        "commit": expected_commit,
        "reviewerRole": None,
        "reviewerRef": None,
        "signedAt": None,
        "signedReviewArtifactSha256": None,
        "professionalReviewDecision": "missing",
        "reviewedDimensions": [],
        "dimensionCount": 0,
        "findingCount": 0,
        "externalBenchmark": {
            "decision": "missing",
            "benchmarkRef": None,
            "aggregateArtifactSha256": None,
            "sampleCount": 0,
            "accuracy": None,
            "noPerQuestionLeak": False,
        },
        "noLeakReview": {
            "decision": "missing",
            "privacyScanArtifactSha256": None,
            "forbiddenFragmentsFound": None,
            "redactionStatus": PRIVACY_BOUNDARY,
        },
        "reviewedArtifacts": [],
        "redactionStatus": PRIVACY_BOUNDARY,
    }


def build_gate(
    *,
    review_evidence_json: Path | None = None,
    expected_commit: str | None = None,
) -> dict[str, Any]:
    expected_commit = expected_commit or _current_commit()
    if not COMMIT_RE.match(expected_commit):
        raise CoreQualityHumanReviewGateError("--expected-commit must be 40 lowercase hex chars")

    contract = _load_json(CONTRACT_PATH)
    _validate_contract(contract)
    bundle_supplied = review_evidence_json is not None
    result_summary = _pending_result(expected_commit)
    human_review_status = "external_review_pending"
    benchmark_status = "external_benchmark_pending"
    no_leak_status = "external_no_leak_review_pending"
    human_gate_status = "blocked"
    human_blocking_items = [
        "professional_rubric_disposition_required",
        "external_benchmark_aggregate_required",
        "privacy_no_leak_signoff_required",
    ]

    if bundle_supplied:
        assert review_evidence_json is not None
        bundle = _load_json(review_evidence_json)
        _assert_no_sensitive(bundle, area="core_quality_human_review_bundle", contract=contract)
        result_summary = _validate_bundle(
            bundle=bundle,
            bundle_sha256=_sha256_file(review_evidence_json),
            expected_commit=expected_commit,
            contract=contract,
        )
        human_review_status = "accepted"
        benchmark_status = "accepted"
        no_leak_status = "accepted"
        human_gate_status = "passed"
        human_blocking_items = []

    summary = {
        "schemaVersion": 1,
        "kind": OUTPUT_KIND,
        "generatedAt": _utc_now(),
        "status": "passed",
        "source": {
            "contract": str(CONTRACT_PATH.relative_to(ROOT)),
            "professionalQualityRubric": str(RUBRIC_PATH.relative_to(ROOT)),
            "reviewEvidenceJson": str(review_evidence_json) if review_evidence_json else None,
            "reviewEvidenceBundleSha256": result_summary["bundleSha256"],
            "expectedCommit": expected_commit,
        },
        "humanReviewStatus": human_review_status,
        "externalBenchmarkStatus": benchmark_status,
        "noLeakReviewStatus": no_leak_status,
        "coreQualityHumanReview": result_summary,
        "humanReviewGate": {
            "status": human_gate_status,
            "blockingItems": human_blocking_items,
        },
        "externalBenchmarkGate": {
            "status": "passed" if benchmark_status == "accepted" else "blocked",
            "blockingItems": [] if benchmark_status == "accepted" else ["external_benchmark_aggregate_required"],
        },
        "noLeakGate": {
            "status": "passed" if no_leak_status == "accepted" else "blocked",
            "blockingItems": [] if no_leak_status == "accepted" else ["privacy_no_leak_signoff_required"],
        },
        "shipGate": {
            "status": "blocked",
            "blockingItems": ["final_measurement_infrastructure_certification_required"],
        },
        "summary": {
            "acceptedReviews": 1 if bundle_supplied else 0,
            "pendingReviews": 0 if bundle_supplied else 1,
            "reviewedDimensions": result_summary["dimensionCount"],
            "reviewedArtifacts": len(result_summary["reviewedArtifacts"]),
            "externalBenchmarkAccepted": benchmark_status == "accepted",
            "noLeakAccepted": no_leak_status == "accepted",
        },
        "privacyBoundary": contract["privacyBoundary"],
        "releaseBoundary": contract["releaseBoundary"],
        "nonClaims": contract["nonClaims"],
    }
    _assert_no_sensitive(summary, area="core_quality_human_review_gate", contract=contract)
    return summary


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="八字/紫微外部专家评审与 benchmark 证据 intake gate。")
    parser.add_argument("--review-evidence-json", type=Path, help="脱敏专家评审 / benchmark / no-leak evidence bundle.")
    parser.add_argument("--expected-commit", help="Expected current commit; defaults to git rev-parse HEAD.")
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON, help="Gate summary output JSON.")
    parser.add_argument("--require-accepted", action="store_true", help="Require accepted external review evidence.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        summary = build_gate(review_evidence_json=args.review_evidence_json, expected_commit=args.expected_commit)
        _write_json(args.output_json, summary)
        print(
            json.dumps(
                {
                    "kind": summary["kind"],
                    "status": summary["status"],
                    "humanReviewGate": summary["humanReviewGate"]["status"],
                    "externalBenchmarkGate": summary["externalBenchmarkGate"]["status"],
                    "noLeakGate": summary["noLeakGate"]["status"],
                    "shipGate": summary["shipGate"]["status"],
                    "acceptedReviews": summary["summary"]["acceptedReviews"],
                },
                ensure_ascii=False,
            )
        )
        if args.require_accepted and summary["humanReviewGate"]["status"] != "passed":
            return 1
        return 0
    except (CoreQualityHumanReviewGateError, OSError, json.JSONDecodeError, subprocess.CalledProcessError) as exc:
        print(f"core quality human review gate error: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
