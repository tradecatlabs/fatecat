from __future__ import annotations

from pathlib import Path


def _find_enterprise_repo_root() -> Path:
    current = Path(__file__).resolve()
    for candidate in [current, *current.parents]:
        if (candidate / "pyproject.toml").exists() and (candidate / "domains").is_dir():
            return candidate
    raise RuntimeError("无法定位仓库根目录")


FATE_REPO_ROOT = _find_enterprise_repo_root()
FATE_CONTRACT_ROOT = FATE_REPO_ROOT / "contracts" / "fate"
FATE_CONFIG_ROOT = FATE_REPO_ROOT / "infra" / "environments" / "local"
FATE_DATA_ROOT = FATE_REPO_ROOT / "domains" / "fate-analysis" / "data-products"
FATE_DATABASE_ROOT = FATE_REPO_ROOT / "infra" / "databases"
FATE_VENDOR_ROOT = FATE_REPO_ROOT / "tools" / "reference-repos"
FATE_RUNTIME_ROOT = FATE_REPO_ROOT / "infra" / "runtime" / "local-state"
FATE_ASSET_ROOT = FATE_CONTRACT_ROOT
FATE_ASSETS_DIR = FATE_CONTRACT_ROOT
FATE_CAPABILITY_DIR = FATE_CONTRACT_ROOT / "capabilities"
FATE_PROFILE_DIR = FATE_CONTRACT_ROOT / "profiles"
FATE_CORE_ROOT = FATE_REPO_ROOT / "domains" / "fate-analysis" / "services" / "fate-core"
FATE_CORE_SCRIPT_ROOT = FATE_CORE_ROOT / "scripts"
FATE_TRUE_SOLAR_TIME_JS = FATE_CORE_SCRIPT_ROOT / "true_solar_time.js"
DANTALION_BRIDGE_JS = FATE_CORE_SCRIPT_ROOT / "dantalion_bridge.js"
FATE_VENDOR_GITHUB_ROOT = FATE_VENDOR_ROOT / "github"
LUNAR_PYTHON_DIR = FATE_VENDOR_ROOT / "github" / "lunar-python-master"
BAZI_1_DIR = FATE_VENDOR_GITHUB_ROOT / "bazi-1-master"
SXWNL_DIR = FATE_VENDOR_GITHUB_ROOT / "sxwnl-master"
IZTRO_DIR = FATE_VENDOR_GITHUB_ROOT / "iztro-main"
FORTEL_ZIWEI_DIR = FATE_VENDOR_GITHUB_ROOT / "fortel-ziweidoushu-main"
MIKABOSHI_DIR = FATE_VENDOR_GITHUB_ROOT / "mikaboshi-main"
CHINESE_DIVINATION_DIR = FATE_VENDOR_GITHUB_ROOT / "Chinese-Divination-master"
ICHING_DIR = FATE_VENDOR_GITHUB_ROOT / "Iching-master"
HOLIDAY_CALENDAR_DIR = FATE_VENDOR_GITHUB_ROOT / "holiday-and-chinese-almanac-calendar-main"
CHINESE_CALENDAR_DIR = FATE_VENDOR_GITHUB_ROOT / "chinese-calendar-master"
JS_ASTRO_DIR = FATE_VENDOR_GITHUB_ROOT / "js_astro-master"
DANTALION_DIR = FATE_VENDOR_GITHUB_ROOT / "dantalion-master"
PAIPAN_DIR = FATE_VENDOR_GITHUB_ROOT / "paipan-master"
SXWNL_INTERFACE_JS = SXWNL_DIR / "sxwnl_interface.js"
