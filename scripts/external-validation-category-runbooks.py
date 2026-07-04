#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import defaultdict
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "contracts" / "fate" / "audit" / "external-validation-category-runbooks.json"
DEFAULT_OUTPUT_JSON = (
    ROOT / "infra" / "runtime" / "local-state" / "exports" / "audit" / "external-validation-category-runbooks.json"
)

WORK_QUEUE_KIND = "fatecat.external_validation_closure_work_queue"
OUTPUT_KIND = "fatecat.external_validation_category_runbooks"
RUNBOOK_STATUS = "operator_runbooks_ready"
REDACTION_RULE = (
    "Only record proof-ref handle, artifact sha256, issuer, captured/expires timestamps, status/count summary and "
    "command hash; remove endpoint URLs, credentials, payloads, user input and report body."
)
EXPIRY_POLICY = "Proof refs expire after 14 days unless the category-specific gate declares a shorter window."
VERIFIER_COMMAND = (
    "bash scripts/external-validation-proof-ref-gate.sh --work-queue-json <work-queue-json> "
    "--evidence-json <proof-ref-bundle-json> --output-json <proof-ref-gate-json>"
)

SENSITIVE_FRAGMENTS = {
    "BEGIN OPENSSH",
    "BEGIN RSA",
    "DATABASE_URL=",
    "DB_DSN=",
    "api_key=",
    "authorization:",
    "callback_url=",
    "password=",
    "private_key",
    "secret=",
    "token=",
    "webhook_url=",
}

FORBIDDEN_TEXT = {
    "dummy proof",
    "fake proof",
    "localhost proof",
    "placeholder proof",
}


class ExternalValidationCategoryRunbooksError(RuntimeError):
    """外部验证 category runbook gate 失败。"""


@dataclass(frozen=True)
class CategoryProfile:
    evidence_type: str
    required_credentials: tuple[str, ...]
    operator_commands: tuple[str, ...]
    proof_ref_slug: str
    failure_rollback: str
    closure_condition: str
    priority: str = "P0"
    status: str = "operator_action_required"


