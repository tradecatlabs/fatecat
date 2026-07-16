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
            "甲乙丙丁\u00a0戊己。\r\n"
            "\r\n"
            "共同正文用于重复标记，不应删除。\r\n" + "这一段很长，用于验证切片不会丢字；" * 35
        ).encode("utf-8"),
        "乙书 - 乙作者.txt": ("序\n共同正文用于重复标记，不应删除。\n另一条正文。\u200b\n").encode("utf-8"),
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
    return corpus


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

    result_a = cleaner.build_dataset(input_dir=source, output_dir=output_a, min_passage_chars=40, max_passage_chars=120)
    result_b = cleaner.build_dataset(input_dir=source, output_dir=output_b, min_passage_chars=40, max_passage_chars=120)

    assert result_a["status"] == result_b["status"] == "passed"
    for filename in json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))["output"]["requiredFiles"]:
        assert (output_a / filename).read_bytes() == (output_b / filename).read_bytes()

    documents = _read_ndjson(output_a / "documents.ndjson")
    paragraphs = _read_ndjson(output_a / "paragraphs.ndjson")
    passages = _read_ndjson(output_a / "passages.ndjson")
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
    manifest = json.loads((output_a / "manifest.json").read_text(encoding="utf-8"))
    quality = json.loads((output_a / "quality-report.json").read_text(encoding="utf-8"))
    assert manifest["status"] == "passed"
    assert quality["summary"]["lineageErrorCount"] == 0
    assert quality["summary"]["invalidUtf8Count"] == 0


def test_normalization_removes_only_allowed_noise_and_preserves_duplicate_paragraphs(tmp_path):
    cleaner = _load_module()
    source = _write_fixture_corpus(tmp_path / "source")
    output = tmp_path / "output"

    cleaner.build_dataset(input_dir=source, output_dir=output, min_passage_chars=40, max_passage_chars=120)

    paragraphs = _read_ndjson(output / "paragraphs.ndjson")
    combined = "\n".join(record["text"] for record in paragraphs)
    assert "\ufeff" not in combined
    assert "\u200b" not in combined
    assert "\u00a0" not in combined
    assert "甲乙丙丁 戊己。" in combined
    repeated = [record for record in paragraphs if record["text"] == "共同正文用于重复标记，不应删除。"]
    assert len(repeated) == 2

    duplicate_records = _read_ndjson(output / "duplicates.ndjson")
    exact_groups = [record for record in duplicate_records if record["kind"] == "exact_paragraph_group"]
    assert any(record["occurrenceCount"] == 2 for record in exact_groups)
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
        cleaner.build_dataset(input_dir=source, output_dir=tmp_path / "output")


def test_cleaner_rejects_input_output_containment(tmp_path):
    cleaner = _load_module()
    source = _write_fixture_corpus(tmp_path / "source")

    with pytest.raises(cleaner.ClassicsDatasetError, match="互相包含"):
        cleaner.build_dataset(input_dir=source, output_dir=source / "derived")
    with pytest.raises(cleaner.ClassicsDatasetError, match="互相包含"):
        cleaner.build_dataset(input_dir=source, output_dir=source.parent)


def test_validate_only_detects_artifact_tampering(tmp_path):
    cleaner = _load_module()
    source = _write_fixture_corpus(tmp_path / "source")
    output = tmp_path / "output"
    cleaner.build_dataset(input_dir=source, output_dir=output, min_passage_chars=40, max_passage_chars=120)

    completed = subprocess.run(
        [
            sys.executable,
            str(SCRIPT_PATH),
            "--input",
            str(source),
            "--output",
            str(output),
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
        cleaner.validate_dataset(output, input_dir=source)


def test_validator_rejects_self_consistent_hashes_when_passage_content_breaks_lineage(tmp_path):
    cleaner = _load_module()
    source = _write_fixture_corpus(tmp_path / "source")
    output = tmp_path / "output"
    cleaner.build_dataset(input_dir=source, output_dir=output, min_passage_chars=40, max_passage_chars=120)

    passages = _read_ndjson(output / "passages.ndjson")
    passages[0]["text"] += "篡改"
    passages[0]["charCount"] = len(passages[0]["text"])
    passages[0]["textSha256"] = _sha256(passages[0]["text"].encode())
    _write_ndjson(output / "passages.ndjson", passages)
    _refresh_integrity_metadata(output)

    with pytest.raises(cleaner.ClassicsDatasetError, match="passage 与 paragraph 内容不一致"):
        cleaner.validate_dataset(output, input_dir=source)


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
    classics_readme = ROOT / "domains" / "fate-analysis" / "data-products" / "classics" / "README.md"
    assert "classics-clean-v1" in classics_readme.read_text(encoding="utf-8")
