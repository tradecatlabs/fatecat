from __future__ import annotations

import argparse
import hashlib
import json
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from fate_core.usecases import PureAnalysisInput, calculate_pure_analysis

PREDICTION_SOURCE = "fatecat_scored_baseline_v1"
LETTERS = ("A", "B", "C", "D")

LOCATION_COORDS: dict[str, tuple[float, float]] = {
    "usa": (-95.7129, 37.0902),
    "us": (-95.7129, 37.0902),
    "america": (-95.7129, 37.0902),
    "香港": (114.1694, 22.3193),
    "hong kong": (114.1694, 22.3193),
    "hk": (114.1694, 22.3193),
    "台湾": (121.5654, 25.0330),
    "taiwan": (121.5654, 25.0330),
    "中国": (116.4074, 39.9042),
    "china": (116.4074, 39.9042),
    "北京": (116.4074, 39.9042),
    "广东": (113.2644, 23.1291),
    "广州": (113.2644, 23.1291),
    "上海": (121.4737, 31.2304),
    "厦门": (118.0894, 24.4798),
}

CATEGORY_ALIASES: dict[str, str] = {
    "事业": "事业",
    "财运": "财运",
    "婚姻": "婚姻",
    "健康": "健康",
    "学业": "学业",
    "子女": "婚姻",
    "家庭": "家庭",
    "灾劫": "健康",
    "官非": "事业",
    "运势": "迁移",
    "外貌": "健康",
    "性格": "事业",
}

ADVERSE_KEYWORDS: dict[str, tuple[tuple[str, float], ...]] = {
    "婚姻": (
        ("夫早亡", 12),
        ("妻早亡", 12),
        ("丧偶", 11),
        ("早亡", 10),
        ("离异", 8),
        ("离婚", 8),
        ("二婚", 6),
        ("未嫁", 5),
        ("未婚", 5),
        ("单身", 4),
    ),
    "家庭": (
        ("贫穷", 10),
        ("过世", 8),
        ("仙逝", 8),
        ("离异", 7),
        ("离婚", 7),
        ("婚外情", 7),
        ("吃百家饭", 7),
        ("不在父母身边", 6),
        ("淡薄", 5),
    ),
    "健康": (
        ("病逝", 12),
        ("严重", 8),
        ("抑郁", 8),
        ("痴", 7),
        ("长期食药", 7),
        ("遗传病", 7),
        ("生病", 6),
        ("交通意外", 6),
        ("撞车", 6),
        ("受伤", 5),
    ),
    "财运": (
        ("被骗", 9),
        ("欠", 8),
        ("债", 8),
        ("输了", 7),
        ("赔", 7),
        ("月光", 6),
        ("没理财", 5),
        ("乱花", 5),
    ),
    "事业": (
        ("负债", 6),
        ("普通公司", 4),
        ("打工", 4),
        ("无业", 6),
        ("刑事", 8),
        ("官非", 8),
    ),
}

SUPPORTIVE_KEYWORDS: dict[str, tuple[tuple[str, float], ...]] = {
    "婚姻": (("一婚", 3), ("已婚", 3), ("结婚", 2), ("有孩子", 2)),
    "家庭": (("富裕", 7), ("当官", 7), ("疼爱", 5), ("融洽", 4), ("村干部", 4), ("从商", 4)),
    "健康": (("平安", 5), ("人平安", 7), ("健康", 4)),
    "财运": (("赚", 5), ("存款", 5), ("积蓄", 5), ("财务自由", 8), ("得财", 6)),
    "事业": (("老板", 5), ("突破", 5), ("升职", 5), ("国企", 4), ("事业单位", 4)),
}


@dataclass(frozen=True)
class OptionScore:
    letter: str
    text: str
    score: float
    reasons: tuple[str, ...]


