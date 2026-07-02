#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
DELIVERY_DIR = REPO_ROOT / "contracts" / "fate" / "delivery"
RELEASE_GATE_PATH = DELIVERY_DIR / "release-gate.json"
RELEASE_GATE_SCHEMA_PATH = DELIVERY_DIR / "schemas" / "release-gate.schema.json"
DELIVERY_REGISTRY_PATH = DELIVERY_DIR / "registry.json"
RESOURCE_SCHEMA_PATH = REPO_ROOT / "contracts" / "fate" / "capabilities" / "schemas" / "resource.schema.json"

SENSITIVE_ASSIGNMENT_TERMS = (
    "token",
    "secret",
    "password",
    "passwd",
    "api[_-]?key",
    "private[_-]?key",
    "DATABASE_URL",
    "DB_DSN",
)
SENSITIVE_BLOCK_TERMS = ("BEGIN RSA", "BEGIN OPENSSH")
SENSITIVE_PATTERN = re.compile(
    "(" + "|".join([rf"{term}\s*=" for term in SENSITIVE_ASSIGNMENT_TERMS] + list(SENSITIVE_BLOCK_TERMS)) + ")",
    re.IGNORECASE,
)
DIGEST_PATTERN = re.compile(r"^sha256:[a-f0-9]{64}$")


@dataclass
class Check:
    id: str
    name: str
    category: str
    status: str
    required_for_live_release: bool
    evidence: str
    external_connectivity: str
    detail: str = ""

    def to_json(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "status": self.status,
            "requiredForLiveRelease": self.required_for_live_release,
            "evidence": self.evidence,
            "externalConnectivity": self.external_connectivity,
            "detail": self.detail,
        }


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def run_capture(args: list[str], *, timeout_seconds: int = 30) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        timeout=timeout_seconds,
        check=False,
    )


def git_value(*args: str) -> str:
    result = run_capture(["git", *args], timeout_seconds=10)
    if result.returncode != 0:
        return ""
    return result.stdout.strip()


def count_status_lines(prefixes: tuple[str, ...] | None = None) -> int:
    result = run_capture(["git", "status", "--porcelain"], timeout_seconds=10)
    if result.returncode != 0:
        return 0
    lines = [line for line in result.stdout.splitlines() if line.strip()]
    if prefixes is None:
        return len(lines)
    return sum(1 for line in lines if line.startswith(prefixes))


def redact(text: str) -> str:
    if not text:
        return ""
    if SENSITIVE_PATTERN.search(text):
        return "[redacted-sensitive-output]"
    return text.strip()[:800]


def is_https_url(url: str) -> bool:
    return url.startswith("https://")


def url_without_secret(url: str) -> str:
    if not url:
        return ""
    if "@" in url.split("://", 1)[-1] or "token" in url.lower() or "secret" in url.lower():
        return "[redacted-url]"
    return url.rstrip("/")


def http_get(url: str, *, timeout_seconds: int) -> tuple[int, str]:
    request = urllib.request.Request(url, headers={"User-Agent": "fatecat-live-release-gate/1.0"})
    with urllib.request.urlopen(request, timeout=timeout_seconds) as response:  # noqa: S310 - release gate only requests operator-provided URLs.
        body = response.read(200_000).decode("utf-8", errors="replace")
        return int(response.status), body


def check_http_endpoint(url: str, marker: str | None, *, timeout_seconds: int) -> tuple[bool, str]:
    try:
        status, body = http_get(url, timeout_seconds=timeout_seconds)
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        return False, f"request failed: {exc.__class__.__name__}"
    if status < 200 or status >= 300:
        return False, f"unexpected status={status}"
    if marker and marker not in body:
        return False, f"missing marker={marker}"
    return True, f"status={status}"


def path_or_url_exists(value: str) -> tuple[bool, str]:
    if not value:
        return False, "not provided"
    if value.startswith(("https://", "http://")):
        if not value.startswith("https://"):
            return False, "artifact URL must use HTTPS"
        return True, url_without_secret(value)
    path = Path(value)
    if not path.is_absolute():
        path = REPO_ROOT / path
    if not path.is_file():
        return False, f"artifact not found: {path}"
    return True, str(path)


