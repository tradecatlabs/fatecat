from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT_PATH = ROOT / "scripts" / "classics-dataset-clean.py"
CONTRACT_PATH = ROOT / "contracts" / "fate" / "data-supply-chain" / "schemas" / "classics-clean-dataset.schema.json"
REGISTRY_PATH = ROOT / "contracts" / "fate" / "data-supply-chain" / "registry.json"


def _load_module():
    spec = importlib.util.spec_from_file_location("classics_dataset_clean", SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"无法加载典籍清洗器：{SCRIPT_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _write_fixture_corpus(base: Path, files: dict[str, bytes] | None = None) -> Path:
    corpus = base / "classics"
    corpus.mkdir(parents=True)
    payloads = files or {
        "甲书 - 甲作者.txt": (
            "\ufeff第一卷\r\n"
            "作者：甲作者\r\n"
            "来源章节：https://ctext.org/wiki.pl?chapter=1\r\n"
            "甲乙丙丁\u00a0戊己。\r\n"
            "\r\n"
            "共同正文用于重复标记，不应删除。\r\n" + "这一段很长，用于验证切片不会丢字；" * 35
        ).encode("utf-8"),
        "乙书 - 乙作者.txt": ("推广包装\n序\n共同正文用于重复标记，不应删除。\n另一条正文。\u200b\n尾部推广\n").encode(
            "utf-8"
        ),
    }
    source_lines = ["system\tmedia_type\trelative_path\tbytes\tsha256\tsource_name"]
    rights_lines = ["asset\tgroup\tstatus\tallowed_use\trelease_policy\tnotes"]
    for filename, data in sorted(payloads.items()):
        (corpus / filename).write_bytes(data)
        relative = f"classics/{filename}"
        source_lines.append(f"bazi\ttext\t{relative}\t{len(data)}\t{_sha256(data)}\tfixture:{filename}")
        rights_lines.append(
            f"{relative}\tpublic_domain_candidate\treview_required\trule_index_seed\t"
            "extract_short_structured_rules_only\t测试夹具"
        )
    (corpus / "source_manifest.tsv").write_text("\n".join(source_lines) + "\n", encoding="utf-8")
    (corpus / "copyright_review.tsv").write_text("\n".join(rights_lines) + "\n", encoding="utf-8")
    policy_documents = []
    for filename, data in sorted(payloads.items()):
        title, _, attribution = Path(filename).stem.partition(" - ")
        is_first = filename.startswith("甲书")
        is_second = filename.startswith("乙书")
        policy_documents.append(
            {
                "sourcePath": f"classics/{filename}",
                "sourceSha256": _sha256(data),
                "familyId": f"fixture-{_sha256(filename.encode())[:8]}",
                "documentRole": "treatise",
                "roleStatus": "curator_assigned",
                "bibliography": {
                    "observedTitle": title,
                    "observedAttribution": attribution or None,
                    "reviewed": None,
                    "reviewStatus": "review_required",
                },
                "completeness": {"status": "unknown", "evidence": []},
                "structure": {"navigationLineRanges": [[2, 2]] if is_second else []},
                "selection": {
                    "mode": "include_line_ranges" if is_second else "all",
                    "includeLineRanges": [[2, 4]] if is_second else [],
                    "ruleSetRefs": ["fixture-envelope"] if is_first else [],
                    "lineRules": [],
                },
                "reviewItems": (
                    [
                        {
                            "id": "fixture-review",
                            "issueType": "fixture_issue",
                            "severity": "low",
                            "summary": "测试复核项。",
                            "evidence": ["fixture"],
                            "blocks": ["fixture_claim"],
                        }
                    ]
                    if is_first
                    else []
                ),
            }
        )
    policy = {
        "schemaVersion": 2,
        "policyId": "fixture-curation-v2",
        "description": "测试整理策略",
        "ruleSets": {
            "fixture-envelope": [
                {
                    "id": "fixture-author",
                    "action": "extract_and_exclude",
                    "target": "embeddedAuthor",
                    "extractMode": "suffix",
                    "match": {"type": "prefix", "value": "作者："},
                    "classification": "source_metadata",
                    "reason": "测试作者元数据。",
                },
                {
                    "id": "fixture-source-url",
                    "action": "extract_and_exclude",
                    "target": "chapterSourceUrls",
                    "extractMode": "after_label",
                    "match": {"type": "prefix", "value": "来源章节：https://ctext.org/"},
                    "classification": "source_metadata",
                    "reason": "测试来源元数据。",
                },
            ]
        },
        "documents": policy_documents,
        "invariants": ["fixture"],
    }
    (corpus / "curation_policy.json").write_text(
        json.dumps(policy, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )
    return corpus


def _build_dataset(cleaner, source: Path, output: Path, **kwargs):
    return cleaner.build_dataset(
        input_dir=source,
        output_dir=output,
        curation_policy_path=source / "curation_policy.json",
        **kwargs,
    )


def _validate_dataset(cleaner, source: Path, output: Path):
    return cleaner.validate_dataset(
        output,
        curation_policy_path=source / "curation_policy.json",
        input_dir=source,
    )


def _read_ndjson(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def _write_ndjson(path: Path, records: list[dict]) -> None:
    path.write_text(
        "".join(
            json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n" for record in records
        ),
        encoding="utf-8",
    )


def _refresh_integrity_metadata(output: Path) -> None:
    manifest_path = output / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    for name in manifest["artifacts"]:
        manifest["artifacts"][name] = _sha256((output / name).read_bytes())
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )
    checksum_names = (
        "documents.ndjson",
        "paragraphs.ndjson",
        "passages.ndjson",
        "duplicates.ndjson",
        "exclusions.ndjson",
        "review-queue.ndjson",
        "quality-report.json",
        "manifest.json",
    )
    (output / "files.sha256").write_text(
        "".join(f"{_sha256((output / name).read_bytes())}  {name}\n" for name in checksum_names),
        encoding="ascii",
    )


def test_cleaner_is_deterministic_traceable_and_keeps_rights_closed(tmp_path):
    cleaner = _load_module()
    source = _write_fixture_corpus(tmp_path / "source")
    output_a = tmp_path / "out-a"
    output_b = tmp_path / "out-b"

    result_a = _build_dataset(cleaner, source, output_a, min_passage_chars=40, max_passage_chars=120)
    result_b = _build_dataset(cleaner, source, output_b, min_passage_chars=40, max_passage_chars=120)

    assert result_a["status"] == result_b["status"] == "passed"
    for filename in json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))["output"]["requiredFiles"]:
        assert (output_a / filename).read_bytes() == (output_b / filename).read_bytes()

    documents = _read_ndjson(output_a / "documents.ndjson")
    paragraphs = _read_ndjson(output_a / "paragraphs.ndjson")
    passages = _read_ndjson(output_a / "passages.ndjson")
    exclusions = _read_ndjson(output_a / "exclusions.ndjson")
    review_queue = _read_ndjson(output_a / "review-queue.ndjson")
    assert len(documents) == 2
    assert all(document["rightsStatus"] == "review_required" for document in documents)
    assert all(document["distributionAllowed"] is False for document in documents)
    assert all(document["productionUseAllowed"] is False for document in documents)
    assert all(document["trainingUseAllowed"] is False for document in documents)
    assert all(passage["sourcePath"].startswith("classics/") for passage in passages)
    assert all(passage["sourceSha256"] for passage in passages)
    assert all(passage["paragraphIds"] for passage in passages)
    assert all(1 <= passage["sourceLineStart"] <= passage["sourceLineEnd"] for passage in passages)
    assert all(passage["charCount"] <= 120 for passage in passages)
    assert all(paragraph["text"] for paragraph in paragraphs)
    assert all(
        paragraph["paragraphType"] in {"document_title", "heading", "navigation", "body"} for paragraph in paragraphs
    )
    assert all(paragraph["sourceLineCount"] == len(paragraph["sourceLineNumbers"]) for paragraph in paragraphs)
    assert any(paragraph["paragraphType"] == "navigation" and paragraph["text"] == "序" for paragraph in paragraphs)
    assert all("序" not in passage["text"] for passage in passages)
    assert len(exclusions) == 4
    assert all("text" not in record for record in exclusions)
    assert len(review_queue) == 1
    assert review_queue[0]["status"] == "pending_human_review"
    first_document = next(document for document in documents if document["title"] == "甲书")
    assert first_document["curationMetadata"]["embeddedAuthor"] == "甲作者"
    assert first_document["curationMetadata"]["chapterSourceUrls"] == ["https://ctext.org/wiki.pl?chapter=1"]
    manifest = json.loads((output_a / "manifest.json").read_text(encoding="utf-8"))
    quality = json.loads((output_a / "quality-report.json").read_text(encoding="utf-8"))
    assert manifest["status"] == "passed"
    assert quality["summary"]["lineageErrorCount"] == 0
    assert quality["summary"]["semanticReplayErrorCount"] == 0
    assert quality["summary"]["passageHeadingBoundaryViolationCount"] == 0
    assert quality["summary"]["navigationPassageCount"] == 0
    assert quality["summary"]["invalidUtf8Count"] == 0


