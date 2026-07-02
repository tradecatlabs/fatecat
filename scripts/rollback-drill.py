#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class Precheck:
    id: str
    name: str
    status: str
    required: bool
    evidence: str
    detail: str = ""

    def to_json(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "status": self.status,
            "required": self.required,
            "evidence": self.evidence,
            "detail": self.detail,
        }


def run_capture(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=REPO_ROOT, text=True, capture_output=True, check=False, timeout=15)


def git_value(*args: str) -> str:
    result = run_capture(["git", *args])
    if result.returncode != 0:
        return ""
    return result.stdout.strip()


def repo_path(value: str) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path
    return REPO_ROOT / path


def file_precheck(check_id: str, name: str, path: str, *, required: bool = True) -> Precheck:
    absolute = repo_path(path)
    exists = absolute.is_file()
    return Precheck(
        id=check_id,
        name=name,
        status="passed" if exists else "failed",
        required=required,
        evidence=path,
        detail="" if exists else "file missing",
    )


def dir_precheck(check_id: str, name: str, path: str, *, required: bool = False) -> Precheck:
    if not path:
        return Precheck(check_id, name, "skipped", required, "not provided", "optional input not provided")
    absolute = repo_path(path)
    exists = absolute.is_dir()
    return Precheck(
        id=check_id,
        name=name,
        status="passed" if exists else "failed",
        required=required,
        evidence=str(absolute),
        detail="" if exists else "directory missing",
    )


def optional_file_precheck(check_id: str, name: str, path: str) -> Precheck:
    if not path:
        return Precheck(check_id, name, "skipped", False, "not provided", "optional input not provided")
    absolute = repo_path(path)
    exists = absolute.is_file()
    return Precheck(
        id=check_id,
        name=name,
        status="passed" if exists else "failed",
        required=False,
        evidence=str(absolute),
        detail="" if exists else "file missing",
    )


def build_candidate_commands() -> list[dict[str, Any]]:
    return [
        {
            "id": "container.previous_image",
            "description": "回滚到上一个已验证 delivery 容器 tag，并重新执行容器 smoke 后推送。",
            "command": "bash scripts/container-release.sh --image ghcr.io/<owner>/fatecat-delivery --tag <previous-good-tag> --push",
            "requiresManualApproval": True,
            "executesInDryRun": False,
        },
        {
            "id": "hf.previous_bundle",
            "description": "用上一个已验证 Hugging Face Space bundle 重新上传 Space。",
            "command": "bash scripts/hf-space-deploy.sh --space <owner>/<space> --bundle-dir <previous-good-bundle> --commit-message 'rollback FateCat HF Space'",
            "requiresManualApproval": True,
            "executesInDryRun": False,
        },
        {
            "id": "post_rollback_readiness",
            "description": "回滚后重新验证生产 API、HF Space、Bot 和 release gate 证据。",
            "command": "bash scripts/live-release-gate.sh --require-live --api-url <live-api-url> --hf-space-url <live-hf-space-url> --run-live-bot --output-json <rollback-release-evidence.json>",
            "requiresManualApproval": True,
            "executesInDryRun": False,
        },
    ]


def build_payload(args: argparse.Namespace) -> dict[str, Any]:
    required_documents = [
        "docs/deployment/huggingface-space.md",
        "docs/reference-materials/operations/测算基础设施 API 接入.md",
        "contracts/fate/delivery/release-gate.json",
        "contracts/fate/delivery/registry.json",
    ]
    required_scripts = [
        "scripts/container-release.sh",
        "scripts/hf-space-deploy.sh",
        "scripts/production-readiness.sh",
        "scripts/public-release-gate.sh",
        "scripts/live-release-gate.sh",
    ]

    prechecks: list[Precheck] = []
    for index, path in enumerate(required_documents, start=1):
        prechecks.append(file_precheck(f"document.{index}", f"Required rollback document: {path}", path))
    for index, path in enumerate(required_scripts, start=1):
        prechecks.append(file_precheck(f"script.{index}", f"Required rollback script: {path}", path))
    prechecks.append(
        dir_precheck("artifact.release_artifacts", "Release artifacts directory", args.release_artifacts_dir)
    )
    prechecks.append(optional_file_precheck("artifact.local_ci_summary", "Local CI summary", args.local_ci_summary))
    prechecks.append(
        optional_file_precheck("artifact.public_release_summary", "Public release summary", args.public_release_summary)
    )

    required_failures = [check for check in prechecks if check.required and check.status != "passed"]
    status = "failed" if required_failures else "passed"
    commit = git_value("rev-parse", "--verify", "HEAD")
    branch = git_value("rev-parse", "--abbrev-ref", "HEAD")

    return {
        "schemaVersion": 1,
        "kind": "fatecat.rollback_drill_evidence",
        "status": status,
        "mode": "dry-run",
        "productionRollbackExecuted": False,
        "generatedAt": datetime.now(UTC).isoformat(),
        "git": {
            "branch": branch,
            "commit": commit,
        },
        "prechecks": [check.to_json() for check in prechecks],
        "candidateCommands": build_candidate_commands(),
        "requiredDocuments": [
            {
                "path": path,
                "exists": repo_path(path).is_file(),
            }
            for path in required_documents
        ],
        "artifacts": {
            "releaseArtifactsDir": str(repo_path(args.release_artifacts_dir)) if args.release_artifacts_dir else "",
            "localCiSummary": str(repo_path(args.local_ci_summary)) if args.local_ci_summary else "",
            "publicReleaseSummary": str(repo_path(args.public_release_summary)) if args.public_release_summary else "",
        },
        "privacyBoundary": "不读取或输出 token、secret、DSN、用户报告正文、生产日志正文或真实用户输入。",
        "limitations": [
            "该 evidence 是本地 dry-run rollback drill，不代表真实生产流量已切换。",
            "真实 live release 前仍需 operator 在目标平台执行或签署真实 rollback drill。",
            "候选命令只记录回滚路径，不会由本脚本自动执行。",
        ],
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate FateCat rollback drill evidence JSON")
    parser.add_argument("--output-json", required=True, help="写入 rollback drill evidence JSON")
    parser.add_argument("--release-artifacts-dir", default="", help="release artifacts 目录，可选")
    parser.add_argument("--local-ci-summary", default="", help="local-ci summary.json，可选")
    parser.add_argument("--public-release-summary", default="", help="public-release summary.txt，可选")
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
                "mode": payload["mode"],
                "outputJson": str(output_path),
                "prechecks": len(payload["prechecks"]),
                "candidateCommands": len(payload["candidateCommands"]),
            },
            ensure_ascii=False,
        )
    )
    return 1 if payload["status"] == "failed" else 0


if __name__ == "__main__":
    raise SystemExit(main())
