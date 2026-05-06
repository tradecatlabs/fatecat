from __future__ import annotations

from typing import Any

from .schema import Cycle, Direction, FactorOutput

GEN = {"木": "火", "火": "土", "土": "金", "金": "水", "水": "木"}
KE = {"木": "土", "土": "水", "水": "火", "火": "金", "金": "木"}


def _clamp(v: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, v))


def _iter_yao(raw: dict[str, Any]) -> list[tuple[int, dict[str, Any]]]:
    """按初爻到上爻顺序抽取爻数据。"""
    items = []
    for i in range(1, 7):
        key = f"yao_{i}"
        if key in raw:
            items.append((i, raw[key]))
    return items


def _pick_subject_object(raw: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    subject = None
    obj = None
    for _, yao in _iter_yao(raw):
        origin = yao.get("origin", {})
        if origin.get("is_subject"):
            subject = origin
        if origin.get("is_object"):
            obj = origin
    if subject is None or obj is None:
        raise ValueError("未找到世爻/应爻，无法生成因子")
    return subject, obj


def _moving_lines(raw: dict[str, Any]) -> list[int]:
    moving = []
    for idx, yao in _iter_yao(raw):
        origin = yao.get("origin", {})
        if origin.get("is_changed"):
            moving.append(idx)
    return moving


def _relation(w1: str, w2: str) -> str:
    if w1 == w2:
        return "same"
    if GEN.get(w1) == w2:
        return "generate"
    if KE.get(w1) == w2:
        return "overcome"
    if GEN.get(w2) == w1:
        return "generated_by"
    if KE.get(w2) == w1:
        return "overcome_by"
    return "unknown"


def _cycle_from_lines(moving: list[int]) -> Cycle:
    if not moving:
        return "1-3d"
    max_line = max(moving)
    if max_line in (1, 2):
        return "intraday"
    if max_line in (3, 4):
        return "1-3d"
    if max_line == 5:
        return "1-2w"
    return "1-3m"


def _kongwang_set(raw: dict[str, Any]) -> set[str]:
    kw = str(raw.get("kongwang", "")).strip()
    return set(kw) if kw else set()


def map_factor(
    raw: dict[str, Any],
    *,
    item: str,
    timestamp: str | None = None,
    cycle_hint: Cycle | None = None,
) -> FactorOutput:
    """把六爻标准化原始数据映射为量化因子。"""
    subject, obj = _pick_subject_object(raw)
    moving = _moving_lines(raw)
    relation = _relation(str(subject.get("wuxing", "")), str(obj.get("wuxing", "")))
    kongwang = _kongwang_set(raw)

    direction: Direction = "neutral"
    strength = 0.5
    confidence = 0.6
    explain: list[str] = []

    if relation in ("same", "generate"):
        direction = "up"
        strength += 0.2
        explain.append("世爻五行与应爻同气或生扶，方向偏上")
    elif relation in ("overcome_by", "generated_by"):
        direction = "down"
        strength -= 0.2
        explain.append("世爻受应爻制约或被生，方向偏下")
    else:
        explain.append("世应关系不明，方向中性")

    if len(moving) == 1:
        strength += 0.1
        confidence += 0.2
        explain.append("单动爻，信号较清晰")
    elif len(moving) >= 3:
        strength -= 0.1
        confidence -= 0.2
        explain.append("多动爻，信号偏杂")
    elif len(moving) == 0:
        confidence -= 0.1
        explain.append("无动爻，信号偏弱")

    if str(subject.get("zhi", "")) in kongwang:
        strength -= 0.15
        confidence -= 0.2
        explain.append("世爻落空亡，信号衰减")

    strength = _clamp(strength)
    confidence = _clamp(confidence)

    cycle = cycle_hint or _cycle_from_lines(moving)
    ts = timestamp or str(raw.get("time", ""))

    return FactorOutput(
        item=item,
        timestamp=ts,
        direction=direction,
        strength=strength,
        confidence=confidence,
        cycle=cycle,
        raw=raw,
        explain=explain,
    )
