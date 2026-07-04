#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_CONTRACT_PATH = ROOT / "contracts" / "fate" / "evaluations" / "core-quality-human-review-bundle-template.json"
TARGET_GATE_CONTRACT_PATH = ROOT / "contracts" / "fate" / "evaluations" / "core-quality-human-review-gate.json"
RUBRIC_PATH = ROOT / "contracts" / "fate" / "evaluations" / "professional-quality-rubric.json"
DEFAULT_OUTPUT_JSON = (
    ROOT
    / "infra"
    / "runtime"
    / "local-state"
    / "exports"
    / "quality"
    / "core-quality-human-review-bundle-template.json"
)
DEFAULT_OUTPUT_TEXT = (
    ROOT / "infra" / "runtime" / "local-state" / "exports" / "quality" / "CORE_QUALITY_HUMAN_REVIEW_BUNDLE_TEMPLATE.md"
)

OUTPUT_KIND = "fatecat.core_quality_human_review_bundle_template"
TARGET_BUNDLE_KIND = "fatecat.core_quality_human_review_bundle"
PRIVACY_BOUNDARY = "redacted_no_secret_values"
REVIEWER_ROLES = ["professional_reviewer", "domain_expert", "external_quality_reviewer"]

COMMIT_RE = re.compile(r"^[a-f0-9]{40}$")
SENSITIVE_RE = re.compile(
    r"(token\s*=|secret\s*=|password\s*=|passwd\s*=|DATABASE_URL\s*=|DB_DSN\s*=|"
    r"api[_-]?key\s*=|private[_-]?key|BEGIN (?:RSA|OPENSSH|PRIVATE)|authorization\s*:)",
    re.IGNORECASE,
)
RAW_URL_RE = re.compile(r"https?://", re.IGNORECASE)
FORBIDDEN_TEXT = ("placeholder proof", "fake proof", "dummy proof", "localhost proof")


class CoreQualityHumanReviewBundleTemplateError(RuntimeError):
    """八字/紫微 core quality 人审 bundle 模板生成失败。"""


def _utc_now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def _load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as fh:
        payload = json.load(fh)
    if not isinstance(payload, dict):
        raise CoreQualityHumanReviewBundleTemplateError(f"JSON root must be object: {path}")
    return payload


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _write_text(path: Path, payload: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload, encoding="utf-8")


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
        raise CoreQualityHumanReviewBundleTemplateError(f"{area}: sensitive-looking assignment detected")
    if RAW_URL_RE.search(rendered):
        raise CoreQualityHumanReviewBundleTemplateError(f"{area}: raw URL detected")
    lower = rendered.lower()
    for marker in FORBIDDEN_TEXT:
        if marker in lower:
            raise CoreQualityHumanReviewBundleTemplateError(f"{area}: forbidden marker detected: {marker}")


def _validate_template_contract(contract: dict[str, Any]) -> None:
    if contract.get("kind") != "fatecat.core_quality_human_review_bundle_template_contract":
        raise CoreQualityHumanReviewBundleTemplateError("template contract kind mismatch")
    required = set(contract.get("requiredOutputFields", []))
    for field in ("bundleSkeleton", "artifactHashInstructions", "noLeakChecklist", "gateExpectation"):
        if field not in required:
            raise CoreQualityHumanReviewBundleTemplateError(f"template contract missing required field: {field}")
    policy = contract.get("templatePolicy")
    if not isinstance(policy, dict) or policy.get("acceptedByTargetGate") is not False:
        raise CoreQualityHumanReviewBundleTemplateError("template contract must declare acceptedByTargetGate=false")


def _validate_target_contract(contract: dict[str, Any]) -> None:
    if contract.get("kind") != "fatecat.core_quality_human_review_contract":
        raise CoreQualityHumanReviewBundleTemplateError("target gate contract kind mismatch")
    if contract.get("inputKind") != TARGET_BUNDLE_KIND:
        raise CoreQualityHumanReviewBundleTemplateError("target gate inputKind mismatch")
    if contract.get("privacyBoundary") != PRIVACY_BOUNDARY:
        raise CoreQualityHumanReviewBundleTemplateError("target gate privacy boundary mismatch")


