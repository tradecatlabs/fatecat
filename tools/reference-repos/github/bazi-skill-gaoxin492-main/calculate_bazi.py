"""
calculate_bazi.py
八字排盘核心计算模块

输入: JSON (via stdin 或直接调用 calculate())
输出: CLI 默认使用终端友好展示；结构化数据供内部复用

流派约定:
  - 早晚子时: sect=2，23:00-23:59 日柱算当天
  - 大运: 按节气推算，男阳/女阴顺排，男阴/女阳逆排
  - 真太阳时: 基于出生地经度校正
"""

import argparse
import json
import os
import re
import sys
import unicodedata
from datetime import datetime, timedelta
from typing import Optional

from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from timezonefinder import TimezoneFinder
import pytz
from lunar_python import Lunar, Solar


# ─────────────────────────────────────────────
# 基础数据表
# ─────────────────────────────────────────────

TIAN_GAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
DI_ZHI   = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

WUXING_GAN = {
    "甲": "木", "乙": "木", "丙": "火", "丁": "火", "戊": "土",
    "己": "土", "庚": "金", "辛": "金", "壬": "水", "癸": "水"
}
WUXING_ZHI = {
    "子": "水", "丑": "土", "寅": "木", "卯": "木", "辰": "土", "巳": "火",
    "午": "火", "未": "土", "申": "金", "酉": "金", "戌": "土", "亥": "水"
}
YINYANG_GAN = {
    "甲": "阳", "乙": "阴", "丙": "阳", "丁": "阴", "戊": "阳",
    "己": "阴", "庚": "阳", "辛": "阴", "壬": "阳", "癸": "阴"
}
YINYANG_ZHI = {
    "子": "阳", "丑": "阴", "寅": "阳", "卯": "阴", "辰": "阳", "巳": "阴",
    "午": "阳", "未": "阴", "申": "阳", "酉": "阴", "戌": "阳", "亥": "阴"
}

# 地支藏干 {地支: [(天干, 类型)]}  类型: 主气/中气/余气
CANG_GAN = {
    "子": [("癸", "主气")],
    "丑": [("己", "主气"), ("癸", "中气"), ("辛", "余气")],
    "寅": [("甲", "主气"), ("丙", "中气"), ("戊", "余气")],
    "卯": [("乙", "主气")],
    "辰": [("戊", "主气"), ("乙", "中气"), ("癸", "余气")],
    "巳": [("丙", "主气"), ("庚", "中气"), ("戊", "余气")],
    "午": [("丁", "主气"), ("己", "余气")],
    "未": [("己", "主气"), ("丁", "中气"), ("乙", "余气")],
    "申": [("庚", "主气"), ("壬", "中气"), ("戊", "余气")],
    "酉": [("辛", "主气")],
    "戌": [("戊", "主气"), ("辛", "中气"), ("丁", "余气")],
    "亥": [("壬", "主气"), ("甲", "余气")],
}

# 十二长生 [长生, 沐浴, 冠带, 临官, 帝旺, 衰, 病, 死, 墓, 绝, 胎, 养]
# 阳干从长生地顺数，阴干从长生地逆数
# 各阳干长生地（地支索引）
YANG_CHANG_SHENG = {"甲": 11, "丙": 2, "戊": 2, "庚": 5, "壬": 8}  # 亥寅巳申
YIN_CHANG_SHENG  = {"乙": 8, "丁": 5, "己": 5, "辛": 2, "癸": 11}  # 申巳寅亥(逆)

SHI_ER_ZHANG_SHENG_NAMES = ["长生", "沐浴", "冠带", "临官", "帝旺", "衰", "病", "死", "墓", "绝", "胎", "养"]

# 十神关系表 (日主天干 → 他干 → 十神)
SHI_SHEN_TABLE = {
    # 格式: (日主阴阳, 目标五行关系, 目标阴阳) → 十神
    # 关系: 同我/生我/我生/克我/我克
}

ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")
WUXING_COLOR = {
    "木": "1;32",
    "火": "1;31",
    "土": "1;33",
    "金": "1;36",
    "水": "1;94",
}

def get_shi_shen(ri_gan: str, target_gan: str) -> str:
    """根据日主和目标天干计算十神"""
    ri_wx = WUXING_GAN[ri_gan]
    ri_yy = YINYANG_GAN[ri_gan]
    tg_wx = WUXING_GAN[target_gan]
    tg_yy = YINYANG_GAN[target_gan]

    # 五行关系
    sheng = {"木": "火", "火": "土", "土": "金", "金": "水", "水": "木"}
    ke   = {"木": "土", "火": "金", "土": "水", "金": "木", "水": "火"}

    same_yy = (ri_yy == tg_yy)

    if tg_wx == ri_wx:
        return "比肩" if same_yy else "劫财"
    elif sheng[ri_wx] == tg_wx:       # 我生
        return "食神" if same_yy else "伤官"
    elif sheng[tg_wx] == ri_wx:       # 生我
        return "偏印" if same_yy else "正印"
    elif ke[ri_wx] == tg_wx:          # 我克
        return "偏财" if same_yy else "正财"
    elif ke[tg_wx] == ri_wx:          # 克我
        return "七杀" if same_yy else "正官"
    return "未知"

