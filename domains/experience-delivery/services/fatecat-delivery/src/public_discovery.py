"""公开站点的机器发现与实体描述。"""

from __future__ import annotations

import json
import os
from html import escape
from typing import Any
from urllib.parse import urlsplit

DEFAULT_PUBLIC_BASE_URL = "https://tradecatlabs-fatecat.hf.space"
DISCOVERY_UPDATED_ON = "2026-07-13"

PUBLIC_FAQS: tuple[tuple[str, str], ...] = (
    (
        "FateCat 是什么？",
        "FateCat 是 TradeCat Labs 面向 Agent 与应用开发者的测算基础设施，负责统一能力协议、结构化计算、证据字段、报告和多端交付。",
    ),
    (
        "FateCat 当前公开支持哪些报告？",
        "公开 Web 工作台当前支持综合八字和紫微斗数两种独立 Markdown 报告；每次请求只选择一个体系。",
    ),
    (
        "FateCat 是否使用 AI 直接计算命盘？",
        "生产路径先由结构化 capability provider 完成计算；AI 是可选解释层，不应根据自然语言自行重算盘面。",
    ),
    (
        "production capability 表示科学预测有效吗？",
        "不表示。production 只表示仓库内存在可执行 provider、契约和质量门禁，不代表传统命理具备科学预测效力。",
    ),
    (
        "Agent 应该如何接入 FateCat？",
        "先读取 capability 注册表和 OpenAPI，只调用状态为 production 的能力，并保留响应中的 evidence 与风险字段。",
    ),
    (
        "FateCat 会把出生资料自动发送给 Gemini 吗？",
        "不会。公开 Web 不会自动把输入或报告发送给 Gemini；用户只能自行复制 Markdown 到外部服务。",
    ),
)


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


def schema_org_graph() -> dict[str, Any]:
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


def about_schema_org_graph() -> dict[str, Any]:
    """构建与公开说明页可见正文一致的文章和问答实体。"""
    base = public_base_url()
    graph = list(schema_org_graph()["@graph"])
    graph.extend(
        [
            {
                "@type": "TechArticle",
                "@id": f"{base}/about#article",
                "headline": "FateCat 测算基础设施：能力、证据与接入说明",
                "description": "FateCat 的项目定位、当前能力、计算与解释边界、证据来源、Agent 接入方式和风险说明。",
                "mainEntityOfPage": f"{base}/about",
                "author": {"@id": f"{base}/#organization"},
                "publisher": {"@id": f"{base}/#organization"},
                "about": {"@id": f"{base}/#software"},
                "datePublished": DISCOVERY_UPDATED_ON,
                "dateModified": DISCOVERY_UPDATED_ON,
                "inLanguage": "zh-CN",
            },
            {
                "@type": "FAQPage",
                "@id": f"{base}/about#faq",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": question,
                        "acceptedAnswer": {"@type": "Answer", "text": answer},
                    }
                    for question, answer in PUBLIC_FAQS
                ],
            },
        ]
    )
    return {"@context": "https://schema.org", "@graph": graph}


