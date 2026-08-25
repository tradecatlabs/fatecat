"""公开站点的机器发现与实体描述。"""

from __future__ import annotations

import json
import os
from functools import cache
from html import escape
from typing import Any
from urllib.parse import urlsplit

from latex2mathml.converter import convert as latex_to_mathml
from markdown_it import MarkdownIt
from mdit_py_plugins.texmath import texmath_plugin

from _paths import REPO_ROOT

DEFAULT_PUBLIC_BASE_URL = "https://tradecatlabs-fatecat.hf.space"
DISCOVERY_UPDATED_ON = "2026-08-26"
ABOUT_PUBLISHED_ON = "2026-07-13"
BAZI_FORMALIZATION_PUBLISHED_ON = "2026-08-25"
BAZI_FORMALIZATION_BASE_PATH = "/articles/bazi-mathematical-formalization"

_BAZI_FORMALIZATION_SOURCE_DIR = (
    REPO_ROOT / "docs" / "reference-materials" / "reference" / "bazi-mathematical-formalization"
)
_BAZI_FORMALIZATION_SOURCE_URL = (
    "https://github.com/tradecatlabs/fatecat/blob/main/"
    "docs/reference-materials/reference/bazi-mathematical-formalization"
)
BAZI_FORMALIZATION_DOCUMENTS: dict[str, dict[str, str]] = {
    "overview": {
        "filename": "README.md",
        "title": "八字数学形式化文档集",
        "description": "FateCat 八字数学形式化的范围、真相源边界、分层模型、里程碑与完成定义。",
    },
    "formal-spec": {
        "filename": "FORMAL_SPEC.md",
        "title": "八字数学基础规范 v0.1",
        "description": "八字输入空间、历法与四柱、有限派生结构、规则语义、证据图和证明义务的工作草案。",
    },
    "build": {
        "filename": "BUILD.md",
        "title": "八字数学形式化构建指南",
        "description": "从来源、规范、机器契约和实现到 fixture、门禁、证据与交付的构建顺序。",
    },
    "maintenance": {
        "filename": "MAINTENANCE.md",
        "title": "八字数学形式化维护指南",
        "description": "形式化资产的版本、变更分类、Profile、兼容、回归、依赖升级和争议处理规则。",
    },
}

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

