#!/usr/bin/env python3

import os
import sys

sys.path.append("modules/telegram/src")
import json
from datetime import datetime

from bazi_calculator import BaziCalculator


def generate_complete_output():
    """生成兼容输出测试文档"""

    # 执行 legacy 计算
    calc = BaziCalculator(birth_dt=datetime(1990, 5, 15, 14, 30), gender="male", longitude=114.1)
    result = calc.calculate()

    # 生成兼容输出文档
    output = []
    output.append("# FateCat 兼容输出测试文档")
    output.append("# 测试时间: 2025-12-15 14:40")
    output.append("# 输入参数: 1990-05-15 14:30 北京 男性")
    output.append("")

    output.append("## 1. 输出字段统计")
    output.append(f"总字段数: {len(result)}个")
    output.append(f"字段列表: {list(result.keys())}")
    output.append("")

    output.append("## 2. 分类输出结果")
    output.append("")

    # 按分类输出
    categories = {
        "核心八字": [
            "fourPillars",
            "hiddenStems",
            "tenGods",
            "twelveGrowth",
            "fiveElements",
            "wuxingState",
            "dayMaster",
        ],
        "特殊宫位": ["specialPalaces", "voidInfo", "mingGua"],
        "神煞格局": ["spirits", "geju", "yongShen"],
        "运势分析": ["majorFortune", "annualFortune", "monthlyFortune", "xiaoYun", "jiaoYun"],
        "时间历法": ["birthInfo", "jieqiDetail", "siling", "trueSolarTime"],
        "传统算命": ["boneWeight", "huangLi"],
        "关系分析": ["ganzhiRelations"],
    }

    for category, fields in categories.items():
        output.append(f"### {category}模块")
        output.append("")

        for field in fields:
            if field in result:
                value = result[field]
                output.append(f"#### {field}")

                # 格式化输出
                if isinstance(value, (dict, list)):
                    try:
                        formatted = json.dumps(value, ensure_ascii=False, indent=2)
                        output.append("```json")
                        output.append(formatted)
                        output.append("```")
                    except Exception:
                        output.append(f"值: {str(value)}")
                else:
                    output.append(f"值: {value}")

                output.append("")

        output.append("")

    # 输出 JSON
    output.append("## 3. JSON 输出")
    output.append("")
    output.append("```json")
    try:
        formatted_json = json.dumps(result, ensure_ascii=False, indent=2, default=str)
        output.append(formatted_json)
    except Exception as e:
        output.append(f"JSON序列化错误: {e}")
        output.append(str(result))
    output.append("```")

    # 写入文件
    output_file = "兼容输出测试文档.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(output))

    print(f"兼容输出测试文档已生成: {os.path.abspath(output_file)}")
    print(f"总字段数: {len(result)}个")
    print(f"文档行数: {len(output)}行")

    return len(result), len(output)


if __name__ == "__main__":
    generate_complete_output()