def _rubric_dimensions(rubric: dict[str, Any]) -> list[dict[str, Any]]:
    dimensions = rubric.get("dimensions")
    if not isinstance(dimensions, list) or not dimensions:
        raise CoreQualityHumanReviewBundleTemplateError("rubric dimensions missing")
    normalized: list[dict[str, Any]] = []
    for index, item in enumerate(dimensions):
        if not isinstance(item, dict) or not item.get("id"):
            raise CoreQualityHumanReviewBundleTemplateError(f"rubric dimension {index} missing id")
        normalized.append(
            {
                "id": str(item["id"]),
                "name": str(item.get("name", "")),
                "capabilities": list(item.get("capabilities", [])),
                "requiredSignals": list(item.get("requiredSignals", [])),
                "decisionOptions": ["pass", "pass_with_findings"],
                "requiredEvidenceRefPrefix": "review-artifact:",
            }
        )
    return normalized


def _artifact_hash_instructions(target_contract: dict[str, Any]) -> list[dict[str, str]]:
    instructions = []
    for artifact_id in target_contract.get("requiredArtifacts", []):
        instructions.append(
            {
                "artifactId": str(artifact_id),
                "sha256Command": "sha256sum <redacted-artifact-file>",
                "expectedField": "reviewedArtifacts[].sha256",
                "acceptedFormat": "64 lowercase hex chars",
                "storageBoundary": "hash only; keep raw artifact outside repository unless it is already safe and tracked",
            }
        )
    return instructions


def _bundle_skeleton(
    *,
    expected_commit: str,
    target_contract: dict[str, Any],
    dimensions: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "schemaVersion": 1,
        "kind": TARGET_BUNDLE_KIND,
        "source": {
            "commit": expected_commit,
            "rubricVersion": "professional-quality-rubric.v1",
            "coreQualityCorpusManifest": "contracts/fate/evaluations/core-quality-corpus.json",
            "mingliBenchGateReportRef": "ci-artifact:<redacted-mingli-bench-gate-summary>",
        },
        "reviewer": {
            "reviewerRole": f"<one-of:{'|'.join(REVIEWER_ROLES)}>",
            "reviewerRef": "review-artifact:<redacted-reviewer-ref>",
            "signedAt": "<UTC timestamp>",
            "signedReviewArtifactSha256": "<sha256-64-lowercase-hex>",
        },
        "professionalReview": {
            "decision": "<accepted_no_blockers|accepted_with_findings>",
            "dimensions": [
                {
                    "id": item["id"],
                    "decision": "<pass|pass_with_findings>",
                    "evidenceRef": f"review-artifact:<redacted-{item['id'].replace('.', '-')}-evidence>",
                    "artifactSha256": "<sha256-64-lowercase-hex>",
                    "findingCount": "<non-negative-integer>",
                }
                for item in dimensions
            ],
        },
        "externalBenchmark": {
            "decision": "accepted",
            "benchmarkRef": "benchmark-artifact:<redacted-external-benchmark-aggregate>",
            "aggregateArtifactSha256": "<sha256-64-lowercase-hex>",
            "sampleCount": "<positive-integer>",
            "accuracy": "<0-to-1-aggregate-number>",
            "noPerQuestionLeak": "<true-after-review>",
        },
        "noLeakReview": {
            "decision": "passed",
            "privacyScanArtifactSha256": "<sha256-64-lowercase-hex>",
            "forbiddenFragmentsFound": 0,
            "redactionStatus": PRIVACY_BOUNDARY,
        },
        "reviewedArtifacts": [
            {
                "id": str(artifact_id),
                "kind": f"fatecat.{str(artifact_id).replace('-', '_')}",
                "sha256": "<sha256-64-lowercase-hex>",
            }
            for artifact_id in target_contract.get("requiredArtifacts", [])
        ],
        "privacyBoundary": PRIVACY_BOUNDARY,
    }