PUBLIC_CAPABILITY_GUIDES: dict[str, dict[str, Any]] = {
    "bazi": {
        "summary": "FateCat 综合八字是独立的 L4 production capability，使用完整出生时间、性别和地点坐标生成结构化计算、证据字段与可复制 Markdown 报告。",
        "scope": (
            "综合八字主线，包括四柱、日主、五行、格局、用神、调候和干支关系。",
            "动态运势，包括大运、流年、流月和小运。",
            "神煞、干支取象和袁天罡称骨作为辅助或民俗附录，不替代核心格局与喜忌判断。",
        ),
        "boundaries": (
            "综合八字报告不混入紫微斗数、黄历择日、六爻、奇门或其他独立体系。",
            "出生时间是必填计算输入；FateCat 不猜测未知时辰，也不生成缺少核心字段的半完整报告。",
            "production 表示 provider、契约和仓库门禁可执行，不表示传统命理具备科学预测效力。",
        ),
        "faqs": (
            (
                "FateCat 综合八字需要哪些核心输入？",
                "核心输入是完整出生日期时间、性别、经度和纬度；姓名、出生地文本和真太阳时开关属于可选字段。",
            ),
            (
                "综合八字报告是否包含紫微斗数？",
                "不包含。综合八字和紫微斗数是两个独立 capability，每次 Web 请求只输出一个体系。",
            ),
            (
                "未知出生时辰能否直接生成完整综合八字报告？",
                "不能。出生日期时间是必填输入，FateCat 不默认猜测未知时辰。",
            ),
            (
                "综合八字结论如何追溯？",
                "能力契约要求保留来源、依据、规则 ID、权重和风险字段，并要求计算轨迹可审计。",
            ),
        ),
    },
    "ziwei": {
        "summary": "FateCat 紫微斗数是独立的 L4 production capability，生成命盘、十二宫、命身宫、三方四正、四化与运限结构，并以独立 Markdown 报告交付。",
        "scope": (
            "紫微斗数命盘、十二宫、命宫与身宫结构。",
            "三方四正、四化落宫以及大限、流年、流月等运限信息。",
            "结构化计算结果、证据字段和独立可复制 Markdown 报告。",
        ),
        "boundaries": (
            "紫微斗数不作为综合八字的附属章节，也不混入默认综合八字报告。",
            "出生时间、性别和地点坐标是必填计算输入；FateCat 不猜测未知时辰。",
            "production 表示 provider、契约和仓库门禁可执行，不表示传统命理具备科学预测效力。",
        ),
        "faqs": (
            (
                "FateCat 紫微斗数需要哪些核心输入？",
                "核心输入是完整出生日期时间、性别、经度和纬度；姓名、出生地文本和真太阳时开关属于可选字段。",
            ),
            (
                "紫微斗数与综合八字是否独立？",
                "是。两者使用独立 capability 和报告 profile，每次 Web 请求只选择并输出一个体系。",
            ),
            (
                "紫微斗数当前覆盖哪些结构？",
                "当前契约覆盖命盘、十二宫、命身宫、三方四正、四化落宫与运限四化，并继续通过规则和 golden 回归加固深度。",
            ),
            (
                "紫微斗数结论如何追溯？",
                "能力契约要求保留来源、依据、规则 ID 和风险字段，并要求计算轨迹可审计。",
            ),
        ),
    },
}


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
                "datePublished": ABOUT_PUBLISHED_ON,
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


def capability_guide_schema_org_graph(capability: dict[str, Any]) -> dict[str, Any]:
    """构建与能力说明页正文一致的实体、文章、面包屑和问答。"""
    capability_id = str(capability.get("capabilityId", ""))
    guide = PUBLIC_CAPABILITY_GUIDES.get(capability_id)
    if guide is None:
        raise ValueError(f"未登记公开能力说明: {capability_id}")
    base = public_base_url()
    guide_url = f"{base}/guides/{capability_id}"
    graph = list(schema_org_graph()["@graph"])
    graph.extend(
        [
            {
                "@type": "DefinedTerm",
                "@id": f"{guide_url}#capability",
                "name": str(capability.get("name", "")),
                "termCode": capability_id,
                "description": str(capability.get("description", "")),
                "url": guide_url,
                "inDefinedTermSet": {
                    "@type": "DefinedTermSet",
                    "name": "FateCat capability registry",
                    "url": f"{base}/api/v1/capabilities",
                },
            },
            {
                "@type": "TechArticle",
                "@id": f"{guide_url}#article",
                "headline": f"FateCat {capability.get('name', '')}能力说明",
                "description": str(guide["summary"]),
                "mainEntityOfPage": guide_url,
                "author": {"@id": f"{base}/#organization"},
                "publisher": {"@id": f"{base}/#organization"},
                "about": {"@id": f"{guide_url}#capability"},
                "datePublished": DISCOVERY_UPDATED_ON,
                "dateModified": DISCOVERY_UPDATED_ON,
                "inLanguage": "zh-CN",
            },
            {
                "@type": "BreadcrumbList",
                "@id": f"{guide_url}#breadcrumb",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "FateCat", "item": f"{base}/about"},
                    {
                        "@type": "ListItem",
                        "position": 2,
                        "name": str(capability.get("name", "")),
                        "item": guide_url,
                    },
                ],
            },
            {
                "@type": "FAQPage",
                "@id": f"{guide_url}#faq",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": question,
                        "acceptedAnswer": {"@type": "Answer", "text": answer},
                    }
                    for question, answer in guide["faqs"]
                ],
            },
        ]
    )
    return {"@context": "https://schema.org", "@graph": graph}


