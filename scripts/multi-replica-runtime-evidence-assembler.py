#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
GATE_PATH = REPO_ROOT / "scripts" / "multi-replica-runtime-gate.py"
DEFAULT_OUTPUT_JSON = (
    REPO_ROOT / "infra" / "runtime" / "local-state" / "exports" / "delivery" / "multi-replica-runtime-evidence.json"
)

PROOF_REF_PREFIXES = ("evidence://", "artifact://", "ci-artifact://")
REDACTION_BOUNDARY = "redacted_no_secret_values"
PENDING_STATUS = "external_connectivity_pending"
LIVE_STATUS = "external_live_passed"

SENSITIVE_FRAGMENTS = {
    "BEGIN OPENSSH",
    "BEGIN RSA",
    "DATABASE_URL=",
    "DB_DSN=",
    "FATE_REPORT_JOB_DATABASE_URL",
    "api_key=",
    "authorization:",
    "callback_url=",
    "password=",
    "postgres://",
    "postgresql://",
    "private_key",
    "secret=",
    "token=",
    "webhook_url=",
}

FORBIDDEN_PROOF_FRAGMENTS = {
    "dry-run",
    "fake",
    "localhost",
    "local only",
    "memory",
    "placeholder",
    "sample",
    "single replica",
    "sqlite",
}


class AssemblerFailure(RuntimeError):
    """多副本 runtime evidence 装配失败。"""


