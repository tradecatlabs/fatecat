#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = REPO_ROOT / "contracts" / "fate" / "audit" / "external-validation-closure.json"
DEFAULT_OUTPUT_JSON = (
    REPO_ROOT / "infra" / "runtime" / "local-state" / "exports" / "audit" / "external-validation-closure-gate.json"
)
FORBIDDEN_MARKERS = (
    "token=",
    "secret=",
    "password=",
    "passwd=",
    "private_key=",
    "DATABASE_URL=",
    "DB_DSN=",
    "BEGIN RSA",
    "BEGIN OPENSSH",
)


class ExternalValidationClosureError(RuntimeError):
    """外部待验证项关闭计划生成失败。"""


@dataclass(frozen=True)
class ClosureProfile:
    category: str
    owner: str
    credential_dependencies: tuple[str, ...]
    required_evidence: tuple[str, ...]
    verification_commands: tuple[str, ...]
    closure_condition: str
    keywords: tuple[str, ...]


PROFILES = (
    ClosureProfile(
        category="release.production_api_live",
        owner="release-ops",
        credential_dependencies=("FATE_LIVE_API_URL", "FATE_API_TOKEN or scoped production token", "CORS allowlist"),
        required_evidence=(
            "HTTPS production API /health passed",
            "HTTPS production API /ready passed",
            "HTTPS production API /metrics contains fatecat_requests_total",
            "CORS/token smoke passed",
        ),
        verification_commands=(
            "bash scripts/production-readiness.sh --api-url <真实API域名>",
            "bash scripts/live-release-gate.sh --api-url <真实API域名> --output-json <path>",
        ),
        closure_condition="真实生产 API 域名、TLS、健康检查、ready、metrics、CORS/token smoke 均通过。",
        keywords=(
            "production api",
            "api url",
            "真实 api",
            "真实api",
            "cors",
            "生产 api",
            "生产域名",
            "/health",
            "/ready",
        ),
    ),
    ClosureProfile(
        category="release.hf_space_live",
        owner="release-ops",
        credential_dependencies=("FATE_HF_SPACE_URL", "Hugging Face Space access when private"),
        required_evidence=("HF Space /web returns 2xx", "HF Space page contains FateCat marker"),
        verification_commands=(
            "bash scripts/live-release-gate.sh --hf-space-url <真实HF Space URL> --output-json <path>",
        ),
        closure_condition="真实 Hugging Face Space /web 可访问并返回 FateCat 页面标记。",
        keywords=("hf space", "hugging face", "hf-space", "hf_space", "hf.space", "space /web"),
    ),
    ClosureProfile(
        category="release.telegram_bot_live",
        owner="bot-ops",
        credential_dependencies=("FATE_BOT_TOKEN", "Telegram Bot network access"),
        required_evidence=("Telegram getMe live smoke passed", "Bot token redacted in output"),
        verification_commands=(
            "bash scripts/live-bot-smoke.sh  # requires FATE_BOT_TOKEN loaded from secret store",
            "bash scripts/live-release-gate.sh --run-live-bot --output-json <path>  # requires FATE_BOT_TOKEN loaded from secret store",
        ),
        closure_condition="真实 Telegram Bot token 存在，live smoke 成功，输出不泄露 token。",
        keywords=("telegram", "bot token", "fate_bot_token", "bot live", "live bot"),
    ),
    ClosureProfile(
        category="runtime.public_webhook_live",
        owner="runtime-ops",
        credential_dependencies=("FATE_REPORT_JOB_DATABASE_URL", "public HTTPS webhook receiver", "webhook secret"),
        required_evidence=("Postgres public webhook live smoke passed", "Receiver signature verification evidence"),
        verification_commands=(
            "bash scripts/postgres-public-webhook-live-smoke.sh --output-json <path>  # requires FATE_REPORT_JOB_DATABASE_URL loaded from secret store",
            "bash scripts/runtime-proof-gate.sh --public-webhook-summary <path> --output-json <path>",
        ),
        closure_condition="真实 Postgres 后端和公网 HTTPS webhook receiver 完成 live smoke。",
        keywords=("public webhook", "公网 webhook", "webhook receiver", "callback", "真实 webhook", "receiver"),
    ),
    ClosureProfile(
        category="runtime.postgres_live",
        owner="runtime-ops",
        credential_dependencies=("FATE_REPORT_JOB_DATABASE_URL", "Postgres network access"),
        required_evidence=("Postgres job store live smoke passed", "worker lease smoke passed with real Postgres"),
        verification_commands=(
            "bash scripts/postgres-job-store-live-smoke.sh --output-json <path>  # requires FATE_REPORT_JOB_DATABASE_URL loaded from secret store",
            "bash scripts/postgres-worker-heartbeat-polling-smoke.sh --output-json <path>  # requires FATE_REPORT_JOB_DATABASE_URL loaded from secret store",
        ),
        closure_condition="真实 Postgres DSN 下 job store、worker lease、heartbeat/polling smoke 均通过。",
        keywords=("postgres", "fate_report_job_database_url", "database_url", "dsn", "数据库", "worker lease"),
    ),
    ClosureProfile(
        category="runtime.multi_replica_live",
        owner="runtime-ops",
        credential_dependencies=(
            "multi-replica runtime environment",
            "external backend access",
            "worker/process supervisor access",
        ),
        required_evidence=(
            "multi-replica runtime evidence gate accepted live proof",
            "restart/lease/heartbeat evidence attached",
            "exactly-once overclaim is absent",
        ),
        verification_commands=(
            "bash scripts/multi-replica-runtime-gate.sh --evidence-json <redacted-proof.json> --output-json <path>",
            "bash scripts/runtime-proof-gate.sh --output-json <path>",
        ),
        closure_condition="长期多副本 runtime、external backend、worker restart/lease/heartbeat 证据通过，且不声明 exactly-once。",
        keywords=(
            "multi-replica",
            "multi_replica",
            "多副本",
            "multi-worker",
            "external backend",
            "external runtime",
            "production worker restart",
            "worker restart",
            "任务继续执行",
            "生产锁",
            "长期运行",
            "exactly-once",
        ),
    ),
    ClosureProfile(
        category="event_platform.live",
        owner="platform-events",
        credential_dependencies=("external broker/webhook subscriber access when required",),
        required_evidence=(
            "event contract gate passed",
            "live event delivery proof attached when required",
            "CloudEvents/AsyncAPI compatibility evidence present",
        ),
        verification_commands=(
            "bash scripts/event-contract-gate.sh --output-json <path>",
            "bash scripts/webhook-smoke.sh --output-json <path>",
        ),
        closure_condition="job/webhook/evaluation/release 事件的 contract、delivery 和 live 订阅证据按要求闭合。",
        keywords=(
            "events.json",
            "event-contract",
            "event contract",
            "liveevidence",
            "asyncevent",
            "cloudevents",
            "asyncapi",
            "event platform",
            "事件",
            "外部 broker",
        ),
    ),
    ClosureProfile(
        category="security.external_secret_provider",
        owner="security-ops",
        credential_dependencies=("Vault/KMS/secret manager credentials", "FATE_EXTERNAL_SECRET_PROVIDER_EVIDENCE"),
        required_evidence=("external secret provider live evidence accepted", "no local static secret fallback"),
        verification_commands=(
            "bash scripts/external-secret-provider-gate.sh --evidence-json <redacted-proof.json> --output-json <path>",
        ),
        closure_condition="真实 Vault/KMS/secret manager proof-ref 通过 gate，且无真实 secret 输出。",
        keywords=("vault", "kms", "secret provider", "external secret", "secret manager", "fernet", "密钥"),
    ),
    ClosureProfile(
        category="security.identity_oidc",
        owner="security-ops",
        credential_dependencies=("OIDC/IdP tenant", "client credentials or signed proof ref"),
        required_evidence=("OIDC login/token validation proof ref accepted", "RBAC scope smoke passed"),
        verification_commands=(
            "bash scripts/security-externalization-gate.sh --evidence-json <redacted-proof.json> --output-json <path>",
        ),
        closure_condition="真实 IdP/OIDC 和 RBAC proof-ref 通过安全外部化 gate。",
        keywords=("oidc", "idp", "oauth", "identity", "rbac", "scoped token", "用户 token"),
    ),
    ClosureProfile(
        category="security.siem_audit",
        owner="security-ops",
        credential_dependencies=("SIEM workspace", "immutable audit storage proof ref"),
        required_evidence=("SIEM ingestion proof accepted", "immutable audit storage proof accepted"),
        verification_commands=(
            "bash scripts/security-externalization-gate.sh --evidence-json <redacted-proof.json> --output-json <path>",
        ),
        closure_condition="真实 SIEM/不可变审计存储 proof-ref 通过 gate。",
        keywords=("siem", "immutable", "audit storage", "不可变", "审计存储", "生产日志"),
    ),
    ClosureProfile(
        category="security.externalization_live",
        owner="security-ops",
        credential_dependencies=("production identity/security evidence proof refs",),
        required_evidence=(
            "production security gate passed",
            "security externalization gate accepted live proof when required",
            "RBAC/OWASP/privacy negative tests passed",
        ),
        verification_commands=(
            "bash scripts/production-security-gate.sh --output-json <path>",
            "bash scripts/security-externalization-gate.sh --evidence-json <redacted-proof.json> --output-json <path>",
        ),
        closure_condition="生产安全外部化、RBAC/OWASP/privacy 和必要 live proof-ref 证据闭合。",
        keywords=(
            "securitycontrol",
            "security-externalization",
            "security externalization",
            "production security",
            "owasp",
            "privacy",
            "tenant",
            "authz",
            "外部生产验证",
        ),
    ),
    ClosureProfile(
        category="observability.otel_slo_live",
        owner="sre-ops",
        credential_dependencies=("OTel collector/backend access", "Prometheus/Alertmanager or trace backend proof ref"),
        required_evidence=("OTel backend query proof accepted", "SLO dashboard/alert route proof accepted"),
        verification_commands=(
            "bash scripts/otel-backend-slo-gate.sh --evidence-json <redacted-proof.json> --output-json <path>",
        ),
        closure_condition="真实 OTel/metrics/traces/SLO/alert proof-ref 通过 staged gate。",
        keywords=("otel", "opentelemetry", "trace backend", "prometheus", "alertmanager", "slo", "监控", "collector"),
    ),
    ClosureProfile(
        category="security.retention_cleanup_live",
        owner="security-ops",
        credential_dependencies=(
            "production scheduler proof ref",
            "Postgres cleanup proof ref",
            "SIEM retention proof ref",
        ),
        required_evidence=("retention production cleanup staged evidence accepted", "no raw deletion payload"),
        verification_commands=(
            "bash scripts/retention-production-cleanup-gate.sh --evidence-json <redacted-proof.json> --output-json <path>",
        ),
        closure_condition="生产 scheduler、Postgres cleanup、SIEM/log retention proof-ref 均通过 staged gate。",
        keywords=("retention", "cleanup", "清理", "留存", "scheduler", "production_deleted", "删除"),
    ),
    ClosureProfile(
        category="developer_platform.live",
        owner="developer-platform",
        credential_dependencies=(
            "public developer portal URL",
            "sandbox token issuer credentials",
            "package registry credentials",
        ),
        required_evidence=("developer portal live smoke passed", "sandbox token issuer/revocation smoke passed"),
        verification_commands=(
            "bash scripts/developer-portal-gate.sh --evidence-json <redacted-proof.json> --output-json <path>",
            "bash scripts/sandbox-access-gateway-gate.sh --evidence-json <redacted-proof.json> --output-json <path>",
        ),
        closure_condition="公网 developer portal、sandbox token service 和 SDK/package evidence 均通过。",
        keywords=(
            "developer portal",
            "sandbox token",
            "sdk",
            "publishedsdk",
            "live sandbox",
            "开发者门户",
            "revocation service",
            "revocation",
        ),
    ),
    ClosureProfile(
        category="delivery.multi_surface_live",
        owner="delivery-ops",
        credential_dependencies=(
            "public API/HF/Bot surface access",
            "delivery surface live evidence",
        ),
        required_evidence=(
            "multi-surface semantic diff passed with live surfaces when required",
            "Bot/API/HF live report hashes or proof refs attached",
        ),
        verification_commands=(
            "bash scripts/multi-surface-semantic-diff.sh --output-json <path>",
            "bash scripts/live-release-gate.sh --output-json <path>",
        ),
        closure_condition="Web/API/Bot/CLI/Skill/HF 等交付面在要求 live 时完成同源语义验证。",
        keywords=(
            "multi-surface",
            "multi_surface",
            "semantic diff",
            "delivery surface",
            "web/api/bot",
            "cli/skill",
            "public demo",
            "多交付面",
        ),
    ),
    ClosureProfile(
        category="release.artifact_current_commit",
        owner="release-ops",
        credential_dependencies=(
            "GitHub Actions workflow access",
            "GHCR or registry permissions when publishing",
            "artifact attestation verification access",
        ),
        required_evidence=(
            "current commit Acceptance run passed",
            "current commit Container run passed",
            "container digest or explicit no-push mode recorded",
            "SBOM/provenance/rollback evidence attached",
        ),
        verification_commands=(
            "bash scripts/current-release-proof.sh --require-current-release --output-json <path>",
            "bash scripts/live-release-gate.sh --output-json <path>",
        ),
        closure_condition="当前 commit 的远端 CI、container、SBOM/provenance、rollback 和必要 registry evidence 均可追溯。",
        keywords=(
            "release artifact",
            "release-artifacts",
            "sbom",
            "provenance",
            "ghcr",
            "attestation",
            "registry digest",
            "container registry",
            "container digest",
            "current commit",
            "release proof",
        ),
    ),
    ClosureProfile(
        category="provider.external_dependency_live",
        owner="provider-platform",
        credential_dependencies=(
            "external provider access when applicable",
            "provider source/license review evidence",
        ),
        required_evidence=(
            "provider dependency smoke passed",
            "provider drift trend gate passed",
            "provider source/license review evidence attached when required",
        ),
        verification_commands=(
            "bash scripts/provider-dependency-smoke.sh --output-json <path>",
            "bash scripts/provider-drift-trend-gate.sh --output-json <path>",
        ),
        closure_condition="provider 实际执行、依赖、source/license 和 drift gate 均有当前证据。",
        keywords=(
            "provider",
            "dependency",
            "drift",
            "lifecycle",
            "license",
            "source/license",
            "远端依赖",
            "production provider",
            "provider 外部",
        ),
    ),
    ClosureProfile(
        category="quality.external_evaluation_live",
        owner="quality-ops",
        credential_dependencies=(
            "external benchmark source access",
            "model/API credentials when live evaluation uses external model",
        ),
        required_evidence=(
            "EvaluationRun summary passed",
            "evaluation trend gate passed",
            "external benchmark usage/license boundary accepted",
            "no prompt/answer/report leakage in artifacts",
        ),
        verification_commands=(
            "bash scripts/run-evaluations.sh --output-dir <dir>",
            "bash scripts/evaluation-trend-gate.sh --history-dir <dir> --output-json <path>",
            "bash scripts/mingli-bench-gate.sh --output-json <path>",
        ),
        closure_condition="外部 benchmark 或模型评测有脱敏 summary、趋势门禁和 license/usage 边界证据。",
        keywords=(
            "evaluation",
            "evaluationrun",
            "external_eval",
            "benchmark",
            "mingli",
            "external model",
            "外部模型",
            "nightly",
            "accuracy",
        ),
    ),
    ClosureProfile(
        category="audit.certification_current_evidence",
        owner="audit-owner",
        credential_dependencies=("current release/audit/certification sidecar evidence",),
        required_evidence=(
            "measurement infrastructure certification summary attached",
            "current release proof/live release/audit bundle sidecars are current when used",
        ),
        verification_commands=(
            "bash scripts/measurement-infrastructure-certification.sh --evidence-dir <dir> --output-json <path>",
        ),
        closure_condition="certification 聚合器引用当前 release/live/audit 证据，且 blocked/pending 语义未被改写。",
        keywords=(
            "certification",
            "measurement_infrastructure_certification",
            "measurement-infrastructure-certification",
            "canclaim100percent",
            "current-audit-bundle",
            "current release proof",
        ),
    ),
    ClosureProfile(
        category="audit.third_party_review",
        owner="audit-owner",
        credential_dependencies=("third-party auditor access", "signed review result"),
        required_evidence=("independent audit result attached", "audit findings tracked or accepted"),
        verification_commands=("bash scripts/audit-handoff-dry-run.sh --bundle-json <bundle> --output-dir <dir>",),
        closure_condition="第三方审计人员完成独立复核，并提供签名/可追溯审计结果。",
        keywords=("third-party audit", "third party audit", "第三方审计", "auditor", "independent auditor"),
    ),
    ClosureProfile(
        category="governance.external_validation_policy_guardrail",
        owner="governance",
        credential_dependencies=("no credential; policy guardrail review",),
        required_evidence=(
            "audit handoff still scans the pending phrase",
            "policy text continues to forbid fake live evidence",
        ),
        verification_commands=(
            "bash scripts/audit-handoff.sh --output-dir <dir>",
            "bash scripts/audit-handoff-dry-run.sh --bundle-json <bundle> --bundle-markdown <markdown> --output-dir <dir>",
        ),
        closure_condition="该 occurrence 是外部验证防伪证政策或测试标记；关闭方式是确认它必须保留，而不是误当成真实 live 待办。",
        keywords=(
            "requiredphrase",
            "audit/handoff",
            "handoff.json",
            "pending external validations",
            "pending external validation",
            "tracked and untracked",
            "json output includes",
            "完整列出",
            "机器真相源",
            "必须标记",
            "统一写",
            "没有证据只能写",
            "真实证据",
            "without proof",
            "all external systems",
            "不能伪造",
            "不伪造",
            "不能声明",
            "不声明",
            "不消除",
            "不能替代",
            "保持 blocked",
            "明确外部连通验证待执行",
            "标为",
            "标记为",
            "外部连通验证待执行项",
            "外部连通验证清单",
            "外部待验证项",
            "外部 live 项",
            "外部生产连通",
            "真实生产外部依赖",
            "所有外部依赖",
            "外部阻断项分层",
            "区分本地可执行",
            "计划必须区分",
            "本地可执行",
            "本地已验证",
            "stop condition",
            "风险边界",
            "所有缺口",
            "本任务不",
            "不阻塞",
            "仍待",
            "仍需",
            "未完成",
            "后续实现",
            "外部凭证",
            "审计包",
            "审计人员",
            "无法直接分派",
            "所有真实外部平台",
            "外部平台",
            "外部 token",
            "生产账号",
            "endpoint",
            "真实域名",
            "真实 token",
            "远程服务",
            "生产完成",
            "不可伪造",
            "no fake live evidence",
            "not claimed",
            "external live evidence absent",
            "external connectivity",
            "externalconnectivity",
            "liveevidencestatus",
            "pending =",
            "pending_phrase",
            "唯一剩余 manual item",
            "manual item",
            "任何 `",
            "外部连通验证待执行清单",
            "roadmap references",
            "rg -n",
            "所有真实生产系统",
            "真实外部 live",
            "report-policy",
            "markdown-report",
            "evidence-coverage-trend",
            "post-0098",
            "post-0108",
        ),
    ),
)

