"""
FateCat 路径管理模块
统一管理仓库内静态资产、运行时数据与模块路径，避免路径继续带旧项目影子。
"""

import os
from pathlib import Path
from typing import Any

# ==================== 仓库与模块根路径 ====================
SERVICE_ROOT = Path(__file__).resolve().parent.parent


def _find_enterprise_repo_root() -> Path:
    current = Path(__file__).resolve()
    for candidate in [current, *current.parents]:
        if (candidate / "pyproject.toml").exists() and (candidate / "domains").is_dir():
            return candidate
    raise RuntimeError("无法定位 FateCat 企业仓库根目录")


REPO_ROOT = _find_enterprise_repo_root()
MODULE_ROOT = SERVICE_ROOT

# ==================== 静态资产路径 ====================
ASSETS_DIR = REPO_ROOT / "contracts" / "fate"
CONFIG_DIR = REPO_ROOT / "infra" / "environments" / "local"
DATA_DIR = REPO_ROOT / "domains" / "fate-analysis" / "data-products"
ASSET_DATABASE_DIR = REPO_ROOT / "infra" / "databases"
VENDOR_DIR = REPO_ROOT / "tools" / "reference-repos"
EXTERNAL_LIBS_DIR = VENDOR_DIR / "github"
WEB_VENDOR_DIR = VENDOR_DIR / "web"
FATE_ASSETS_DIR = REPO_ROOT / "contracts" / "fate"
ENV_FILE = CONFIG_DIR / ".env"

# ==================== 运行时路径 ====================
RUNTIME_DIR = REPO_ROOT / "infra" / "runtime" / "local-state"
RUNTIME_DATABASE_DIR = RUNTIME_DIR / "database"

# ==================== 核心模块路径 ====================
FATE_CORE_ROOT = REPO_ROOT / "domains" / "fate-analysis" / "services" / "fate-core"
FATE_CORE_SRC_DIR = FATE_CORE_ROOT / "src"

# ==================== 模块内部路径 ====================
SRC_DIR = MODULE_ROOT / "src"
SCRIPTS_DIR = MODULE_ROOT / "scripts"
OUTPUT_DIR = MODULE_ROOT / "output"
LOGS_DIR = OUTPUT_DIR / "logs"
TXT_DIR = OUTPUT_DIR / "txt"
QUEUE_DIR = OUTPUT_DIR / "queue"
PROMPTS_DIR = SRC_DIR / "prompts"

# ==================== 数据库与数据文件 ====================
BAZI_SCHEMA_DIR = ASSET_DATABASE_DIR / "bazi"
BAZI_SCHEMA_PATH = BAZI_SCHEMA_DIR / "schema_v2.sql"
BAZI_DB_DIR = RUNTIME_DATABASE_DIR / "bazi"
BAZI_DB_PATH = BAZI_DB_DIR / "bazi.db"
CHINA_COORDS_CSV = DATA_DIR / "china_coordinates.csv"

# ==================== 外部库路径 ====================
LUNAR_PYTHON_DIR = EXTERNAL_LIBS_DIR / "lunar-python-master"
BAZI_1_DIR = EXTERNAL_LIBS_DIR / "bazi-1-master"
SXWNL_DIR = EXTERNAL_LIBS_DIR / "sxwnl-master"
IZTRO_DIR = EXTERNAL_LIBS_DIR / "iztro-main"
FORTEL_ZIWEI_DIR = EXTERNAL_LIBS_DIR / "fortel-ziweidoushu-main"
MIKABOSHI_DIR = EXTERNAL_LIBS_DIR / "mikaboshi-main"
CHINESE_DIVINATION_DIR = EXTERNAL_LIBS_DIR / "Chinese-Divination-master"
ICHING_DIR = EXTERNAL_LIBS_DIR / "Iching-master"
HOLIDAY_CALENDAR_DIR = EXTERNAL_LIBS_DIR / "holiday-and-chinese-almanac-calendar-main"
CHINESE_CALENDAR_DIR = EXTERNAL_LIBS_DIR / "chinese-calendar-master"
JS_ASTRO_DIR = EXTERNAL_LIBS_DIR / "js_astro-master"
DANTALION_DIR = EXTERNAL_LIBS_DIR / "dantalion-master"
PAIPAN_DIR = EXTERNAL_LIBS_DIR / "paipan-master"

