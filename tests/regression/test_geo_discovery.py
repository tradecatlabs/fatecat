from __future__ import annotations

import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[2]
DELIVERY_SRC = ROOT / "domains" / "experience-delivery" / "services" / "fatecat-delivery" / "src"
FATE_CORE_SRC = ROOT / "domains" / "fate-analysis" / "services" / "fate-core" / "src"

for source_root in (DELIVERY_SRC, FATE_CORE_SRC):
    if str(source_root) not in sys.path:
        sys.path.insert(0, str(source_root))

from main import app  # noqa: E402
from public_discovery import (  # noqa: E402
    PUBLIC_CAPABILITY_GUIDES,
    PUBLIC_FAQS,
    about_schema_org_graph,
    public_base_url,
    schema_org_graph,
)


def test_public_root_redirects_permanently_to_web():
    response = TestClient(app, follow_redirects=False).get("/")

    assert response.status_code == 308
    assert response.headers["location"] == "/web"


def test_robots_declares_public_crawl_policy_and_sitemap():
    response = TestClient(app).get("/robots.txt")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/plain")
    assert "User-agent: *" in response.text
    assert "Allow: /" in response.text
    assert "Disallow: /metrics" in response.text
    assert "Disallow: /api/v1/report/jobs" in response.text
    assert "Sitemap: https://tradecatlabs-fatecat.hf.space/sitemap.xml" in response.text


def test_sitemap_is_parseable_and_contains_canonical_resources():
    response = TestClient(app).get("/sitemap.xml")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/xml")
    root = ET.fromstring(response.text)
    namespace = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    urls = {node.text for node in root.findall("s:url/s:loc", namespace)}
    assert "https://tradecatlabs-fatecat.hf.space/web" in urls
    assert "https://tradecatlabs-fatecat.hf.space/about" in urls
    assert "https://tradecatlabs-fatecat.hf.space/guides/bazi" in urls
    assert "https://tradecatlabs-fatecat.hf.space/guides/ziwei" in urls
    assert "https://tradecatlabs-fatecat.hf.space/llms.txt" in urls
    assert "https://tradecatlabs-fatecat.hf.space/openapi.json" in urls
    assert "https://tradecatlabs-fatecat.hf.space/api/v1/capabilities" in urls
    assert "https://tradecatlabs-fatecat.hf.space/api/v1/discovery/query-set" in urls
    assert len(urls) == 11


def test_web_exposes_canonical_metadata_and_schema_org_graph():
    response = TestClient(app).get("/web")

    assert response.status_code == 200
    text = response.text
    assert '<link rel="canonical" href="https://tradecatlabs-fatecat.hf.space/web">' in text
    assert '<meta name="description"' in text
    assert '<meta name="author" content="TradeCat Labs">' in text
    assert '<link rel="sitemap" type="application/xml" href="/sitemap.xml"' in text
    match = re.search(r'<script type="application/ld\+json">(.*?)</script>', text)
    assert match
    payload = json.loads(match.group(1))
    graph_types = {item["@type"] for item in payload["@graph"]}
    assert graph_types == {"Organization", "SoftwareApplication", "WebSite", "WebApplication"}


def test_about_page_is_answer_first_traceable_and_schema_aligned():
    response = TestClient(app).get("/about")

    assert response.status_code == 200
    assert response.headers["cache-control"] == "public, max-age=300"
    assert '</llms.txt>; rel="alternate"; type="text/plain"' in response.headers["link"]
    text = response.text
    assert '<link rel="canonical" href="https://tradecatlabs-fatecat.hf.space/about">' in text
    assert "<main><article>" in text
    assert "<strong>结论：</strong>" in text
    assert "FateCat capability 生命周期与交付面" in text
    assert "来源与复核入口" in text
    assert "风险与隐私边界" in text
    for forbidden in ("<style", " style=", " class="):
        assert forbidden not in text
    assert text.count("<h3>") == len(PUBLIC_FAQS)
    for capability_id in ("bazi", "ziwei", "almanac", "meihua", "liuyao", "qimen"):
        assert f"<code>{capability_id}</code>" in text
    assert 'href="/guides/bazi"' in text
    assert 'href="/guides/ziwei"' in text

    match = re.search(r'<script type="application/ld\+json">(.*?)</script>', text)
    assert match
    payload = json.loads(match.group(1))
    by_type = {item["@type"]: item for item in payload["@graph"]}
    assert "TechArticle" in by_type
    assert "FAQPage" in by_type
    assert len(by_type["FAQPage"]["mainEntity"]) == len(PUBLIC_FAQS)
    visible_answers = {answer for _, answer in PUBLIC_FAQS}
    schema_answers = {item["acceptedAnswer"]["text"] for item in by_type["FAQPage"]["mainEntity"]}
    assert schema_answers == visible_answers


