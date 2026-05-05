import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "modules" / "fate_core" / "src"))

from fate_core.contracts import get_profile_fields  # noqa: E402


def test_pure_analysis_profile_contains_core_fields():
    fields = get_profile_fields("pure_analysis")

    assert "fourPillars" in fields
    assert "majorFortune" in fields
    assert "yongShen" in fields


def test_pure_analysis_profile_excludes_extension_fields():
    fields = get_profile_fields("pure_analysis")

    assert "ziweiChart" not in fields
    assert "planetPositions" not in fields
    assert "liuyaoHexagram" not in fields
    assert "nameAnalysis" not in fields
