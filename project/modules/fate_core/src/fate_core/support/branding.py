from __future__ import annotations

import json
from functools import lru_cache
from typing import Any

from .paths import FATE_REPO_ROOT

BRANDING_CONFIG_PATH = FATE_REPO_ROOT / "assets" / "config" / "branding.json"
REQUIRED_BRANDING_KEYS = (
    "name",
    "heroTitle",
    "sponsorText",
    "tagline",
    "tradecatRepo",
    "fatecatRepo",
    "ca",
    "disclaimerTitle",
    "disclaimerText",
    "cliBanner",
    "telegramFooter",
    "reportFooterTitle",
)


@lru_cache(maxsize=1)
def load_branding() -> dict[str, str]:
    """加载统一品牌与免责声明配置。"""
    if not BRANDING_CONFIG_PATH.exists():
        raise FileNotFoundError(f"品牌配置不存在: {BRANDING_CONFIG_PATH}")

    raw = json.loads(BRANDING_CONFIG_PATH.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise RuntimeError("品牌配置格式错误：必须是 JSON 对象")

    missing = [key for key in REQUIRED_BRANDING_KEYS if not raw.get(key)]
    if missing:
        raise RuntimeError(f"品牌配置缺少字段: {', '.join(missing)}")

    return {key: str(raw[key]).strip() for key in REQUIRED_BRANDING_KEYS}


def get_branding_payload() -> dict[str, str]:
    """返回适合 JSON/API/Agent 结果的结构化品牌字段。"""
    branding = load_branding()
    return {
        "name": branding["name"],
        "heroTitle": branding["heroTitle"],
        "sponsorText": branding["sponsorText"],
        "tagline": branding["tagline"],
        "tradecatRepo": branding["tradecatRepo"],
        "fatecatRepo": branding["fatecatRepo"],
        "ca": branding["ca"],
    }


def get_disclaimer_payload() -> str:
    """返回统一免责声明正文。"""
    return load_branding()["disclaimerText"]


def build_disclaimer_text() -> str:
    """构造纯文本免责声明。"""
    branding = load_branding()
    return "\n".join([branding["disclaimerTitle"], branding["disclaimerText"]])


def build_disclaimer_markdown() -> str:
    """构造 Markdown 免责声明。"""
    branding = load_branding()
    return "\n".join([f"**{branding['disclaimerTitle']}**", branding["disclaimerText"]])


def attach_branding(payload: dict[str, Any]) -> dict[str, Any]:
    """给结构化输出附加免责声明与品牌信息。"""
    enriched: dict[str, Any] = {"disclaimer": get_disclaimer_payload()}
    enriched.update(payload)
    enriched["branding"] = get_branding_payload()
    return enriched


def build_brand_footer_text(*, compact: bool = False) -> str:
    """构造纯文本品牌尾注。"""
    branding = load_branding()
    if compact:
        return "\n".join(
            [
                f"赞助支持：{branding['name']}",
                branding["cliBanner"],
                f"TradeCat Repo: {branding['tradecatRepo']}",
                f"CA: {branding['ca']}",
            ]
        )

    return "\n".join(
        [
            branding["heroTitle"],
            branding["sponsorText"],
            branding["tagline"],
            f"TradeCat Repo: {branding['tradecatRepo']}",
            f"FateCat Repo: {branding['fatecatRepo']}",
            f"CA: {branding['ca']}",
        ]
    )


def build_brand_footer_markdown(*, compact: bool = False) -> str:
    """构造 Markdown 友好的品牌尾注。"""
    branding = load_branding()
    if compact:
        return "\n".join(
            [
                f"*赞助支持：{branding['name']}*",
                branding["cliBanner"],
                f"TradeCat Repo: {branding['tradecatRepo']}",
                f"CA: `{branding['ca']}`",
            ]
        )

    return "\n".join(
        [
            f"*{branding['heroTitle']}*",
            branding["sponsorText"],
            branding["tagline"],
            f"TradeCat Repo: {branding['tradecatRepo']}",
            f"FateCat Repo: {branding['fatecatRepo']}",
            f"CA: `{branding['ca']}`",
        ]
    )


def build_branding_text(*, compact: bool = False) -> str:
    """构造启动界面文案，免责声明始终置顶。"""
    return f"{build_disclaimer_text()}\n\n{build_brand_footer_text(compact=compact)}"


def build_branding_markdown(*, compact: bool = False) -> str:
    """构造 Markdown 启动界面文案，免责声明始终置顶。"""
    return f"{build_disclaimer_markdown()}\n\n{build_brand_footer_markdown(compact=compact)}"


def append_branding_text(text: str, *, compact: bool = False) -> str:
    """在纯文本结果顶部加免责声明，尾部追加品牌文案。"""
    body = text.rstrip()
    return f"{build_disclaimer_text()}\n\n{body}\n\n——\n{build_brand_footer_text(compact=compact)}"


def append_branding_markdown(text: str, *, compact: bool = False) -> str:
    """在 Markdown 结果顶部加免责声明，尾部追加品牌文案。"""
    body = text.rstrip()
    return f"{build_disclaimer_markdown()}\n\n{body}\n\n——\n{build_brand_footer_markdown(compact=compact)}"
