"""fate_core 命理胶水层主包。

顶层包保持轻量，避免能力发现命令提前加载需要外部引擎资产的计算模块。
"""

from __future__ import annotations

from typing import Any

__all__ = [
    "PureAnalysisInput",
    "calculate_pure_analysis",
]


def __getattr__(name: str) -> Any:
    if name in __all__:
        from .usecases import PureAnalysisInput, calculate_pure_analysis

        return {
            "PureAnalysisInput": PureAnalysisInput,
            "calculate_pure_analysis": calculate_pure_analysis,
        }[name]
    raise AttributeError(name)