# ==================== 脚本路径 ====================
TRUE_SOLAR_TIME_JS = SCRIPTS_DIR / "true_solar_time.js"
SXWNL_INTERFACE_JS = SXWNL_DIR / "sxwnl_interface.js"
DANTALION_BRIDGE_JS = SCRIPTS_DIR / "dantalion_bridge.js"


def ensure_dirs():
    """确保必要目录存在。"""
    for path in [LOGS_DIR, TXT_DIR, QUEUE_DIR, BAZI_DB_DIR]:
        path.mkdir(parents=True, exist_ok=True)


def get_env_file() -> Path:
    """获取统一配置文件路径。"""
    if not ENV_FILE.exists():
        raise FileNotFoundError(
            f"配置文件不存在: {ENV_FILE}\n请复制 infra/environments/local/.env.example 为 infra/environments/local/.env 并填写配置"
        )
    return ENV_FILE


def check_dependencies() -> dict[str, Any]:
    """检查必需依赖与可选依赖。"""
    results: dict[str, Any] = {"ok": True, "errors": [], "warnings": []}

    required = [
        (BAZI_SCHEMA_PATH, "数据库 schema"),
        (LUNAR_PYTHON_DIR, "lunar-python 库"),
        (BAZI_1_DIR, "bazi-1 库"),
        (SXWNL_DIR, "sxwnl 库"),
        (CHINA_COORDS_CSV, "城市坐标数据"),
    ]
    optional = [
        (FORTEL_ZIWEI_DIR, "fortel-ziweidoushu 库（紫微斗数）"),
        (DANTALION_DIR, "dantalion 库（现代八字）"),
        (IZTRO_DIR, "iztro 库（紫微斗数）"),
        (MIKABOSHI_DIR, "mikaboshi 库（风水罗盘）"),
        (CHINESE_DIVINATION_DIR, "Chinese-Divination 库（六爻梅花）"),
        (ICHING_DIR, "Iching 库（易经）"),
        (HOLIDAY_CALENDAR_DIR, "holiday-calendar（黄历）"),
        (CHINESE_CALENDAR_DIR, "chinese-calendar（农历）"),
        (JS_ASTRO_DIR, "js_astro 库（天文）"),
        (PAIPAN_DIR, "paipan 库（真太阳时）"),
    ]

    for path, name in required:
        if not path.exists():
            results["ok"] = False
            results["errors"].append(f"缺少必需依赖: {name} ({path})")

    for path, name in optional:
        if not path.exists():
            results["warnings"].append(f"缺少可选依赖: {name} ({path})")

    file_token = ""
    if ENV_FILE.exists():
        from dotenv import dotenv_values

        config = dotenv_values(ENV_FILE)
        file_token = str(config.get("FATE_BOT_TOKEN") or "").strip()

    if not (os.getenv("FATE_BOT_TOKEN", "").strip() or file_token):
        results["ok"] = False
        results["errors"].append("未配置 FATE_BOT_TOKEN（环境变量或本地 .env）")

    return results


def startup_check():
    """启动时执行完整检查。"""
    print("[fatecat] 启动检查...")

    ensure_dirs()
    print("  ✅ 目录结构已就绪")

    results = check_dependencies()
    for warn in results["warnings"]:
        print(f"  ⚠️  {warn}")

    if not results["ok"]:
        print("  ❌ 启动检查失败:")
        for err in results["errors"]:
            print(f"     - {err}")
        raise RuntimeError("依赖检查失败，请修复后重试")

    print("  ✅ 依赖检查通过")
    return True