def test_about_schema_contains_current_article_and_faq_entities():
    payload = about_schema_org_graph()
    graph_types = {item["@type"] for item in payload["@graph"]}

    assert {"TechArticle", "FAQPage"} <= graph_types


def test_about_page_does_not_depend_on_provider_health_payload(monkeypatch):
    main_module = sys.modules["main"]

    def fail_if_called():
        raise AssertionError("公开说明页不得调用完整 provider health payload")

    monkeypatch.setattr(main_module, "_capabilities_payload", fail_if_called)
    response = TestClient(app).get("/about")

    assert response.status_code == 200
    assert "<code>bazi</code>" in response.text


def test_flagship_capability_guides_are_traceable_and_schema_aligned():
    client = TestClient(app)
    expected_engines = {"bazi": "fate-core-bazi-v1", "ziwei": "fate-core-ziwei-v1"}

    for capability_id, guide in PUBLIC_CAPABILITY_GUIDES.items():
        response = client.get(f"/guides/{capability_id}")
        assert response.status_code == 200
        assert response.headers["cache-control"] == "public, max-age=300"
        text = response.text
        canonical = f"https://tradecatlabs-fatecat.hf.space/guides/{capability_id}"
        assert f'<link rel="canonical" href="{canonical}">' in text
        assert "<main><article>" in text
        assert "<strong>结论：</strong>" in text
        assert "输入契约" in text
        assert "证据与复现" in text
        assert "边界与禁止声明" in text
        assert f"<code>{expected_engines[capability_id]}</code>" in text
        for field in ("birthDateTime", "longitude", "latitude"):
            assert field in text
        for forbidden in ("<style", " style=", " class="):
            assert forbidden not in text
        assert text.count("<section><h3>") == len(guide["faqs"])

        match = re.search(r'<script type="application/ld\+json">(.*?)</script>', text)
        assert match
        payload = json.loads(match.group(1))
        graph = payload["@graph"]
        graph_types = {item["@type"] for item in graph}
        assert {"TechArticle", "DefinedTerm", "BreadcrumbList", "FAQPage"} <= graph_types
        faq = next(item for item in graph if item["@type"] == "FAQPage")
        schema_answers = {item["acceptedAnswer"]["text"] for item in faq["mainEntity"]}
        assert schema_answers == {answer for _, answer in guide["faqs"]}


def test_only_l4_web_capabilities_have_public_guides():
    client = TestClient(app)

    for capability_id in ("almanac", "meihua", "liuyao", "qimen", "unknown"):
        assert client.get(f"/guides/{capability_id}").status_code == 404


def test_capability_guides_do_not_depend_on_provider_health(monkeypatch):
    main_module = sys.modules["main"]

    def fail_if_called(*args, **kwargs):  # noqa: ANN002, ANN003
        raise AssertionError("公开能力说明页不得调用 provider health")

    monkeypatch.setattr(main_module, "_capability_provider_payload", fail_if_called)
    response = TestClient(app).get("/guides/bazi")

    assert response.status_code == 200
    assert "fate-core-bazi-v1" in response.text


