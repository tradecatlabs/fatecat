from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Callable
from datetime import datetime
from pathlib import Path
from typing import Any, NoReturn, cast

from fate_core.capabilities import CapabilityExecutor, CapabilityInput, list_capabilities
from fate_core.support import attach_branding, build_branding_text
from fate_core.support.paths import (
    FATE_CONFIG_ROOT,
    FATE_DATA_ROOT,
    FATE_DATABASE_ROOT,
    FATE_PROFILE_DIR,
    FATE_REPO_ROOT,
    FATE_VENDOR_ROOT,
)
from fate_core.usecases import (
    PureAnalysisInput,
    build_pure_analysis_input_from_payload,
    calculate_pure_analysis,
    normalize_pure_analysis_payload,
    parse_datetime,
)


class BrandingArgumentParser(argparse.ArgumentParser):
    """在帮助与错误输出中强制携带品牌文案。"""

    def error(self, message: str) -> NoReturn:
        self.print_usage(sys.stderr)
        print(f"{self.prog}: error: {message}", file=sys.stderr)
        print("", file=sys.stderr)
        print(build_branding_text(compact=False), file=sys.stderr)
        raise SystemExit(2)


def _parse_datetime(value: str) -> datetime:
    return parse_datetime(value)


def _parse_bool(value: Any, default: bool = True) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)

    normalized = str(value).strip().lower()
    if normalized in {"1", "true", "yes", "y", "on", "是"}:
        return True
    if normalized in {"0", "false", "no", "n", "off", "否"}:
        return False
    raise ValueError(f"无法解析布尔值: {value}")


def _first_non_empty(*values: Any) -> Any:
    for value in values:
        if value not in (None, ""):
            return value
    return None


def _load_json_payload(args: argparse.Namespace) -> dict[str, Any]:
    raw_text = None

    if args.input_json:
        raw_text = args.input_json
    elif args.input_file:
        raw_text = Path(args.input_file).read_text(encoding="utf-8")
    elif not sys.stdin.isatty():
        stdin_text = sys.stdin.read()
        if stdin_text.strip():
            raw_text = stdin_text

    if raw_text is not None:
        payload = json.loads(raw_text)
        if not isinstance(payload, dict):
            raise ValueError("输入 JSON 必须是对象")
        return payload

    return {
        "birthDateTime": args.birth_datetime,
        "gender": args.gender,
        "longitude": args.longitude,
        "latitude": args.latitude,
        "name": args.name,
        "birthPlace": args.birth_place,
        "useTrueSolarTime": args.use_true_solar_time,
    }


def _normalize_payload(raw_payload: dict[str, Any]) -> dict[str, Any]:
    return normalize_pure_analysis_payload(raw_payload)


def _build_pure_analysis_input(payload: dict[str, Any]) -> PureAnalysisInput:
    return build_pure_analysis_input_from_payload(payload)


def _write_json_payload(payload: dict[str, Any], *, pretty: bool, output_file: str | None = None) -> None:
    serialized = json.dumps(payload, ensure_ascii=False, indent=2 if pretty else None)
    if output_file:
        target_path = Path(output_file)
        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_text(serialized + "\n", encoding="utf-8")
        return
    print(serialized)


