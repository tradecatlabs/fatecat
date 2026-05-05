#!/usr/bin/env python3

import os
import sys

sys.path.append("modules/telegram/src")
from datetime import datetime

from bazi_calculator import BaziCalculator


def generate_user_report():
    """生成用户友好的八字排盘报告"""

    # 执行计算
    calc = BaziCalculator(birth_dt=datetime(1990, 5, 15, 14, 30), gender="male", longitude=114.1)
    result = calc.calculate()

    # 生成报告
    report = []

    # 标题
    report.append("═" * 60)
    report.append("                    八字排盘详细报告")
    report.append("═" * 60)
    report.append("")
    report.append("姓名：张三                    性别：男")
    report.append("公历：1990年05月15日 14时30分")
    report.append("农历：" + result["birthInfo"]["lunarCn"])
    report.append("生肖：" + result["birthInfo"]["zodiac"] + "        星座：" + result["birthInfo"]["constellation"])
    report.append("地点：深圳                    经度：114.1°E")
    report.append("真太阳时：" + result["trueSolarTime"])
    report.append("")

    # 四柱八字
    report.append("┌" + "─" * 58 + "┐")
    report.append("│                        四柱八字                        │")
    report.append("├" + "─" * 58 + "┤")

    pillars = result["fourPillars"]
    report.append("│        年柱        月柱        日柱        时柱        │")
    report.append("│      ────────    ────────    ────────    ────────      │")
    report.append(
        f"│        {pillars['year']['fullName']}        {pillars['month']['fullName']}        {pillars['day']['fullName']}        {pillars['hour']['fullName']}        │"
    )
    report.append(
        f"│      {pillars['year']['nayin']}    {pillars['month']['nayin']}    {pillars['day']['nayin']}    {pillars['hour']['nayin']}      │"
    )
    report.append("└" + "─" * 58 + "┘")
    report.append("")

    # 藏干十神
    report.append("┌" + "─" * 58 + "┐")
    report.append("│                        藏干十神                        │")
    report.append("├" + "─" * 58 + "┤")

    hidden = result["hiddenStems"]
    tengods = result["tenGods"]

    report.append("│  藏干：")
    report.append(f"│    年支{pillars['year']['branch']}藏：{' '.join(hidden['year'])}")
    report.append(f"│    月支{pillars['month']['branch']}藏：{' '.join(hidden['month'])}")
    report.append(f"│    日支{pillars['day']['branch']}藏：{' '.join(hidden['day'])}")
    report.append(f"│    时支{pillars['hour']['branch']}藏：{' '.join(hidden['hour'])}")
    report.append("│")
    report.append("│  十神：")
    report.append(f"│    年柱：{tengods['year']['stem']} - {' '.join(tengods['year']['branch'])}")
    report.append(f"│    月柱：{tengods['month']['stem']} - {' '.join(tengods['month']['branch'])}")
    report.append(f"│    日柱：{tengods['day']['stem']} - {' '.join(tengods['day']['branch'])}")
    report.append(f"│    时柱：{tengods['hour']['stem']} - {' '.join(tengods['hour']['branch'])}")
    report.append("└" + "─" * 58 + "┘")
    report.append("")

    # 五行分析
    report.append("┌" + "─" * 58 + "┐")
    report.append("│                        五行分析                        │")
    report.append("├" + "─" * 58 + "┤")

    elements = result["fiveElements"]
    wuxing_state = result["wuxingState"]

    report.append("│  五行统计：")
    for elem, data in elements.items():
        cn_name = data["chineseName"]
        count = data["count"]
        percent = data["percentage"]
        state = wuxing_state[elem]["state"]
        report.append(f"│    {cn_name}：{count}个 ({percent}%) - {state}")

    report.append("│")
    report.append("│  日主分析：")
    daymaster = result["dayMaster"]
    report.append(f"│    日主：{daymaster['stem']}({daymaster['elementCn']}) - {daymaster['yinYang']}")
    report.append(f"│    强弱：{daymaster['strength']}")
    report.append(f"│    自坐：{daymaster['selfSitting']}")
    report.append("└" + "─" * 58 + "┘")
    report.append("")

    # 神煞系统
    report.append("┌" + "─" * 58 + "┐")
    report.append("│                        神煞系统                        │")
    report.append("├" + "─" * 58 + "┤")

    spirits = result["spirits"]
    report.append("│  吉神：")
    if spirits["auspicious"]:
        for spirit in spirits["auspicious"]:
            report.append(f"│    ✓ {spirit}")
    else:
        report.append("│    无")

    report.append("│")
    report.append("│  凶煞：")
    if spirits["inauspicious"]:
        for spirit in spirits["inauspicious"]:
            report.append(f"│    ✗ {spirit}")
    else:
        report.append("│    无")

    report.append("│")
    report.append("│  特殊：")
    if spirits["special"]:
        for spirit in spirits["special"]:
            report.append(f"│    ◆ {spirit}")
    else:
        report.append("│    无")

    report.append("└" + "─" * 58 + "┘")
    report.append("")

    # 格局用神
    report.append("┌" + "─" * 58 + "┐")
    report.append("│                      格局用神                          │")
    report.append("├" + "─" * 58 + "┤")

    geju = result["geju"]
    yongshen = result["yongShen"]

    report.append(f"│  主格局：{geju['main']}")
    if len(geju["patterns"]) > 1:
        report.append("│  兼格局：" + "、".join([p for p in geju["patterns"] if p != geju["main"]]))

    report.append("│")
    report.append("│  调候用神：")
    if yongshen["tiaoHou"]["xi"]:
        report.append(f"│    喜用：{' '.join(yongshen['tiaoHou']['xi'])}")
    if yongshen["tiaoHou"]["ji"]:
        report.append(f"│    忌神：{' '.join(yongshen['tiaoHou']['ji'])}")

    if yongshen.get("note"):
        report.append(f"│  说明：{yongshen['note']}")

    report.append("└" + "─" * 58 + "┘")
    report.append("")

    # 大运流年
    report.append("┌" + "─" * 58 + "┐")
    report.append("│                      大运流年                          │")
    report.append("├" + "─" * 58 + "┤")

    major_fortune = result["majorFortune"]
    report.append(f"│  起运：{major_fortune['direction']} - {major_fortune['startDetail']}")
    report.append(f"│  交运：{major_fortune['startAge']}岁 ({major_fortune['startYear']}年)")

    report.append("│")
    report.append("│  大运排列：")
    for pillar in major_fortune["pillars"][:5]:  # 显示前5步大运
        shishen = pillar.get("shishen", pillar.get("tenGod", "未知"))
        report.append(f"│    {pillar['age']}岁: {pillar['fullName']} ({shishen}) - {pillar['startYear']}年起")

    report.append("└" + "─" * 58 + "┘")
    report.append("")

    # 称骨算命
    report.append("┌" + "─" * 58 + "┐")
    report.append("│                      称骨算命                          │")
    report.append("├" + "─" * 58 + "┤")

    bone_weight = result["boneWeight"]
    report.append(f"│  骨重：{bone_weight['weightCn']}")
    report.append("│")
    report.append("│  命书：")

    # 分行显示命书内容
    text_lines = bone_weight["text"].split("，")
    for line in text_lines:
        if line.strip():
            report.append(f"│    {line.strip()}")

    report.append("└" + "─" * 58 + "┘")
    report.append("")

    # 命宫分析
    report.append("┌" + "─" * 58 + "┐")
    report.append("│                      命宫分析                          │")
    report.append("├" + "─" * 58 + "┤")

    ming_gua = result["mingGua"]
    special_palaces = result["specialPalaces"]

    report.append(f"│  命卦：{ming_gua['guaName']}卦 - {ming_gua['group']}")
    report.append(f"│  方位：{ming_gua['direction']}")
    report.append("│")
    report.append("│  特殊宫位：")
    report.append(f"│    胎元：{special_palaces['taiYuan']['pillar']} ({special_palaces['taiYuan']['nayin']})")
    report.append(f"│    胎息：{special_palaces['taiXi']['pillar']} ({special_palaces['taiXi']['nayin']})")
    report.append(f"│    命宫：{special_palaces['mingGong']['pillar']} ({special_palaces['mingGong']['nayin']})")
    report.append(f"│    身宫：{special_palaces['shenGong']['pillar']} ({special_palaces['shenGong']['nayin']})")

    report.append("└" + "─" * 58 + "┘")
    report.append("")

    # 报告尾部
    report.append("═" * 60)
    report.append("                  FateCat 八字排盘系统")
    report.append("                    生成时间：2025-12-15 14:41")
    report.append("═" * 60)

    # 写入文件
    output_file = "八字排盘详细报告.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(report))

    print(f"八字排盘详细报告已生成: {os.path.abspath(output_file)}")
    print(f"报告行数: {len(report)}行")

    return len(report)


if __name__ == "__main__":
    generate_user_report()