def _as_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def benchmark_year(item: dict[str, Any]) -> int | None:
    question_number = int(item.get("question_number", 0) or 0)
    return 2022 + ((question_number - 1) // 40) if question_number > 0 else None


def normalize_gender(value: Any) -> str:
    text = str(value or "").strip().lower()
    return "female" if text in {"女", "female", "f", "坤", "坤造"} else "male"


def location_coords(birth_info: dict[str, Any]) -> tuple[float, float]:
    keys = [
        str(birth_info.get("location", "")).strip().lower(),
        str(birth_info.get("country", "")).strip().lower(),
        str(birth_info.get("raw", "")).strip().lower(),
    ]
    for key in keys:
        for marker, coords in LOCATION_COORDS.items():
            if marker.lower() in key:
                return coords
    return 116.4074, 39.9042


def build_birth_dt(birth_info: dict[str, Any]) -> datetime:
    return datetime(
        int(birth_info["year"]),
        int(birth_info["month"]),
        int(birth_info["day"]),
        int(birth_info.get("hour", 0) or 0),
        int(birth_info.get("minute", 0) or 0),
    )


def option_letters(item: dict[str, Any]) -> list[str]:
    options = _as_list(item.get("options"))
    letters = [str(option.get("letter", "")).strip().upper() for option in options if isinstance(option, dict)]
    return [letter for letter in letters if letter in LETTERS] or list(LETTERS)


def _topic_scores(result: dict[str, Any]) -> dict[str, int]:
    benchmark = _as_dict(result.get("baziBenchmark"))
    profiles = _as_list(benchmark.get("topicProfiles"))
    scores: dict[str, int] = {}
    for profile in profiles:
        if not isinstance(profile, dict):
            continue
        topic = str(profile.get("topic", "")).strip()
        score = profile.get("score")
        if topic and isinstance(score, int | float):
            scores[topic] = int(score)
    return scores


def _relation_pressure(result: dict[str, Any]) -> float:
    branch_relations = _as_dict(result.get("branchRelations"))
    canonical = _as_list(branch_relations.get("canonical"))
    conflicts = [
        item for item in canonical if isinstance(item, dict) and item.get("relation") in {"冲", "刑", "害", "破"}
    ]
    return min(1.0, len(conflicts) / 12)


def _category_pressure(category: str, result: dict[str, Any]) -> float:
    canonical = CATEGORY_ALIASES.get(category, category)
    topics = _topic_scores(result)
    if canonical in topics:
        return max(0.0, min(1.0, topics[canonical] / 100))
    if canonical == "家庭":
        return max(0.35, _relation_pressure(result))
    return 0.45


def _years(text: str) -> list[int]:
    return [int(match) for match in re.findall(r"(?:19|20)\d{2}", text)]


def _fortune_years(result: dict[str, Any]) -> list[int]:
    benchmark = _as_dict(result.get("baziBenchmark"))
    triggers = _as_list(benchmark.get("fortuneTriggers"))
    years: list[int] = []
    for trigger in triggers:
        if isinstance(trigger, dict) and isinstance(trigger.get("year"), int):
            years.append(int(trigger["year"]))
    return years


def _stable_tiebreaker(item: dict[str, Any], result: dict[str, Any], letter: str) -> float:
    depth = _as_dict(result.get("baziRuleDepth"))
    seed = {
        "question": item.get("question"),
        "category": item.get("category"),
        "letter": letter,
        "fourPillars": result.get("fourPillars"),
        "dayMaster": result.get("dayMaster"),
        "ruleDepthVersion": depth.get("registryVersion"),
    }
    digest = hashlib.sha256(json.dumps(seed, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()
    return (int(digest[:6], 16) % 1000) / 10000


def score_options(item: dict[str, Any], result: dict[str, Any]) -> list[OptionScore]:
    category = str(item.get("category", "")).strip()
    canonical = CATEGORY_ALIASES.get(category, category)
    pressure = _category_pressure(category, result)
    fortune_years = _fortune_years(result)
    options = _as_list(item.get("options"))
    scores: list[OptionScore] = []

    for option in options:
        if not isinstance(option, dict):
            continue
        letter = str(option.get("letter", "")).strip().upper()
        if letter not in LETTERS:
            continue
        text = str(option.get("text", ""))
        score = 0.0
        reasons: list[str] = []

        for keyword, weight in ADVERSE_KEYWORDS.get(canonical, ()):
            if keyword in text:
                delta = weight * (0.55 + pressure)
                score += delta
                reasons.append(f"{canonical}.adverse:{keyword}+{delta:.2f}")

        for keyword, weight in SUPPORTIVE_KEYWORDS.get(canonical, ()):
            if keyword in text:
                delta = weight * (1.15 - pressure if pressure < 0.7 else 0.15)
                score += delta
                reasons.append(f"{canonical}.supportive:{keyword}+{delta:.2f}")

        option_years = _years(text)
        if option_years and fortune_years:
            distance = min(abs(year - trigger) for year in option_years for trigger in fortune_years)
            delta = max(0.0, 4.0 - distance / 2)
            if delta > 0:
                score += delta
                reasons.append(f"fortune.year_distance:{distance}+{delta:.2f}")

        tie = _stable_tiebreaker(item, result, letter)
        score += tie
        if not reasons:
            reasons.append(f"stable_tiebreaker+{tie:.4f}")
        scores.append(OptionScore(letter=letter, text=text, score=round(score, 4), reasons=tuple(reasons)))

    if scores:
        return sorted(scores, key=lambda item: (item.score, item.letter), reverse=True)

    return [
        OptionScore(
            letter=letter,
            text="",
            score=_stable_tiebreaker(item, result, letter),
            reasons=("missing_options_stable_tiebreaker",),
        )
        for letter in option_letters(item)
    ]


def choose_answer(item: dict[str, Any], result: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    scores = score_options(item, result)
    selected = scores[0]
    runner_up = scores[1] if len(scores) > 1 else None
    margin = selected.score - (runner_up.score if runner_up else 0)
    confidence = 0.35
    if margin >= 8:
        confidence = 0.62
    elif margin >= 3:
        confidence = 0.5
    trace = {
        "schemaVersion": 1,
        "source": PREDICTION_SOURCE,
        "category": item.get("category"),
        "categoryPressure": round(_category_pressure(str(item.get("category", "")), result), 4),
        "confidence": confidence,
        "margin": round(margin, 4),
        "boundary": "弱规则 baseline：用于样本外评测链路，不等同专业专题推理器。",
        "optionScores": [
            {
                "letter": score.letter,
                "text": score.text,
                "score": score.score,
                "reasons": list(score.reasons),
            }
            for score in scores
        ],
    }
    return selected.letter, trace


def _load_questions(data_path: Path, selected_year: int | None, sample_size: int | None) -> list[dict[str, Any]]:
    payload = json.loads(data_path.read_text(encoding="utf-8"))
    questions = payload.get("questions")
    if not isinstance(questions, list):
        raise SystemExit(f"MingLi-Bench 数据结构异常: {data_path}")

    filtered: list[dict[str, Any]] = []
    for item in questions:
        if not isinstance(item, dict):
            continue
        if selected_year is not None and benchmark_year(item) != selected_year:
            continue
        filtered.append(item)
    return filtered[:sample_size] if sample_size is not None else filtered


def generate_predictions(
    data_path: Path,
    output_jsonl: Path,
    *,
    selected_year: int | None = None,
    sample_size: int | None = None,
) -> list[dict[str, Any]]:
    questions = _load_questions(data_path, selected_year, sample_size)
    rows: list[dict[str, Any]] = []
    result_cache: dict[tuple[Any, ...], dict[str, Any]] = {}

    for item in questions:
        birth_info = _as_dict(item.get("birth_info"))
        longitude, latitude = location_coords(birth_info)
        birth_dt = build_birth_dt(birth_info)
        gender = normalize_gender(birth_info.get("gender"))
        birth_place = str(birth_info.get("location") or birth_info.get("country") or "")
        cache_key = (
            birth_dt.isoformat(timespec="minutes"),
            gender,
            round(longitude, 6),
            round(latitude, 6),
            birth_place,
            False,
        )
        result = result_cache.get(cache_key)
        if result is None:
            result = calculate_pure_analysis(
                PureAnalysisInput(
                    birth_dt=birth_dt,
                    gender=gender,
                    longitude=longitude,
                    latitude=latitude,
                    birth_place=birth_place,
                    name="MingLi-Bench 匿名样本",
                    use_true_solar_time=False,
                )
            )
            result_cache[cache_key] = result
        predicted, trace = choose_answer(item, result)
        depth = _as_dict(result.get("baziRuleDepth"))
        rows.append(
            {
                "question_id": item.get("id"),
                "question_number": item.get("question_number"),
                "benchmark_year": benchmark_year(item),
                "category": item.get("category"),
                "predicted_answer": predicted,
                "prediction_source": PREDICTION_SOURCE,
                "response": f"答案：{predicted}",
                "scoring_trace": trace,
                "fatecat_evidence": {
                    "fourPillars": result.get("fourPillars"),
                    "dayMaster": result.get("dayMaster"),
                    "topicProfiles": _topic_scores(result),
                    "baziRuleDepthVersion": depth.get("registryVersion"),
                    "coordinatePolicy": "benchmark coarse location fallback; not production geocoding",
                },
            }
        )

    output_jsonl.parent.mkdir(parents=True, exist_ok=True)
    with output_jsonl.open("w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    return rows


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate FateCat MingLi-Bench scored baseline predictions.")
    parser.add_argument("--data", required=True, type=Path)
    parser.add_argument("--output-jsonl", required=True, type=Path)
    parser.add_argument("--year", type=int)
    parser.add_argument("--sample", type=int)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    rows = generate_predictions(
        args.data,
        args.output_jsonl,
        selected_year=args.year,
        sample_size=args.sample,
    )
    print(
        json.dumps(
            {
                "predictions": len(rows),
                "output": str(args.output_jsonl),
                "source": PREDICTION_SOURCE,
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