CATEGORY_PROFILES: dict[str, CategoryProfile] = {
    "audit.certification_current_evidence": CategoryProfile(
        evidence_type="current_certification_audit_bundle",
        required_credentials=("GitHub Actions read access", "current local evidence directory"),
        operator_commands=(
            "bash scripts/measurement-infrastructure-certification.sh --evidence-dir <local-ci-output-dir> --output-json <certification-json>",
            "bash scripts/current-audit-bundle.sh --output-dir <audit-output-dir> --local-ci-output-dir <local-ci-output-dir>",
        ),
        proof_ref_slug="audit-certification-current-evidence",
        failure_rollback="Keep certification canClaim100Percent=false and attach failed domain summary to audit handoff.",
        closure_condition="Current release, live gate, audit bundle, proof-ref gate and category runbooks are all regenerated for the same commit.",
    ),
    "audit.third_party_review": CategoryProfile(
        evidence_type="third_party_audit_review",
        required_credentials=("third-party auditor access", "redacted audit handoff package"),
        operator_commands=(
            "bash scripts/audit-handoff.sh --output-dir <audit-handoff-dir>",
            "bash scripts/audit-handoff-dry-run.sh --bundle-json <audit-handoff-json> --bundle-markdown <audit-handoff-md> --output-dir <dry-run-dir>",
        ),
        proof_ref_slug="audit-third-party-review",
        failure_rollback="Do not mark audit accepted; keep external audit review pending in certification.",
        closure_condition="Independent reviewer signs off the redacted audit package and all open external evidence items remain listed.",
    ),
    "delivery.multi_surface_live": CategoryProfile(
        evidence_type="multi_surface_live_parity",
        required_credentials=("production API access", "HF Space access", "Telegram Bot access"),
        operator_commands=(
            "bash scripts/production-readiness.sh --api-url <redacted-api-url> --require-live-bot",
            "bash scripts/multi-surface-semantic-diff.sh --output-json <semantic-diff-json>",
        ),
        proof_ref_slug="delivery-multi-surface-live",
        failure_rollback="Keep public release blocked and route users to the last verified surface.",
        closure_condition="API, Web/HF, Bot and CLI/Skill produce matching semantic hashes on the same redacted fixture.",
    ),
    "developer_platform.live": CategoryProfile(
        evidence_type="developer_platform_live",
        required_credentials=(
            "developer portal operator access",
            "sandbox token issuer access",
            "SDK package registry access",
        ),
        operator_commands=(
            "bash scripts/developer-platform-gate.sh --output-json <developer-platform-gate-json>",
            "bash scripts/developer-portal-gate.sh --output-json <developer-portal-gate-json>",
            "bash scripts/sandbox-access-gateway-gate.sh --output-json <sandbox-gateway-json>",
        ),
        proof_ref_slug="developer-platform-live",
        failure_rollback="Keep public developer onboarding disabled and publish local docs-only status.",
        closure_condition="Portal, SDK package metadata and sandbox token issue/revoke smoke are verified without exposing credentials.",
    ),
    "event_platform.live": CategoryProfile(
        evidence_type="event_platform_live",
        required_credentials=("event broker or webhook receiver access", "redacted event audit evidence"),
        operator_commands=(
            "bash scripts/event-contract-gate.sh --output-json <event-contract-gate-json>",
            "bash scripts/webhook-outbox-redelivery-smoke.sh --output-json <webhook-redelivery-json>",
        ),
        proof_ref_slug="event-platform-live",
        failure_rollback="Keep async delivery marked local-contract only and do not enable production event consumers.",
        closure_condition="CloudEvents-compatible job/webhook events are delivered, replayable and traceable in the external runtime.",
    ),
    "governance.external_validation_policy_guardrail": CategoryProfile(
        evidence_type="external_validation_policy_guardrail",
        required_credentials=("governance reviewer approval",),
        operator_commands=(
            "bash scripts/external-validation-closure-gate.sh --pending-external-json <pending-json> --output-json <closure-plan-json>",
        ),
        proof_ref_slug="governance-external-validation-policy-guardrail",
        failure_rollback="Keep the policy guardrail occurrence open and require reviewer sign-off before category closure.",
        closure_condition="Policy wording is reviewed and still forbids local dry-run, raw URL or synthetic evidence from closing live evidence.",
        priority="P1",
        status="policy_review_required",
    ),
    "manual_triage": CategoryProfile(
        evidence_type="manual_triage_assignment",
        required_credentials=("engineering audit owner assignment",),
        operator_commands=(
            "bash scripts/external-validation-closure-gate.sh --pending-external-json <pending-json> --output-json <closure-plan-json>",
        ),
        proof_ref_slug="manual-triage-assignment",
        failure_rollback="Keep occurrence under manual_triage and do not convert it to closed evidence.",
        closure_condition="Manual item is reclassified into a specific category with owner, evidence command and closure condition.",
        priority="P1",
        status="manual_triage_required",
    ),
    "observability.otel_slo_live": CategoryProfile(
        evidence_type="otel_slo_live",
        required_credentials=(
            "OTel collector access",
            "trace backend access",
            "metrics dashboard access",
            "alert route access",
        ),
        operator_commands=(
            "bash scripts/otel-collector-slo-gate.sh --output-json <otel-collector-json>",
            "bash scripts/otel-backend-slo-gate.sh --output-json <otel-backend-json>",
            "bash scripts/observability-slo-gate.sh --output-json <observability-slo-json>",
        ),
        proof_ref_slug="observability-otel-slo-live",
        failure_rollback="Keep SLO dashboards in staged mode and disable production-ready observability claim.",
        closure_condition="Collector, trace query, dashboard and alert route evidence are all captured with redacted proof refs.",
    ),
    "provider.external_dependency_live": CategoryProfile(
        evidence_type="provider_external_dependency_live",
        required_credentials=("provider dependency access", "license review owner approval"),
        operator_commands=(
            "bash scripts/provider-dependency-smoke.sh --output-json <provider-dependency-json>",
            "bash scripts/provider-drift-scanner.sh --output-json <provider-drift-json>",
            "bash scripts/provider-lifecycle-gate.sh --output-json <provider-lifecycle-json>",
        ),
        proof_ref_slug="provider-external-dependency-live",
        failure_rollback="Keep provider marked local dependency only and block promotion if source/license drift is unresolved.",
        closure_condition="Provider dependency execution, source/license lifecycle and drift evidence are verified for current commit.",
    ),
    "quality.external_evaluation_live": CategoryProfile(
        evidence_type="external_evaluation_live",
        required_credentials=("evaluation runner access", "benchmark artifact access", "human review owner approval"),
        operator_commands=(
            "bash scripts/mingli-bench-gate.sh --output-json <mingli-bench-json>",
            "bash scripts/core-quality-corpus-gate.sh --output-json <core-quality-json>",
            "bash scripts/evidence-coverage-trend-gate.sh --output-json <coverage-trend-json>",
        ),
        proof_ref_slug="quality-external-evaluation-live",
        failure_rollback="Keep benchmark result as local baseline and record failure taxonomy before promotion.",
        closure_condition="External benchmark summary, corpus trend and evidence coverage gate are attached without question-level leakage.",
    ),
    "release.artifact_current_commit": CategoryProfile(
        evidence_type="current_release_artifact_proof",
        required_credentials=(
            "GitHub Actions read access",
            "container registry read access",
            "attestation verification access",
        ),
        operator_commands=(
            "bash scripts/release-artifacts.sh --output-dir <release-artifacts-dir> --summary-json <release-summary-json>",
            "bash scripts/current-release-proof.sh --require-current-release --output-json <current-release-proof-json>",
        ),
        proof_ref_slug="release-artifact-current-commit",
        failure_rollback="Keep release proof blocked and do not promote image digest for the current commit.",
        closure_condition="Current commit CI, container digest, SBOM/provenance, attestation and rollback evidence all match.",
    ),
    "release.hf_space_live": CategoryProfile(
        evidence_type="hf_space_live_smoke",
        required_credentials=("HF Space operator access", "public Space URL", "release artifact access"),
        operator_commands=(
            "bash scripts/hf-space-deploy.sh --dry-run --space <redacted-space-id>",
            "bash scripts/production-readiness.sh --api-url <redacted-hf-space-url>",
        ),
        proof_ref_slug="release-hf-space-live",
        failure_rollback="Keep HF Space link marked external connectivity pending and leave prior stable Space untouched.",
        closure_condition="HF Space responds to health and report smoke using the current commit image or package.",
    ),
    "release.production_api_live": CategoryProfile(
        evidence_type="production_api_live_smoke",
        required_credentials=("production API URL", "production API token", "CORS policy access"),
        operator_commands=(
            "bash scripts/production-readiness.sh --api-url <redacted-api-url>",
            "bash scripts/live-release-gate.sh --require-live --output-json <live-release-gate-json>",
        ),
        proof_ref_slug="release-production-api-live",
        failure_rollback="Keep release gate blocked and route traffic to the last verified API deployment.",
        closure_condition="Production API health, readiness, authenticated report smoke and CORS evidence pass with redacted proof refs.",
    ),
    "release.telegram_bot_live": CategoryProfile(
        evidence_type="telegram_bot_live_smoke",
        required_credentials=("Telegram Bot token", "Bot webhook or polling access", "redacted chat test context"),
        operator_commands=(
            "bash scripts/live-release-gate.sh --run-live-bot --output-json <live-release-gate-json>",
            "bash scripts/production-readiness.sh --require-live-bot",
        ),
        proof_ref_slug="release-telegram-bot-live",
        failure_rollback="Disable Bot live claim and keep bot delivery in dry-run mode.",
        closure_condition="Telegram Bot accepts a redacted live smoke request and returns the same report contract as API/Web.",
    ),
    "runtime.multi_replica_live": CategoryProfile(
        evidence_type="multi_replica_runtime_live",
        required_credentials=("Postgres DSN", "worker deployment access", "metrics backend access"),
        operator_commands=(
            "bash scripts/multi-replica-runtime-evidence-assembler.sh --ack-external-live --output-json <runtime-evidence-json>",
            "bash scripts/multi-replica-runtime-gate.sh --evidence-json <runtime-evidence-json> --output-json <runtime-gate-json>",
        ),
        proof_ref_slug="runtime-multi-replica-live",
        failure_rollback="Scale down to single verified worker and keep exactly-once claims disabled.",
        closure_condition="Multiple workers run long enough to prove lease, heartbeat, restart recovery and no duplicate terminal job.",
    ),
    "runtime.postgres_live": CategoryProfile(
        evidence_type="postgres_runtime_live",
        required_credentials=("Postgres DSN", "migration owner access", "worker lease test access"),
        operator_commands=(
            "bash scripts/postgres-job-store-live-smoke.sh --require-live --output-json <postgres-live-json>",
            "bash scripts/postgres-worker-heartbeat-polling-smoke.sh --require-live --output-json <heartbeat-json>",
        ),
        proof_ref_slug="runtime-postgres-live",
        failure_rollback="Keep SQLite/local backend as default and block Postgres production promotion.",
        closure_condition="Postgres schema, job persistence, worker lease, heartbeat and restart recovery live smoke pass.",
    ),
    "runtime.public_webhook_live": CategoryProfile(
        evidence_type="public_webhook_live",
        required_credentials=("Postgres DSN", "public HTTPS webhook receiver", "webhook signing secret"),
        operator_commands=(
            "bash scripts/postgres-public-webhook-live-smoke.sh --require-live --output-json <public-webhook-json>",
            "bash scripts/runtime-proof-gate.sh --output-json <runtime-proof-json>",
        ),
        proof_ref_slug="runtime-public-webhook-live",
        failure_rollback="Keep public webhook delivery disabled and retain outbox retry records for inspection.",
        closure_condition="A real public HTTPS receiver gets a signed terminal callback and runtime proof gate accepts the evidence.",
    ),
    "security.external_secret_provider": CategoryProfile(
        evidence_type="external_secret_provider_live",
        required_credentials=("Vault or KMS access", "secret manager audit proof", "key rotation proof"),
        operator_commands=(
            "bash scripts/external-secret-provider-gate.sh --output-json <external-secret-json>",
            "bash scripts/security-externalization-gate.sh --output-json <security-externalization-json>",
        ),
        proof_ref_slug="security-external-secret-provider",
        failure_rollback="Keep local encrypted config vault only and block production secret externalization claim.",
        closure_condition="External Vault/KMS or secret manager proof refs pass gate without exposing secret values.",
    ),
    "security.externalization_live": CategoryProfile(
        evidence_type="security_externalization_live",
        required_credentials=("security owner approval", "IdP/SIEM/retention proof refs", "production policy access"),
        operator_commands=(
            "bash scripts/production-security-gate.sh --output-json <production-security-json>",
            "bash scripts/security-externalization-gate.sh --output-json <security-externalization-json>",
        ),
        proof_ref_slug="security-externalization-live",
        failure_rollback="Keep production security gate in staged mode and block public production claim.",
        closure_condition="OIDC, SIEM, retention cleaner, secret provider and OWASP controls are externally evidenced.",
    ),
    "security.identity_oidc": CategoryProfile(
        evidence_type="identity_oidc_live",
        required_credentials=(
            "IdP admin access",
            "OIDC issuer metadata",
            "JWKS read proof",
            "tenant authorization test account",
        ),
        operator_commands=(
            "bash scripts/security-externalization-gate.sh --output-json <security-externalization-json>",
            "bash scripts/security-smoke.sh --output-json <security-smoke-json>",
        ),
        proof_ref_slug="security-identity-oidc",
        failure_rollback="Keep local token smoke as the only accepted auth evidence and block OIDC production claim.",
        closure_condition="OIDC issuer/JWKS, scope enforcement and tenant negative authorization tests pass with redacted proof refs.",
    ),
    "security.retention_cleanup_live": CategoryProfile(
        evidence_type="retention_cleanup_live",
        required_credentials=("production retention scheduler access", "Postgres cleanup proof", "log retention proof"),
        operator_commands=(
            "bash scripts/retention-production-cleanup-gate.sh --output-json <retention-production-json>",
            "bash scripts/retention-cleanup.sh --dry-run --output-json <retention-dry-run-json>",
        ),
        proof_ref_slug="security-retention-cleanup-live",
        failure_rollback="Keep retention cleanup in dry-run mode and block data deletion claim until reviewer approval.",
        closure_condition="Production scheduler, records cleanup and log/SIEM retention evidence are redacted and accepted.",
    ),
    "security.siem_audit": CategoryProfile(
        evidence_type="siem_audit_live",
        required_credentials=("SIEM ingestion access", "immutable audit storage proof", "query proof owner approval"),
        operator_commands=(
            "bash scripts/security-externalization-gate.sh --output-json <security-externalization-json>",
            "bash scripts/audit-handoff-dry-run.sh --bundle-json <audit-handoff-json> --bundle-markdown <audit-handoff-md> --output-dir <dry-run-dir>",
        ),
        proof_ref_slug="security-siem-audit",
        failure_rollback="Keep SIEM live evidence pending and retain local audit logs only as non-production proof.",
        closure_condition="SIEM or immutable audit store ingestion, query and retention proof refs pass without raw log payload.",
    ),
}