def get_shi_er_chang_sheng(tian_gan: str, di_zhi: str) -> str:
    """计算天干在地支的十二长生状态"""
    zhi_idx = DI_ZHI.index(di_zhi)
    yy = YINYANG_GAN[tian_gan]

    if yy == "阳":
        wx = WUXING_GAN[tian_gan]
        # 找对应阳干
        for g, idx in YANG_CHANG_SHENG.items():
            if WUXING_GAN[g] == wx:
                start = idx
                break
        else:
            return "未知"
        pos = (zhi_idx - start) % 12
    else:
        wx = WUXING_GAN[tian_gan]
        for g, idx in YIN_CHANG_SHENG.items():
            if WUXING_GAN[g] == wx:
                start = idx
                break
        else:
            return "未知"
        pos = (start - zhi_idx) % 12

    return SHI_ER_ZHANG_SHENG_NAMES[pos]


# ─────────────────────────────────────────────
# 真太阳时校正
# ─────────────────────────────────────────────

def resolve_birth_place(birth_place: str, birth_dt: Optional[datetime] = None) -> dict:
    """解析出生地，返回经纬度、时区和解析来源。"""
    geolocator = Nominatim(user_agent="bazi_skill", timeout=10)
    timezone_finder = TimezoneFinder()
    fallback_locations = {
        "北京": (39.9, 116.4), "上海": (31.2, 121.5), "广州": (23.1, 113.3),
        "深圳": (22.5, 114.1), "成都": (30.7, 104.1), "杭州": (30.3, 120.2),
        "武汉": (30.6, 114.3), "西安": (34.3, 108.9), "南京": (32.1, 118.8),
        "重庆": (29.6, 106.5), "天津": (39.1, 117.2), "沈阳": (41.8, 123.4),
        "长沙": (28.2, 113.0), "哈尔滨": (45.8, 126.5), "济南": (36.7, 117.0),
        "郑州": (34.7, 113.6), "昆明": (25.0, 102.7), "福州": (26.1, 119.3),
        "合肥": (31.8, 117.3), "南昌": (28.7, 115.9),
    }

    queries = [birth_place.strip()]
    if re.search(r"[\u4e00-\u9fff]", birth_place) and "中国" not in birth_place and "China" not in birth_place:
        queries.append(f"{birth_place}, China")

    location = None
    for query in queries:
        for language in ("zh", None):
            try:
                location = geolocator.geocode(query, language=language)
            except Exception:
                location = None
            if location:
                break
        if location:
            break

    source = "geocoder"
    resolved_name = birth_place
    if location:
        latitude = float(location.latitude)
        longitude = float(location.longitude)
        resolved_name = getattr(location, "address", birth_place) or birth_place
    else:
        matched = None
        for key, coords in fallback_locations.items():
            if key in birth_place:
                matched = (key, coords)
                break
        if matched:
            resolved_name = matched[0]
            latitude, longitude = matched[1]
            source = "builtin-fallback"
        else:
            raise ValueError(
                f"无法解析出生地：{birth_place}。请提供更完整的地点名称（如 城市, 国家/地区），"
                "或直接提供可识别的标准地名。"
            )

    timezone_name = timezone_finder.timezone_at(lng=longitude, lat=latitude)
    if not timezone_name:
        timezone_name = timezone_finder.closest_timezone_at(lng=longitude, lat=latitude)
    if not timezone_name:
        timezone_name = "Asia/Shanghai"

    timezone_obj = pytz.timezone(timezone_name)
    if birth_dt is None:
        offset_minutes = int(datetime.now(timezone_obj).utcoffset().total_seconds() // 60)
    else:
        try:
            localized_dt = timezone_obj.localize(birth_dt, is_dst=None)
        except Exception:
            localized_dt = timezone_obj.localize(birth_dt, is_dst=False)
        offset_minutes = int(localized_dt.utcoffset().total_seconds() // 60)

    standard_longitude = offset_minutes / 4.0
    return {
        "lat": latitude,
        "lon": longitude,
        "timezone": timezone_name,
        "standard_longitude": standard_longitude,
        "resolved_name": resolved_name,
        "source": source,
    }


def get_coordinates(birth_place: str, birth_dt: Optional[datetime] = None) -> tuple[float, float]:
    """兼容旧接口：城市名 → (纬度, 经度)。"""
    location_info = resolve_birth_place(birth_place, birth_dt)
    return location_info["lat"], location_info["lon"]


def correct_solar_time(dt: datetime, longitude: float, standard_longitude: float = 120.0) -> datetime:
    """
    真太阳时校正
    基准经度按出生地所在时区推导，默认回落到 120°E。
    每偏差1°经度 = 4分钟
    """
    delta_minutes = (longitude - standard_longitude) * 4
    return dt + timedelta(minutes=delta_minutes)


# ─────────────────────────────────────────────
# 刑冲合会判断
# ─────────────────────────────────────────────

def calc_xing_chong_he_hui(pillars: dict) -> dict:
    """
    计算四柱间的刑冲合会
    pillars: {"year": (天干, 地支), "month": ..., "day": ..., "hour": ...}
    """
    result = {"he": [], "chong": [], "xing": [], "hui": [], "hai": [], "po": []}
    pillar_names = ["year", "month", "day", "hour"]
    zhi_list = [pillars[p][1] for p in pillar_names]
    gan_list = [pillars[p][0] for p in pillar_names]

    def get_dist(i, j):
        d = abs(i - j)
        return "相邻" if d == 1 else ("隔位" if d == 2 else "遥位")

    def build_positions(targets: tuple[str, ...], hits: list[int]) -> list[int]:
        positions = []
        used = set()
        for target in targets:
            for idx in hits:
                if idx not in used and zhi_list[idx] == target:
                    positions.append(idx)
                    used.add(idx)
                    break
        return positions

    # 天干合
    TIAN_GAN_HE = [("甲", "己", "土"), ("乙", "庚", "金"), ("丙", "辛", "水"),
                   ("丁", "壬", "木"), ("戊", "癸", "火")]
    for i in range(4):
        for j in range(i+1, 4):
            for g1, g2, wx in TIAN_GAN_HE:
                if (gan_list[i] == g1 and gan_list[j] == g2) or \
                   (gan_list[i] == g2 and gan_list[j] == g1):
                    result["he"].append({
                        "type": "天干合", "element": wx,
                        "pillars": [pillar_names[i], pillar_names[j]],
                        "detail": f"{gan_list[i]}{gan_list[j]}合{wx}({get_dist(i, j)})"
                    })

    # 天干冲
    TIAN_GAN_CHONG = [{"甲", "庚"}, {"乙", "辛"}, {"丙", "壬"}, {"丁", "癸"}]
    for i in range(4):
        for j in range(i+1, 4):
            if {gan_list[i], gan_list[j]} in TIAN_GAN_CHONG:
                result["chong"].append({
                    "type": "天干冲",
                    "pillars": [pillar_names[i], pillar_names[j]],
                    "detail": f"{gan_list[i]}{gan_list[j]}相冲({get_dist(i, j)})"
                })

    # 地支六合
    ZHI_LIU_HE = [("子", "丑", "土"), ("寅", "亥", "木"), ("卯", "戌", "火"),
                  ("辰", "酉", "金"), ("巳", "申", "水"), ("午", "未", "火")]
    for i in range(4):
        for j in range(i+1, 4):
            for z1, z2, wx in ZHI_LIU_HE:
                if (zhi_list[i] == z1 and zhi_list[j] == z2) or \
                   (zhi_list[i] == z2 and zhi_list[j] == z1):
                    result["he"].append({
                        "type": "地支六合", "element": wx,
                        "pillars": [pillar_names[i], pillar_names[j]],
                        "detail": f"{zhi_list[i]}{zhi_list[j]}合{wx}({get_dist(i, j)})"
                    })

    # 地支三合 / 半合 / 拱局
    SAN_HE = [("申", "子", "辰", "水"), ("亥", "卯", "未", "木"),
              ("寅", "午", "戌", "火"), ("巳", "酉", "丑", "金")]
    for z1, z2, z3, wx in SAN_HE:
        hits = [i for i, z in enumerate(zhi_list) if z in (z1, z2, z3)]
        chars_set = set(zhi_list[h] for h in hits)
        if len(chars_set) == 3:
            idxs = sorted(build_positions((z1, z2, z3), hits))
            result["hui"].append({
                "type": "三合局", "element": wx,
                "pillars": [pillar_names[idx] for idx in idxs],
                "detail": f"{z1}{z2}{z3}三合{wx}局"
            })
        elif len(chars_set) == 2:
            # 区分半合与拱局，需两两检查以防出现两个相同地支
            for i_idx in range(len(hits)):
                for j_idx in range(i_idx+1, len(hits)):
                    p1, p2 = hits[i_idx], hits[j_idx]
                    c1, c2 = zhi_list[p1], zhi_list[p2]
                    if c1 != c2: # 确保不是重复字，如两个"未"
                        dist = get_dist(p1, p2)
                        if z2 in (c1, c2):
                            result["hui"].append({
                                "type": "半合", "element": wx,
                                "pillars": [pillar_names[p1], pillar_names[p2]],
                                "detail": f"{c1}{c2}半合{wx}({dist})"
                            })
                        else:
                            result["hui"].append({
                                "type": "拱局", "element": wx,
                                "pillars": [pillar_names[p1], pillar_names[p2]],
                                "detail": f"{c1}{c2}拱合{wx}({dist})"
                            })

    # 地支三会
    SAN_HUI = [("寅", "卯", "辰", "木"), ("巳", "午", "未", "火"),
               ("申", "酉", "戌", "金"), ("亥", "子", "丑", "水")]
    for z1, z2, z3, wx in SAN_HUI:
        if all(z in zhi_list for z in (z1, z2, z3)):
            hits = [i for i, z in enumerate(zhi_list) if z in (z1, z2, z3)]
            idxs = sorted(build_positions((z1, z2, z3), hits))
            result["hui"].append({
                "type": "三会局", "element": wx,
                "pillars": [pillar_names[i] for i in idxs],
                "detail": f"{z1}{z2}{z3}三会{wx}局"
            })

    # 地支相冲
    CHONG_PAIRS = [{"子", "午"}, {"丑", "未"}, {"寅", "申"},
                   {"卯", "酉"}, {"辰", "戌"}, {"巳", "亥"}]
    for i in range(4):
        for j in range(i+1, 4):
            if {zhi_list[i], zhi_list[j]} in CHONG_PAIRS:
                result["chong"].append({
                    "type": "地支冲",
                    "pillars": [pillar_names[i], pillar_names[j]],
                    "detail": f"{zhi_list[i]}{zhi_list[j]}相冲({get_dist(i, j)})"
                })

    # 地支相刑（无礼/无恩/恃势/自刑）
    XING_PAIRS = {
        frozenset(("子", "卯")): "无礼之刑",
        frozenset(("寅", "巳")): "无恩之刑",
        frozenset(("巳", "申")): "无恩之刑",
        frozenset(("寅", "申")): "无恩之刑",
        frozenset(("丑", "未")): "恃势之刑",
        frozenset(("未", "戌")): "恃势之刑",
        frozenset(("丑", "戌")): "恃势之刑",
    }
    for i in range(4):
        for j in range(i+1, 4):
            xing_type = XING_PAIRS.get(frozenset((zhi_list[i], zhi_list[j])))
            if xing_type:
                result["xing"].append({
                    "type": xing_type,
                    "pillars": [pillar_names[i], pillar_names[j]],
                    "detail": f"{zhi_list[i]}{zhi_list[j]}相刑({get_dist(i, j)})"
                })

    # 三刑全局
    SAN_XING = [("寅", "巳", "申"), ("丑", "戌", "未")]
    for group in SAN_XING:
        hits = [i for i, z in enumerate(zhi_list) if z in group]
        chars_set = set(zhi_list[h] for h in hits)
        if len(chars_set) == 3:
            idxs = sorted(build_positions(group, hits))
            result["xing"].append({
                "type": "三刑全",
                "pillars": [pillar_names[i] for i in idxs],
                "detail": f"{''.join(group)}三刑全"
            })

    # 自刑: 辰辰/午午/酉酉/亥亥
    ZI_XING = ["辰", "午", "酉", "亥"]
    for i in range(4):
        for j in range(i+1, 4):
            if zhi_list[i] == zhi_list[j] and zhi_list[i] in ZI_XING:
                result["xing"].append({
                    "type": "自刑",
                    "pillars": [pillar_names[i], pillar_names[j]],
                    "detail": f"{zhi_list[i]}{zhi_list[j]}自刑({get_dist(i, j)})"
                })

    # 地支相害
    HAI_PAIRS = [{"子", "未"}, {"丑", "午"}, {"寅", "巳"},
                 {"卯", "辰"}, {"申", "亥"}, {"酉", "戌"}]
    for i in range(4):
        for j in range(i+1, 4):
            if {zhi_list[i], zhi_list[j]} in HAI_PAIRS:
                result["hai"].append({
                    "type": "地支害",
                    "pillars": [pillar_names[i], pillar_names[j]],
                    "detail": f"{zhi_list[i]}{zhi_list[j]}相害({get_dist(i, j)})"
                })

    # 地支相破
    PO_PAIRS = [{"子", "酉"}, {"丑", "辰"}, {"寅", "亥"},
                {"卯", "午"}, {"巳", "申"}, {"未", "戌"}]
    for i in range(4):
        for j in range(i+1, 4):
            if {zhi_list[i], zhi_list[j]} in PO_PAIRS:
                result["po"].append({
                    "type": "地支破",
                    "pillars": [pillar_names[i], pillar_names[j]],
                    "detail": f"{zhi_list[i]}{zhi_list[j]}相破({get_dist(i, j)})"
                })

    # 去重
    for key in result:
        seen = set()
        unique = []
        for item in result[key]:
            sig = str(sorted(item.get("pillars", []))) + item.get("detail", "")
            if sig not in seen:
                seen.add(sig)
                unique.append(item)
        result[key] = unique

    return result


# ─────────────────────────────────────────────
# 流年计算
# ─────────────────────────────────────────────

def get_liu_nian(ref_dt: datetime, ri_gan: str) -> dict:
    """按指定日期获取当下流年干支及十神。"""
    solar = Solar.fromYmd(ref_dt.year, ref_dt.month, ref_dt.day)
    lunar = solar.getLunar()
    gz = lunar.getYearInGanZhiExact()
    gan = gz[0]
    zhi = gz[1]
    tg_ss = get_shi_shen(ri_gan, gan)
    dz_cang = CANG_GAN.get(zhi, [])
    dz_ss_list = [get_shi_shen(ri_gan, g) for g, _ in dz_cang if g in WUXING_GAN]
    return {
        "year": ref_dt.year,
        "reference_date": ref_dt.strftime("%Y-%m-%d"),
        "boundary_rule": "流年以立春为界；公历年初若未过立春，仍按上一年干支计。",
        "gan_zhi": gz,
        "tian_gan": gan,
        "di_zhi": zhi,
        "tian_gan_shi_shen": tg_ss,
        "di_zhi_shi_shen": dz_ss_list
    }


# ─────────────────────────────────────────────
# 柱信息构建
# ─────────────────────────────────────────────

def build_pillar(gan: str, zhi: str, ri_gan: Optional[str] = None, is_day_pillar: bool = False) -> dict:
    """构建单柱完整信息"""
    gan_info = {
        "value": gan,
        "wuxing": WUXING_GAN[gan],
        "yinyang": YINYANG_GAN[gan],
    }
    if ri_gan and not is_day_pillar:
        gan_info["shi_shen"] = get_shi_shen(ri_gan, gan)

    # 藏干
    cang_raw = CANG_GAN.get(zhi, [])
    cang_result = {}
    keys = ["zhu_qi", "zhong_qi", "yu_qi"]
    for i, (cg, ctype) in enumerate(cang_raw):
        if i < 3:
            entry = {"value": cg, "wuxing": WUXING_GAN.get(cg, ""), "type": ctype}
            if ri_gan:
                entry["shi_shen"] = get_shi_shen(ri_gan, cg)
            cang_result[keys[i]] = entry
    for k in keys:
        if k not in cang_result:
            cang_result[k] = None

    zhi_info = {
        "value": zhi,
        "wuxing": WUXING_ZHI[zhi],
        "yinyang": YINYANG_ZHI[zhi],
        "cang_gan": cang_result
    }

    # 十二长生
    if ri_gan:
        chang_sheng = get_shi_er_chang_sheng(ri_gan, zhi)
    else:
        chang_sheng = get_shi_er_chang_sheng(gan, zhi)

    return {
        "tian_gan": gan_info,
        "di_zhi": zhi_info,
        "shi_er_zhang_sheng": chang_sheng
    }


def text_width(text: str) -> int:
    """估算终端显示宽度，兼容中文对齐。"""
    width = 0
    for char in ANSI_RE.sub("", str(text)):
        width += 2 if unicodedata.east_asian_width(char) in ("W", "F") else 1
    return width


def pad_text(text: str, width: int) -> str:
    text = str(text)
    return text + " " * max(0, width - text_width(text))


def style(text: str, code: str, enabled: bool) -> str:
    if not enabled:
        return text
    return f"\033[{code}m{text}\033[0m"


def should_use_color(color_mode: str) -> bool:
    if color_mode == "always":
        return True
    if color_mode == "never":
        return False
    if os.environ.get("NO_COLOR"):
        return False
    if os.environ.get("CLICOLOR_FORCE") == "1":
        return True
    return sys.stdout.isatty()


def style_wuxing(text: str, wuxing: str, enabled: bool) -> str:
    return style(text, WUXING_COLOR.get(wuxing, "0"), enabled)


def format_gan(gan: str, enabled: bool) -> str:
    return style_wuxing(gan, WUXING_GAN[gan], enabled)


def format_zhi(zhi: str, enabled: bool) -> str:
    return style_wuxing(zhi, WUXING_ZHI[zhi], enabled)


def format_gan_zhi(gan: str, zhi: str, enabled: bool) -> str:
    return f"{format_gan(gan, enabled)}{format_zhi(zhi, enabled)}"


def format_wuxing_label(wuxing: str, yinyang: str, enabled: bool) -> str:
    return f"{style_wuxing(wuxing, wuxing, enabled)}{yinyang}"


def render_table(headers: list[str], rows: list[list[str]]) -> str:
    widths = [text_width(header) for header in headers]
    for row in rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], text_width(cell))

    header_line = " | ".join(pad_text(header, widths[i]) for i, header in enumerate(headers))
    separator = "-+-".join("-" * widths[i] for i in range(len(headers)))
    body = [" | ".join(pad_text(cell, widths[i]) for i, cell in enumerate(row)) for row in rows]
    return "\n".join([header_line, separator, *body])


