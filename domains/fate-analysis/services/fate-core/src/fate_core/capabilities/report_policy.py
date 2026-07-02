from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import Any

# Ponytail existence: report policy gate is the smallest auditable guard between
# generated report summaries and capability risk policy. It deliberately stays
# dependency-free; richer NLP/snapshot gates belong to later infrastructure slices.
# Owner: tradecatlabs/fate-core. Verification: test_capability_protocol.py.

POLICY_GATE_VERSION = "report-policy-gate-v1"
POLICY_MATCH_ENGINE = "literal-substring-v1"
SNAPSHOT_GATE_VERSION = "markdown-snapshot-gate-v1"

_REQUIRED_MARKDOWN_HEADINGS: dict[str, tuple[str, ...]] = {
    "bazi": (
        "# 命理排盘报告：",
        "## 第一卷：先天命格（静态分析）",
        "## 第二卷：后天运路（动态趋势）",
        "## 第三卷：民俗与建议（生活应用）",
    ),
    "ziwei": (
        "# 紫微斗数报告：",
        "## 紫微斗数",
        "## 紫微结构解读（依据版）",
        "### 大限/流年联动",
    ),
}


def build_report_policy_gate(
    *,
    content: Any,
    forbidden_claims: Iterable[str],
    checked_fields: Iterable[str],
    excluded_fields: Iterable[str],
    scope: str = "capability-report-envelope",
    content_coverage: str = "report sections and metadata summary only",
    policy_source: str = "risk.forbiddenClaims",
    allowed_context_prefixes: Iterable[str] = (),
) -> dict[str, Any]:
    """Build a minimal report policy gate result.

    The scanner intentionally checks caller-selected generated content only. It
    must not scan the forbidden-claims list itself, otherwise every capability
    would fail merely because the policy is present in the response.
    """

    normalized_claims = _normalize_claims(forbidden_claims)
    normalized_checked_fields = _normalize_fields(checked_fields)
    normalized_excluded_fields = _normalize_fields(excluded_fields)
    normalized_allowed_context_prefixes = _normalize_fields(allowed_context_prefixes)
    matches = _scan_forbidden_claims(
        content,
        normalized_claims,
        excluded_fields=normalized_excluded_fields,
        root_path="report",
        allowed_context_prefixes=normalized_allowed_context_prefixes,
    )
    return {
        "version": POLICY_GATE_VERSION,
        "status": "fail" if matches else "pass",
        "engine": POLICY_MATCH_ENGINE,
        "scope": scope,
        "contentCoverage": content_coverage,
        "checkedFields": normalized_checked_fields,
        "excludedFields": normalized_excluded_fields,
        "policySource": policy_source,
        "forbiddenClaimsCount": len(normalized_claims),
        "checkedTextCount": sum(1 for _path, _text in _iter_text_items(content, "report", normalized_excluded_fields)),
        "matches": matches,
    }


def build_markdown_report_policy_gate(
    *,
    markdown: str,
    forbidden_claims: Iterable[str],
    report_system: str,
) -> dict[str, Any]:
    """Build a policy gate for user-visible Markdown report content."""

    return build_report_policy_gate(
        content={"markdown": markdown},
        forbidden_claims=forbidden_claims,
        checked_fields=["report.markdown"],
        excluded_fields=[
            "report.risk.forbiddenClaims",
            "risk.forbiddenClaims",
            "report.policyGate",
            "report.snapshotGate",
        ],
        scope=f"markdown-report:{report_system}",
        content_coverage="用户可见 Markdown 正文。",
        policy_source="capability.riskPolicy.forbiddenClaims",
        allowed_context_prefixes=[
            "不输出",
            "不承诺",
            "不代表",
            "不替代",
            "不能替代",
            "不得替代",
            "不得作为",
            "避免",
            "禁止",
        ],
    )