def test_geo_query_set_is_public_stable_and_contains_no_platform_results():
    response = TestClient(app).get("/api/v1/discovery/query-set")

    assert response.status_code == 200
    assert response.headers["cache-control"] == "public, max-age=300"
    payload = response.json()
    source = json.loads((ROOT / "contracts/fate/discovery/query-set.json").read_text(encoding="utf-8"))
    assert payload == source
    assert payload["samplingPolicy"]["resultState"] == "external_validation_pending"
    assert len(payload["prompts"]) == 12
    result_keys = {"answer", "answerText", "brandMentioned", "brandRecommended", "rank"}
    assert all(not (result_keys & set(prompt)) for prompt in payload["prompts"])


def test_public_base_url_accepts_self_hosting_and_rejects_paths(monkeypatch):
    monkeypatch.setenv("FATE_PUBLIC_BASE_URL", "http://127.0.0.1:8001/")
    assert public_base_url() == "http://127.0.0.1:8001"

    monkeypatch.setenv("FATE_PUBLIC_BASE_URL", "https://example.com/fatecat")
    try:
        public_base_url()
    except ValueError as exc:
        assert "scheme 与 host" in str(exc)
    else:
        raise AssertionError("带路径的公开基址必须被拒绝")

    for invalid in ("https://user@example.com", "https://example.com?source=test", "https://example.com#site"):
        monkeypatch.setenv("FATE_PUBLIC_BASE_URL", invalid)
        try:
            public_base_url()
        except ValueError:
            pass
        else:
            raise AssertionError(f"非法公开基址必须被拒绝: {invalid}")


def test_schema_org_graph_contains_only_current_public_identity():
    payload = schema_org_graph()
    by_type = {item["@type"]: item for item in payload["@graph"]}

    assert by_type["Organization"]["name"] == "TradeCat Labs"
    assert by_type["Organization"]["alternateName"] == "交易猫实验室"
    assert by_type["SoftwareApplication"]["name"] == "FateCat"
    assert by_type["SoftwareApplication"]["codeRepository"] == "https://github.com/tradecatlabs/fatecat"
    assert by_type["SoftwareApplication"]["dateModified"] == "2026-07-14"
    assert "六爻" not in json.dumps(payload, ensure_ascii=False)


def test_llms_is_fact_first_and_distinguishes_production_from_planned():
    response = TestClient(app).get("/llms.txt")

    assert response.status_code == 200
    assert response.headers["cache-control"] == "public, max-age=300"
    text = response.text
    for section in (
        "## Canonical Identity",
        "## What FateCat Is",
        "## What FateCat Is Not",
        "## Availability Matrix",
        "## Evidence and Reproducibility",
        "## High-Intent Questions and Answers",
        "## Citation Guidance",
        "## Storage, Privacy, and Risk",
    ):
        assert section in text
    assert "Production in this registry" in text
    assert "planned and must not be described as implemented" in text
    assert "not a claim of scientific validity" in text
    assert "https://tradecatlabs-fatecat.hf.space/about" in text
    assert "https://tradecatlabs-fatecat.hf.space/guides/bazi" in text
    assert "https://tradecatlabs-fatecat.hf.space/guides/ziwei" in text


def test_geo_audit_is_part_of_public_release_gate():
    release_gate = (ROOT / "scripts" / "public-release-gate.sh").read_text(encoding="utf-8")
    local_ci = (ROOT / "scripts" / "local-ci.sh").read_text(encoding="utf-8")

    assert 'python_bin="${runtime_root}/.venv/bin/python"' in release_gate
    assert 'python_bin="python3"' in release_gate
    assert '"${script_dir}/geo-audit.py"' in release_gate
    assert '"${script_dir}/geo-query-set-gate.py"' in release_gate
    assert "tests/regression/test_geo_discovery.py" in local_ci
    assert '"${script_dir}/geo-query-set-gate.py"' in local_ci


def test_geo_audit_checks_redirect_and_capability_lifecycle_sets():
    audit_source = (ROOT / "scripts" / "geo-audit.py").read_text(encoding="utf-8")

    assert 'Check("root.permanent_redirect"' in audit_source
    assert '"capabilities.available_set"' in audit_source
    assert '"capabilities.production_maturity_set"' in audit_source
    assert '"capabilities.validated_maturity_set"' in audit_source
    assert '"capabilities.planned_set"' in audit_source