def _load_env_values(env_path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not env_path.exists():
        return values

    for line in env_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, raw_value = stripped.split("=", 1)
        values[key.strip()] = raw_value.strip().strip("'\"")
    return values


def _collect_health_report(mode: str) -> dict[str, Any]:
    env_path = FATE_CONFIG_ROOT / ".env"
    checks: list[dict[str, Any]] = []

    def add_path_check(name: str, path: Path, *, required: bool = True) -> None:
        exists = path.exists()
        checks.append(
            {
                "name": name,
                "required": required,
                "path": str(path),
                "ok": exists if required else True,
                "exists": exists,
            }
        )

    add_path_check("profile", FATE_PROFILE_DIR / "pure_analysis.json")
    add_path_check("schema", FATE_DATABASE_ROOT / "bazi" / "schema_v2.sql")
    add_path_check("location_catalog", FATE_DATA_ROOT / "locations" / "location_catalog.ndjson.gz")
    add_path_check("location_manifest", FATE_DATA_ROOT / "locations" / "manifest.json")
    add_path_check("lunar_python", FATE_VENDOR_ROOT / "github" / "lunar-python-master")
    add_path_check("bazi_1", FATE_VENDOR_ROOT / "github" / "bazi-1-master")
    add_path_check("sxwnl", FATE_VENDOR_ROOT / "github" / "sxwnl-master")

    env_values = _load_env_values(env_path)
    if mode == "delivery":
        checks.append(
            {
                "name": "env_file",
                "required": True,
                "path": str(env_path),
                "ok": env_path.exists(),
                "exists": env_path.exists(),
            }
        )
        checks.append(
            {
                "name": "bot_token",
                "required": True,
                "path": str(env_path),
                "ok": bool(env_values.get("FATE_BOT_TOKEN")),
                "exists": bool(env_values.get("FATE_BOT_TOKEN")),
            }
        )

    ok = all(item["ok"] for item in checks)
    return {
        "success": ok,
        "mode": mode,
        "repoRoot": str(FATE_REPO_ROOT),
        "checks": checks,
    }


def _run_pure_analysis(args: argparse.Namespace) -> int:
    payload = _load_json_payload(args)
    pure_input = _build_pure_analysis_input(payload)
    result = calculate_pure_analysis(pure_input)
    _write_json_payload(
        attach_branding(
            {
                "success": True,
                "profile": "pure_analysis",
                "data": result,
            }
        ),
        pretty=args.pretty,
        output_file=args.output_file,
    )
    return 0


def _run_health(args: argparse.Namespace) -> int:
    report = _collect_health_report(args.mode)
    pretty = args.json or args.pretty
    _write_json_payload(attach_branding(report), pretty=pretty, output_file=args.output_file)
    return 0 if report["success"] else 1


def _run_capabilities(args: argparse.Namespace) -> int:
    capabilities = [
        {
            "capabilityId": item.capability_id,
            "name": item.name,
            "tradition": item.tradition,
            "status": item.status,
            "defaultVisibility": item.default_visibility,
            "maturity": {
                "level": item.maturity_level,
                "status": item.maturity_status,
                "summary": item.maturity_summary,
            },
            "engine": {
                "provider": item.provider,
                "engineVersion": item.engine_version,
                "deterministic": item.deterministic,
            },
            "reportProfile": item.report_profile,
            "evidencePolicy": item.evidence_policy,
            "testGate": item.test_gate,
            "riskLevel": item.risk_level,
        }
        for item in list_capabilities()
    ]
    _write_json_payload(attach_branding({"success": True, "capabilities": capabilities}), pretty=args.pretty)
    return 0


def _run_capability_execute(args: argparse.Namespace) -> int:
    payload = _load_json_payload(args)
    result = CapabilityExecutor().execute(CapabilityInput(capability_id=args.capability_id, payload=payload))
    _write_json_payload(
        attach_branding(
            {
                "success": True,
                "capabilityId": result.capability_id,
                "status": result.status,
                "reportProfile": result.report_profile,
                "data": result.data,
                "evidence": result.evidence,
                "risk": result.risk,
                "metadata": getattr(result, "metadata", {}),
            }
        ),
        pretty=args.pretty,
        output_file=args.output_file,
    )
    return 0


def _run_serve(args: argparse.Namespace) -> int:
    print(build_branding_text(compact=False))
    print("")
    print("fate-core CLI 只负责纯分析与 capability 执行；交付服务请从 delivery 服务入口启动。", file=sys.stderr)
    return 2


def build_parser() -> argparse.ArgumentParser:
    parser = BrandingArgumentParser(
        prog="fatecat",
        description="FateCat 命理分析与交付 CLI",
        epilog=build_branding_text(compact=False),
        formatter_class=argparse.RawTextHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    pure_parser = subparsers.add_parser("pure-analysis", help="执行纯命理分析并输出 JSON")
    pure_parser.add_argument("--input-json", help="直接传入 JSON 字符串")
    pure_parser.add_argument("--input-file", help="从 JSON 文件读取输入")
    pure_parser.add_argument("--birth-datetime", help="出生时间，支持 1990-01-01 08:00:00 或 ISO8601")
    pure_parser.add_argument("--gender", help="性别，如 男 / 女")
    pure_parser.add_argument("--longitude", type=float, help="出生地经度")
    pure_parser.add_argument("--latitude", type=float, help="出生地纬度")
    pure_parser.add_argument("--name", help="姓名")
    pure_parser.add_argument("--birth-place", help="出生地名称")
    pure_parser.add_argument("--use-true-solar-time", default=True, type=_parse_bool, help="是否启用真太阳时")
    pure_parser.add_argument("--output-file", help="将结果写入指定文件")
    pure_parser.add_argument("--pretty", action="store_true", help="格式化输出 JSON")
    pure_parser.set_defaults(handler=_run_pure_analysis)

    health_parser = subparsers.add_parser("health", help="检查纯分析或交付层依赖是否就绪")
    health_parser.add_argument("--mode", choices=("pure", "delivery"), default="pure", help="检查模式")
    health_parser.add_argument("--json", action="store_true", help="以 JSON 友好模式输出")
    health_parser.add_argument("--pretty", action="store_true", help="格式化输出 JSON")
    health_parser.add_argument("--output-file", help="将结果写入指定文件")
    health_parser.set_defaults(handler=_run_health)

    capabilities_parser = subparsers.add_parser("capabilities", help="列出统一测算能力注册表")
    capabilities_parser.add_argument("--pretty", action="store_true", help="格式化输出 JSON")
    capabilities_parser.set_defaults(handler=_run_capabilities)

    capability_parser = subparsers.add_parser("capability", help="执行指定生产化测算能力")
    capability_parser.add_argument("capability_id", help="能力 ID，例如 bazi")
    capability_parser.add_argument("--input-json", help="直接传入 JSON 字符串")
    capability_parser.add_argument("--input-file", help="从 JSON 文件读取输入")
    capability_parser.add_argument("--birth-datetime", help="出生时间，支持 1990-01-01 08:00:00 或 ISO8601")
    capability_parser.add_argument("--gender", help="性别，如 男 / 女")
    capability_parser.add_argument("--longitude", type=float, help="出生地经度")
    capability_parser.add_argument("--latitude", type=float, help="出生地纬度")
    capability_parser.add_argument("--name", help="姓名")
    capability_parser.add_argument("--birth-place", help="出生地名称")
    capability_parser.add_argument("--use-true-solar-time", default=True, type=_parse_bool, help="是否启用真太阳时")
    capability_parser.add_argument("--output-file", help="将结果写入指定文件")
    capability_parser.add_argument("--pretty", action="store_true", help="格式化输出 JSON")
    capability_parser.set_defaults(handler=_run_capability_execute)

    serve_parser = subparsers.add_parser("serve", help="提示交付服务启动边界")
    serve_parser.add_argument("mode", choices=("bot", "api", "both"), help="启动模式")
    serve_parser.set_defaults(handler=_run_serve)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        handler = cast(Callable[[argparse.Namespace], int], args.handler)
        return handler(args)
    except Exception as exc:
        _write_json_payload(attach_branding({"success": False, "error": str(exc)}), pretty=True)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