def build_template(*, expected_commit: str | None = None) -> dict[str, Any]:
    expected_commit = expected_commit or _current_commit()
    if not COMMIT_RE.match(expected_commit):
        raise CoreQualityHumanReviewBundleTemplateError("--expected-commit must be 40 lowercase hex chars")

    template_contract = _load_json(TEMPLATE_CONTRACT_PATH)
    target_contract = _load_json(TARGET_GATE_CONTRACT_PATH)
    rubric = _load_json(RUBRIC_PATH)
    _validate_template_contract(template_contract)
    _validate_target_contract(target_contract)
    dimensions = _rubric_dimensions(rubric)

    template = {
        "schemaVersion": 1,
        "kind": OUTPUT_KIND,
        "status": "operator_action_required",
        "generatedAt": _utc_now(),
        "source": {
            "templateContract": str(TEMPLATE_CONTRACT_PATH.relative_to(ROOT)),
            "targetGateContract": str(TARGET_GATE_CONTRACT_PATH.relative_to(ROOT)),
            "professionalQualityRubric": str(RUBRIC_PATH.relative_to(ROOT)),
            "targetGateCommand": template_contract["targetGateCommand"],
            "commit": expected_commit,
        },
        "summary": {
            "targetBundleKind": TARGET_BUNDLE_KIND,
            "rubricDimensions": len(dimensions),
            "requiredReviewedArtifacts": len(target_contract.get("requiredArtifacts", [])),
            "readyToSubmitToGate": False,
            "templateAcceptedByTargetGate": False,
        },
        "templateGate": {
            "status": "operator_action_required",
            "blockingItems": [
                "professional_reviewer_disposition_required",
                "external_benchmark_aggregate_required",
                "no_leak_signoff_required",
                "sha256_fields_must_be_filled",
            ],
            "reason": "template is ready for operator rehearsal, but contains placeholders and is intentionally not accepted evidence",
        },
        "templatePolicy": template_contract["templatePolicy"],
        "bundleSkeleton": _bundle_skeleton(
            expected_commit=expected_commit,
            target_contract=target_contract,
            dimensions=dimensions,
        ),
        "dimensionChecklist": dimensions,
        "artifactHashInstructions": _artifact_hash_instructions(target_contract),
        "noLeakChecklist": {
            "forbiddenFragmentSource": template_contract["noLeakPolicy"]["forbiddenFragmentSource"],
            "requiredResult": template_contract["noLeakPolicy"]["requiredResult"],
            "redactionStatus": PRIVACY_BOUNDARY,
            "checks": [
                "verify bundle contains only artifact refs, aggregate stats, sha256 hashes and role names",
                "verify reviewer identity, real birth data, benchmark item details and report body are absent",
                "scan final bundle with core-quality-human-review-gate before submission",
                "store only the accepted gate summary and redacted bundle hash in release evidence",
            ],
        },
        "operatorChecklist": [
            {
                "step": "prepare-redacted-artifacts",
                "command": "sha256sum <redacted-artifact-file>",
                "expectedEvidence": "64 lowercase hex digest for every reviewed artifact",
            },
            {
                "step": "fill-bundle-outside-repo",
                "command": "cp <template-json> <redacted-bundle-json>",
                "expectedEvidence": "all placeholders replaced with redacted refs, aggregate values and hashes",
            },
            {
                "step": "run-target-gate",
                "command": template_contract["targetGateCommand"],
                "expectedEvidence": "humanReviewGate, externalBenchmarkGate and noLeakGate are passed",
            },
            {
                "step": "keep-certification-blocked-until-all-domains-pass",
                "command": "bash scripts/measurement-infrastructure-certification.sh --evidence-dir <local-ci-output-dir> --require-certified",
                "expectedEvidence": "only final all-domain evidence may set canClaim100Percent true",
            },
        ],
        "gateExpectation": {
            "templateAcceptedByTargetGate": False,
            "expectedTargetGateResultWhenTemplateIsUsedDirectly": "rejected",
            "expectedReason": "template output kind is not the target evidence kind and skeleton contains placeholders",
            "targetGateCommand": template_contract["targetGateCommand"],
        },
        "privacyBoundary": PRIVACY_BOUNDARY,
        "releaseBoundary": template_contract["releaseBoundary"],
        "nonClaims": template_contract["nonClaims"],
    }
    _assert_no_sensitive(template, area="core quality human review bundle template")
    return template


