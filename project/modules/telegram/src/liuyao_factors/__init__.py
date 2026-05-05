from __future__ import annotations

from datetime import datetime

from .engine import build_raw
from .mapper import map_factor
from .schema import FactorOutput

__all__ = [
    "generate_factor",
    "build_raw",
    "map_factor",
    "FactorOutput",
]


def generate_factor(
    *,
    item: str,
    timestamp: datetime | str | None = None,
    method: str = "seeded",
    seed: str | int | None = None,
    cnts: list[int] | None = None,
    cycle_hint: str | None = None,
) -> FactorOutput:
    """生成六爻因子（主入口）。

    传参约定：
    - item: 标的名称（交易对/商品名）
    - timestamp: ISO 时间字符串或 datetime，默认当前中国时间
    - method: seeded/random/manual
      - seeded: 使用 seed 或 item+timestamp 生成确定性 cnts
      - random: 随机起卦
      - manual: 必须传 cnts
    - seed: 任意可哈希字符串/整数（用于 seeded）
    - cnts: 6个元素的列表，每个元素为0-3（3枚铜钱中正面数量）
    - cycle_hint: 强制周期（intraday/1-3d/1-2w/1-3m）
    """
    if method == "manual" and cnts is None:
        raise ValueError("method=manual 时必须传入 cnts")
    use_cnts = None if method in ("random", "seeded") else cnts
    use_seed = None if method == "random" else seed

    raw = build_raw(item=item, timestamp=timestamp, cnts=use_cnts, seed=use_seed)
    return map_factor(raw, item=item, timestamp=raw.get("time"), cycle_hint=cycle_hint)
