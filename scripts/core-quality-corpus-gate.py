#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
CONTRACT_ROOT = REPO_ROOT / "contracts" / "fate" / "evaluations"
DEFAULT_MANIFEST = CONTRACT_ROOT / "core-quality-corpus.json"
DEFAULT_POLICY = CONTRACT_ROOT / "report-diff-policy.json"
DEFAULT_REGISTRY = CONTRACT_ROOT / "registry.json"
DEFAULT_OUTPUT_JSON = (
    REPO_ROOT / "infra" / "runtime" / "local-state" / "exports" / "quality" / "core-quality-corpus-gate.json"
)


class CoreQualityCorpusGateError(RuntimeError):
    """核心质量语料门禁失败。"""


def _load_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise CoreQualityCorpusGateError(f"缺少文件: {path}") from exc
    except json.JSONDecodeError as exc:
        raise CoreQualityCorpusGateError(f"JSON 格式错误: {path}: {exc}") from exc


def _rel(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def _repo_path(value: str) -> Path:
    return (REPO_ROOT / value).resolve()


def _birth_place(input_payload: dict[str, Any]) -> str | None:
    value = input_payload.get("birthPlace")
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        nested = value.get("name")
        return str(nested) if nested is not None else None
    return None


def _append_check(checks: list[dict[str, Any]], name: str, ok: bool, details: str) -> None:
    checks.append({"name": name, "ok": ok, "details": details})


def _require(checks: list[dict[str, Any]], name: str, condition: bool, details: str) -> None:
    _append_check(checks, name, condition, details)
    if not condition:
        raise CoreQualityCorpusGateError(f"{name}: {details}")


def _validate_registry(
    manifest: dict[str, Any], policy: dict[str, Any], registry: dict[str, Any]
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    resources = {
        item["id"]: item for item in registry.get("resources", []) if isinstance(item, dict) and item.get("id")
    }
    dataset_ids = {item["datasetId"] for item in manifest["corpora"]}
    _require(
        checks,
        "registry:core_quality_manifest",
        registry["metadata"].get("coreQualityCorpusManifest") == _rel(DEFAULT_MANIFEST),
        str(registry["metadata"].get("coreQualityCorpusManifest")),
    )
    _require(
        checks,
        "registry:report_diff_policy",
        registry["metadata"].get("reportDiffPolicy") == _rel(DEFAULT_POLICY),
        str(registry["metadata"].get("reportDiffPolicy")),
    )
    _require(
        checks,
        "registry:gate_command",
        registry["metadata"].get("coreQualityCorpusGateCommand") == manifest["releaseGate"]["command"],
        str(registry["metadata"].get("coreQualityCorpusGateCommand")),
    )
    for dataset_id in sorted(dataset_ids):
        _require(checks, f"registry:dataset:{dataset_id}", dataset_id in resources, "registered")
    _require(
        checks,
        "policy:threshold:bazi",
        int(policy["thresholds"]["minBaziGoldenCases"]) >= 300,
        str(policy["thresholds"].get("minBaziGoldenCases")),
    )
    _require(
        checks,
        "policy:threshold:ziwei",
        int(policy["thresholds"]["minZiweiGoldenCases"]) >= 8,
        str(policy["thresholds"].get("minZiweiGoldenCases")),
    )
    structural = policy.get("structuralDiff", {})
    _require(checks, "policy:structural_diff:summary_only", structural.get("summaryOnly") is True, str(structural))
    _require(
        checks,
        "policy:structural_diff:required_fields",
        set(manifest["reportDiffPolicy"]["requiredStructuralSummary"])
        <= set(structural.get("requiredSummaryFields", [])),
        str(structural.get("requiredSummaryFields")),
    )
    forbidden = set(structural.get("forbiddenStoredFields", []))
    _require(
        checks,
        "policy:structural_diff:no_full_body",
        set(manifest["reportDiffPolicy"]["forbiddenStoredFields"]) <= forbidden,
        str(sorted(forbidden)),
    )
    for profile_id, profile in policy["profiles"].items():
        minimum = structural.get("profileMinimums", {}).get(profile_id, {})
        structure = profile["structurePolicy"]
        _require(
            checks,
            f"policy:structural_diff:{profile_id}:headings",
            len(structure["requiredTopLevelHeadings"]) >= int(minimum.get("minRequiredTopLevelHeadings", 0)),
            str(len(structure["requiredTopLevelHeadings"])),
        )
        _require(
            checks,
            f"policy:structural_diff:{profile_id}:core_blocks",
            len(structure["requiredCoreBlocks"]) >= int(minimum.get("minRequiredCoreBlocks", 0)),
            str(len(structure["requiredCoreBlocks"])),
        )
        _require(
            checks,
            f"policy:structural_diff:{profile_id}:forbidden_blocks",
            len(structure["forbiddenDefaultBlocks"]) >= int(minimum.get("forbiddenDefaultBlockCountMin", 0)),
            str(len(structure["forbiddenDefaultBlocks"])),
        )
    return checks


def _validate_corpus(corpus: dict[str, Any]) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    path = _repo_path(str(corpus["path"]))
    _require(checks, "path_exists", path.exists(), _rel(path))
    data = _load_json(path)
    cases = data.get("cases")
    _require(checks, "cases:list", isinstance(cases, list), "cases must be list")
    cases = cases or []
    _require(
        checks, "case_count", len(cases) >= int(corpus["minCaseCount"]), f"{len(cases)} >= {corpus['minCaseCount']}"
    )
    _require(checks, "usage_role", corpus["usageRole"] == "evaluation_only", corpus["usageRole"])
    _require(checks, "privacy_class", corpus["privacyClass"] == "anonymous_fixture", corpus["privacyClass"])
    _require(checks, "source", data.get("source") == corpus["source"], str(data.get("source")))
    required_fields = set(corpus["requiredInputFields"])
    required_place = str(corpus["requiredBirthPlace"])
    required_tags = set(corpus.get("requiredCoverageTags", []))
    fixture_required_tags = set((data.get("coverageRequirements") or {}).get("requiredTags", []))
    if required_tags or fixture_required_tags:
        observed_tags = {str(tag) for case in cases for tag in case.get("coverageTags", [])}
        _require(
            checks,
            "coverage_tags",
            (required_tags | fixture_required_tags) <= observed_tags,
            str(sorted((required_tags | fixture_required_tags) - observed_tags)),
        )
    ids: set[str] = set()
    for index, case in enumerate(cases):
        case_id = str(case.get("id") or "")
        _require(checks, f"case:{index}:id", bool(case_id), "id present")
        _require(checks, f"case:{case_id}:unique", case_id not in ids, "unique")
        ids.add(case_id)
        input_payload = case.get("input")
        _require(checks, f"case:{case_id}:input", isinstance(input_payload, dict), "input present")
        missing = sorted(required_fields - set(input_payload or {}))
        _require(checks, f"case:{case_id}:required_input_fields", not missing, str(missing))
        if required_tags or fixture_required_tags:
            tags = case.get("coverageTags")
            _require(
                checks,
                f"case:{case_id}:coverage_tags",
                isinstance(tags, list) and all(isinstance(tag, str) and tag for tag in tags),
                str(tags),
            )
        _require(
            checks,
            f"case:{case_id}:birth_place",
            _birth_place(input_payload or {}) == required_place,
            str(_birth_place(input_payload or {})),
        )
        _require(checks, f"case:{case_id}:expected", isinstance(case.get("expected"), dict), "expected present")
    return {
        "id": corpus["id"],
        "capabilityId": corpus["capabilityId"],
        "path": corpus["path"],
        "caseCount": len(cases),
        "minCaseCount": corpus["minCaseCount"],
        "coverageTagCount": len({str(tag) for case in cases for tag in case.get("coverageTags", [])}),
        "checks": checks,
    }


def run_gate(
    *,
    manifest_path: Path = DEFAULT_MANIFEST,
    policy_path: Path = DEFAULT_POLICY,
    registry_path: Path = DEFAULT_REGISTRY,
) -> dict[str, Any]:
    manifest = _load_json(manifest_path)
    policy = _load_json(policy_path)
    registry = _load_json(registry_path)
    checks: list[dict[str, Any]] = []

    _require(checks, "manifest:schema", manifest.get("schemaVersion") == 1, str(manifest.get("schemaVersion")))
    _require(checks, "manifest:kind", manifest.get("kind") == "fatecat.core_quality_corpus", str(manifest.get("kind")))
    _require(
        checks,
        "manifest:release_gate",
        manifest["releaseGate"].get("required") is True,
        str(manifest["releaseGate"].get("required")),
    )
    _require(checks, "policy:schema", policy.get("schemaVersion") == 1, str(policy.get("schemaVersion")))
    _require(checks, "policy:kind", policy.get("kind") == "fatecat.report_diff_policy", str(policy.get("kind")))
    _require(
        checks,
        "policy:default_report",
        policy["invariants"].get("defaultReportSystem") == "bazi",
        str(policy["invariants"].get("defaultReportSystem")),
    )
    _require(
        checks,
        "policy:forbidden_ziwei_in_bazi",
        "紫微斗数" in policy["profiles"]["bazi"]["structurePolicy"]["forbiddenDefaultBlocks"],
        "ziwei blocked from bazi default",
    )
    _require(
        checks,
        "policy:forbidden_bazi_in_ziwei",
        "八字排盘详情" in policy["profiles"]["ziwei"]["structurePolicy"]["forbiddenDefaultBlocks"],
        "bazi blocked from ziwei profile",
    )

    registry_checks = _validate_registry(manifest, policy, registry)
    checks.extend(registry_checks)

    corpus_results = [_validate_corpus(corpus) for corpus in manifest["corpora"]]
    for result in corpus_results:
        checks.extend(
            {"name": f"{result['id']}:{item['name']}", "ok": item["ok"], "details": item["details"]}
            for item in result["checks"]
        )

    failed = [item for item in checks if not item["ok"]]
    return {
        "schemaVersion": 1,
        "kind": "fatecat.core_quality_corpus_gate",
        "generatedAt": datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "status": "failed" if failed else "passed",
        "manifest": _rel(manifest_path),
        "reportDiffPolicy": _rel(policy_path),
        "registry": _rel(registry_path),
        "summary": {
            "corpusCount": len(corpus_results),
            "totalCaseCount": sum(int(item["caseCount"]) for item in corpus_results),
            "failedCheckCount": len(failed),
        },
        "corpora": corpus_results,
        "checks": checks,
        "privacyBoundary": manifest["privacyBoundary"],
        "productionBoundary": manifest["productionBoundary"],
        "limits": manifest["limitations"],
    }


def write_summary(summary: dict[str, Any], output_json: Path) -> None:
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="校验八字/紫微核心质量语料 manifest 与完整报告 diff 策略。")
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST, help="核心质量语料 manifest 路径。")
    parser.add_argument("--report-diff-policy", type=Path, default=DEFAULT_POLICY, help="完整报告 diff 策略路径。")
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY, help="evaluation registry 路径。")
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON, help="输出 gate summary JSON。")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        summary = run_gate(
            manifest_path=args.manifest, policy_path=args.report_diff_policy, registry_path=args.registry
        )
        write_summary(summary, args.output_json)
        print(
            json.dumps(
                {
                    "status": summary["status"],
                    "corpusCount": summary["summary"]["corpusCount"],
                    "totalCaseCount": summary["summary"]["totalCaseCount"],
                },
                ensure_ascii=False,
            )
        )
        return 0 if summary["status"] == "passed" else 1
    except CoreQualityCorpusGateError as exc:
        error_summary = {
            "schemaVersion": 1,
            "kind": "fatecat.core_quality_corpus_gate",
            "generatedAt": datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
            "status": "failed",
            "error": str(exc),
        }
        write_summary(error_summary, args.output_json)
        print(f"core quality corpus gate error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
