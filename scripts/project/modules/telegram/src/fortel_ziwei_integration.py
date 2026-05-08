#!/usr/bin/env python3
"""
专业紫微斗数集成器 - 强制使用原生库，失败即报错

外部库依赖注入 (相对路径从项目根目录):
├── assets/vendor/github/fortel-ziweidoushu-main/  # 专业紫微斗数
└── assets/vendor/github/iztro-main/lib/index.js   # iztro核心算法

运行环境: Node.js 18+
纯净性声明: 强制调用原生TypeScript算法，失败即抛异常终止
"""

import json
import os
import shutil
import subprocess
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any, cast

from _paths import IZTRO_DIR

IZTRO_PATH = Path(IZTRO_DIR)

# 英文到中文映射
EN_TO_CN = {
    "origin": "本命",
    "decadal": "大限",
    "yearly": "流年",
    "monthly": "流月",
    "daily": "流日",
    "hourly": "流时",
    "major": "主星",
    "minor": "辅星",
    "soft": "吉星",
    "tough": "煞星",
    "adjective": "杂曜",
    "flower": "桃花",
    "lucun": "禄存",
    "tianma": "天马",
    "success": "成功",
}


def _load_package_json(repo_dir: Path) -> dict:
    """读取 Node 仓库 package.json。"""
    package_json = repo_dir / "package.json"
    if not package_json.exists():
        raise RuntimeError(f"缺少 package.json: {package_json}")
    try:
        return cast(dict[str, Any], json.loads(package_json.read_text(encoding="utf-8")))
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"package.json 解析失败: {package_json}: {exc}") from exc


def _resolve_node_package_entry(repo_dir: Path, fallback: str = "lib/index.js") -> Path:
    """按 package.json main 字段解析入口文件。"""
    package_meta = _load_package_json(repo_dir)
    entry = package_meta.get("main") or fallback
    return repo_dir / entry


def _has_npm_script(repo_dir: Path, script_name: str) -> bool:
    """判断 package.json 是否声明了指定 npm script。"""
    package_meta = _load_package_json(repo_dir)
    scripts = package_meta.get("scripts", {})
    return isinstance(scripts, dict) and script_name in scripts


def _run_npm_command(repo_dir: Path, args: list[str], timeout: int) -> subprocess.CompletedProcess:
    """执行 npm 命令并保留错误上下文。"""
    npm_bin = shutil.which("npm")
    if not npm_bin:
        raise RuntimeError("未找到 npm，无法自动准备 iztro 依赖")

    result = subprocess.run(
        [npm_bin, *args],
        cwd=repo_dir,
        capture_output=True,
        text=True,
        timeout=timeout,
        env=dict(os.environ),
    )
    if result.returncode != 0:
        stderr = result.stderr.strip()
        stdout = result.stdout.strip()
        detail = stderr or stdout or "无输出"
        raise RuntimeError(f"npm {' '.join(args)} 失败: {detail}")
    return result


def _ensure_iztro_ready(repo_dir: Path) -> Path:
    """确保 iztro 已安装依赖并生成入口文件。"""
    repo_dir = Path(repo_dir)
    node_modules_dir = repo_dir / "node_modules"
    entry_path = _resolve_node_package_entry(repo_dir)

    if node_modules_dir.exists() and entry_path.exists():
        return entry_path

    if not node_modules_dir.exists():
        _run_npm_command(repo_dir, ["install", "--no-fund", "--no-audit"], timeout=300)

    entry_path = _resolve_node_package_entry(repo_dir)
    if not entry_path.exists() and _has_npm_script(repo_dir, "build"):
        _run_npm_command(repo_dir, ["run", "build"], timeout=300)
        entry_path = _resolve_node_package_entry(repo_dir)

    if not entry_path.exists():
        raise RuntimeError(f"iztro 入口缺失: {entry_path}；已尝试自动安装/构建，请检查 {repo_dir / 'package.json'}")

    return entry_path


