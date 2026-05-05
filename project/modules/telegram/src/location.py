"""中国城市经纬度查询（优先离线区县级库 china-region，回退内置 CSV）"""

import csv
import re

try:
    import china_region  # 区县级经纬度离线库，search / search_all

    _CR_AVAILABLE = True
except Exception:
    _CR_AVAILABLE = False

# 回退数据
from _paths import CHINA_COORDS_CSV

_DATA = {}
_csv_path = CHINA_COORDS_CSV


def _load_csv():
    if _DATA:
        return
    with open(_csv_path, encoding="utf-8") as f:
        for row in csv.reader(f):
            if len(row) >= 4:
                code, name, lng, lat = row[0], row[1], float(row[2]), float(row[3])
                _DATA[name] = (lng, lat, code)
                # 去掉行政区后缀也能匹配
                for suffix in ["市", "区", "县", "省", "自治区", "特别行政区"]:
                    if name.endswith(suffix) and len(name) > 2:
                        _DATA[name[: -len(suffix)]] = (lng, lat, code)


_load_csv()


def _normalized_queries(query: str) -> list[str]:
    """构造若干查询关键词，优先精确（县区名），再回退原文本"""
    q = query.strip()
    if not q:
        return []
    merged = q.replace(" ", "")
    candidates = []
    # 抓取末尾的“XX区/县/市/旗/州/盟”片段
    matches = re.findall(r"([\u4e00-\u9fa5]{1,8}?(?:区|县|市|旗|州|盟))", merged)
    candidates.extend(matches)
    candidates.append(merged)
    candidates = [c for c in candidates if c]
    # 去重，保持顺序
    seen = set()
    uniq = []
    for c in candidates:
        if c in seen:
            continue
        seen.add(c)
        uniq.append(c)
    return uniq


def _search_cr(query: str) -> list[tuple[str, float, float]]:
    """china-region 模糊搜索，返回 [(名称, lng, lat)]"""
    if not _CR_AVAILABLE:
        return []
    res = []
    for q in _normalized_queries(query):
        try:
            items = china_region.search_all(q)  # 已按匹配度排序
        except Exception:
            items = []
        for item in items:
            # 组名如“山东省济南市历下区”
            name = "".join([item.get("province", ""), item.get("city", ""), item.get("county", "")]) or q
            county = item.get("county", "")
            score = 0
            if county and county in query:
                score += 3
            if name and name == query:
                score += 2
            if query in name or name in query:
                score += 1
            try:
                lng = float(item["longitude"])
                lat = float(item["latitude"])
            except Exception:
                continue
            res.append((score, name, lng, lat))
        if res:
            break  # 有结果就不再用更宽松的查询
    # 去重
    res.sort(key=lambda x: (-x[0], len(x[1])))
    seen = set()
    uniq = []
    for _, n, lng, lat in res:
        if n in seen:
            continue
        seen.add(n)
        uniq.append((n, lng, lat))
    return uniq


def search(query: str) -> list[tuple[str, float, float]]:
    """搜索地点，返回 [(名称, 经度, 纬度), ...]"""
    query = query.strip()
    if not query:
        return []
    # 1) 优先用 china-region 全量区县库
    res = _search_cr(query)
    if res:
        return res

    # 2) 回退到内置 CSV 子串匹配（市级）
    results = []
    for name, (lng, lat, _code) in _DATA.items():
        if query in name or name in query:
            results.append((name, lng, lat))
    # 去重
    seen = set()
    unique = []
    for r in results:
        if r[0] not in seen:
            seen.add(r[0])
            unique.append(r)
    return unique


def get_coords(name: str) -> tuple[float, float] | None:
    """获取经纬度，返回 (经度, 纬度) 或 None"""
    name = name.strip()
    if not name:
        return None

    # china-region 优先
    res = _search_cr(name)
    if res:
        return res[0][1], res[0][2]

    # 内置 CSV 精确
    if name in _DATA:
        return _DATA[name][:2]
    # 内置 CSV 模糊
    for key, (lng, lat, _code) in _DATA.items():
        if name in key or key in name:
            return (lng, lat)
    return None


# 常用城市快捷
COMMON_CITIES = {
    "北京": (116.4, 39.9),
    "上海": (121.5, 31.2),
    "广州": (113.3, 23.1),
    "深圳": (114.1, 22.5),
    "成都": (104.1, 30.7),
    "杭州": (120.2, 30.3),
    "重庆": (106.5, 29.5),
    "武汉": (114.3, 30.6),
    "西安": (108.9, 34.3),
    "南京": (118.8, 32.1),
    "天津": (117.2, 39.1),
    "苏州": (120.6, 31.3),
}


def get(name: str) -> tuple[float, float]:
    """
    获取经纬度（严格模式）
    - 支持用户直接传入“lng,lat”
    - 支持常用城市快捷与离线库
    - 未命中则抛出异常（禁止回退到“北京”导致静默错误）
    """
    name = (name or "").strip()
    if not name:
        raise ValueError("地点为空")

    # 允许直接传入坐标字符串：lng,lat
    m = re.match(r"^\s*(-?\d+(?:\.\d+)?)\s*,\s*(-?\d+(?:\.\d+)?)\s*$", name)
    if m:
        return float(m.group(1)), float(m.group(2))

    if name in COMMON_CITIES:
        return COMMON_CITIES[name]

    coords = get_coords(name)
    if coords:
        return coords

    raise ValueError(f"地点无法识别: {name}")


if __name__ == "__main__":
    print(f"CSV 数据量: {len(_DATA)} china-region: {_CR_AVAILABLE}")
    print(f"北京: {get('北京')}")
    print(f"历下区: {get('历下区')}")
    print(f"搜索'济南市历下区': {search('济南市历下区')[:3]}")
