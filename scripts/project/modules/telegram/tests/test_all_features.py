#!/usr/bin/env python3

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import json
from datetime import datetime

from bazi_calculator import BaziCalculator
from location import get as get_loc


def test_all_features():
    print("🔮 测试所有功能")
    print("=" * 60)

    # 创建计算器
    lng, lat = get_loc("北京")
    calc = BaziCalculator(
        birth_dt=datetime(1990, 5, 15, 14, 30),
        gender="male",
        longitude=lng,
        latitude=lat,
        name="测试用户",
        birth_place="北京",
    )

    # 执行计算
    try:
        result = calc.calculate()
    except Exception as e:
        print(f"❌ 计算失败: {e}")
        return

    # 统计字段数量
    total_fields = len(result)
    print(f"📊 总字段数: {total_fields}")
    print()

    # 显示关键字段（失败即抛异常，不再使用 error dict 口径）
    fp = result.get("fourPillars", {})
    if fp:
        print(
            f"✅ fourPillars: {fp['year']['fullName']} {fp['month']['fullName']} {fp['day']['fullName']} {fp['hour']['fullName']}"
        )
    sp = result.get("spiritsFull", {}).get("byPillar", {})
    if sp:
        print(
            f"✅ spiritsFull: 年{len(sp.get('year', []))} 月{len(sp.get('month', []))} 日{len(sp.get('day', []))} 时{len(sp.get('hour', []))}"
        )
    ys = result.get("yongShen", {}).get("tiaoHou", {})
    if ys:
        print(f"✅ yongShen: 喜{len(ys.get('xi', []))} 忌{len(ys.get('ji', []))}")
    ctst = result.get("completeTrueSolarTime", {})
    if ctst:
        print(f"✅ completeTrueSolarTime: {ctst.get('trueSolarTime')}")

    print()
    print("=" * 60)
    print(f"🎯 功能完成度: {total_fields}个字段")

    # 保存结果到文件
    with open("complete_result.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print("📄 结果已保存到 complete_result.json")


if __name__ == "__main__":
    test_all_features()
