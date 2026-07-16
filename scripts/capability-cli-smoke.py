#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import tempfile
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
CLI_WRAPPER = REPO_ROOT / "scripts" / "capability-cli.sh"
DEFAULT_OUTPUT_JSON = (
    REPO_ROOT / "infra" / "runtime" / "local-state" / "exports" / "delivery" / "capability-cli-smoke.json"
)

AVAILABLE_FIXTURES: dict[str, dict[str, Any]] = {
    "bazi": {
        "birthDateTime": "1990-01-01 08:00:00",
        "gender": "male",
        "longitude": 116.4074,
        "latitude": 39.9042,
        "name": "测试用户",
        "birthPlace": "北京市",
        "useTrueSolarTime": True,
    },
    "ziwei": {
        "birthDateTime": "1990-01-01 08:00:00",
        "gender": "male",
        "longitude": 116.4074,
        "latitude": 39.9042,
        "name": "测试用户",
        "birthPlace": "北京市",
        "useTrueSolarTime": True,
    },
    "almanac": {
        "dateRange": {"start": "2026-07-02", "end": "2026-07-04"},
        "eventType": "开业",
        "place": "北京市",
    },
    "meihua": {
        "question": "测试问题",
        "castMethod": "number",
        "castValue": "3,8,6",
        "place": "北京市",
    },
}

EXPECTED_DATA_KEYS: dict[str, tuple[str, ...]] = {
    "bazi": ("fourPillars", "analysisEvidence", "accuracyGuards"),
    "ziwei": ("ziweiChart", "analysisEvidence", "ziweiGoldenGuards"),
    "almanac": ("days", "recommendations", "analysisEvidence"),
    "meihua": ("hexagrams", "bodyUse", "analysisEvidence"),
}

EXPECTED_MATURITY_STATUS = {
    "bazi": "production",
    "ziwei": "production",
    "almanac": "validated",
    "meihua": "validated",
}

PLANNED_FIXTURE: dict[str, Any] = {
    "question": "测试问题",
    "castMethod": "time",
    "castTime": "2026-05-08 08:00:00",
}

FORBIDDEN_SUMMARY_SNIPPETS = (
    "BEGIN RSA",
    "BEGIN OPENSSH",
    "DATABASE_URL=",
    "DB_DSN=",
    "FATE_BOT_TOKEN=",
    "api_key=",
    "secret=",
    "password=",
    "passwd=",
)


class CapabilityCliSmokeError(RuntimeError):
    """capability CLI smoke 未满足交付面基线。"""


