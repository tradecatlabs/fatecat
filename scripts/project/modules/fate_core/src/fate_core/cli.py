from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections.abc import Callable
from datetime import datetime
from pathlib import Path
from typing import Any, NoReturn, cast

from fate_core.support import attach_branding, build_branding_text
from fate_core.support.paths import FATE_PROFILE_DIR, FATE_REPO_ROOT
from fate_core.usecases import PureAnalysisInput, calculate_pure_analysis, normalize_gender


class BrandingArgumentParser(argparse.ArgumentParser):
    """在帮助与错误输出中强制携带品牌文案。"""

    def error(self, message: str) -> NoReturn:
        self.print_usage(sys.stderr)
        print(f"{self.prog}: error: {message}", file=sys.stderr)
        print("", file=sys.stderr)
        print(build_branding_text(compact=False), file=sys.stderr)
        raise SystemExit(2)


def _parse_datetime(value: str) -> datetime:
    normalized = value.strip()
    if not normalized:
        raise ValueError("birthDateTime 不能为空")

    if normalized.endswith("Z"):
        normalized = normalized[:-1] + "+00:00"

    try:
        parsed = datetime.fromisoformat(normalized)
        return parsed.replace(tzinfo=None) if parsed.tzinfo else parsed
    except ValueError:
        pass

    for time_format in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y/%m/%d %H:%M:%S", "%Y/%m/%d %H:%M"):
        try:
            return datetime.strptime(normalized, time_format)
        except ValueError:
            continue

    raise ValueError(f"无法解析出生时间: {value}")


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
    birth_place_value = raw_payload.get("birthPlace")
    birth_place_object: dict[str, Any] = birth_place_value if isinstance(birth_place_value, dict) else {}
    raw_options = raw_payload.get("options")
    options: dict[str, Any] = raw_options if isinstance(raw_options, dict) else {}

    birth_datetime = _first_non_empty(
        raw_payload.get("birthDateTime"),
        raw_payload.get("birth_datetime"),
        raw_payload.get("birth_dt"),
        raw_payload.get("datetime"),
    )
    if not birth_datetime and raw_payload.get("birthDate") and raw_payload.get("birthTime"):
        birth_datetime = f"{raw_payload['birthDate']} {raw_payload['birthTime']}"

    longitude = _first_non_empty(
        raw_payload.get("longitude"),
        raw_payload.get("lng"),
        birth_place_object.get("longitude"),
        birth_place_object.get("lng"),
    )
    latitude = _first_non_empty(
        raw_payload.get("latitude"),
        raw_payload.get("lat"),
        birth_place_object.get("latitude"),
        birth_place_object.get("lat"),
    )
    birth_place_name = _first_non_empty(
        raw_payload.get("birth_place"),
        raw_payload.get("birthPlaceName"),
        birth_place_value if isinstance(birth_place_value, str) else None,
        birth_place_object.get("name"),
    )
    use_true_solar_time = _first_non_empty(
        raw_payload.get("useTrueSolarTime"),
        raw_payload.get("use_true_solar_time"),
        options.get("useTrueSolarTime"),
    )

    normalized = {
        "birthDateTime": birth_datetime,
        "gender": _first_non_empty(raw_payload.get("gender"), raw_payload.get("sex")),
        "longitude": longitude,
        "latitude": latitude,
        "name": raw_payload.get("name"),
        "birthPlace": birth_place_name or "",
        "useTrueSolarTime": _parse_bool(use_true_solar_time, default=True),
    }

    missing = [
        field for field in ("birthDateTime", "gender", "longitude", "latitude") if normalized[field] in (None, "")
    ]
    if missing:
        raise ValueError(f"缺少必填字段: {', '.join(missing)}")

    normalized["longitude"] = float(normalized["longitude"])
    normalized["latitude"] = float(normalized["latitude"])
    normalized["gender"] = normalize_gender(str(normalized["gender"]))
    return normalized


def _build_pure_analysis_input(payload: dict[str, Any]) -> PureAnalysisInput:
    normalized = _normalize_payload(payload)
    return PureAnalysisInput(
        birth_dt=_parse_datetime(str(normalized["birthDateTime"])),
        gender=str(normalized["gender"]),
        longitude=normalized["longitude"],
        latitude=normalized["latitude"],
        name=normalized["name"],
        birth_place=str(normalized["birthPlace"]),
        use_true_solar_time=normalized["useTrueSolarTime"],
    )


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
    assets_dir = FATE_REPO_ROOT / "assets"
    config_dir = assets_dir / "config"
    env_path = config_dir / ".env"
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
    add_path_check("schema", assets_dir / "database" / "bazi" / "schema_v2.sql")
    add_path_check("coordinates", assets_dir / "data" / "china_coordinates.csv")
    add_path_check("lunar_python", assets_dir / "vendor" / "github" / "lunar-python-master")
    add_path_check("bazi_1", assets_dir / "vendor" / "github" / "bazi-1-master")
    add_path_check("sxwnl", assets_dir / "vendor" / "github" / "sxwnl-master")

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


def _run_serve(args: argparse.Namespace) -> int:
    start_script = FATE_REPO_ROOT / "modules" / "telegram" / "start.py"
    command = [sys.executable, str(start_script), args.mode]
    print(build_branding_text(compact=False))
    print("")
    completed = subprocess.run(command, cwd=FATE_REPO_ROOT, check=False)
    return completed.returncode


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

    serve_parser = subparsers.add_parser("serve", help="启动 Telegram 交付层")
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
