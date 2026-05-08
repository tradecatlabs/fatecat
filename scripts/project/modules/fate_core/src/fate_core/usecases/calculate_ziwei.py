from __future__ import annotations

from typing import Any

from fate_core.adapters import ZiweiIztroInput, calculate_ziwei_iztro
from fate_core.usecases.calculate_pure_analysis import (
    PureAnalysisInput,
    build_pure_analysis_input_from_payload,
    normalize_gender,
)


def build_ziwei_input_from_payload(raw_payload: dict[str, Any]) -> PureAnalysisInput:
    """从统一 payload 构造紫微斗数输入。"""
    return build_pure_analysis_input_from_payload(raw_payload)


def _public_place(place: str) -> str:
    return place if "北京" in place else "已填写（非北京地区已隐藏）"


def _select_ziwei_payload(raw: dict[str, Any], payload: PureAnalysisInput) -> dict[str, Any]:
    input_payload = {
        "name": payload.name or "命主",
        "gender": normalize_gender(payload.gender),
        "birthDateTime": payload.birth_dt.strftime("%Y-%m-%d %H:%M:%S"),
        "birthPlace": _public_place(payload.birth_place),
        "longitude": payload.longitude,
        "latitude": payload.latitude,
        "useTrueSolarTime": payload.use_true_solar_time,
    }

    return {
        "capabilityId": "ziwei",
        "input": input_payload,
        "inputTrace": raw.get("inputTrace", {}),
        "birthInfo": raw.get("birthInfo", {}),
        "ziweiChart": raw.get("ziweiChart", {}),
        "palaceAnalysis": raw.get("palaceAnalysis", {}),
        "fiveElementsClass": raw.get("fiveElementsClass", ""),
        "starInfluence": raw.get("starInfluence", {}),
        "starPositions": raw.get("starPositions", []),
        "ziweiHoroscope": raw.get("ziweiHoroscope", {}),
        "meta": {
            "birthPlaceDisplay": _public_place(payload.birth_place),
            "source": "BaziCalculator true-solar pipeline + fortel/iztro",
            "legacyZiweiBasic": "disabled",
        },
    }


def _build_evidence(data: dict[str, Any]) -> dict[str, Any]:
    return {
        "schemaVersion": 1,
        "capabilityId": "ziwei",
        "source": "iztro",
        "items": {
            "ziweiChart": {
                "source": "fortel_ziwei_integration -> iztro",
                "ruleIds": ["ziwei.iztro_chart", "ziwei.palace_metadata", "ziwei.decadal_ranges"],
                "basis": ["ziweiChart", "palaceAnalysis", "starPositions", "fiveElementsClass"],
                "risk": "folk_reference",
            },
            "horoscope": {
                "source": "iztro horoscope",
                "ruleIds": ["ziwei.horoscope_cycles", "ziwei.mutagen_scope"],
                "basis": ["ziweiHoroscope"],
                "risk": "folk_reference",
            },
            "timePipeline": {
                "source": "BaziCalculator true-solar pipeline",
                "ruleIds": ["bazi.true_solar_time_pipeline", "ziwei.time_index"],
                "basis": ["inputTrace.originalTime", "inputTrace.trueSolarTime", "inputTrace.timeZhi"],
                "risk": "calendar_boundary",
            },
        },
        "coverage": {
            "hasChart": bool(data.get("ziweiChart")),
            "hasHoroscope": bool(data.get("ziweiHoroscope")),
            "palaceCount": len(data.get("palaceAnalysis", [])) if isinstance(data.get("palaceAnalysis"), list) else 0,
            "starPositionCount": len(data.get("starPositions", []))
            if isinstance(data.get("starPositions"), list)
            else 0,
            "hasInputTrace": bool(data.get("inputTrace")),
        },
    }


def calculate_ziwei(payload: PureAnalysisInput) -> dict[str, Any]:
    """计算紫微斗数独立 capability。"""
    adapter_payload = ZiweiIztroInput(
        birth_dt=payload.birth_dt,
        gender=normalize_gender(payload.gender),
        longitude=payload.longitude,
        latitude=payload.latitude,
        name=payload.name,
        birth_place=_public_place(payload.birth_place),
        use_true_solar_time=payload.use_true_solar_time,
    )
    raw = calculate_ziwei_iztro(adapter_payload)
    data = _select_ziwei_payload(raw, payload)
    data["analysisEvidence"] = _build_evidence(data)
    return data
