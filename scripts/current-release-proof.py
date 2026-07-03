#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
DIGEST_PATTERN = re.compile(r"^sha256:[0-9a-f]{64}$")
SENSITIVE_PATTERN = re.compile(
    r"(gh[pousr]_[A-Za-z0-9_]+|token\s*=|secret\s*=|password\s*=|passwd\s*=|private[_-]?key\s*=|BEGIN RSA|BEGIN OPENSSH)",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class ProofCheck:
    id: str
    name: str
    category: str
    status: str
    required: bool
    evidence: str
    detail: str = ""

    def to_json(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "status": self.status,
            "required": self.required,
            "evidence": self.evidence,
            "detail": self.detail,
        }


def run_capture(args: list[str], *, timeout_seconds: int = 30) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        timeout=timeout_seconds,
        check=False,
    )


def redact(text: str) -> str:
    if not text:
        return ""
    stripped = text.strip()
    if SENSITIVE_PATTERN.search(stripped):
        return "[redacted-sensitive-output]"
    return stripped[-2000:]


def git_value(*args: str) -> str:
    result = run_capture(["git", *args], timeout_seconds=15)
    if result.returncode != 0:
        return ""
    return result.stdout.strip()


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as fh:
        payload = json.load(fh)
    if not isinstance(payload, dict):
        raise ValueError("json root must be object")
    return payload


def gh_json(args: list[str], *, timeout_seconds: int = 45) -> tuple[Any | None, str]:
    result = run_capture(["gh", *args], timeout_seconds=timeout_seconds)
    if result.returncode != 0:
        return None, redact(result.stderr or result.stdout)
    try:
        return json.loads(result.stdout), ""
    except json.JSONDecodeError as exc:
        return None, f"invalid gh json: {exc.msg}"


def origin_repo_slug() -> str:
    payload, error = gh_json(["repo", "view", "--json", "nameWithOwner"], timeout_seconds=20)
    if isinstance(payload, dict):
        name_with_owner = payload.get("nameWithOwner")
        if isinstance(name_with_owner, str) and "/" in name_with_owner:
            return name_with_owner
    remote = git_value("remote", "get-url", "origin")
    if remote.startswith("https://github.com/"):
        return remote.removeprefix("https://github.com/").removesuffix(".git")
    if remote.startswith("git@github.com:"):
        return remote.removeprefix("git@github.com:").removesuffix(".git")
    if error:
        return ""
    return remote


def workflow_run_from_view(run_id: str) -> tuple[dict[str, Any] | None, str]:
    payload, error = gh_json(
        [
            "run",
            "view",
            run_id,
            "--json",
            "databaseId,headSha,status,conclusion,displayTitle,url,createdAt,event,workflowName",
        ],
        timeout_seconds=45,
    )
    if isinstance(payload, dict):
        return payload, ""
    return None, error


def find_successful_run(
    *,
    workflow: str,
    branch: str,
    commit: str,
    limit: int,
    run_id: str,
) -> tuple[dict[str, Any] | None, str]:
    if run_id:
        payload, error = workflow_run_from_view(run_id)
        if payload is None:
            return None, error
        return payload, ""
    payload, error = gh_json(
        [
            "run",
            "list",
            "--workflow",
            workflow,
            "--branch",
            branch,
            "--limit",
            str(limit),
            "--json",
            "databaseId,headSha,status,conclusion,displayTitle,url,createdAt,event,workflowName",
        ],
        timeout_seconds=45,
    )
    if not isinstance(payload, list):
        return None, error
    candidates = [
        item
        for item in payload
        if isinstance(item, dict)
        and item.get("headSha") == commit
        and item.get("status") == "completed"
        and item.get("conclusion") == "success"
    ]
    if not candidates:
        return None, f"no successful {workflow} run for {commit[:12]}"
    return candidates[0], ""


