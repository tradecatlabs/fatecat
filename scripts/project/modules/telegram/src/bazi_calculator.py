"""
FateCat 遗留八字排盘装配器 - 复用外部成熟库并输出标准报告所需字段

外部库依赖注入 (相对路径从项目根目录):
├── assets/vendor/github/lunar-python-master     # 核心历法库 (强制依赖)
├── assets/vendor/github/bazi-1-master           # 五行量化、神煞数据
├── assets/vendor/github/sxwnl-master            # 寿星万年历 (Node.js)
├── assets/vendor/github/iztro-main              # 紫微斗数 (TypeScript)
├── assets/vendor/github/fortel-ziweidoushu-main # 专业紫微斗数
├── assets/vendor/github/mikaboshi-main          # 风水罗盘 (Rust)
├── assets/vendor/github/Chinese-Divination-master # 六爻/梅花/奇门
├── assets/vendor/github/Iching-master           # 易经系统
├── assets/vendor/github/holiday-and-chinese-almanac-calendar-main # 节假日历法
└── assets/vendor/github/chinese-calendar-master # 中国历法

本地模块调用 (相对路径从src目录):
├── sxwnl_integration.py          -> sxwnl-master
├── fortel_ziwei_integration.py   -> fortel-ziweidoushu-main, iztro-main
├── mikaboshi_fengshui_integration.py -> mikaboshi-main
├── astro_integration.py          -> js_astro-master
├── dantalion_integration.py      -> dantalion-main
├── advanced_calendar_integration.py -> holiday-and-chinese-almanac-calendar-main
├── enhanced_yijing_integration.py -> Iching-master, Chinese-Divination-master
├── meihua.py                     -> Chinese-Divination-master, bazi-1-master
├── liuyao.py                     -> Chinese-Divination-master, bazi-1-master
├── liuren.py                     -> 原生实现
├── qimen.py                      -> Chinese-Divination-master
├── ziwei.py                      -> iztro-main
├── zeri.py                       -> bazi-1-master, lunar-python-master
├── hehun.py                      -> bazi-1-master, lunar-python-master
└── xingming.py                   -> bazi-name-master, bazi-1-master

纯净性声明: 失败即终止，零降级策略
"""

import ast
import importlib
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

# 外部库路径 (统一使用 _paths 模块)
from _paths import BAZI_1_DIR, DANTALION_DIR, LUNAR_PYTHON_DIR, SRC_DIR
from utils.timezone import ensure_cn, fmt_cn, now_cn

sys.path.insert(0, str(LUNAR_PYTHON_DIR))
sys.path.insert(0, str(BAZI_1_DIR))

# 核心依赖强制导入 - 失败即终止
from datas import day_shens, g_shens, jinbuhuan, month_shens, shens_infos, tiaohous, year_shens
from ganzhi import gan5, gan_desc, gan_health, ten_deities, zhi5, zhi_desc
from lunar_python import Solar
from lunar_python.util.LunarUtil import LunarUtil
from sizi import summarys as sizi_summarys

# 五行映射 (全部使用中文)
STEM_ELEM = {
    "甲": "木",
    "乙": "木",
    "丙": "火",
    "丁": "火",
    "戊": "土",
    "己": "土",
    "庚": "金",
    "辛": "金",
    "壬": "水",
    "癸": "水",
}
BRANCH_ELEM = {
    "子": "水",
    "丑": "土",
    "寅": "木",
    "卯": "木",
    "辰": "土",
    "巳": "火",
    "午": "火",
    "未": "土",
    "申": "金",
    "酉": "金",
    "戌": "土",
    "亥": "水",
}
ELEM_CN = {
    "木": "木",
    "火": "火",
    "土": "土",
    "金": "金",
    "水": "水",
    "wood": "木",
    "fire": "火",
    "earth": "土",
    "metal": "金",
    "water": "水",
}

# 十神映射
SHISHEN = {
    "甲": {
        "甲": "比肩",
        "乙": "劫财",
        "丙": "食神",
        "丁": "伤官",
        "戊": "偏财",
        "己": "正财",
        "庚": "七杀",
        "辛": "正官",
        "壬": "偏印",
        "癸": "正印",
    },
    "乙": {
        "甲": "劫财",
        "乙": "比肩",
        "丙": "伤官",
        "丁": "食神",
        "戊": "正财",
        "己": "偏财",
        "庚": "正官",
        "辛": "七杀",
        "壬": "正印",
        "癸": "偏印",
    },
    "丙": {
        "甲": "偏印",
        "乙": "正印",
        "丙": "比肩",
        "丁": "劫财",
        "戊": "食神",
        "己": "伤官",
        "庚": "偏财",
        "辛": "正财",
        "壬": "七杀",
        "癸": "正官",
    },
    "丁": {
        "甲": "正印",
        "乙": "偏印",
        "丙": "劫财",
        "丁": "比肩",
        "戊": "伤官",
        "己": "食神",
        "庚": "正财",
        "辛": "偏财",
        "壬": "正官",
        "癸": "七杀",
    },
    "戊": {
        "甲": "七杀",
        "乙": "正官",
        "丙": "偏印",
        "丁": "正印",
        "戊": "比肩",
        "己": "劫财",
        "庚": "食神",
        "辛": "伤官",
        "壬": "偏财",
        "癸": "正财",
    },
    "己": {
        "甲": "正官",
        "乙": "七杀",
        "丙": "正印",
        "丁": "偏印",
        "戊": "劫财",
        "己": "比肩",
        "庚": "伤官",
        "辛": "食神",
        "壬": "正财",
        "癸": "偏财",
    },
    "庚": {
        "甲": "偏财",
        "乙": "正财",
        "丙": "七杀",
        "丁": "正官",
        "戊": "偏印",
        "己": "正印",
        "庚": "比肩",
        "辛": "劫财",
        "壬": "食神",
        "癸": "伤官",
    },
    "辛": {
        "甲": "正财",
        "乙": "偏财",
        "丙": "正官",
        "丁": "七杀",
        "戊": "正印",
        "己": "偏印",
        "庚": "劫财",
        "辛": "比肩",
        "壬": "伤官",
        "癸": "食神",
    },
    "壬": {
        "甲": "食神",
        "乙": "伤官",
        "丙": "偏财",
        "丁": "正财",
        "戊": "七杀",
        "己": "正官",
        "庚": "偏印",
        "辛": "正印",
        "壬": "比肩",
        "癸": "劫财",
    },
    "癸": {
        "甲": "伤官",
        "乙": "食神",
        "丙": "正财",
        "丁": "偏财",
        "戊": "正官",
        "己": "七杀",
        "庚": "正印",
        "辛": "偏印",
        "壬": "劫财",
        "癸": "比肩",
    },
}

# 五行旺相休囚死 (月支决定)
WUXING_STATE = {
    "寅": {"木": "旺", "火": "相", "水": "休", "金": "囚", "土": "死"},
    "卯": {"木": "旺", "火": "相", "水": "休", "金": "囚", "土": "死"},
    "辰": {"土": "旺", "金": "相", "火": "休", "木": "囚", "水": "死"},
    "巳": {"火": "旺", "土": "相", "木": "休", "水": "囚", "金": "死"},
    "午": {"火": "旺", "土": "相", "木": "休", "水": "囚", "金": "死"},
    "未": {"土": "旺", "金": "相", "火": "休", "木": "囚", "水": "死"},
    "申": {"金": "旺", "水": "相", "土": "休", "火": "囚", "木": "死"},
    "酉": {"金": "旺", "水": "相", "土": "休", "火": "囚", "木": "死"},
    "戌": {"土": "旺", "金": "相", "火": "休", "木": "囚", "水": "死"},
    "亥": {"水": "旺", "木": "相", "金": "休", "土": "囚", "火": "死"},
    "子": {"水": "旺", "木": "相", "金": "休", "土": "囚", "火": "死"},
    "丑": {"土": "旺", "金": "相", "火": "休", "木": "囚", "水": "死"},
}

# 人元司令分野 (月支 -> [(藏干, 天数)])
SILING = {
    "寅": [("戊", 7), ("丙", 7), ("甲", 16)],
    "卯": [("甲", 10), ("乙", 20)],
    "辰": [("乙", 9), ("癸", 3), ("戊", 18)],
    "巳": [("戊", 5), ("庚", 9), ("丙", 16)],
    "午": [("丙", 10), ("己", 9), ("丁", 11)],
    "未": [("丁", 9), ("乙", 3), ("己", 18)],
    "申": [("戊", 10), ("壬", 3), ("庚", 17)],
    "酉": [("庚", 10), ("辛", 20)],
    "戌": [("辛", 9), ("丁", 3), ("戊", 18)],
    "亥": [("戊", 7), ("甲", 5), ("壬", 18)],
    "子": [("壬", 10), ("癸", 20)],
    "丑": [("癸", 9), ("辛", 3), ("己", 18)],
}

# 建禄表 (日干 -> 禄位)
JIANLU = {
    "甲": "寅",
    "乙": "卯",
    "丙": "巳",
    "丁": "午",
    "戊": "巳",
    "己": "午",
    "庚": "申",
    "辛": "酉",
    "壬": "亥",
    "癸": "子",
}

# 羊刃表 (日干 -> 刃位)
YANGREN_POS = {"甲": "卯", "丙": "午", "戊": "午", "庚": "酉", "壬": "子"}

# 调候用神表（外部 bazi-1 datas.tiaohous）
TIAOHOU = tiaohous


