from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT_PATH = ROOT / "scripts" / "core-quality-human-review-gate.py"
CONTRACT_PATH = ROOT / "contracts" / "fate" / "evaluations" / "core-quality-human-review-gate.json"
RUBRIC_PATH = ROOT / "contracts" / "fate" / "evaluations" / "professional-quality-rubric.json"


def _load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _review_bundle(*, commit: str = "a" * 40) -> dict:
    rubric = json.loads(RUBRIC_PATH.read_text(encoding="utf-8"))
    dimensions = []
    for index, item in enumerate(rubric["dimensions"]):
        dimensions.append(
            {
                "id": item["id"],
                "decision": "pass_with_findings" if index == 0 else "pass",
                "evidenceRef": f"review-artifact:dimension-{index:02d}",
                "artifactSha256": f"{index + 1:064x}"[-64:],
                "findingCount": 1 if index == 0 else 0,
            }
        )
    return {
        "schemaVersion": 1,
        "kind": "fatecat.core_quality_human_review_bundle",
        "source": {
            "commit": commit,
            "rubricVersion": "professional-quality-rubric.v1",
            "coreQualityCorpusManifest": "contracts/fate/evaluations/core-quality-corpus.json",
            "mingliBenchGateReportRef": "ci-artifact:mingli-bench-gate-summary",
        },
        "reviewer": {
            "reviewerRole": "domain_expert",
            "reviewerRef": "review-artifact:expert-ref-redacted",
            "signedAt": "2026-07-04T00:00:00Z",
            "signedReviewArtifactSha256": "b" * 64,
        },
        "professionalReview": {
            "decision": "accepted_with_findings",
            "dimensions": dimensions,
        },
        "externalBenchmark": {
            "decision": "accepted",
            "benchmarkRef": "benchmark-artifact:external-benchmark-aggregate",
            "aggregateArtifactSha256": "c" * 64,
            "sampleCount": 120,
            "accuracy": 0.73,
            "noPerQuestionLeak": True,
        },
        "noLeakReview": {
            "decision": "passed",
            "privacyScanArtifactSha256": "d" * 64,
            "forbiddenFragmentsFound": 0,
            "redactionStatus": "redacted_no_secret_values",
        },
        "reviewedArtifacts": [
            {"id": "professional-quality-rubric", "kind": "fatecat.professional_quality_rubric", "sha256": "e" * 64},
            {"id": "core-quality-corpus-gate", "kind": "fatecat.core_quality_corpus_gate", "sha256": "f" * 64},
            {"id": "mingli-bench-gate", "kind": "fatecat.mingli_bench_gate", "sha256": "1" * 64},
            {"id": "evidence-coverage-trend-gate", "kind": "fatecat.evidence_coverage_trend_gate", "sha256": "2" * 64},
            {"id": "bazi-ziwei-l4-golden-smoke", "kind": "fatecat.bazi_ziwei_l4_golden_smoke", "sha256": "3" * 64},
        ],
        "privacyBoundary": "redacted_no_secret_values",
    }


def test_core_quality_human_review_contract_lists_boundaries() -> None:
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))

    assert contract["kind"] == "fatecat.core_quality_human_review_contract"
    assert contract["inputKind"] == "fatecat.core_quality_human_review_bundle"
    assert contract["outputKind"] == "fatecat.core_quality_human_review_gate"
    assert "coreQualityHumanReview" in contract["requiredOutputFields"]
    assert "externalBenchmarkGate" in contract["requiredOutputFields"]
    assert "noLeakGate" in contract["requiredOutputFields"]
    assert "https://" in contract["forbiddenReportFragments"]
    assert "Does not mean bazi/ziwei professional quality is 100% proven." in contract["nonClaims"]


def test_core_quality_human_review_gate_defaults_to_external_pending() -> None:
    module = _load_module(SCRIPT_PATH, "fatecat_core_quality_human_review_gate_pending")

    gate = module.build_gate(expected_commit="a" * 40)

    assert gate["kind"] == "fatecat.core_quality_human_review_gate"
    assert gate["status"] == "passed"
    assert gate["humanReviewStatus"] == "external_review_pending"
    assert gate["externalBenchmarkStatus"] == "external_benchmark_pending"
    assert gate["noLeakReviewStatus"] == "external_no_leak_review_pending"
    assert gate["humanReviewGate"]["status"] == "blocked"
    assert gate["shipGate"]["status"] == "blocked"
    assert gate["summary"]["pendingReviews"] == 1


