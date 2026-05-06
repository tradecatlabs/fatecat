from __future__ import annotations

import hashlib
import random
from datetime import datetime
from typing import Any

from utils.timezone import ensure_cn, now_cn


def _validate_cnts(cnts: list[int]) -> None:
    """校验铜钱结果列表（长度6，元素为0-3）。"""
    if len(cnts) != 6:
        raise ValueError("cnts 必须为长度 6 的列表")
    for v in cnts:
        if v not in (0, 1, 2, 3):
            raise ValueError("cnts 元素只能是 0/1/2/3")


def _coerce_datetime(ts: datetime | str | None) -> datetime:
    """统一时间输入，默认使用中国时区当前时间（去掉 tzinfo 以兼容 divicast）。"""
    if ts is None:
        dt = now_cn()
    elif isinstance(ts, datetime):
        dt = ts
    else:
        dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
    dt = ensure_cn(dt)
    return dt.replace(tzinfo=None)


def _seed_to_int(seed: str | int) -> int:
    """将任意 seed 转成稳定整数。"""
    if isinstance(seed, int):
        return seed
    h = hashlib.sha256(seed.encode("utf-8")).hexdigest()
    return int(h[:16], 16)


def _build_cnts(
    *,
    cnts: list[int] | None,
    seed: str | int | None,
    item: str,
    dt: datetime,
) -> list[int]:
    """生成或校验 cnts（铜钱正面数）。"""
    if cnts is not None:
        _validate_cnts(cnts)
        return cnts
    if seed is None:
        seed = f"{item}|{dt.isoformat()}"
    rnd = random.Random(_seed_to_int(seed))
    return [bin(rnd.randrange(0, 8)).count("1") for _ in range(6)]


def build_raw(
    *,
    item: str,
    timestamp: datetime | str | None = None,
    cnts: list[int] | None = None,
    seed: str | int | None = None,
) -> dict[str, Any]:
    """生成六爻原始标准化 JSON（divicast 输出）。"""
    dt = _coerce_datetime(timestamp)
    cnts = _build_cnts(cnts=cnts, seed=seed, item=item, dt=dt)

    try:
        from divicast.sixline import DivinatorySymbol, to_standard_format
    except Exception as exc:  # pragma: no cover - 运行时依赖错误
        raise RuntimeError("divicast 未安装或不可用，请先安装依赖") from exc

    ds = DivinatorySymbol.create(cnts=cnts, now=dt)
    model = to_standard_format(ds)
    if hasattr(model, "model_dump"):
        return model.model_dump(exclude_none=True)
    if hasattr(model, "dict"):
        return model.dict(exclude_none=True)  # type: ignore[call-arg]
    return dict(model)