def test_semantic_paragraphs_join_wrapped_lines_and_passages_stay_inside_headings(tmp_path):
    cleaner = _load_module()
    payload = (
        "语义书\n第一卷\n论甲\n这是被排版拆开的\n一句正文。\nASCII word\nboundary test.\n论乙\n乙段正文。\n"
    ).encode()
    source = _write_fixture_corpus(tmp_path / "source", {"语义书 - 测试作者.txt": payload})
    output = tmp_path / "output"

    _build_dataset(cleaner, source, output, min_passage_chars=20, max_passage_chars=120)

    paragraphs = _read_ndjson(output / "paragraphs.ndjson")
    passages = _read_ndjson(output / "passages.ndjson")
    assert any(paragraph["text"] == "这是被排版拆开的一句正文。" for paragraph in paragraphs)
    assert any(paragraph["text"] == "ASCII word boundary test." for paragraph in paragraphs)
    assert [paragraph["paragraphType"] for paragraph in paragraphs[:3]] == [
        "document_title",
        "heading",
        "heading",
    ]
    assert {tuple(passage["headingPath"]) for passage in passages} == {
        ("第一卷", "论甲"),
        ("第一卷", "论乙"),
    }
    assert all("论甲" not in passage["text"] and "论乙" not in passage["text"] for passage in passages)


