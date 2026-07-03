from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GATE_PATH = ROOT / "scripts" / "mingli-bench-gate.py"
CONTRACT_PATH = ROOT / "contracts" / "fate" / "evaluations" / "mingli-bench-gate.json"


def _load_gate():
    spec = importlib.util.spec_from_file_location("fatecat_mingli_bench_gate", GATE_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_mingli_bench_gate_writes_redacted_aggregate_summary(tmp_path):
    gate = _load_gate()
    output_json = tmp_path / "mingli-bench-gate.json"

    exit_code = gate.main(["--year", "2025", "--sample", "3", "--output-json", str(output_json)])

    assert exit_code == 0
    stored = json.loads(output_json.read_text(encoding="utf-8"))
    assert stored["kind"] == "fatecat.mingli_bench_gate"
    assert stored["status"] == "passed"
    assert stored["coreCorpus"]["status"] == "passed"
    assert stored["benchmark"]["dataset"] == "FortuneTellingBench"
    assert stored["benchmark"]["totalQuestions"] >= 160
    assert stored["benchmark"]["baseline"]["sampleSize"] == 3
    assert stored["benchmark"]["baseline"]["answered"] == 3
    assert stored["licenseBoundary"]["usageRole"] == "evaluation_only"
    assert stored["licenseBoundary"]["productionUseAllowed"] is False
    assert stored["evaluationBoundary"]["releaseRequired"] is False
    assert stored["noLeak"]["status"] == "passed"


def test_mingli_bench_gate_contract_forbids_detail_leakage():
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    gate = _load_gate()

    assert contract["reportKind"] == "fatecat.mingli_bench_gate"
    assert '"answer"' in contract["forbiddenReportFragments"]
    assert "tools/reference-repos/github/MingLi-Bench-main/data/data.json" in contract["requiredLocalSources"]

    summary = gate.run_gate(selected_year=2025, sample_size=2)
    rendered = json.dumps(summary, ensure_ascii=False)
    for fragment in contract["forbiddenReportFragments"]:
        assert fragment not in rendered