def _load_gate_module():
    spec = importlib.util.spec_from_file_location("fatecat_multi_replica_runtime_gate", GATE_PATH)
    if spec is None or spec.loader is None:
        raise AssemblerFailure(f"cannot load gate module from {GATE_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _render(payload: Any) -> str:
    return json.dumps(payload, ensure_ascii=False, sort_keys=True)


def _assert_no_sensitive_fragments(payload: Any) -> None:
    rendered = _render(payload).lower()
    bad = sorted(fragment for fragment in SENSITIVE_FRAGMENTS if fragment.lower() in rendered)
    if bad:
        raise AssemblerFailure(f"sensitive fragment detected: {', '.join(bad)}")
    if re.search(r"https?://", rendered, re.I):
        raise AssemblerFailure("raw http/https URL is forbidden in evidence")


def _parse_timestamp(value: str, field: str) -> datetime:
    try:
        normalized = value.replace("Z", "+00:00")
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise AssemblerFailure(f"{field} must be ISO-8601 timestamp") from exc
    if parsed.tzinfo is None:
        raise AssemblerFailure(f"{field} must include timezone")
    return parsed.astimezone(UTC)


def _format_ts(value: datetime) -> str:
    return value.astimezone(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def _validate_proof_ref(field: str, value: str) -> str:
    if not value:
        raise AssemblerFailure(f"{field} is required")
    lowered = value.lower()
    if not value.startswith(PROOF_REF_PREFIXES):
        raise AssemblerFailure(f"{field} must use a redacted proof ref prefix")
    bad = sorted(fragment for fragment in FORBIDDEN_PROOF_FRAGMENTS if fragment in lowered)
    if bad:
        raise AssemblerFailure(f"{field} contains forbidden proof fragment: {', '.join(bad)}")
    _assert_no_sensitive_fragments(value)
    return value


def _positive_int(value: int | None, field: str) -> int:
    if value is None or isinstance(value, bool) or value <= 0:
        raise AssemblerFailure(f"{field} must be positive integer")
    return value


def _base_payload(status: str) -> dict[str, Any]:
    return {
        "schemaVersion": 1,
        "kind": "fatecat.multi_replica_runtime_evidence",
        "status": status,
        "generatedAt": datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "privacyBoundary": (
            "该 evidence 只允许保存脱敏证明句柄；不得包含 DSN、token、secret、webhook URL、"
            "报告正文、用户输入、生产日志正文或真实外部账号信息。"
        ),
        "nonClaims": [
            "does_not_claim_exactly_once",
            "does_not_replace_public_webhook_live_proof",
            "does_not_replace_external_secret_provider_live_proof",
            "does_not_replace_metrics_backend_proof",
        ],
    }


def build_pending_payload() -> dict[str, Any]:
    payload = _base_payload(PENDING_STATUS)
    payload.update(
        {
            "externalConnectivity": "外部连通验证待执行",
            "requiredExternalInputs": [
                "real multi-replica Postgres runtime",
                "public webhook receiver proof",
                "external secret provider proof",
                "external metrics backend proof",
                "24h soak run with at least 2 replicas and 100 completed jobs",
            ],
        }
    )
    return payload


def build_live_payload(args: argparse.Namespace) -> dict[str, Any]:
    if not args.ack_external_live:
        raise AssemblerFailure("--ack-external-live is required with --external-live")
    if args.exactly_once_claim:
        raise AssemblerFailure("exactly-once claim is forbidden")

    started_at = _parse_timestamp(args.started_at, "--started-at")
    finished_at = _parse_timestamp(args.finished_at, "--finished-at")
    if finished_at <= started_at:
        raise AssemblerFailure("--finished-at must be after --started-at")

    observed_duration = int((finished_at - started_at).total_seconds())
    duration_seconds = args.duration_seconds if args.duration_seconds is not None else observed_duration
    duration_seconds = _positive_int(duration_seconds, "--duration-seconds")
    if duration_seconds > observed_duration:
        raise AssemblerFailure("--duration-seconds cannot exceed finished_at - started_at")

    runtime = {
        "mode": "external_postgres_multi_replica",
        "backend": "backend.postgres",
        "verificationStatus": "passed_multi_replica_soak",
        "replicaCount": _positive_int(args.replica_count, "--replica-count"),
        "durationSeconds": duration_seconds,
        "completedJobCount": _positive_int(args.completed_job_count, "--completed-job-count"),
        "concurrentWorkerProofRef": _validate_proof_ref(
            "--concurrent-worker-proof-ref", args.concurrent_worker_proof_ref
        ),
        "leaseContentionProofRef": _validate_proof_ref("--lease-contention-proof-ref", args.lease_contention_proof_ref),
        "restartRecoveryProofRef": _validate_proof_ref("--restart-recovery-proof-ref", args.restart_recovery_proof_ref),
        "heartbeatContinuityProofRef": _validate_proof_ref(
            "--heartbeat-continuity-proof-ref", args.heartbeat_continuity_proof_ref
        ),
        "noDuplicateTerminalJobProofRef": _validate_proof_ref(
            "--no-duplicate-terminal-job-proof-ref", args.no_duplicate_terminal_job_proof_ref
        ),
        "publicWebhookProofRef": _validate_proof_ref("--public-webhook-proof-ref", args.public_webhook_proof_ref),
        "externalSecretProviderProofRef": _validate_proof_ref(
            "--external-secret-provider-proof-ref", args.external_secret_provider_proof_ref
        ),
        "metricsProofRef": _validate_proof_ref("--metrics-proof-ref", args.metrics_proof_ref),
        "redactionBoundary": REDACTION_BOUNDARY,
    }

    payload = _base_payload(LIVE_STATUS)
    payload.update(
        {
            "externalConnectivity": "external_live_evidence_supplied_by_operator",
            "run": {
                "runId": _validate_proof_ref("--run-id", args.run_id),
                "startedAt": _format_ts(started_at),
                "finishedAt": _format_ts(finished_at),
                "operatorAttestationRef": _validate_proof_ref(
                    "--operator-attestation-ref", args.operator_attestation_ref
                ),
                "assemblerVersion": 1,
            },
            "runtime": runtime,
        }
    )
    return payload


def validate_with_gate(payload: dict[str, Any]) -> None:
    _assert_no_sensitive_fragments(payload)
    gate = _load_gate_module()
    contract = gate._load_json(gate.CONTRACT_PATH)
    gate.validate_multi_replica_evidence(payload, contract)


def write_payload(payload: dict[str, Any], output_json: Path) -> None:
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="装配 FateCat multi-replica runtime 脱敏 evidence JSON。")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--pending", action="store_true", help="输出外部连通待验证 evidence。")
    mode.add_argument("--external-live", action="store_true", help="输出 operator 提供的外部 live evidence。")
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON, help="evidence JSON 输出路径。")
    parser.add_argument("--ack-external-live", action="store_true", help="确认以下 proof refs 来自真实外部 live run。")
    parser.add_argument("--exactly-once-claim", action="store_true", help="负例开关：该声明会被拒绝。")
    parser.add_argument("--run-id", default="", help="脱敏 run id 证明句柄。")
    parser.add_argument("--started-at", default="", help="soak 开始时间，ISO-8601。")
    parser.add_argument("--finished-at", default="", help="soak 结束时间，ISO-8601。")
    parser.add_argument("--replica-count", type=int, help="参与运行的副本数。")
    parser.add_argument("--duration-seconds", type=int, help="soak 持续秒数；缺省时由开始/结束时间计算。")
    parser.add_argument("--completed-job-count", type=int, help="完成 job 数。")
    parser.add_argument("--operator-attestation-ref", default="", help="operator attestation 脱敏证明句柄。")
    parser.add_argument("--concurrent-worker-proof-ref", default="", help="并发 worker 证明句柄。")
    parser.add_argument("--lease-contention-proof-ref", default="", help="lease 竞争证明句柄。")
    parser.add_argument("--restart-recovery-proof-ref", default="", help="重启恢复证明句柄。")
    parser.add_argument("--heartbeat-continuity-proof-ref", default="", help="heartbeat 连续性证明句柄。")
    parser.add_argument("--no-duplicate-terminal-job-proof-ref", default="", help="未观察到重复终态 job 证明句柄。")
    parser.add_argument("--public-webhook-proof-ref", default="", help="公网 webhook live 证明句柄。")
    parser.add_argument("--external-secret-provider-proof-ref", default="", help="外部 secret provider live 证明句柄。")
    parser.add_argument("--metrics-proof-ref", default="", help="外部 metrics backend 证明句柄。")
    return parser


def run(args: argparse.Namespace) -> dict[str, Any]:
    if args.external_live:
        payload = build_live_payload(args)
    else:
        payload = build_pending_payload()
    validate_with_gate(payload)
    return payload


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        payload = run(args)
        write_payload(payload, args.output_json)
        print(
            json.dumps(
                {
                    "status": payload["status"],
                    "kind": payload["kind"],
                    "externalConnectivity": payload["externalConnectivity"],
                    "output": str(args.output_json),
                },
                ensure_ascii=False,
                sort_keys=True,
            )
        )
        return 0
    except AssemblerFailure as exc:
        print(f"multi-replica runtime evidence assembler error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
