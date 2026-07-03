#!/usr/bin/env python3
from __future__ import annotations

import argparse
import ast
import hashlib
import importlib.util
import json
import re
import sys
import time
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
DELIVERY_SRC = REPO_ROOT / "domains" / "experience-delivery" / "services" / "fatecat-delivery" / "src"
FATE_CORE_SRC = REPO_ROOT / "domains" / "fate-analysis" / "services" / "fate-core" / "src"
DEFAULT_OUTPUT = REPO_ROOT / "infra" / "runtime" / "local-state" / "exports" / "multi-surface-semantic-diff.json"
REPORT_SYSTEMS = ("bazi", "ziwei")
CAPABILITY_CLI_SMOKE = REPO_ROOT / "scripts" / "capability-cli-smoke.py"
FORBIDDEN_MARKERS = (
    "token=",
    "secret=",
    "password=",
    "passwd=",
    "private_key=",
    "BEGIN RSA",
    "BEGIN OPENSSH",
    "# 命理排盘报告",
    "# 紫微斗数报告",
)
VOLATILE_PATTERNS = (
    (
        re.compile(r"^\| 运限日期 \| .* \|$", flags=re.MULTILINE),
        "| 运限日期 | <normalized-runtime-as-of> |",
    ),
)

if str(DELIVERY_SRC) not in sys.path:
    sys.path.insert(0, str(DELIVERY_SRC))
if str(FATE_CORE_SRC) not in sys.path:
    sys.path.insert(0, str(FATE_CORE_SRC))

from fastapi.testclient import TestClient  # noqa: E402

from calculation_service import calculate_delivery_result  # noqa: E402
from location import get as get_location  # noqa: E402
from main import _build_markdown_report_payload, app  # noqa: E402
from models import BaziRequest  # noqa: E402
from report_generator import generate_full_report  # noqa: E402
from web_forms import WebReportForm  # noqa: E402
from web_report_service import build_web_report_result  # noqa: E402


class MultiSurfaceSemanticDiffError(RuntimeError):
    """多交付面语义 diff 失败。"""


@dataclass(frozen=True)
class SurfaceMarkdown:
    surface_id: str
    route: str
    markdown: str


def utc_now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def normalize_semantic_markdown(markdown: str) -> tuple[str, list[str]]:
    normalized = markdown
    applied: list[str] = []
    for pattern, replacement in VOLATILE_PATTERNS:
        next_value = pattern.sub(replacement, normalized)
        if next_value != normalized:
            applied.append(pattern.pattern)
            normalized = next_value
    return normalized, applied


def build_api_payload(report_system: str) -> dict[str, Any]:
    longitude, latitude = get_location("北京")
    return {
        "name": "测试样本",
        "gender": "male",
        "birthDate": "1990-01-01",
        "birthTime": "08:00:00",
        "birthPlace": {
            "name": "北京",
            "longitude": longitude,
            "latitude": latitude,
            "timezone": "Asia/Shanghai",
        },
        "options": {
            "useTrueSolarTime": True,
            "daylightSaving": "auto",
            "midnightMode": "early",
            "calendarType": "solar",
            "reportSystem": report_system,
        },
    }


def wait_for_job(client: TestClient, job_id: str, *, timeout_seconds: float = 8.0) -> dict[str, Any]:
    deadline = time.monotonic() + timeout_seconds
    last_body: dict[str, Any] = {}
    while time.monotonic() < deadline:
        response = client.get(f"/api/v1/report/jobs/{job_id}")
        if response.status_code != 200:
            raise MultiSurfaceSemanticDiffError(f"job status request failed: {response.status_code}")
        last_body = response.json()
        status = last_body.get("data", {}).get("status")
        if status in {"succeeded", "failed", "expired", "cancelled"}:
            return last_body
        time.sleep(0.05)
    raise MultiSurfaceSemanticDiffError(f"report job did not finish: {last_body}")


def render_api_direct(report_system: str) -> SurfaceMarkdown:
    payload = build_api_payload(report_system)
    markdown = _build_markdown_report_payload(BaziRequest(**payload))["markdown"]
    return SurfaceMarkdown(
        surface_id="surface.fastapi.direct",
        route="main._build_markdown_report_payload",
        markdown=markdown,
    )