def read_json_evidence(value: str, *, timeout_seconds: int) -> tuple[bool, str, dict[str, Any] | None, str]:
    if not value:
        return False, "not provided", None, "not provided"
    if value.startswith(("https://", "http://")):
        if not value.startswith("https://"):
            return False, "artifact URL must use HTTPS", None, "artifact URL must use HTTPS"
        evidence = url_without_secret(value)
        try:
            status, body = http_get(value, timeout_seconds=timeout_seconds)
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            return False, evidence, None, f"request failed: {exc.__class__.__name__}"
        if status < 200 or status >= 300:
            return False, evidence, None, f"unexpected status={status}"
        try:
            payload = json.loads(body)
        except json.JSONDecodeError as exc:
            return False, evidence, None, f"invalid json: {exc.msg}"
        if not isinstance(payload, dict):
            return False, evidence, None, "json root must be an object"
        return True, evidence, payload, ""

    path = Path(value)
    if not path.is_absolute():
        path = REPO_ROOT / path
    if not path.is_file():
        return False, f"artifact not found: {path}", None, f"artifact not found: {path}"
    try:
        payload = load_json(path)
    except json.JSONDecodeError as exc:
        return False, str(path), None, f"invalid json: {exc.msg}"
    if not isinstance(payload, dict):
        return False, str(path), None, "json root must be an object"
    return True, str(path), payload, ""


def check_local_ci_summary(
    value: str,
    *,
    current_commit: str,
    timeout_seconds: int,
) -> tuple[str, str, str]:
    ok, evidence, payload, detail = read_json_evidence(value, timeout_seconds=timeout_seconds)
    if not ok or payload is None:
        return "fail", evidence, detail

    errors: list[str] = []
    if payload.get("schemaVersion") != 1:
        errors.append("schemaVersion must be 1")
    if payload.get("kind") != "fatecat.local_ci_summary":
        errors.append("kind must be fatecat.local_ci_summary")
    if payload.get("profile") != "quick":
        errors.append("profile must be quick")
    if payload.get("status") != "passed":
        errors.append("status must be passed")
    if payload.get("commit") != current_commit:
        errors.append("summary commit does not match current HEAD")

    artifacts = payload.get("artifacts")
    if not isinstance(artifacts, dict):
        errors.append("artifacts must be an object")
    else:
        for key in ("releaseArtifacts", "liveReleaseGate"):
            if not artifacts.get(key):
                errors.append(f"artifacts.{key} is required")

    if errors:
        return "fail", evidence, "; ".join(errors)
    return "pass", evidence, f"profile=quick; commit={current_commit}; finishedAt={payload.get('finishedAt', '')}"


def check_rollback_drill_evidence(
    value: str,
    *,
    current_commit: str,
    timeout_seconds: int,
) -> tuple[str, str, str]:
    ok, evidence, payload, detail = read_json_evidence(value, timeout_seconds=timeout_seconds)
    if not ok or payload is None:
        return "fail", evidence, detail

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
        errors.append("productionRollbackExecuted must be false for local evidence")

    git_payload = payload.get("git")
    if not isinstance(git_payload, dict) or git_payload.get("commit") != current_commit:
        errors.append("rollback drill commit does not match current HEAD")

    prechecks = payload.get("prechecks")
    if not isinstance(prechecks, list) or not prechecks:
        errors.append("prechecks must be a non-empty list")
    else:
        failed_required = [
            item.get("id", "<unknown>")
            for item in prechecks
            if isinstance(item, dict) and item.get("required") is True and item.get("status") != "passed"
        ]
        if failed_required:
            errors.append("required prechecks failed: " + ", ".join(failed_required))

    candidate_commands = payload.get("candidateCommands")
    if not isinstance(candidate_commands, list) or not candidate_commands:
        errors.append("candidateCommands must be a non-empty list")
    else:
        for item in candidate_commands:
            if not isinstance(item, dict) or not item.get("command"):
                errors.append("candidateCommands entries must include command")
                break
            if item.get("executesInDryRun") is not False:
                errors.append("candidateCommands must not execute during dry-run")
                break

    required_documents = payload.get("requiredDocuments")
    if not isinstance(required_documents, list) or not required_documents:
        errors.append("requiredDocuments must be a non-empty list")
    elif any(not isinstance(item, dict) or item.get("exists") is not True for item in required_documents):
        errors.append("requiredDocuments must all exist")

    if errors:
        return "fail", evidence, "; ".join(errors)
    return "pass", evidence, f"mode=dry-run; commit={current_commit}; commands={len(candidate_commands)}"


