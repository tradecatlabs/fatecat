#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = REPO_ROOT / "contracts" / "fate" / "audit" / "measurement-infrastructure-certification.json"
DEFAULT_OUTPUT_JSON = (
    REPO_ROOT
    / "infra"
    / "runtime"
    / "local-state"
    / "exports"
    / "certification"
    / "measurement-infrastructure-certification.json"
)


class CertificationGateError(RuntimeError):
    """测算基础设施认证聚合器发现结构性错误。"""


@dataclass(frozen=True)
class DomainSpec:
    domain_id: str
    title: str
    files: tuple[str, ...]
    pending_markers: tuple[str, ...] = ()
    blocked_markers: tuple[str, ...] = ()


DOMAIN_SPECS = (
    DomainSpec("provider", "Provider governance", ("provider-drift-trend-gate.json",)),
    DomainSpec(
        "core_quality",
        "Core bazi/ziwei quality",
        ("core-quality-corpus-gate.json", "mingli-bench-gate.json", "data-supply-chain-gate.json"),
    ),
    DomainSpec("event_platform", "Event platform", ("event-contract-gate.json",)),
    DomainSpec(
        "developer_platform",
        "Developer platform",
        ("developer-platform-gate.json", "developer-portal-gate.json", "sandbox-access-gateway-gate.json"),
        pending_markers=(
            "liveSandboxTokenService",
            "publishedSdkPackages",
            "livePublicTokenService",
            "externalPortalLive",
        ),
    ),
    DomainSpec(
        "security_privacy",
        "Security and privacy",
        (
            "production-security-gate.json",
            "security-externalization-gate.json",
            "retention-production-cleanup-gate.json",
            "external-secret-provider-gate.json",
        ),
        pending_markers=("liveEvidenceStatus",),
        blocked_markers=("shipGate",),
    ),
    DomainSpec(
        "observability_sre",
        "Observability and SRE",
        (
            "observability-slo-gate.json",
            "observability-trace-slo-smoke.json",
            "otel-collector-slo-gate.json",
            "otel-backend-slo-gate.json",
        ),
        pending_markers=("liveEvidenceStatus",),
    ),
    DomainSpec(
        "runtime",
        "Durable runtime",
        ("runtime-backend-gate.json", "multi-replica-runtime-gate.json", "runtime-proof-gate.json"),
        pending_markers=("liveEvidenceStatus", "runtimeProofStatus"),
        blocked_markers=("shipGate",),
    ),
    DomainSpec(
        "release",
        "Release proof",
        ("live-release-gate.json", "current-release-proof.json"),
        blocked_markers=("shipGate", "proofGate"),
    ),
    DomainSpec(
        "audit",
        "Audit handoff",
        ("current-audit-bundle/current-audit-bundle.json",),
        pending_markers=("pendingExternalValidationCount",),
        blocked_markers=("auditGate",),
    ),
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as fh:
        payload = json.load(fh)
    if not isinstance(payload, dict):
        raise CertificationGateError(f"JSON root must be object: {path}")
    return payload


def _utc_now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def _status_of(payload: dict[str, Any]) -> str:
    status = payload.get("status")
    if status in {"passed", "pass"}:
        return "passed"
    if status in {"blocked", "external_connectivity_pending"}:
        return "pending"
    if status in {"failed", "fail"}:
        return "failed"
    return "in-progress"


def _blocked_items(payload: dict[str, Any], markers: tuple[str, ...]) -> list[str]:
    items: list[str] = []
    for key in markers:
        gate = payload.get(key)
        if isinstance(gate, dict) and gate.get("status") in {"blocked", "failed", "fail"}:
            items.extend(str(item) for item in gate.get("blockingItems", []))
            if not items:
                items.append(f"{key}.status={gate.get('status')}")
        elif isinstance(gate, str) and gate in {"blocked", "failed", "fail"}:
            items.append(f"{key}={gate}")
    return items


def _pending_items(payload: dict[str, Any], markers: tuple[str, ...]) -> list[str]:
    items: list[str] = []
    for key in markers:
        value = payload.get(key)
        if isinstance(value, str) and "待执行" in value:
            items.append(f"{key}={value}")
        elif isinstance(value, str) and value in {"pending", "external_connectivity_pending"}:
            items.append(f"{key}={value}")
        elif value is False:
            items.append(f"{key}=not_live")
        elif type(value) is int:
            if key.endswith("Count") and value > 0:
                items.append(f"{key}={value}")
            elif not key.endswith("Count") and value == 0:
                items.append(f"{key}=not_live")
    return items


def _domain_status(evidence: list[dict[str, Any]], missing: list[str]) -> str:
    if missing:
        return "failed"
    statuses = {_status_of(item["payload"]) for item in evidence}
    blocked = any(item["blockingItems"] for item in evidence)
    pending = any(item["pendingItems"] for item in evidence)
    if "failed" in statuses:
        return "failed"
    if blocked:
        return "blocked"
    if pending:
        return "pending"
    if statuses == {"passed"}:
        return "passed"
    return "in-progress"


def _evaluate_domain(evidence_dir: Path, spec: DomainSpec) -> dict[str, Any]:
    evidence: list[dict[str, Any]] = []
    missing: list[str] = []
    for rel_path in spec.files:
        path = evidence_dir / rel_path
        if not path.is_file():
            missing.append(rel_path)
            continue
        payload = _load_json(path)
        evidence.append(
            {
                "path": str(path),
                "status": _status_of(payload),
                "blockingItems": _blocked_items(payload, spec.blocked_markers),
                "pendingItems": _pending_items(payload, spec.pending_markers),
                "payload": payload,
            }
        )
    status = _domain_status(evidence, missing)
    return {
        "id": spec.domain_id,
        "title": spec.title,
        "status": status,
        "missingEvidence": missing,
        "evidence": [
            {
                "path": item["path"],
                "status": item["status"],
                "blockingItems": item["blockingItems"],
                "pendingItems": item["pendingItems"],
            }
            for item in evidence
        ],
    }


def _assert_no_forbidden(summary: dict[str, Any], contract: dict[str, Any]) -> None:
    rendered = json.dumps(summary, ensure_ascii=False, sort_keys=True)
    forbidden = [item for item in contract["forbiddenReportFragments"] if item in rendered]
    if forbidden:
        raise CertificationGateError(f"certification summary contains forbidden fragments: {', '.join(forbidden)}")


def run_gate(*, evidence_dir: Path) -> dict[str, Any]:
    contract = _load_json(CONTRACT_PATH)
    if not evidence_dir.is_dir():
        raise CertificationGateError(f"evidence dir missing: {evidence_dir}")
    domains = [_evaluate_domain(evidence_dir, spec) for spec in DOMAIN_SPECS]
    blocking_items: list[dict[str, Any]] = []
    external_pending: list[dict[str, Any]] = []
    failed_domains: list[str] = []
    for domain in domains:
        if domain["status"] == "failed":
            failed_domains.append(domain["id"])
        if domain["status"] == "blocked":
            blocking_items.append({"domain": domain["id"], "reason": "blocked_gate"})
        for item in domain["evidence"]:
            for pending in item["pendingItems"]:
                external_pending.append({"domain": domain["id"], "path": item["path"], "reason": pending})
    if failed_domains:
        status = "failed"
    elif blocking_items or external_pending:
        status = "blocked"
    elif all(domain["status"] == "passed" for domain in domains):
        status = "passed"
    else:
        status = "in-progress"
    summary: dict[str, Any] = {
        "schemaVersion": 1,
        "kind": "fatecat.measurement_infrastructure_certification",
        "generatedAt": _utc_now(),
        "status": status,
        "certificationGate": {
            "canClaim100Percent": status == "passed",
            "policy": "Only status=passed can support a 100% measurement infrastructure claim.",
            "failedDomains": failed_domains,
        },
        "domains": domains,
        "externalPending": external_pending,
        "blockingItems": blocking_items,
        "evidenceDir": str(evidence_dir),
        "privacyBoundary": contract["privacyBoundary"],
        "releaseBoundary": contract["releaseBoundary"],
        "nonClaims": contract["nonClaims"],
    }
    _assert_no_forbidden(summary, contract)
    return summary


def write_summary(summary: dict[str, Any], output_json: Path) -> None:
    output_json.parent.mkdir(parents=True, exist_ok=True)
    with output_json.open("w", encoding="utf-8") as fh:
        json.dump(summary, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="聚合测算基础设施 100% certification dry-run 证据。")
    parser.add_argument(
        "--evidence-dir", type=Path, required=True, help="local-ci output dir containing gate artifacts."
    )
    parser.add_argument(
        "--output-json", type=Path, default=DEFAULT_OUTPUT_JSON, help="certification summary output JSON."
    )
    parser.add_argument("--require-certified", action="store_true", help="Require status=passed; otherwise exit 1.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        summary = run_gate(evidence_dir=args.evidence_dir)
        write_summary(summary, args.output_json)
        print(
            json.dumps(
                {
                    "status": summary["status"],
                    "canClaim100Percent": summary["certificationGate"]["canClaim100Percent"],
                    "domains": len(summary["domains"]),
                    "externalPending": len(summary["externalPending"]),
                    "blockingItems": len(summary["blockingItems"]),
                },
                ensure_ascii=False,
            )
        )
        if args.require_certified and summary["status"] != "passed":
            return 1
        return 0 if summary["status"] in {"passed", "blocked", "in-progress"} else 1
    except (CertificationGateError, OSError, json.JSONDecodeError) as exc:
        print(f"measurement infrastructure certification error: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