def render_api_http(client: TestClient, report_system: str) -> SurfaceMarkdown:
    response = client.post("/api/v1/report/markdown", json=build_api_payload(report_system))
    if response.status_code != 200:
        raise MultiSurfaceSemanticDiffError(f"API markdown failed: {response.status_code} {response.text[:200]}")
    body = response.json()
    markdown = body.get("data", {}).get("markdown")
    if not isinstance(markdown, str) or not markdown:
        raise MultiSurfaceSemanticDiffError("API markdown response missing markdown")
    return SurfaceMarkdown(surface_id="surface.fastapi.http", route="/api/v1/report/markdown", markdown=markdown)


def render_api_job(client: TestClient, report_system: str) -> SurfaceMarkdown:
    response = client.post("/api/v1/report/jobs", json=build_api_payload(report_system))
    if response.status_code != 202:
        raise MultiSurfaceSemanticDiffError(f"API report job failed: {response.status_code} {response.text[:200]}")
    job_id = response.json().get("data", {}).get("jobId")
    if not job_id:
        raise MultiSurfaceSemanticDiffError("API report job missing jobId")
    final_body = wait_for_job(client, str(job_id))
    data = final_body.get("data", {})
    if data.get("status") != "succeeded":
        raise MultiSurfaceSemanticDiffError(f"API report job not succeeded: {data.get('status')}")
    markdown = data.get("result", {}).get("markdown")
    if not isinstance(markdown, str) or not markdown:
        raise MultiSurfaceSemanticDiffError("API report job missing markdown")
    return SurfaceMarkdown(surface_id="surface.fastapi.job", route="/api/v1/report/jobs", markdown=markdown)


def render_web_direct(report_system: str) -> SurfaceMarkdown:
    result = build_web_report_result(
        WebReportForm(
            birth_date="1990-01-01",
            birth_time="08:00",
            birth_place="北京",
            gender="male",
            name="测试样本",
            report_system=report_system,
        )
    )
    return SurfaceMarkdown(
        surface_id="surface.web.direct",
        route="web_report_service.build_web_report_result",
        markdown=result.markdown,
    )


def render_web_job(client: TestClient, report_system: str) -> SurfaceMarkdown:
    response = client.post(
        "/api/v1/report/jobs/web",
        json={
            "birthDate": "1990-01-01",
            "birthTime": "08:00",
            "birthPlace": "北京",
            "gender": "male",
            "name": "测试样本",
            "reportSystem": report_system,
        },
    )
    if response.status_code != 202:
        raise MultiSurfaceSemanticDiffError(f"Web report job failed: {response.status_code} {response.text[:200]}")
    job_id = response.json().get("data", {}).get("jobId")
    if not job_id:
        raise MultiSurfaceSemanticDiffError("Web report job missing jobId")
    final_body = wait_for_job(client, str(job_id))
    data = final_body.get("data", {})
    if data.get("status") != "succeeded":
        raise MultiSurfaceSemanticDiffError(f"Web report job not succeeded: {data.get('status')}")
    markdown = data.get("result", {}).get("markdown")
    if not isinstance(markdown, str) or not markdown:
        raise MultiSurfaceSemanticDiffError("Web report job missing markdown")
    return SurfaceMarkdown(surface_id="surface.web.job", route="/api/v1/report/jobs/web", markdown=markdown)


def render_bot_dry_run(report_system: str) -> SurfaceMarkdown:
    longitude, latitude = get_location("北京")
    calculation = calculate_delivery_result(
        birth_dt=datetime(1990, 1, 1, 8, 0),
        gender="male",
        longitude=longitude,
        latitude=latitude,
        birth_place="北京",
        name="测试样本",
        report_system=report_system,
        use_true_solar_time=True,
        bazi_engine="capability",
    )
    markdown = generate_full_report(
        calculation.data,
        hide=calculation.report_hide,
        report_system=calculation.report_system,
    )
    return SurfaceMarkdown(
        surface_id="surface.telegram_bot.dry_run",
        route="bot canonical renderer dry-run without Telegram import",
        markdown=markdown,
    )