def translate_value(obj):
    """递归翻译英文值为中文"""
    if isinstance(obj, dict):
        return {k: translate_value(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [translate_value(v) for v in obj]
    elif isinstance(obj, str) and obj in EN_TO_CN:
        return EN_TO_CN[obj]
    return obj


class FortelZiweiCalculator:
    """专业紫微斗数集成器 - 强制使用原生库，失败即报错"""

    def __init__(self, birth_dt: datetime, gender: str, longitude: float):
        self.birth_dt = birth_dt
        self.gender = gender
        self.longitude = longitude

    def _hour_to_shichen(self, hour: int) -> int:
        """小时转时辰索引(0-11)"""
        return ((hour + 1) // 2) % 12

    def calculate_ziwei_chart(self) -> dict[str, Any]:
        """紫微斗数计算 - 强制使用原生算法"""
        return self._call_native_iztro()

    def calculate_professional_ziwei(self, as_of: datetime | None = None) -> dict[str, Any]:
        """专业紫微计算"""
        result = self._call_native_iztro(as_of=as_of)
        return {
            "professionalZiwei": result,
            "stars": result.get("stars", {}),
            "palaces": result.get("palaces", {}),
            "fiveElementsClass": result.get("fiveElementsClass", ""),
            "influence": result.get("fiveElementsClass", {}),
            "horoscope": result.get("horoscope", {}),
        }

    def calculate_complete_ziwei_system(self, as_of: datetime | None = None) -> dict[str, Any]:
        """完整紫微系统"""
        return self.calculate_professional_ziwei(as_of=as_of)

    def _call_native_iztro(self, as_of: datetime | None = None) -> dict:
        """强制调用iztro原生算法"""
        shichen = self._hour_to_shichen(self.birth_dt.hour)
        gender_en = "male" if self.gender in ["male", "男", "m"] else "female"
        as_of = as_of or datetime.now()
        as_of_shichen = self._hour_to_shichen(as_of.hour)
        entry_path = _ensure_iztro_ready(IZTRO_PATH)

        js_script = f"""
        const {{ astro }} = require({json.dumps(str(entry_path))});
        const normalizeStar = (s) => s ? ({{
            name: s.name || "",
            type: s.type || "",
            scope: s.scope || "",
            brightness: s.brightness || "",
            mutagen: s.mutagen || ""
        }}) : {{}};
        const normalizeStars = (stars) => Array.isArray(stars) ? stars.map(normalizeStar) : [];
        const normalizePalace = (p) => p ? ({{
            index: p.index,
            name: p.name || "",
            heavenlyStem: p.heavenlyStem || "",
            earthlyBranch: p.earthlyBranch || "",
            isBodyPalace: Boolean(p.isBodyPalace),
            isOriginalPalace: Boolean(p.isOriginalPalace),
            majorStars: normalizeStars(p.majorStars),
            minorStars: normalizeStars(p.minorStars),
            adjectiveStars: normalizeStars(p.adjectiveStars),
            changsheng12: p.changsheng12 || "",
            boshi12: p.boshi12 || "",
            jiangqian12: p.jiangqian12 || "",
            suiqian12: p.suiqian12 || "",
            decadal: p.decadal || null,
            ages: Array.isArray(p.ages) ? p.ages : [],
            decadal_now: p.decadal_now || null,
            year_now: p.year_now || null
        }}) : {{}};
        const normalizeHoroscopeScope = (scope) => scope ? ({{
            heavenlyStem: scope.heavenlyStem || "",
            earthlyBranch: scope.earthlyBranch || "",
            palaceNames: Array.isArray(scope.palaceNames) ? scope.palaceNames : [],
            mutagen: Array.isArray(scope.mutagen) ? scope.mutagen : [],
            stars: Array.isArray(scope.stars) ? scope.stars.map(block => normalizeStars(block)) : []
        }}) : {{}};
        try {{
            const result = astro.bySolar(
                '{self.birth_dt.year}-{self.birth_dt.month:02d}-{self.birth_dt.day:02d}',
                {shichen},
                '{gender_en}',
                true,
                'zh-CN'
            );
            const asOf = new Date({as_of.year}, {as_of.month - 1}, {as_of.day}, {as_of.hour}, {as_of.minute}, {as_of.second});
            const hz = result.horoscope(asOf, {as_of_shichen});
            const hzOut = {{
                solarDate: hz.solarDate,
                lunarDate: hz.lunarDate,
                age: hz.age,
                decadal: normalizeHoroscopeScope(hz.decadal),
                yearly: normalizeHoroscopeScope(hz.yearly),
                monthly: normalizeHoroscopeScope(hz.monthly),
                daily: normalizeHoroscopeScope(hz.daily),
                hourly: normalizeHoroscopeScope(hz.hourly),
            }};
            console.log(JSON.stringify({{
                source: "iztro原生算法",
                algorithm: "紫微斗数",
                solarDate: result.solarDate,
                lunarDate: result.lunarDate,
                rawDates: result.rawDates || null,
                zodiac: result.zodiac || "",
                sign: result.sign || "",
                gender: result.gender || "",
                time: result.time || "",
                timeRange: result.timeRange || "",
                fiveElementsClass: result.fiveElementsClass,
                soul: result.soul,
                body: result.body,
                earthlyBranchOfSoulPalace: result.earthlyBranchOfSoulPalace || "",
                earthlyBranchOfBodyPalace: result.earthlyBranchOfBodyPalace || "",
                palaces: result.palaces ? result.palaces.map(normalizePalace) : [],
                horoscope: hzOut,
                status: "success"
            }}));
        }} catch (e) {{
            console.log(JSON.stringify({{error: e.message}}));
            process.exit(1);
        }}
        """

        with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".js", delete=False) as temp_file:
            temp_file.write(js_script)
            temp_path = temp_file.name

        try:
            env = dict(os.environ)
            env["TZ"] = "Asia/Shanghai"
            result = subprocess.run(
                ["node", temp_path],
                capture_output=True,
                text=True,
                timeout=30,
                env=env,
            )

            if result.returncode != 0:
                stderr = result.stderr.strip() or result.stdout.strip()
                raise RuntimeError(f"iztro原生算法执行失败: {stderr}")

            try:
                data = json.loads(result.stdout)
                return cast(dict[str, Any], translate_value(data))
            except json.JSONDecodeError as e:
                raise RuntimeError(f"iztro输出解析失败: {e}") from e
        finally:
            try:
                os.unlink(temp_path)
            except FileNotFoundError:
                pass
