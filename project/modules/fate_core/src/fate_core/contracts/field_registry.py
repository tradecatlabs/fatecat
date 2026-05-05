from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from fate_core.contracts.profile_loader import load_profile


def get_profile_fields(profile_name: str) -> tuple[str, ...]:
    """返回某个 profile 允许输出的字段列表。"""
    profile = load_profile(profile_name)
    return tuple(profile["fields"])


def project_result(result: Mapping[str, Any], profile_name: str) -> dict[str, Any]:
    """按 profile 投影输出字段。"""
    return {field_name: result[field_name] for field_name in get_profile_fields(profile_name) if field_name in result}