def summarize_cang_gan(cang_gan: dict, color_enabled: bool = False) -> str:
    items = []
    for key in ("zhu_qi", "zhong_qi", "yu_qi"):
        entry = cang_gan.get(key)
        if not entry:
            continue
        gan_text = format_gan(entry["value"], color_enabled)
        shi_shen = entry.get("shi_shen")
        if shi_shen:
            items.append(f"{gan_text}({shi_shen})")
        else:
            items.append(gan_text)
    return "/".join(items) if items else "-"


def summarize_relations(xchh: dict) -> str:
    labels = {
        "he": "合",
        "chong": "冲",
        "xing": "刑",
        "hui": "会",
        "hai": "害",
        "po": "破",
    }
    parts = []
    for key in ("he", "chong", "xing", "hui", "hai", "po"):
        items = xchh.get(key, [])
        if items:
            parts.append(f"{labels[key]}: " + "；".join(item["detail"] for item in items))
    return "\n".join(parts) if parts else "未见显著合冲刑会"


def render_pillar_block(name: str, pillar: dict, color_enabled: bool) -> str:
    tian_gan = pillar["tian_gan"]
    di_zhi = pillar["di_zhi"]
    shi_shen = tian_gan.get("shi_shen") or "日主"
    cang_gan = summarize_cang_gan(di_zhi["cang_gan"], color_enabled)
    gan_zhi = format_gan_zhi(tian_gan["value"], di_zhi["value"], color_enabled)
    tian_gan_text = format_gan(tian_gan["value"], color_enabled)
    di_zhi_text = format_zhi(di_zhi["value"], color_enabled)
    return "\n".join([
        f"{name}: {gan_zhi}",
        f"  天干: {tian_gan_text}  {shi_shen}  {format_wuxing_label(tian_gan['wuxing'], tian_gan['yinyang'], color_enabled)}",
        f"  地支: {di_zhi_text}  {format_wuxing_label(di_zhi['wuxing'], di_zhi['yinyang'], color_enabled)}",
        f"  藏干: {cang_gan}",
        f"  长生: {pillar['shi_er_zhang_sheng']}",
    ])


