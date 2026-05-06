from __future__ import annotations

from pathlib import Path


def _find_repo_root() -> Path:
    current = Path(__file__).resolve()
    for candidate in [current, *current.parents]:
        if (candidate / "pyproject.toml").exists():
            return candidate
    raise RuntimeError("无法定位仓库根目录")


FATE_REPO_ROOT = _find_repo_root()
FATE_ASSETS_DIR = FATE_REPO_ROOT / "assets" / "fate"
FATE_PROFILE_DIR = FATE_ASSETS_DIR / "profiles"
TELEGRAM_SRC_DIR = FATE_REPO_ROOT / "modules" / "telegram" / "src"