MANUAL_PROFILE = ClosureProfile(
    category="manual_triage",
    owner="engineering-audit",
    credential_dependencies=("human classification",),
    required_evidence=("manual owner assignment", "specific closure command or proof-ref added"),
    verification_commands=(
        "bash scripts/external-validation-closure-gate.sh --pending-external-json <path> --output-json <path>",
    ),
    closure_condition="人工复核该 occurrence，补充准确 owner、凭证依赖、关闭条件和复核命令。",
    keywords=(),
)


def _utc_now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def _load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def _sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _short_id(item: dict[str, Any]) -> str:
    raw = f"{item.get('path')}:{item.get('line')}:{item.get('excerpt')}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]


def _redact(value: str) -> str:
    redacted = value
    for marker in ("token=", "secret=", "password=", "passwd=", "DATABASE_URL=", "DB_DSN="):
        lower = redacted.lower()
        index = lower.find(marker.lower())
        if index >= 0:
            end = redacted.find(" ", index)
            if end < 0:
                end = len(redacted)
            redacted = redacted[:index] + marker.rstrip("=") + ":[redacted]" + redacted[end:]
    return redacted


def _profile_for(item: dict[str, Any]) -> ClosureProfile:
    haystack = " ".join(str(item.get(field, "")) for field in ("path", "excerpt", "phrase", "id")).casefold()
    for profile in PROFILES:
        if any(keyword.casefold() in haystack for keyword in profile.keywords):
            return profile
    return MANUAL_PROFILE