def check_container_release_evidence(
    value: str,
    *,
    current_commit: str,
    timeout_seconds: int,
) -> tuple[str, str, str]:
    ok, evidence, payload, detail = read_json_evidence(value, timeout_seconds=timeout_seconds)
    if not ok or payload is None:
        return "fail", evidence, detail

    errors: list[str] = []
    if payload.get("schemaVersion") != 1:
        errors.append("schemaVersion must be 1")
    if payload.get("kind") != "fatecat.container_release_evidence":
        errors.append("kind must be fatecat.container_release_evidence")
    if payload.get("status") != "passed":
        errors.append("status must be passed")
    image_id = str(payload.get("imageId") or "")
    if not DIGEST_PATTERN.match(image_id):
        errors.append("imageId must be sha256:<64 hex>")
    if payload.get("buildStatus") not in {"passed", "skipped"}:
        errors.append("buildStatus must be passed or skipped")
    if payload.get("smokeStatus") != "passed":
        errors.append("smokeStatus must be passed")
    if payload.get("pushExecuted") is not False:
        errors.append("pushExecuted must be false for local evidence")

    git_payload = payload.get("git")
    if not isinstance(git_payload, dict) or git_payload.get("commit") != current_commit:
        errors.append("container evidence commit does not match current HEAD")

    if errors:
        return "fail", evidence, "; ".join(errors)

    repo_digests = payload.get("repoDigests")
    repo_digest_count = len(repo_digests) if isinstance(repo_digests, list) else 0
    return "pass", evidence, f"imageId={image_id}; repoDigests={repo_digest_count}; smoke=passed"