def test_normalization_removes_only_allowed_noise_and_preserves_duplicate_paragraphs(tmp_path):
    cleaner = _load_module()
    source = _write_fixture_corpus(tmp_path / "source")
    output = tmp_path / "output"

    _build_dataset(cleaner, source, output, min_passage_chars=40, max_passage_chars=120)

    paragraphs = _read_ndjson(output / "paragraphs.ndjson")
    combined = "\n".join(record["text"] for record in paragraphs)
    assert "\ufeff" not in combined
    assert "\u200b" not in combined
    assert "\u00a0" not in combined
    assert "甲乙丙丁 戊己。" in combined
    assert "作者：" not in combined
    assert "来源章节：" not in combined
    assert "推广包装" not in combined
    assert "尾部推广" not in combined
    repeated = [record for record in paragraphs if record["text"] == "共同正文用于重复标记，不应删除。"]
    assert len(repeated) == 2

    duplicate_records = _read_ndjson(output / "duplicates.ndjson")
    exact_groups = [record for record in duplicate_records if record["kind"] == "exact_paragraph_group"]
    assert any(record["occurrenceCount"] == 2 for record in exact_groups)
    paragraph_by_id = {record["paragraphId"]: record for record in paragraphs}
    assert all(
        paragraph_by_id[paragraph_id]["paragraphType"] == "body"
        for record in exact_groups
        for paragraph_id in record["paragraphIds"]
    )
    assert all("text" not in record for record in duplicate_records)


@pytest.mark.parametrize(
    "payload",
    [
        b"\xff\xfe\x00\x01",
        "合法正文\x00非法尾部".encode(),
        "合法正文\x07非法尾部".encode(),
    ],
)
def test_cleaner_rejects_invalid_utf8_and_control_characters(tmp_path, payload):
    cleaner = _load_module()
    source = _write_fixture_corpus(tmp_path / "source", {"坏文件.txt": payload})

    with pytest.raises(cleaner.ClassicsDatasetError):
        _build_dataset(cleaner, source, tmp_path / "output")


def test_cleaner_rejects_input_output_containment(tmp_path):
    cleaner = _load_module()
    source = _write_fixture_corpus(tmp_path / "source")

    with pytest.raises(cleaner.ClassicsDatasetError, match="互相包含"):
        _build_dataset(cleaner, source, source / "derived")
    with pytest.raises(cleaner.ClassicsDatasetError, match="互相包含"):
        _build_dataset(cleaner, source, source.parent)


