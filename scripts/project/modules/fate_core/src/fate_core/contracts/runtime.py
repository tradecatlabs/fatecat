from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from fate_core.adapters.legacy_bazi import LegacyBaziInput


@dataclass(frozen=True)
class PureAnalysisRuntime:
    """纯命理分析运行时上下文。"""

    payload: LegacyBaziInput
    calculator: Any
    calc_now: datetime
    ec: Any
    lunar: Any
    yun: Any
    four_pillars: dict[str, Any]
    hidden_stems: dict[str, Any]
    ten_gods: dict[str, Any]
    twelve_growth: dict[str, Any]
    five_elements: dict[str, Any]
    special_palaces: dict[str, Any]
    void_info: dict[str, Any]
    day_master_seed: dict[str, Any]
