from __future__ import annotations

from pathlib import Path

from .schema import FactorOutput


def save_json(
    factor: FactorOutput,
    *,
    output_dir: Path,
    filename: str | None = None,
) -> Path:
    """保存因子 JSON 到指定目录。"""
    output_dir.mkdir(parents=True, exist_ok=True)
    if filename is None:
        safe_item = factor.item.replace("/", "_").replace(" ", "_")
        filename = f"liuyao_{safe_item}_{factor.timestamp.replace(':', '-')}.json"
    path = output_dir / filename
    path.write_text(factor.to_json(), encoding="utf-8")
    return path
