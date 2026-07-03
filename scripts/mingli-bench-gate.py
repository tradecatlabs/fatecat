#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
import tempfile
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from types import ModuleType
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
FATE_CORE_SRC = REPO_ROOT / "domains" / "fate-analysis" / "services" / "fate-core" / "src"
DEFAULT_OUTPUT_JSON = (
    REPO_ROOT / "infra" / "runtime" / "local-state" / "exports" / "evaluations" / "mingli-bench-gate.json"
)
CONTRACT_PATH = REPO_ROOT / "contracts" / "fate" / "evaluations" / "mingli-bench-gate.json"
CORE_QUALITY_GATE_PATH = REPO_ROOT / "scripts" / "core-quality-corpus-gate.py"
EVALUATION_REGISTRY_PATH = REPO_ROOT / "contracts" / "fate" / "evaluations" / "registry.json"
DATA_SUPPLY_CHAIN_REGISTRY_PATH = REPO_ROOT / "contracts" / "fate" / "data-supply-chain" / "registry.json"
VENDOR_SOURCES_PATH = REPO_ROOT / "tools" / "reference-repos" / "vendor_sources.json"
MINGLI_DATA_PATH = REPO_ROOT / "tools" / "reference-repos" / "github" / "MingLi-Bench-main" / "data" / "data.json"