def test_core_quality_human_review_gate_accepts_redacted_bundle(tmp_path: Path) -> None:
    module = _load_module(SCRIPT_PATH, "fatecat_core_quality_human_review_gate_accepted")
    bundle_json = tmp_path / "core-quality-review.json"
    _write_json(bundle_json, _review_bundle())

    gate = module.build_gate(review_evidence_json=bundle_json, expected_commit="a" * 40)
    serialized = json.dumps(gate, ensure_ascii=False, sort_keys=True)

    assert gate["humanReviewGate"]["status"] == "passed"
    assert gate["externalBenchmarkGate"]["status"] == "passed"
    assert gate["noLeakGate"]["status"] == "passed"
    assert gate["summary"]["acceptedReviews"] == 1
    assert gate["summary"]["reviewedDimensions"] >= 8
    assert gate["source"]["reviewEvidenceBundleSha256"] == _sha256_file(bundle_json)
    assert "https://" not in serialized
    assert f"to{'ken'}=" not in serialized.lower()
    assert '"question"' not in serialized
    assert '"answer"' not in serialized


def test_core_quality_human_review_gate_rejects_raw_url_sensitive_commit_mismatch_and_missing_dimension(
    tmp_path: Path,
) -> None:
    module = _load_module(SCRIPT_PATH, "fatecat_core_quality_human_review_gate_negative")

    bundle = _review_bundle()
    bundle["reviewer"]["reviewerRef"] = "https://example.invalid/reviewer"
    bundle_json = tmp_path / "url.json"
    _write_json(bundle_json, bundle)
    assert module.main(["--review-evidence-json", str(bundle_json), "--expected-commit", "a" * 40]) == 1

    bundle = _review_bundle()
    bundle["reviewer"]["reviewerRef"] = f"to{'ken'}=redacted"
    bundle_json = tmp_path / "secret.json"
    _write_json(bundle_json, bundle)
    assert module.main(["--review-evidence-json", str(bundle_json), "--expected-commit", "a" * 40]) == 1

    bundle = _review_bundle(commit="b" * 40)
    bundle_json = tmp_path / "commit.json"
    _write_json(bundle_json, bundle)
    assert module.main(["--review-evidence-json", str(bundle_json), "--expected-commit", "a" * 40]) == 1

    bundle = _review_bundle()
    bundle["professionalReview"]["dimensions"].pop()
    bundle_json = tmp_path / "missing-dimension.json"
    _write_json(bundle_json, bundle)
    assert module.main(["--review-evidence-json", str(bundle_json), "--expected-commit", "a" * 40]) == 1


def test_core_quality_human_review_gate_cli_outputs_summary(tmp_path: Path) -> None:
    bundle_json = tmp_path / "core-quality-review.json"
    output_json = tmp_path / "core-quality-human-review-gate.json"
    _write_json(bundle_json, _review_bundle())

    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT_PATH),
            "--review-evidence-json",
            str(bundle_json),
            "--output-json",
            str(output_json),
            "--expected-commit",
            "a" * 40,
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    cli_summary = json.loads(result.stdout)

    assert cli_summary["kind"] == "fatecat.core_quality_human_review_gate"
    assert cli_summary["humanReviewGate"] == "passed"
    assert cli_summary["externalBenchmarkGate"] == "passed"
    assert cli_summary["noLeakGate"] == "passed"
    assert cli_summary["shipGate"] == "blocked"
    assert output_json.is_file()


def test_core_quality_human_review_gate_wiring_mentions_local_ci_docs_registry_and_certification() -> None:
    local_ci = (ROOT / "scripts" / "local-ci.sh").read_text(encoding="utf-8")
    scripts_agents = (ROOT / "scripts" / "AGENTS.md").read_text(encoding="utf-8")
    eval_agents = (ROOT / "contracts" / "fate" / "evaluations" / "AGENTS.md").read_text(encoding="utf-8")
    tests_agents = (ROOT / "tests" / "AGENTS.md").read_text(encoding="utf-8")
    registry = (ROOT / "contracts" / "fate" / "evaluations" / "registry.json").read_text(encoding="utf-8")
    certification = (ROOT / "scripts" / "measurement-infrastructure-certification.py").read_text(encoding="utf-8")
    roadmap = (ROOT / "docs" / "reference-materials" / "roadmap" / "测算基础设施100%实现计划.md").read_text(
        encoding="utf-8"
    )

    assert "core quality human review gate" in local_ci
    assert "FATE_LOCAL_CI_CORE_QUALITY_HUMAN_REVIEW_GATE" in local_ci
    assert "core-quality-human-review-gate.py" in scripts_agents
    assert "core-quality-human-review-gate.json" in eval_agents
    assert "test_core_quality_human_review_gate.py" in tests_agents
    assert "run.core_quality_human_review_gate" in registry
    assert "core-quality-human-review-gate.json" in certification
    assert "Core quality human review evidence intake" in roadmap