def _capability_guide_schema_org_json(capability: dict[str, Any]) -> str:
    return json.dumps(
        capability_guide_schema_org_graph(capability),
        ensure_ascii=False,
        separators=(",", ":"),
    ).replace("</", "<\\/")


def _rewrite_bazi_formalization_links(tokens: list[Any]) -> None:
    """把内部链接改写为稳定路由，并移除渲染器生成的视觉属性。"""
    routes = {
        metadata["filename"]: (
            BAZI_FORMALIZATION_BASE_PATH
            if document_id == "overview"
            else f"{BAZI_FORMALIZATION_BASE_PATH}/{document_id}"
        )
        for document_id, metadata in BAZI_FORMALIZATION_DOCUMENTS.items()
    }
    routes["AGENTS.md"] = f"{_BAZI_FORMALIZATION_SOURCE_URL}/AGENTS.md"
    for token in tokens:
        if token.attrs:
            token.attrs.pop("class", None)
            token.attrs.pop("style", None)
        if token.type == "link_open":
            href = token.attrGet("href") or ""
            path, marker, fragment = href.partition("#")
            if path in routes:
                suffix = f"#{fragment}" if marker else ""
                token.attrSet("href", routes[path] + suffix)
        if token.children:
            _rewrite_bazi_formalization_links(token.children)


def _render_inline_math(tokens: list[Any], idx: int, _options: dict[str, Any], _env: dict[str, Any]) -> str:
    """把行内 TeX 转换为浏览器原生 MathML。"""
    return latex_to_mathml(tokens[idx].content.strip(), display="inline")


def _render_block_math(tokens: list[Any], idx: int, _options: dict[str, Any], _env: dict[str, Any]) -> str:
    """把块级 TeX 转换为浏览器原生 MathML。"""
    return latex_to_mathml(tokens[idx].content.strip(), display="block") + "\n"


def _render_numbered_block_math(tokens: list[Any], idx: int, _options: dict[str, Any], _env: dict[str, Any]) -> str:
    """以无样式语义 HTML 保留带编号的块级公式。"""
    mathml = latex_to_mathml(tokens[idx].content.strip(), display="block")
    return f"<figure>{mathml}<figcaption>({escape(tokens[idx].info)})</figcaption></figure>\n"


@cache
def _render_bazi_formalization_body(document_id: str) -> str:
    """读取固定文章源并缓存无原始 HTML 的语义正文。"""
    metadata = BAZI_FORMALIZATION_DOCUMENTS.get(document_id)
    if metadata is None:
        raise ValueError(f"未登记的八字数学形式化文档: {document_id}")
    source = (_BAZI_FORMALIZATION_SOURCE_DIR / metadata["filename"]).read_text(encoding="utf-8")
    renderer = (
        MarkdownIt("commonmark", {"html": False, "linkify": False, "typographer": False})
        .enable("table")
        .use(texmath_plugin, delimiters="brackets")
    )
    renderer.renderer.rules["fence"] = lambda tokens, idx, _options, _env: (
        "<pre><code>" + escape(tokens[idx].content, quote=False) + "</code></pre>\n"
    )
    renderer.renderer.rules["math_inline"] = _render_inline_math
    renderer.renderer.rules["math_block"] = _render_block_math
    renderer.renderer.rules["math_block_eqno"] = _render_numbered_block_math
    tokens = renderer.parse(source)
    if len(tokens) >= 3 and tokens[0].type == "heading_open" and tokens[0].tag == "h1":
        del tokens[:3]
    _rewrite_bazi_formalization_links(tokens)
    return renderer.renderer.render(tokens, renderer.options, {})