def _utc_now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def _load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as fh:
        payload = json.load(fh)
    if not isinstance(payload, dict):
        raise ExternalValidationCategoryRunbooksError(f"JSON root must be object: {path}")
    return payload


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _short_hash(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:16]


def _stable_unique(values: list[str]) -> list[str]:
    return sorted({value for value in values if value})


def _render(payload: Any) -> str:
    return json.dumps(payload, ensure_ascii=False, sort_keys=True)


def _assert_no_forbidden(payload: Any, *, area: str) -> None:
    rendered = _render(payload).lower()
    bad = sorted(fragment for fragment in SENSITIVE_FRAGMENTS if fragment.lower() in rendered)
    if re.search(r"https?://", rendered, re.I):
        bad.append("raw_url")
    bad.extend(sorted(fragment for fragment in FORBIDDEN_TEXT if fragment in rendered))
    if bad:
        raise ExternalValidationCategoryRunbooksError(f"{area}: forbidden fragment detected: {', '.join(bad)}")


def _validate_work_queue(work_queue: dict[str, Any]) -> list[dict[str, Any]]:
    if work_queue.get("kind") != WORK_QUEUE_KIND:
        raise ExternalValidationCategoryRunbooksError(f"workQueue.kind must be {WORK_QUEUE_KIND}")
    work_items = work_queue.get("workItems")
    if not isinstance(work_items, list):
        raise ExternalValidationCategoryRunbooksError("workQueue.workItems must be array")
    validated: list[dict[str, Any]] = []
    for index, item in enumerate(work_items):
        if not isinstance(item, dict):
            raise ExternalValidationCategoryRunbooksError(f"work item {index} must be object")
        for field in (
            "id",
            "owner",
            "category",
            "priority",
            "status",
            "credentialDependencies",
            "requiredEvidence",
            "verificationCommands",
            "closureCondition",
            "occurrences",
        ):
            if field not in item:
                raise ExternalValidationCategoryRunbooksError(f"work item {index} missing {field}")
        if item["category"] not in CATEGORY_PROFILES:
            raise ExternalValidationCategoryRunbooksError(f"runbook profile missing for category: {item['category']}")
        for field in ("credentialDependencies", "requiredEvidence", "verificationCommands", "occurrences"):
            if not isinstance(item[field], list):
                raise ExternalValidationCategoryRunbooksError(f"work item {item['id']} field {field} must be array")
        validated.append(item)
    return validated


