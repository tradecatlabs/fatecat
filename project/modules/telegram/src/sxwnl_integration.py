#!/usr/bin/env python3
"""
寿星万年历集成器 - 强制使用原生库，失败即报错

外部库依赖注入 (相对路径从项目根目录):
└── assets/vendor/github/sxwnl-master/
    ├── sxwnl_interface.js  # 接口文件
    └── 源程序/
        ├── lunar.js    # 核心历法算法
        └── JW.js       # 儒略日计算

运行环境: Node.js 18+
纯净性声明: 强制调用原生JavaScript算法，失败即抛异常终止
"""

import json
import subprocess
from datetime import datetime
from typing import Any

from _paths import SXWNL_INTERFACE_JS

SXWNL_INTERFACE = str(SXWNL_INTERFACE_JS)


class SXWNLCalculator:
    """寿星万年历集成器 - 强制使用原生库，失败即报错"""

    def __init__(self, birth_dt: datetime, longitude: float):
        self.birth_dt = birth_dt
        self.longitude = longitude

    def calculate_high_precision_calendar(self) -> dict[str, Any]:
        """高精度历法计算 - 强制使用寿星万年历原生算法"""
        result = subprocess.run(
            [
                "node",
                SXWNL_INTERFACE,
                str(self.birth_dt.year),
                str(self.birth_dt.month),
                str(self.birth_dt.day),
                str(self.birth_dt.hour),
                str(self.birth_dt.minute),
            ],
            capture_output=True,
            text=True,
            timeout=30,
        )

        if result.returncode != 0:
            raise RuntimeError(f"寿星万年历原生算法执行失败: {result.stderr}")

        try:
            data = json.loads(result.stdout)
            return {
                "sxwnl": data,
                "precision": {"level": "astronomical", "source": "sxwnl-master"},
                "astronomy": {"julianDay": data.get("julianDay", 0)},
            }
        except json.JSONDecodeError as e:
            raise RuntimeError(f"寿星万年历输出解析失败: {e}") from e

    def get_complete_analysis(self) -> dict[str, Any]:
        """完整分析"""
        return self.calculate_high_precision_calendar()