def render_bazi_formalization_article_html(document_id: str = "overview") -> str:
    """把现有数学形式化文档渲染为无 CSS、无 JavaScript 的公开文章。"""
    metadata = BAZI_FORMALIZATION_DOCUMENTS.get(document_id)
    if metadata is None:
        raise ValueError(f"未登记的八字数学形式化文档: {document_id}")
    base = public_base_url()
    article_path = (
        BAZI_FORMALIZATION_BASE_PATH if document_id == "overview" else f"{BAZI_FORMALIZATION_BASE_PATH}/{document_id}"
    )
    document_links = "".join(
        "<li>"
        f'<a href="{escape(BAZI_FORMALIZATION_BASE_PATH if slug == "overview" else f"{BAZI_FORMALIZATION_BASE_PATH}/{slug}", quote=True)}">'
        f"{escape(item['title'])}</a>"
        "</li>"
        for slug, item in BAZI_FORMALIZATION_DOCUMENTS.items()
    )
    return "\n".join(
        [
            "<!doctype html>",
            '<html lang="zh-CN">',
            "<head>",
            '<meta charset="utf-8">',
            '<meta name="viewport" content="width=device-width, initial-scale=1">',
            f'<meta name="description" content="{escape(metadata["description"], quote=True)}">',
            '<meta name="author" content="TradeCat Labs">',
            f'<meta name="date" content="{BAZI_FORMALIZATION_PUBLISHED_ON}">',
            '<meta name="robots" content="index,follow,max-snippet:-1">',
            f'<link rel="canonical" href="{escape(base + article_path, quote=True)}">',
            f"<title>{escape(metadata['title'])}｜FateCat</title>",
            "</head>",
            "<body>",
            '<header><nav aria-label="主要入口"><a href="/web">Web 工作台</a> | <a href="/about">项目说明</a> | <a href="/guides/bazi">综合八字能力说明</a> | <a href="/llms.txt">llms.txt</a></nav></header>',
            "<main><article>",
            f"<h1>{escape(metadata['title'])}</h1>",
            '<p>状态：工作草案 v0.1；发布者：TradeCat Labs（交易猫实验室）；最近评审：<time datetime="2026-08-25">2026-08-25</time>。</p>',
            "<p><strong>边界：</strong>本文只描述形式化与软件可验证性，不证明传统命理具备现代科学意义上的因果性或预测效力。</p>",
            '<nav aria-label="八字数学形式化文档"><h2>文档目录</h2><ul>' + document_links + "</ul></nav>",
            _render_bazi_formalization_body(document_id),
            "</article></main>",
            "</body>",
            "</html>",
        ]
    )