def _json_dumps(payload: dict[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=False, separators=(",", ":"))


def _sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _run_command(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise CapabilityCliSmokeError(message)


def _load_output(path: Path) -> tuple[dict[str, Any], bytes]:
    raw = path.read_bytes()
    payload = json.loads(raw.decode("utf-8"))
    _assert(isinstance(payload, dict), f"{path.name} 输出不是 JSON 对象")
    return payload, raw


def _summarize_success(capability_id: str, payload: dict[str, Any], raw: bytes, duration_ms: float) -> dict[str, Any]:
    data = payload.get("data")
    evidence = payload.get("evidence")
    metadata = payload.get("metadata")

    _assert(payload.get("success") is True, f"{capability_id} success 不是 true")
    _assert(payload.get("capabilityId") == capability_id, f"{capability_id} capabilityId 不一致")
    _assert(payload.get("availability") == "available", f"{capability_id} availability 不是 available")
    _assert(
        payload.get("status") == EXPECTED_MATURITY_STATUS[capability_id],
        f"{capability_id} maturity status 不一致",
    )
    _assert(payload.get("reportProfile") == capability_id, f"{capability_id} reportProfile 不一致")
    _assert(isinstance(data, dict), f"{capability_id} data 不是对象")
    _assert(isinstance(evidence, dict), f"{capability_id} evidence 不是对象")
    _assert(isinstance(metadata, dict), f"{capability_id} metadata 不是对象")

    for key in EXPECTED_DATA_KEYS[capability_id]:
        _assert(key in data, f"{capability_id} data 缺少 {key}")

    return {
        "capabilityId": capability_id,
        "success": True,
        "availability": payload["availability"],
        "status": payload["status"],
        "reportProfile": payload["reportProfile"],
        "durationMs": round(duration_ms, 3),
        "stdoutSha256": _sha256_bytes(raw),
        "stdoutBytes": len(raw),
        "dataKeys": sorted(data.keys())[:48],
        "evidenceKeys": sorted(evidence.keys())[:48],
        "metadataKeys": sorted(metadata.keys())[:48],
    }


def _execute_capability(capability_id: str, fixture: dict[str, Any], work_dir: Path) -> dict[str, Any]:
    output_file = work_dir / f"{capability_id}.json"
    command = [
        "bash",
        str(CLI_WRAPPER),
        capability_id,
        "--input-json",
        _json_dumps(fixture),
        "--output-file",
        str(output_file),
        "--pretty",
    ]
    started = time.perf_counter()
    completed = _run_command(command)
    duration_ms = (time.perf_counter() - started) * 1000

    if completed.returncode != 0:
        raise CapabilityCliSmokeError(
            f"{capability_id} CLI 执行失败: exit={completed.returncode} stderr={completed.stderr.strip()[:500]}"
        )
    _assert(output_file.exists(), f"{capability_id} 未写出 output-file")
    payload, raw = _load_output(output_file)
    return _summarize_success(capability_id, payload, raw, duration_ms)


def _execute_planned_rejection() -> dict[str, Any]:
    command = [
        "bash",
        str(CLI_WRAPPER),
        "liuyao",
        "--input-json",
        _json_dumps(PLANNED_FIXTURE),
        "--pretty",
    ]
    completed = _run_command(command)
    stdout = completed.stdout.encode("utf-8")
    _assert(completed.returncode == 1, f"planned capability 未拒绝执行: exit={completed.returncode}")
    payload = json.loads(completed.stdout)
    _assert(payload.get("success") is False, "planned capability 拒绝输出缺少 success=false")
    _assert("尚未生产化" in str(payload.get("error", "")), "planned capability 拒绝原因未说明尚未生产化")

    return {
        "capabilityId": "liuyao",
        "success": False,
        "expectedExitCode": 1,
        "actualExitCode": completed.returncode,
        "stdoutSha256": _sha256_bytes(stdout),
        "stdoutBytes": len(stdout),
        "errorContains": "尚未生产化",
    }


def _assert_summary_safe(summary: dict[str, Any]) -> None:
    text = json.dumps(summary, ensure_ascii=False)
    for snippet in FORBIDDEN_SUMMARY_SNIPPETS:
        if snippet in text:
            raise CapabilityCliSmokeError(f"smoke summary 含禁止片段: {snippet}")


def run_smoke() -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="fatecat-capability-cli-smoke-") as tmp:
        work_dir = Path(tmp)
        results = [
            _execute_capability(capability_id, fixture, work_dir)
            for capability_id, fixture in AVAILABLE_FIXTURES.items()
        ]
        planned_rejection = _execute_planned_rejection()

    summary = {
        "schemaVersion": 1,
        "kind": "fatecat.capability_cli_smoke",
        "generatedAt": datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "status": "passed",
        "smokeScope": "local_cli_capability_command",
        "entrypoint": "bash scripts/capability-cli.sh <capability_id>",
        "canonicalChain": [
            "scripts/capability-cli.sh",
            "domains/fate-analysis/services/fate-core/src/fate_core/cli.py::_run_capability_execute",
            "domains/fate-analysis/services/fate-core/src/fate_core/capabilities/executor.py::CapabilityExecutor",
        ],
        "capabilityCount": len(results),
        "capabilities": results,
        "plannedCapabilityRejection": planned_rejection,
        "externalConnectivity": "not_required",
        "privacyBoundary": "只使用北京固定脱敏样例；summary 只保存 hash、字节数、字段名和状态，不保存姓名、完整报告正文、token、secret、DSN、webhook URL 或生产账号。",
        "limitations": [
            "该 smoke 只证明本地 CLI JSON capability 入口可执行。",
            "该 smoke 不证明标准 Markdown 多端同源、Web/API/Bot live、Hugging Face Space 或生产部署可用。",
        ],
    }
    _assert_summary_safe(summary)
    return summary


def write_summary(summary: dict[str, Any], output_json: Path) -> None:
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="执行 capability CLI 交付面本地 smoke，并输出机器可读 JSON。")
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON, help="smoke summary JSON 输出路径。")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        summary = run_smoke()
        write_summary(summary, args.output_json)
        print(json.dumps({"status": summary["status"], "capabilities": summary["capabilityCount"]}, ensure_ascii=False))
        return 0
    except CapabilityCliSmokeError as exc:
        print(f"capability CLI smoke error: {exc}", flush=True)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
