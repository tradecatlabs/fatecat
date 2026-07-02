#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
DIGEST_PATTERN = re.compile(r"^sha256:[a-f0-9]{64}$")


def run_capture(args: list[str], *, timeout_seconds: int) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
        timeout=timeout_seconds,
    )


def git_value(*args: str) -> str:
    result = run_capture(["git", *args], timeout_seconds=15)
    if result.returncode != 0:
        return ""
    return result.stdout.strip()


def redact_output(text: str) -> str:
    if not text:
        return ""
    lowered = text.lower()
    if any(marker in lowered for marker in ("token=", "secret=", "password=", "passwd=", "private_key=")):
        return "[redacted-sensitive-output]"
    return text.strip()[-4000:]


def inspect_image(image: str) -> tuple[dict[str, Any] | None, str]:
    result = run_capture(["docker", "image", "inspect", image], timeout_seconds=30)
    if result.returncode != 0:
        return None, redact_output(result.stderr or result.stdout)
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        return None, f"docker inspect invalid json: {exc.msg}"
    if not payload:
        return None, "docker inspect returned empty list"
    return payload[0], ""


def build_payload(args: argparse.Namespace) -> dict[str, Any]:
    started_at = datetime.now(UTC).isoformat()
    build_status = "skipped" if args.skip_build else "failed"
    smoke_status = "skipped" if args.skip_smoke else "failed"
    build_output = ""
    smoke_output = ""

    if not args.skip_build:
        build_result = run_capture(
            [
                "bash",
                "scripts/container-build.sh",
                "--image",
                args.image,
                "--progress",
                args.progress,
            ],
            timeout_seconds=args.build_timeout_seconds,
        )
        build_status = "passed" if build_result.returncode == 0 else "failed"
        build_output = redact_output(build_result.stdout + "\n" + build_result.stderr)
    if build_status == "failed":
        smoke_status = "skipped"
    elif not args.skip_smoke:
        smoke_result = run_capture(
            [
                "bash",
                "scripts/container-smoke.sh",
                "--image",
                args.image,
                "--skip-build",
                "--port",
                str(args.port),
                "--startup-timeout",
                str(args.startup_timeout_seconds),
            ],
            timeout_seconds=args.smoke_timeout_seconds,
        )
        smoke_status = "passed" if smoke_result.returncode == 0 else "failed"
        smoke_output = redact_output(smoke_result.stdout + "\n" + smoke_result.stderr)

    image_payload, inspect_error = inspect_image(args.image)
    image_id = ""
    repo_digests: list[str] = []
    created = ""
    architecture = ""
    os_name = ""
    if image_payload:
        image_id = str(image_payload.get("Id") or "")
        repo_digests = [str(item) for item in image_payload.get("RepoDigests") or []]
        created = str(image_payload.get("Created") or "")
        architecture = str(image_payload.get("Architecture") or "")
        os_name = str(image_payload.get("Os") or "")

    status = "passed"
    errors: list[str] = []
    if build_status not in {"passed", "skipped"}:
        errors.append("build failed")
    if smoke_status not in {"passed", "skipped"}:
        errors.append("smoke failed")
    if not DIGEST_PATTERN.match(image_id):
        errors.append("imageId is not sha256:<64 hex>")
    if args.require_smoke and smoke_status != "passed":
        errors.append("smokeStatus must be passed")
    if errors:
        status = "failed"

    finished_at = datetime.now(UTC).isoformat()
    return {
        "schemaVersion": 1,
        "kind": "fatecat.container_release_evidence",
        "status": status,
        "image": args.image,
        "imageId": image_id,
        "repoDigests": repo_digests,
        "registryDigestPresent": bool(repo_digests),
        "pushExecuted": False,
        "buildStatus": build_status,
        "smokeStatus": smoke_status,
        "generatedAt": finished_at,
        "startedAt": started_at,
        "git": {
            "branch": git_value("rev-parse", "--abbrev-ref", "HEAD"),
            "commit": git_value("rev-parse", "--verify", "HEAD"),
        },
        "docker": {
            "created": created,
            "architecture": architecture,
            "os": os_name,
            "inspectError": inspect_error,
        },
        "commands": {
            "build": f"bash scripts/container-build.sh --image {args.image} --progress {args.progress}",
            "smoke": f"bash scripts/container-smoke.sh --image {args.image} --skip-build --port {args.port} --startup-timeout {args.startup_timeout_seconds}",
        },
        "outputs": {
            "build": build_output,
            "smoke": smoke_output,
        },
        "privacyBoundary": "不读取或输出 registry token、docker login secret、用户报告正文或生产日志正文。",
        "limitations": [
            "该 evidence 证明本地 Docker image build/smoke 和 imageId，不代表 GHCR/registry RepoDigest 已推送。",
            "pushExecuted=false；真实 live release 仍需 registry digest 或远端 CI 发布证据。",
            "RepoDigests 为空时，imageId 只能作为本地 baseline digest 使用。",
        ],
        "errors": errors,
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate FateCat local container release evidence JSON")
    parser.add_argument("--output-json", required=True, help="写入 container release evidence JSON")
    parser.add_argument("--image", default="fatecat-delivery:local", help="容器镜像名")
    parser.add_argument("--port", type=int, default=8021, help="container smoke host port")
    parser.add_argument(
        "--progress", default="plain", choices=("auto", "plain", "tty", "rawjson"), help="docker build progress"
    )
    parser.add_argument("--skip-build", action="store_true", help="跳过 docker build，仅 inspect/smoke 已有镜像")
    parser.add_argument("--skip-smoke", action="store_true", help="跳过 container smoke")
    parser.add_argument(
        "--require-smoke", action=argparse.BooleanOptionalAction, default=True, help="要求 smokeStatus=passed"
    )
    parser.add_argument("--build-timeout-seconds", type=int, default=900, help="build timeout")
    parser.add_argument("--smoke-timeout-seconds", type=int, default=180, help="smoke timeout")
    parser.add_argument("--startup-timeout-seconds", type=int, default=90, help="container startup timeout")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    payload = build_payload(args)
    output_path = Path(args.output_json)
    if not output_path.is_absolute():
        output_path = REPO_ROOT / output_path
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "schemaVersion": payload["schemaVersion"],
                "status": payload["status"],
                "image": payload["image"],
                "imageId": payload["imageId"],
                "buildStatus": payload["buildStatus"],
                "smokeStatus": payload["smokeStatus"],
                "registryDigestPresent": payload["registryDigestPresent"],
                "outputJson": str(output_path),
            },
            ensure_ascii=False,
        )
    )
    return 1 if payload["status"] == "failed" else 0


if __name__ == "__main__":
    raise SystemExit(main())