def check_run(
    *,
    check_id: str,
    name: str,
    workflow: str,
    branch: str,
    commit: str,
    limit: int,
    run_id: str,
    skip_remote: bool,
) -> tuple[ProofCheck, dict[str, Any] | None]:
    if skip_remote:
        return (
            ProofCheck(check_id, name, "github_actions", "pending", True, "remote check skipped"),
            None,
        )
    payload, error = find_successful_run(
        workflow=workflow,
        branch=branch,
        commit=commit,
        limit=limit,
        run_id=run_id,
    )
    if payload is None:
        return ProofCheck(check_id, name, "github_actions", "pending", True, "not found", error), None
    errors: list[str] = []
    if payload.get("headSha") != commit:
        errors.append("headSha does not match current commit")
    if payload.get("status") != "completed":
        errors.append("run is not completed")
    if payload.get("conclusion") != "success":
        errors.append("run conclusion is not success")
    status = "fail" if errors else "pass"
    return (
        ProofCheck(
            check_id,
            name,
            "github_actions",
            status,
            True,
            str(payload.get("url", "")),
            "; ".join(errors) if errors else f"runId={payload.get('databaseId')}",
        ),
        payload,
    )


def list_run_artifacts(repo: str, run_id: int | str) -> tuple[list[dict[str, Any]], str]:
    payload, error = gh_json(
        ["api", f"repos/{repo}/actions/runs/{run_id}/artifacts", "--paginate"],
        timeout_seconds=45,
    )
    if not isinstance(payload, dict):
        return [], error
    artifacts = payload.get("artifacts")
    if not isinstance(artifacts, list):
        return [], "artifacts field missing"
    return [item for item in artifacts if isinstance(item, dict)], ""


def inspect_registry_digest(image_ref: str) -> tuple[str, str]:
    result = run_capture(
        ["docker", "buildx", "imagetools", "inspect", image_ref, "--format", "{{json .Manifest}}"],
        timeout_seconds=60,
    )
    if result.returncode != 0:
        return "", redact(result.stderr or result.stdout)
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        return "", f"docker manifest json invalid: {exc.msg}"
    digest = str(payload.get("digest", ""))
    if not DIGEST_PATTERN.match(digest):
        return "", f"manifest digest invalid: {digest}"
    return digest, ""


def verify_attestation(oci_ref: str, repo: str) -> tuple[bool, str]:
    result = run_capture(
        ["gh", "attestation", "verify", f"oci://{oci_ref}", "--repo", repo],
        timeout_seconds=90,
    )
    if result.returncode != 0:
        return False, redact(result.stderr or result.stdout)
    return True, redact(result.stdout)


def check_rollback_evidence(path_text: str, *, current_commit: str) -> ProofCheck:
    if not path_text:
        return ProofCheck(
            "release.rollback_drill",
            "Rollback drill evidence",
            "rollback",
            "pending",
            True,
            "not provided",
        )
    path = Path(path_text)
    if not path.is_absolute():
        path = REPO_ROOT / path
    try:
        payload = load_json(path)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return ProofCheck(
            "release.rollback_drill",
            "Rollback drill evidence",
            "rollback",
            "fail",
            True,
            str(path),
            f"invalid rollback evidence: {exc.__class__.__name__}",
        )
    errors: list[str] = []
    if payload.get("schemaVersion") != 1:
        errors.append("schemaVersion must be 1")
    if payload.get("kind") != "fatecat.rollback_drill_evidence":
        errors.append("kind must be fatecat.rollback_drill_evidence")
    if payload.get("status") != "passed":
        errors.append("status must be passed")
    if payload.get("mode") != "dry-run":
        errors.append("mode must be dry-run")
    if payload.get("productionRollbackExecuted") is not False:
        errors.append("productionRollbackExecuted must be false")
    git_payload = payload.get("git")
    if not isinstance(git_payload, dict) or git_payload.get("commit") != current_commit:
        errors.append("rollback commit must match current HEAD")
    return ProofCheck(
        "release.rollback_drill",
        "Rollback drill evidence",
        "rollback",
        "fail" if errors else "pass",
        True,
        str(path),
        "; ".join(errors) if errors else "dry-run rollback evidence accepted",
    )


