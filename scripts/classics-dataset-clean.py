#!/usr/bin/env python3
"""将 canonical 命理典籍确定性清洗为内部可追溯数据集。"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import shutil
import tempfile
import unicodedata
from collections import defaultdict
from collections.abc import Iterable, Sequence
from pathlib import Path
from typing import Any, Final

REPO_ROOT: Final = Path(__file__).resolve().parents[1]
DEFAULT_INPUT: Final = REPO_ROOT / "domains" / "fate-analysis" / "data-products" / "classics"
DEFAULT_OUTPUT: Final = REPO_ROOT / "infra" / "runtime" / "local-state" / "exports" / "datasets" / "classics-clean-v2"
DEFAULT_CONTRACT: Final = (
    REPO_ROOT / "contracts" / "fate" / "data-supply-chain" / "schemas" / "classics-clean-dataset.schema.json"
)
DEFAULT_CURATION_POLICY: Final = DEFAULT_INPUT / "curation_policy.json"
SCHEMA_VERSION: Final = "classics-clean-dataset.v2"
NORMALIZATION_PROFILE: Final = "classics-clean-v2"
BUILDER_PATH: Final = "scripts/classics-dataset-clean.py"
SOURCE_MANIFEST_NAME: Final = "source_manifest.tsv"
COPYRIGHT_REVIEW_NAME: Final = "copyright_review.tsv"
REMOVE_CHARACTERS: Final = frozenset({"\ufeff", "\u200b", "\u200c", "\u200d", "\u2060"})
SENTENCE_ENDINGS: Final = frozenset("。！？；：.!?;")
HEADING_PATTERN: Final = re.compile(
    r"^(?:"
    r"#{1,6}\s*.+|"
    r"第?[一二三四五六七八九十百千万零〇两0-9]+[卷章节篇部集回](?:\s*.+)?|"
    r"[卷章节篇部集][一二三四五六七八九十百千万零〇两0-9]+(?:\s*.+)?|"
    r"(?:序|序言|自序|凡例|目录|总目录|总论|提要|跋|后序|附录)|"
    r"(?:论|释|解)[^，。！？；]{1,24}"
    r")[：:]?$"
)
OUTPUT_DATA_FILES: Final = (
    "documents.ndjson",
    "paragraphs.ndjson",
    "passages.ndjson",
    "duplicates.ndjson",
    "exclusions.ndjson",
    "review-queue.ndjson",
    "quality-report.json",
)
ALLOWED_DOCUMENT_ROLES: Final = frozenset(
    {
        "source_text",
        "source_with_commentary",
        "commentary",
        "annotated_source",
        "treatise",
        "compendium",
        "mixed_notes",
    }
)
ALLOWED_COMPLETENESS_STATUS: Final = frozenset({"partial", "unknown"})
ALLOWED_REVIEW_SEVERITY: Final = frozenset({"high", "medium", "low"})


class ClassicsDatasetError(RuntimeError):
    """典籍数据集不满足清洗或验证契约。"""


def _json_dumps(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _sha256_text(value: str) -> str:
    return _sha256_bytes(value.encode("utf-8"))


def _sha256_file(path: Path) -> str:
    return _sha256_bytes(path.read_bytes())


def _load_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ClassicsDatasetError(f"无法读取 JSON：{path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise ClassicsDatasetError(f"JSON 根节点必须是对象：{path}")
    return payload


def _read_tsv(path: Path, required_columns: Sequence[str]) -> list[dict[str, str]]:
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle, delimiter="\t")
            columns = set(reader.fieldnames or ())
            missing = sorted(set(required_columns) - columns)
            if missing:
                raise ClassicsDatasetError(f"TSV 缺少字段 {missing}：{path}")
            return [dict(row) for row in reader]
    except (OSError, UnicodeDecodeError, csv.Error) as exc:
        raise ClassicsDatasetError(f"无法读取 TSV：{path}: {exc}") from exc


def _assert_unique(rows: Sequence[dict[str, str]], key: str, source: Path) -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    for row in rows:
        value = row.get(key, "")
        if not value:
            raise ClassicsDatasetError(f"TSV 字段 {key} 不能为空：{source}")
        if value in result:
            raise ClassicsDatasetError(f"TSV 字段 {key} 重复：{value}: {source}")
        result[value] = row
    return result


def _load_curation_policy(path: Path, source_paths: set[str]) -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    policy = _load_json(path)
    required_policy_fields = {"schemaVersion", "policyId", "description", "ruleSets", "documents", "invariants"}
    missing_policy_fields = sorted(required_policy_fields - set(policy))
    if missing_policy_fields:
        raise ClassicsDatasetError(f"curation policy 缺少字段：{missing_policy_fields}")
    if not isinstance(policy["ruleSets"], dict) or not isinstance(policy["documents"], list):
        raise ClassicsDatasetError("curation policy 的 ruleSets/documents 类型错误")

    required_document_fields = {
        "sourcePath",
        "sourceSha256",
        "familyId",
        "documentRole",
        "roleStatus",
        "bibliography",
        "completeness",
        "selection",
        "reviewItems",
    }
    documents: dict[str, dict[str, Any]] = {}
    for document in policy["documents"]:
        if not isinstance(document, dict):
            raise ClassicsDatasetError("curation policy document 必须是对象")
        missing = sorted(required_document_fields - set(document))
        if missing:
            raise ClassicsDatasetError(f"curation policy document 缺少字段 {missing}")
        source_path = str(document["sourcePath"])
        if source_path in documents:
            raise ClassicsDatasetError(f"curation policy sourcePath 重复：{source_path}")
        if document["documentRole"] not in ALLOWED_DOCUMENT_ROLES or document["roleStatus"] != "curator_assigned":
            raise ClassicsDatasetError(f"curation policy 文本角色非法：{source_path}")
        bibliography = document["bibliography"]
        if (
            not isinstance(bibliography, dict)
            or bibliography.get("reviewed") is not None
            or bibliography.get("reviewStatus") != "review_required"
        ):
            raise ClassicsDatasetError(f"curation policy 书目复核边界非法：{source_path}")
        completeness = document["completeness"]
        if not isinstance(completeness, dict) or completeness.get("status") not in ALLOWED_COMPLETENESS_STATUS:
            raise ClassicsDatasetError(f"curation policy 完整性状态非法：{source_path}")
        _validate_selection_policy(document, policy)
        review_ids: set[str] = set()
        for item in document["reviewItems"]:
            if not isinstance(item, dict):
                raise ClassicsDatasetError(f"curation review item 必须是对象：{source_path}")
            required_review = {"id", "issueType", "severity", "summary", "evidence", "blocks"}
            if required_review - set(item) or item["severity"] not in ALLOWED_REVIEW_SEVERITY:
                raise ClassicsDatasetError(f"curation review item 字段或 severity 非法：{source_path}")
            item_id = str(item["id"])
            if item_id in review_ids:
                raise ClassicsDatasetError(f"curation review item id 重复：{source_path}: {item_id}")
            review_ids.add(item_id)
        documents[source_path] = document

    if set(documents) != source_paths:
        missing = sorted(source_paths - set(documents))
        extra = sorted(set(documents) - source_paths)
        raise ClassicsDatasetError(f"curation policy 覆盖错误：missing={missing} extra={extra}")
    return policy, documents


def _validate_selection_policy(document: dict[str, Any], policy: dict[str, Any]) -> None:
    source_path = str(document["sourcePath"])
    selection = document["selection"]
    if not isinstance(selection, dict):
        raise ClassicsDatasetError(f"curation selection 必须是对象：{source_path}")
    required = {"mode", "includeLineRanges", "ruleSetRefs", "lineRules"}
    if required - set(selection) or selection["mode"] not in {"all", "include_line_ranges"}:
        raise ClassicsDatasetError(f"curation selection 字段或 mode 非法：{source_path}")
    ranges = selection["includeLineRanges"]
    if selection["mode"] == "include_line_ranges" and not ranges:
        raise ClassicsDatasetError(f"include_line_ranges 缺少范围：{source_path}")
    if selection["mode"] == "all" and ranges:
        raise ClassicsDatasetError(f"mode=all 不得声明 includeLineRanges：{source_path}")
    previous_end = 0
    for item in ranges:
        if (
            not isinstance(item, list)
            or len(item) != 2
            or not all(isinstance(value, int) for value in item)
            or item[0] < 1
            or item[0] > item[1]
            or item[0] <= previous_end
        ):
            raise ClassicsDatasetError(f"includeLineRanges 非升序闭区间：{source_path}: {item}")
        previous_end = item[1]
    for reference in selection["ruleSetRefs"]:
        if reference not in policy["ruleSets"]:
            raise ClassicsDatasetError(f"curation ruleSetRef 不存在：{source_path}: {reference}")
    rule_ids: set[str] = set()
    for rule in _resolved_selection_rules(document, policy):
        required_rule = {"id", "action", "match", "classification", "reason"}
        if required_rule - set(rule):
            raise ClassicsDatasetError(f"curation rule 缺少字段：{source_path}: {rule}")
        rule_id = str(rule["id"])
        if rule_id in rule_ids:
            raise ClassicsDatasetError(f"curation rule id 重复：{source_path}: {rule_id}")
        rule_ids.add(rule_id)
        match = rule["match"]
        if (
            rule["action"] not in {"exclude", "extract_and_exclude"}
            or not isinstance(match, dict)
            or match.get("type") not in {"exact", "prefix"}
            or not isinstance(match.get("value"), str)
            or not match["value"]
        ):
            raise ClassicsDatasetError(f"curation rule action/match 非法：{source_path}: {rule_id}")
        if rule["action"] == "extract_and_exclude" and (
            not rule.get("target") or rule.get("extractMode") not in {"suffix", "after_label"}
        ):
            raise ClassicsDatasetError(f"extract_and_exclude 缺少 target/extractMode：{source_path}: {rule_id}")


def _resolved_selection_rules(document: dict[str, Any], policy: dict[str, Any]) -> list[dict[str, Any]]:
    selection = document["selection"]
    rules: list[dict[str, Any]] = []
    for reference in selection.get("ruleSetRefs", []):
        rule_set = policy["ruleSets"].get(reference)
        if not isinstance(rule_set, list):
            raise ClassicsDatasetError(f"curation rule set 类型错误：{reference}")
        rules.extend(rule_set)
    line_rules = selection.get("lineRules", [])
    if not isinstance(line_rules, list):
        raise ClassicsDatasetError(f"curation lineRules 类型错误：{document['sourcePath']}")
    rules.extend(line_rules)
    return rules


def _line_in_ranges(line_number: int, ranges: Sequence[Sequence[int]]) -> bool:
    return any(int(start) <= line_number <= int(end) for start, end in ranges)


def _matching_rule(text: str, rules: Sequence[dict[str, Any]]) -> dict[str, Any] | None:
    matches: list[dict[str, Any]] = []
    for rule in rules:
        match = rule["match"]
        if match["type"] == "exact" and text == match["value"]:
            matches.append(rule)
        elif match["type"] == "prefix" and text.startswith(match["value"]):
            matches.append(rule)
    if len(matches) > 1:
        raise ClassicsDatasetError(f"同一源行命中多个 curation rule：{[item['id'] for item in matches]}")
    return matches[0] if matches else None


def _store_extracted_metadata(metadata: dict[str, Any], target: str, value: str) -> None:
    if target == "chapterSourceUrls":
        metadata.setdefault(target, []).append(value)
        return
    if target not in metadata:
        metadata[target] = value
        return
    current = metadata[target]
    if not isinstance(current, list):
        current = [current]
        metadata[target] = current
    current.append(value)


def _apply_curation_policy(
    *,
    raw_lines: Sequence[str],
    document_id: str,
    source_path: str,
    source_sha256: str,
    document_policy: dict[str, Any],
    policy: dict[str, Any],
) -> tuple[list[tuple[int, str]], list[dict[str, Any]], dict[str, Any]]:
    selection = document_policy["selection"]
    ranges = selection["includeLineRanges"]
    if ranges and int(ranges[-1][1]) > len(raw_lines):
        raise ClassicsDatasetError(f"curation includeLineRanges 越界：{source_path}: {ranges[-1][1]}>{len(raw_lines)}")
    rules = _resolved_selection_rules(document_policy, policy)
    selected: list[tuple[int, str]] = []
    exclusions: list[dict[str, Any]] = []
    metadata: dict[str, Any] = {}

    for line_number, raw_line in enumerate(raw_lines, start=1):
        normalized_line = _normalize_line(raw_line)
        exclusion_rule: dict[str, Any] | None = None
        if selection["mode"] == "include_line_ranges" and not _line_in_ranges(line_number, ranges):
            exclusion_rule = {
                "id": "include-line-ranges-boundary",
                "classification": "non_content_wrapper",
                "reason": "该源行位于人工审定正文范围之外。",
                "action": "exclude",
            }
        elif normalized_line:
            exclusion_rule = _matching_rule(normalized_line, rules)

        if exclusion_rule is None:
            selected.append((line_number, raw_line))
            continue
        if not normalized_line:
            continue
        if exclusion_rule["action"] == "extract_and_exclude":
            prefix = str(exclusion_rule["match"]["value"])
            if exclusion_rule["extractMode"] == "after_label":
                if "：" not in normalized_line:
                    raise ClassicsDatasetError(f"after_label 规则未命中中文标签分隔符：{source_path}:{line_number}")
                extracted_value = normalized_line.split("：", 1)[1].strip()
            else:
                extracted_value = normalized_line[len(prefix) :].strip()
            _store_extracted_metadata(metadata, str(exclusion_rule["target"]), extracted_value)
        exclusions.append(
            {
                "schemaVersion": SCHEMA_VERSION,
                "kind": "excluded_source_line",
                "exclusionId": f"{document_id}:x{len(exclusions) + 1:06d}",
                "documentId": document_id,
                "sourcePath": source_path,
                "sourceSha256": source_sha256,
                "sourceLine": line_number,
                "textSha256": _sha256_text(raw_line),
                "charCount": len(raw_line),
                "ruleId": str(exclusion_rule["id"]),
                "classification": str(exclusion_rule["classification"]),
                "reason": str(exclusion_rule["reason"]),
            }
        )
    return selected, exclusions, metadata


def _is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
    except ValueError:
        return False
    return True


def _manifest_path(path: Path) -> str:
    resolved = path.resolve()
    try:
        return str(resolved.relative_to(REPO_ROOT))
    except ValueError:
        return f"external:{resolved.name}"


def _validate_path_boundary(input_dir: Path, output_dir: Path) -> tuple[Path, Path]:
    source = input_dir.resolve()
    target = output_dir.resolve()
    if source == target or _is_relative_to(target, source) or _is_relative_to(source, target):
        raise ClassicsDatasetError("输入目录与输出目录不得相同或互相包含")
    return source, target


def _reject_forbidden_characters(text: str, path: Path) -> None:
    for index, character in enumerate(text):
        if character in "\t\n\r" or character in REMOVE_CHARACTERS:
            continue
        if character == "\x00" or unicodedata.category(character) == "Cc":
            codepoint = f"U+{ord(character):04X}"
            raise ClassicsDatasetError(f"发现禁止控制字符 {codepoint}：{path} 字符偏移 {index}")


def _semantic_fingerprint(text: str) -> str:
    normalized = unicodedata.normalize("NFC", text)
    normalized = "".join(character for character in normalized if character not in REMOVE_CHARACTERS)
    normalized = normalized.replace("\u00a0", " ")
    return "".join(character for character in normalized if not character.isspace())


def _normalize_line(line: str) -> str:
    value = unicodedata.normalize("NFC", line)
    value = "".join(character for character in value if character not in REMOVE_CHARACTERS)
    value = value.replace("\u00a0", " ")
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def _parse_title_author(filename: str) -> tuple[str, str | None]:
    stem = Path(filename).stem
    if " - " not in stem:
        return stem, None
    title, author = stem.rsplit(" - ", 1)
    return title.strip(), author.strip() or None


def _document_id(source_path: str) -> str:
    return f"doc-{_sha256_text(source_path)[:20]}"


def _is_heading(text: str) -> bool:
    return len(text) <= 48 and bool(HEADING_PATTERN.fullmatch(text))


def _heading_text(text: str) -> str:
    return re.sub(r"^#{1,6}\s*", "", text).rstrip("：:").strip()


def _split_oversized_text(text: str, max_chars: int) -> list[str]:
    if len(text) <= max_chars:
        return [text]
    chunks: list[str] = []
    remaining = text
    while len(remaining) > max_chars:
        lower_bound = max_chars // 2
        boundary = max(
            (index + 1 for index, character in enumerate(remaining[:max_chars]) if character in SENTENCE_ENDINGS),
            default=0,
        )
        cut = boundary if boundary >= lower_bound else max_chars
        chunk = remaining[:cut].strip()
        if not chunk:
            chunk = remaining[:max_chars]
            cut = max_chars
        chunks.append(chunk)
        remaining = remaining[cut:].strip()
    if remaining:
        chunks.append(remaining)
    if _semantic_fingerprint("".join(chunks)) != _semantic_fingerprint(text):
        raise ClassicsDatasetError("超长段落切分发生内容丢失")
    return chunks


def _write_ndjson(path: Path, records: Iterable[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for record in records:
            handle.write(_json_dumps(record))
            handle.write("\n")


def _read_ndjson(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    try:
        with path.open("r", encoding="utf-8") as handle:
            for line_number, line in enumerate(handle, start=1):
                if not line.strip():
                    continue
                value = json.loads(line)
                if not isinstance(value, dict):
                    raise ClassicsDatasetError(f"NDJSON 记录必须是对象：{path}:{line_number}")
                records.append(value)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ClassicsDatasetError(f"无法读取 NDJSON：{path}: {exc}") from exc
    return records


def _build_passages(
    *,
    document_id: str,
    paragraphs: Sequence[dict[str, Any]],
    source_path: str,
    source_sha256: str,
    rights: dict[str, str],
    max_chars: int,
) -> list[dict[str, Any]]:
    fragments: list[dict[str, Any]] = []
    for paragraph in paragraphs:
        for text in _split_oversized_text(str(paragraph["text"]), max_chars):
            fragments.append({"paragraph": paragraph, "text": text})

    passages: list[dict[str, Any]] = []
    current: list[dict[str, Any]] = []
    current_chars = 0

    def flush() -> None:
        nonlocal current, current_chars
        if not current:
            return
        text = "\n".join(str(fragment["text"]) for fragment in current)
        paragraph_ids = list(dict.fromkeys(str(fragment["paragraph"]["paragraphId"]) for fragment in current))
        paragraph_sequences = [int(fragment["paragraph"]["sequence"]) for fragment in current]
        source_lines = [int(fragment["paragraph"]["sourceLineStart"]) for fragment in current]
        heading_path = next(
            (
                list(fragment["paragraph"]["headingPath"])
                for fragment in current
                if fragment["paragraph"]["headingPath"]
            ),
            [],
        )
        sequence = len(passages) + 1
        passages.append(
            {
                "schemaVersion": SCHEMA_VERSION,
                "kind": "passage",
                "passageId": f"{document_id}:s{sequence:06d}",
                "documentId": document_id,
                "sequence": sequence,
                "paragraphIds": paragraph_ids,
                "paragraphStart": min(paragraph_sequences),
                "paragraphEnd": max(paragraph_sequences),
                "sourceLineStart": min(source_lines),
                "sourceLineEnd": max(int(fragment["paragraph"]["sourceLineEnd"]) for fragment in current),
                "headingPath": heading_path,
                "text": text,
                "textSha256": _sha256_text(text),
                "charCount": len(text),
                "sourcePath": source_path,
                "sourceSha256": source_sha256,
                "rightsStatus": rights["status"],
                "allowedUse": rights["allowed_use"],
                "releasePolicy": rights["release_policy"],
                "distributionAllowed": False,
                "productionUseAllowed": False,
                "trainingUseAllowed": False,
            }
        )
        current = []
        current_chars = 0

    for fragment in fragments:
        extra = len(str(fragment["text"])) + (1 if current else 0)
        if current and current_chars + extra > max_chars:
            flush()
        current.append(fragment)
        current_chars += len(str(fragment["text"])) + (1 if len(current) > 1 else 0)
    flush()
    return passages


def _duplicate_records(
    paragraphs: Sequence[dict[str, Any]], passages: Sequence[dict[str, Any]]
) -> tuple[list[dict[str, Any]], dict[str, int]]:
    paragraph_groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    passage_groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    document_hashes: dict[str, set[str]] = defaultdict(set)

    for paragraph in paragraphs:
        if int(paragraph["charCount"]) >= 12:
            text_hash = str(paragraph["textSha256"])
            paragraph_groups[text_hash].append(paragraph)
            document_hashes[str(paragraph["documentId"])].add(text_hash)
    for passage in passages:
        passage_groups[str(passage["textSha256"])].append(passage)

    records: list[dict[str, Any]] = []
    for text_hash, group in sorted(paragraph_groups.items()):
        if len(group) < 2:
            continue
        records.append(
            {
                "schemaVersion": SCHEMA_VERSION,
                "kind": "exact_paragraph_group",
                "textSha256": text_hash,
                "occurrenceCount": len(group),
                "paragraphIds": sorted(str(item["paragraphId"]) for item in group),
                "documentIds": sorted({str(item["documentId"]) for item in group}),
                "action": "retain_and_review",
            }
        )
    for text_hash, group in sorted(passage_groups.items()):
        if len(group) < 2:
            continue
        records.append(
            {
                "schemaVersion": SCHEMA_VERSION,
                "kind": "exact_passage_group",
                "textSha256": text_hash,
                "occurrenceCount": len(group),
                "passageIds": sorted(str(item["passageId"]) for item in group),
                "documentIds": sorted({str(item["documentId"]) for item in group}),
                "action": "retain_and_review",
            }
        )

    document_ids = sorted(document_hashes)
    overlap_count = 0
    for left_index, left_id in enumerate(document_ids):
        for right_id in document_ids[left_index + 1 :]:
            left_hashes = document_hashes[left_id]
            right_hashes = document_hashes[right_id]
            shared = left_hashes & right_hashes
            if not shared:
                continue
            overlap_count += 1
            denominator = min(len(left_hashes), len(right_hashes)) or 1
            records.append(
                {
                    "schemaVersion": SCHEMA_VERSION,
                    "kind": "document_overlap",
                    "leftDocumentId": left_id,
                    "rightDocumentId": right_id,
                    "sharedParagraphHashCount": len(shared),
                    "containmentOnSmallerDocument": round(len(shared) / denominator, 6),
                    "action": "retain_and_review",
                }
            )

    kind_order = {"exact_paragraph_group": 0, "exact_passage_group": 1, "document_overlap": 2}
    records.sort(
        key=lambda item: (
            kind_order[str(item["kind"])],
            str(item.get("textSha256", "")),
            str(item.get("leftDocumentId", "")),
            str(item.get("rightDocumentId", "")),
        )
    )
    return records, {
        "exactParagraphGroupCount": sum(item["kind"] == "exact_paragraph_group" for item in records),
        "exactPassageGroupCount": sum(item["kind"] == "exact_passage_group" for item in records),
        "documentOverlapPairCount": overlap_count,
    }


def _source_aggregate_sha256(documents: Sequence[dict[str, Any]]) -> str:
    payload = "\n".join(f"{item['sourcePath']}\t{item['sourceSha256']}" for item in documents)
    return _sha256_text(payload)


def _prepare_records(
    input_dir: Path,
    contract: dict[str, Any],
    policy: dict[str, Any],
    policy_documents: dict[str, dict[str, Any]],
    min_passage_chars: int,
    max_passage_chars: int,
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    dict[str, Any],
]:
    required_source_columns = list(contract["input"]["requiredSourceManifestColumns"])
    required_rights_columns = list(contract["input"]["requiredCopyrightColumns"])
    source_path = input_dir / SOURCE_MANIFEST_NAME
    rights_path = input_dir / COPYRIGHT_REVIEW_NAME
    source_rows = _read_tsv(source_path, required_source_columns)
    rights_rows = _read_tsv(rights_path, required_rights_columns)
    source_by_relative = _assert_unique(source_rows, "relative_path", source_path)
    rights_by_asset = _assert_unique(rights_rows, "asset", rights_path)
    text_files = sorted(input_dir.glob("*.txt"), key=lambda path: path.name)
    if not text_files:
        raise ClassicsDatasetError(f"输入目录没有 TXT：{input_dir}")

    documents: list[dict[str, Any]] = []
    paragraphs: list[dict[str, Any]] = []
    passages: list[dict[str, Any]] = []
    exclusions: list[dict[str, Any]] = []
    review_queue: list[dict[str, Any]] = []
    quality_documents: list[dict[str, Any]] = []

    for text_path in text_files:
        if text_path.is_symlink() or not text_path.is_file():
            raise ClassicsDatasetError(f"输入 TXT 必须是普通文件：{text_path}")
        relative_path = f"classics/{text_path.name}"
        source = source_by_relative.get(relative_path)
        rights = rights_by_asset.get(relative_path)
        document_policy = policy_documents.get(relative_path)
        if source is None:
            raise ClassicsDatasetError(f"source_manifest.tsv 未登记：{relative_path}")
        if rights is None:
            raise ClassicsDatasetError(f"copyright_review.tsv 未登记：{relative_path}")
        if document_policy is None:
            raise ClassicsDatasetError(f"curation policy 未登记：{relative_path}")
        if source["media_type"] != "text":
            raise ClassicsDatasetError(f"canonical TXT 的 media_type 必须是 text：{relative_path}")
        if rights["status"] != contract["rightsBoundary"]["requiredRightsStatus"]:
            raise ClassicsDatasetError(f"典籍版权状态不得自动放宽：{relative_path}: {rights['status']}")

        raw_bytes = text_path.read_bytes()
        actual_sha256 = _sha256_bytes(raw_bytes)
        if str(len(raw_bytes)) != source["bytes"] or actual_sha256 != source["sha256"]:
            raise ClassicsDatasetError(f"canonical TXT 与 source_manifest.tsv 不一致：{relative_path}")
        if document_policy["sourceSha256"] != actual_sha256:
            raise ClassicsDatasetError(f"curation policy source hash 漂移：{relative_path}")
        try:
            raw_text = raw_bytes.decode("utf-8", errors="strict")
        except UnicodeDecodeError as exc:
            raise ClassicsDatasetError(f"canonical TXT 不是严格 UTF-8：{relative_path}: {exc}") from exc
        _reject_forbidden_characters(raw_text, text_path)

        document_id = _document_id(relative_path)
        raw_lines = raw_text.splitlines()
        selected_lines, document_exclusions, curation_metadata = _apply_curation_policy(
            raw_lines=raw_lines,
            document_id=document_id,
            source_path=relative_path,
            source_sha256=actual_sha256,
            document_policy=document_policy,
            policy=policy,
        )
        document_paragraphs: list[dict[str, Any]] = []
        current_heading: list[str] = []
        blank_line_count = sum(not _normalize_line(line) for line in raw_lines)
        selected_blank_line_count = 0
        removed_invisible_count = sum(raw_text.count(character) for character in REMOVE_CHARACTERS)
        normalized_space_count = raw_text.count("\u00a0")

        for source_line_number, raw_line in selected_lines:
            normalized_line = _normalize_line(raw_line)
            if not normalized_line:
                selected_blank_line_count += 1
                continue
            if _is_heading(normalized_line):
                current_heading = [_heading_text(normalized_line)]
            sequence = len(document_paragraphs) + 1
            paragraph = {
                "schemaVersion": SCHEMA_VERSION,
                "kind": "paragraph",
                "paragraphId": f"{document_id}:p{sequence:06d}",
                "documentId": document_id,
                "sequence": sequence,
                "sourceLineStart": source_line_number,
                "sourceLineEnd": source_line_number,
                "headingPath": list(current_heading),
                "text": normalized_line,
                "textSha256": _sha256_text(normalized_line),
                "charCount": len(normalized_line),
            }
            document_paragraphs.append(paragraph)

        if not document_paragraphs:
            raise ClassicsDatasetError(f"canonical TXT 清洗后为空：{relative_path}")
        normalized_text = "\n".join(str(item["text"]) for item in document_paragraphs)
        selected_raw_text = "\n".join(raw_line for _, raw_line in selected_lines)
        if _semantic_fingerprint(selected_raw_text) != _semantic_fingerprint(normalized_text):
            raise ClassicsDatasetError(f"清洗前后非空白内容不一致：{relative_path}")

        document_passages = _build_passages(
            document_id=document_id,
            paragraphs=document_paragraphs,
            source_path=relative_path,
            source_sha256=actual_sha256,
            rights=rights,
            max_chars=max_passage_chars,
        )
        title, author = _parse_title_author(text_path.name)
        quality_flags = ["rights_review_required"]
        if rights["group"] in {"mixed_notes", "modern_text_candidate"}:
            quality_flags.append(f"source_group_{rights['group']}")
        if source["source_name"].startswith("canonical:"):
            quality_flags.append("source_provenance_needs_strengthening")
        if document_policy["completeness"]["status"] == "partial":
            quality_flags.append("source_text_partial")
        if document_policy["reviewItems"]:
            quality_flags.append("curation_review_pending")
        document = {
            "schemaVersion": SCHEMA_VERSION,
            "kind": "document",
            "documentId": document_id,
            "system": source["system"],
            "title": title,
            "author": author,
            "sourcePath": relative_path,
            "sourceSha256": actual_sha256,
            "sourceBytes": len(raw_bytes),
            "sourceName": source["source_name"],
            "rightsStatus": rights["status"],
            "allowedUse": rights["allowed_use"],
            "releasePolicy": rights["release_policy"],
            "distributionAllowed": False,
            "productionUseAllowed": False,
            "trainingUseAllowed": False,
            "normalizationProfile": NORMALIZATION_PROFILE,
            "normalizedSha256": _sha256_text(normalized_text),
            "normalizedCharCount": len(normalized_text),
            "paragraphCount": len(document_paragraphs),
            "passageCount": len(document_passages),
            "qualityFlags": quality_flags,
            "familyId": document_policy["familyId"],
            "documentRole": document_policy["documentRole"],
            "roleStatus": document_policy["roleStatus"],
            "bibliography": document_policy["bibliography"],
            "completeness": document_policy["completeness"],
            "curationPolicyId": policy["policyId"],
            "curationMetadata": curation_metadata,
            "excludedSourceLineCount": len(document_exclusions),
        }
        documents.append(document)
        paragraphs.extend(document_paragraphs)
        passages.extend(document_passages)
        exclusions.extend(document_exclusions)
        for review_sequence, item in enumerate(document_policy["reviewItems"], start=1):
            review_queue.append(
                {
                    "schemaVersion": SCHEMA_VERSION,
                    "kind": "curation_review_item",
                    "reviewId": f"{document_id}:r{review_sequence:04d}",
                    "policyItemId": item["id"],
                    "documentId": document_id,
                    "sourcePath": relative_path,
                    "issueType": item["issueType"],
                    "severity": item["severity"],
                    "summary": item["summary"],
                    "evidence": item["evidence"],
                    "blocks": item["blocks"],
                    "status": "pending_human_review",
                }
            )
        quality_documents.append(
            {
                "documentId": document_id,
                "sourcePath": relative_path,
                "sourceLineCount": len(raw_lines),
                "blankLineCount": blank_line_count,
                "selectedBlankLineCount": selected_blank_line_count,
                "selectedSourceLineCount": len(selected_lines),
                "excludedSourceLineCount": len(document_exclusions),
                "paragraphCount": len(document_paragraphs),
                "passageCount": len(document_passages),
                "normalizedCharCount": len(normalized_text),
                "removedInvisibleCharacterCount": removed_invisible_count,
                "normalizedNoBreakSpaceCount": normalized_space_count,
                "qualityFlags": quality_flags,
                "familyId": document_policy["familyId"],
                "documentRole": document_policy["documentRole"],
                "completenessStatus": document_policy["completeness"]["status"],
                "reviewItemCount": len(document_policy["reviewItems"]),
            }
        )

    duplicate_records, duplicate_summary = _duplicate_records(paragraphs, passages)
    short_passages = sum(int(item["charCount"]) < min_passage_chars for item in passages)
    quality_report = {
        "schemaVersion": SCHEMA_VERSION,
        "datasetId": NORMALIZATION_PROFILE,
        "status": "passed",
        "summary": {
            "documentCount": len(documents),
            "paragraphCount": len(paragraphs),
            "passageCount": len(passages),
            "sourceBytes": sum(int(item["sourceBytes"]) for item in documents),
            "normalizedChars": sum(int(item["normalizedCharCount"]) for item in documents),
            "shortPassageCount": short_passages,
            "lineageErrorCount": 0,
            "invalidUtf8Count": 0,
            "excludedSourceLineCount": len(exclusions),
            "reviewItemCount": len(review_queue),
            "partialDocumentCount": sum(item["completeness"]["status"] == "partial" for item in documents),
            "familyCount": len({item["familyId"] for item in documents}),
            **duplicate_summary,
        },
        "documents": quality_documents,
        "rightsBoundary": contract["rightsBoundary"],
        "limits": [
            "重复标记不等于重复内容应删除。",
            "标题识别只用于导航，不构成古籍版本校勘。",
            "清洗结果不构成版权确认、训练许可或生产可用性证明。",
            "curation 文本角色、完整性和 observed bibliography 是整理元数据，不构成权威书目认证。",
        ],
    }
    return documents, paragraphs, passages, duplicate_records, exclusions, review_queue, quality_report


def _write_dataset(
    *,
    output_dir: Path,
    contract_path: Path,
    contract: dict[str, Any],
    documents: Sequence[dict[str, Any]],
    paragraphs: Sequence[dict[str, Any]],
    passages: Sequence[dict[str, Any]],
    duplicates: Sequence[dict[str, Any]],
    exclusions: Sequence[dict[str, Any]],
    review_queue: Sequence[dict[str, Any]],
    quality_report: dict[str, Any],
    input_dir: Path,
    curation_policy_path: Path,
    min_passage_chars: int,
    max_passage_chars: int,
) -> None:
    output_dir.parent.mkdir(parents=True, exist_ok=True)
    temporary_dir = Path(tempfile.mkdtemp(prefix=f".{output_dir.name}.build-", dir=output_dir.parent))
    backup_dir = output_dir.parent / f".{output_dir.name}.backup"
    try:
        _write_ndjson(temporary_dir / "documents.ndjson", documents)
        _write_ndjson(temporary_dir / "paragraphs.ndjson", paragraphs)
        _write_ndjson(temporary_dir / "passages.ndjson", passages)
        _write_ndjson(temporary_dir / "duplicates.ndjson", duplicates)
        _write_ndjson(temporary_dir / "exclusions.ndjson", exclusions)
        _write_ndjson(temporary_dir / "review-queue.ndjson", review_queue)
        (temporary_dir / "quality-report.json").write_text(
            f"{_json_dumps(quality_report)}\n", encoding="utf-8", newline="\n"
        )

        artifact_hashes = {name: _sha256_file(temporary_dir / name) for name in OUTPUT_DATA_FILES}
        manifest = {
            "schemaVersion": SCHEMA_VERSION,
            "datasetId": NORMALIZATION_PROFILE,
            "status": "passed",
            "contractId": contract["contractId"],
            "contractPath": _manifest_path(contract_path),
            "builder": BUILDER_PATH,
            "normalizationProfile": NORMALIZATION_PROFILE,
            "parameters": {
                "minPassageChars": min_passage_chars,
                "maxPassageChars": max_passage_chars,
            },
            "source": {
                "inputRole": "canonical_classics",
                "sourceManifestSha256": _sha256_file(input_dir / SOURCE_MANIFEST_NAME),
                "copyrightReviewSha256": _sha256_file(input_dir / COPYRIGHT_REVIEW_NAME),
                "curationPolicyPath": _manifest_path(curation_policy_path),
                "curationPolicySha256": _sha256_file(curation_policy_path),
                "sourceAggregateSha256": _source_aggregate_sha256(documents),
                "documentCount": len(documents),
            },
            "counts": {
                "documentCount": len(documents),
                "paragraphCount": len(paragraphs),
                "passageCount": len(passages),
                "duplicateRecordCount": len(duplicates),
                "exclusionRecordCount": len(exclusions),
                "reviewItemCount": len(review_queue),
            },
            "artifacts": artifact_hashes,
            "rightsBoundary": contract["rightsBoundary"],
        }
        (temporary_dir / "manifest.json").write_text(f"{_json_dumps(manifest)}\n", encoding="utf-8", newline="\n")
        checksum_files = (*OUTPUT_DATA_FILES, "manifest.json")
        checksum_text = "".join(f"{_sha256_file(temporary_dir / name)}  {name}\n" for name in checksum_files)
        (temporary_dir / "files.sha256").write_text(checksum_text, encoding="ascii", newline="\n")

        if backup_dir.exists():
            raise ClassicsDatasetError(f"发现上次未清理的交换备份目录：{backup_dir}")
        if output_dir.exists():
            os.replace(output_dir, backup_dir)
        try:
            os.replace(temporary_dir, output_dir)
        except Exception:
            if backup_dir.exists() and not output_dir.exists():
                os.replace(backup_dir, output_dir)
            raise
        if backup_dir.exists():
            shutil.rmtree(backup_dir)
    finally:
        if temporary_dir.exists():
            shutil.rmtree(temporary_dir)


def build_dataset(
    *,
    input_dir: Path,
    output_dir: Path,
    contract_path: Path = DEFAULT_CONTRACT,
    curation_policy_path: Path = DEFAULT_CURATION_POLICY,
    min_passage_chars: int = 200,
    max_passage_chars: int = 1200,
) -> dict[str, Any]:
    source, target = _validate_path_boundary(input_dir, output_dir)
    if min_passage_chars < 1 or max_passage_chars < min_passage_chars:
        raise ClassicsDatasetError("切片字符上限必须大于等于下限，且下限至少为 1")
    contract = _load_json(contract_path)
    source_paths = {f"classics/{path.name}" for path in source.glob("*.txt")}
    policy, policy_documents = _load_curation_policy(curation_policy_path, source_paths)
    expected_max = int(contract["chunking"]["defaultMaxPassageChars"])
    if max_passage_chars > expected_max:
        raise ClassicsDatasetError(f"maxPassageChars 不得超过契约上限 {expected_max}")
    documents, paragraphs, passages, duplicates, exclusions, review_queue, quality_report = _prepare_records(
        source,
        contract,
        policy,
        policy_documents,
        min_passage_chars,
        max_passage_chars,
    )
    _write_dataset(
        output_dir=target,
        contract_path=contract_path,
        contract=contract,
        documents=documents,
        paragraphs=paragraphs,
        passages=passages,
        duplicates=duplicates,
        exclusions=exclusions,
        review_queue=review_queue,
        quality_report=quality_report,
        input_dir=source,
        curation_policy_path=curation_policy_path,
        min_passage_chars=min_passage_chars,
        max_passage_chars=max_passage_chars,
    )
    return validate_dataset(
        target,
        contract_path=contract_path,
        curation_policy_path=curation_policy_path,
        input_dir=source,
    )


def _require_fields(record: dict[str, Any], fields: Sequence[str], record_id: str) -> None:
    missing = sorted(set(fields) - set(record))
    if missing:
        raise ClassicsDatasetError(f"记录缺少字段 {missing}：{record_id}")


def _validate_checksums(output_dir: Path) -> None:
    checksum_path = output_dir / "files.sha256"
    entries: dict[str, str] = {}
    for line_number, line in enumerate(checksum_path.read_text(encoding="ascii").splitlines(), start=1):
        match = re.fullmatch(r"([0-9a-f]{64})  ([A-Za-z0-9._-]+)", line)
        if not match:
            raise ClassicsDatasetError(f"files.sha256 格式错误：{line_number}")
        expected, name = match.groups()
        if name in entries:
            raise ClassicsDatasetError(f"files.sha256 文件名重复：{name}")
        entries[name] = expected
    expected_names = {*OUTPUT_DATA_FILES, "manifest.json"}
    if set(entries) != expected_names:
        raise ClassicsDatasetError(f"files.sha256 文件集合错误：{sorted(entries)}")
    for name, expected in entries.items():
        path = output_dir / name
        if not path.is_file() or _sha256_file(path) != expected:
            raise ClassicsDatasetError(f"输出文件 hash 不一致：{name}")


def validate_dataset(
    output_dir: Path,
    *,
    contract_path: Path = DEFAULT_CONTRACT,
    curation_policy_path: Path = DEFAULT_CURATION_POLICY,
    input_dir: Path | None = None,
) -> dict[str, Any]:
    target = output_dir.resolve()
    contract = _load_json(contract_path)
    required_files = set(contract["output"]["requiredFiles"])
    missing_files = sorted(name for name in required_files if not (target / name).is_file())
    if missing_files:
        raise ClassicsDatasetError(f"数据集缺少输出文件：{missing_files}")
    _validate_checksums(target)

    documents = _read_ndjson(target / "documents.ndjson")
    paragraphs = _read_ndjson(target / "paragraphs.ndjson")
    passages = _read_ndjson(target / "passages.ndjson")
    duplicates = _read_ndjson(target / "duplicates.ndjson")
    exclusions = _read_ndjson(target / "exclusions.ndjson")
    review_queue = _read_ndjson(target / "review-queue.ndjson")
    quality = _load_json(target / "quality-report.json")
    manifest = _load_json(target / "manifest.json")
    if manifest.get("status") != "passed" or manifest.get("contractId") != contract["contractId"]:
        raise ClassicsDatasetError("manifest status 或 contractId 与清洗契约不一致")
    if manifest.get("rightsBoundary") != contract["rightsBoundary"]:
        raise ClassicsDatasetError("manifest 权限边界与清洗契约不一致")
    if manifest.get("source", {}).get("curationPolicySha256") != _sha256_file(curation_policy_path):
        raise ClassicsDatasetError("manifest curation policy hash 不一致")

    policy, policy_documents = _load_curation_policy(
        curation_policy_path, {str(item.get("sourcePath", "")) for item in documents}
    )

    for filename in OUTPUT_DATA_FILES:
        expected = manifest["artifacts"].get(filename)
        if not expected or expected != _sha256_file(target / filename):
            raise ClassicsDatasetError(f"manifest artifact hash 不一致：{filename}")

    document_by_id: dict[str, dict[str, Any]] = {}
    for document in documents:
        _require_fields(document, contract["requiredDocumentFields"], str(document.get("documentId", "<missing>")))
        document_id = str(document["documentId"])
        if document_id in document_by_id or document.get("kind") != "document":
            raise ClassicsDatasetError(f"document ID 重复或 kind 错误：{document_id}")
        if any(
            document.get(field) is not False
            for field in ("distributionAllowed", "productionUseAllowed", "trainingUseAllowed")
        ):
            raise ClassicsDatasetError(f"document 权限边界被放宽：{document_id}")
        if document.get("rightsStatus") != contract["rightsBoundary"]["requiredRightsStatus"]:
            raise ClassicsDatasetError(f"document rightsStatus 错误：{document_id}")
        if not re.fullmatch(r"[0-9a-f]{64}", str(document["sourceSha256"])):
            raise ClassicsDatasetError(f"document sourceSha256 格式错误：{document_id}")
        document_policy = policy_documents.get(str(document["sourcePath"]))
        if document_policy is None or document_policy["sourceSha256"] != document["sourceSha256"]:
            raise ClassicsDatasetError(f"document curation policy 断链：{document_id}")
        expected_curation_fields = {
            "familyId": document_policy["familyId"],
            "documentRole": document_policy["documentRole"],
            "roleStatus": document_policy["roleStatus"],
            "bibliography": document_policy["bibliography"],
            "completeness": document_policy["completeness"],
            "curationPolicyId": policy["policyId"],
        }
        if any(document.get(field) != value for field, value in expected_curation_fields.items()):
            raise ClassicsDatasetError(f"document curation metadata 与 policy 不一致：{document_id}")
        document_by_id[document_id] = document

    paragraph_by_id: dict[str, dict[str, Any]] = {}
    paragraphs_by_document: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for paragraph in paragraphs:
        _require_fields(paragraph, contract["requiredParagraphFields"], str(paragraph.get("paragraphId", "<missing>")))
        paragraph_id = str(paragraph["paragraphId"])
        document_id = str(paragraph["documentId"])
        if paragraph_id in paragraph_by_id or document_id not in document_by_id or paragraph.get("kind") != "paragraph":
            raise ClassicsDatasetError(f"paragraph 引用、ID 或 kind 错误：{paragraph_id}")
        text = str(paragraph["text"])
        if not text or _sha256_text(text) != paragraph["textSha256"] or len(text) != paragraph["charCount"]:
            raise ClassicsDatasetError(f"paragraph 内容 hash 或长度错误：{paragraph_id}")
        paragraph_by_id[paragraph_id] = paragraph
        paragraphs_by_document[document_id].append(paragraph)

    passages_by_document: dict[str, list[dict[str, Any]]] = defaultdict(list)
    max_chars = int(manifest["parameters"]["maxPassageChars"])
    seen_passage_ids: set[str] = set()
    for passage in passages:
        _require_fields(passage, contract["requiredPassageFields"], str(passage.get("passageId", "<missing>")))
        passage_id = str(passage["passageId"])
        document_id = str(passage["documentId"])
        if passage_id in seen_passage_ids or document_id not in document_by_id or passage.get("kind") != "passage":
            raise ClassicsDatasetError(f"passage 引用、ID 或 kind 错误：{passage_id}")
        seen_passage_ids.add(passage_id)
        if any(str(item) not in paragraph_by_id for item in passage["paragraphIds"]):
            raise ClassicsDatasetError(f"passage paragraphIds 断链：{passage_id}")
        referenced_paragraphs = [paragraph_by_id[str(item)] for item in passage["paragraphIds"]]
        if any(str(item["documentId"]) != document_id for item in referenced_paragraphs):
            raise ClassicsDatasetError(f"passage 引用了其他文档的 paragraph：{passage_id}")
        text = str(passage["text"])
        if (
            not text
            or len(text) > max_chars
            or len(text) != passage["charCount"]
            or _sha256_text(text) != passage["textSha256"]
        ):
            raise ClassicsDatasetError(f"passage 内容 hash、长度或上限错误：{passage_id}")
        document = document_by_id[document_id]
        if passage["sourcePath"] != document["sourcePath"] or passage["sourceSha256"] != document["sourceSha256"]:
            raise ClassicsDatasetError(f"passage 来源断链：{passage_id}")
        expected_paragraph_range = (
            min(int(item["sequence"]) for item in referenced_paragraphs),
            max(int(item["sequence"]) for item in referenced_paragraphs),
        )
        expected_source_range = (
            min(int(item["sourceLineStart"]) for item in referenced_paragraphs),
            max(int(item["sourceLineEnd"]) for item in referenced_paragraphs),
        )
        if (passage["paragraphStart"], passage["paragraphEnd"]) != expected_paragraph_range:
            raise ClassicsDatasetError(f"passage paragraph range 错误：{passage_id}")
        if (passage["sourceLineStart"], passage["sourceLineEnd"]) != expected_source_range:
            raise ClassicsDatasetError(f"passage source line range 错误：{passage_id}")
        if any(
            passage.get(field) is not False
            for field in ("distributionAllowed", "productionUseAllowed", "trainingUseAllowed")
        ):
            raise ClassicsDatasetError(f"passage 权限边界被放宽：{passage_id}")
        passages_by_document[document_id].append(passage)

    exclusions_by_document: dict[str, list[dict[str, Any]]] = defaultdict(list)
    seen_exclusion_ids: set[str] = set()
    seen_excluded_lines: set[tuple[str, int]] = set()
    for exclusion in exclusions:
        _require_fields(
            exclusion,
            contract["requiredExclusionFields"],
            str(exclusion.get("exclusionId", "<missing>")),
        )
        exclusion_id = str(exclusion["exclusionId"])
        document_id = str(exclusion["documentId"])
        source_line = int(exclusion["sourceLine"])
        document = document_by_id.get(document_id)
        if (
            exclusion_id in seen_exclusion_ids
            or (document_id, source_line) in seen_excluded_lines
            or document is None
            or exclusion.get("kind") != "excluded_source_line"
            or "text" in exclusion
        ):
            raise ClassicsDatasetError(f"exclusion ID、line、document 或隐私边界错误：{exclusion_id}")
        if exclusion["sourcePath"] != document["sourcePath"] or exclusion["sourceSha256"] != document["sourceSha256"]:
            raise ClassicsDatasetError(f"exclusion 来源断链：{exclusion_id}")
        if not re.fullmatch(r"[0-9a-f]{64}", str(exclusion["textSha256"])):
            raise ClassicsDatasetError(f"exclusion textSha256 格式错误：{exclusion_id}")
        seen_exclusion_ids.add(exclusion_id)
        seen_excluded_lines.add((document_id, source_line))
        exclusions_by_document[document_id].append(exclusion)

    review_by_document: dict[str, list[dict[str, Any]]] = defaultdict(list)
    seen_review_ids: set[str] = set()
    for review_item in review_queue:
        _require_fields(
            review_item,
            contract["requiredReviewItemFields"],
            str(review_item.get("reviewId", "<missing>")),
        )
        review_id = str(review_item["reviewId"])
        document_id = str(review_item["documentId"])
        document = document_by_id.get(document_id)
        if (
            review_id in seen_review_ids
            or document is None
            or review_item.get("kind") != "curation_review_item"
            or review_item.get("status") != "pending_human_review"
            or review_item.get("severity") not in ALLOWED_REVIEW_SEVERITY
        ):
            raise ClassicsDatasetError(f"review item ID、document、status 或 severity 错误：{review_id}")
        document_policy = policy_documents[str(document["sourcePath"])]
        policy_item = next(
            (item for item in document_policy["reviewItems"] if item["id"] == review_item["policyItemId"]),
            None,
        )
        expected_fields = ("issueType", "severity", "summary", "evidence", "blocks")
        if (
            policy_item is None
            or review_item["sourcePath"] != document["sourcePath"]
            or any(review_item[field] != policy_item[field] for field in expected_fields)
        ):
            raise ClassicsDatasetError(f"review item 与 policy 不一致：{review_id}")
        seen_review_ids.add(review_id)
        review_by_document[document_id].append(review_item)

    for document_id, document in document_by_id.items():
        document_paragraphs = sorted(paragraphs_by_document[document_id], key=lambda item: int(item["sequence"]))
        document_passages = sorted(passages_by_document[document_id], key=lambda item: int(item["sequence"]))
        if len(document_paragraphs) != document["paragraphCount"] or len(document_passages) != document["passageCount"]:
            raise ClassicsDatasetError(f"document 计数不一致：{document_id}")
        if [int(item["sequence"]) for item in document_paragraphs] != list(range(1, len(document_paragraphs) + 1)):
            raise ClassicsDatasetError(f"document paragraph sequence 不连续：{document_id}")
        if [int(item["sequence"]) for item in document_passages] != list(range(1, len(document_passages) + 1)):
            raise ClassicsDatasetError(f"document passage sequence 不连续：{document_id}")
        normalized_text = "\n".join(str(item["text"]) for item in document_paragraphs)
        if _sha256_text(normalized_text) != document["normalizedSha256"]:
            raise ClassicsDatasetError(f"document normalizedSha256 不一致：{document_id}")
        passage_text = "\n".join(str(item["text"]) for item in document_passages)
        if _semantic_fingerprint(passage_text) != _semantic_fingerprint(normalized_text):
            raise ClassicsDatasetError(f"document passage 与 paragraph 内容不一致：{document_id}")
        if len(exclusions_by_document[document_id]) != document["excludedSourceLineCount"]:
            raise ClassicsDatasetError(f"document exclusion 计数不一致：{document_id}")
        expected_review_count = len(policy_documents[str(document["sourcePath"])]["reviewItems"])
        if len(review_by_document[document_id]) != expected_review_count:
            raise ClassicsDatasetError(f"document review queue 计数不一致：{document_id}")

    allowed_duplicate_kinds = {"exact_paragraph_group", "exact_passage_group", "document_overlap"}
    if any(item.get("kind") not in allowed_duplicate_kinds or "text" in item for item in duplicates):
        raise ClassicsDatasetError("duplicates.ndjson 含非法 kind 或复制了正文")

    if input_dir is not None:
        source, _ = _validate_path_boundary(input_dir, target)
        if manifest["source"]["sourceManifestSha256"] != _sha256_file(source / SOURCE_MANIFEST_NAME):
            raise ClassicsDatasetError("数据集 source_manifest.tsv 已漂移")
        if manifest["source"]["copyrightReviewSha256"] != _sha256_file(source / COPYRIGHT_REVIEW_NAME):
            raise ClassicsDatasetError("数据集 copyright_review.tsv 已漂移")
        for document in documents:
            source_file = source / Path(str(document["sourcePath"])).name
            if not source_file.is_file() or _sha256_file(source_file) != document["sourceSha256"]:
                raise ClassicsDatasetError(f"数据集来源已漂移：{document['sourcePath']}")
            raw_text = source_file.read_text(encoding="utf-8", errors="strict")
            selected_lines, expected_exclusions, expected_metadata = _apply_curation_policy(
                raw_lines=raw_text.splitlines(),
                document_id=str(document["documentId"]),
                source_path=str(document["sourcePath"]),
                source_sha256=str(document["sourceSha256"]),
                document_policy=policy_documents[str(document["sourcePath"])],
                policy=policy,
            )
            actual_exclusions = sorted(
                exclusions_by_document[str(document["documentId"])], key=lambda item: int(item["sourceLine"])
            )
            if actual_exclusions != expected_exclusions or document["curationMetadata"] != expected_metadata:
                raise ClassicsDatasetError(f"数据集 exclusion/metadata 与 policy 重放不一致：{document['sourcePath']}")
            selected_raw_text = "\n".join(line for _, line in selected_lines)
            normalized_text = "\n".join(
                str(item["text"])
                for item in sorted(
                    paragraphs_by_document[str(document["documentId"])], key=lambda item: int(item["sequence"])
                )
            )
            if _semantic_fingerprint(selected_raw_text) != _semantic_fingerprint(normalized_text):
                raise ClassicsDatasetError(f"数据集正文选择与 paragraph 内容不一致：{document['sourcePath']}")

    if manifest["source"]["sourceAggregateSha256"] != _source_aggregate_sha256(documents):
        raise ClassicsDatasetError("manifest sourceAggregateSha256 与 document 来源不一致")

    expected_counts = {
        "documentCount": len(documents),
        "paragraphCount": len(paragraphs),
        "passageCount": len(passages),
        "duplicateRecordCount": len(duplicates),
        "exclusionRecordCount": len(exclusions),
        "reviewItemCount": len(review_queue),
    }
    if manifest.get("counts") != expected_counts:
        raise ClassicsDatasetError("manifest counts 与输出记录不一致")
    quality_summary = quality.get("summary", {})
    if (
        quality.get("status") != "passed"
        or quality.get("rightsBoundary") != contract["rightsBoundary"]
        or quality_summary.get("documentCount") != len(documents)
        or quality_summary.get("lineageErrorCount") != 0
        or quality_summary.get("invalidUtf8Count") != 0
        or quality_summary.get("excludedSourceLineCount") != len(exclusions)
        or quality_summary.get("reviewItemCount") != len(review_queue)
    ):
        raise ClassicsDatasetError("quality-report 状态或文档计数错误")
    return {
        "status": "passed",
        "datasetId": manifest["datasetId"],
        "output": str(target),
        "counts": expected_counts,
        "sourceAggregateSha256": manifest["source"]["sourceAggregateSha256"],
        "rightsBoundary": manifest["rightsBoundary"],
    }


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT, help="canonical 典籍输入目录")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="ignored 本地派生数据集目录")
    parser.add_argument("--contract", type=Path, default=DEFAULT_CONTRACT, help="数据集契约 JSON")
    parser.add_argument(
        "--curation-policy",
        type=Path,
        default=DEFAULT_CURATION_POLICY,
        help="source-hash 绑定的正文选择与书目整理策略 JSON",
    )
    parser.add_argument("--min-passage-chars", type=int, default=200, help="质量统计中的目标最小切片字符数")
    parser.add_argument("--max-passage-chars", type=int, default=1200, help="切片硬上限")
    parser.add_argument("--validate-only", action="store_true", help="只验证已有输出，不重新生成")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    try:
        if args.validate_only:
            result = validate_dataset(
                args.output,
                contract_path=args.contract,
                curation_policy_path=args.curation_policy,
                input_dir=args.input,
            )
        else:
            result = build_dataset(
                input_dir=args.input,
                output_dir=args.output,
                contract_path=args.contract,
                curation_policy_path=args.curation_policy,
                min_passage_chars=args.min_passage_chars,
                max_passage_chars=args.max_passage_chars,
            )
    except ClassicsDatasetError as exc:
        raise SystemExit(f"classics dataset failed: {exc}") from exc
    print(_json_dumps(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