def _validate_contract(contract: dict[str, Any]) -> None:
    if contract.get("kind") != "fatecat.external_validation_category_runbooks_contract":
        raise ExternalValidationCategoryRunbooksError("contract.kind mismatch")
    missing = sorted(set(CATEGORY_PROFILES) - set(contract.get("knownCategories", [])))
    extra = sorted(set(contract.get("knownCategories", [])) - set(CATEGORY_PROFILES))
    if missing or extra:
        raise ExternalValidationCategoryRunbooksError(
            f"contract knownCategories mismatch missing={missing} extra={extra}"
        )
    required = set(contract.get("requiredFieldsPerRunbook", []))
    for field in ("proofRefArtifactPattern", "failureRollback", "closureCondition", "verifierCommand"):
        if field not in required:
            raise ExternalValidationCategoryRunbooksError(f"contract missing required runbook field: {field}")


def _proof_ref_pattern(category: str, profile: CategoryProfile) -> str:
    return f"evidence://external-validation/{profile.proof_ref_slug}/<run-id>"


def _build_runbook(category: str, items: list[dict[str, Any]]) -> dict[str, Any]:
    profile = CATEGORY_PROFILES[category]
    owners = _stable_unique([str(item["owner"]) for item in items])
    required_credentials = _stable_unique(
        list(profile.required_credentials)
        + [entry for item in items for entry in item.get("credentialDependencies", []) if isinstance(entry, str)]
    )
    operator_commands = _stable_unique(
        list(profile.operator_commands)
        + [entry for item in items for entry in item.get("verificationCommands", []) if isinstance(entry, str)]
        + [VERIFIER_COMMAND]
    )
    source_work_item_ids = _stable_unique([str(item["id"]) for item in items])
    occurrence_count = sum(len(item.get("occurrences") or []) for item in items)
    closure_conditions = _stable_unique(
        [str(item["closureCondition"]) for item in items if isinstance(item.get("closureCondition"), str)]
        + [profile.closure_condition]
    )
    runbook = {
        "id": f"external-runbook.{_short_hash(category)}",
        "category": category,
        "owners": owners,
        "priority": profile.priority,
        "status": profile.status,
        "evidenceType": profile.evidence_type,
        "requiredCredentials": required_credentials,
        "operatorCommands": operator_commands,
        "proofRefArtifactPattern": _proof_ref_pattern(category, profile),
        "redactionRule": REDACTION_RULE,
        "expiryPolicy": EXPIRY_POLICY,
        "failureRollback": profile.failure_rollback,
        "closureCondition": profile.closure_condition,
        "closureConditionsFromQueue": closure_conditions,
        "verifierCommand": VERIFIER_COMMAND,
        "sourceWorkItemIds": source_work_item_ids,
        "occurrenceCount": occurrence_count,
        "nonClaims": [
            "Runbook readiness does not prove live evidence has passed.",
            "Operator must attach a redacted proof-ref bundle before category closure can be reviewed.",
        ],
    }
    _assert_no_forbidden(runbook, area=f"runbook {category}")
    return runbook