def render_pretty_chart(chart: dict, color_mode: str = "auto") -> str:
    color_enabled = should_use_color(color_mode)
    confirmed = chart["input_confirmed"]
    original_chart = chart["original_chart"]
    life_cycle = chart["life_cycle"]
    current_year = chart["system_context"]["current_year"]
    current_liu_nian = chart["system_context"]["current_liu_nian"]
    pillar_order = [
        ("年柱", original_chart["year_pillar"]),
        ("月柱", original_chart["month_pillar"]),
        ("日柱", original_chart["day_pillar"]),
        ("时柱", original_chart["hour_pillar"]),
    ]

    pillar_blocks = [render_pillar_block(name, pillar, color_enabled) for name, pillar in pillar_order]

    da_yun_rows = []
    for index, item in enumerate(life_cycle["da_yun_list"]):
        marker = "=>" if index == life_cycle["current_da_yun_index"] else "  "
        gan_zhi = item["gan_zhi"]
        da_yun_rows.append([
            style(marker, "1;35", color_enabled) if marker == "=>" else marker,
            str(item["step"]),
            format_gan_zhi(gan_zhi[0], gan_zhi[1], color_enabled),
            item["tian_gan_shi_shen"],
            "/".join(item["di_zhi_shi_shen"]) if item["di_zhi_shi_shen"] else "-",
            f"{item['start_age']}-{item['end_age']}岁",
            f"{item['start_year']}-{item['end_year']}",
        ])

    title = style("=== 八字命盘 ===", "1;36", color_enabled)
    subtitle = style(
        f"{confirmed['solar_datetime_original']}  {confirmed['birth_place']}  {'男' if confirmed['gender'] == 'M' else '女'}",
        "2;37",
        color_enabled,
    )
    corrected = (
        f"真太阳时: {confirmed['solar_datetime_corrected']}"
        f"  经纬度: {confirmed['coordinates']['lat']}, {confirmed['coordinates']['lon']}"
        f"  时区: {confirmed['timezone']}"
        f"  解析: {confirmed['birth_place_resolved']} ({confirmed['location_source']})"
        f"  历法: {'农历' if confirmed['calendar_type'] == 'lunar' else '公历'}"
    )
    ri_gan = original_chart["ri_zhu_tian_gan"]
    day_master = style(
        f"日主: {format_gan(ri_gan, color_enabled)}({format_wuxing_label(original_chart['ri_zhu_wuxing'], original_chart['ri_zhu_yinyang'], color_enabled)})",
        "1;33",
        color_enabled,
    )
    liu_nian_gz = current_liu_nian["gan_zhi"]
    liu_nian = (
        f"当前流年: {current_year} {format_gan_zhi(liu_nian_gz[0], liu_nian_gz[1], color_enabled)}"
        f"  天干十神: {current_liu_nian['tian_gan_shi_shen']}"
        f"  地支十神: {'/'.join(current_liu_nian['di_zhi_shi_shen']) if current_liu_nian['di_zhi_shi_shen'] else '-'}"
    )
    liu_nian_rule = current_liu_nian["boundary_rule"]
    qi_yun = f"起运: {life_cycle['qi_yun_age']}岁 ({life_cycle['qi_yun_date']})"
    display_hint = "显示模式: ANSI 彩色" if color_enabled else "显示模式: 纯文本（当前环境不支持或未启用 ANSI 颜色）"

    lines = [
        title,
        subtitle,
        display_hint,
        corrected,
        day_master,
        "",
        style("[四柱总览]", "1;34", color_enabled),
        "\n\n".join(pillar_blocks),
        "",
        style("[刑冲合会害破]", "1;34", color_enabled),
        summarize_relations(original_chart["xing_chong_he_hui"]),
        "",
        style("[大运]", "1;34", color_enabled),
        f"说明: 标记 => 的为当前大运。{qi_yun}",
        render_table(["  ", "步", "干支", "天干十神", "地支十神", "年龄", "年份"], da_yun_rows),
        "",
        style("[当下]", "1;34", color_enabled),
        liu_nian,
        liu_nian_rule,
    ]
    return "\n".join(lines)