class BaziCalculator:
    """八字计算器"""

    def __init__(
        self,
        birth_dt: datetime,
        gender: str,
        longitude: float = None,
        name: str = "",
        birth_place: str = "",
        latitude: float = None,
        use_true_solar_time: bool = True,
    ):
        if longitude is None:
            raise ValueError("缺失经度: 禁止使用默认经度/回退值")
        if latitude is None:
            raise ValueError("缺失纬度: 禁止使用默认纬度/回退值")

        # 原始公历输入（假定为北京时间）
        self.birth_dt = ensure_cn(birth_dt)
        self.gender = gender
        self.longitude = longitude
        self.latitude = latitude
        self.use_true_solar_time = use_true_solar_time
        self.name = name or "命主"
        self.birth_place = birth_place or "未知"
        self.solar = self.lunar = self.ec = None
        self.true_solar_detail = {}
        self.zi_time_analysis = {}

        # 真太阳时只修正一次
        if use_true_solar_time:
            self.calc_dt, self.true_solar_detail, self.zi_time_analysis = self._calc_true_solar_time_detail(
                self.birth_dt, longitude, latitude
            )
        else:
            self.calc_dt = self.birth_dt
            self.true_solar_detail = {
                "originalTime": fmt_cn(self.birth_dt, "%Y-%m-%d %H:%M:%S"),
                "trueSolarTime": fmt_cn(self.birth_dt, "%Y-%m-%d %H:%M:%S"),
                "longitudeOffsetMinutes": 0,
                "astronomicalOffsetMinutes": 0,
                "totalOffsetMinutes": 0,
                "note": "未启用真太阳时修正",
            }
            self.zi_time_analysis = {"rule": "未启用真太阳时修正", "timeZhi": "", "zwzShift": False}
        self.true_solar_time = self.calc_dt

        # 强制使用lunar-python原生算法（基于修正后的时间）
        tst = self.calc_dt
        self.solar = Solar.fromYmdHms(tst.year, tst.month, tst.day, tst.hour, tst.minute, tst.second)
        self.lunar = self.solar.getLunar()
        self.ec = self.lunar.getEightChar()

    def calculate(self, hide: dict[str, bool] | None = None) -> dict[str, Any]:
        if not self.ec:
            raise RuntimeError("lunar-python初始化失败")

        ec = self.ec
        hide = hide or {}
        calc_now = now_cn()

        # 四柱
        four_pillars = {
            p: self._pillar(
                getattr(ec, f"get{p.title()}")(),
                getattr(ec, f"get{p.title()}Gan")(),
                getattr(ec, f"get{p.title()}Zhi")(),
            )
            for p in ["year", "month", "day"]
        }
        four_pillars["hour"] = self._pillar(ec.getTime(), ec.getTimeGan(), ec.getTimeZhi())

        # 藏干
        hidden = {p: getattr(ec, f"get{p.title()}HideGan")() for p in ["year", "month", "day"]}
        hidden["hour"] = ec.getTimeHideGan()

        # 十神
        ten_gods = {
            p: {
                "stem": getattr(ec, f"get{p.title()}ShiShenGan")(),
                "branch": getattr(ec, f"get{p.title()}ShiShenZhi")(),
            }
            for p in ["year", "month", "day"]
        }
        ten_gods["hour"] = {"stem": ec.getTimeShiShenGan(), "branch": ec.getTimeShiShenZhi()}

        # 十二长生
        twelve = {p: getattr(ec, f"get{p.title()}DiShi")() for p in ["year", "month", "day"]}
        twelve["hour"] = ec.getTimeDiShi()

        # 五行
        five_elem = self._calc_elements(four_pillars, hidden)

        # 补齐中英双键，兼容测试与展示
        def _alias_five_elements(fe: dict) -> dict:
            map_cn = {"木": "wood", "火": "fire", "土": "earth", "金": "metal", "水": "water"}
            res = dict(fe)
            # 若只有中文键，补英文；若只有英文，补中文
            for cn, en in map_cn.items():
                if cn in fe and en not in fe:
                    res[en] = fe[cn]
                if en in fe and cn not in fe:
                    res[cn] = fe[en]
            return res

        five_elem = _alias_five_elements(five_elem)

        # 特殊宫位
        palaces = {
            "taiYuan": {"pillar": ec.getTaiYuan(), "nayin": ec.getTaiYuanNaYin()},
            "taiXi": {"pillar": ec.getTaiXi(), "nayin": ec.getTaiXiNaYin()},
            "mingGong": {"pillar": ec.getMingGong(), "nayin": ec.getMingGongNaYin()},
            "shenGong": {"pillar": ec.getShenGong(), "nayin": ec.getShenGongNaYin()},
        }

        # 空亡
        void = {
            "year": {"xun": ec.getYearXun(), "kong": ec.getYearXunKong()},
            "month": {"xun": ec.getMonthXun(), "kong": ec.getMonthXunKong()},
            "day": {"xun": ec.getDayXun(), "kong": ec.getDayXunKong()},
            "hour": {"xun": ec.getTimeXun(), "kong": ec.getTimeXunKong()},
        }

        # 大运
        yun = ec.getYun(1 if self.gender == "male" else 0)
        major = self._calc_fortune(yun)

        # 流年
        annual = self._calc_annual()

        # 流月
        monthly = self._calc_monthly(yun)
        monthly = self._add_monthly_shishen(monthly, ec.getDayGan())

        # 神煞（仅使用外部全量表，禁止本地简表口径）
        spirits = self._calc_all_spirits(ec)
        spirits_full = spirits
        # 干支取象（bazi-1 原生字典）
        ganzhi_imagery = self._calc_ganzhi_imagery(four_pillars)
        # 五行健康/开运提示（bazi-1 原生字典）
        wuxing_health = {}
        if not hide.get("health", False):
            wuxing_health = self._calc_wuxing_health_tips()
        # 神煞释义（仅对“本盘出现的神煞”展开，避免无意义全字典铺开）
        spirits_explain = self._calc_spirits_explain(spirits_full)
        gz_extra = self._calc_ganzhi_extra(four_pillars, hidden)
        wx_scores = self._calc_wuxing_scores(four_pillars)
        zhi_rel = self._calc_zhi_relations(four_pillars)
        climate = self._calc_climate_scores(four_pillars)

        # 日主强弱（与五行分数口径统一：保留 bazi-1 weak/strong 原始字段，再归一为五档展示）
        day_elem = STEM_ELEM[ec.getDayGan()]
        strength = wx_scores.get("weakStrong")

        # 称骨算命
        year_gz = ec.getYear()
        lunar_month = self.lunar.getMonth()
        lunar_day = self.lunar.getDay()
        hour_zhi = ec.getTimeZhi()
        bone = calc_bone_weight(year_gz, abs(lunar_month), lunar_day, hour_zhi)

        # 命卦
        ming_gua = calc_ming_gua(self.calc_dt.year, self.gender)

        # 干支关系
        gz_relations = self._calc_ganzhi_relations(four_pillars)

        # 五行状态
        month_zhi = ec.getMonthZhi()
        wuxing_state = self._calc_wuxing_state(five_elem, month_zhi)

        # 节气详情
        jieqi_detail = self._calc_jieqi_detail()

        # 大运十神纳音
        major_with_shishen = self._add_fortune_shishen(major, ec.getDayGan())

        # 流年十神纳音
        annual_with_shishen = self._add_annual_shishen(annual, ec.getDayGan())

        # 人元司令分野
        days_from_jie = jieqi_detail.get("prevJieQi", {}).get("daysAfter", 0)
        siling = self._calc_siling(ec.getMonthZhi(), days_from_jie)

        # 格局判断
        geju = self._calc_geju(ec, four_pillars)

        # 自坐（日干对日支的十二长生）
        self_sitting = self._calc_self_sitting(ec.getDayGan(), ec.getDayZhi())

        # 用神分析（后续大运/流年/小运神煞与作用依赖）
        yongshen = self._calc_yongshen(ec.getDayGan(), ec.getMonthZhi(), four_pillars)
        analysis_evidence = self._calc_analysis_evidence(
            four_pillars=four_pillars,
            hidden_stems=hidden,
            day_master={
                "stem": ec.getDayGan(),
                "element": day_elem,
                "elementCn": ELEM_CN[day_elem],
                "yinYang": "阳" if LunarUtil.GAN.index(ec.getDayGan()) % 2 == 0 else "阴",
                "strength": strength,
                "selfSitting": self_sitting,
            },
            wuxing_scores=wx_scores,
            geju=geju,
            yongshen=yongshen,
            ganzhi_relations=gz_relations,
            branch_relations=zhi_rel,
            spirits=spirits_full,
            bone_weight=bone,
        )

        # 小运（需用神信息）
        xiao_yun = self._calc_xiao_yun(yun, ec, yongshen)

        # 交运时间
        jiao_yun = self._calc_jiao_yun(yun)

        # 黄历信息（可关闭计算）
        huangli = {}
        if not hide.get("huangli", False):
            huangli = self._calc_huangli()

        # 集成所有扩展模块
        sxwnlCalendar = {}
        highPrecisionTime = {}
        astronomicalData = {}
        ziweiChart = {}
        palaceAnalysis = {}
        starInfluence = {}
        starPositions = []
        ziweiHoroscope = {}
        fengshuiCompass = {}
        directionAnalysis = {}
        nineStars = {}
        bagua = {}
        planetPositions = {}
        zodiacSigns = {}
        aspects = {}
        houses = {}
        modernBazi = {}
        typeScriptModel = {}
        apiInterface = {}
        multiCalendar = {}
        holidays = {}
        festivals = {}
        ziweiBasic = {}
        performance = {}
        caching = {}
        optimization = {}

        if not hide.get("extensions", False):
            # === 专业扩展功能 - 强制原生算法，失败即终止 ===
            from fortel_ziwei_integration import FortelZiweiCalculator
            from sxwnl_integration import SXWNLCalculator

            def _run_with_perf(fn, name):
                t0 = time.monotonic()
                try:
                    return fn()
                except Exception as e:
                    raise RuntimeError(f"{name} failed: {e}") from e
                finally:
                    dur = int((time.monotonic() - t0) * 1000)
                    print(f"[PERF] ext {name} {dur}ms")

            sxwnl_result = _run_with_perf(
                lambda: SXWNLCalculator(self.calc_dt, self.longitude).calculate_high_precision_calendar(), "sxwnl"
            )
            ziwei_result = _run_with_perf(
                lambda: FortelZiweiCalculator(self.calc_dt, self.gender, self.longitude).calculate_professional_ziwei(
                    as_of=calc_now
                ),
                "ziwei",
            )
            need_lat = (not hide.get("fengshui", False)) or (not hide.get("astro", False))
            if need_lat and self.latitude is None:
                raise RuntimeError("缺失纬度: 无法启动风水罗盘/天文占星模块")

            fengshui_result = {}
            if not hide.get("fengshui", False):
                from mikaboshi_fengshui_integration import MikaboshiFengshuiCalculator

                fengshui_result = _run_with_perf(
                    lambda: MikaboshiFengshuiCalculator(
                        self.calc_dt, self.longitude, self.latitude
                    ).calculate_fengshui_compass(),
                    "fengshui",
                )

            astro_result = {}
            if not hide.get("astro", False):
                from astro_integration import AstroCalculator

                astro_result = _run_with_perf(
                    lambda: AstroCalculator(
                        self.calc_dt, self.longitude, self.latitude
                    ).calculate_astronomical_positions(),
                    "astro",
                )

            sxwnlCalendar = sxwnl_result.get("sxwnl", {})
            highPrecisionTime = sxwnl_result.get("precision", {})
            astronomicalData = sxwnl_result.get("astronomy", {})

            ziweiChart = ziwei_result.get("professionalZiwei", {})
            palaceAnalysis = ziwei_result.get("palaces", {})
            starInfluence = ziwei_result.get("fiveElementsClass", ziwei_result.get("influence", {}))
            ziweiHoroscope = ziwei_result.get("horoscope", {})

            def _build_star_positions(palaces):
                positions = []
                for p in palaces or []:
                    majors = [s.get("name", "") for s in p.get("majorStars", []) if s]
                    minors = [s.get("name", "") for s in p.get("minorStars", []) if s]
                    adjs = [s.get("name", "") for s in p.get("adjectiveStars", []) if s]
                    positions.append(
                        {
                            "index": p.get("index"),
                            "palace": p.get("name", ""),
                            "heavenlyStem": p.get("heavenlyStem", ""),
                            "earthlyBranch": p.get("earthlyBranch", ""),
                            "isBodyPalace": bool(p.get("isBodyPalace")),
                            "isOriginalPalace": bool(p.get("isOriginalPalace")),
                            "majorStars": majors,
                            "minorStars": minors,
                            "adjectiveStars": adjs,
                        }
                    )
                return positions

            starPositions = _build_star_positions(palaceAnalysis)

            fengshuiCompass = fengshui_result.get("fengshuiCompass", {}) if isinstance(fengshui_result, dict) else {}
            directionAnalysis = fengshui_result.get("directions", {}) if isinstance(fengshui_result, dict) else {}
            nineStars = fengshui_result.get("stars", {}) if isinstance(fengshui_result, dict) else {}
            bagua = fengshui_result.get("bagua", {}) if isinstance(fengshui_result, dict) else {}

            planetPositions = astro_result.get("astronomy", {}) if isinstance(astro_result, dict) else {}
            zodiacSigns = astro_result.get("zodiac", {}) if isinstance(astro_result, dict) else {}
            aspects = astro_result.get("aspects", {}) if isinstance(astro_result, dict) else {}
            houses = astro_result.get("houses", {}) if isinstance(astro_result, dict) else {}

            if not hide.get("system", False):
                # 现代化八字（强制依赖外部 dantalion-master；缺失即终止）
                dantalion_repo = DANTALION_DIR
                dist_js = dantalion_repo / "packages/dantalion-core/dist/index.js"
                if not dist_js.exists():
                    raise RuntimeError(
                        "dantalion-core 未构建（缺少 dist/index.js），请先在 dantalion-master 目录执行构建再重试"
                    )
                from dantalion_integration import DantalionCalculator

                dantalion = DantalionCalculator(self.calc_dt, self.gender)
                dantalion_result = dantalion.calculate_modern_bazi()
                modernBazi = dantalion_result.get("modernBazi", {})
                typeScriptModel = dantalion_result.get("typescript", {})
                apiInterface = dantalion_result.get("api", {})

                from system_optimization import SystemOptimization

                sys_opt = SystemOptimization()
                performance = (
                    sys_opt.get_performance_metrics()
                    if hasattr(sys_opt, "get_performance_metrics")
                    else {"status": "active"}
                )
                caching = sys_opt.get_cache_stats() if hasattr(sys_opt, "get_cache_stats") else {"status": "active"}
                optimization = {"level": "native", "algorithm": "original"}

            if not hide.get("calendar", False):
                from advanced_calendar_integration import AdvancedCalendarCalculator

                calendar_calc = AdvancedCalendarCalculator(calc_now)  # 当前日期的历法
                calendar_result = calendar_calc.calculate_advanced_calendar()
                multiCalendar = calendar_result.get("advancedCalendar", {}).get("multiCalendar", {})
                holidays = calendar_result.get("advancedCalendar", {}).get("holidayCalendar", {})
                festivals = calendar_result.get("advancedCalendar", {}).get("chineseCalendar", {})

            from ziwei import ZiweiCalculator

            ziwei_basic_calc = ZiweiCalculator({"fourPillars": four_pillars}, self.calc_dt, self.gender)
            ziwei_basic_result = ziwei_basic_calc.calculate()
            ziweiBasic = ziwei_basic_result.get("ziwei", {})

        # === 传统命理功能 - 调用原生算法模块 ===
        # 占卜类模块使用当前时间（非出生时间）
        now = calc_now

        meihuaYishu = {}
        numberDivination = {}
        liurenDivination = {}
        qimenDunjia = {}
        mysticalGates = {}
        liuyaoHexagram = {}
        if not hide.get("divination", False):
            from meihua import MeiHuaCalculator

            meihua_calc = MeiHuaCalculator({"fourPillars": four_pillars}, now)  # 当前时间起卦
            meihua_result = meihua_calc.calculate()
            meihuaYishu = meihua_result.get("meihua", {})
            numberDivination = meihua_result.get("meihua", {}).get("wuXingAnalysis", {})

            from liuren import LiurenCalculator

            liuren_calc = LiurenCalculator({"fourPillars": four_pillars})
            liuren_result = liuren_calc.calculate()
            liurenDivination = liuren_result.get("liuren", {})

            from qimen import QimenCalculator

            qimen_calc = QimenCalculator({"fourPillars": four_pillars, "currentTime": now})  # 当前时间排盘
            qimen_result = qimen_calc.calculate()
            qimenDunjia = qimen_result.get("qimen", {})
            mysticalGates = qimen_result.get("qimen", {}).get("bamen", {})

            from liuyao import LiuYaoCalculator

            liuyao_calc = LiuYaoCalculator(
                "命理分析", {"fourPillars": four_pillars, "currentTime": now}
            )  # 当前时间起卦
            liuyao_result = liuyao_calc.calculate()
            liuyaoHexagram = liuyao_result.get("liuyao", {})

        # liuyaoHexagram 已在 divination 分支中计算；关闭时为空 dict

        hexagrams = {}
        yijingAnalysis = {}
        divination = {}
        if not hide.get("yijing", False):
            from enhanced_yijing_integration import EnhancedYijingCalculator

            yijing_calc = EnhancedYijingCalculator(now)  # 当前时间起卦
            yijing_result = yijing_calc.calculate_enhanced_yijing()
            hexagrams = yijing_result.get("enhancedYijing", {}).get("multipleQiGua", {})
            yijingAnalysis = yijing_result.get("enhancedYijing", {})
            divination = yijing_result.get("enhancedYijing", {}).get("philosophicalAnalysis", {})

        dateSelection = {}
        auspiciousDates = []
        if not hide.get("zeri", False):
            from datetime import timedelta

            from zeri import ZeRiCalculator

            zeri_calc = ZeRiCalculator(now, now + timedelta(days=30), "通用")  # 从当前日期开始择日
            zeri_result = zeri_calc.calculate()
            dateSelection = zeri_result.get("zeri", {})
            auspiciousDates = zeri_result.get("zeri", {}).get("recommendedDates", [])

        # 真太阳时细节：严格复用 paipan-master（与 calc_dt 同口径），禁止双口径
        complete_true_solar_time = self.true_solar_detail
        zi_time_analysis = self.zi_time_analysis

        # 姓名合婚需要姓名、配偶八字等独立输入契约；标准排盘不输出占位结果。
        marriageCompatibility = {}
        baziMatching = {}
        nameAnalysis = {}
        fiveGrids = {}
        strokeAnalysis = {}

        # ====== 大运 / 流年 神煞 ======
        base_day_gan = ec.getDayGan()
        base_day_zhi = ec.getDayZhi()
        base_month_zhi = ec.getMonthZhi()
        base_year_zhi = ec.getYearZhi()
        major_spirits = []
        for dy in major_with_shishen.get("pillars", []):
            if not isinstance(dy, dict):
                continue
            gz = dy.get("ganZhi") or dy.get("fullName", "") or ""
            if len(gz) >= 2:
                gan, zhi = gz[0], gz[1]
                s_list = self._calc_spirits_for_ganzhi(
                    gan, zhi, base_day_gan, base_day_zhi, base_month_zhi, base_year_zhi
                )
                major_spirits.append(
                    {
                        "startYear": dy.get("startYear"),
                        "ganZhi": gz,
                        "spirits": s_list,
                        "wuxingContribution": self._calc_wuxing_contrib(gan, zhi),
                    }
                )
        annual_spirits = []
        for an in annual_with_shishen:
            if not isinstance(an, dict):
                continue
            gz = an.get("ganZhi") or an.get("fullName", "") or ""
            if len(gz) >= 2:
                gan, zhi = gz[0], gz[1]
                s_list = self._calc_spirits_for_ganzhi(
                    gan, zhi, base_day_gan, base_day_zhi, base_month_zhi, base_year_zhi
                )
                annual_spirits.append({"year": an.get("year"), "ganZhi": gz, "spirits": s_list})
        monthly_spirits = []
        for mo in monthly:
            if not isinstance(mo, dict):
                continue
            gz = mo.get("ganZhi", "") or ""
            if len(gz) >= 2:
                gan, zhi = gz[0], gz[1]
                s_list = self._calc_spirits_for_ganzhi(
                    gan, zhi, base_day_gan, base_day_zhi, base_month_zhi, base_year_zhi
                )
                monthly_spirits.append(
                    {
                        "year": mo.get("year", ""),
                        "month": mo.get("month", mo.get("monthCn", "")),
                        "monthCn": mo.get("monthCn", ""),
                        "ganZhi": gz,
                        "spirits": s_list,
                    }
                )

        # 构建结果
        sizi_summary = self._calc_sizi_summary(four_pillars)
        result = {
            # 用户传参
            "input": {
                "name": self.name,
                "gender": "male" if self.gender == "male" else "female",
                "birthDate": self.birth_dt.strftime("%Y-%m-%d"),
                "birthTime": self.birth_dt.strftime("%H:%M"),
                "birthPlace": self.birth_place,
                "longitude": self.longitude,
                "latitude": self.latitude,
                "options": {"useTrueSolarTime": True, "calendarType": "solar"},
            },
            "inputTrace": {
                "originalTime": self.birth_dt.strftime("%Y-%m-%d %H:%M:%S"),
                "trueSolarTime": self.true_solar_time.strftime("%Y-%m-%d %H:%M:%S"),
                "useTrueSolarTime": self.use_true_solar_time,
                "longitude": self.longitude,
                "latitude": self.latitude,
                "timeZhi": self.zi_time_analysis.get("timeZhi", ""),
                "ziTimeAnalysis": self.zi_time_analysis,
                "trueSolarDetail": complete_true_solar_time,
                "fixLeap": True,
            },
            # 计算信息
            "meta": {
                "trueSolarTime": self.true_solar_time.strftime("%Y-%m-%d %H:%M:%S"),
                "calculateTime": fmt_cn(calc_now, "%Y-%m-%d %H:%M:%S"),
                "genderCn": "乾造(男)" if self.gender == "male" else "坤造(女)",
            },
            "fourPillars": four_pillars,
            "hiddenStems": hidden,
            "tenGods": ten_gods,
            "twelveGrowth": twelve,
            "fiveElements": five_elem,
            "wuxingState": wuxing_state,
            "specialPalaces": palaces,
            "voidInfo": void,
            "spirits": spirits,
            "spiritsFull": spirits_full,
            "spiritsExplain": spirits_explain,
            "dayMaster": {
                "stem": ec.getDayGan(),
                "element": day_elem,
                "elementCn": ELEM_CN[day_elem],
                "yinYang": "阳" if LunarUtil.GAN.index(ec.getDayGan()) % 2 == 0 else "阴",
                "strength": strength,
                "selfSitting": self_sitting,
            },
            "ganzhiRelations": gz_relations,
            "ganzhiImagery": ganzhi_imagery,
            "ganzhiExtra": gz_extra,
            "branchRelations": zhi_rel,
            "wuxingScores": wx_scores,
            "climateScores": climate,
            "wuxingHealthTips": wuxing_health,
            "majorFortune": major_with_shishen,
            "majorFortuneSpirits": major_spirits,
            "annualFortune": annual_with_shishen,
            "annualSpirits": annual_spirits,
            "monthlyFortune": monthly,
            "monthlySpirits": monthly_spirits,
            "boneWeight": bone,
            "mingGua": ming_gua,
            "birthInfo": self._get_birth_info(),
            "jieqiDetail": jieqi_detail,
            "siling": siling,
            "geju": geju,
            "xiaoYun": xiao_yun,
            "jiaoYun": jiao_yun,
            "trueSolarTime": self.true_solar_time.strftime("%Y-%m-%d %H:%M:%S"),
            "yongShen": yongshen,
            "analysisEvidence": analysis_evidence,
            "siziSummary": sizi_summary,
            "huangLi": huangli,
            # 专业扩展功能 (27个字段)
            "sxwnlCalendar": sxwnlCalendar,
            "highPrecisionTime": highPrecisionTime,
            "astronomicalData": astronomicalData,
            "ziweiChart": ziweiChart,
            "starPositions": starPositions,
            "palaceAnalysis": palaceAnalysis,
            "starInfluence": starInfluence,
            "ziweiHoroscope": ziweiHoroscope,
            "fengshuiCompass": fengshuiCompass,
            "directionAnalysis": directionAnalysis,
            "nineStars": nineStars,
            "bagua": bagua,
            "planetPositions": planetPositions,
            "zodiacSigns": zodiacSigns,
            "aspects": aspects,
            "houses": houses,
            "modernBazi": modernBazi,
            "typeScriptModel": typeScriptModel,
            "apiInterface": apiInterface,
            "multiCalendar": multiCalendar,
            "holidays": holidays,
            "festivals": festivals,
            "hexagrams": hexagrams,
            "yijingAnalysis": yijingAnalysis,
            "divination": divination,
            "performance": performance,
            "caching": caching,
            "optimization": optimization,
            # 传统命理功能 (14个字段)
            "marriageCompatibility": marriageCompatibility,
            "baziMatching": baziMatching,
            "nameAnalysis": nameAnalysis,
            "fiveGrids": fiveGrids,
            "strokeAnalysis": strokeAnalysis,
            "liuyaoHexagram": liuyaoHexagram,
            "meihuaYishu": meihuaYishu,
            "numberDivination": numberDivination,
            "dateSelection": dateSelection,
            "auspiciousDates": auspiciousDates,
            "qimenDunjia": qimenDunjia,
            "mysticalGates": mysticalGates,
            "liurenDivination": liurenDivination,
            "ziweiBasic": ziweiBasic,
            "completeTrueSolarTime": complete_true_solar_time,
            "ziTimeAnalysis": zi_time_analysis,
        }

        # 全局翻译英文为中文
        result = self._translate_to_chinese(result)
        return self._json_safe(result)

    def _translate_to_chinese(self, obj):
        """递归翻译英文值为中文"""
        EN_CN = {
            "origin": "本命",
            "major": "主星",
            "soft": "吉星",
            "tough": "煞星",
            "lucun": "禄存",
            "tianma": "天马",
            "success": "成功",
            "active": "启用",
            "male": "男",
            "female": "女",
            "astronomical": "天文级",
            "normal": "正常",
            "placidus": "普拉西德",
            "native": "原生",
            "original": "原生",
            "compatible": "兼容",
        }
        if isinstance(obj, dict):
            return {k: self._translate_to_chinese(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._translate_to_chinese(v) for v in obj]
        elif isinstance(obj, str) and obj in EN_CN:
            return EN_CN[obj]
        return obj

    def _json_safe(self, obj):
        """递归将 datetime 等不可序列化对象转为字符串"""
        from datetime import datetime

        if isinstance(obj, dict):
            return {k: self._json_safe(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [self._json_safe(v) for v in obj]
        if isinstance(obj, datetime):
            return obj.isoformat()
        return obj

    def calculate_complete(self) -> dict[str, Any]:
        result = {}

        # Phase 1: 寿星万年历高精度历法
        spec = importlib.util.spec_from_file_location("sxwnl_integration", str(SRC_DIR / "sxwnl_integration.py"))
        sxwnl_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(sxwnl_module)
        sxwnl_calc = sxwnl_module.SXWNLCalculator(self.calc_dt, self.longitude)
        sxwnl_result = sxwnl_calc.get_complete_analysis()
        result.update(sxwnl_result)

        # Phase 2: 专业紫微斗数系统
        spec = importlib.util.spec_from_file_location(
            "fortel_ziwei_integration", str(SRC_DIR / "fortel_ziwei_integration.py")
        )
        fortel_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(fortel_module)
        fortel_calc = fortel_module.FortelZiweiCalculator(self.calc_dt, self.gender, self.longitude)
        fortel_result = fortel_calc.calculate_complete_ziwei_system()
        result.update(fortel_result)

        # Phase 3: 风水罗盘系统
        spec = importlib.util.spec_from_file_location(
            "mikaboshi_fengshui_integration", str(SRC_DIR / "mikaboshi_fengshui_integration.py")
        )
        fengshui_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(fengshui_module)
        # 严格使用已解析的经纬度，不做“地点回退/猜测”
        latitude = getattr(self, "latitude", None)
        if latitude is None:
            raise RuntimeError("缺失纬度: 无法启动风水/占星模块")
        fengshui_calc = fengshui_module.MikaboshiFengshuiCalculator(self.calc_dt, self.longitude, latitude)
        fengshui_result = fengshui_calc.calculate_complete_fengshui_system()
        result.update(fengshui_result)

        # Phase 4: 天文占星计算
        spec = importlib.util.spec_from_file_location("astro_integration", str(SRC_DIR / "astro_integration.py"))
        astro_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(astro_module)
        astro_calc = astro_module.AstroCalculator(self.calc_dt, self.longitude, latitude)
        astro_result = astro_calc.get_complete_astro_analysis()
        result.update(astro_result)

        # Phase 5: 现代化八字重构
        spec = importlib.util.spec_from_file_location(
            "dantalion_integration", str(SRC_DIR / "dantalion_integration.py")
        )
        dantalion_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(dantalion_module)
        dantalion_calc = dantalion_module.DantalionCalculator(self.calc_dt, self.gender)
        dantalion_result = dantalion_calc.get_complete_modern_analysis()
        result.update(dantalion_result)

        # bazi-1完整五行评分系统
        spec = importlib.util.spec_from_file_location("bazi1_integration", str(SRC_DIR / "bazi1_integration.py"))
        bazi1_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(bazi1_module)
        bazi1_calc = bazi1_module.Bazi1Integration(result["fourPillars"])
        bazi1_result = bazi1_calc.get_complete_analysis()
        result.update(bazi1_result)

        # 完整真太阳时计算
        spec = importlib.util.spec_from_file_location("true_solar_time", str(SRC_DIR / "true_solar_time.py"))
        tst_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(tst_module)
        tst_calc = tst_module.TrueSolarTimeCalculator(self.birth_dt, self.longitude)
        tst_result = tst_calc.calculate_true_solar_time()
        zi_result = tst_calc.calculate_early_late_zi_time()
        result["completeTrueSolarTime"] = tst_result
        result["ziTimeAnalysis"] = zi_result

        # 奇门遁甲
        spec = importlib.util.spec_from_file_location("qimen", str(SRC_DIR / "qimen.py"))
        qimen_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(qimen_module)
        qimen_calc = qimen_module.QimenCalculator(result)
        result.update(qimen_calc.calculate())

        # 紫微斗数 (基础版，与专业版并存)
        spec = importlib.util.spec_from_file_location("ziwei", str(SRC_DIR / "ziwei.py"))
        ziwei_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(ziwei_module)
        ziwei_calc = ziwei_module.ZiweiCalculator(result, self.calc_dt, self.gender)
        result.update(ziwei_calc.calculate())

        # 大六壬
        spec = importlib.util.spec_from_file_location("liuren", str(SRC_DIR / "liuren.py"))
        liuren_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(liuren_module)
        liuren_calc = liuren_module.LiurenCalculator(result)
        result.update(liuren_calc.calculate())

        return result

    def _get_birth_info(self) -> dict:
        """出生信息"""
        prev_jq = self.lunar.getPrevJieQi()
        next_jq = self.lunar.getNextJieQi()
        return {
            "solar": self.birth_dt.strftime("%Y-%m-%d %H:%M"),
            "trueSolarTime": self.true_solar_time.strftime("%Y-%m-%d %H:%M"),
            "lunar": self.lunar.toString(),
            "lunarCn": f"{self.lunar.getYearInChinese()}年{self.lunar.getMonthInChinese()}月{self.lunar.getDayInChinese()}",
            "zodiac": self.lunar.getYearShengXiao(),
            "constellation": self.solar.getXingZuo(),
            "xiu": self.lunar.getXiu(),
            "xingXiu": f"{self.lunar.getXiu()}宿{self.lunar.getZheng()}方{self.lunar.getAnimal()}",
            "prevJieQi": prev_jq.getName() if prev_jq else "",
            "nextJieQi": next_jq.getName() if next_jq else "",
        }

    def _calc_huangli(self) -> dict:
        """黄历信息"""
        return {
            "yi": self.lunar.getDayYi(),  # 宜
            "ji": self.lunar.getDayJi(),  # 忌
            "jiShen": self.lunar.getDayJiShen(),  # 吉神
            "xiongSha": self.lunar.getDayXiongSha(),  # 凶煞
            "pengZu": f"{self.lunar.getPengZuGan()} {self.lunar.getPengZuZhi()}",  # 彭祖百忌
            "chong": self.lunar.getDayChongDesc(),  # 冲
            "sha": self.lunar.getDaySha(),  # 煞
            "taiShen": self.lunar.getDayPositionTai(),  # 胎神
            "zhiXing": self.lunar.getZhiXing(),  # 值星
        }

    def _pillar(self, full: str, stem: str, branch: str) -> dict:
        return {
            "stem": stem,
            "branch": branch,
            "fullName": full,
            "nayin": LunarUtil.NAYIN.get(full, ""),
            "stemElement": STEM_ELEM.get(stem, ""),
            "branchElement": BRANCH_ELEM.get(branch, ""),
        }

    def _calc_elements(self, pillars: dict, hidden: dict) -> dict:
        elems = {"木": [], "火": [], "土": [], "金": [], "水": []}
        for pos, p in pillars.items():
            elem = p["stemElement"]
            elems[elem].append(f"{pos}干{p['stem']}")
            for h in hidden.get(pos, []):
                elems[STEM_ELEM[h]].append(f"{pos}支藏{h}")
        total = sum(len(v) for v in elems.values())
        return {
            e: {"count": len(v), "percentage": round(len(v) / total * 100, 1) if total else 0, "items": v}
            for e, v in elems.items()
        }

    def _calc_fortune(self, yun) -> dict:
        da_yuns = yun.getDaYun()
        start_y, start_m, start_d = yun.getStartYear(), yun.getStartMonth(), yun.getStartDay()
        start_age = start_y + (1 if start_m >= 6 else 0)
        pillars = []
        for dy in da_yuns[1:11]:
            gz = dy.getGanZhi()
            if gz:
                pillars.append(
                    {
                        "age": dy.getStartAge(),
                        "startYear": dy.getStartYear(),
                        "stem": gz[0],
                        "branch": gz[1],
                        "fullName": gz,
                        "startDate": "",
                    }
                )
        return {
            "direction": "顺行" if yun.isForward() else "逆行",
            "startAge": start_age,
            "startYear": da_yuns[1].getStartYear() if len(da_yuns) > 1 else 0,
            "startDetail": f"{start_y}年{start_m}月{start_d}天",
            "pillars": pillars,
        }

    def _calc_annual(self) -> list[dict]:
        """
        生成“全生命周期”流年列表
        - 基于 lunar-python 的大运/流年原生接口
        - 覆盖全部大运年份，不再仅限未来10年
        - 按年份升序去重
        """
        yun = self.ec.getYun(1 if self.gender == "male" else 0)
        da_yuns = yun.getDaYun()
        result = []
        seen = set()
        for dy in da_yuns:
            for ln in dy.getLiuNian():
                year = ln.getYear()
                gz = ln.getGanZhi()
                if not gz:
                    continue
                if year in seen:
                    continue
                seen.add(year)
                result.append({"year": year, "stem": gz[0], "branch": gz[1], "fullName": gz})
        # 禁止兜底/回退：原生接口无结果即视为计算失败
        if not result:
            raise RuntimeError("流年计算失败: lunar-python 原生接口未返回任何流年数据")
        # 按年份升序
        result.sort(key=lambda x: x["year"])
        return result

    def _calc_monthly(self, yun) -> list[dict]:
        """
        全量流月
        - 遍历所有大运 → 流年 → 流月
        - 去重、按年份+月份升序
        """
        da_yuns = yun.getDaYun()
        if not da_yuns:
            return []
        seen = set()
        result = []
        for dy in da_yuns:
            for ln in dy.getLiuNian():
                year = ln.getYear()
                for ly in ln.getLiuYue():
                    month_idx = ly.getIndex() + 1
                    key = (year, month_idx)
                    if key in seen:
                        continue
                    seen.add(key)
                    result.append(
                        {
                            "year": year,
                            "month": month_idx,
                            "monthCn": ly.getMonthInChinese(),
                            "ganZhi": ly.getGanZhi(),
                            "stem": ly.getGanZhi()[0],
                            "branch": ly.getGanZhi()[1],
                        }
                    )
        result.sort(key=lambda x: (x["year"], x["month"]))
        return result

    def _calc_all_spirits(self, ec) -> dict:
        """
        全量神煞（bazi-1 原生映射）
        对齐 bazi-1-master/bazi.py:get_shens 逻辑，使用 datas.py 中 year_shens/month_shens/day_shens/g_shens
        """
        by_pillar = {"year": [], "month": [], "day": [], "hour": []}
        desc_map = {}

        branches = {
            "year": ec.getYearZhi(),
            "month": ec.getMonthZhi(),
            "day": ec.getDayZhi(),
            "hour": ec.getTimeZhi(),
        }
        stems = {
            "year": ec.getYearGan(),
            "month": ec.getMonthGan(),
            "day": ec.getDayGan(),
            "hour": ec.getTimeGan(),
        }
        me = ec.getDayGan()
        month_br = ec.getMonthZhi()
        day_br = ec.getDayZhi()

        for pillar in by_pillar.keys():
            gan_ = stems[pillar]
            zhi_ = branches[pillar]

            # 年支系
            for name, mp in year_shens.items():
                if zhi_ in mp.get(branches["year"], ""):
                    by_pillar[pillar].append(name)

            # 月支系
            for name, mp in month_shens.items():
                val = mp.get(month_br, "")
                if (gan_ and gan_ in val) or (zhi_ and zhi_ in val):
                    by_pillar[pillar].append(name)

            # 日支系
            for name, mp in day_shens.items():
                val = mp.get(day_br, "")
                if zhi_ and zhi_ in val:
                    by_pillar[pillar].append(name)

            # 日主系
            for name, mp in g_shens.items():
                val = mp.get(me, "")
                if zhi_ and zhi_ in val:
                    by_pillar[pillar].append(name)

        # 去重保持顺序，并收集描述
        for k, v in by_pillar.items():
            seen = set()
            uniq = []
            for item in v:
                if item in seen:
                    continue
                seen.add(item)
                uniq.append(item)
            by_pillar[k] = uniq
            for item in uniq:
                if item in shens_infos:
                    desc_map[item] = shens_infos[item]

        return {"byPillar": by_pillar, "descriptions": desc_map}

    def _calc_spirits_explain(self, spirits_full: dict) -> dict[str, str]:
        """神煞释义（仅展开本盘出现的神煞）。

        说明：
        - 严格复用 bazi-1 的 `datas.shens_infos`。
        - 不做额外推断，不引入新口径。
        """
        if not isinstance(spirits_full, dict):
            return {}
        desc = spirits_full.get("descriptions")
        return desc if isinstance(desc, dict) else {}

    def _calc_ganzhi_imagery(self, pillars: dict) -> dict[str, Any]:
        """干支取象（bazi-1 原生字典 gan_desc / zhi_desc）。"""
        out: dict[str, Any] = {}
        for pos in ["year", "month", "day", "hour"]:
            p = pillars.get(pos, {}) if isinstance(pillars, dict) else {}
            gan = p.get("stem", "")
            zhi = p.get("branch", "")
            out[pos] = {
                "stem": gan,
                "stemImagery": (gan_desc.get(gan, "") or "").strip(),
                "branch": zhi,
                "branchImagery": (zhi_desc.get(zhi, "") or "").strip(),
            }
        return out

    def _calc_wuxing_health_tips(self) -> dict[str, str]:
        """五行健康/开运提示（bazi-1 原生字典 gan_health）。

        注意：
        - 仅输出原文，不做“按分数归因”的自写推断。
        """
        out: dict[str, str] = {}
        if not isinstance(gan_health, dict):
            return out
        for k, v in gan_health.items():
            if not k:
                continue
            out[str(k)] = (v or "").strip() if isinstance(v, str) else str(v)
        return out

    def _calc_spirits_for_ganzhi(
        self,
        gan: str,
        zhi: str,
        ref_day_gan: str,
        ref_day_zhi: str,
        ref_month_zhi: str = None,
        ref_year_zhi: str = None,
    ) -> list:
        """
        针对单个干支（用于大运/流年），复用 bazi-1 神煞映射，参考本命年支/月支/日干/日支。
        """
        res = []
        ref_month_zhi = ref_month_zhi or zhi
        ref_year_zhi = ref_year_zhi or zhi
        ref_day_zhi = ref_day_zhi or zhi
        # 年支系
        for name, mp in year_shens.items():
            if zhi in mp.get(ref_year_zhi, ""):
                res.append(name)
        # 月支系
        for name, mp in month_shens.items():
            val = mp.get(ref_month_zhi, "")
            if (gan and gan in val) or (zhi and zhi in val):
                res.append(name)
        # 日支系
        for name, mp in day_shens.items():
            val = mp.get(ref_day_zhi, "")
            if zhi and zhi in val:
                res.append(name)
        # 日主系
        for name, mp in g_shens.items():
            val = mp.get(ref_day_gan, "")
            if zhi and zhi in val:
                res.append(name)
        uniq = []
        seen = set()
        for s in res:
            if s in seen:
                continue
            seen.add(s)
            uniq.append(s)

        return uniq

    def _calc_ganzhi_extra(self, pillars: dict, hidden: dict[str, list[str]] = None) -> dict:
        """
        干支合/克/入库 等扩展关系
        逻辑对齐 bazi-1-master/bazi.py 中的 gan_zhi_he / gan_ke / zhi_ku，
        直接复用同一数据表 ten_deities / zhi5，保持原始判定规则。
        """
        hidden = hidden or {}
        result = {
            "he": {},  # 干支是否相合
            "heDetail": {},  # 干支相合依据
            "ke": [],  # 天干相克列表
            "keDetail": [],  # 天干相克依据（带柱位）
            "ku": {},  # 地支入库
            "kuDetail": {},  # 地支入库依据
        }

        def gan_zhi_he_fn(zhu):
            gan, zhi = zhu
            return ten_deities[gan]["合"] in zhi5[zhi]

        def gan_ke_dir(gan1, gan2):
            """
            天干相克方向判定（依据 bazi-1 datas.ten_deities 结构）：
            - 若 gan1['克'] == gan2['本']，则 gan1 克 gan2
            - 若 gan2['克'] == gan1['本']，则 gan2 克 gan1
            说明：bazi-1 的 gan_ke() 是“是否存在相克”，这里补齐方向信息以便“依据版”输出。
            """
            out = []
            if ten_deities[gan1]["克"] == ten_deities[gan2]["本"]:
                out.append((gan1, gan2))
            if ten_deities[gan2]["克"] == ten_deities[gan1]["本"]:
                out.append((gan2, gan1))
            return out

        def zhi_ku_fn(zhi, items):
            if zhi not in "辰戌丑未":
                return False
            return min(zhi5[zhi], key=zhi5[zhi].get) in items

        # 干支相合：每柱干支
        for pillar, p in pillars.items():
            stem = p.get("stem")
            branch = p.get("branch")
            if stem and branch:
                try:
                    he_gan = ten_deities[stem]["合"]
                    zhi_hidden_score = zhi5.get(branch, {}) if branch in zhi5 else {}
                    zhi_hidden = list(zhi_hidden_score.keys()) if isinstance(zhi_hidden_score, dict) else []
                    hit = bool(gan_zhi_he_fn((stem, branch)))
                    result["he"][pillar] = hit
                    result["heDetail"][pillar] = {
                        "ganZhi": f"{stem}{branch}",
                        "gan": stem,
                        "zhi": branch,
                        "heGan": he_gan,
                        "zhiHidden": zhi_hidden,
                        "zhiHiddenScore": zhi_hidden_score,
                        "hitItem": he_gan if hit else "",
                        "hit": hit,
                    }
                except Exception as e:
                    raise RuntimeError(f"干支相合计算失败: pillar={pillar} stem={stem} branch={branch}: {e}") from e

        # 天干相克：两两组合
        order = ["year", "month", "day", "hour"]
        named_stems = [(k, pillars.get(k, {}).get("stem")) for k in order]
        named_stems = [(k, v) for k, v in named_stems if v]
        n = len(named_stems)
        for i in range(n):
            for j in range(i + 1, n):
                pa, a = named_stems[i]
                pb, b = named_stems[j]
                try:
                    for g_from, g_to in gan_ke_dir(a, b):
                        # 用 “柱位 + 天干” 输出，便于报告展开
                        if g_from == a and g_to == b:
                            result["ke"].append(f"{a}克{b}")
                            result["keDetail"].append(
                                {"from": pa, "to": pb, "text": f"{pa}干{a}克{pb}干{b}", "ganFrom": a, "ganTo": b}
                            )
                        elif g_from == b and g_to == a:
                            result["ke"].append(f"{b}克{a}")
                            result["keDetail"].append(
                                {"from": pb, "to": pa, "text": f"{pb}干{b}克{pa}干{a}", "ganFrom": b, "ganTo": a}
                            )
                except Exception as e:
                    raise RuntimeError(f"天干相克计算失败: {pa}干{a} vs {pb}干{b}: {e}") from e
        # 去重（保持顺序）
        seen = set()
        uniq = []
        for item in result["keDetail"]:
            txt = item.get("text", "")
            if not txt or txt in seen:
                continue
            seen.add(txt)
            uniq.append(item)
        result["keDetail"] = uniq

        # 地支入库：每柱地支
        ku_element_map = {"辰": "水", "戌": "火", "丑": "金", "未": "木"}
        for pillar, p in pillars.items():
            branch = p.get("branch")
            if branch:
                try:
                    hiddens = hidden.get(pillar, []) if isinstance(hidden, dict) else []
                    is_ku = branch in "辰戌丑未"
                    zhi_hidden_score = zhi5.get(branch, {}) if branch in zhi5 else {}
                    weakest = (
                        min(zhi_hidden_score, key=zhi_hidden_score.get)
                        if is_ku and isinstance(zhi_hidden_score, dict) and zhi_hidden_score
                        else ""
                    )
                    weakest_score = (
                        zhi_hidden_score.get(weakest) if weakest and isinstance(zhi_hidden_score, dict) else None
                    )
                    in_ku = bool(zhi_ku_fn(branch, hiddens or []))
                    result["ku"][pillar] = in_ku
                    result["kuDetail"][pillar] = {
                        "zhi": branch,
                        "isKu": is_ku,
                        "kuElement": ku_element_map.get(branch, "") if is_ku else "",
                        "weakestGan": weakest,
                        "weakestScore": weakest_score,
                        "hidden": hiddens or [],
                        "zhiHiddenScore": zhi_hidden_score,
                        "hitItem": weakest if in_ku else "",
                        "hit": in_ku,
                    }
                except Exception as e:
                    raise RuntimeError(f"地支入库计算失败: pillar={pillar} branch={branch}: {e}") from e

        return result

    def _calc_wuxing_scores(self, pillars: dict) -> dict:
        """
        五行分数、天干分数、身强判断
        对齐 bazi-1-master/bazi.py 的 scores / gan_scores / weak / strong 计算思路
        """
        scores = {"金": 0, "木": 0, "水": 0, "火": 0, "土": 0}
        gan_scores = dict.fromkeys("甲乙丙丁戊己庚辛壬癸", 0)

        stems = [p.get("stem") for p in pillars.values() if p.get("stem")]
        branches = [p.get("branch") for p in pillars.values() if p.get("branch")]

        # 干加基分
        for gan in stems:
            scores[gan5[gan]] += 5
            gan_scores[gan] += 5

        # 支累加（含日月支，同源逻辑：list(zhis)+[zhis.month]）
        for zhi in branches + (branches[1:2]):  # 月支再加一次
            for gan in zhi5[zhi]:
                scores[gan5[gan]] += zhi5[zhi][gan]
                gan_scores[gan] += zhi5[zhi][gan]

        # 身强弱：参考 bazi.py weak 判定（简化为：有长/帝/建则偏强；否则看比/劫+库数量）
        day_stem = pillars["day"]["stem"]
        me_status = []
        weak = True
        for zhi in branches:
            me_status.append(ten_deities[day_stem][zhi])
            if ten_deities[day_stem][zhi] in ("长", "帝", "建"):
                weak = False
        if weak:
            if me_status.count("库") + sum(1 for g in stems if ten_deities[day_stem][g] in ("比", "劫")) > 2:
                weak = False

        # bazi-1 原生 raw score：比/劫/枭/印 四项总和
        me_attrs = ten_deities[day_stem].inverse
        strong_score = (
            gan_scores[me_attrs["比"]]
            + gan_scores[me_attrs["劫"]]
            + gan_scores[me_attrs["枭"]]
            + gan_scores[me_attrs["印"]]
        )

        def _status_summary(seq):
            if not seq:
                return ""
            fav = ("长", "帝", "建", "旺", "相")
            score = sum(1 for s in seq if s in fav)
            return f"强势位{score}处 / 共{len(seq)}处"

        strength_label = self._map_strength_label(weak=weak, strong_score=strong_score)

        return {
            "fiveElementScore": scores,
            "ganScore": gan_scores,
            "weak": weak,
            "strongScore": strong_score,
            "weakStrong": strength_label,
            "statusDetail": me_status,
            "statusSummary": _status_summary(me_status),
        }

    @staticmethod
    def _map_strength_label(*, weak: bool, strong_score: int) -> str:
        """
        将 bazi-1 原生 strong score 归一到五档展示口径。

        归一策略：
        1. 先尊重 bazi-1 原生 weak 布尔值，避免出现“weak=True 但标签偏强”的矛盾。
        2. 再用 strong score 细分到五档展示口径。
        3. 上游 README 中“通常 >29 为强”仅作为分带经验线，不覆盖 weak 的最终判定。
        """
        if weak:
            if strong_score <= 20:
                return "身弱"
            if strong_score <= 28:
                return "中和偏弱"
            return "中和"

        if strong_score <= 25:
            return "中和偏弱"
        if strong_score <= 33:
            return "中和"
        if strong_score <= 37:
            return "中和偏强"
        return "身强"

    def _calc_wuxing_contrib(self, gan: str, zhi: str) -> dict:
        """
        单柱五行贡献（含藏干，口径与 _calc_wuxing_scores 保持一致）
        """
        scores = {"金": 0, "木": 0, "水": 0, "火": 0, "土": 0}
        if gan in gan5:
            scores[gan5[gan]] += 5
        if zhi in zhi5:
            for hgan, w in zhi5[zhi].items():
                scores[gan5[hgan]] += w
        return scores

    def _calc_zhi_relations(self, pillars: dict) -> dict:
        """
        地支六合 / 三会 / 三合 / 破害刑冲 关系
        直接读取 bazi-1-master/ganzhi.py 中的表：zhi_6hes, zhi_huis, zhi_3hes, zhi_atts
        """
        try:
            from ganzhi import zhi_3hes, zhi_6hes, zhi_atts, zhi_huis
        except Exception as e:
            raise RuntimeError(f"地支关系数据表导入失败: {e}") from e

        pos_order = ["year", "month", "day", "hour"]
        branches_by_pos = [(p, pillars[p]["branch"]) for p in pos_order if pillars.get(p)]
        branches = [b for _, b in branches_by_pos]
        pos_name = {"year": "年", "month": "月", "day": "日", "hour": "时"}
        zhi_pos_map: dict[str, list[str]] = {}
        for p, b in branches_by_pos:
            zhi_pos_map.setdefault(b, []).append(p)

        result = {
            "liuHe": [],
            "liuHeDetail": [],
            "sanHui": [],
            "sanHuiDetail": [],
            "sanHe": [],
            "sanHeDetail": [],
            "conflicts": [],
            "conflictsDetail": [],
        }

        # 六合判断：任意两支匹配表
        for i in range(len(branches_by_pos)):
            for j in range(i + 1, len(branches_by_pos)):
                pa, a = branches_by_pos[i]
                pb, b = branches_by_pos[j]
                key = a + b
                key_rev = b + a
                elem = ""
                if key in zhi_6hes:
                    elem = zhi_6hes.get(key, "")
                elif key_rev in zhi_6hes:
                    elem = zhi_6hes.get(key_rev, "")
                else:
                    continue
                result["liuHe"].append(f"{a}{b}({elem})" if elem else f"{a}{b}")
                result["liuHeDetail"].append(
                    {
                        "text": f"{pos_name.get(pa, pa)}支{a}与{pos_name.get(pb, pb)}支{b}六合{('(' + elem + ')') if elem else ''}",
                        "a": a,
                        "b": b,
                        "pa": pa,
                        "pb": pb,
                        "element": elem,
                    }
                )

        # 三会：三支组成表中的 key
        branch_set = set(branches)
        for key, val in zhi_huis.items():
            if set(key).issubset(branch_set):
                result["sanHui"].append(f"{key}({val})")
                parts = []
                for ch in key:
                    poss = zhi_pos_map.get(ch, [])
                    pos_txt = "".join([pos_name.get(p, p) for p in poss]) if poss else ""
                    parts.append({"zhi": ch, "pos": poss, "posCn": pos_txt})
                result["sanHuiDetail"].append(
                    {
                        "pattern": key,
                        "element": val,
                        "parts": parts,
                        "text": "三会：" + "".join([f"{x['zhi']}({x['posCn']})" for x in parts]) + f" => {val}",
                    }
                )

        # 三合：按 zhi_3hes key（两支+长生支）
        for k, v in zhi_3hes.items():
            if set(k).issubset(set(branches)):
                result["sanHe"].append(f"{k}({v})")
                parts = []
                for ch in k:
                    poss = zhi_pos_map.get(ch, [])
                    pos_txt = "".join([pos_name.get(p, p) for p in poss]) if poss else ""
                    parts.append({"zhi": ch, "pos": poss, "posCn": pos_txt})
                result["sanHeDetail"].append(
                    {
                        "pattern": k,
                        "value": v,
                        "parts": parts,
                        "text": "三合：" + "".join([f"{x['zhi']}({x['posCn']})" for x in parts]) + f" => {v}",
                    }
                )

        # 冲/刑/害/破
        for pa, a in branches_by_pos:
            att = zhi_atts.get(a, {})
            for rel_key, target in att.items():
                if not target:
                    continue
                target_set = target if isinstance(target, tuple) else (target,)
                matched = [t for t in target_set if t in branch_set]
                if not matched:
                    continue
                # 保持旧输出（不带柱位）
                result["conflicts"].append(f"{a}{rel_key}{''.join(matched)}")
                # 依据输出：带柱位与匹配详情
                to_parts = []
                for t in matched:
                    poss = zhi_pos_map.get(t, []) or [""]
                    for pb in poss:
                        to_parts.append({"pos": pb, "posCn": pos_name.get(pb, pb), "zhi": t})
                full = len(matched) == len(target_set)
                result["conflictsDetail"].append(
                    {
                        "from": pa,
                        "fromZhi": a,
                        "rel": rel_key,
                        "to": matched,
                        "full": full,
                        "text": f"{pos_name.get(pa, pa)}支{a}{rel_key}"
                        + "".join([f"{x['posCn']}支{x['zhi']}" for x in to_parts])
                        + ("" if full else "（半）"),
                    }
                )

        # 去重
        for k in ["liuHe", "sanHui", "sanHe", "conflicts"]:
            result[k] = list(dict.fromkeys(result[k]))
        for k in ["liuHeDetail", "sanHuiDetail", "sanHeDetail", "conflictsDetail"]:
            seen = set()
            uniq = []
            for item in result.get(k, []):
                txt = item.get("text") if isinstance(item, dict) else str(item)
                if not txt or txt in seen:
                    continue
                seen.add(txt)
                uniq.append(item)
            result[k] = uniq

        return result

    def _calc_climate_scores(self, pillars: dict) -> dict:
        """
        温湿度分数（暖燥/寒湿）+ 拱神（三会补缺）
        约束：禁止“复刻公式/自写口径”。
        实现：直接调用 bazi-1-master/bazi.py 的原生输出并解析（作为事实来源）。
        备注：空亡命中仍复用 bazi-1-master/common.py 的 get_empty（外部库原生函数）。
        """
        # -------------------- 1) 解析 bazi.py 原生“湿度分数/拱” --------------------
        if not isinstance(pillars, dict) or not pillars:
            raise RuntimeError("温湿度/拱神计算失败: pillars 为空")

        zhis = [pillars[p]["branch"] for p in ["year", "month", "day", "hour"]]
        me = pillars["day"]["stem"]
        day_zhi = pillars["day"]["branch"]

        # 使用“真太阳时”日期作为 bazi.py 的输入口径（与本系统上游一致）
        # bazi.py 的 hourGZ 只依赖小时整数（双时辰），分钟不影响时支划分。
        dt = self.true_solar_time
        hour = int(dt.strftime("%H"))

        bazi_py = BAZI_1_DIR / "bazi.py"
        if not bazi_py.exists():
            raise RuntimeError("温湿度/拱神计算失败: 缺少 bazi-1-master/bazi.py")

        env = dict(**os.environ)
        # bazi.py 依赖本仓库的 local checkout（避免系统 pip 环境不一致）
        env["PYTHONPATH"] = ":".join(
            [
                str(BAZI_1_DIR),
                str(LUNAR_PYTHON_DIR),
                env.get("PYTHONPATH", ""),
            ]
        )
        # 固定 TZ，避免跨环境输出口径漂移
        env["TZ"] = "Asia/Shanghai"

        try:
            proc = subprocess.run(
                [
                    sys.executable,
                    str(bazi_py),
                    "-g",
                    str(dt.year),
                    str(dt.month),
                    str(dt.day),
                    str(hour),
                ],
                capture_output=True,
                text=True,
                timeout=12,
                env=env,
            )
        except Exception as e:
            raise RuntimeError(f"温湿度/拱神计算失败: bazi.py 调用异常: {e}") from e

        if proc.returncode != 0:
            stderr = (proc.stderr or "").strip()
            raise RuntimeError(f"温湿度/拱神计算失败: bazi.py 退出码={proc.returncode}: {stderr}")

        out = proc.stdout or ""

        def _strip_ansi(s: str) -> str:
            return re.sub(r"\x1b\[[0-9;]*m", "", s)

        out = _strip_ansi(out)

        # 形如：湿度分数 4 正为暖燥，负为寒湿，正常区间[-6,6] 拱： []
        m = re.search(r"湿度分数\s+(-?\d+)\s+.*?拱：\s*(\[[^\]]*\])", out)
        if not m:
            # 失败即报错（禁止回退到自写公式）
            raise RuntimeError("温湿度/拱神计算失败: 未找到 bazi.py 输出中的‘湿度分数’行")

        try:
            temps_score = int(m.group(1))
        except Exception as e:
            raise RuntimeError(f"温湿度/拱神计算失败: 湿度分数字段解析失败: {e}") from e

        raw_list = m.group(2)
        try:
            gongs_raw = ast.literal_eval(raw_list)
            gongs = [str(x) for x in gongs_raw] if isinstance(gongs_raw, list) else []
        except Exception as e:
            raise RuntimeError(f"温湿度/拱神计算失败: 拱列表解析失败: {e}") from e

        # -------------------- 2) 空亡命中：复用 bazi-1 common.get_empty --------------------
        try:
            from common import get_empty
        except Exception as e:
            raise RuntimeError(f"温湿度/拱神计算失败: common.get_empty 导入失败: {e}") from e

        empties_hit: list[str] = []
        for z in zhis:
            if get_empty((me, day_zhi), z) == "空":
                empties_hit.append(z)

        return {
            "temperatureScore": temps_score,
            "hint": "正为暖燥，负为寒湿，正常区间[-6,6]",
            "gongs": gongs,
            "empties": empties_hit,
        }

    def _calc_ganzhi_relations(self, pillars: dict) -> dict:
        """干支关系（合冲刑害破）"""
        stems = [pillars[p]["stem"] for p in ["year", "month", "day", "hour"]]
        branches = [pillars[p]["branch"] for p in ["year", "month", "day", "hour"]]
        pos_names = ["年", "月", "日", "时"]

        result = {"tianGan": [], "diZhi": []}

        # 天干五合
        gan_he = {"甲己": "土", "乙庚": "金", "丙辛": "水", "丁壬": "木", "戊癸": "火"}
        for i in range(4):
            for j in range(i + 1, 4):
                pair = stems[i] + stems[j]
                pair_rev = stems[j] + stems[i]
                if pair in gan_he:
                    result["tianGan"].append(f"{pos_names[i]}{pos_names[j]}{pair}合化{gan_he[pair]}")
                elif pair_rev in gan_he:
                    result["tianGan"].append(f"{pos_names[i]}{pos_names[j]}{pair_rev}合化{gan_he[pair_rev]}")

        # 天干相冲
        gan_chong = {"甲庚", "乙辛", "丙壬", "丁癸"}
        for i in range(4):
            for j in range(i + 1, 4):
                pair = stems[i] + stems[j]
                pair_rev = stems[j] + stems[i]
                if pair in gan_chong or pair_rev in gan_chong:
                    result["tianGan"].append(f"{pos_names[i]}{pos_names[j]}{stems[i]}{stems[j]}冲")

        # 地支六合
        zhi_he = {"子丑": "土", "寅亥": "木", "卯戌": "火", "辰酉": "金", "巳申": "水", "午未": "火"}
        for i in range(4):
            for j in range(i + 1, 4):
                pair = branches[i] + branches[j]
                pair_rev = branches[j] + branches[i]
                if pair in zhi_he:
                    result["diZhi"].append(f"{pos_names[i]}{pos_names[j]}{pair}合{zhi_he[pair]}")
                elif pair_rev in zhi_he:
                    result["diZhi"].append(f"{pos_names[i]}{pos_names[j]}{pair_rev}合{zhi_he[pair_rev]}")

        # 地支六冲
        zhi_chong = {"子午", "丑未", "寅申", "卯酉", "辰戌", "巳亥"}
        for i in range(4):
            for j in range(i + 1, 4):
                pair = branches[i] + branches[j]
                pair_rev = branches[j] + branches[i]
                if pair in zhi_chong or pair_rev in zhi_chong:
                    result["diZhi"].append(f"{pos_names[i]}{pos_names[j]}{branches[i]}{branches[j]}冲")

        # 地支三合
        san_he = [("申子辰", "水"), ("寅午戌", "火"), ("巳酉丑", "金"), ("亥卯未", "木")]
        for pattern, elem in san_he:
            matched = [(i, b) for i, b in enumerate(branches) if b in pattern]
            if len(matched) >= 3:
                result["diZhi"].append(f"{''.join([b for _, b in matched])}三合{elem}局")
            elif len(matched) == 2:
                result["diZhi"].append(f"{''.join([b for _, b in matched])}半合{elem}")

        # 地支相刑
        xing = [
            ("寅巳申", "无恩之刑"),
            ("丑戌未", "恃势之刑"),
            ("子卯", "无礼之刑"),
            ("辰辰", "自刑"),
            ("午午", "自刑"),
            ("酉酉", "自刑"),
            ("亥亥", "自刑"),
        ]
        for pattern, name in xing:
            matched = [b for b in branches if b in pattern]
            if len(matched) >= 2:
                result["diZhi"].append(f"{''.join(matched)}刑({name})")

        # 地支相害
        zhi_hai = {"子未", "丑午", "寅巳", "卯辰", "申亥", "酉戌"}
        for i in range(4):
            for j in range(i + 1, 4):
                pair = branches[i] + branches[j]
                pair_rev = branches[j] + branches[i]
                if pair in zhi_hai or pair_rev in zhi_hai:
                    result["diZhi"].append(f"{pos_names[i]}{pos_names[j]}{branches[i]}{branches[j]}害")

        # 地支相破
        zhi_po = {"子酉", "丑辰", "寅亥", "卯午", "巳申", "未戌"}
        for i in range(4):
            for j in range(i + 1, 4):
                pair = branches[i] + branches[j]
                pair_rev = branches[j] + branches[i]
                if pair in zhi_po or pair_rev in zhi_po:
                    result["diZhi"].append(f"{pos_names[i]}{pos_names[j]}{branches[i]}{branches[j]}破")

        return result

    def _calc_wuxing_state(self, five_elem: dict, month_zhi: str) -> dict:
        """五行旺相休囚死状态"""
        state_map = WUXING_STATE.get(month_zhi, {})
        result = {}
        for elem in ["木", "火", "土", "金", "水"]:
            state = state_map.get(elem, "")
            result[elem] = {"state": state}

        # 生成状态描述
        desc = []
        for state in ["旺", "相", "休", "囚", "死"]:
            for elem, info in result.items():
                if info["state"] == state:
                    desc.append(f"{elem}{state}")
        result["description"] = "、".join(desc)
        return result

    def _calc_siling(self, month_zhi: str, days_from_jieqi: int) -> dict:
        """人元司令分野"""
        siling_list = SILING.get(month_zhi, [])
        if not siling_list:
            return {"current": "", "detail": []}

        current_gan = ""
        accumulated = 0
        detail = []
        for gan, days in siling_list:
            start = accumulated + 1
            end = accumulated + days
            detail.append({"gan": gan, "days": days, "range": f"{start}-{end}日"})
            if accumulated < days_from_jieqi <= accumulated + days:
                current_gan = gan
            accumulated += days

        # 如果超出范围，取最后一个
        if not current_gan and siling_list:
            current_gan = siling_list[-1][0]

        return {"current": current_gan, "daysFromJieqi": days_from_jieqi, "detail": detail}

    def _calc_geju(self, ec, four_pillars: dict) -> dict:
        """格局判断"""
        day_gan = ec.getDayGan()
        month_zhi = ec.getMonthZhi()
        month_gan = ec.getMonthGan()

        geju_list = []

        # 建禄格：月支为日干之禄
        if JIANLU.get(day_gan) == month_zhi:
            geju_list.append("建禄格")

        # 羊刃格：月支为日干之刃（仅阳干）
        if YANGREN_POS.get(day_gan) == month_zhi:
            geju_list.append("羊刃格")

        # 正官格：月支藏干透出正官
        month_hidden = self._get_hidden_stems(month_zhi)
        for h_gan in month_hidden:
            shishen = SHISHEN.get(day_gan, {}).get(h_gan, "")
            if shishen == "正官" and h_gan == month_gan:
                geju_list.append("正官格")
            elif shishen == "七杀" and h_gan == month_gan:
                geju_list.append("七杀格")
            elif shishen == "正财" and h_gan == month_gan:
                geju_list.append("正财格")
            elif shishen == "偏财" and h_gan == month_gan:
                geju_list.append("偏财格")
            elif shishen == "正印" and h_gan == month_gan:
                geju_list.append("正印格")
            elif shishen == "偏印" and h_gan == month_gan:
                geju_list.append("偏印格")
            elif shishen == "食神" and h_gan == month_gan:
                geju_list.append("食神格")
            elif shishen == "伤官" and h_gan == month_gan:
                geju_list.append("伤官格")

        # 去重
        geju_list = list(dict.fromkeys(geju_list))

        return {"patterns": geju_list, "main": geju_list[0] if geju_list else "普通格局"}

    def _get_hidden_stems(self, zhi: str) -> list:
        """获取地支藏干"""
        hidden_map = {
            "子": ["癸"],
            "丑": ["己", "癸", "辛"],
            "寅": ["甲", "丙", "戊"],
            "卯": ["乙"],
            "辰": ["戊", "乙", "癸"],
            "巳": ["丙", "庚", "戊"],
            "午": ["丁", "己"],
            "未": ["己", "丁", "乙"],
            "申": ["庚", "壬", "戊"],
            "酉": ["辛"],
            "戌": ["戊", "辛", "丁"],
            "亥": ["壬", "甲"],
        }
        return hidden_map.get(zhi, [])

    def _calc_true_solar_time(self, dt: datetime, longitude: float, latitude: float = None) -> datetime:
        """
        计算真太阳时
        强制使用外部 paipan-master 原生算法；失败即报错，禁止回退简化公式
        """
        script = Path(__file__).parent.parent / "scripts" / "true_solar_time.js"
        if not script.exists():
            raise RuntimeError("真太阳时脚本缺失: true_solar_time.js")
        lat_val = latitude if latitude is not None else 0
        try:
            out = (
                subprocess.check_output(
                    [
                        "node",
                        str(script),
                        "--dt",
                        dt.strftime("%Y-%m-%d %H:%M:%S"),
                        "--lon",
                        str(longitude),
                        "--lat",
                        str(lat_val),
                    ],
                    timeout=8,
                )
                .decode("utf-8")
                .strip()
            )
            if not out:
                raise RuntimeError("真太阳时计算返回为空")
            return datetime.strptime(out, "%Y-%m-%d %H:%M:%S")
        except Exception as e:
            raise RuntimeError(f"真太阳时计算失败: {e}") from e

    def _calc_true_solar_time_detail(
        self, dt: datetime, longitude: float, latitude: float
    ) -> tuple[datetime, dict[str, Any], dict[str, Any]]:
        """
        计算真太阳时（带分解信息）
        只复用 paipan-master（通过 scripts/true_solar_time.js），禁止双口径/自写公式。
        """
        script = Path(__file__).parent.parent / "scripts" / "true_solar_time.js"
        if not script.exists():
            raise RuntimeError("真太阳时脚本缺失: true_solar_time.js")
        try:
            out = (
                subprocess.check_output(
                    [
                        "node",
                        str(script),
                        "--dt",
                        dt.strftime("%Y-%m-%d %H:%M:%S"),
                        "--lon",
                        str(longitude),
                        "--lat",
                        str(latitude),
                        "--json",
                    ],
                    timeout=8,
                )
                .decode("utf-8")
                .strip()
            )
            if not out:
                raise RuntimeError("真太阳时计算返回为空")
            payload = json.loads(out)
            true_str = payload.get("trueSolarTime")
            if not true_str:
                raise RuntimeError("真太阳时 JSON 缺失 trueSolarTime")
            true_dt = datetime.strptime(true_str, "%Y-%m-%d %H:%M:%S")
            offsets = payload.get("offsets", {}) if isinstance(payload.get("offsets", {}), dict) else {}
            detail = {
                "originalTime": dt.strftime("%Y-%m-%d %H:%M:%S"),
                "trueSolarTime": true_str,
                "longitudeOffsetMinutes": offsets.get("longitudeOffsetMinutes"),
                "astronomicalOffsetMinutes": offsets.get("astronomicalOffsetMinutes"),
                "totalOffsetMinutes": offsets.get("totalOffsetMinutes"),
                "note": "真太阳时分解（天文算法口径，含经度修正与均时差）",
            }
            zi = payload.get("ziTimeAnalysis", {}) if isinstance(payload.get("ziTimeAnalysis", {}), dict) else {}
            return ensure_cn(true_dt), detail, zi
        except Exception as e:
            raise RuntimeError(f"真太阳时计算失败: {e}") from e

    def _calc_all_void(self, ec) -> dict:
        """计算四柱空亡"""
        result = {}
        pillars = [
            ("year", ec.getYear()),
            ("month", ec.getMonth()),
            ("day", ec.getDay()),
            ("hour", ec.getTime()),
        ]
        for name, gz in pillars:
            kong = LunarUtil.getXunKong(gz)
            result[name] = {"pillar": gz, "kong": kong}
        return result

    def _calc_self_sitting(self, day_gan: str, day_zhi: str) -> str:
        """计算自坐（日干对日支的十二长生）"""
        changsheng = ["长生", "沐浴", "冠带", "临官", "帝旺", "衰", "病", "死", "墓", "绝", "胎", "养"]
        # 阳干顺行，阴干逆行
        yang_start = {"甲": "亥", "丙": "寅", "戊": "寅", "庚": "巳", "壬": "申"}
        yin_start = {"乙": "午", "丁": "酉", "己": "酉", "辛": "子", "癸": "卯"}

        branches = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

        if day_gan in yang_start:
            start = yang_start[day_gan]
            start_idx = branches.index(start)
            zhi_idx = branches.index(day_zhi)
            pos = (zhi_idx - start_idx) % 12
        elif day_gan in yin_start:
            start = yin_start[day_gan]
            start_idx = branches.index(start)
            zhi_idx = branches.index(day_zhi)
            pos = (start_idx - zhi_idx) % 12
        else:
            return ""

        return changsheng[pos]

    def _calc_yongshen(self, day_gan: str, month_zhi: str, pillars: dict) -> dict:
        """用神分析（调候用神）

        约束：禁止自写替代口径；以 bazi-1 原生数据表为事实来源。
        """
        key = day_gan + month_zhi
        # 以金不换调候表为“可读口径依据”，避免对编码串做错误推断
        basis = jinbuhuan.get(key, "")
        if not basis:
            raise RuntimeError(f"用神依据缺失: bazi-1 datas.jinbuhuan[{key}] 不存在")

        # 解析基础字符串：示例 "调候：喜壬戊丙 忌丁  大运：... 备注：..."
        stems_set = {"甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"}
        xi_shen: list[str] = []
        ji_shen: list[str] = []
        note = ""
        try:
            # 喜/忌：取“调候：”段落中的喜忌
            m = re.search(r"调候：.*?喜([^\\s]+)\\s+忌([^\\s]+)", basis)
            if m:
                xi_shen = [c for c in m.group(1) if c in stems_set]
                ji_shen = [c for c in m.group(2) if c in stems_set]
            # 备注
            m2 = re.search(r"备注：(.+)$", basis)
            if m2:
                note = m2.group(1).strip()
        except Exception as e:
            raise RuntimeError(f"用神依据解析失败: key={key} basis={basis}: {e}") from e

        # 同步保留原始编码（便于审计/对齐），但不以它作为喜忌解析来源
        tiaohou_raw = TIAOHOU.get(key, "")

        # 检查四柱中是否有喜神/忌神
        all_stems = [pillars[p]["stem"] for p in ["year", "month", "day", "hour"]]

        xi_in_bazi = [s for s in xi_shen if s in all_stems]
        ji_in_bazi = [s for s in ji_shen if s in all_stems]

        day_elem = STEM_ELEM[day_gan]

        return {
            "tiaoHou": {"xi": xi_shen, "ji": ji_shen},
            "xiInBazi": xi_in_bazi,
            "jiInBazi": ji_in_bazi,
            "hasXi": len(xi_in_bazi) > 0,
            "hasJi": len(ji_in_bazi) > 0,
            "note": note,
            "dayElement": day_elem,
            "elementRelation": {},
            "basis": basis,
            "basisSource": "金不换调候表",
            "tiaohouRaw": tiaohou_raw,
        }

    def _calc_sizi_summary(self, pillars: dict) -> dict[str, str]:
        """四柱断语（外部 bazi-1 sizi.summarys）

        说明：
        - 仅做数据查表，不做自写推断。
        - key 规则对齐 bazi-1-master/bazi.py:
          sum_index = ''.join([me, '日', *zhus[3]])
        """
        try:
            day_gan = pillars.get("day", {}).get("stem", "")
            hour_gan = pillars.get("hour", {}).get("stem", "")
            hour_zhi = pillars.get("hour", {}).get("branch", "")
            key = f"{day_gan}日{hour_gan}{hour_zhi}"
            text = sizi_summarys.get(key, "")
            return {"key": key, "text": text, "source": "bazi-1/sizi.summarys"}
        except Exception as e:
            raise RuntimeError(f"四柱断语查表失败: {e}") from e

    def _calc_xiao_yun(self, yun, ec, yongshen) -> list[dict]:
        """
        小运全量（覆盖全部大运阶段）
        - 聚合所有大运的 getXiaoYun，按年份去重排序
        """
        da_yuns = yun.getDaYun()
        if not da_yuns:
            return []
        seen = set()
        result = []
        day_gan = ec.getDayGan()
        month_zhi = ec.getMonthZhi()
        year_zhi = ec.getYearZhi()
        for dy in da_yuns:
            for xy in dy.getXiaoYun():
                year = xy.getYear()
                age = year - self.calc_dt.year
                key = year
                if key in seen:
                    continue
                seen.add(key)
                gz = xy.getGanZhi()
                gan, zhi = (gz[0], gz[1]) if len(gz) >= 2 else ("", "")
                # 十神
                shi_shen = ten_deities.get(day_gan, {}).get(gan, "")
                # 纳音
                na_yin = LunarUtil.NAYIN.get(gz, "") if gz else ""
                # 神煞
                spirits = self._calc_spirits_for_ganzhi(gan, zhi, day_gan, month_zhi, year_zhi)
                result.append(
                    {
                        "age": age,
                        "year": year,
                        "ganZhi": gz,
                        "shiShen": shi_shen,
                        "naYin": na_yin,
                        "spirits": spirits,
                    }
                )
        result.sort(key=lambda x: x["year"])
        return result

    def _calc_jiao_yun(self, yun) -> dict:
        """计算交运时间"""
        start_solar = yun.getStartSolar()
        start_year = yun.getStartYear()
        start_month = yun.getStartMonth()
        start_day = yun.getStartDay()
        start_hour = start_solar.getHour() if start_solar else None
        start_min = start_solar.getMinute() if start_solar else None
        start_sec = start_solar.getSecond() if start_solar else None

        # 交运节气
        da_yuns = yun.getDaYun()
        jiao_jieqi = ""
        if len(da_yuns) > 1:
            # 从第一个大运获取交运信息
            first_dy = da_yuns[1]
            # 根据大运干支推算交运节气
            dy_zhi = first_dy.getGanZhi()[1] if len(first_dy.getGanZhi()) > 1 else ""
            jieqi_map = {
                "寅": "立春",
                "卯": "惊蛰",
                "辰": "清明",
                "巳": "立夏",
                "午": "芒种",
                "未": "小暑",
                "申": "立秋",
                "酉": "白露",
                "戌": "寒露",
                "亥": "立冬",
                "子": "大雪",
                "丑": "小寒",
            }
            jiao_jieqi = jieqi_map.get(dy_zhi, "")

        return {
            "startYear": start_year,
            "startMonth": start_month,
            "startDay": start_day,
            "startHour": start_hour,
            "startMinute": start_min,
            "startSecond": start_sec,
            "startDate": f"{start_solar.getYear()}-{start_solar.getMonth():02d}-{start_solar.getDay():02d} {start_hour or 0:02d}:{start_min or 0:02d}:{start_sec or 0:02d}"
            if start_solar
            else "",
            "description": f"出生后{start_year}年{start_month}月{start_day}天{start_hour or 0}时{start_min or 0}分起运",
            "jiaoJieQi": jiao_jieqi,
        }

    def _calc_jieqi_detail(self) -> dict:
        """节气详情"""
        prev_jq = self.lunar.getPrevJieQi()
        next_jq = self.lunar.getNextJieQi()

        prev_solar = prev_jq.getSolar() if prev_jq else None
        next_solar = next_jq.getSolar() if next_jq else None

        # 计算距离天数
        birth_date = self.calc_dt.date()
        prev_days = next_days = 0
        if prev_solar:
            prev_date = datetime(prev_solar.getYear(), prev_solar.getMonth(), prev_solar.getDay()).date()
            prev_days = (birth_date - prev_date).days
        if next_solar:
            next_date = datetime(next_solar.getYear(), next_solar.getMonth(), next_solar.getDay()).date()
            next_days = (next_date - birth_date).days

        return {
            "prevJieQi": {
                "name": prev_jq.getName() if prev_jq else "",
                "date": prev_solar.toYmd() if prev_solar else "",
                "daysAfter": prev_days,
            },
            "nextJieQi": {
                "name": next_jq.getName() if next_jq else "",
                "date": next_solar.toYmd() if next_solar else "",
                "daysBefore": next_days,
            },
            "description": f"出生于{prev_jq.getName()}后{prev_days}天，{next_jq.getName()}前{next_days}天"
            if prev_jq and next_jq
            else "",
        }

    def _calc_analysis_evidence(
        self,
        *,
        four_pillars: dict[str, Any],
        hidden_stems: dict[str, Any],
        day_master: dict[str, Any],
        wuxing_scores: dict[str, Any],
        geju: dict[str, Any],
        yongshen: dict[str, Any],
        ganzhi_relations: dict[str, Any],
        branch_relations: dict[str, Any],
        spirits: dict[str, Any],
        bone_weight: dict[str, Any],
    ) -> dict[str, Any]:
        """生成综合八字结论的机器可读依据，不直接渲染到默认 Markdown。"""
        month_pillar = four_pillars.get("month", {}) if isinstance(four_pillars, dict) else {}
        day_pillar = four_pillars.get("day", {}) if isinstance(four_pillars, dict) else {}
        month_branch = month_pillar.get("branch", "")
        day_stem = day_master.get("stem", "")
        yongshen_tiaohou = yongshen.get("tiaoHou", {}) if isinstance(yongshen, dict) else {}

        def evidence_item(
            *,
            conclusion: object,
            basis: list[str],
            sources: list[str],
            rule_ids: list[str],
            weight: str,
            visibility: str = "audit",
        ) -> dict[str, Any]:
            return {
                "conclusion": conclusion,
                "basis": [item for item in basis if str(item).strip()],
                "sources": sources,
                "ruleIds": rule_ids,
                "weight": weight,
                "visibility": visibility,
            }

        spirits_count = 0
        if isinstance(spirits, dict):
            by_pillar = spirits.get("byPillar", {})
            if isinstance(by_pillar, dict):
                spirits_count = sum(len(items) for items in by_pillar.values() if isinstance(items, list))

        return {
            "schemaVersion": 1,
            "profile": "comprehensive_bazi",
            "visibilityDefault": "hidden",
            "weightPolicy": {
                "core": "八字核心：月令、日主、藏干、透干、五行、调候、格局、干支关系。",
                "fortune": "八字动态：大运、流年、流月、小运。",
                "auxiliary": "八字辅助：神煞、干支取象。",
                "folk": "民俗辅助：袁天罡称骨；只作附录，不参与核心喜忌和格局判断。",
            },
            "items": {
                "dayMaster": evidence_item(
                    conclusion={
                        "stem": day_stem,
                        "element": day_master.get("elementCn") or day_master.get("element", ""),
                        "strength": day_master.get("strength", ""),
                    },
                    basis=[
                        f"日柱={day_pillar.get('fullName', '')}",
                        f"月令={month_branch}",
                        f"五行强弱={wuxing_scores.get('weakStrong', '')}",
                    ],
                    sources=["lunar-python", "bazi-1"],
                    rule_ids=["bazi.month_command_priority", "bazi.day_master_strength"],
                    weight="core",
                ),
                "wuxingPreference": evidence_item(
                    conclusion={
                        "xi": yongshen_tiaohou.get("xi", []),
                        "ji": yongshen_tiaohou.get("ji", []),
                        "note": yongshen.get("note", "") if isinstance(yongshen, dict) else "",
                    },
                    basis=[
                        f"月令={month_branch}",
                        f"五行分数={wuxing_scores.get('fiveElementScore', {})}",
                        f"天干分数={wuxing_scores.get('ganScore', {})}",
                    ],
                    sources=["bazi-1", "穷通宝鉴规则索引"],
                    rule_ids=["bazi.regulating_climate", "bazi.balance_five_elements"],
                    weight="core",
                ),
                "pattern": evidence_item(
                    conclusion={
                        "main": geju.get("main", "") if isinstance(geju, dict) else "",
                        "patterns": geju.get("patterns", []) if isinstance(geju, dict) else [],
                    },
                    basis=[
                        f"月令={month_branch}",
                        f"月柱={month_pillar.get('fullName', '')}",
                        f"藏干={hidden_stems}",
                    ],
                    sources=["lunar-python", "bazi-1", "子平真诠规则索引"],
                    rule_ids=["bazi.pattern_by_month_command", "bazi.pattern_root_transparency"],
                    weight="core",
                ),
                "ganzhiRelations": evidence_item(
                    conclusion={
                        "tianGan": ganzhi_relations.get("tianGan", {}) if isinstance(ganzhi_relations, dict) else {},
                        "diZhi": branch_relations,
                    },
                    basis=[
                        f"四柱={','.join(p.get('fullName', '') for p in four_pillars.values() if isinstance(p, dict))}",
                    ],
                    sources=["lunar-python", "项目干支关系规则"],
                    rule_ids=["bazi.stem_branch_relations"],
                    weight="core",
                ),
                "spirits": evidence_item(
                    conclusion={"count": spirits_count},
                    basis=["神煞按年/月/日/时柱合并去重；仅作辅助解释。"],
                    sources=["bazi-1"],
                    rule_ids=["bazi.spirits_auxiliary_only"],
                    weight="auxiliary",
                ),
                "boneWeight": evidence_item(
                    conclusion={
                        "weight": bone_weight.get("weight", "") if isinstance(bone_weight, dict) else "",
                        "textPresent": bool(bone_weight.get("text", "")) if isinstance(bone_weight, dict) else False,
                    },
                    basis=["称骨按年、月、日、时权重求和；不参与喜忌、格局、旺衰判断。"],
                    sources=["袁天罡称骨民俗表"],
                    rule_ids=["folk.bone_weight_appendix_only"],
                    weight="folk",
                ),
            },
        }

    def _calc_jianchu(self, ec) -> dict:
        """
        建除十二神
        - 公式来源: bazi-1-master/bazi.py (seq = 12 - 月支序; index = (日支序 + seq) % 12)
        - 数据来源: bazi-1-master/datas.py -> jianchus
        """
        try:
            data_path = BAZI_1_DIR / "datas.py"
            text = data_path.read_text(encoding="utf-8")
            start = text.find("jianchus")
            if start == -1:
                raise RuntimeError("建除十二神数据缺失: datas.py 中未找到 jianchus")
            brace_start = text.find("{", start)
            # 向后扩展到完整字典（到匹配的右花括号）
            depth = 0
            end_idx = brace_start
            for i, ch in enumerate(text[brace_start:], brace_start):
                if ch == "{":
                    depth += 1
                elif ch == "}":
                    depth -= 1
                    if depth == 0:
                        end_idx = i
                        break
            segment = text[brace_start : end_idx + 1]
            jianchus = ast.literal_eval(segment)
            zhi_list = list(LunarUtil.ZHI)
            month_zhi = ec.getMonthZhi()
            day_zhi = ec.getDayZhi()
            seq = 12 - zhi_list.index(month_zhi)
            idx = (zhi_list.index(day_zhi) + seq) % 12
            name, desc = jianchus.get(idx, ("", ""))
            return {
                "index": idx,
                "name": name,
                "description": desc,
                "monthZhi": month_zhi,
                "dayZhi": day_zhi,
            }
        except Exception as e:
            raise RuntimeError(f"建除十二神计算失败: {e}") from e

    def _add_fortune_shishen(self, major: dict, day_gan: str) -> dict:
        """为大运添加十神和纳音"""
        for p in major.get("pillars", []):
            stem = p.get("stem", "")
            if stem and day_gan in SHISHEN:
                p["shiShen"] = SHISHEN[day_gan].get(stem, "")
            p["nayin"] = LunarUtil.NAYIN.get(p.get("fullName", ""), "")
        return major

    def _add_annual_shishen(self, annual: list[dict], day_gan: str) -> list[dict]:
        """为流年添加十神和纳音"""
        for p in annual:
            stem = p.get("stem", "")
            if stem and day_gan in SHISHEN:
                p["shiShen"] = SHISHEN[day_gan].get(stem, "")
            p["nayin"] = LunarUtil.NAYIN.get(p.get("fullName", ""), "")
        return annual

    def _add_monthly_shishen(self, monthly: list[dict], day_gan: str) -> list[dict]:
        """为流月添加十神和纳音"""
        for p in monthly:
            stem = p.get("stem", "")
            if stem and day_gan in SHISHEN:
                p["shiShen"] = SHISHEN[day_gan].get(stem, "")
            nayin = LunarUtil.NAYIN.get(p.get("ganZhi", ""), "")
            p["nayin"] = nayin
            p["naYin"] = nayin  # 兼容渲染层
        return monthly


def calc_true_solar_time(dt: datetime, longitude: float) -> datetime:
    """真太阳时"""
    return dt + timedelta(minutes=(longitude - 120) * 4)


# ========== 称骨算命 ==========
BONE_YEAR = {
    "甲子": 1.2,
    "乙丑": 0.9,
    "丙寅": 0.6,
    "丁卯": 0.7,
    "戊辰": 1.2,
    "己巳": 0.5,
    "庚午": 0.9,
    "辛未": 0.8,
    "壬申": 0.7,
    "癸酉": 0.8,
    "甲戌": 1.5,
    "乙亥": 0.9,
    "丙子": 1.6,
    "丁丑": 0.8,
    "戊寅": 0.8,
    "己卯": 1.9,
    "庚辰": 1.2,
    "辛巳": 0.6,
    "壬午": 0.8,
    "癸未": 0.7,
    "甲申": 0.5,
    "乙酉": 1.5,
    "丙戌": 0.6,
    "丁亥": 1.6,
    "戊子": 1.5,
    "己丑": 0.7,
    "庚寅": 0.9,
    "辛卯": 1.2,
    "壬辰": 1.0,
    "癸巳": 0.7,
    "甲午": 1.5,
    "乙未": 0.6,
    "丙申": 0.5,
    "丁酉": 1.4,
    "戊戌": 1.4,
    "己亥": 0.9,
    "庚子": 0.7,
    "辛丑": 0.7,
    "壬寅": 0.9,
    "癸卯": 1.2,
    "甲辰": 0.8,
    "乙巳": 0.7,
    "丙午": 1.3,
    "丁未": 0.5,
    "戊申": 1.4,
    "己酉": 0.5,
    "庚戌": 0.9,
    "辛亥": 1.7,
    "壬子": 0.5,
    "癸丑": 0.7,
    "甲寅": 1.2,
    "乙卯": 0.8,
    "丙辰": 0.8,
    "丁巳": 0.6,
    "戊午": 1.9,
    "己未": 0.6,
    "庚申": 0.8,
    "辛酉": 1.6,
    "壬戌": 1.0,
    "癸亥": 0.7,
}
BONE_MONTH = {1: 0.6, 2: 0.7, 3: 1.8, 4: 0.9, 5: 0.5, 6: 1.6, 7: 0.9, 8: 1.5, 9: 1.8, 10: 0.8, 11: 0.9, 12: 0.5}
BONE_DAY = {
    1: 0.5,
    2: 1.0,
    3: 0.8,
    4: 1.5,
    5: 1.6,
    6: 1.5,
    7: 0.8,
    8: 1.6,
    9: 0.8,
    10: 1.6,
    11: 0.9,
    12: 1.7,
    13: 0.8,
    14: 1.7,
    15: 1.0,
    16: 0.8,
    17: 0.9,
    18: 1.8,
    19: 0.5,
    20: 1.5,
    21: 1.0,
    22: 0.9,
    23: 0.8,
    24: 0.9,
    25: 1.5,
    26: 1.8,
    27: 0.7,
    28: 0.8,
    29: 1.6,
    30: 0.6,
}
BONE_HOUR = {
    "子": 1.6,
    "丑": 0.6,
    "寅": 0.7,
    "卯": 1.0,
    "辰": 0.9,
    "巳": 1.6,
    "午": 1.0,
    "未": 0.8,
    "申": 0.8,
    "酉": 0.9,
    "戌": 0.6,
    "亥": 0.6,
}
BONE_TEXT = {
    2.1: "终身行乞孤苦之命",
    2.2: "一生劳碌之命",
    2.3: "终身困苦之命",
    2.4: "一生薄福之命",
    2.5: "六亲无靠自立更生之命",
    2.6: "平生衣禄苦中求之命",
    2.7: "一生衣禄不周之命",
    2.8: "一生行事似飘蓬之命",
    2.9: "初年运限未曾亨之命",
    3.0: "劳劳碌碌苦中求之命",
    3.1: "先苦后甘之命",
    3.2: "性巧过人衣食到贵之命",
    3.3: "早年作事事难成之命",
    3.4: "财谷有余主得内助之命",
    3.5: "生平福量不周全之命",
    3.6: "超群拔类衣禄厚重之命",
    3.7: "聪明富贵之命",
    3.8: "财帛丰厚宜称之命",
    3.9: "少年命运不通之命",
    4.0: "富贵近益生匪浅之命",
    4.1: "税户近贵门庭光彩之命",
    4.2: "兵权有职富贵才能之命",
    4.3: "财禄厚重白手成家之命",
    4.4: "初年无财中年有财之命",
    4.5: "福禄丰厚极富且贵之命",
    4.6: "富贵有余福寿双全之命",
    4.7: "高官禄厚学业饱满之命",
    4.8: "官员财禄厚重之命",
    4.9: "性巧精神仓库财禄之命",
    5.0: "文武才能钱谷丰盛之命",
    5.1: "官职财禄荣华富贵之命",
    5.2: "掌握兵权富贵长命",
    5.3: "僧道门中近贵之命",
    5.4: "大富大贵之命",
    5.5: "官职财禄丰厚之命",
    5.6: "官职长享荣华富贵之命",
    5.7: "官职财禄皆有之命",
    5.8: "官禄旺相才能性直富贵之命",
    5.9: "官品极品之命",
    6.0: "官职王侯之命",
    6.1: "名利双收之命",
    6.2: "权贵之命",
    6.3: "受职高官之命",
    6.4: "权贵显达之命",
    6.5: "细推此命福不轻之命",
    6.6: "大富大贵之命",
    6.7: "一世荣华富贵之命",
    6.8: "富贵双全之命",
    6.9: "受职于天之命",
    7.0: "荣华富贵之命",
    7.1: "此命生成大不同之命",
    7.2: "此格推来福禄宏之命",
}


def calc_bone_weight(year_gz: str, lunar_month: int, lunar_day: int, hour_zhi: str) -> dict:
    """称骨算命（含构成明细）"""
    y = BONE_YEAR.get(year_gz, 0)
    m = BONE_MONTH.get(lunar_month, 0)
    d = BONE_DAY.get(lunar_day, 0)
    h = BONE_HOUR.get(hour_zhi, 0)
    total = round(y + m + d + h, 1)

    # 找最接近的评语
    text = ""
    for w, t in sorted(BONE_TEXT.items()):
        if total <= w:
            text = t
            break
    if not text:
        text = BONE_TEXT.get(7.2, "大富大贵之命")

    liang = int(total)
    qian = int((total - liang) * 10)
    return {
        "weight": total,
        "weightCn": f"{liang}两{qian}钱",
        "text": text,
        "components": {
            "year": {"ganZhi": year_gz, "weight": y},
            "month": {"month": lunar_month, "weight": m},
            "day": {"day": lunar_day, "weight": d},
            "hour": {"zhi": hour_zhi, "weight": h},
        },
    }


# ========== 命卦计算 ==========
GUA_NAMES = ["坎", "坤", "震", "巽", "中", "乾", "兑", "艮", "离"]
GUA_DIRECTION = {"坎": "北", "坤": "西南", "震": "东", "巽": "东南", "乾": "西北", "兑": "西", "艮": "东北", "离": "南"}


def calc_ming_gua(year: int, gender: str) -> dict:
    """命卦计算"""
    # 年份各位数相加
    s = sum(int(d) for d in str(year))
    while s >= 10:
        s = sum(int(d) for d in str(s))

    if gender == "male":
        gua_num = 11 - s if year < 2000 else 9 - s
        if gua_num <= 0:
            gua_num += 9
    else:
        gua_num = 4 + s if year < 2000 else 6 + s
        if gua_num > 9:
            gua_num -= 9

    # 5为中宫，男归坤，女归艮
    if gua_num == 5:
        gua_num = 2 if gender == "male" else 8

    gua_name = GUA_NAMES[gua_num - 1] if 1 <= gua_num <= 9 else "坤"
    xi_si = gua_name in ["乾", "兑", "艮", "坤"]

    return {
        "guaNum": gua_num,
        "guaName": gua_name,
        "direction": GUA_DIRECTION.get(gua_name, ""),
        "group": "西四命" if xi_si else "东四命",
    }
