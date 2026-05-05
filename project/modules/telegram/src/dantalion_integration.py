#!/usr/bin/env python3
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
现代化八字集成器 - 通过外部 dantalion-core (Node) 计算
"""

import json
import subprocess
from datetime import datetime
from typing import Any

from _paths import DANTALION_BRIDGE_JS

BRIDGE = DANTALION_BRIDGE_JS


class DantalionCalculator:
    """现代化八字集成器（严格复用外部 dantalion-core）"""

    def __init__(self, birth_dt: datetime, gender: str):
        self.birth_dt = birth_dt
        self.gender = gender

    def calculate_modern_bazi(self) -> dict[str, Any]:
        """调用外部 dantalion-core 生成现代化人格分析"""
        if not BRIDGE.exists():
            raise RuntimeError("缺少 dantalion_bridge.js，无法调用 dantalion-core")
        birth_str = self.birth_dt.strftime("%Y-%m-%d")
        try:
            out = subprocess.check_output(
                ["node", str(BRIDGE), "--birth", birth_str],
                timeout=10,
            ).decode("utf-8")
            data = json.loads(out)
        except Exception as e:
            raise RuntimeError(f"dantalion-core 调用失败: {e}") from e

        return {
            "modernBazi": {
                "source": "dantalion-core",
                "birthDate": birth_str,
                "gender": self.gender,
                "personality": data,
            },
            "typescript": {"model": "dantalion-core"},
            "api": {"interface": "node-bridge"},
        }

    def get_complete_modern_analysis(self) -> dict[str, Any]:
        return self.calculate_modern_bazi()