def build_payload(args: argparse.Namespace) -> dict[str, Any]:
    commit = args.commit or git_value("rev-parse", "--verify", "HEAD")
    branch = args.branch or git_value("rev-parse", "--abbrev-ref", "HEAD")
    short_sha = commit[:12]
    repo = args.repo or origin_repo_slug()
    image = args.container_image
    tag = args.container_tag or short_sha
    image_ref = f"{image}:{tag}"
    checks: list[ProofCheck] = []

    dirty_lines = [line for line in git_value("status", "--porcelain").splitlines() if line.strip()]
    checks.append(
        ProofCheck(
            "release.git_clean",
            "Clean git state",
            "git",
            "pass" if not dirty_lines else "fail",
            True,
            "git status --porcelain",
            "" if not dirty_lines else f"dirtyCount={len(dirty_lines)}",
        )
    )

    origin_head = git_value("rev-parse", "--verify", f"origin/{branch}")
    checks.append(
        ProofCheck(
            "release.origin_current",
            "Origin branch contains current commit",
            "git",
            "pass" if origin_head == commit else "pending",
            True,
            f"origin/{branch}",
            "origin matches HEAD"
            if origin_head == commit
            else f"originHead={origin_head[:12] if origin_head else 'missing'}",
        )
    )

    acceptance_check, acceptance_run = check_run(
        check_id="release.acceptance_current_commit",
        name="Acceptance workflow for current commit",
        workflow=args.acceptance_workflow,
        branch=branch,
        commit=commit,
        limit=args.run_limit,
        run_id=args.acceptance_run_id,
        skip_remote=args.skip_remote,
    )
    checks.append(acceptance_check)

    container_check, container_run = check_run(
        check_id="release.container_workflow_current_commit",
        name="Container workflow for current commit",
        workflow=args.container_workflow,
        branch=branch,
        commit=commit,
        limit=args.run_limit,
        run_id=args.container_run_id,
        skip_remote=args.skip_remote,
    )
    checks.append(container_check)

    container_run_id = container_run.get("databaseId") if isinstance(container_run, dict) else ""
    expected_artifact = f"fatecat-release-artifacts-{commit}"
    artifact_detail = "container run not available"
    artifact_evidence = expected_artifact
    artifact_status = "pending"
    if args.skip_remote:
        artifact_detail = "remote check skipped"
    elif container_run_id:
        artifacts, artifact_error = list_run_artifacts(repo, container_run_id)
        matching = [item for item in artifacts if item.get("name") == expected_artifact and not item.get("expired")]
        if matching:
            artifact_status = "pass"
            artifact_evidence = str(matching[0].get("archive_download_url") or expected_artifact)
            artifact_detail = f"artifactId={matching[0].get('id')}; size={matching[0].get('size_in_bytes')}"
        else:
            artifact_detail = artifact_error or f"missing artifact {expected_artifact}"
    checks.append(
        ProofCheck(
            "release.release_artifacts_uploaded",
            "Remote release artifacts uploaded",
            "release_artifact",
            artifact_status,
            True,
            artifact_evidence,
            artifact_detail,
        )
    )

    digest = args.container_digest
    digest_detail = ""
    if args.skip_remote and not digest:
        checks.append(
            ProofCheck(
                "release.container_registry_digest",
                "Container registry digest",
                "container",
                "pending",
                True,
                image_ref,
                "remote check skipped",
            )
        )
    else:
        if not digest:
            digest, digest_detail = inspect_registry_digest(image_ref)
        checks.append(
            ProofCheck(
                "release.container_registry_digest",
                "Container registry digest",
                "container",
                "pass" if DIGEST_PATTERN.match(digest) else "fail",
                True,
                f"{image}@{digest}" if DIGEST_PATTERN.match(digest) else image_ref,
                digest_detail or f"tag={tag}",
            )
        )

    if not DIGEST_PATTERN.match(digest):
        checks.append(
            ProofCheck(
                "release.container_attestation",
                "Container attestation verification",
                "attestation",
                "pending",
                True,
                image_ref,
                "container digest missing",
            )
        )
    elif args.skip_remote:
        checks.append(
            ProofCheck(
                "release.container_attestation",
                "Container attestation verification",
                "attestation",
                "pending",
                True,
                f"{image}@{digest}",
                "remote check skipped",
            )
        )
    else:
        ok, detail = verify_attestation(f"{image}@{digest}", repo)
        checks.append(
            ProofCheck(
                "release.container_attestation",
                "Container attestation verification",
                "attestation",
                "pass" if ok else "fail",
                True,
                f"oci://{image}@{digest}",
                detail,
            )
        )

    checks.append(check_rollback_evidence(args.rollback_evidence_path, current_commit=commit))

    failed = [item.id for item in checks if item.required and item.status == "fail"]
    pending = [item.id for item in checks if item.required and item.status == "pending"]
    gate_status = "fail" if failed else "blocked" if pending else "passed"
    status = "failed" if args.require_current_release and gate_status != "passed" else "passed"

    return {
        "schemaVersion": 1,
        "kind": "fatecat.current_release_proof",
        "status": status,
        "mode": "required-current-release" if args.require_current_release else "local-contract",
        "generatedAt": datetime.now(UTC).isoformat(),
        "git": {
            "branch": branch,
            "commit": commit,
            "originHead": origin_head,
            "dirtyCount": len(dirty_lines),
        },
        "github": {
            "repo": repo,
            "acceptanceWorkflow": args.acceptance_workflow,
            "containerWorkflow": args.container_workflow,
            "acceptanceRunId": acceptance_run.get("databaseId") if isinstance(acceptance_run, dict) else "",
            "containerRunId": container_run_id,
        },
        "container": {
            "image": image,
            "tag": tag,
            "digest": digest if DIGEST_PATTERN.match(digest) else "",
            "pushedRef": f"{image}@{digest}" if DIGEST_PATTERN.match(digest) else "",
        },
        "checks": [item.to_json() for item in checks],
        "proofGate": {
            "status": gate_status,
            "blockingItems": failed + pending,
            "failedItems": failed,
            "pendingItems": pending,
        },
        "privacyBoundary": "不读取或输出 GitHub token、registry token、secret、DSN、用户输入、报告正文或生产日志正文。",
        "limitations": [
            "该 gate 只证明当前 commit 的 release proof，不证明生产 API/HF/Bot live 已全部通过。",
            "rollback drill 为 dry-run 时只能证明回滚路径可审计，不代表真实生产流量已切换。",
            "缺少真实外部证据时必须保持 blocked 或 failed，不能伪造成 release ready。",
        ],
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Assemble and verify current commit release proof evidence.")
    parser.add_argument("--output-json", required=True, help="写入 current release proof JSON")
    parser.add_argument("--require-current-release", action="store_true", help="缺少当前 release proof 时返回非零")
    parser.add_argument("--skip-remote", action="store_true", help="跳过 gh/docker 远端查询，仅输出 pending 合同")
    parser.add_argument("--commit", default="", help="覆盖当前 commit，默认 git HEAD")
    parser.add_argument("--branch", default="", help="覆盖当前分支，默认 git 当前分支")
    parser.add_argument("--repo", default="", help="GitHub repo slug，默认从 gh/git origin 推断")
    parser.add_argument("--run-limit", type=int, default=30, help="查询最近 workflow run 数量")
    parser.add_argument("--acceptance-workflow", default="acceptance.yml", help="acceptance workflow 文件名")
    parser.add_argument("--container-workflow", default="container.yml", help="container workflow 文件名")
    parser.add_argument("--acceptance-run-id", default="", help="显式 acceptance run id")
    parser.add_argument("--container-run-id", default="", help="显式 container run id")
    parser.add_argument("--container-image", default="ghcr.io/tradecatlabs/fatecat-delivery", help="GHCR image")
    parser.add_argument("--container-tag", default="", help="容器 tag，默认当前 commit 短 SHA 12 位")
    parser.add_argument("--container-digest", default="", help="已知 registry digest，格式 sha256:<64 hex>")
    parser.add_argument("--rollback-evidence-path", default="", help="rollback drill evidence JSON")
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
                "status": payload["status"],
                "mode": payload["mode"],
                "proofGate": payload["proofGate"]["status"],
                "checks": len(payload["checks"]),
                "pending": len(payload["proofGate"]["pendingItems"]),
                "failed": len(payload["proofGate"]["failedItems"]),
                "outputJson": str(output_path),
            },
            ensure_ascii=False,
        )
    )
    return 1 if payload["status"] == "failed" else 0


if __name__ == "__main__":
    raise SystemExit(main())
