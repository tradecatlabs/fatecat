#!/usr/bin/env python3
"""审计 FateCat 公开站点的 GEO 机器发现链路。"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class FetchResult:
    url: str
    final_url: str
    status: int
    content_type: str
    location: str
    body: str


@dataclass(frozen=True)
class Check:
    check_id: str
    ok: bool
    evidence: str


class NoRedirectHandler(urllib.request.HTTPRedirectHandler):
    """保留重定向响应，便于验证永久跳转语义。"""

    def redirect_request(self, req, fp, code, msg, headers, newurl):  # noqa: ANN001, ANN201
        return None


def fetch(url: str, *, timeout: float, follow_redirects: bool = True) -> FetchResult:
    request = urllib.request.Request(
        url,
        headers={"Accept": "*/*", "User-Agent": "FateCat-GEO-Audit/1.0"},
    )
    try:
        opener = urllib.request.build_opener() if follow_redirects else urllib.request.build_opener(NoRedirectHandler())
        with opener.open(request, timeout=timeout) as response:
            body = response.read().decode("utf-8", errors="replace")
            return FetchResult(
                url=url,
                final_url=response.geturl(),
                status=response.status,
                content_type=response.headers.get("Content-Type", ""),
                location=response.headers.get("Location", ""),
                body=body,
            )
    except urllib.error.HTTPError as exc:
        return FetchResult(
            url=url,
            final_url=exc.geturl(),
            status=exc.code,
            content_type=exc.headers.get("Content-Type", ""),
            location=exc.headers.get("Location", ""),
            body=exc.read().decode("utf-8", errors="replace"),
        )
    except urllib.error.URLError as exc:
        return FetchResult(
            url=url,
            final_url=url,
            status=0,
            content_type="",
            location="",
            body=f"network_error:{type(exc.reason).__name__}",
        )


def contains(result: FetchResult, needle: str) -> bool:
    return needle in result.body


def run_audit(base_url: str, *, timeout: float) -> dict[str, Any]:
    base = base_url.rstrip("/")
    resources = {
        "root": fetch(base + "/", timeout=timeout, follow_redirects=False),
        "web": fetch(base + "/web", timeout=timeout),
        "about": fetch(base + "/about", timeout=timeout),
        "llms": fetch(base + "/llms.txt", timeout=timeout),
        "robots": fetch(base + "/robots.txt", timeout=timeout),
        "sitemap": fetch(base + "/sitemap.xml", timeout=timeout),
        "openapi": fetch(base + "/openapi.json", timeout=timeout),
        "docs": fetch(base + "/docs", timeout=timeout),
        "capabilities": fetch(base + "/api/v1/capabilities", timeout=timeout),
        "providers": fetch(base + "/api/v1/providers", timeout=timeout),
    }
    web = resources["web"]
    about = resources["about"]
    llms = resources["llms"]
    robots = resources["robots"]
    sitemap = resources["sitemap"]
    checks = [
        Check("root.permanent_redirect", resources["root"].status == 308, f"status={resources['root'].status}"),
        Check(
            "root.redirects_to_web",
            resources["root"].location == "/web",
            resources["root"].location,
        ),
        Check("web.http_200", web.status == 200, f"status={web.status}"),
        Check("web.html", "text/html" in web.content_type, web.content_type),
        Check("web.canonical", contains(web, f'<link rel="canonical" href="{base}/web">'), f"canonical={base}/web"),
        Check("web.description", contains(web, '<meta name="description"'), "meta description"),
        Check("web.author", contains(web, '<meta name="author" content="TradeCat Labs">'), "TradeCat Labs"),
        Check("web.llms_link", contains(web, 'href="/llms.txt"'), "/llms.txt"),
        Check("web.sitemap_link", contains(web, 'href="/sitemap.xml"'), "/sitemap.xml"),
        Check("web.json_ld", contains(web, 'type="application/ld+json"'), "Schema.org JSON-LD"),
        Check("web.about_link", contains(web, 'href="/about"'), "/about"),
        Check("about.http_200", about.status == 200, f"status={about.status}"),
        Check("about.html", "text/html" in about.content_type, about.content_type),
        Check(
            "about.canonical",
            contains(about, f'<link rel="canonical" href="{base}/about">'),
            f"canonical={base}/about",
        ),
        Check("about.article", contains(about, "<main><article>"), "semantic main/article"),
        Check("about.summary", contains(about, "<strong>结论：</strong>"), "answer-first summary"),
        Check("about.capability_table", contains(about, "FateCat capability 生命周期与交付面"), "capability table"),
        Check("about.sources", contains(about, "来源与复核入口"), "source ledger"),
        Check("about.faq", contains(about, "<h2>常见问题</h2>"), "visible FAQ"),
        Check("about.risk", contains(about, "风险与隐私边界"), "risk boundary"),
        Check("robots.http_200", robots.status == 200, f"status={robots.status}"),
        Check("robots.default_agent", contains(robots, "User-agent: *"), "User-agent: *"),
        Check("robots.sitemap", contains(robots, f"Sitemap: {base}/sitemap.xml"), f"{base}/sitemap.xml"),
        Check("sitemap.http_200", sitemap.status == 200, f"status={sitemap.status}"),
        Check("sitemap.xml", "application/xml" in sitemap.content_type, sitemap.content_type),
        Check("sitemap.web", contains(sitemap, f"<loc>{base}/web</loc>"), f"{base}/web"),
        Check("sitemap.about", contains(sitemap, f"<loc>{base}/about</loc>"), f"{base}/about"),
        Check("sitemap.llms", contains(sitemap, f"<loc>{base}/llms.txt</loc>"), f"{base}/llms.txt"),
        Check("llms.http_200", llms.status == 200, f"status={llms.status}"),
        Check("llms.plain_text", "text/plain" in llms.content_type, llms.content_type),
        Check("llms.identity", contains(llms, "## Canonical Identity"), "Canonical Identity"),
        Check("llms.availability", contains(llms, "## Availability Matrix"), "Availability Matrix"),
        Check("llms.sources", contains(llms, "Canonical evidence sources"), "evidence sources"),
        Check("llms.questions", contains(llms, "## High-Intent Questions and Answers"), "high-intent Q&A"),
        Check("llms.citation", contains(llms, "## Citation Guidance"), "citation guidance"),
        Check("llms.risk", contains(llms, "## Storage, Privacy, and Risk"), "risk boundary"),
        Check("openapi.http_200", resources["openapi"].status == 200, f"status={resources['openapi'].status}"),
        Check("docs.http_200", resources["docs"].status == 200, f"status={resources['docs'].status}"),
        Check(
            "capabilities.http_200",
            resources["capabilities"].status == 200,
            f"status={resources['capabilities'].status}",
        ),
        Check("providers.http_200", resources["providers"].status == 200, f"status={resources['providers'].status}"),
    ]

    try:
        ET.fromstring(sitemap.body)
    except ET.ParseError as exc:
        checks.append(Check("sitemap.parseable", False, str(exc)))
    else:
        checks.append(Check("sitemap.parseable", True, "valid XML"))

    try:
        capability_payload = json.loads(resources["capabilities"].body)
        capability_items = capability_payload["data"]["capabilities"]
        status_by_id = {item["capabilityId"]: item["status"] for item in capability_items}
    except (json.JSONDecodeError, KeyError, TypeError) as exc:
        checks.append(Check("capabilities.lifecycle_parseable", False, type(exc).__name__))
    else:
        production_ids = {capability_id for capability_id, status in status_by_id.items() if status == "production"}
        planned_ids = {capability_id for capability_id, status in status_by_id.items() if status == "planned"}
        checks.append(
            Check(
                "capabilities.production_set",
                production_ids == {"bazi", "ziwei", "almanac", "meihua"},
                ",".join(sorted(production_ids)),
            )
        )
        checks.append(
            Check(
                "capabilities.planned_set",
                planned_ids == {"liuyao", "qimen", "daliuren", "fengshui_nine_stars", "name_marriage"},
                ",".join(sorted(planned_ids)),
            )
        )

    json_ld_match = re.search(r'<script type="application/ld\+json">(.*?)</script>', web.body, flags=re.DOTALL)
    try:
        json_ld = json.loads(json_ld_match.group(1)) if json_ld_match else None
    except json.JSONDecodeError as exc:
        checks.append(Check("web.json_ld_parseable", False, str(exc)))
    else:
        graph_types = {item.get("@type") for item in (json_ld or {}).get("@graph", []) if isinstance(item, dict)}
        required_types = {"Organization", "SoftwareApplication", "WebSite", "WebApplication"}
        checks.append(Check("web.json_ld_parseable", required_types <= graph_types, ",".join(sorted(graph_types))))

    about_json_ld_match = re.search(r'<script type="application/ld\+json">(.*?)</script>', about.body, flags=re.DOTALL)
    try:
        about_json_ld = json.loads(about_json_ld_match.group(1)) if about_json_ld_match else None
    except json.JSONDecodeError as exc:
        checks.append(Check("about.json_ld_parseable", False, str(exc)))
    else:
        about_graph = (about_json_ld or {}).get("@graph", [])
        about_types = {item.get("@type") for item in about_graph if isinstance(item, dict)}
        faq_value = next(
            (
                item.get("mainEntity", [])
                for item in about_graph
                if isinstance(item, dict) and item.get("@type") == "FAQPage"
            ),
            [],
        )
        faq_items = faq_value if isinstance(faq_value, list) else []
        checks.append(
            Check(
                "about.json_ld_parseable",
                {"TechArticle", "FAQPage"} <= about_types,
                ",".join(sorted(about_types)),
            )
        )
        visible_faq_count = about.body.count("<section><h3>")
        checks.append(
            Check(
                "about.faq_schema_alignment",
                visible_faq_count >= 5 and len(faq_items) == visible_faq_count,
                f"visible={visible_faq_count},schema={len(faq_items)}",
            )
        )

    passed = sum(check.ok for check in checks)
    failed = len(checks) - passed
    return {
        "schemaVersion": 1,
        "kind": "fatecat.geo_discovery_audit",
        "baseUrl": base,
        "status": "passed" if failed == 0 else "failed",
        "score": round(passed * 100 / len(checks), 2),
        "summary": {"checks": len(checks), "passed": passed, "failed": failed},
        "checks": [asdict(check) for check in checks],
        "resources": {name: asdict(result) | {"body": "<omitted>"} for name, result in resources.items()},
        "externalMetrics": {
            "aiCrawlerSuccessRate": "requires edge/access logs",
            "indexCoverage": "requires search-console ownership",
            "brandMentionRate": "requires repeated AI-platform sampling",
            "answerCitationRate": "requires repeated AI-platform sampling",
            "recommendationExposure": "requires repeated AI-platform sampling",
            "organicTraffic": "requires analytics access",
            "effectiveVisitsAndConversion": "requires consented analytics and conversion events",
        },
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", required=True, help="待审计公开服务基址")
    parser.add_argument("--output-json", help="可选 JSON 输出路径")
    parser.add_argument("--timeout", type=float, default=30.0, help="单请求超时秒数")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = run_audit(args.base_url, timeout=args.timeout)
    serialized = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output_json:
        output = Path(args.output_json)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(serialized, encoding="utf-8")
    print(serialized, end="")
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    sys.exit(main())
