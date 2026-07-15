from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import Any

# Ponytail existence: report policy gate is the smallest auditable guard between
# generated report summaries and capability risk policy. It deliberately stays
# dependency-free; richer NLP/snapshot gates belong to later infrastructure slices.
# Owner: tradecatlabs/fate-core. Verification: test_capability_protocol.py.

POLICY_GATE_VERSION = "report-policy-gate-v1"
POLICY_MATCH_ENGINE = "literal-substring-v1"
SNAPSHOT_GATE_VERSION = "markdown-snapshot-gate-v2"

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

_EXPECTED_MARKDOWN_OUTLINES: dict[str, tuple[str, ...]] = {
    "bazi": (
        "# 命理排盘报告：",
        "## 第一卷：先天命格（静态分析）",
        "### 基本资料（含真太阳时、节气）",
        "#### 基本资料",
        "#### 空亡信息（依据）",
        "### 八字排盘详情",
        "### 神煞断语",
        "### 日主概览",
        "### 五行喜忌（调候与平衡）",
        "#### 五行比例",
        "#### 五行分数",
        "#### 天干分数",
        "### 五行停匀与寒湿燥热（调候依据）",
        "### 干支取象（原文）",
        "### 命造格局（格局用神）",
        "### 节气司令",
        "### 干支关系",
        "#### 天干关系",
        "#### 干支相合（依据）",
        "#### 天干相克（依据）",
        "#### 地支入库（依据）",
        "#### 地支关系",
        "## 第二卷：后天运路（动态趋势）",
        "### 运势分析",
        "#### 大运分析",
        "#### 流年",
        "#### 近期流年指引（近",
        "#### 流月运势",
        "#### 近期流月指引（近",
        "#### 小运",
        "## 第三卷：民俗与建议（生活应用）",
        "### 袁天罡称骨",
    ),
    "ziwei": (
        "# 紫微斗数报告：",
        "## 紫微斗数",
        "### 入盘依据",
        "### 命宫与身宫",
        "### 十二宫",
        "## 紫微结构解读（依据版）",
        "### 命宫/身宫断语",
        "### 主星组合",
        "### 三方四正",
        "### 四化落宫",
        "### 大限/流年联动",
        "## 紫微运限四化（大限/流年/流月/流日/流时）",
        "### 大限",
        "### 流年",
        "### 流月",
        "### 流日",
        "### 流时",
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
    """Build a structure gate from Markdown headings."""

    headings = _extract_markdown_headings(markdown)
    heading_texts = [item["text"] for item in headings]
    required = list(_REQUIRED_MARKDOWN_HEADINGS.get(report_system, ()))
    missing = [item for item in required if not _heading_present(item, heading_texts)]
    structure_violations = _validate_markdown_heading_structure(headings, report_system)
    return {
        "version": SNAPSHOT_GATE_VERSION,
        "status": "fail" if missing or structure_violations else "pass",
        "scope": f"markdown-report:{report_system}",
        "contentCoverage": (
            "Markdown heading structure only: required headings, one H1, first-heading level, "
            "level increments, known-heading levels and canonical order; full body snapshot diff belongs to a later gate."
        ),
        "reportSystem": report_system,
        "requiredHeadings": required,
        "missingHeadings": missing,
        "structureViolations": structure_violations,
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


def _validate_markdown_heading_structure(
    headings: list[dict[str, Any]],
    report_system: str,
) -> list[dict[str, Any]]:
    violations: list[dict[str, Any]] = []
    if not headings:
        return violations

    first = headings[0]
    if first["level"] != 1:
        violations.append(
            {
                "code": "first_heading_not_h1",
                "line": first["line"],
                "actualLevel": first["level"],
                "title": first["title"],
            }
        )

    h1_headings = [item for item in headings if item["level"] == 1]
    if len(h1_headings) != 1:
        violations.append(
            {
                "code": "invalid_h1_count",
                "expectedCount": 1,
                "actualCount": len(h1_headings),
                "lines": [item["line"] for item in h1_headings],
            }
        )

    seen: dict[str, int] = {}
    previous = headings[0]
    for item in headings:
        text = item["text"]
        if text in seen:
            violations.append(
                {
                    "code": "duplicate_heading",
                    "title": item["title"],
                    "firstLine": seen[text],
                    "line": item["line"],
                }
            )
        else:
            seen[text] = item["line"]

        if item is not previous and item["level"] > previous["level"] + 1:
            violations.append(
                {
                    "code": "heading_level_skip",
                    "line": item["line"],
                    "previousLevel": previous["level"],
                    "actualLevel": item["level"],
                    "title": item["title"],
                }
            )
        previous = item

    outline = _EXPECTED_MARKDOWN_OUTLINES.get(report_system, ())
    expected_positions: list[int] = []
    for item in headings:
        matching_index = _matching_outline_index(item["title"], outline)
        if matching_index is None:
            continue
        expected_positions.append(matching_index)
        expected_level, _title = _split_heading_spec(outline[matching_index])
        if item["level"] != expected_level:
            violations.append(
                {
                    "code": "unexpected_heading_level",
                    "line": item["line"],
                    "title": item["title"],
                    "expectedLevel": expected_level,
                    "actualLevel": item["level"],
                }
            )

    if expected_positions != sorted(expected_positions):
        violations.append(
            {
                "code": "unexpected_heading_order",
                "expectedOrder": list(outline),
                "actualOrder": [item["text"] for item in headings],
            }
        )
    return violations


def _matching_outline_index(title: str, outline: tuple[str, ...]) -> int | None:
    for index, specification in enumerate(outline):
        _level, expected_title = _split_heading_spec(specification)
        if expected_title.endswith(("：", "（近")):
            if title.startswith(expected_title):
                return index
        elif title == expected_title:
            return index
    return None


def _split_heading_spec(specification: str) -> tuple[int, str]:
    marker, separator, title = specification.partition(" ")
    if not separator or not marker or any(char != "#" for char in marker):
        raise ValueError(f"invalid Markdown heading specification: {specification}")
    return len(marker), title


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