def test_cleaner_fails_closed_on_policy_hash_drift_and_out_of_range_selection(tmp_path):
    cleaner = _load_module()
    source = _write_fixture_corpus(tmp_path / "source")
    policy_path = source / "curation_policy.json"
    policy = json.loads(policy_path.read_text(encoding="utf-8"))
    policy["documents"][0]["sourceSha256"] = "0" * 64
    policy_path.write_text(json.dumps(policy, ensure_ascii=False), encoding="utf-8")
    with pytest.raises(cleaner.ClassicsDatasetError, match="source hash 漂移"):
        _build_dataset(cleaner, source, tmp_path / "hash-drift")

    source = _write_fixture_corpus(tmp_path / "range-source")
    policy_path = source / "curation_policy.json"
    policy = json.loads(policy_path.read_text(encoding="utf-8"))
    target = next(item for item in policy["documents"] if item["sourcePath"].endswith("乙书 - 乙作者.txt"))
    target["selection"]["includeLineRanges"] = [[2, 999]]
    policy_path.write_text(json.dumps(policy, ensure_ascii=False), encoding="utf-8")
    with pytest.raises(cleaner.ClassicsDatasetError, match="越界"):
        _build_dataset(cleaner, source, tmp_path / "range-error")

    source = _write_fixture_corpus(tmp_path / "navigation-range-source")
    policy_path = source / "curation_policy.json"
    policy = json.loads(policy_path.read_text(encoding="utf-8"))
    policy["documents"][0]["structure"]["navigationLineRanges"] = [[1, 999]]
    policy_path.write_text(json.dumps(policy, ensure_ascii=False), encoding="utf-8")
    with pytest.raises(cleaner.ClassicsDatasetError, match="navigationLineRanges 越界"):
        _build_dataset(cleaner, source, tmp_path / "navigation-range-error")


def test_cleaner_rejects_unreviewed_bibliography_being_marked_as_reviewed(tmp_path):
    cleaner = _load_module()
    source = _write_fixture_corpus(tmp_path / "source")
    policy_path = source / "curation_policy.json"
    policy = json.loads(policy_path.read_text(encoding="utf-8"))
    policy["documents"][0]["bibliography"]["reviewed"] = {"title": "未经证据核实"}
    policy_path.write_text(json.dumps(policy, ensure_ascii=False), encoding="utf-8")

    with pytest.raises(cleaner.ClassicsDatasetError, match="书目复核边界非法"):
        _build_dataset(cleaner, source, tmp_path / "output")