def render_capability_guide_html(capability: dict[str, Any]) -> str:
    """生成不依赖 JavaScript 的旗舰 capability 权威说明页。"""
    capability_id = str(capability.get("capabilityId", ""))
    guide = PUBLIC_CAPABILITY_GUIDES.get(capability_id)
    if guide is None:
        raise ValueError(f"未登记公开能力说明: {capability_id}")
    base = public_base_url()
    name = str(capability.get("name", ""))
    maturity = capability.get("maturity") if isinstance(capability.get("maturity"), dict) else {}
    engine = capability.get("engine") if isinstance(capability.get("engine"), dict) else {}
    report = capability.get("report") if isinstance(capability.get("report"), dict) else {}
    evidence = capability.get("evidence") if isinstance(capability.get("evidence"), dict) else {}
    evidence_policy = capability.get("evidencePolicy") if isinstance(capability.get("evidencePolicy"), dict) else {}
    risk_policy = capability.get("riskPolicy") if isinstance(capability.get("riskPolicy"), dict) else {}

    def list_items(values: object) -> str:
        items = values if isinstance(values, (list, tuple)) else ()
        return "".join(f"<li><code>{escape(str(item))}</code></li>" for item in items)

    scope_html = "".join(f"<li>{escape(str(item))}</li>" for item in guide["scope"])
    boundary_html = "".join(f"<li>{escape(str(item))}</li>" for item in guide["boundaries"])
    faq_html = "\n".join(
        f"<section><h3>{escape(question)}</h3><p>{escape(answer)}</p></section>" for question, answer in guide["faqs"]
    )
    deterministic = "是" if engine.get("deterministic") is True else "否"
    return "\n".join(
        [
            "<!doctype html>",
            '<html lang="zh-CN">',
            "<head>",
            '<meta charset="utf-8">',
            '<meta name="viewport" content="width=device-width, initial-scale=1">',
            f'<meta name="description" content="{escape(str(guide["summary"]), quote=True)}">',
            '<meta name="author" content="TradeCat Labs">',
            f'<meta name="date" content="{DISCOVERY_UPDATED_ON}">',
            '<meta name="robots" content="index,follow,max-snippet:-1">',
            f'<link rel="canonical" href="{escape(base + "/guides/" + capability_id, quote=True)}">',
            '<link rel="alternate" type="text/plain" href="/llms.txt" title="FateCat llms.txt">',
            '<script type="application/ld+json">' + _capability_guide_schema_org_json(capability) + "</script>",
            f"<title>FateCat {escape(name)}能力说明</title>",
            "</head>",
            "<body>",
            '<header><nav aria-label="主要入口"><a href="/about">项目说明</a> | <a href="/web">Web 工作台</a> | <a href="/docs">API 文档</a> | <a href="/llms.txt">llms.txt</a> | <a href="https://github.com/tradecatlabs/fatecat">GitHub</a></nav></header>',
            "<main><article>",
            f"<h1>FateCat {escape(name)}能力说明</h1>",
            f"<p><strong>结论：</strong>{escape(str(guide['summary']))}</p>",
            f'<p>发布者：TradeCat Labs（交易猫实验室）；最后审阅：<time datetime="{DISCOVERY_UPDATED_ON}">{DISCOVERY_UPDATED_ON}</time>。</p>',
            "<h2>能力事实</h2>",
            "<dl>"
            f"<dt>能力 ID</dt><dd><code>{escape(capability_id)}</code></dd>"
            f"<dt>状态</dt><dd>{escape(str(capability.get('status', '')))}</dd>"
            f"<dt>成熟度</dt><dd>{escape(str(maturity.get('level', '')))}</dd>"
            f"<dt>引擎</dt><dd><code>{escape(str(engine.get('provider', '')))}</code></dd>"
            f"<dt>引擎版本</dt><dd><code>{escape(str(engine.get('engineVersion', '')))}</code></dd>"
            f"<dt>确定性计算</dt><dd>{deterministic}</dd>"
            f"<dt>报告 profile</dt><dd><code>{escape(str(report.get('profile', '')))}</code></dd>"
            "</dl>",
            "<h2>能力范围</h2>",
            f"<ul>{scope_html}</ul>",
            "<h2>输入契约</h2>",
            f"<h3>必填字段</h3><ul>{list_items(capability.get('inputRequired'))}</ul>",
            f"<h3>可选字段</h3><ul>{list_items(capability.get('inputOptional'))}</ul>",
            "<h2>证据与复现</h2>",
            f"<p>响应要求保留以下 evidence 字段：</p><ul>{list_items(evidence.get('fields'))}</ul>",
            "<dl>"
            f"<dt>规则 ID 必需</dt><dd>{'是' if evidence_policy.get('ruleIdRequired') else '否'}</dd>"
            f"<dt>来源必需</dt><dd>{'是' if evidence_policy.get('sourceRequired') else '否'}</dd>"
            f"<dt>计算轨迹必需</dt><dd>{'是' if evidence_policy.get('calculationTraceRequired') else '否'}</dd>"
            "</dl>",
            "<h2>边界与禁止声明</h2>",
            f"<ul>{boundary_html}</ul>",
            f"<p>风险等级：<code>{escape(str(risk_policy.get('riskLevel', '')))}</code>；禁止声明：</p>",
            f"<ul>{list_items(risk_policy.get('forbiddenClaims'))}</ul>",
            "<h2>接入方式</h2>",
            f'<ol><li>读取 <a href="/capabilities/{escape(capability_id, quote=True)}">capability JSON</a>。</li><li>按照 <a href="/openapi.json">OpenAPI</a> 提交完整输入。</li><li>通过 <code>POST /capabilities/{escape(capability_id)}/calculate</code> 执行。</li><li>保留返回的结构化结果、evidence、engineVersion 与风险字段。</li></ol>',
            "<h2>来源与复核入口</h2>",
            f'<ul><li><a href="/capabilities/{escape(capability_id, quote=True)}">实时 capability JSON</a></li><li><a href="https://github.com/tradecatlabs/fatecat/blob/main/contracts/fate/capabilities/registry.json">版本化 capability registry</a></li><li><a href="/openapi.json">OpenAPI JSON</a></li><li><a href="https://github.com/tradecatlabs/fatecat/actions">GitHub Actions</a></li></ul>',
            "<h2>常见问题</h2>",
            faq_html,
            "</article></main>",
            "</body>",
            "</html>",
        ]
    )


