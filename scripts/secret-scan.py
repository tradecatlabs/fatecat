#!/usr/bin/env python3
from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import math
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ALLOWLIST = ROOT / "contracts/fate/security/secret-scan-allowlist.json"
DEFAULT_OUTPUT = ROOT / "infra/runtime/local-state/exports/security/secret-scan.json"
MAX_FILE_BYTES = 1_000_000

SECRET_PATTERNS: tuple[tuple[str, str, re.Pattern[str]], ...] = (
    (
        "private_key",
        "high",
        re.compile(r"-----BEGIN (?:RSA |DSA |EC |OPENSSH |PGP )?PRIVATE KEY-----"),
    ),
    ("aws_access_key_id", "high", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("github_token", "high", re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{36,255}\b")),
    ("openai_api_key", "high", re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{20,}\b")),
    ("slack_token", "high", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{20,}\b")),
    ("telegram_bot_token", "high", re.compile(r"\b\d{8,12}:[A-Za-z0-9_-]{35,}\b")),
    (
        "jwt",
        "medium",
        re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b"),
    ),
    (
        "dsn_with_password",
        "high",
        re.compile(r"(?i)\b(?:postgres(?:ql)?|mysql|mongodb(?:\+srv)?|redis)://[^/\s:@]+:[^@\s/]+@"),
    ),
)

GENERIC_ASSIGNMENT = re.compile(
    r"(?i)\b(?P<name>[A-Z0-9_]*(?:TOKEN|SECRET|API[_-]?KEY|PASSWORD|PASSWD|PRIVATE[_-]?KEY|DATABASE_URL|DB_DSN|WEBHOOK)[A-Z0-9_-]*)\b"
    r"\s*(?:=|:)\s*(?P<value>['\"]?[^'\"\s#;,]+)"
)


@dataclass(frozen=True)
class Finding:
    path: str
    line: int
    rule: str
    severity: str
    variable: str | None
    fingerprint: str
    redacted: str


def shannon_entropy(value: str) -> float:
    if not value:
        return 0.0
    counts = {char: value.count(char) for char in set(value)}
    length = len(value)
    return -sum((count / length) * math.log2(count / length) for count in counts.values())


def fingerprint(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8", errors="ignore")).hexdigest()[:16]


def redact(value: str) -> str:
    clean = value.strip()
    if len(clean) <= 8:
        return "<redacted>"
    return f"{clean[:3]}...{clean[-3:]} (len={len(clean)})"


def load_allowlist(path: Path = DEFAULT_ALLOWLIST) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def is_placeholder(value: str, allowlist: dict[str, Any]) -> bool:
    lowered = value.strip().strip("'\"").lower()
    if not lowered:
        return True
    if lowered.startswith(("<", "${", "$", "{")):
        return True
    placeholder_tokens = [str(item).lower() for item in allowlist.get("placeholderTokens", [])]
    if any(token and token in lowered for token in placeholder_tokens):
        return True
    if any(marker in lowered for marker in ("example", "placeholder", "dummy", "fake", "test", "sample", "your")):
        return True
    return False


def is_allowed_line(line: str, allowlist: dict[str, Any]) -> bool:
    return any(fragment in line for fragment in allowlist.get("allowedValueFragments", []))


def path_is_excluded(path: str, allowlist: dict[str, Any]) -> bool:
    excluded = allowlist.get("excludedPathPrefixes", [])
    return any(path.startswith(prefix) for prefix in excluded)


def should_scan_path(path: str, allowlist: dict[str, Any]) -> bool:
    if path_is_excluded(path, allowlist):
        return False
    ignored_globs = (
        "*.png",
        "*.jpg",
        "*.jpeg",
        "*.gif",
        "*.webp",
        "*.ico",
        "*.pdf",
        "*.zip",
        "*.xlsx",
        "*.xls",
        "*.sqlite",
        "*.sqlite3",
        "*.db",
        "*.pyc",
    )
    return not any(fnmatch.fnmatch(path, pattern) for pattern in ignored_globs)


def scan_line(path: str, line_number: int, line: str, allowlist: dict[str, Any]) -> list[Finding]:
    if is_allowed_line(line, allowlist):
        return []

    findings: list[Finding] = []
    for rule, severity, pattern in SECRET_PATTERNS:
        for match in pattern.finditer(line):
            value = match.group(0)
            if is_placeholder(value, allowlist):
                continue
            findings.append(
                Finding(
                    path=path,
                    line=line_number,
                    rule=rule,
                    severity=severity,
                    variable=None,
                    fingerprint=fingerprint(value),
                    redacted=redact(value),
                )
            )

    for match in GENERIC_ASSIGNMENT.finditer(line):
        variable = match.group("name")
        raw_value = match.group("value").strip().strip("'\"")
        if "(" in raw_value or ")" in raw_value:
            continue
        if is_placeholder(raw_value, allowlist):
            continue
        if len(raw_value) < 20 and "://" not in raw_value:
            continue
        if "://" not in raw_value and shannon_entropy(raw_value) < 3.5:
            continue
        findings.append(
            Finding(
                path=path,
                line=line_number,
                rule="generic_secret_assignment",
                severity="medium",
                variable=variable,
                fingerprint=fingerprint(raw_value),
                redacted=redact(raw_value),
            )
        )

    return findings


def scan_text(path: str, content: str, allowlist: dict[str, Any]) -> list[Finding]:
    findings: list[Finding] = []
    for index, line in enumerate(content.splitlines(), start=1):
        findings.extend(scan_line(path, index, line, allowlist))
    return findings


def git_candidate_files(root: Path) -> list[str]:
    result = subprocess.run(
        ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
        cwd=root,
        check=True,
        capture_output=True,
        text=False,
    )
    return [item.decode("utf-8") for item in result.stdout.split(b"\0") if item]


def read_text_file(path: Path) -> str | None:
    try:
        if path.stat().st_size > MAX_FILE_BYTES:
            return None
        return path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return None


def scan_repository(root: Path = ROOT, allowlist_path: Path = DEFAULT_ALLOWLIST) -> dict[str, Any]:
    allowlist = load_allowlist(allowlist_path)
    findings: list[Finding] = []
    scanned_files = 0
    skipped_files = 0

    for relative_path in git_candidate_files(root):
        if not should_scan_path(relative_path, allowlist):
            skipped_files += 1
            continue
        content = read_text_file(root / relative_path)
        if content is None:
            skipped_files += 1
            continue
        scanned_files += 1
        findings.extend(scan_text(relative_path, content, allowlist))

    payload_findings = [
        {
            "path": item.path,
            "line": item.line,
            "rule": item.rule,
            "severity": item.severity,
            "variable": item.variable,
            "fingerprint": item.fingerprint,
            "redacted": item.redacted,
        }
        for item in findings
    ]
    return {
        "schemaVersion": 1,
        "generatedAt": datetime.now(UTC).isoformat(),
        "scanner": "fatecat-secret-scan",
        "status": "passed" if not findings else "failed",
        "summary": {
            "scannedFiles": scanned_files,
            "skippedFiles": skipped_files,
            "findingCount": len(findings),
        },
        "findings": payload_findings,
        "privacyBoundary": "summary 不输出疑似密钥原文；只输出路径、行号、规则、severity、短指纹和脱敏长度。",
        "scope": "tracked and untracked non-ignored first-party text files; excludes reference repos, archive and binary/large files.",
    }


def write_summary(summary: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="扫描 tracked first-party 文件中的疑似真实 secret。")
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--allowlist", type=Path, default=DEFAULT_ALLOWLIST)
    args = parser.parse_args(argv)

    summary = scan_repository(ROOT, args.allowlist)
    write_summary(summary, args.output_json)
    print(json.dumps({"status": summary["status"], **summary["summary"]}, ensure_ascii=False))
    return 0 if summary["status"] == "passed" else 1


if __name__ == "__main__":
    sys.exit(main())