def test_validate_only_detects_artifact_tampering(tmp_path):
    cleaner = _load_module()
    source = _write_fixture_corpus(tmp_path / "source")
    output = tmp_path / "output"
    _build_dataset(cleaner, source, output, min_passage_chars=40, max_passage_chars=120)

    completed = subprocess.run(
        [
            sys.executable,
            str(SCRIPT_PATH),
            "--input",
            str(source),
            "--output",
            str(output),
            "--curation-policy",
            str(source / "curation_policy.json"),
            "--validate-only",
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, completed.stderr
    assert json.loads(completed.stdout)["status"] == "passed"

    with (output / "passages.ndjson").open("a", encoding="utf-8") as handle:
        handle.write("{}\n")
    with pytest.raises(cleaner.ClassicsDatasetError, match="hash 不一致"):
        _validate_dataset(cleaner, source, output)


def test_validator_rejects_self_consistent_hashes_when_passage_content_breaks_lineage(tmp_path):
    cleaner = _load_module()
    source = _write_fixture_corpus(tmp_path / "source")
    output = tmp_path / "output"
    _build_dataset(cleaner, source, output, min_passage_chars=40, max_passage_chars=120)

    passages = _read_ndjson(output / "passages.ndjson")
    passages[0]["text"] += "篡改"
    passages[0]["charCount"] = len(passages[0]["text"])
    passages[0]["textSha256"] = _sha256(passages[0]["text"].encode())
    _write_ndjson(output / "passages.ndjson", passages)
    _refresh_integrity_metadata(output)

    with pytest.raises(cleaner.ClassicsDatasetError, match="passage 与 body paragraph 内容不一致"):
        _validate_dataset(cleaner, source, output)


def test_validator_rejects_navigation_or_heading_paragraph_in_passage(tmp_path):
    cleaner = _load_module()
    source = _write_fixture_corpus(tmp_path / "source")
    output = tmp_path / "output"
    _build_dataset(cleaner, source, output, min_passage_chars=40, max_passage_chars=120)

    paragraphs = _read_ndjson(output / "paragraphs.ndjson")
    passages = _read_ndjson(output / "passages.ndjson")
    navigation = next(paragraph for paragraph in paragraphs if paragraph["paragraphType"] == "navigation")
    passage = next(item for item in passages if item["documentId"] == navigation["documentId"])
    passage["paragraphIds"].append(navigation["paragraphId"])
    passage["paragraphStart"] = min(passage["paragraphStart"], navigation["sequence"])
    passage["paragraphEnd"] = max(passage["paragraphEnd"], navigation["sequence"])
    passage["sourceLineStart"] = min(passage["sourceLineStart"], navigation["sourceLineStart"])
    passage["sourceLineEnd"] = max(passage["sourceLineEnd"], navigation["sourceLineEnd"])
    _write_ndjson(output / "passages.ndjson", passages)
    _refresh_integrity_metadata(output)

    with pytest.raises(cleaner.ClassicsDatasetError, match="跨标题边界或消费了非正文"):
        _validate_dataset(cleaner, source, output)


def test_validator_rejects_self_consistent_schema_version_drift(tmp_path):
    cleaner = _load_module()
    source = _write_fixture_corpus(tmp_path / "source")
    output = tmp_path / "output"
    _build_dataset(cleaner, source, output, min_passage_chars=40, max_passage_chars=120)

    paragraphs = _read_ndjson(output / "paragraphs.ndjson")
    paragraphs[0]["schemaVersion"] = "classics-clean-dataset.v2"
    _write_ndjson(output / "paragraphs.ndjson", paragraphs)
    _refresh_integrity_metadata(output)

    with pytest.raises(cleaner.ClassicsDatasetError, match="paragraph schemaVersion 错误"):
        _validate_dataset(cleaner, source, output)


def test_real_canonical_policy_removes_known_noncontent_and_preserves_sources(tmp_path):
    cleaner = _load_module()
    source = ROOT / "domains" / "fate-analysis" / "data-products" / "classics"
    output = tmp_path / "classics-clean-v3"
    source_hashes_before = {path.name: _sha256(path.read_bytes()) for path in source.glob("*.txt")}

    result = _build_dataset(cleaner, source, output)

    assert result["counts"] == {
        "documentCount": 14,
        "paragraphCount": 16079,
        "passageCount": 1430,
        "duplicateRecordCount": 484,
        "exclusionRecordCount": 146,
        "reviewItemCount": 21,
    }
    searchable_text = (output / "paragraphs.ndjson").read_text(encoding="utf-8") + (
        output / "passages.ndjson"
    ).read_text(encoding="utf-8")
    for marker in (
        "微信公众号",
        "2338856113",
        "ireadweek.com",
        "整理说明：本文件基于",
        "来源章节：https://ctext.org/",
        "抓取范围：",
        "千里命稿终",
        "滴天髓全文终",
        '"text":"---"',
    ):
        assert marker not in searchable_text

    documents = _read_ndjson(output / "documents.ndjson")
    assert sum(document["completeness"]["status"] == "partial" for document in documents) == 2
    ctext_documents = [document for document in documents if document["curationMetadata"].get("embeddedSourceUrl")]
    assert len(ctext_documents) == 6
    assert all(
        document["curationMetadata"]["embeddedSourceUrl"].startswith("https://ctext.org/")
        for document in ctext_documents
    )
    assert all(document["bibliography"]["reviewed"] is None for document in documents)
    quality = json.loads((output / "quality-report.json").read_text(encoding="utf-8"))
    assert quality["summary"]["semanticReplayErrorCount"] == 0
    assert quality["summary"]["passageHeadingBoundaryViolationCount"] == 0
    assert quality["summary"]["navigationPassageCount"] == 0
    assert quality["summary"]["paragraphTypeCounts"] == {
        "body": 14727,
        "document_title": 29,
        "heading": 865,
        "navigation": 458,
    }
    assert source_hashes_before == {path.name: _sha256(path.read_bytes()) for path in source.glob("*.txt")}


def test_contract_registry_and_documentation_wire_the_internal_dataset():
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    asset = next(item for item in registry["assets"] if item["id"] == "asset.classics.cleaned_internal")

    assert contract["rightsBoundary"] == {
        "distributionAllowed": False,
        "productionUseAllowed": False,
        "trainingUseAllowed": False,
        "requiredRightsStatus": "review_required",
        "allowedPurposes": ["internal_reference", "rule_index_seed", "human_review"],
    }
    assert asset["lifecycleLayer"] == "derived"
    assert asset["licensePolicy"]["productionUseAllowed"] is False
    assert asset["exportPolicy"]["allowedInPublicExport"] is False
    assert asset["productionEligibility"]["status"] == "review_required"

    assert "classics-dataset-clean.py" in (ROOT / "scripts" / "AGENTS.md").read_text(encoding="utf-8")
    assert "test_classics_dataset_clean.py" in (ROOT / "tests" / "AGENTS.md").read_text(encoding="utf-8")
    assert "tests/regression/test_classics_dataset_clean.py" in (ROOT / "scripts" / "local-ci.sh").read_text(
        encoding="utf-8"
    )
    classics_readme = ROOT / "domains" / "fate-analysis" / "data-products" / "classics" / "README.md"
    assert "classics-clean-v3" in classics_readme.read_text(encoding="utf-8")
