#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
DELIVERY_SRC = REPO_ROOT / "domains" / "experience-delivery" / "services" / "fatecat-delivery" / "src"
FATE_CORE_SRC = REPO_ROOT / "domains" / "fate-analysis" / "services" / "fate-core" / "src"
DEFAULT_OUTPUT = REPO_ROOT / "infra" / "runtime" / "local-state" / "exports" / "developer" / "openapi.json"
REQUIRED_PATHS = [
    "/metadata",
    "/capabilities",
    "/capabilities/{capability_id}",
    "/capabilities/{capability_id}/calculate",
    "/providers",
    "/providers/{provider_id}",
    "/errors",
    "/evaluations",
    "/evaluations/{evaluation_id}",
    "/observability",
    "/observability/{signal_id}",
    "/security",
    "/security/{control_id}",
    "/surfaces",
    "/surfaces/{surface_id}",
    "/reports",
    "/api/v1/report/jobs",
    "/api/v1/report/jobs/{job_id}",
    "/api/v1/report/jobs/{job_id}/cancel",
]


class OpenAPIExportError(RuntimeError):
    """OpenAPI 导出未满足开发者接入基线。"""


def _load_app():
    for path in (str(DELIVERY_SRC), str(FATE_CORE_SRC)):
        if path not in sys.path:
            sys.path.insert(0, path)
    from main import app  # noqa: PLC0415

    return app


def _operation_ids(schema: dict[str, Any]) -> list[str]:
    ids: list[str] = []
    for path_item in schema.get("paths", {}).values():
        if not isinstance(path_item, dict):
            continue
        for method_spec in path_item.values():
            if isinstance(method_spec, dict) and method_spec.get("operationId"):
                ids.append(str(method_spec["operationId"]))
    return ids


def validate_openapi_schema(schema: dict[str, Any]) -> None:
    version = str(schema.get("openapi", ""))
    if not version.startswith("3."):
        raise OpenAPIExportError(f"OpenAPI version must start with 3.x, got {version!r}")

    paths = schema.get("paths")
    if not isinstance(paths, dict):
        raise OpenAPIExportError("OpenAPI schema missing paths object")

    missing = [path for path in REQUIRED_PATHS if path not in paths]
    if missing:
        raise OpenAPIExportError(f"OpenAPI schema missing required paths: {', '.join(missing)}")

    ids = _operation_ids(schema)
    duplicate_ids = sorted({operation_id for operation_id in ids if ids.count(operation_id) > 1})
    if duplicate_ids:
        raise OpenAPIExportError(f"OpenAPI schema contains duplicate operationIds: {', '.join(duplicate_ids)}")


def export_openapi(output: Path = DEFAULT_OUTPUT) -> dict[str, Any]:
    app = _load_app()
    schema = app.openapi()
    validate_openapi_schema(schema)

    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8") as fh:
        json.dump(schema, fh, ensure_ascii=False, indent=2)
        fh.write("\n")

    return {
        "schemaVersion": 1,
        "generatedAt": datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "status": "passed",
        "output": str(output),
        "openapi": schema.get("openapi"),
        "pathCount": len(schema.get("paths", {})),
        "requiredPathCount": len(REQUIRED_PATHS),
        "operationIdCount": len(_operation_ids(schema)),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="导出 FateCat OpenAPI JSON，并校验开发者接入必备路径。")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="OpenAPI JSON 输出路径。")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        summary = export_openapi(args.output)
        print(json.dumps(summary, ensure_ascii=False))
        return 0
    except OpenAPIExportError as exc:
        print(f"openapi export error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