def static_bot_chain_checks() -> list[dict[str, Any]]:
    bot_path = DELIVERY_SRC / "bot.py"
    source = bot_path.read_text(encoding="utf-8")
    tree = ast.parse(source)
    functions = {node.name: node for node in tree.body if isinstance(node, ast.FunctionDef)}
    errors: list[str] = []
    if "_build_bot_report_markdown" not in functions:
        errors.append("bot.py must expose _build_bot_report_markdown")
    helper_source = ast.get_source_segment(source, functions.get("_build_bot_report_markdown")) or ""
    calc_source = ast.get_source_segment(source, functions.get("_calc_and_save_report")) or ""
    if "calculate_delivery_result" not in helper_source:
        errors.append("_build_bot_report_markdown must call calculate_delivery_result")
    if "generate_full_report" not in helper_source:
        errors.append("_build_bot_report_markdown must call generate_full_report")
    if 'bazi_engine="capability"' not in helper_source:
        errors.append('_build_bot_report_markdown must set bazi_engine="capability"')
    if "_build_bot_report_markdown" not in calc_source:
        errors.append("_calc_and_save_report must reuse _build_bot_report_markdown")
    return [
        {
            "id": "bot.canonical_renderer_static_chain",
            "status": "passed" if not errors else "failed",
            "path": str(bot_path.relative_to(REPO_ROOT)),
            "errors": errors,
        }
    ]