def require_evidence_by_id(policy: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {item["id"]: item for item in policy["requiredEvidence"]}


def check_contracts() -> list[str]:
    errors: list[str] = []
    policy = load_json(RELEASE_GATE_PATH)
    schema = load_json(RELEASE_GATE_SCHEMA_PATH)
    delivery_registry = load_json(DELIVERY_REGISTRY_PATH)
    resource_schema = load_json(RESOURCE_SCHEMA_PATH)

    required_fields = set(schema["requiredReleaseGateFields"])
    missing = required_fields - set(policy)
    if missing:
        errors.append(f"release-gate.json missing fields: {', '.join(sorted(missing))}")

    evidence_fields = set(schema["requiredEvidenceFields"])
    for evidence in policy.get("requiredEvidence", []):
        evidence_missing = evidence_fields - set(evidence)
        if evidence_missing:
            errors.append(f"{evidence.get('id', '<missing-id>')} missing: {', '.join(sorted(evidence_missing))}")

    required_ids = {
        "evidence.local_ci_quick",
        "evidence.remote_ci_current_commit",
        "evidence.production_api_live",
        "evidence.hf_space_live",
        "evidence.telegram_bot_live",
        "evidence.container_digest",
        "evidence.sbom_artifact",
        "evidence.provenance_artifact",
        "evidence.rollback_drill",
        "evidence.clean_git_state",
    }
    actual_ids = {item["id"] for item in policy.get("requiredEvidence", [])}
    missing_ids = required_ids - actual_ids
    if missing_ids:
        errors.append(f"release gate missing required evidence ids: {', '.join(sorted(missing_ids))}")

    if "ReleaseGate" not in resource_schema.get("resourceTypes", []):
        errors.append("resource schema does not declare ReleaseGate")
    if delivery_registry.get("schemas", {}).get("releaseGate") != str(RELEASE_GATE_SCHEMA_PATH.relative_to(REPO_ROOT)):
        errors.append("delivery registry does not reference release-gate schema")
    if delivery_registry.get("releaseGate", {}).get("contract") != str(RELEASE_GATE_PATH.relative_to(REPO_ROOT)):
        errors.append("delivery registry does not reference release-gate contract")

    for path in (
        REPO_ROOT / "scripts" / "production-readiness.sh",
        REPO_ROOT / "scripts" / "live-bot-smoke.sh",
        REPO_ROOT / "scripts" / "hf-space-deploy.sh",
        REPO_ROOT / "scripts" / "container-release.sh",
        REPO_ROOT / "scripts" / "public-release-gate.sh",
        REPO_ROOT / ".github" / "workflows" / "acceptance.yml",
        REPO_ROOT / ".github" / "workflows" / "container.yml",
        REPO_ROOT / ".github" / "workflows" / "hf-space-deploy.yml",
    ):
        if not path.exists():
            errors.append(f"release dependency file missing: {path.relative_to(REPO_ROOT)}")

    serialized = json.dumps(policy, ensure_ascii=False)
    if SENSITIVE_PATTERN.search(serialized):
        errors.append("release-gate contract appears to contain sensitive inline value")
    return errors


def build_checks(args: argparse.Namespace, evidence_by_id: dict[str, dict[str, Any]]) -> list[Check]:
    checks: list[Check] = []

    def add(
        evidence_id: str,
        status: str,
        evidence: str,
        *,
        detail: str = "",
    ) -> None:
        item = evidence_by_id[evidence_id]
        checks.append(
            Check(
                id=evidence_id,
                name=item["name"],
                category=item["category"],
                status=status,
                required_for_live_release=bool(item["requiredForLiveRelease"]),
                evidence=redact(evidence),
                external_connectivity=item["externalConnectivity"],
                detail=redact(detail),
            )
        )

    current_commit = git_value("rev-parse", "--verify", "HEAD")

    local_ci_summary = args.local_ci_summary or os.getenv("FATE_LOCAL_CI_SUMMARY", "")
    if local_ci_summary:
        status, evidence, detail = check_local_ci_summary(
            local_ci_summary,
            current_commit=current_commit,
            timeout_seconds=args.timeout_seconds,
        )
        add("evidence.local_ci_quick", status, evidence, detail=detail)
    else:
        add("evidence.local_ci_quick", "pending", "local CI summary not provided")

    ci_run_url = args.github_run_url or os.getenv("FATE_GITHUB_ACTIONS_RUN_URL", "")
    ci_commit = args.github_commit or os.getenv("FATE_GITHUB_ACTIONS_COMMIT", "")
    if ci_run_url and ci_commit:
        if not ci_run_url.startswith("https://github.com/"):
            add("evidence.remote_ci_current_commit", "fail", "GitHub Actions run URL must be github.com HTTPS")
        elif ci_commit != current_commit:
            add(
                "evidence.remote_ci_current_commit",
                "fail",
                url_without_secret(ci_run_url),
                detail=f"ci commit {ci_commit} != current commit {current_commit}",
            )
        else:
            add("evidence.remote_ci_current_commit", "pass", url_without_secret(ci_run_url), detail=current_commit)
    else:
        add(
            "evidence.remote_ci_current_commit",
            "pending",
            "GitHub Actions run URL/current commit evidence not provided",
        )

    api_url = url_without_secret(args.api_url or os.getenv("FATE_LIVE_API_URL", ""))
    if api_url:
        if not is_https_url(api_url):
            add("evidence.production_api_live", "fail", api_url, detail="API URL must use HTTPS")
        else:
            failures: list[str] = []
            for suffix, marker in (("/health", None), ("/ready", None), ("/metrics", "fatecat_requests_total")):
                ok, detail = check_http_endpoint(f"{api_url}{suffix}", marker, timeout_seconds=args.timeout_seconds)
                if not ok:
                    failures.append(f"{suffix}: {detail}")
            add(
                "evidence.production_api_live",
                "fail" if failures else "pass",
                api_url,
                detail="; ".join(failures) if failures else "/health /ready /metrics ok",
            )
    else:
        add("evidence.production_api_live", "pending", "production API URL not provided")

    hf_space_url = url_without_secret(args.hf_space_url or os.getenv("FATE_HF_SPACE_URL", ""))
    if hf_space_url:
        if not (hf_space_url.startswith("https://") and ".hf.space" in hf_space_url):
            add("evidence.hf_space_live", "fail", hf_space_url, detail="HF Space URL must be HTTPS *.hf.space")
        else:
            web_url = hf_space_url.rstrip("/")
            if not web_url.endswith("/web"):
                web_url = f"{web_url}/web"
            ok, detail = check_http_endpoint(web_url, "FateCat", timeout_seconds=args.timeout_seconds)
            add("evidence.hf_space_live", "pass" if ok else "fail", web_url, detail=detail)
    else:
        add("evidence.hf_space_live", "pending", "Hugging Face Space URL not provided")

    bot_token_present = bool(os.getenv("FATE_BOT_TOKEN", "").strip())
    if args.run_live_bot:
        if not bot_token_present:
            add("evidence.telegram_bot_live", "fail", "FATE_BOT_TOKEN not provided")
        else:
            result = run_capture(["bash", "scripts/live-bot-smoke.sh"], timeout_seconds=max(args.timeout_seconds, 30))
            if result.returncode == 0:
                add("evidence.telegram_bot_live", "pass", "scripts/live-bot-smoke.sh", detail=redact(result.stdout))
            else:
                add(
                    "evidence.telegram_bot_live",
                    "fail",
                    "scripts/live-bot-smoke.sh",
                    detail=redact(result.stderr or result.stdout),
                )
    elif bot_token_present:
        add("evidence.telegram_bot_live", "pending", "FATE_BOT_TOKEN present; rerun with --run-live-bot")
    else:
        add("evidence.telegram_bot_live", "pending", "FATE_BOT_TOKEN not provided")

    digest = args.container_digest or os.getenv("FATE_CONTAINER_IMAGE_DIGEST", "")
    container_evidence_path = args.container_evidence_path or os.getenv("FATE_CONTAINER_RELEASE_EVIDENCE_PATH", "")
    if container_evidence_path:
        status, evidence, detail = check_container_release_evidence(
            container_evidence_path,
            current_commit=current_commit,
            timeout_seconds=args.timeout_seconds,
        )
        add("evidence.container_digest", status, evidence, detail=detail)
    elif digest:
        add(
            "evidence.container_digest",
            "pass" if DIGEST_PATTERN.match(digest) else "fail",
            digest if DIGEST_PATTERN.match(digest) else "invalid digest format",
        )
    else:
        add("evidence.container_digest", "pending", "container digest not provided")

    sbom_path = args.sbom_path or os.getenv("FATE_RELEASE_SBOM_PATH", "")
    ok, evidence = path_or_url_exists(sbom_path)
    add("evidence.sbom_artifact", "pass" if ok else "pending", evidence)

    provenance_path = args.provenance_path or os.getenv("FATE_RELEASE_PROVENANCE_PATH", "")
    ok, evidence = path_or_url_exists(provenance_path)
    add("evidence.provenance_artifact", "pass" if ok else "pending", evidence)

    rollback_path = args.rollback_evidence_path or os.getenv("FATE_ROLLBACK_DRILL_EVIDENCE_PATH", "")
    if rollback_path:
        status, evidence, detail = check_rollback_drill_evidence(
            rollback_path,
            current_commit=current_commit,
            timeout_seconds=args.timeout_seconds,
        )
        add("evidence.rollback_drill", status, evidence, detail=detail)
    else:
        add("evidence.rollback_drill", "pending", "rollback drill evidence not provided")

    dirty_count = count_status_lines()
    untracked_count = count_status_lines(("??",))
    if dirty_count == 0:
        add("evidence.clean_git_state", "pass", "git status clean")
    else:
        add(
            "evidence.clean_git_state",
            "fail" if args.require_clean_worktree else "pending",
            f"dirty_count={dirty_count}; untracked_count={untracked_count}",
            detail="clean worktree required for live release",
        )

    return checks


def summarize(checks: list[Check], *, require_live: bool) -> dict[str, Any]:
    counts = {
        "pass": sum(1 for check in checks if check.status == "pass"),
        "pending": sum(1 for check in checks if check.status == "pending"),
        "fail": sum(1 for check in checks if check.status == "fail"),
    }
    required_blocking = [
        check.id for check in checks if check.required_for_live_release and check.status in {"pending", "fail"}
    ]
    if any(check.status == "fail" for check in checks):
        ship_status = "fail" if require_live else "blocked"
    elif required_blocking:
        ship_status = "blocked"
    else:
        ship_status = "pass"
    return {
        "checks": len(checks),
        "passed": counts["pass"],
        "pending": counts["pending"],
        "failed": counts["fail"],
        "requiredBlocking": required_blocking,
        "shipGateStatus": ship_status,
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="FateCat live release evidence gate")
    parser.add_argument("--output-json", default="", help="写入 gate JSON 摘要")
    parser.add_argument("--require-live", action="store_true", help="要求所有 live release 必需证据通过")
    parser.add_argument("--require-clean-worktree", action="store_true", help="要求 git worktree 干净")
    parser.add_argument("--run-live-bot", action="store_true", help="使用真实 FATE_BOT_TOKEN 调用 Telegram get_me")
    parser.add_argument("--api-url", default="", help="真实生产 API 根地址")
    parser.add_argument("--hf-space-url", default="", help="真实 Hugging Face Space 根地址或 /web 地址")
    parser.add_argument("--github-run-url", default="", help="当前 commit 对应 GitHub Actions run URL")
    parser.add_argument("--github-commit", default="", help="GitHub Actions run head SHA")
    parser.add_argument("--container-digest", default="", help="容器镜像 digest，格式 sha256:<64 hex>")
    parser.add_argument(
        "--container-evidence-path", default="", help="container release evidence JSON 本地路径或 HTTPS URL"
    )
    parser.add_argument("--sbom-path", default="", help="SBOM artifact 本地路径或 HTTPS URL")
    parser.add_argument("--provenance-path", default="", help="provenance artifact 本地路径或 HTTPS URL")
    parser.add_argument("--rollback-evidence-path", default="", help="rollback drill artifact 本地路径或 HTTPS URL")
    parser.add_argument(
        "--local-ci-summary", default="", help="local-ci/public-release gate summary 本地路径或 HTTPS URL"
    )
    parser.add_argument("--timeout-seconds", type=int, default=8, help="单个外部请求超时")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    if args.require_live:
        args.require_clean_worktree = True
        args.run_live_bot = True

    contract_errors = check_contracts()
    policy = load_json(RELEASE_GATE_PATH)
    evidence_by_id = require_evidence_by_id(policy)
    checks = build_checks(args, evidence_by_id)
    for error in contract_errors:
        checks.append(
            Check(
                id="contract.release_gate",
                name="Release gate contract integrity",
                category="local_ci",
                status="fail",
                required_for_live_release=True,
                evidence="contract validation",
                external_connectivity="not_required",
                detail=error,
            )
        )

    summary = summarize(checks, require_live=args.require_live)
    branch = git_value("rev-parse", "--abbrev-ref", "HEAD")
    commit = git_value("rev-parse", "--verify", "HEAD")
    dirty_count = count_status_lines()
    untracked_count = count_status_lines(("??",))

    top_status = "failed" if contract_errors or (args.require_live and summary["requiredBlocking"]) else "passed"
    result = {
        "schemaVersion": 1,
        "generatedAt": datetime.now(UTC).isoformat(),
        "status": top_status,
        "mode": "live-required" if args.require_live else "local-contract",
        "releaseGate": str(RELEASE_GATE_PATH.relative_to(REPO_ROOT)),
        "git": {
            "branch": branch,
            "commit": commit,
            "dirtyCount": dirty_count,
            "untrackedCount": untracked_count,
            "clean": dirty_count == 0,
        },
        "summary": summary,
        "shipGate": {
            "status": summary["shipGateStatus"],
            "blockingItems": summary["requiredBlocking"],
            "policy": policy["shipGate"]["policy"],
        },
        "checks": [check.to_json() for check in checks],
        "privacyBoundary": policy["metadata"]["privacy"],
    }

    serialized = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output_json:
        output_path = Path(args.output_json)
        if not output_path.is_absolute():
            output_path = REPO_ROOT / output_path
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(serialized + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "status": result["status"],
                "mode": result["mode"],
                "shipGate": result["shipGate"]["status"],
                "checks": summary["checks"],
                "passed": summary["passed"],
                "pending": summary["pending"],
                "failed": summary["failed"],
            },
            ensure_ascii=False,
        )
    )
    return 1 if result["status"] == "failed" else 0


if __name__ == "__main__":
    raise SystemExit(main())
