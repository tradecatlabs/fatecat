"""公开站点的机器发现与实体描述。"""

from __future__ import annotations

import json
import os
from html import escape
from urllib.parse import urlsplit

DEFAULT_PUBLIC_BASE_URL = "https://tradecatlabs-fatecat.hf.space"
DISCOVERY_UPDATED_ON = "2026-07-13"


def public_base_url() -> str:
    """返回不含路径的公开规范基址。"""
    raw = os.getenv("FATE_PUBLIC_BASE_URL", DEFAULT_PUBLIC_BASE_URL).strip().rstrip("/")
    parsed = urlsplit(raw)
    if (
        parsed.scheme not in {"http", "https"}
        or not parsed.netloc
        or parsed.path
        or parsed.query
        or parsed.fragment
        or parsed.username
        or parsed.password
    ):
        raise ValueError("FATE_PUBLIC_BASE_URL 必须是仅含 scheme 与 host 的 HTTP(S) 地址")
    return raw


def schema_org_graph() -> dict[str, object]:
    """构建仅包含已验证公开事实的 Schema.org 实体图。"""
    base = public_base_url()
    organization_id = f"{base}/#organization"
    software_id = f"{base}/#software"
    return {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Organization",
                "@id": organization_id,
                "name": "TradeCat Labs",
                "alternateName": "交易猫实验室",
                "url": "https://github.com/tradecatlabs",
                "sameAs": [
                    "https://github.com/tradecatlabs",
                    "https://huggingface.co/tradecatlabs",
                    "https://x.com/tradecatlabs",
                ],
            },
            {
                "@type": "SoftwareApplication",
                "@id": software_id,
                "name": "FateCat",
                "alternateName": "FateCat 测算基础设施",
                "description": "面向 Agent 与应用开发者的测算基础设施，提供统一能力协议、可复现计算核心、证据化解释层和多端交付接口。",
                "applicationCategory": "DeveloperApplication",
                "operatingSystem": "Web, Linux",
                "url": f"{base}/web",
                "codeRepository": "https://github.com/tradecatlabs/fatecat",
                "license": "https://github.com/tradecatlabs/fatecat/blob/main/LICENSE",
                "provider": {"@id": organization_id},
                "isAccessibleForFree": True,
                "dateModified": DISCOVERY_UPDATED_ON,
                "featureList": [
                    "综合八字结构化计算与 Markdown 报告",
                    "紫微斗数结构化计算与 Markdown 报告",
                    "统一 capability 与 evidence 契约",
                    "FastAPI、Web、Telegram、CLI 与 Agent 交付接口",
                ],
            },
            {
                "@type": "WebSite",
                "@id": f"{base}/#website",
                "name": "FateCat",
                "url": base,
                "inLanguage": ["zh-CN", "en"],
                "publisher": {"@id": organization_id},
                "about": {"@id": software_id},
                "dateModified": DISCOVERY_UPDATED_ON,
            },
            {
                "@type": "WebApplication",
                "@id": f"{base}/web#application",
                "name": "FateCat Web Markdown 报告",
                "url": f"{base}/web",
                "applicationCategory": "UtilitiesApplication",
                "browserRequirements": "Requires a modern browser; core form has a server-side fallback.",
                "isAccessibleForFree": True,
                "provider": {"@id": organization_id},
                "about": {"@id": software_id},
                "dateModified": DISCOVERY_UPDATED_ON,
            },
        ],
    }


def schema_org_json() -> str:
    """序列化 JSON-LD，并防止内容提前结束 script 标签。"""
    return json.dumps(schema_org_graph(), ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


def render_robots_txt() -> str:
    """生成公开抓取策略。"""
    base = public_base_url()
    return "\n".join(
        [
            "User-agent: *",
            "Allow: /",
            "Disallow: /metrics",
            "Disallow: /api/v1/report/jobs",
            "Disallow: /api/v1/integrations",
            f"Sitemap: {base}/sitemap.xml",
            "",
        ]
    )


def render_sitemap_xml() -> str:
    """生成公开、稳定、可安全索引的站点地图。"""
    base = public_base_url()
    paths = (
        ("/web", "daily", "1.0"),
        ("/llms.txt", "weekly", "0.9"),
        ("/docs", "weekly", "0.8"),
        ("/openapi.json", "weekly", "0.8"),
        ("/api/v1/capabilities", "weekly", "0.8"),
        ("/api/v1/providers", "weekly", "0.7"),
        ("/api/v1/report/systems", "weekly", "0.7"),
    )
    entries = []
    for path, frequency, priority in paths:
        entries.append(
            "<url>"
            f"<loc>{escape(base + path)}</loc>"
            f"<lastmod>{DISCOVERY_UPDATED_ON}</lastmod>"
            f"<changefreq>{frequency}</changefreq>"
            f"<priority>{priority}</priority>"
            "</url>"
        )
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(entries) + "\n</urlset>\n"
    )


__all__ = [
    "DISCOVERY_UPDATED_ON",
    "public_base_url",
    "render_robots_txt",
    "render_sitemap_xml",
    "schema_org_graph",
    "schema_org_json",
]