class MingLiBenchGateError(RuntimeError):
    """MingLi-Bench 聚合门禁发现阻断项。"""


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_script_module(path: Path, module_name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise MingLiBenchGateError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _append_check(
    checks: list[dict[str, Any]],
    findings: list[dict[str, Any]],
    name: str,
    ok: bool,
    details: str,
    *,
    severity: str = "block",
) -> None:
    checks.append({"name": name, "ok": ok, "details": details})
    if not ok:
        findings.append({"severity": severity, "name": name, "details": details})


def _repo_path(ref: str) -> Path:
    if Path(ref).is_absolute() or ".." in Path(ref).parts:
        raise MingLiBenchGateError(f"unsafe repo path: {ref}")
    return REPO_ROOT / ref


def _render(payload: Any) -> str:
    return json.dumps(payload, ensure_ascii=False, sort_keys=True)


def _benchmark_year(item: dict[str, Any]) -> int | None:
    question_number = int(item.get("question_number", 0) or 0)
    return 2022 + ((question_number - 1) // 40) if question_number > 0 else None


def _load_questions() -> list[dict[str, Any]]:
    payload = _load_json(MINGLI_DATA_PATH)
    questions = payload.get("questions")
    if not isinstance(questions, list):
        raise MingLiBenchGateError(f"MingLi-Bench 数据结构异常: {MINGLI_DATA_PATH}")
    return [item for item in questions if isinstance(item, dict)]


def _vendor_entry() -> dict[str, Any] | None:
    payload = _load_json(VENDOR_SOURCES_PATH)
    for scope in ("required", "optionalFutureFeatures", "legacyUnreviewedSnapshots"):
        for item in payload.get(scope, []):
            if isinstance(item, dict) and item.get("id") == "MingLi-Bench":
                return {**item, "_scope": scope}
    return None


def _registry_resource(registry: dict[str, Any], resource_id: str) -> dict[str, Any] | None:
    for item in registry.get("resources", []):
        if isinstance(item, dict) and item.get("id") == resource_id:
            return item
    return None


def _supply_chain_asset(asset_id: str) -> dict[str, Any] | None:
    registry = _load_json(DATA_SUPPLY_CHAIN_REGISTRY_PATH)
    for item in registry.get("assets", []):
        if isinstance(item, dict) and item.get("id") == asset_id:
            return item
    return None


def _core_corpus_summary(checks: list[dict[str, Any]], findings: list[dict[str, Any]]) -> dict[str, Any]:
    gate = _load_script_module(CORE_QUALITY_GATE_PATH, "fatecat_core_quality_gate_for_mingli")
    summary = gate.run_gate()
    _append_check(
        checks, findings, "core_corpus_gate_status", summary.get("status") == "passed", str(summary.get("status"))
    )
    return {
        "status": summary.get("status"),
        "corpusCount": summary.get("summary", {}).get("corpusCount"),
        "totalCaseCount": summary.get("summary", {}).get("totalCaseCount"),
        "manifest": summary.get("manifest"),
        "reportDiffPolicy": summary.get("reportDiffPolicy"),
        "privacyBoundary": "core corpus summary only; detailed fixture rows are not embedded",
    }


def _benchmark_stats(questions: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "dataset": "FortuneTellingBench",
        "totalQuestions": len(questions),
        "availableYears": sorted({year for item in questions if (year := _benchmark_year(item)) is not None}),
        "categories": dict(sorted(Counter(str(item.get("category", "未分类")) for item in questions).items())),
    }


def _generate_baseline(selected_year: int | None, sample_size: int) -> dict[str, Any]:
    if str(FATE_CORE_SRC) not in sys.path:
        sys.path.insert(0, str(FATE_CORE_SRC))
    from fate_core.evaluation import mingli_baseline  # noqa: PLC0415

    with tempfile.TemporaryDirectory(prefix="fatecat-mingli-gate-") as tmp_dir:
        predictions_path = Path(tmp_dir) / "predictions.jsonl"
        rows = mingli_baseline.generate_predictions(
            MINGLI_DATA_PATH,
            predictions_path,
            selected_year=selected_year,
            sample_size=sample_size,
        )

    questions = [item for item in _load_questions() if selected_year is None or _benchmark_year(item) == selected_year][
        :sample_size
    ]
    question_by_id = {str(item.get("id")): item for item in questions}
    answered = 0
    correct = 0
    by_category: dict[str, dict[str, Any]] = {}
    for row in rows:
        qid = str(row.get("question_id"))
        question = question_by_id.get(qid, {})
        category = str(row.get("category") or question.get("category") or "未分类")
        bucket = by_category.setdefault(category, {"total": 0, "answered": 0, "correct": 0})
        bucket["total"] += 1
        predicted = str(row.get("predicted_answer") or "")
        if predicted:
            answered += 1
            bucket["answered"] += 1
        if predicted and predicted == question.get("answer"):
            correct += 1
            bucket["correct"] += 1

    for bucket in by_category.values():
        bucket["accuracy"] = round(bucket["correct"] / bucket["answered"], 4) if bucket["answered"] else 0
    return {
        "sampleSize": sample_size,
        "selectedYear": selected_year,
        "answered": answered,
        "missing": len(rows) - answered,
        "correct": correct,
        "accuracy": round(correct / answered, 4) if answered else 0,
        "byCategory": dict(sorted(by_category.items())),
        "predictionSource": mingli_baseline.PREDICTION_SOURCE,
        "boundary": "FateCat weak-rule baseline aggregate only; no per-question outputs, benchmark answers or report bodies are stored.",
    }


def _validate_sources(contract: dict[str, Any], checks: list[dict[str, Any]], findings: list[dict[str, Any]]) -> None:
    for ref in contract.get("requiredLocalSources", []):
        path = _repo_path(str(ref))
        _append_check(checks, findings, f"source_exists:{ref}", path.exists(), "path exists")


def _validate_license_boundary(checks: list[dict[str, Any]], findings: list[dict[str, Any]]) -> dict[str, Any]:
    vendor = _vendor_entry()
    _append_check(checks, findings, "vendor_entry_exists", vendor is not None, "MingLi-Bench")
    if vendor is None:
        return {"status": "failed"}
    asset = _supply_chain_asset("asset.mingli_bench.offline")
    export_policy = asset.get("exportPolicy", {}) if asset else {}
    production = asset.get("productionEligibility", {}) if asset else {}
    _append_check(checks, findings, "supply_chain_asset_exists", asset is not None, "asset.mingli_bench.offline")
    _append_check(
        checks,
        findings,
        "vendor_usage_role",
        vendor.get("usageRole") == "evaluation_only",
        str(vendor.get("usageRole")),
    )
    _append_check(
        checks,
        findings,
        "vendor_not_production",
        vendor.get("productionUseAllowed") is False,
        str(vendor.get("productionUseAllowed")),
    )
    _append_check(
        checks, findings, "vendor_license_spdx", vendor.get("licenseStatus") == "spdx", str(vendor.get("licenseStatus"))
    )
    _append_check(
        checks,
        findings,
        "asset_export_blocked",
        export_policy.get("allowedInPublicExport") is False,
        str(export_policy.get("allowedInPublicExport")),
    )
    _append_check(
        checks,
        findings,
        "asset_production_evaluation_only",
        production.get("status") == "evaluation_only",
        str(production.get("status")),
    )
    return {
        "license": vendor.get("license"),
        "licenseStatus": vendor.get("licenseStatus"),
        "usageRole": vendor.get("usageRole"),
        "distributionAllowed": vendor.get("distributionAllowed"),
        "productionUseAllowed": vendor.get("productionUseAllowed"),
        "vendorRevision": vendor.get("revision"),
        "vendorRevisionStatus": vendor.get("revisionStatus"),
        "assetExportStatus": export_policy.get("status"),
        "assetProductionStatus": production.get("status"),
    }


def _validate_evaluation_boundary(checks: list[dict[str, Any]], findings: list[dict[str, Any]]) -> dict[str, Any]:
    registry = _load_json(EVALUATION_REGISTRY_PATH)
    dataset = _registry_resource(registry, "dataset.mingli_bench_offline")
    run = _registry_resource(registry, "run.mingli_bench_offline")
    _append_check(checks, findings, "evaluation_dataset_exists", dataset is not None, "dataset.mingli_bench_offline")
    _append_check(checks, findings, "evaluation_run_exists", run is not None, "run.mingli_bench_offline")
    if dataset is not None:
        _append_check(
            checks,
            findings,
            "dataset_evaluation_only",
            dataset.get("usageRole") == "evaluation_only",
            str(dataset.get("usageRole")),
        )
        _append_check(
            checks,
            findings,
            "dataset_requires_reference_repo",
            dataset.get("localAvailability") == "requires_reference_repo",
            str(dataset.get("localAvailability")),
        )
    if run is not None:
        _append_check(checks, findings, "run_optional", run.get("gateType") == "optional", str(run.get("gateType")))
        _append_check(
            checks,
            findings,
            "run_not_release_required",
            run.get("releaseRequired") is False,
            str(run.get("releaseRequired")),
        )
    return {
        "datasetId": dataset.get("id") if dataset else None,
        "runId": run.get("id") if run else None,
        "usageRole": dataset.get("usageRole") if dataset else None,
        "runGateType": run.get("gateType") if run else None,
        "releaseRequired": run.get("releaseRequired") if run else None,
        "externalConnectivity": "not_required_for_offline_stats",
    }


def _assert_no_leak(summary: dict[str, Any], contract: dict[str, Any]) -> dict[str, Any]:
    rendered = _render(summary)
    forbidden = [fragment for fragment in contract.get("forbiddenReportFragments", []) if str(fragment) in rendered]
    if forbidden:
        raise MingLiBenchGateError(f"MingLi-Bench gate summary contains forbidden fragments: {', '.join(forbidden)}")
    return {
        "status": "passed",
        "checkedFragments": len(contract.get("forbiddenReportFragments", [])),
        "policy": "summary-only aggregate; no question text, birth info, standard answers, per-question results or report bodies",
    }


def run_gate(*, selected_year: int | None = 2025, sample_size: int = 5) -> dict[str, Any]:
    contract = _load_json(CONTRACT_PATH)
    checks: list[dict[str, Any]] = []
    findings: list[dict[str, Any]] = []
    _append_check(
        checks,
        findings,
        "contract_kind",
        contract.get("reportKind") == "fatecat.mingli_bench_gate",
        str(contract.get("reportKind")),
    )
    _validate_sources(contract, checks, findings)
    core_corpus = _core_corpus_summary(checks, findings)
    questions = _load_questions()
    benchmark = _benchmark_stats(questions)
    benchmark["sample"] = {"selectedYear": selected_year, "sampleSize": sample_size}
    benchmark["baseline"] = _generate_baseline(selected_year, sample_size)
    _append_check(
        checks,
        findings,
        "benchmark_total_questions",
        benchmark["totalQuestions"] >= 160,
        str(benchmark["totalQuestions"]),
    )
    _append_check(
        checks,
        findings,
        "benchmark_baseline_answered",
        benchmark["baseline"]["answered"] == sample_size,
        str(benchmark["baseline"]["answered"]),
    )
    license_boundary = _validate_license_boundary(checks, findings)
    evaluation_boundary = _validate_evaluation_boundary(checks, findings)
    summary: dict[str, Any] = {
        "schemaVersion": 1,
        "generatedAt": datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "kind": "fatecat.mingli_bench_gate",
        "status": "failed" if findings else "passed",
        "coreCorpus": core_corpus,
        "benchmark": benchmark,
        "licenseBoundary": license_boundary,
        "evaluationBoundary": evaluation_boundary,
        "checks": checks,
        "findings": findings,
        "privacyBoundary": "MingLi-Bench gate 只输出聚合统计、license/usage 边界和 baseline 汇总；不得保存题目、出生信息、标准答案、逐题结果、报告正文、token、secret 或 DSN。",
        "limits": [
            "不调用外部模型 API。",
            "不把 benchmark 标准答案注入 production provider。",
            "不证明外部专家人工准确率。",
            "不自动同步 MingLi-Bench 上游 HEAD。",
        ],
    }
    summary["noLeak"] = _assert_no_leak(summary, contract)
    return summary


def write_summary(summary: dict[str, Any], output_json: Path) -> None:
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="执行 FateCat MingLi-Bench 离线聚合门禁。")
    parser.add_argument("--year", type=int, default=2025, help="用于 FateCat baseline smoke 的 benchmark 年份。")
    parser.add_argument("--sample", type=int, default=5, help="用于 FateCat baseline smoke 的样本数。")
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON, help="summary JSON 输出路径。")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        summary = run_gate(selected_year=args.year, sample_size=args.sample)
        write_summary(summary, args.output_json)
        print(
            json.dumps(
                {
                    "status": summary["status"],
                    "totalQuestions": summary["benchmark"]["totalQuestions"],
                    "sampleSize": summary["benchmark"]["baseline"]["sampleSize"],
                    "answered": summary["benchmark"]["baseline"]["answered"],
                    "accuracy": summary["benchmark"]["baseline"]["accuracy"],
                    "findings": len(summary["findings"]),
                },
                ensure_ascii=False,
            )
        )
        return 0 if summary["status"] == "passed" else 1
    except (MingLiBenchGateError, OSError, json.JSONDecodeError) as exc:
        print(f"MingLi-Bench gate error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