def build_summary(*, work_queue_json: Path) -> dict[str, Any]:
    if not work_queue_json.is_file():
        raise ExternalValidationCategoryRunbooksError(f"work queue json missing: {work_queue_json}")
    contract = _load_json(CONTRACT_PATH)
    _validate_contract(contract)
    work_queue = _load_json(work_queue_json)
    work_items = _validate_work_queue(work_queue)

    by_category: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in work_items:
        by_category[str(item["category"])].append(item)

    runbooks = [_build_runbook(category, by_category[category]) for category in sorted(by_category)]
    ship_status = "blocked" if runbooks else "passed"
    summary = {
        "schemaVersion": 1,
        "kind": OUTPUT_KIND,
        "generatedAt": _utc_now(),
        "status": "passed",
        "source": {
            "workQueueJson": str(work_queue_json),
            "workQueueSha256": _sha256_file(work_queue_json),
            "workQueueKind": work_queue.get("kind"),
            "workItemCount": len(work_items),
        },
        "summary": {
            "categories": len(by_category),
            "runbooks": len(runbooks),
            "workItems": len(work_items),
            "occurrences": sum(runbook["occurrenceCount"] for runbook in runbooks),
            "knownCategoryProfiles": len(CATEGORY_PROFILES),
        },
        "runbookStatus": RUNBOOK_STATUS,
        "runbookGate": {
            "status": "passed",
            "policy": "All input categories must have an operator runbook profile before external live closure work starts.",
        },
        "shipGate": {
            "status": ship_status,
            "blockingItems": ["category_live_execution_pending", "proof_ref_evidence_pending"] if runbooks else [],
            "reason": (
                "category runbooks are ready for operators but live execution and proof-ref review are still pending"
                if runbooks
                else "no external validation category runbooks required"
            ),
            "policy": contract["runbookPolicy"]["shipGate"],
        },
        "runbooks": runbooks,
        "privacyBoundary": contract["privacyBoundary"],
        "nonClaims": contract["nonClaims"],
    }
    _assert_no_forbidden(summary, area="summary")
    return summary


def write_summary(summary: dict[str, Any], output_json: Path) -> None:
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build external validation category runbooks from work queue.")
    parser.add_argument(
        "--work-queue-json", type=Path, required=True, help="external-validation-closure-work-queue.json"
    )
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON, help="output category runbooks JSON")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        summary = build_summary(work_queue_json=args.work_queue_json)
        write_summary(summary, args.output_json)
        print(
            json.dumps(
                {
                    "status": summary["status"],
                    "runbookStatus": summary["runbookStatus"],
                    "shipGate": summary["shipGate"]["status"],
                    "runbooks": summary["summary"]["runbooks"],
                    "categories": summary["summary"]["categories"],
                    "outputJson": str(args.output_json),
                },
                ensure_ascii=False,
            )
        )
        return 0
    except (ExternalValidationCategoryRunbooksError, OSError, json.JSONDecodeError) as exc:
        print(f"external validation category runbooks error: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
