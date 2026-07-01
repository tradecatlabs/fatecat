from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
TELEGRAM_SRC = ROOT / "domains" / "experience-delivery" / "services" / "fatecat-delivery" / "src"

if str(TELEGRAM_SRC) not in sys.path:
    sys.path.insert(0, str(TELEGRAM_SRC))

import location  # noqa: E402


@pytest.mark.parametrize(
    ("raw", "message"),
    [
        ("999,999", "经度必须在 -180 到 180 之间"),
        ("181,0", "经度必须在 -180 到 180 之间"),
        ("-181,0", "经度必须在 -180 到 180 之间"),
        ("0,91", "纬度必须在 -90 到 90 之间"),
        ("0,-91", "纬度必须在 -90 到 90 之间"),
    ],
)
def test_direct_coordinate_input_rejects_out_of_range_values(raw: str, message: str):
    with pytest.raises(ValueError, match=message):
        location.get(raw)


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("180,90", (180.0, 90.0)),
        ("-180,-90", (-180.0, -90.0)),
        ("0,0", (0.0, 0.0)),
    ],
)
def test_direct_coordinate_input_accepts_legal_boundaries(raw: str, expected: tuple[float, float]):
    assert location.get(raw) == expected
