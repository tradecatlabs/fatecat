from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_mingli_bench_evaluation_smoke_computes_accuracy(tmp_path):
    predictions = tmp_path / "predictions.jsonl"
    output_json = tmp_path / "evaluation.json"
    rows = [
        {"question_id": "ftb_0001", "predicted_answer": "A"},
        {"question_id": "ftb_0002", "predicted_answer": "C"},
        {"question_id": "ftb_0003", "predicted_answer": "C"},
        {"question_id": "ftb_0004", "predicted_answer": "C"},
        {"question_id": "ftb_0005", "predicted_answer": "B"},
    ]
    predictions.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n", encoding="utf-8")

    subprocess.run(
        [
            "bash",
            "scripts/run-mingli-bench.sh",
            "--sample",
            "5",
            "--predictions-file",
            str(predictions),
            "--output-json",
            str(output_json),
        ],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )

    report = json.loads(output_json.read_text(encoding="utf-8"))
    assert report["evaluation"]["total"] == 5
    assert report["evaluation"]["answered"] == 5
    assert report["evaluation"]["correct"] == 5
    assert report["evaluation"]["accuracy"] == 1.0


def test_mingli_bench_predictions_can_be_generated_from_fatecat(tmp_path):
    predictions = tmp_path / "fatecat-predictions.jsonl"
    output_json = tmp_path / "evaluation.json"

    generated = subprocess.run(
        [
            "bash",
            "scripts/generate-mingli-predictions.sh",
            "--year",
            "2025",
            "--sample",
            "2",
            "--output-jsonl",
            str(predictions),
        ],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    payload = json.loads(generated.stdout)
    assert payload["predictions"] == 2
    assert payload["source"] == "fatecat_scored_baseline_v1"

    rows = [json.loads(line) for line in predictions.read_text(encoding="utf-8").splitlines()]
    assert len(rows) == 2
    assert {row["prediction_source"] for row in rows} == {"fatecat_scored_baseline_v1"}
    assert all(row["fatecat_evidence"]["fourPillars"] for row in rows)
    assert all(row["scoring_trace"]["optionScores"] for row in rows)
    assert all(row["scoring_trace"]["boundary"] for row in rows)
    assert all(row["predicted_answer"] in {"A", "B", "C", "D"} for row in rows)

    subprocess.run(
        [
            "bash",
            "scripts/run-mingli-bench.sh",
            "--year",
            "2025",
            "--sample",
            "2",
            "--predictions-file",
            str(predictions),
            "--output-json",
            str(output_json),
        ],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    report = json.loads(output_json.read_text(encoding="utf-8"))
    assert report["evaluation"]["total"] == 2
    assert report["evaluation"]["answered"] == 2
    assert 0 <= report["evaluation"]["accuracy"] <= 1


def test_mingli_baseline_reuses_chart_for_same_birth_input(tmp_path, monkeypatch):
    from fate_core.evaluation import mingli_baseline

    data_path = tmp_path / "data.json"
    output_jsonl = tmp_path / "predictions.jsonl"
    birth_info = {
        "year": 1990,
        "month": 5,
        "day": 6,
        "hour": 7,
        "minute": 30,
        "gender": "female",
        "location": "香港",
    }
    options = [
        {"letter": "A", "text": "严重健康问题"},
        {"letter": "B", "text": "平安"},
        {"letter": "C", "text": "普通公司"},
        {"letter": "D", "text": "富裕"},
    ]
    data_path.write_text(
        json.dumps(
            {
                "questions": [
                    {
                        "id": "ftb_cache_001",
                        "question_number": 1,
                        "category": "健康",
                        "birth_info": birth_info,
                        "options": options,
                        "answer": "A",
                    },
                    {
                        "id": "ftb_cache_002",
                        "question_number": 2,
                        "category": "健康",
                        "birth_info": birth_info,
                        "options": options,
                        "answer": "B",
                    },
                ]
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    calls = []

    def fake_calculate(input_payload):
        calls.append(input_payload)
        return {
            "fourPillars": {"year": "庚午", "month": "辛巳", "day": "壬申", "hour": "甲辰"},
            "dayMaster": {"stem": "壬", "element": "水"},
            "baziRuleDepth": {"registryVersion": "test"},
            "baziBenchmark": {
                "topicProfiles": [{"topic": "健康", "score": 80}],
                "fortuneTriggers": [],
            },
        }

    monkeypatch.setattr(mingli_baseline, "calculate_pure_analysis", fake_calculate)

    rows = mingli_baseline.generate_predictions(data_path, output_jsonl)
    written_rows = [json.loads(line) for line in output_jsonl.read_text(encoding="utf-8").splitlines()]

    assert len(calls) == 1
    assert len(rows) == 2
    assert written_rows == rows
    assert all(row["predicted_answer"] in {"A", "B", "C", "D"} for row in rows)
    forbidden_leakage_fields = {"expected", "answer", "correct", "gold", "label"}
    assert all(forbidden_leakage_fields.isdisjoint(row) for row in rows)


def test_mingli_relation_pressure_reads_canonical_branch_relations():
    from fate_core.evaluation.mingli_baseline import _relation_pressure

    result = {
        "branchRelations": {
            "canonical": [
                {"relation": "冲"},
                {"relation": "刑"},
                {"relation": "害"},
                {"relation": "破"},
                {"relation": "六合"},
            ]
        }
    }

    assert _relation_pressure(result) == 4 / 12
