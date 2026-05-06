import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))


def test_liuyao_factor_seeded_deterministic():
    try:
        from liuyao_factors import generate_factor
    except Exception as exc:  # pragma: no cover
        pytest.skip(f"依赖不可用，跳过: {exc}")

    factor1 = generate_factor(
        item="BTCUSDT",
        timestamp="2026-01-19T12:00:00+08:00",
        method="seeded",
        seed="BTCUSDT|2026-01-19T12:00:00+08:00",
    )
    factor2 = generate_factor(
        item="BTCUSDT",
        timestamp="2026-01-19T12:00:00+08:00",
        method="seeded",
        seed="BTCUSDT|2026-01-19T12:00:00+08:00",
    )

    assert factor1.to_json() == factor2.to_json()
    assert factor1.item == "BTCUSDT"
    assert factor1.timestamp
