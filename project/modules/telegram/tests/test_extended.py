#!/usr/bin/env python3

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from datetime import datetime

from bazi_calculator import BaziCalculator
from location import get as get_loc


def test_extended_features():
    print("🔮 测试扩展功能")
    print("=" * 50)

    # 创建计算器
    lng, lat = get_loc("深圳")
    calc = BaziCalculator(
        birth_dt=datetime(1990, 5, 15, 14, 30),
        gender="male",
        longitude=lng,
        latitude=lat,
        name="张三",
        birth_place="深圳",
    )

    # 执行计算
    try:
        result = calc.calculate()
    except Exception as e:
        print(f"❌ 计算失败: {e}")
        return

    # 显示基础信息
    fp = result["fourPillars"]
    print(f"四柱: {fp['year']['fullName']} {fp['month']['fullName']} {fp['day']['fullName']} {fp['hour']['fullName']}")

    # 显示扩展功能（存在即打印关键摘要）
    qm = result.get("qimenDunjia", {})
    if qm:
        print("🎯 奇门遁甲: 已计算")
    zw = result.get("ziweiBasic", {})
    if zw:
        mg = zw.get("mingGong", {})
        if isinstance(mg, dict) and mg.get("dizhi"):
            print(f"⭐ 紫微斗数: 命宫{mg.get('dizhi')}")
    lr = result.get("liurenDivination", {})
    if lr:
        print("🔢 大六壬: 已计算")

    print("=" * 50)
    print("✅ 扩展功能测试完成")


if __name__ == "__main__":
    test_extended_features()
