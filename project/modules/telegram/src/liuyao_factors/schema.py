from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from typing import Any, Literal

Direction = Literal["up", "down", "neutral"]
Cycle = Literal["intraday", "1-3d", "1-2w", "1-3m"]


@dataclass
class FactorOutput:
    """六爻量化因子输出结构。"""

    item: str
    timestamp: str
    direction: Direction
    strength: float
    confidence: float
    cycle: Cycle
    raw: dict[str, Any] = field(default_factory=dict)
    explain: list[str] = field(default_factory=list)
    source: str = "divicast"
    version: str = "v1"

    def to_dict(self) -> dict[str, Any]:
        """转为 dict（中文字段仅限 explain）。"""
        return asdict(self)

    def to_json(self) -> str:
        """转为 JSON 字符串（保留中文）。"""
        return json.dumps(self.to_dict(), ensure_ascii=False, sort_keys=True)
