"""公开 Markdown 投影契约校验。

领域结果保留完整证据；本模块只验证用户可见报告是否落在 profile 明确允许的结构内。
"""

from __future__ import annotations

import json
import re
from functools import cache
from typing import Any

from fate_core.support.paths import FATE_CAPABILITY_DIR


class PublicReportContractError(ValueError):
    """公开报告超出 profile 允许边界。"""


_TABLE_SEPARATOR_CELL = re.compile(r"^:?-{2,}:?$")


def _string_tuple(value: Any, field: str, report_system: str) -> tuple[str, ...]:
    if not isinstance(value, list) or not value:
        raise PublicReportContractError(f"{report_system}.publicMarkdown.{field} 必须是非空数组")
    items = tuple(str(item).strip() for item in value)
    if any(not item for item in items):
        raise PublicReportContractError(f"{report_system}.publicMarkdown.{field} 不能包含空值")
    return items


@cache
def load_public_markdown_contract(report_system: str) -> dict[str, tuple[Any, ...]]:
    """加载并规范化 capability profile 的公开 Markdown 契约。"""
    normalized = str(report_system).strip().lower()
    profile_path = FATE_CAPABILITY_DIR / "profiles" / f"{normalized}.json"
    try:
        payload = json.loads(profile_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise PublicReportContractError(f"无法加载公开报告 profile: {normalized}") from exc

    public_markdown = payload.get("publicMarkdown")
    if not isinstance(public_markdown, dict):
        raise PublicReportContractError(f"{normalized}.publicMarkdown 缺失")

    headers = public_markdown.get("allowedTableHeaders")
    if not isinstance(headers, list) or not headers:
        raise PublicReportContractError(f"{normalized}.publicMarkdown.allowedTableHeaders 必须是非空数组")
    normalized_headers: list[tuple[str, ...]] = []
    for header in headers:
        if not isinstance(header, list) or not header:
            raise PublicReportContractError(f"{normalized}.publicMarkdown.allowedTableHeaders 存在非法表头")
        cells = tuple(str(cell).strip() for cell in header)
        if any(not cell for cell in cells):
            raise PublicReportContractError(f"{normalized}.publicMarkdown.allowedTableHeaders 不能包含空值")
        normalized_headers.append(cells)

    return {
        "headingPrefixes": _string_tuple(public_markdown.get("headingPrefixes"), "headingPrefixes", normalized),
        "allowedHeadings": _string_tuple(public_markdown.get("allowedHeadings"), "allowedHeadings", normalized),
        "allowedTableHeaders": tuple(normalized_headers),
        "allowedMetadataLabels": _string_tuple(
            public_markdown.get("allowedMetadataLabels"), "allowedMetadataLabels", normalized
        ),
        "machineOnlyResultPaths": _string_tuple(
            public_markdown.get("machineOnlyResultPaths"), "machineOnlyResultPaths", normalized
        ),
        "forbiddenRenderedTerms": _string_tuple(
            public_markdown.get("forbiddenRenderedTerms"), "forbiddenRenderedTerms", normalized
        ),
    }


def _table_cells(line: str) -> tuple[str, ...]:
    return tuple(cell.strip() for cell in line.strip().strip("|").split("|"))


def _is_table_separator(line: str) -> bool:
    if not line.startswith("|"):
        return False
    cells = _table_cells(line)
    return bool(cells) and all(_TABLE_SEPARATOR_CELL.fullmatch(cell) for cell in cells)


def validate_public_markdown(markdown: str, report_system: str) -> str:
    """按 profile 白名单验证公开 Markdown，并原样返回正文。"""
    contract = load_public_markdown_contract(report_system)
    allowed_headings = set(contract["allowedHeadings"])
    heading_prefixes = contract["headingPrefixes"]
    allowed_table_headers = set(contract["allowedTableHeaders"])
    allowed_metadata_labels = set(contract["allowedMetadataLabels"])
    lines = markdown.splitlines()
    violations: list[str] = []

    for line in lines:
        if not line.startswith("#"):
            continue
        if line in allowed_headings or any(line.startswith(prefix) for prefix in heading_prefixes):
            continue
        violations.append(f"未允许标题: {line}")

    for index, line in enumerate(lines):
        if not line.startswith("|") or index + 1 >= len(lines) or not _is_table_separator(lines[index + 1]):
            continue
        header = _table_cells(line)
        if header not in allowed_table_headers:
            violations.append(f"未允许表头: {' / '.join(header)}")
            continue
        if header != ("项目", "内容"):
            continue
        row_index = index + 2
        while row_index < len(lines) and lines[row_index].startswith("|"):
            row = _table_cells(lines[row_index])
            if row and row[0] not in allowed_metadata_labels:
                violations.append(f"未允许元数据标签: {row[0]}")
            row_index += 1

    for term in contract["forbiddenRenderedTerms"]:
        if term in markdown:
            violations.append(f"机器字段进入公开报告: {term}")

    if violations:
        detail = "；".join(dict.fromkeys(violations))
        raise PublicReportContractError(f"{report_system} 公开 Markdown 契约失败: {detail}")
    return markdown


__all__ = ["PublicReportContractError", "load_public_markdown_contract", "validate_public_markdown"]