def render_about_html(capabilities: list[dict[str, Any]]) -> str:
    """生成可抓取、可引用且不依赖 JavaScript 的项目权威说明页。"""
    base = public_base_url()
    capability_rows = []
    for item in capabilities:
        capability_id = str(item.get("capabilityId", ""))
        maturity_value = item.get("maturity")
        maturity: dict[str, Any] = maturity_value if isinstance(maturity_value, dict) else {}
        surfaces_value = item.get("surfaces")
        surfaces: dict[str, Any] = surfaces_value if isinstance(surfaces_value, dict) else {}
        available_surfaces = [name for name, enabled in surfaces.items() if enabled]
        name = escape(str(item.get("name", "")))
        if capability_id in PUBLIC_CAPABILITY_GUIDES:
            name = f'<a href="/guides/{escape(capability_id, quote=True)}">{name}</a>'
        capability_rows.append(
            "<tr>"
            f"<td><code>{escape(capability_id)}</code></td>"
            f"<td>{name}</td>"
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
        ("/guides/bazi", "weekly", "0.9"),
        ("/guides/ziwei", "weekly", "0.9"),
        (BAZI_FORMALIZATION_BASE_PATH, "monthly", "0.8"),
        (f"{BAZI_FORMALIZATION_BASE_PATH}/formal-spec", "monthly", "0.7"),
        (f"{BAZI_FORMALIZATION_BASE_PATH}/build", "monthly", "0.7"),
        (f"{BAZI_FORMALIZATION_BASE_PATH}/maintenance", "monthly", "0.7"),
        ("/llms.txt", "weekly", "0.9"),
        ("/docs", "weekly", "0.8"),
        ("/openapi.json", "weekly", "0.8"),
        ("/api/v1/capabilities", "weekly", "0.8"),
        ("/api/v1/providers", "weekly", "0.7"),
        ("/api/v1/report/systems", "weekly", "0.7"),
        ("/api/v1/discovery/query-set", "weekly", "0.6"),
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
    "ABOUT_PUBLISHED_ON",
    "BAZI_FORMALIZATION_BASE_PATH",
    "BAZI_FORMALIZATION_DOCUMENTS",
    "BAZI_FORMALIZATION_PUBLISHED_ON",
    "DISCOVERY_UPDATED_ON",
    "PUBLIC_CAPABILITY_GUIDES",
    "PUBLIC_FAQS",
    "about_schema_org_graph",
    "capability_guide_schema_org_graph",
    "public_base_url",
    "render_about_html",
    "render_bazi_formalization_article_html",
    "render_capability_guide_html",
    "render_robots_txt",
    "render_sitemap_xml",
    "schema_org_graph",
    "schema_org_json",
]
