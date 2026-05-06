#!/usr/bin/env python3

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import json
from datetime import datetime

from bazi_calculator import BaziCalculator
from location import get as get_loc


def test_complete_integration():
    print("🔮 测试 legacy 集成功能")
    print("=" * 70)

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

    print("🎯 关键字段校验:")
    ctst = result.get("completeTrueSolarTime", {})
    if ctst:
        print(f"✅ 真太阳时: {ctst.get('trueSolarTime')}")
    zta = result.get("ziTimeAnalysis", {})
    if zta:
        print(f"✅ 子时判定: 时支{zta.get('timeZhi', '')} 触发{zta.get('zwzShift')}")
    ws = result.get("wuxingScores", {})
    if ws:
        print(f"✅ 强弱口径: {ws.get('weakStrong')}")
    sp = result.get("spiritsFull", {}).get("byPillar", {})
    if sp:
        print(
            f"✅ 神煞口径: 年{len(sp.get('year', []))} 月{len(sp.get('month', []))} 日{len(sp.get('day', []))} 时{len(sp.get('hour', []))}"
        )

    print()
    print("=" * 70)
    print(f"🎯 当前集成字段数: {total_fields}个字段")
    print("🌟 当前结果来自本地 legacy 计算链路")

    # 保存结果
    with open("complete_integration_result.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2, default=str)
    print("📄 结果已保存到 complete_integration_result.json")


if __name__ == "__main__":
    test_complete_integration()