def build_markdown_snapshot_gate(*, markdown: str, report_system: str) -> dict[str, Any]:
    """Build a lightweight structure snapshot gate from Markdown headings."""

    headings = _extract_markdown_headings(markdown)
    heading_texts = [item["text"] for item in headings]
    required = list(_REQUIRED_MARKDOWN_HEADINGS.get(report_system, ()))
    missing = [item for item in required if not _heading_present(item, heading_texts)]
    return {
        "version": SNAPSHOT_GATE_VERSION,
        "status": "fail" if missing else "pass",
        "scope": f"markdown-report:{report_system}",
        "contentCoverage": "Markdown heading structure only; full body snapshot diff belongs to a later gate.",
        "reportSystem": report_system,
        "requiredHeadings": required,
        "missingHeadings": missing,
        "headingCount": len(headings),
        "headings": headings,
    }


def _normalize_claims(claims: Iterable[str]) -> list[str]:
    normalized: list[str] = []
    seen: set[str] = set()
    for item in claims:
        claim = str(item).strip()
        if not claim or claim in seen:
            continue
        seen.add(claim)
        normalized.append(claim)
    return normalized


def _normalize_fields(fields: Iterable[str]) -> list[str]:
    normalized: list[str] = []
    seen: set[str] = set()
    for item in fields:
        field = str(item).strip()
        if not field or field in seen:
            continue
        seen.add(field)
        normalized.append(field)
    return normalized


def _extract_markdown_headings(markdown: str) -> list[dict[str, Any]]:
    headings: list[dict[str, Any]] = []
    for line_number, raw_line in enumerate(markdown.splitlines(), start=1):
        stripped = raw_line.strip()
        if not stripped.startswith("#"):
            continue
        marker, _sep, title = stripped.partition(" ")
        if not marker or any(char != "#" for char in marker):
            continue
        level = len(marker)
        if level > 6 or not title.strip():
            continue
        headings.append(
            {
                "level": level,
                "text": f"{marker} {title.strip()}",
                "title": title.strip(),
                "line": line_number,
            }
        )
    return headings


def _heading_present(required: str, headings: list[str]) -> bool:
    if required.endswith("："):
        return any(heading.startswith(required) for heading in headings)
    return required in headings


def _scan_forbidden_claims(
    content: Any,
    forbidden_claims: list[str],
    *,
    excluded_fields: list[str],
    root_path: str,
    allowed_context_prefixes: list[str],
) -> list[dict[str, Any]]:
    matches: list[dict[str, Any]] = []
    for path, text in _iter_text_items(content, root_path, excluded_fields):
        for claim in forbidden_claims:
            start = 0
            while True:
                index = text.find(claim, start)
                if index < 0:
                    break
                start = index + len(claim)
                if _has_allowed_context_prefix(text, index, allowed_context_prefixes):
                    continue
                matches.append(
                    {
                        "claim": claim,
                        "path": path,
                        "excerpt": _excerpt(text, claim),
                    }
                )
    return matches


def _has_allowed_context_prefix(text: str, claim_index: int, prefixes: list[str]) -> bool:
    if not prefixes:
        return False
    start = max(0, claim_index - 12)
    prefix_window = text[start:claim_index]
    return any(prefix_window.endswith(prefix) for prefix in prefixes)


def _iter_text_items(content: Any, path: str, excluded_fields: list[str]) -> Iterable[tuple[str, str]]:
    if _is_excluded(path, excluded_fields):
        return

    if isinstance(content, str):
        if content:
            yield path, content
        return

    if isinstance(content, Mapping):
        for key, value in content.items():
            child_path = f"{path}.{key}"
            yield from _iter_text_items(value, child_path, excluded_fields)
        return

    if isinstance(content, (list, tuple)):
        for index, value in enumerate(content):
            child_path = f"{path}[{index}]"
            yield from _iter_text_items(value, child_path, excluded_fields)


def _is_excluded(path: str, excluded_fields: list[str]) -> bool:
    for field in excluded_fields:
        if path == field or path.startswith(f"{field}.") or path.startswith(f"{field}["):
            return True
    return False


def _excerpt(text: str, claim: str, *, radius: int = 18) -> str:
    index = text.find(claim)
    if index < 0:
        return text[: radius * 2]
    start = max(0, index - radius)
    end = min(len(text), index + len(claim) + radius)
    prefix = "..." if start > 0 else ""
    suffix = "..." if end < len(text) else ""
    return f"{prefix}{text[start:end]}{suffix}"
