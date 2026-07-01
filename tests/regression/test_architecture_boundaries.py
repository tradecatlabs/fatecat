from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FATE_CORE_SRC = ROOT / "domains" / "fate-analysis" / "services" / "fate-core" / "src"


def test_fate_core_source_does_not_reference_delivery_implementation_paths():
    forbidden_markers = (
        "TELEGRAM_SRC_DIR",
        "fatecat-delivery",
        "domains/experience-delivery",
    )
    offenders: list[str] = []

    for path in FATE_CORE_SRC.rglob("*"):
        if not path.is_file() or path.suffix in {".pyc", ".pyo"} or "__pycache__" in path.parts:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for marker in forbidden_markers:
            if marker in text:
                offenders.append(f"{path.relative_to(ROOT)} contains {marker}")

    assert offenders == []
