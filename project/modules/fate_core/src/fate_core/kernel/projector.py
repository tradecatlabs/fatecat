from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from fate_core.contracts import project_result


def project_by_profile(result: Mapping[str, Any], profile_name: str) -> dict[str, Any]:
    """将完整结果按 profile 裁剪为目标输出。"""
    return dict(project_result(result, profile_name))