def _render_text(template: dict[str, Any]) -> str:
    lines = [
        "# Core Quality Human Review Bundle Template",
        "",
        f"- Status: `{template['status']}`",
        f"- Template gate: `{template['templateGate']['status']}`",
        f"- Rubric dimensions: `{template['summary']['rubricDimensions']}`",
        f"- Required reviewed artifacts: `{template['summary']['requiredReviewedArtifacts']}`",
        f"- Ready to submit to gate: `{str(template['summary']['readyToSubmitToGate']).lower()}`",
        "",
        "## Hash Instructions",
        "",
    ]
    for item in template["artifactHashInstructions"]:
        lines.extend(
            [
                f"### {item['artifactId']}",
                "",
                f"- Command: `{item['sha256Command']}`",
                f"- Expected field: `{item['expectedField']}`",
                f"- Accepted format: `{item['acceptedFormat']}`",
                "",
            ]
        )
    lines.extend(["## Dimension Checklist", ""])
    for item in template["dimensionChecklist"]:
        signals = ", ".join(item["requiredSignals"])
        lines.extend(
            [
                f"### {item['id']}",
                "",
                f"- Name: `{item['name']}`",
                f"- Capabilities: `{', '.join(item['capabilities'])}`",
                f"- Required signals: `{signals}`",
                "- Required output fields: `decision`, `evidenceRef`, `artifactSha256`, `findingCount`",
                "",
            ]
        )
    lines.extend(
        [
            "## No-Leak Checklist",
            "",
            f"- Forbidden fragment source: `{template['noLeakChecklist']['forbiddenFragmentSource']}`",
            f"- Required result: `{template['noLeakChecklist']['requiredResult']}`",
            f"- Redaction status: `{template['noLeakChecklist']['redactionStatus']}`",
            "",
            "## Operator Checklist",
            "",
        ]
    )
    for item in template["operatorChecklist"]:
        lines.extend(
            [
                f"### {item['step']}",
                "",
                f"- Command: `{item['command']}`",
                f"- Expected evidence: `{item['expectedEvidence']}`",
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
    _assert_no_sensitive(rendered, area="template text")
    return rendered


def write_template(*, template: dict[str, Any], output_json: Path, output_text: Path) -> None:
    _write_json(output_json, template)
    _write_text(output_text, _render_text(template))


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build core quality human review bundle rehearsal template.")
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON)
    parser.add_argument("--output-markdown", type=Path, default=DEFAULT_OUTPUT_TEXT)
    parser.add_argument("--expected-commit")
    return parser.parse_args(argv)


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        template = build_template(expected_commit=args.expected_commit)
        output_json = _resolve(args.output_json)
        output_text = _resolve(args.output_markdown)
        write_template(template=template, output_json=output_json, output_text=output_text)
        print(
            json.dumps(
                {
                    "kind": template["kind"],
                    "status": template["status"],
                    "templateGate": template["templateGate"]["status"],
                    "rubricDimensions": template["summary"]["rubricDimensions"],
                    "requiredReviewedArtifacts": template["summary"]["requiredReviewedArtifacts"],
                    "readyToSubmitToGate": template["summary"]["readyToSubmitToGate"],
                    "templateAcceptedByTargetGate": template["summary"]["templateAcceptedByTargetGate"],
                    "outputJson": str(output_json),
                    "outputMarkdown": str(output_text),
                },
                ensure_ascii=False,
                sort_keys=True,
            )
        )
        return 0
    except (
        CoreQualityHumanReviewBundleTemplateError,
        OSError,
        json.JSONDecodeError,
        subprocess.CalledProcessError,
    ) as exc:
        print(f"core quality human review bundle template error: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