def _about_schema_org_json() -> str:
    return json.dumps(about_schema_org_graph(), ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


def render_about_html(capabilities: list[dict[str, Any]]) -> str:
    """生成可抓取、可引用且不依赖 JavaScript 的项目权威说明页。"""
    base = public_base_url()
    capability_rows = []
    for item in capabilities:
        maturity_value = item.get("maturity")
        maturity: dict[str, Any] = maturity_value if isinstance(maturity_value, dict) else {}
        surfaces_value = item.get("surfaces")
        surfaces: dict[str, Any] = surfaces_value if isinstance(surfaces_value, dict) else {}
        available_surfaces = [name for name, enabled in surfaces.items() if enabled]
        capability_rows.append(
            "<tr>"
            f"<td><code>{escape(str(item.get('capabilityId', '')))}</code></td>"
            f"<td>{escape(str(item.get('name', '')))}</td>"
            f"<td>{escape(str(item.get('status', '')))}</td>"
            f"<td>{escape(str(maturity.get('level', '')))}</td>"
            f"<td>{escape(', '.join(available_surfaces) or '仅登记')}</td>"
            "</tr>"
        )

    faq_html = "\n".join(
        f"<section><h3>{escape(question)}</h3><p>{escape(answer)}</p></section>" for question, answer in PUBLIC_FAQS
    )
    return "\n".join(
        [
            "<!doctype html>",
            '<html lang="zh-CN">',
            "<head>",
            '<meta charset="utf-8">',
            '<meta name="viewport" content="width=device-width, initial-scale=1">',
            '<meta name="description" content="FateCat 的项目定位、当前能力、证据来源、Agent 接入方式和风险边界。">',
            '<meta name="author" content="TradeCat Labs">',
            f'<meta name="date" content="{DISCOVERY_UPDATED_ON}">',
            '<meta name="robots" content="index,follow,max-snippet:-1">',
            f'<link rel="canonical" href="{escape(base + "/about", quote=True)}">',
            '<link rel="alternate" type="text/plain" href="/llms.txt" title="FateCat llms.txt">',
            '<script type="application/ld+json">' + _about_schema_org_json() + "</script>",
            "<title>FateCat 测算基础设施：能力、证据与接入说明</title>",
            "</head>",
            "<body>",
            '<header><nav aria-label="主要入口"><a href="/web">Web 工作台</a> | <a href="/docs">API 文档</a> | <a href="/llms.txt">llms.txt</a> | <a href="https://github.com/tradecatlabs/fatecat">GitHub</a></nav></header>',
            "<main><article>",
            "<h1>FateCat 测算基础设施：能力、证据与接入说明</h1>",
            "<p><strong>结论：</strong>FateCat 将结构化测算与可选 AI 解释分离，为 Agent 和应用提供统一 capability 契约、可复现计算、证据字段、Markdown 报告与多端接口。</p>",
            f'<p>发布者：TradeCat Labs（交易猫实验室）；最后审阅：<time datetime="{DISCOVERY_UPDATED_ON}">{DISCOVERY_UPDATED_ON}</time>。</p>',
            "<h2>项目事实</h2>",
            '<dl><dt>项目</dt><dd>FateCat</dd><dt>定位</dt><dd>面向 Agent 与应用开发者的测算基础设施</dd><dt>许可证</dt><dd>MIT</dd><dt>规范源码</dt><dd><a href="https://github.com/tradecatlabs/fatecat">tradecatlabs/fatecat</a></dd><dt>公开服务</dt><dd><a href="/web">FateCat Web</a></dd></dl>',
            "<h2>当前能力与可用面</h2>",
            "<p>下表由实时 capability 注册表生成。production 表示存在可执行 provider 与仓库门禁，不表示科学预测有效；planned 能力不可执行。</p>",
            '<table><caption>FateCat capability 生命周期与交付面</caption><thead><tr><th scope="col">能力 ID</th><th scope="col">名称</th><th scope="col">状态</th><th scope="col">成熟度</th><th scope="col">公开交付面</th></tr></thead><tbody>',
            *capability_rows,
            "</tbody></table>",
            '<p><a href="/api/v1/capabilities">查看实时 capability JSON</a>；<a href="/api/v1/providers">查看 provider JSON</a>。</p>',
            "<h2>计算、解释与证据边界</h2>",
            "<ol><li>服务端规范化出生时间、地区、时区和经纬度等输入。</li><li>状态为 production 的 provider 生成结构化计算结果。</li><li>FateCat 组织 evidence、风险字段和 Markdown 报告。</li><li>AI 或 Agent 可解释结果，但不应从自然语言重新计算命盘。</li></ol>",
            "<p>相同规范化输入和引擎版本应产生相同结构化计算结果。该工程可复现性不等于传统命理具备科学预测效力。</p>",
            "<h2>Agent 接入步骤</h2>",
            '<ol><li>读取 <a href="/api/v1/capabilities">capability 注册表</a>。</li><li>读取 <a href="/openapi.json">OpenAPI JSON</a> 或 <a href="/docs">交互式文档</a>。</li><li>只调用状态为 production 的能力，并提交契约要求的完整输入。</li><li>保留响应中的 evidence、engineVersion 和风险字段。</li><li>不得把 planned 能力、民俗解释或 AI 总结描述为科学事实。</li></ol>',
            "<h2>来源与复核入口</h2>",
            '<ul><li><a href="https://github.com/tradecatlabs/fatecat/blob/main/contracts/fate/capabilities/registry.json">Capability 契约</a></li><li><a href="https://github.com/tradecatlabs/fatecat/actions">GitHub Actions</a></li><li><a href="/llms.txt">AI / Agent 事实文档</a></li><li><a href="/sitemap.xml">站点地图</a></li><li><a href="https://github.com/tradecatlabs/fatecat/blob/main/LICENSE">MIT License</a></li></ul>',
            "<h2>常见问题</h2>",
            faq_html,
            "<h2>风险与隐私边界</h2>",
            "<p>传统命理输出仅供文化研究、算法测试和娱乐参考，不承诺确定未来，也不替代医疗、法律、金融或心理专业意见。公开 Web 默认不写用户记录数据库，但报告会回显用户提交的出生信息；不要提交不希望出现在报告中的敏感资料。</p>",
            "</article></main>",
            "</body>",
            "</html>",
        ]
    )


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
        ("/about", "weekly", "0.9"),
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
    "PUBLIC_FAQS",
    "about_schema_org_graph",
    "public_base_url",
    "render_about_html",
    "render_robots_txt",
    "render_sitemap_xml",
    "schema_org_graph",
    "schema_org_json",
]