def _validate_pending_items(payload: Any) -> list[dict[str, Any]]:
    if not isinstance(payload, list):
        raise ExternalValidationClosureError("pending external JSON root must be an array")
    items: list[dict[str, Any]] = []
    for index, item in enumerate(payload):
        if not isinstance(item, dict):
            raise ExternalValidationClosureError(f"pending item {index} must be object")
        path = item.get("path")
        line = item.get("line")
        excerpt = item.get("excerpt")
        if not isinstance(path, str) or not path:
            raise ExternalValidationClosureError(f"pending item {index} missing path")
        if not isinstance(line, int) or line <= 0:
            raise ExternalValidationClosureError(f"pending item {index} missing positive line")
        if not isinstance(excerpt, str) or not excerpt:
            raise ExternalValidationClosureError(f"pending item {index} missing excerpt")
        items.append(item)
    return items


def _assert_no_forbidden(summary: dict[str, Any]) -> None:
    rendered = json.dumps(summary, ensure_ascii=False, sort_keys=True)
    forbidden = [marker for marker in FORBIDDEN_MARKERS if marker.lower() in rendered.lower()]
    if forbidden:
        raise ExternalValidationClosureError(
            "closure plan contains forbidden sensitive marker: " + ", ".join(forbidden)
        )


def build_summary(*, pending_external_json: Path) -> dict[str, Any]:
    if not pending_external_json.is_file():
        raise ExternalValidationClosureError(f"pending external json missing: {pending_external_json}")
    contract = _load_json(CONTRACT_PATH)
    pending_items = _validate_pending_items(_load_json(pending_external_json))
    closure_items: list[dict[str, Any]] = []
    categories: dict[str, int] = {}
    credential_kinds: set[str] = set()
    for item in pending_items:
        profile = _profile_for(item)
        categories[profile.category] = categories.get(profile.category, 0) + 1
        credential_kinds.update(profile.credential_dependencies)
        excerpt = _redact(str(item["excerpt"]))
        closure_items.append(
            {
                "id": f"external.{_short_id(item)}",
                "source": {
                    "id": str(item.get("id") or _short_id(item)),
                    "path": item["path"],
                    "line": item["line"],
                    "excerpt": excerpt,
                    "excerptSha256": _sha256_text(str(item["excerpt"])),
                },
                "category": profile.category,
                "owner": profile.owner,
                "status": (
                    "manual_triage_required" if profile.category == "manual_triage" else "external_connectivity_pending"
                ),
                "credentialDependencies": list(profile.credential_dependencies),
                "requiredEvidence": list(profile.required_evidence),
                "verificationCommands": list(profile.verification_commands),
                "closureCondition": profile.closure_condition,
                "privacyBoundary": "不得输出真实 token、secret、DSN、私钥、生产日志正文、用户报告正文或外部账号数据。",
            }
        )

    manual_triage = categories.get("manual_triage", 0)
    ship_status = "blocked" if closure_items else "passed"
    summary = {
        "schemaVersion": 1,
        "kind": "fatecat.external_validation_closure_plan",
        "generatedAt": _utc_now(),
        "status": "passed",
        "source": {
            "pendingExternalJson": str(pending_external_json),
            "itemCount": len(pending_items),
        },
        "summary": {
            "total": len(closure_items),
            "planned": len(closure_items),
            "manualTriage": manual_triage,
            "categories": dict(sorted(categories.items())),
            "credentialDependencyKinds": sorted(credential_kinds),
            "externalConnectivity": "外部连通验证待执行" if closure_items else "none",
        },
        "shipGate": {
            "status": ship_status,
            "blockingItems": sorted(categories) if closure_items else [],
            "policy": contract["categoryPolicy"]["shipGate"],
        },
        "items": closure_items,
        "privacyBoundary": contract["privacyBoundary"],
        "nonClaims": contract["nonClaims"],
    }
    _assert_no_forbidden(summary)
    return summary


def write_summary(summary: dict[str, Any], output_json: Path) -> None:
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build external validation closure plan from pending audit items.")
    parser.add_argument("--pending-external-json", type=Path, required=True, help="pending-external-validations.json")
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON, help="output closure plan JSON")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        summary = build_summary(pending_external_json=args.pending_external_json)
        write_summary(summary, args.output_json)
        print(
            json.dumps(
                {
                    "status": summary["status"],
                    "shipGate": summary["shipGate"]["status"],
                    "total": summary["summary"]["total"],
                    "manualTriage": summary["summary"]["manualTriage"],
                    "categories": len(summary["summary"]["categories"]),
                    "outputJson": str(args.output_json),
                },
                ensure_ascii=False,
            )
        )
        return 0
    except (ExternalValidationClosureError, OSError, json.JSONDecodeError) as exc:
        print(f"external validation closure gate error: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