def load_capability_cli_smoke_module():
    spec = importlib.util.spec_from_file_location(
        "fatecat_capability_cli_smoke_for_semantic_diff", CAPABILITY_CLI_SMOKE
    )
    if spec is None or spec.loader is None:
        raise MultiSurfaceSemanticDiffError("cannot load capability CLI smoke module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def cli_capability_evidence() -> dict[str, Any]:
    smoke = load_capability_cli_smoke_module()
    summary = smoke.run_smoke()
    if summary.get("status") != "passed":
        raise MultiSurfaceSemanticDiffError("CLI capability smoke did not pass")

    capabilities = summary.get("capabilities", [])
    if not isinstance(capabilities, list) or not capabilities:
        raise MultiSurfaceSemanticDiffError("CLI capability smoke missing capabilities")

    required = {"almanac", "bazi", "meihua", "ziwei"}
    observed = {item.get("capabilityId") for item in capabilities if isinstance(item, dict)}
    missing = sorted(required - observed)
    if missing:
        raise MultiSurfaceSemanticDiffError(f"CLI capability smoke missing capability fixture(s): {', '.join(missing)}")

    planned_rejection = summary.get("plannedCapabilityRejection", {})
    if not isinstance(planned_rejection, dict) or planned_rejection.get("actualExitCode") != 1:
        raise MultiSurfaceSemanticDiffError("CLI capability smoke did not prove planned capability rejection")

    return {
        "surfaceId": "surface.cli",
        "status": "passed",
        "evidenceKind": summary.get("kind"),
        "semanticRole": "non_markdown_capability_json_evidence",
        "entrypoint": summary.get("entrypoint"),
        "canonicalChain": summary.get("canonicalChain", []),
        "capabilities": [
            {
                "capabilityId": item["capabilityId"],
                "status": item["status"],
                "reportProfile": item["reportProfile"],
                "stdoutSha256": item["stdoutSha256"],
                "stdoutBytes": item["stdoutBytes"],
                "dataKeys": item["dataKeys"],
                "evidenceKeys": item["evidenceKeys"],
            }
            for item in capabilities
        ],
        "plannedCapabilityRejection": {
            "capabilityId": planned_rejection.get("capabilityId"),
            "actualExitCode": planned_rejection.get("actualExitCode"),
            "stdoutSha256": planned_rejection.get("stdoutSha256"),
            "stdoutBytes": planned_rejection.get("stdoutBytes"),
            "errorContains": planned_rejection.get("errorContains"),
        },
        "nonMarkdownBoundary": (
            "CLI 当前证明 capability JSON 入口复用 CapabilityExecutor/provider registry；"
            "不把 CLI 结果纳入标准 Markdown hash 相等集合。"
        ),
    }


def static_skill_chain_checks() -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    sources = {
        "SKILL.md": (REPO_ROOT / "SKILL.md").read_text(encoding="utf-8"),
        "references/commands.md": (REPO_ROOT / "references" / "commands.md").read_text(encoding="utf-8"),
        "references/io-contract.md": (REPO_ROOT / "references" / "io-contract.md").read_text(encoding="utf-8"),
    }
    required_snippets = {
        "SKILL.md": (
            "FateCat 是面向 Agent 与应用开发者的测算基础设施",
            "bash scripts/preflight.sh --mode pure --bootstrap --pretty",
            "bash scripts/preflight.sh --mode delivery --bootstrap --pretty",
            "bash scripts/delivery-smoke.sh --target api",
            "bash scripts/delivery-smoke.sh --target bot",
            "bash scripts/acceptance.sh --with-dev",
            "bash scripts/production-readiness.sh --api-url",
        ),
        "references/commands.md": (
            "bash scripts/local-ci.sh --profile quick",
            "bash scripts/capability-cli.sh bazi",
            "bash scripts/capability-cli-smoke.sh --output-json",
            "bash scripts/acceptance.sh --with-dev",
        ),
        "references/io-contract.md": (
            "bash scripts/capability-cli.sh <capability_id>",
            "CapabilityExecutor",
            "Markdown 仍由 delivery API/Web/Bot",
        ),
    }

    for path, snippets in required_snippets.items():
        text = sources[path]
        missing = [snippet for snippet in snippets if snippet not in text]
        checks.append(
            {
                "id": f"skill.command_chain.{path}",
                "status": "passed" if not missing else "failed",
                "path": path,
                "missingSnippetCount": len(missing),
                "missingSnippets": missing,
            }
        )
    return checks


def agent_skill_evidence() -> dict[str, Any]:
    checks = static_skill_chain_checks()
    errors = [f"{check['path']} missing {check['missingSnippets']}" for check in checks if check["status"] != "passed"]
    return {
        "surfaceId": "surface.agent_skill",
        "status": "passed" if not errors else "failed",
        "semanticRole": "non_markdown_skill_command_chain_evidence",
        "checkedFiles": [check["path"] for check in checks],
        "checks": checks,
        "canonicalChain": [
            "SKILL.md",
            "references/commands.md",
            "references/io-contract.md",
            "scripts/preflight.sh",
            "scripts/capability-cli.sh",
            "scripts/delivery-smoke.sh",
            "domains/fate-analysis/services/fate-core/src/fate_core/cli.py",
            "domains/experience-delivery/services/fatecat-delivery/src/main.py",
        ],
        "nonMarkdownBoundary": (
            "Agent Skill 是安装、调用和验收说明；标准 Markdown 仍通过 delivery API/Web/Bot 链路生成，"
            "Skill 自身不得拼接报告正文。"
        ),
        "errors": errors,
    }


def surface_records(markdowns: list[SurfaceMarkdown]) -> tuple[list[dict[str, Any]], bool]:
    normalized_values: list[tuple[SurfaceMarkdown, str, list[str]]] = []
    for item in markdowns:
        normalized, applied = normalize_semantic_markdown(item.markdown)
        normalized_values.append((item, normalized, applied))

    baseline = normalized_values[0][1]
    baseline_hash = sha256_text(baseline)
    records: list[dict[str, Any]] = []
    all_equal = True
    for item, normalized, applied in normalized_values:
        is_equal = normalized == baseline
        all_equal = all_equal and is_equal
        records.append(
            {
                "surfaceId": item.surface_id,
                "route": item.route,
                "status": "passed" if is_equal else "failed",
                "byteLength": len(item.markdown.encode("utf-8")),
                "lineCount": item.markdown.count("\n") + 1,
                "rawSha256": sha256_text(item.markdown),
                "semanticSha256": sha256_text(normalized),
                "equalToBaseline": is_equal,
                "normalizedVolatilePatterns": applied,
                "baselineSemanticSha256": baseline_hash,
            }
        )
    return records, all_equal


def build_report_system_comparison(report_system: str) -> dict[str, Any]:
    client = TestClient(app)
    markdowns = [
        render_api_direct(report_system),
        render_api_http(client, report_system),
        render_api_job(client, report_system),
        render_web_direct(report_system),
        render_web_job(client, report_system),
        render_bot_dry_run(report_system),
    ]
    records, all_equal = surface_records(markdowns)
    return {
        "reportSystem": report_system,
        "status": "passed" if all_equal else "failed",
        "baselineSurface": records[0]["surfaceId"],
        "semanticSha256": records[0]["semanticSha256"],
        "surfaces": records,
    }


def assert_no_forbidden_markers(payload: dict[str, Any]) -> None:
    text = json.dumps(payload, ensure_ascii=False, sort_keys=True)
    hits = [marker for marker in FORBIDDEN_MARKERS if marker in text]
    if hits:
        raise MultiSurfaceSemanticDiffError(f"output contains forbidden marker(s): {', '.join(hits)}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate semantic equality across API/Web/Bot Markdown surfaces and CLI/Skill evidence surfaces."
    )
    parser.add_argument("--output-json", default=str(DEFAULT_OUTPUT), help="写入机器可读语义 diff 证据 JSON。")
    parser.add_argument(
        "--report-system",
        action="append",
        choices=REPORT_SYSTEMS,
        help="限定报告体系；可重复传入。默认覆盖 bazi 与 ziwei。",
    )
    parser.add_argument("--pretty", action="store_true", help="stdout 输出格式化 JSON。")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report_systems = tuple(dict.fromkeys(args.report_system or REPORT_SYSTEMS))
    bot_static_checks = static_bot_chain_checks()
    cli_skill_evidence = [cli_capability_evidence(), agent_skill_evidence()]
    comparisons = [build_report_system_comparison(report_system) for report_system in report_systems]
    errors: list[str] = []
    for comparison in comparisons:
        if comparison["status"] != "passed":
            errors.append(f"{comparison['reportSystem']} semantic hashes diverged")
    for check in bot_static_checks:
        if check["status"] != "passed":
            errors.extend(check.get("errors", []))
    for evidence in cli_skill_evidence:
        if evidence["status"] != "passed":
            errors.extend(evidence.get("errors", [f"{evidence['surfaceId']} evidence failed"]))

    status = "passed" if not errors else "failed"
    payload: dict[str, Any] = {
        "schemaVersion": 1,
        "kind": "fatecat.multi_surface_semantic_diff",
        "status": status,
        "generatedAt": utc_now(),
        "reportSystems": list(report_systems),
        "fixedFixture": {
            "profile": "beijing_test_user",
            "birthDate": "1990-01-01",
            "birthTime": "08:00",
            "birthPlace": "北京",
            "nameClass": "测试用户",
            "coordinateSource": "delivery location.get('北京')",
        },
        "semanticPolicy": {
            "comparison": "normalized_markdown_semantic_hash",
            "requiredLocalSurfaces": [
                "surface.fastapi.direct",
                "surface.fastapi.http",
                "surface.fastapi.job",
                "surface.web.direct",
                "surface.web.job",
                "surface.telegram_bot.dry_run",
            ],
            "requiredLocalEvidenceSurfaces": [
                "surface.cli",
                "surface.agent_skill",
            ],
            "volatileNormalization": [
                {
                    "field": "ziwei.inputTrace.asOf",
                    "markdownPattern": "| 运限日期 | <runtime time> |",
                    "reason": "紫微运限日期是报告生成时刻；跨异步 job 秒级差异不代表盘面语义差异。",
                }
            ],
            "noMarkdownBodyInEvidence": True,
        },
        "comparisons": comparisons,
        "botStaticChecks": bot_static_checks,
        "nonMarkdownSurfaceEvidence": cli_skill_evidence,
        "externalPending": [
            {
                "surfaceId": "surface.telegram_bot.live",
                "status": "外部连通验证待执行",
                "requiredEvidence": "真实 FATE_BOT_TOKEN 与 Telegram live smoke。",
            },
            {
                "surfaceId": "surface.huggingface_space",
                "status": "外部连通验证待执行",
                "requiredEvidence": "真实 HF Space URL 与 production-readiness live evidence。",
            },
        ],
        "errors": errors,
        "privacyBoundary": "证据只保存 Markdown hash、长度、行数、surface id 和归一化策略；不保存完整报告正文、真实用户输入、token、secret、DSN 或 webhook URL。",
    }
    assert_no_forbidden_markers(payload)

    output_path = Path(args.output_json)
    if not output_path.is_absolute():
        output_path = REPO_ROOT / output_path
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(
        json.dumps(
            payload if args.pretty else {"status": status, "outputJson": str(output_path)}, ensure_ascii=False, indent=2
        )
    )
    return 0 if status == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
