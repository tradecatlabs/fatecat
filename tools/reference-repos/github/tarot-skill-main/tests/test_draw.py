import importlib.util
from pathlib import Path

PATH = Path(__file__).resolve().parents[1] / "scripts" / "draw.py"
SPEC = importlib.util.spec_from_file_location("draw", PATH)
draw = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(draw)


def test_draw_contract():
    a = draw.draw_cards("three", "事业", 123, "night")
    assert a == draw.draw_cards("three", "事业", 123, "night")
    h = draw.draw_cards("horseshoe", seed=7, time_factor="morning")
    cards = [c["card"] for c in h["cards"]]
    assert len(cards) == 7
    assert len(cards) == len(set(cards))
    assert h["cards"][0]["position"] == "远期过去"
    assert h["cards"][-1]["position"] == "结果"