def parse_cli_args(argv: list[str]) -> tuple[dict, str, str]:
    parser = argparse.ArgumentParser(description="八字排盘计算")
    parser.add_argument("payload", nargs="?", help="JSON 参数")
    parser.add_argument("--pretty", action="store_true", help="以终端友好的格式展示命盘")
    parser.add_argument("--color", choices=["auto", "always", "never"], default="auto", help="pretty 模式下的颜色策略")
    parser.add_argument("--json", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args(argv)

    if args.pretty and args.json:
        parser.error("--pretty 和 --json 不能同时使用")

    if args.pretty:
        output_mode = "pretty"
    elif args.json:
        output_mode = "json"
    else:
        output_mode = "pretty" if args.payload else "json"

    if args.payload:
        params = json.loads(args.payload)
    else:
        params = json.load(sys.stdin)

    return params, output_mode, args.color


# ─────────────────────────────────────────────
# 主函数
# ─────────────────────────────────────────────

def calculate(
    calendar_type: str,   # "gregorian" | "lunar"
    year: int,
    month: int,
    day: int,
    hour: int,
    minute: int,
    gender: str,          # "M" | "F"
    birth_place: str,
    is_leap_month: bool = False
) -> dict:

    # 1. 构建出生地本地时间
    local_dt = datetime(year, month, day, hour, minute)

    # 2. 获取出生地经纬度与时区
    location_info = resolve_birth_place(birth_place, local_dt)
    lat = location_info["lat"]
    lon = location_info["lon"]

    # 3. 真太阳时校正
    corrected_dt = correct_solar_time(local_dt, lon, location_info["standard_longitude"])

    # 4. 转换为 Solar 对象
    if calendar_type == "lunar":
        lunar_obj = Lunar.fromYmdHms(year, month, day, corrected_dt.hour, corrected_dt.minute, 0)
        if is_leap_month:
            # lunar-python 闰月处理
            lunar_obj = Lunar.fromYmdHms(year, -month, day, corrected_dt.hour, corrected_dt.minute, 0)
        solar_obj = lunar_obj.getSolar()
    else:
        solar_obj = Solar.fromYmdHms(
            corrected_dt.year, corrected_dt.month, corrected_dt.day,
            corrected_dt.hour, corrected_dt.minute, 0
        )

    # 5. 八字排盘（sect=2: 23:00-23:59 算当天）
    bazi = solar_obj.getLunar().getEightChar()
    bazi.setSect(2)

    # 提取四柱干支
    year_gz  = (bazi.getYearGan(), bazi.getYearZhi())
    month_gz = (bazi.getMonthGan(), bazi.getMonthZhi())
    day_gz   = (bazi.getDayGan(), bazi.getDayZhi())
    hour_gz  = (bazi.getTimeGan(), bazi.getTimeZhi())

    ri_gan = day_gz[0]

    # 6. 构建四柱
    year_pillar  = build_pillar(*year_gz,  ri_gan=ri_gan)
    month_pillar = build_pillar(*month_gz, ri_gan=ri_gan)
    day_pillar   = build_pillar(*day_gz,   ri_gan=ri_gan, is_day_pillar=True)
    hour_pillar  = build_pillar(*hour_gz,  ri_gan=ri_gan)

    # 7. 刑冲合会
    pillars_map = {
        "year": year_gz, "month": month_gz,
        "day": day_gz, "hour": hour_gz
    }
    xchh = calc_xing_chong_he_hui(pillars_map)

    # 8. 大运
    yun = bazi.getYun(1 if gender == "M" else 0)
    qi_yun_solar = yun.getStartSolar()
    qi_yun_age = qi_yun_solar.getYear() - solar_obj.getYear()
    
    # 获取大运列表
    da_yun_list = []
    current_dt = datetime.now()
    current_year_ad = current_dt.year
    current_da_yun_index = 0

    for i, dy in enumerate(yun.getDaYun()):
        if dy.getIndex() == 0:
            continue  # 跳过第0柱（命宫/小运起始）
        start_year = dy.getStartYear()
        end_year   = dy.getEndYear()
        start_age  = dy.getStartAge()
        end_age    = dy.getEndAge()
        gan_dy = dy.getGanZhi()[0]
        zhi_dy = dy.getGanZhi()[1]

        tg_ss = get_shi_shen(ri_gan, gan_dy)
        dz_cang = CANG_GAN.get(zhi_dy, [])
        dz_ss_list = [get_shi_shen(ri_gan, g) for g, _ in dz_cang if g in WUXING_GAN]

        entry = {
            "step": len(da_yun_list) + 1,
            "gan_zhi": gan_dy + zhi_dy,
            "tian_gan_shi_shen": tg_ss,
            "di_zhi_shi_shen": dz_ss_list,
            "di_zhi_cang_gan": [g for g, _ in dz_cang],
            "start_age": start_age,
            "end_age": end_age,
            "start_year": start_year,
            "end_year": end_year
        }
        da_yun_list.append(entry)

        if start_year <= current_year_ad <= end_year:
            current_da_yun_index = len(da_yun_list) - 1

    # 9. 流年
    liu_nian = get_liu_nian(current_dt, ri_gan)

    # 10. 组装输出
    return {
        "system_context": {
            "current_date": current_dt.strftime("%Y-%m-%d"),
            "current_year": current_year_ad,
            "current_liu_nian": liu_nian
        },
        "input_confirmed": {
            "solar_datetime_original": local_dt.strftime("%Y-%m-%d %H:%M"),
            "solar_datetime_corrected": corrected_dt.strftime("%Y-%m-%d %H:%M"),
            "birth_place": birth_place,
            "birth_place_resolved": location_info["resolved_name"],
            "coordinates": {"lat": round(lat, 4), "lon": round(lon, 4)},
            "timezone": location_info["timezone"],
            "location_source": location_info["source"],
            "gender": gender,
            "calendar_type": calendar_type
        },
        "original_chart": {
            "ri_zhu_tian_gan": ri_gan,
            "ri_zhu_wuxing": WUXING_GAN[ri_gan],
            "ri_zhu_yinyang": YINYANG_GAN[ri_gan],
            "year_pillar": year_pillar,
            "month_pillar": month_pillar,
            "day_pillar": day_pillar,
            "hour_pillar": hour_pillar,
            "xing_chong_he_hui": xchh
        },
        "life_cycle": {
            "qi_yun_age": qi_yun_age,
            "qi_yun_date": f"{qi_yun_solar.getYear()}-{qi_yun_solar.getMonth():02d}-{qi_yun_solar.getDay():02d}",
            "current_da_yun_index": current_da_yun_index,
            "da_yun_list": da_yun_list
        }
    }


# ─────────────────────────────────────────────
# CLI 入口（供 Tool Call 调用）
# ─────────────────────────────────────────────

if __name__ == "__main__":
    params, output_mode, color_mode = parse_cli_args(sys.argv[1:])
    params.setdefault("calendar_type", "gregorian")
    result = calculate(**params)
    if output_mode == "pretty":
        print(render_pretty_chart(result, color_mode=color_mode))
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))
