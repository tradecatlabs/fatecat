#!/usr/bin/env python3
"""算准网“基础/典籍”栏目可恢复、可审计的本地语料抓取器。"""

from __future__ import annotations

import argparse
import contextlib
import dataclasses
import datetime as dt
import gzip
import hashlib
import html as html_lib
import ipaddress
import json
import mimetypes
import os
import re
import socket
import sqlite3
import statistics
import time
import unicodedata
import urllib.parse
import urllib.robotparser
import xml.etree.ElementTree as ET
from collections.abc import Iterable, Iterator
from pathlib import Path
from typing import Any, Final

try:
    import httpx
    from bs4 import BeautifulSoup, Comment, NavigableString, Tag
except ImportError as exc:  # pragma: no cover - 仅在依赖缺失环境触发
    raise SystemExit("缺少抓取依赖；请执行：uv pip install --python .venv/bin/python -e '.[data]'") from exc


BASE_URL: Final = "https://www.suanzhun.net"
ROOT_URLS: Final = (f"{BASE_URL}/jichu/", f"{BASE_URL}/dianji/")
EXPECTED_CATEGORY_SLUGS: Final = {
    "jichu": {
        "caiguan",
        "changshi",
        "diaohou",
        "geju",
        "mangpai",
        "minglishuyu",
        "tongguan",
        "wangshuai",
        "xinpai",
    },
    "dianji": {
        "baojianlishilu",
        "bazitiyao",
        "baziyuyongshen",
        "ditiansui",
        "ditiansuichanwei",
        "jinxiangmishu",
        "lantaimiaoxuan",
        "mangpaichujiminglixue",
        "minglitanyuan",
        "mingliyueyan",
        "minglizhenjuedaodu",
        "qianliminggao",
        "qianliminggaobuchong",
        "qiongtongbaojian",
        "qitadanpian",
        "sancheyilan",
        "sanmingtonghui",
        "shenfengtongkao",
        "sizhuyucejingyanjiqiao",
        "wuxingdayi",
        "wuxingjingji",
        "xingpinghuihai",
        "yuanhaiziping",
        "yudinzhipin",
        "yuyandianji",
        "zipingguanjian",
        "zipingzhen",
        "zipingzhenpingzhu",
    },
}
ROBOTS_URL: Final = f"{BASE_URL}/robots.txt"
SITEMAP_URL: Final = f"{BASE_URL}/sitemap.xml"
SCHEMA_VERSION: Final = "suanzhun-corpus.v2"
USER_AGENT: Final = "FateCatCorpusCrawler/1.0"
TRACKING_KEYS: Final = {"fbclid", "gclid", "ref", "source"}
ATTACHMENT_SUFFIXES: Final = {
    ".7z",
    ".csv",
    ".doc",
    ".docx",
    ".epub",
    ".pdf",
    ".rar",
    ".rtf",
    ".txt",
    ".xls",
    ".xlsx",
    ".xml",
    ".zip",
}
DROP_SELECTORS: Final = (
    "script",
    "style",
    "noscript",
    "iframe",
    "form",
    "object",
    "embed",
    "nav",
    "footer",
    ".bdf",
    ".p2",
    ".related",
    ".recommend",
    ".recommendation",
    ".advertisement",
    ".ads",
    ".ad",
    "[id*='related']",
    "[class*='xiangguan']",
    "[class*='tuijian']",
)


def utc_now() -> str:
    return dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def json_dumps(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def canonicalize_url(url: str, base_url: str = BASE_URL) -> str:
    """规范化站内 URL，移除 fragment 与追踪参数。"""
    absolute = urllib.parse.urljoin(base_url, html_lib.unescape(url.strip()))
    parsed = urllib.parse.urlsplit(absolute)
    scheme = (
        "https"
        if parsed.hostname and parsed.hostname.lower() in {"suanzhun.net", "www.suanzhun.net"}
        else parsed.scheme.lower()
    )
    hostname = (parsed.hostname or "").lower()
    if hostname in {"suanzhun.net", "www.suanzhun.net"}:
        hostname = "www.suanzhun.net"
    port = parsed.port
    netloc = hostname
    if port and not ((scheme == "https" and port == 443) or (scheme == "http" and port == 80)):
        netloc = f"{hostname}:{port}"
    path = re.sub(r"/{2,}", "/", parsed.path or "/")
    if path.endswith("/index.html"):
        path = path[: -len("index.html")]
    query_pairs = []
    for key, value in urllib.parse.parse_qsl(parsed.query, keep_blank_values=True):
        lowered = key.lower()
        if lowered.startswith("utm_") or lowered in TRACKING_KEYS:
            continue
        query_pairs.append((key, value))
    query = urllib.parse.urlencode(sorted(query_pairs))
    return urllib.parse.urlunsplit((scheme, netloc, path, query, ""))


@dataclasses.dataclass(frozen=True, slots=True)
class UrlClass:
    kind: str
    section_hint: str | None = None
    category_slug: str | None = None
    base_url: str | None = None
    page_number: int | None = None


def classify_url(url: str) -> UrlClass:
    normalized = canonicalize_url(url)
    parsed = urllib.parse.urlsplit(normalized)
    if parsed.hostname != "www.suanzhun.net" or parsed.scheme not in {"http", "https"}:
        return UrlClass("ignore")
    path = parsed.path
    current = re.fullmatch(r"/(article|book)/(\d+)(?:_(\d+))?\.html", path)
    if current:
        base_url = urllib.parse.urlunsplit(
            (parsed.scheme, parsed.netloc, f"/{current.group(1)}/{current.group(2)}.html", "", "")
        )
        return UrlClass(
            "detail",
            "jichu" if current.group(1) == "article" else "dianji",
            base_url=base_url,
            page_number=int(current.group(3) or 1),
        )
    legacy = re.fullmatch(r"/(jichu|dianji)/([^/]+)/(\d+)(?:_(\d+))?\.html", path)
    if legacy:
        base_url = urllib.parse.urlunsplit(
            (parsed.scheme, parsed.netloc, f"/{legacy.group(1)}/{legacy.group(2)}/{legacy.group(3)}.html", "", "")
        )
        return UrlClass(
            "detail",
            legacy.group(1),
            legacy.group(2),
            base_url,
            int(legacy.group(4) or 1),
        )
    listing = re.fullmatch(r"/(jichu|dianji)(?:/([^/]+))?/(?:index(?:_\d+)?\.html)?", path)
    if listing:
        return UrlClass("list", listing.group(1), listing.group(2))
    return UrlClass("ignore")


def _normal_text(value: str) -> str:
    value = unicodedata.normalize("NFKC", value).replace("\xa0", " ")
    value = re.sub(r"[ \t\f\v]+", " ", value)
    value = re.sub(r" *\n *", "\n", value)
    value = re.sub(r"\n{3,}", "\n\n", value)
    return value.strip()


def _safe_filename(value: str, max_length: int = 80) -> str:
    value = unicodedata.normalize("NFKC", value)
    value = re.sub(r"[<>:\"/\\|?*\x00-\x1f]", "-", value)
    value = re.sub(r"\s+", "-", value).strip(" .-")
    value = re.sub(r"-{2,}", "-", value)
    reserved = {"CON", "PRN", "AUX", "NUL", *(f"COM{i}" for i in range(1, 10)), *(f"LPT{i}" for i in range(1, 10))}
    if not value or value.upper() in reserved:
        value = "untitled"
    return value[:max_length].rstrip(" .-") or "untitled"


def _record_id(url: str) -> str:
    info = classify_url(url)
    path = urllib.parse.urlsplit(info.base_url or url).path
    current = re.fullmatch(r"/(article|book)/(\d+)\.html", path)
    if current:
        return f"{current.group(1)}-{current.group(2)}"
    legacy = re.fullmatch(r"/(jichu|dianji)/([^/]+)/(\d+)\.html", path)
    if legacy:
        return f"{legacy.group(1)}-{legacy.group(2)}-{legacy.group(3)}"
    return f"url-{hashlib.sha256(url.encode()).hexdigest()[:16]}"


@dataclasses.dataclass(slots=True)
class ParsedPage:
    source_url: str
    page_type: str
    target_urls: list[str]
    base_url: str | None = None
    page_number: int = 1
    page_count: int = 1
    in_scope: bool = False
    section: str | None = None
    category_slug: str | None = None
    category_title: str | None = None
    title: str | None = None
    author: str | None = None
    publisher: str | None = None
    source_name: str | None = None
    published_at: str | None = None
    description: str | None = None
    breadcrumbs: list[dict[str, str | None]] = dataclasses.field(default_factory=list)
    headings: list[dict[str, Any]] = dataclasses.field(default_factory=list)
    body_html: str = ""
    body_text: str = ""
    body_markdown: str = ""
    body_links: list[str] = dataclasses.field(default_factory=list)
    media_urls: list[str] = dataclasses.field(default_factory=list)
    attachment_urls: list[str] = dataclasses.field(default_factory=list)

    @property
    def record_id(self) -> str:
        return _record_id(self.base_url or self.source_url)


def _target_links(soup: BeautifulSoup, source_url: str) -> list[str]:
    targets: set[str] = set()
    for node in soup.select("a[href]"):
        href = node.get("href", "")
        if not href or href.startswith(("javascript:", "mailto:", "tel:")):
            continue
        target = canonicalize_url(href, source_url)
        if classify_url(target).kind != "ignore":
            targets.add(target)
    targets.discard(canonicalize_url(source_url))
    return sorted(targets)


def _detail_page_url(base_url: str, page_number: int) -> str:
    if page_number < 1:
        raise ValueError("详情页页码必须大于等于 1")
    if page_number == 1:
        return base_url
    parsed = urllib.parse.urlsplit(base_url)
    if not parsed.path.endswith(".html"):
        raise ValueError(f"详情页基址不是 HTML: {base_url}")
    path = f"{parsed.path[:-5]}_{page_number}.html"
    return urllib.parse.urlunsplit((parsed.scheme, parsed.netloc, path, "", ""))


def _expand_detail_pagination(
    soup: BeautifulSoup,
    info: UrlClass,
    targets: list[str],
    source_url: str,
) -> tuple[list[str], int]:
    """由可见末页推导完整详情页序列，避免分页窗口隐藏中间页。"""
    if info.kind != "detail" or not info.base_url:
        return targets, 1
    page_numbers = {info.page_number or 1}
    for target in targets:
        target_info = classify_url(target)
        if target_info.kind == "detail" and target_info.base_url == info.base_url and target_info.page_number:
            page_numbers.add(target_info.page_number)
    for node in soup.select(".posts-nav, .pagination, .pages"):
        text = _normal_text(node.get_text(" ", strip=True))
        page_numbers.update(int(match.group(2)) for match in re.finditer(r"(\d+)\s*/\s*(\d+)", text))
        page_numbers.update(int(match.group(1)) for match in re.finditer(r"共\s*(\d+)\s*页", text))
    page_count = max(page_numbers, default=1)
    expanded = set(targets)
    expanded.update(_detail_page_url(info.base_url, number) for number in range(1, page_count + 1))
    expanded.discard(source_url)
    return sorted(expanded), page_count


def _breadcrumbs(article: Tag | BeautifulSoup, source_url: str) -> list[dict[str, str | None]]:
    node = article.select_one(".breadcrumbs, .breadcrumb")
    if not node:
        return []
    result: list[dict[str, str | None]] = []
    for anchor in node.select("a"):
        text = _normal_text(anchor.get_text(" ", strip=True))
        href = anchor.get("href")
        result.append({"text": text, "url": canonicalize_url(href, source_url) if href else None})
    raw = _normal_text(node.get_text(" ", strip=True))
    tail = re.split(r"[>›»]", raw)[-1].strip()
    if tail and (not result or tail != result[-1]["text"]):
        result.append({"text": tail, "url": None})
    return result


def _scope_from_breadcrumbs(items: list[dict[str, str | None]]) -> tuple[str | None, str | None, str | None]:
    section = None
    category_slug = None
    category_title = None
    for item in items:
        url = item.get("url")
        if not url:
            continue
        info = classify_url(url)
        if info.kind == "list" and info.section_hint in {"jichu", "dianji"}:
            section = info.section_hint
            if info.category_slug:
                category_slug = info.category_slug
                category_title = item.get("text")
    return section, category_slug, category_title


def _metadata(article: Tag, soup: BeautifulSoup) -> tuple[str | None, str | None, str | None, str | None, str | None]:
    title_node = article.select_one("h1.singletitle, h1")
    title = _normal_text(title_node.get_text(" ", strip=True)) if title_node else None
    body = article.select_one(".content-text, .content, .article-content")
    header_parts: list[str] = []
    for node in article.descendants:
        if node is body:
            break
        if isinstance(node, NavigableString):
            header_parts.append(str(node))
    header_text = _normal_text("\n".join(header_parts)[:1500])
    date_match = re.search(r"(?:日期|发布时间|时间)\s*[:：]\s*(\d{4})[.年/-](\d{1,2})[.月/-](\d{1,2})", header_text)
    published_at = None
    if date_match:
        published_at = f"{int(date_match.group(1)):04d}-{int(date_match.group(2)):02d}-{int(date_match.group(3)):02d}"
    publisher_match = re.search(r"(?:发布者|来源)\s*[:：]\s*([^\n|]+)", header_text)
    publisher = publisher_match.group(1).strip() if publisher_match else None
    author_match = re.search(r"作者\s*[:：]\s*([^\n|]+)", header_text)
    author = author_match.group(1).strip() if author_match else None
    description_node = soup.select_one("meta[name='description']")
    description = _normal_text(description_node.get("content", "")) if description_node else None
    return title, published_at, publisher, author or None, description


def _resource_urls(body: Tag, source_url: str) -> tuple[list[str], list[str], list[str]]:
    media: set[str] = set()
    attachments: set[str] = set()
    links: set[str] = set()
    for node in body.select("img, video, audio, source"):
        value = node.get("src") or node.get("data-src") or node.get("data-original")
        if value:
            media.add(canonicalize_url(value, source_url))
        srcset = node.get("srcset") or node.get("data-srcset")
        if srcset:
            for candidate in srcset.split(","):
                media.add(canonicalize_url(candidate.strip().split()[0], source_url))
    for node in body.select("a[href]"):
        url = canonicalize_url(node.get("href", ""), source_url)
        if urllib.parse.urlsplit(url).scheme not in {"http", "https"}:
            continue
        links.add(url)
        if Path(urllib.parse.urlsplit(url).path).suffix.lower() in ATTACHMENT_SUFFIXES:
            attachments.add(url)
    return sorted(media), sorted(attachments), sorted(links)


def _clean_body(body: Tag, source_url: str) -> Tag:
    clone_soup = BeautifulSoup(str(body), "html.parser")
    clone = clone_soup.select_one(".content-text") or clone_soup
    for marker in clone.find_all(string=lambda value: isinstance(value, Comment) and "content_text" in value):
        for sibling in list(marker.next_siblings):
            sibling.extract()
        marker.extract()
    for selector in DROP_SELECTORS:
        for node in clone.select(selector):
            node.decompose()
    for node in clone.find_all(True):
        if node.name in {"img", "video", "audio", "source"}:
            lazy = node.get("data-src") or node.get("data-original")
            if lazy and not node.get("src"):
                node["src"] = lazy
        if node.get("href"):
            href = canonicalize_url(node["href"], source_url)
            if urllib.parse.urlsplit(href).scheme in {"http", "https"}:
                node["href"] = href
            else:
                del node["href"]
        if node.get("src"):
            src = canonicalize_url(node["src"], source_url)
            if urllib.parse.urlsplit(src).scheme in {"http", "https"}:
                node["src"] = src
            else:
                del node["src"]
        if node.get("srcset"):
            candidates = []
            for candidate in str(node["srcset"]).split(","):
                parts = candidate.strip().split()
                url = canonicalize_url(parts[0], source_url)
                if urllib.parse.urlsplit(url).scheme in {"http", "https"}:
                    candidates.append(" ".join([url, *parts[1:]]))
            if candidates:
                node["srcset"] = ", ".join(candidates)
            else:
                del node["srcset"]
        allowed = {"href", "src", "srcset", "alt", "title", "colspan", "rowspan", "width", "height", "controls"}
        node.attrs = {key: value for key, value in node.attrs.items() if key in allowed}
    return clone


def _inline_markdown(node: Tag | NavigableString) -> str:
    if isinstance(node, NavigableString):
        return str(node)
    inner = "".join(_inline_markdown(child) for child in node.children)
    if node.name in {"strong", "b"}:
        return f"**{inner.strip()}**"
    if node.name in {"em", "i"}:
        return f"*{inner.strip()}*"
    if node.name == "code":
        return f"`{inner.strip()}`"
    if node.name == "a" and node.get("href"):
        return f"[{inner.strip()}]({node['href']})"
    if node.name == "img" and node.get("src"):
        return f"![{node.get('alt', '')}]({node['src']})"
    if node.name == "br":
        return "\n"
    return inner


def _table_markdown(table: Tag) -> str:
    rows: list[list[str]] = []
    for tr in table.select("tr"):
        cells = [_normal_text(cell.get_text(" ", strip=True)).replace("|", "\\|") for cell in tr.select("th, td")]
        if cells:
            rows.append(cells)
    if not rows:
        return ""
    width = max(len(row) for row in rows)
    rows = [row + [""] * (width - len(row)) for row in rows]
    lines = ["| " + " | ".join(rows[0]) + " |", "| " + " | ".join(["---"] * width) + " |"]
    lines.extend("| " + " | ".join(row) + " |" for row in rows[1:])
    return "\n".join(lines)


def _block_markdown(node: Tag | NavigableString, depth: int = 0) -> str:
    if isinstance(node, NavigableString):
        return _normal_text(str(node))
    name = node.name
    if name in {f"h{i}" for i in range(1, 7)}:
        return f"{'#' * int(name[1])} {_normal_text(node.get_text(' ', strip=True))}\n\n"
    if name == "table":
        return _table_markdown(node) + "\n\n"
    if name == "blockquote":
        text = _normal_text(node.get_text("\n", strip=True))
        return "\n".join(f"> {line}" for line in text.splitlines()) + "\n\n"
    if name == "pre":
        return f"```\n{node.get_text()}\n```\n\n"
    if name in {"ul", "ol"}:
        lines = []
        for index, li in enumerate(node.find_all("li", recursive=False), 1):
            marker = f"{index}." if name == "ol" else "-"
            lines.append(f"{'  ' * depth}{marker} {_normal_text(_inline_markdown(li))}")
        return "\n".join(lines) + "\n\n"
    if name in {"p", "div", "section", "article"}:
        blocks = "".join(_block_markdown(child, depth) for child in node.children)
        if any(
            isinstance(child, Tag)
            and child.name
            in {"p", "div", "section", "h1", "h2", "h3", "h4", "h5", "h6", "ul", "ol", "table", "blockquote", "pre"}
            for child in node.children
        ):
            return blocks
        return _normal_text(_inline_markdown(node)) + "\n\n"
    if name == "br":
        return "\n"
    return "".join(_block_markdown(child, depth) for child in node.children)


def _to_markdown(body: Tag) -> str:
    return _normal_text("".join(_block_markdown(child) for child in body.children)) + "\n"


def parse_page(html: bytes, source_url: str) -> ParsedPage:
    """把列表页或详情页解析为稳定的中间模型。"""
    source_url = canonicalize_url(source_url)
    info = classify_url(source_url)
    soup = BeautifulSoup(html, "html.parser")
    targets = _target_links(soup, source_url)
    if info.kind != "detail":
        return ParsedPage(source_url=source_url, page_type=info.kind, target_urls=targets)
    targets, page_count = _expand_detail_pagination(soup, info, targets, source_url)

    article = soup.select_one("article.box, article") or soup
    crumbs = _breadcrumbs(article, source_url)
    section, category_slug, category_title = _scope_from_breadcrumbs(crumbs)
    title, published_at, publisher, author, description = _metadata(article, soup)
    body = article.select_one(".content-text, .content, .article-content")
    if body is None:
        return ParsedPage(
            source_url=source_url,
            page_type="detail",
            target_urls=targets,
            base_url=info.base_url,
            page_number=info.page_number or 1,
            page_count=page_count,
            in_scope=False,
            breadcrumbs=crumbs,
            title=title,
        )
    cleaned = _clean_body(body, source_url)
    media_urls, attachment_urls, body_links = _resource_urls(cleaned, source_url)
    body_html = cleaned.decode_contents(formatter="minimal").strip()
    body_text = _normal_text(cleaned.get_text("\n", strip=True))
    headings = [
        {"level": int(node.name[1]), "text": _normal_text(node.get_text(" ", strip=True))}
        for node in cleaned.select("h1, h2, h3, h4, h5, h6")
    ]
    return ParsedPage(
        source_url=source_url,
        page_type="detail",
        target_urls=targets,
        base_url=info.base_url,
        page_number=info.page_number or 1,
        page_count=page_count,
        in_scope=section in {"jichu", "dianji"},
        section=section,
        category_slug=category_slug or info.category_slug or "uncategorized",
        category_title=category_title,
        title=title,
        author=author,
        publisher=publisher,
        source_name=publisher,
        published_at=published_at,
        description=description,
        breadcrumbs=crumbs,
        headings=headings,
        body_html=body_html,
        body_text=body_text,
        body_markdown=_to_markdown(cleaned),
        body_links=body_links,
        media_urls=media_urls,
        attachment_urls=attachment_urls,
    )


def build_content_relpaths(page: ParsedPage) -> tuple[Path, Path]:
    if not page.section:
        raise ValueError("越界页面不能生成正文路径")
    return _content_relpaths(
        page.section,
        page.category_slug or "uncategorized",
        page.record_id,
        page.title,
    )


def _content_relpaths(
    section: str,
    category_slug: str,
    record_id: str,
    title: str | None,
) -> tuple[Path, Path]:
    category = _safe_filename(category_slug, 60)
    stem = f"{record_id}--{_safe_filename(title or 'untitled')}"
    parent = Path("content") / section / category
    return parent / f"{stem}.html", parent / f"{stem}.md"


@dataclasses.dataclass(slots=True)
class FetchResult:
    url: str
    final_url: str
    status_code: int | None
    body: bytes
    content_type: str | None
    elapsed_ms: int
    attempts: int
    error: str | None = None


class Fetcher:
    """带连接复用、限速、有限重试与体积上限的同步下载器。"""

    def __init__(
        self,
        *,
        delay_seconds: float,
        timeout_seconds: float,
        max_attempts: int,
        max_page_bytes: int,
    ) -> None:
        self.delay_seconds = delay_seconds
        self.max_attempts = max_attempts
        self.max_page_bytes = max_page_bytes
        self.last_request_at = 0.0
        self.client = httpx.Client(
            headers={
                "User-Agent": USER_AGENT,
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/*;q=0.8,*/*;q=0.5",
                "Accept-Language": "zh-CN,zh;q=0.9",
            },
            timeout=httpx.Timeout(timeout_seconds),
            follow_redirects=False,
        )
        self.request_count = 0
        self.retry_count = 0

    def close(self) -> None:
        self.client.close()

    def _pace(self) -> None:
        remaining = self.delay_seconds - (time.monotonic() - self.last_request_at)
        if remaining > 0:
            time.sleep(remaining)

    def _single(self, url: str, max_bytes: int) -> tuple[httpx.Response, bytes, int]:
        self._pace()
        started = time.monotonic()
        with self.client.stream("GET", url) as response:
            self.last_request_at = time.monotonic()
            self.request_count += 1
            declared = response.headers.get("content-length")
            if declared and int(declared) > max_bytes:
                raise ValueError(f"响应声明体积超过上限: {declared} > {max_bytes}")
            chunks: list[bytes] = []
            size = 0
            for chunk in response.iter_bytes():
                size += len(chunk)
                if size > max_bytes:
                    raise ValueError(f"响应实际体积超过上限: {size} > {max_bytes}")
                chunks.append(chunk)
            body = b"".join(chunks)
        return response, body, int((time.monotonic() - started) * 1000)

    def fetch(
        self,
        url: str,
        *,
        max_bytes: int | None = None,
        allow_external: bool = False,
        external_host_allowlist: set[str] | None = None,
    ) -> FetchResult:
        max_bytes = max_bytes or self.max_page_bytes
        current = canonicalize_url(url)
        total_elapsed = 0
        last_error = None
        last_status = None
        attempts_used = 0
        for attempt in range(1, self.max_attempts + 1):
            attempts_used = attempt
            redirects = 0
            try:
                while True:
                    host = urllib.parse.urlsplit(current).hostname
                    if (not allow_external and host != "www.suanzhun.net") or (
                        allow_external
                        and host not in (external_host_allowlist or set())
                        and not _is_public_http_url(current)
                    ):
                        raise ValueError("重定向目标不在允许的公开网络边界内")
                    response, body, elapsed = self._single(current, max_bytes)
                    total_elapsed += elapsed
                    last_status = response.status_code
                    if response.status_code in {301, 302, 303, 307, 308}:
                        location = response.headers.get("location")
                        if not location or redirects >= 5:
                            raise ValueError("重定向缺少 Location 或超过 5 次")
                        current = canonicalize_url(location, current)
                        redirects += 1
                        continue
                    if response.status_code in {408, 425, 429, 500, 502, 503, 504}:
                        if attempt < self.max_attempts:
                            retry_after = response.headers.get("retry-after", "")
                            delay = float(retry_after) if retry_after.isdigit() else min(2 ** (attempt - 1), 8)
                            self.retry_count += 1
                            time.sleep(delay)
                            break
                    return FetchResult(
                        url=url,
                        final_url=current,
                        status_code=response.status_code,
                        body=body,
                        content_type=response.headers.get("content-type"),
                        elapsed_ms=total_elapsed,
                        attempts=attempt,
                    )
            except ValueError as exc:
                last_error = f"{type(exc).__name__}: {exc}"
                break
            except (httpx.HTTPError, OSError) as exc:
                last_error = f"{type(exc).__name__}: {exc}"
                if attempt < self.max_attempts:
                    self.retry_count += 1
                    time.sleep(min(2 ** (attempt - 1), 8))
                    continue
                break
        return FetchResult(
            url=url,
            final_url=current,
            status_code=last_status,
            body=b"",
            content_type=None,
            elapsed_ms=total_elapsed,
            attempts=attempts_used,
            error=last_error or f"HTTP {last_status}",
        )


class CrawlStore:
    """抓取状态与追溯关系的单一真相源。"""

    def __init__(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(path)
        self.connection.row_factory = sqlite3.Row
        self.connection.execute("PRAGMA foreign_keys = ON")
        self.connection.execute("PRAGMA journal_mode = WAL")
        self.connection.execute("PRAGMA synchronous = NORMAL")
        self._create_schema()

    def _create_schema(self) -> None:
        self.connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS frontier (
                url TEXT PRIMARY KEY,
                kind TEXT NOT NULL,
                section_hint TEXT,
                category_slug TEXT,
                status TEXT NOT NULL DEFAULT 'pending',
                priority INTEGER NOT NULL,
                depth INTEGER NOT NULL DEFAULT 0,
                discovered_from TEXT,
                attempts INTEGER NOT NULL DEFAULT 0,
                http_status INTEGER,
                fetched_at TEXT,
                error TEXT,
                raw_path TEXT,
                response_sha256 TEXT,
                elapsed_ms INTEGER,
                content_type TEXT
            );
            CREATE INDEX IF NOT EXISTS frontier_status_priority_idx
                ON frontier(status, priority, depth, url);
            CREATE TABLE IF NOT EXISTS edges (
                source_url TEXT NOT NULL,
                target_url TEXT NOT NULL,
                relation TEXT NOT NULL,
                discovered_at TEXT NOT NULL,
                PRIMARY KEY(source_url, target_url, relation)
            );
            CREATE TABLE IF NOT EXISTS documents (
                source_url TEXT PRIMARY KEY,
                record_id TEXT NOT NULL UNIQUE,
                section TEXT NOT NULL,
                category_slug TEXT NOT NULL,
                title TEXT,
                content_sha256 TEXT NOT NULL,
                duplicate_of TEXT,
                html_path TEXT NOT NULL,
                markdown_path TEXT NOT NULL,
                data_json TEXT NOT NULL,
                extracted_at TEXT NOT NULL
            );
            CREATE INDEX IF NOT EXISTS documents_content_sha_idx ON documents(content_sha256);
            CREATE TABLE IF NOT EXISTS document_pages (
                page_url TEXT PRIMARY KEY,
                base_url TEXT NOT NULL,
                page_number INTEGER NOT NULL CHECK(page_number >= 1),
                page_count INTEGER NOT NULL CHECK(page_count >= page_number),
                section TEXT NOT NULL,
                category_slug TEXT NOT NULL,
                content_sha256 TEXT NOT NULL,
                raw_path TEXT NOT NULL,
                data_json TEXT NOT NULL,
                extracted_at TEXT NOT NULL,
                pagination_scanned INTEGER NOT NULL DEFAULT 1,
                UNIQUE(base_url, page_number)
            );
            CREATE INDEX IF NOT EXISTS document_pages_base_idx
                ON document_pages(base_url, page_number);
            CREATE TABLE IF NOT EXISTS resources (
                url TEXT PRIMARY KEY,
                kind TEXT NOT NULL,
                source_url TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'pending',
                attempts INTEGER NOT NULL DEFAULT 0,
                http_status INTEGER,
                fetched_at TEXT,
                error TEXT,
                content_type TEXT,
                sha256 TEXT,
                local_path TEXT,
                byte_size INTEGER
            );
            CREATE INDEX IF NOT EXISTS resources_status_idx ON resources(status, url);
            CREATE TABLE IF NOT EXISTS page_resources (
                page_url TEXT NOT NULL,
                resource_url TEXT NOT NULL,
                kind TEXT NOT NULL,
                PRIMARY KEY(page_url, resource_url),
                FOREIGN KEY(page_url) REFERENCES document_pages(page_url) ON DELETE CASCADE,
                FOREIGN KEY(resource_url) REFERENCES resources(url) ON DELETE CASCADE
            );
            CREATE TABLE IF NOT EXISTS document_resources (
                source_url TEXT NOT NULL,
                resource_url TEXT NOT NULL,
                kind TEXT NOT NULL,
                PRIMARY KEY(source_url, resource_url),
                FOREIGN KEY(source_url) REFERENCES documents(source_url) ON DELETE CASCADE,
                FOREIGN KEY(resource_url) REFERENCES resources(url) ON DELETE CASCADE
            );
            CREATE TABLE IF NOT EXISTS sitemap_entries (
                url TEXT PRIMARY KEY,
                kind TEXT NOT NULL,
                seen_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS runs (
                run_id TEXT PRIMARY KEY,
                started_at TEXT NOT NULL,
                finished_at TEXT,
                status TEXT NOT NULL,
                options_json TEXT NOT NULL,
                summary_json TEXT
            );
            """
        )
        self._backfill_document_pages()
        self.connection.commit()

    def _backfill_document_pages(self) -> None:
        """把 v1 逻辑文档无损登记为待重新扫描的第一页证据。"""
        rows = self.connection.execute(
            """
            SELECT d.* FROM documents d
            LEFT JOIN document_pages p ON p.page_url = d.source_url
            WHERE p.page_url IS NULL
            ORDER BY d.source_url
            """
        ).fetchall()
        for row in rows:
            record = json.loads(row["data_json"])
            page_count = max(1, int(record.get("page_count") or 1))
            self.connection.execute(
                """
                INSERT INTO document_pages(
                    page_url, base_url, page_number, page_count, section, category_slug,
                    content_sha256, raw_path, data_json, extracted_at, pagination_scanned
                ) VALUES (?, ?, 1, ?, ?, ?, ?, ?, ?, ?, 0)
                """,
                (
                    row["source_url"],
                    row["source_url"],
                    page_count,
                    row["section"],
                    row["category_slug"],
                    row["content_sha256"],
                    record.get("raw_path") or "",
                    row["data_json"],
                    row["extracted_at"],
                ),
            )
        self.connection.execute(
            """
            INSERT OR IGNORE INTO page_resources(page_url, resource_url, kind)
            SELECT dr.source_url, dr.resource_url, dr.kind
            FROM document_resources dr
            JOIN document_pages p ON p.page_url = dr.source_url
            """
        )

    def close(self) -> None:
        self.connection.commit()
        with contextlib.suppress(sqlite3.OperationalError):
            self.connection.execute("PRAGMA wal_checkpoint(TRUNCATE)")
        self.connection.close()

    def add_url(self, url: str, *, discovered_from: str | None = None, depth: int = 0) -> bool:
        url = canonicalize_url(url)
        info = classify_url(url)
        if info.kind == "ignore":
            return False
        priority = 10 if info.kind == "list" else 20
        cursor = self.connection.execute(
            """
            INSERT OR IGNORE INTO frontier(
                url, kind, section_hint, category_slug, status, priority, depth, discovered_from
            ) VALUES (?, ?, ?, ?, 'pending', ?, ?, ?)
            """,
            (url, info.kind, info.section_hint, info.category_slug, priority, depth, discovered_from),
        )
        return cursor.rowcount > 0

    def add_edge(self, source: str, target: str, relation: str) -> None:
        self.connection.execute(
            "INSERT OR IGNORE INTO edges(source_url, target_url, relation, discovered_at) VALUES (?, ?, ?, ?)",
            (source, target, relation, utc_now()),
        )

    def next_page(self) -> sqlite3.Row | None:
        return self.connection.execute(
            "SELECT * FROM frontier WHERE status = 'pending' ORDER BY priority, depth, url LIMIT 1"
        ).fetchone()

    def mark_fetching(self, url: str) -> None:
        self.connection.execute("UPDATE frontier SET status = 'fetching', error = NULL WHERE url = ?", (url,))
        self.connection.commit()

    def finish_page(
        self, url: str, result: FetchResult, status: str, *, raw_path: str | None = None, error: str | None = None
    ) -> None:
        self.connection.execute(
            """
            UPDATE frontier SET status = ?, attempts = attempts + ?, http_status = ?, fetched_at = ?,
                error = ?, raw_path = ?, response_sha256 = ?, elapsed_ms = ?, content_type = ?
            WHERE url = ?
            """,
            (
                status,
                result.attempts,
                result.status_code,
                utc_now(),
                error or result.error,
                raw_path,
                sha256_bytes(result.body) if result.body else None,
                result.elapsed_ms,
                result.content_type,
                url,
            ),
        )
        self.connection.commit()

    def add_page_resource(self, page_url: str, url: str, kind: str) -> None:
        self.connection.execute(
            "INSERT OR IGNORE INTO resources(url, kind, source_url) VALUES (?, ?, ?)",
            (url, kind, page_url),
        )
        self.connection.execute(
            "INSERT OR IGNORE INTO page_resources(page_url, resource_url, kind) VALUES (?, ?, ?)",
            (page_url, url, kind),
        )


def _atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    with temporary.open("wb") as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, path)


def _write_json(path: Path, value: Any) -> None:
    _atomic_write(path, (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode())


def _raw_relpath(url: str) -> Path:
    digest = hashlib.sha256(url.encode()).hexdigest()
    return Path("raw/pages") / digest[:2] / f"{digest}.html.gz"


def _save_raw(output: Path, url: str, body: bytes) -> str:
    relpath = _raw_relpath(url)
    _atomic_write(output / relpath, gzip.compress(body, compresslevel=6, mtime=0))
    return relpath.as_posix()


def _relation(source: str, target: str, source_type: str) -> str:
    target_info = classify_url(target)
    if target_info.kind == "list":
        if "index_" in urllib.parse.urlsplit(target).path:
            return "pagination"
        return "category"
    source_info = classify_url(source)
    if (
        source_type == "detail"
        and source_info.base_url
        and source_info.base_url == target_info.base_url
        and target_info.page_number
    ):
        return "detail_pagination"
    return "list_item" if source_type == "list" else "related_or_adjacent"


def _document_record(page: ParsedPage, raw_path: str, fetched_at: str) -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "record_id": page.record_id,
        "section": page.section,
        "category": {"slug": page.category_slug, "title": page.category_title},
        "title": page.title,
        "author": page.author,
        "publisher": page.publisher,
        "source_name": page.source_name,
        "published_at": page.published_at,
        "description": page.description,
        "source_url": page.source_url,
        "logical_source_url": page.base_url or page.source_url,
        "page_number": page.page_number,
        "page_count": page.page_count,
        "breadcrumbs": page.breadcrumbs,
        "chapter_path": [item["text"] for item in page.breadcrumbs if item.get("text")],
        "headings": page.headings,
        "body_html": page.body_html,
        "body_text": page.body_text,
        "body_markdown": page.body_markdown,
        "body_links": page.body_links,
        "discovered_links": page.target_urls,
        "media_urls": page.media_urls,
        "attachment_urls": page.attachment_urls,
        "raw_path": raw_path,
        "fetched_at": fetched_at,
    }


def _save_document_page(store: CrawlStore, page: ParsedPage, raw_path: str) -> None:
    if not page.section or not page.base_url:
        raise ValueError("越界页面或缺少逻辑文章基址，不能保存详情页")
    fetched_at = utc_now()
    content_hash = sha256_bytes(_normal_text(page.body_text).encode())
    record = _document_record(page, raw_path, fetched_at)
    record["content_sha256"] = content_hash
    store.connection.execute(
        """
        INSERT INTO document_pages(
            page_url, base_url, page_number, page_count, section, category_slug,
            content_sha256, raw_path, data_json, extracted_at, pagination_scanned
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
        ON CONFLICT(page_url) DO UPDATE SET
            base_url = excluded.base_url, page_number = excluded.page_number,
            page_count = excluded.page_count, section = excluded.section,
            category_slug = excluded.category_slug, content_sha256 = excluded.content_sha256,
            raw_path = excluded.raw_path, data_json = excluded.data_json,
            extracted_at = excluded.extracted_at, pagination_scanned = 1
        """,
        (
            page.source_url,
            page.base_url,
            page.page_number,
            page.page_count,
            page.section,
            page.category_slug or "uncategorized",
            content_hash,
            raw_path,
            json_dumps(record),
            fetched_at,
        ),
    )
    store.connection.execute("DELETE FROM page_resources WHERE page_url = ?", (page.source_url,))
    for url in page.media_urls:
        store.add_page_resource(page.source_url, url, "media")
    for url in page.attachment_urls:
        store.add_page_resource(page.source_url, url, "attachment")


def _ordered_unique(records: list[dict[str, Any]], key: str) -> list[Any]:
    result: list[Any] = []
    seen: set[str] = set()
    for record in records:
        for item in record.get(key, []):
            marker = json_dumps(item) if isinstance(item, (dict, list)) else str(item)
            if marker not in seen:
                seen.add(marker)
                result.append(item)
    return result


def _materialize_document(store: CrawlStore, output: Path, base_url: str) -> bool:
    rows = store.connection.execute(
        "SELECT * FROM document_pages WHERE base_url = ? ORDER BY page_number",
        (base_url,),
    ).fetchall()
    if not rows:
        return False
    page_count = max(int(row["page_count"]) for row in rows)
    page_numbers = [int(row["page_number"]) for row in rows]
    if page_numbers != list(range(1, page_count + 1)):
        return False
    records = [json.loads(row["data_json"]) for row in rows]
    first = records[0]
    section = str(first["section"])
    category = first.get("category") or {}
    category_slug = str(category.get("slug") or "uncategorized")
    record_id = _record_id(base_url)
    title = first.get("title")
    html_rel, markdown_rel = _content_relpaths(section, category_slug, record_id, title)

    if page_count == 1:
        body_html = first.get("body_html", "")
        body_markdown = first.get("body_markdown", "")
    else:
        body_html = "\n".join(
            (
                f'<section data-source-page="{row["page_number"]}" '
                f'data-source-url="{html_lib.escape(row["page_url"], quote=True)}">\n'
                f"{record.get('body_html', '')}\n</section>"
            )
            for row, record in zip(rows, records, strict=True)
        )
        body_markdown = (
            "\n\n".join(
                (
                    f"<!-- source-page: {row['page_number']} {row['page_url']} -->\n\n"
                    f"{record.get('body_markdown', '').strip()}"
                )
                for row, record in zip(rows, records, strict=True)
            ).rstrip()
            + "\n"
        )
    body_text = "\n\n".join(record.get("body_text", "") for record in records).strip()
    headings = []
    for row, record in zip(rows, records, strict=True):
        for heading in record.get("headings", []):
            headings.append({**heading, "source_page": int(row["page_number"])})
    source_pages = [
        {
            "page_number": int(row["page_number"]),
            "source_url": row["page_url"],
            "raw_path": row["raw_path"],
            "fetched_at": row["extracted_at"],
            "content_sha256": row["content_sha256"],
        }
        for row in rows
    ]
    content_hash = sha256_bytes(_normal_text(body_text).encode())
    duplicate_of = None
    escaped_title = html_lib.escape(title or "未命名")
    source = html_lib.escape(base_url, quote=True)
    rendered = (
        '<!doctype html>\n<html lang="zh-CN"><head><meta charset="utf-8">'
        f'<title>{escaped_title}</title></head><body><article data-source-url="{source}">'
        f"<h1>{escaped_title}</h1>\n{body_html}\n</article></body></html>\n"
    )
    _atomic_write(output / html_rel, rendered.encode())
    markdown = (
        f"# {title or '未命名'}\n\n"
        f"- 原始链接：{base_url}\n"
        f"- 栏目：{section}\n"
        f"- 分类：{category.get('title') or category_slug}\n"
        f"- 作者：{first.get('author') or '未标注'}\n"
        f"- 来源：{first.get('source_name') or '未标注'}\n"
        f"- 发布时间：{first.get('published_at') or '未标注'}\n"
        f"- 来源页数：{page_count}\n\n"
        f"{body_markdown}"
    )
    _atomic_write(output / markdown_rel, markdown.encode())
    record = {
        **first,
        "schema_version": SCHEMA_VERSION,
        "record_id": record_id,
        "source_url": base_url,
        "logical_source_url": base_url,
        "page_count": page_count,
        "source_pages": source_pages,
        "headings": headings,
        "body_html": body_html,
        "body_text": body_text,
        "body_markdown": body_markdown,
        "body_links": _ordered_unique(records, "body_links"),
        "discovered_links": _ordered_unique(records, "discovered_links"),
        "media_urls": _ordered_unique(records, "media_urls"),
        "attachment_urls": _ordered_unique(records, "attachment_urls"),
        "raw_path": rows[0]["raw_path"],
        "fetched_at": max(str(row["extracted_at"]) for row in rows),
    }
    record.pop("page_number", None)
    record["content_sha256"] = content_hash
    record["duplicate_of"] = duplicate_of
    record["html_path"] = html_rel.as_posix()
    record["markdown_path"] = markdown_rel.as_posix()
    store.connection.execute(
        """
        INSERT INTO documents(
            source_url, record_id, section, category_slug, title, content_sha256,
            duplicate_of, html_path, markdown_path, data_json, extracted_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(source_url) DO UPDATE SET
            title = excluded.title, content_sha256 = excluded.content_sha256,
            duplicate_of = excluded.duplicate_of, html_path = excluded.html_path,
            markdown_path = excluded.markdown_path, data_json = excluded.data_json,
            extracted_at = excluded.extracted_at
        """,
        (
            base_url,
            record_id,
            section,
            category_slug,
            title,
            content_hash,
            duplicate_of,
            html_rel.as_posix(),
            markdown_rel.as_posix(),
            json_dumps(record),
            utc_now(),
        ),
    )
    store.connection.execute("DELETE FROM document_resources WHERE source_url = ?", (base_url,))
    store.connection.execute(
        """
        INSERT OR IGNORE INTO document_resources(source_url, resource_url, kind)
        SELECT ?, pr.resource_url, pr.kind
        FROM page_resources pr
        JOIN document_pages p ON p.page_url = pr.page_url
        WHERE p.base_url = ?
        """,
        (base_url, base_url),
    )
    return True


def _materialize_all_documents(store: CrawlStore, output: Path) -> tuple[int, int]:
    materialized = 0
    incomplete = 0
    for row in store.connection.execute("SELECT DISTINCT base_url FROM document_pages ORDER BY base_url").fetchall():
        if _materialize_document(store, output, row["base_url"]):
            materialized += 1
        else:
            incomplete += 1
    _rebuild_duplicate_aliases(store)
    store.connection.commit()
    return materialized, incomplete


def _rebuild_duplicate_aliases(store: CrawlStore) -> int:
    """按内容哈希和最小 URL 重建无环、确定性的重复别名。"""
    store.connection.execute("UPDATE documents SET duplicate_of = NULL")
    aliases = 0
    groups = store.connection.execute(
        """
        SELECT content_sha256, MIN(source_url) AS canonical_url, COUNT(*) AS item_count
        FROM documents GROUP BY content_sha256 HAVING COUNT(*) > 1
        ORDER BY content_sha256
        """
    ).fetchall()
    for group in groups:
        store.connection.execute(
            """
            UPDATE documents SET duplicate_of = ?
            WHERE content_sha256 = ? AND source_url <> ?
            """,
            (group["canonical_url"], group["content_sha256"], group["canonical_url"]),
        )
        aliases += int(group["item_count"]) - 1
    return aliases


def _is_public_http_url(url: str) -> bool:
    parsed = urllib.parse.urlsplit(url)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        return False
    if parsed.hostname == "www.suanzhun.net":
        return True
    try:
        addresses = socket.getaddrinfo(parsed.hostname, parsed.port or 443, type=socket.SOCK_STREAM)
    except socket.gaierror:
        return False
    for address in addresses:
        ip = ipaddress.ip_address(address[4][0])
        if not ip.is_global:
            return False
    return bool(addresses)


def _resource_suffix(url: str, content_type: str | None) -> str:
    suffix = Path(urllib.parse.urlsplit(url).path).suffix.lower()
    if suffix and re.fullmatch(r"\.[a-z0-9]{1,8}", suffix):
        return suffix
    mime = (content_type or "").split(";", 1)[0].strip()
    return mimetypes.guess_extension(mime) or ".bin"


def _fetch_resources(
    store: CrawlStore,
    fetcher: Fetcher,
    output: Path,
    robots: urllib.robotparser.RobotFileParser,
    *,
    allow_external: bool,
    external_host_allowlist: set[str],
    max_resource_bytes: int,
    max_resources: int,
) -> int:
    processed = 0
    rows = store.connection.execute(
        "SELECT * FROM resources WHERE status = 'pending' ORDER BY url LIMIT ?", (max_resources,)
    ).fetchall()
    for row in rows:
        processed += 1
        url = row["url"]
        parsed = urllib.parse.urlsplit(url)
        explicitly_allowed = parsed.hostname in external_host_allowlist
        if not explicitly_allowed and not _is_public_http_url(url):
            status, error = "invalid", "资源 URL 非公开 HTTP(S) 地址"
            store.connection.execute(
                "UPDATE resources SET status = ?, error = ?, fetched_at = ? WHERE url = ?",
                (status, error, utc_now(), url),
            )
            continue
        if parsed.hostname != "www.suanzhun.net" and not allow_external:
            store.connection.execute(
                "UPDATE resources SET status = 'skipped_external', error = ?, fetched_at = ? WHERE url = ?",
                ("未启用外部媒体下载", utc_now(), url),
            )
            continue
        if parsed.hostname == "www.suanzhun.net" and not robots.can_fetch(USER_AGENT, url):
            store.connection.execute(
                "UPDATE resources SET status = 'denied', error = ?, fetched_at = ? WHERE url = ?",
                ("robots.txt 禁止抓取", utc_now(), url),
            )
            continue
        result = fetcher.fetch(
            url,
            max_bytes=max_resource_bytes,
            allow_external=parsed.hostname != "www.suanzhun.net",
            external_host_allowlist=external_host_allowlist,
        )
        if result.status_code and 200 <= result.status_code < 300 and result.body:
            digest = sha256_bytes(result.body)
            suffix = _resource_suffix(url, result.content_type)
            relpath = Path("media") / digest[:2] / f"{digest}{suffix}"
            if not (output / relpath).exists():
                _atomic_write(output / relpath, result.body)
            store.connection.execute(
                """
                UPDATE resources SET status = 'done', attempts = attempts + ?, http_status = ?,
                    fetched_at = ?, error = NULL, content_type = ?, sha256 = ?, local_path = ?, byte_size = ?
                WHERE url = ?
                """,
                (
                    result.attempts,
                    result.status_code,
                    utc_now(),
                    result.content_type,
                    digest,
                    relpath.as_posix(),
                    len(result.body),
                    url,
                ),
            )
        else:
            status = "unavailable" if result.status_code in {404, 410} else "failed"
            store.connection.execute(
                """
                UPDATE resources SET status = ?, attempts = attempts + ?, http_status = ?,
                    fetched_at = ?, error = ? WHERE url = ?
                """,
                (
                    status,
                    result.attempts,
                    result.status_code,
                    utc_now(),
                    result.error or f"HTTP {result.status_code}",
                    url,
                ),
            )
        if processed % 25 == 0:
            print(f"[资源] 已处理 {processed}/{len(rows)}", flush=True)
        store.connection.commit()
    store.connection.commit()
    return processed


def _parse_sitemap(body: bytes) -> list[str]:
    root = ET.fromstring(body)
    urls = []
    for node in root.iter():
        if node.tag.endswith("loc") and node.text:
            with contextlib.suppress(ValueError):
                urls.append(canonicalize_url(node.text.strip()))
    return sorted(set(urls))


def _load_robots_and_sitemap(
    store: CrawlStore, fetcher: Fetcher, output: Path
) -> tuple[urllib.robotparser.RobotFileParser, int]:
    meta = output / "raw/meta"
    robots_result = fetcher.fetch(ROBOTS_URL, max_bytes=2 * 1024 * 1024)
    parser = urllib.robotparser.RobotFileParser()
    parser.set_url(ROBOTS_URL)
    if robots_result.status_code == 404:
        parser.parse([])
    elif robots_result.status_code and 200 <= robots_result.status_code < 300:
        _atomic_write(meta / "robots.txt", robots_result.body)
        parser.parse(robots_result.body.decode("utf-8", errors="replace").splitlines())
    else:
        raise RuntimeError(f"无法安全读取 robots.txt: {robots_result.error or robots_result.status_code}")

    sitemap_count = 0
    if parser.can_fetch(USER_AGENT, SITEMAP_URL):
        sitemap_result = fetcher.fetch(SITEMAP_URL, max_bytes=20 * 1024 * 1024)
        if sitemap_result.status_code and 200 <= sitemap_result.status_code < 300:
            _atomic_write(meta / "sitemap.xml.gz", gzip.compress(sitemap_result.body, compresslevel=6, mtime=0))
            for url in _parse_sitemap(sitemap_result.body):
                info = classify_url(url)
                if info.kind == "ignore":
                    continue
                store.connection.execute(
                    "INSERT INTO sitemap_entries(url, kind, seen_at) VALUES (?, ?, ?) "
                    "ON CONFLICT(url) DO UPDATE SET kind = excluded.kind, seen_at = excluded.seen_at",
                    (url, info.kind, utc_now()),
                )
                store.add_url(url, discovered_from=SITEMAP_URL)
                sitemap_count += 1
            store.connection.commit()
        else:
            print(
                f"[警告] sitemap.xml 读取失败，继续依赖页面递归: {sitemap_result.error or sitemap_result.status_code}"
            )
    return parser, sitemap_count


def _prepare_frontier(store: CrawlStore, *, force_refresh: bool, refresh_resources: bool) -> None:
    store.connection.execute("UPDATE frontier SET status = 'pending' WHERE status = 'fetching'")
    store.connection.execute("UPDATE frontier SET status = 'pending' WHERE status = 'failed'")
    store.connection.execute("UPDATE resources SET status = 'pending' WHERE status = 'failed'")
    if force_refresh:
        store.connection.execute(
            "UPDATE frontier SET status = 'pending' WHERE status IN ('done', 'ignored_scope', 'unavailable', 'denied')"
        )
        store.connection.execute(
            """
            UPDATE resources SET status = 'pending'
            WHERE status IN ('done', 'unavailable', 'failed', 'invalid', 'denied', 'skipped_external')
            """
        )
    elif refresh_resources:
        store.connection.execute(
            """
            UPDATE resources SET status = 'pending'
            WHERE status IN ('done', 'unavailable', 'failed', 'invalid', 'denied', 'skipped_external')
            """
        )
    else:
        list_cutoff = (dt.datetime.now(dt.UTC) - dt.timedelta(hours=24)).replace(microsecond=0).isoformat()
        detail_cutoff = (dt.datetime.now(dt.UTC) - dt.timedelta(days=7)).replace(microsecond=0).isoformat()
        store.connection.execute(
            "UPDATE frontier SET status = 'pending' WHERE kind = 'list' AND status = 'done' AND fetched_at < ?",
            (list_cutoff,),
        )
        store.connection.execute(
            "UPDATE frontier SET status = 'pending' WHERE kind = 'detail' AND status = 'done' AND fetched_at < ?",
            (detail_cutoff,),
        )
        store.connection.execute(
            "UPDATE frontier SET status = 'pending' WHERE status = 'unavailable' AND fetched_at < ?",
            (detail_cutoff,),
        )
        store.connection.execute(
            "UPDATE resources SET status = 'pending' WHERE status = 'unavailable' AND fetched_at < ?",
            (detail_cutoff,),
        )
    for url in ROOT_URLS:
        store.add_url(url)
    store.connection.commit()


def _recover_frontier_from_saved_details(store: CrawlStore, output: Path) -> tuple[int, int]:
    """从 v1 原始响应恢复详情分页发现，无需重抓已完成的第一页。"""
    rows = store.connection.execute(
        """
        SELECT page_url, raw_path FROM document_pages
        WHERE page_number = 1 AND pagination_scanned = 0
        ORDER BY page_url
        """
    ).fetchall()
    scanned = 0
    discovered = 0
    for row in rows:
        path = output / row["raw_path"]
        if not path.is_file():
            print(f"[警告] 旧详情页缺少原始响应，无法恢复分页: {row['page_url']}", flush=True)
            continue
        try:
            page = parse_page(gzip.decompress(path.read_bytes()), row["page_url"])
        except (OSError, ValueError) as exc:
            print(f"[警告] 旧详情页原始响应无法解析: {row['page_url']} ({exc})", flush=True)
            continue
        if page.page_type != "detail" or not page.in_scope or not page.title or not page.body_text:
            print(f"[警告] 旧详情页重新解析后不满足正文契约: {row['page_url']}", flush=True)
            continue
        _save_document_page(store, page, row["raw_path"])
        for target in page.target_urls:
            if store.add_url(target, discovered_from=row["page_url"]):
                discovered += 1
            store.add_edge(row["page_url"], target, _relation(row["page_url"], target, "detail"))
        scanned += 1
    store.connection.commit()
    return scanned, discovered


def _crawl_pages(
    store: CrawlStore,
    fetcher: Fetcher,
    output: Path,
    robots: urllib.robotparser.RobotFileParser,
    *,
    max_pages: int,
) -> int:
    processed = 0
    while processed < max_pages:
        row = store.next_page()
        if row is None:
            break
        url = row["url"]
        store.mark_fetching(url)
        if not robots.can_fetch(USER_AGENT, url):
            empty = FetchResult(url, url, None, b"", None, 0, 0, "robots.txt 禁止抓取")
            store.finish_page(url, empty, "denied")
            processed += 1
            continue
        result = fetcher.fetch(url)
        raw_path = _save_raw(output, url, result.body) if result.body else None
        if result.status_code in {404, 410}:
            store.finish_page(url, result, "unavailable", raw_path=raw_path, error=f"HTTP {result.status_code}")
            processed += 1
            continue
        if result.status_code in {401, 403}:
            store.finish_page(url, result, "denied", raw_path=raw_path, error=f"HTTP {result.status_code}")
            processed += 1
            continue
        if not result.status_code or not 200 <= result.status_code < 300:
            store.finish_page(
                url,
                result,
                "failed",
                raw_path=raw_path,
                error=result.error or f"HTTP {result.status_code}",
            )
            processed += 1
            continue
        try:
            page = parse_page(result.body, url)
            for target in page.target_urls:
                store.add_url(target, discovered_from=url, depth=row["depth"] + 1)
                store.add_edge(url, target, _relation(url, target, page.page_type))
            if page.page_type == "detail":
                if not page.in_scope:
                    store.finish_page(url, result, "ignored_scope", raw_path=raw_path)
                elif not page.title or (page.page_number == 1 and not page.body_text):
                    store.finish_page(url, result, "failed", raw_path=raw_path, error="详情页缺少标题或正文")
                else:
                    _save_document_page(store, page, raw_path or "")
                    store.finish_page(url, result, "done", raw_path=raw_path)
            else:
                store.finish_page(url, result, "done", raw_path=raw_path)
        except Exception as exc:  # noqa: BLE001 - 单页失败必须入账并继续
            store.finish_page(url, result, "failed", raw_path=raw_path, error=f"解析失败 {type(exc).__name__}: {exc}")
        processed += 1
        if processed % 25 == 0:
            counts = dict(store.connection.execute("SELECT status, COUNT(*) FROM frontier GROUP BY status").fetchall())
            print(f"[页面] 已处理 {processed}；队列状态 {json_dumps(counts)}", flush=True)
    return processed


def _write_ndjson(path: Path, rows: Iterable[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    with temporary.open("wb") as handle:
        for row in rows:
            handle.write((json_dumps(row) + "\n").encode())
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, path)


def _repair_document_files(store: CrawlStore, output: Path) -> int:
    """把旧版共享去重文件迁移为逐来源文件，避免增量刷新破坏追溯性。"""
    repaired = 0
    for row in store.connection.execute("SELECT * FROM documents ORDER BY source_url").fetchall():
        record = json.loads(row["data_json"])
        parent = Path("content") / record["section"] / _safe_filename(record["category"]["slug"], 60)
        stem = f"{record['record_id']}--{_safe_filename(record.get('title') or 'untitled')}"
        html_rel = parent / f"{stem}.html"
        markdown_rel = parent / f"{stem}.md"
        if (
            row["html_path"] == html_rel.as_posix()
            and row["markdown_path"] == markdown_rel.as_posix()
            and (output / html_rel).is_file()
            and (output / markdown_rel).is_file()
        ):
            continue
        title = html_lib.escape(record.get("title") or "未命名")
        source_url = record["source_url"]
        source = html_lib.escape(source_url, quote=True)
        rendered = (
            '<!doctype html>\n<html lang="zh-CN"><head><meta charset="utf-8">'
            f'<title>{title}</title></head><body><article data-source-url="{source}">'
            f"<h1>{title}</h1>\n{record['body_html']}\n</article></body></html>\n"
        )
        _atomic_write(output / html_rel, rendered.encode())
        markdown = (
            f"# {record.get('title') or '未命名'}\n\n"
            f"- 原始链接：{source_url}\n"
            f"- 栏目：{record['section']}\n"
            f"- 分类：{record['category'].get('title') or record['category']['slug']}\n"
            f"- 作者：{record.get('author') or '未标注'}\n"
            f"- 来源：{record.get('source_name') or '未标注'}\n"
            f"- 发布时间：{record.get('published_at') or '未标注'}\n\n"
            f"{record['body_markdown']}"
        )
        _atomic_write(output / markdown_rel, markdown.encode())
        record["html_path"] = html_rel.as_posix()
        record["markdown_path"] = markdown_rel.as_posix()
        store.connection.execute(
            "UPDATE documents SET html_path = ?, markdown_path = ?, data_json = ? WHERE source_url = ?",
            (html_rel.as_posix(), markdown_rel.as_posix(), json_dumps(record), source_url),
        )
        repaired += 1
    store.connection.commit()
    return repaired


def _export_records(store: CrawlStore, output: Path) -> dict[str, int]:
    repaired = _repair_document_files(store, output)
    resources_by_source: dict[str, list[dict[str, Any]]] = {}
    for item in store.connection.execute(
        """
        SELECT dr.source_url, dr.kind, r.url, r.status, r.local_path, r.sha256,
            r.content_type, r.byte_size
        FROM document_resources dr JOIN resources r ON r.url = dr.resource_url
        ORDER BY dr.source_url, r.url
        """
    ):
        resource = dict(item)
        source_url = resource.pop("source_url")
        resources_by_source.setdefault(source_url, []).append(resource)
    document_count = store.connection.execute("SELECT COUNT(*) FROM documents").fetchone()[0]

    def document_records() -> Iterator[dict[str, Any]]:
        for row in store.connection.execute("SELECT * FROM documents ORDER BY section, category_slug, source_url"):
            record = json.loads(row["data_json"])
            record["resources"] = resources_by_source.get(row["source_url"], [])
            yield record

    _write_ndjson(output / "records/documents.ndjson", document_records())

    page_rows = [dict(row) for row in store.connection.execute("SELECT * FROM frontier ORDER BY url")]
    document_page_rows = [
        dict(row)
        for row in store.connection.execute(
            """
            SELECT page_url, base_url, page_number, page_count, section, category_slug,
                content_sha256, raw_path, extracted_at
            FROM document_pages ORDER BY base_url, page_number
            """
        )
    ]
    page_resource_rows = [
        dict(row)
        for row in store.connection.execute(
            "SELECT page_url, resource_url, kind FROM page_resources ORDER BY page_url, resource_url"
        )
    ]
    edge_count = store.connection.execute("SELECT COUNT(*) FROM edges").fetchone()[0]

    def edge_records() -> Iterator[dict[str, Any]]:
        for row in store.connection.execute("SELECT * FROM edges ORDER BY source_url, target_url, relation"):
            yield dict(row)

    resource_rows = [dict(row) for row in store.connection.execute("SELECT * FROM resources ORDER BY url")]
    _write_ndjson(output / "manifests/pages.ndjson", page_rows)
    _write_ndjson(output / "manifests/document-pages.ndjson", document_page_rows)
    _write_ndjson(output / "manifests/page-resources.ndjson", page_resource_rows)
    _write_ndjson(output / "manifests/links.ndjson", edge_records())
    _write_ndjson(output / "manifests/resources.ndjson", resource_rows)

    failures = [row for row in page_rows if row["status"] == "failed"]
    failures.extend({"entity": "resource", **row} for row in resource_rows if row["status"] == "failed")
    unavailable = [row for row in page_rows if row["status"] in {"unavailable", "denied"}]
    unavailable.extend(
        {"entity": "resource", **row}
        for row in resource_rows
        if row["status"] in {"unavailable", "denied", "invalid", "skipped_external"}
    )
    duplicates = [
        {"source_url": row["source_url"], "duplicate_of": row["duplicate_of"], "content_sha256": row["content_sha256"]}
        for row in store.connection.execute(
            "SELECT source_url, duplicate_of, content_sha256 FROM documents WHERE duplicate_of IS NOT NULL ORDER BY source_url"
        )
    ]
    _write_ndjson(output / "reports/failures.ndjson", failures)
    _write_ndjson(output / "reports/unavailable.ndjson", unavailable)
    _write_ndjson(output / "reports/duplicates.ndjson", duplicates)
    return {
        "documents": document_count,
        "pages": len(page_rows),
        "document_pages": len(document_page_rows),
        "page_resources": len(page_resource_rows),
        "links": edge_count,
        "resources": len(resource_rows),
        "failures": len(failures),
        "unavailable": len(unavailable),
        "duplicates": len(duplicates),
        "repaired_document_files": repaired,
    }


def _percentile(values: list[int], percentile: float) -> int:
    if not values:
        return 0
    ordered = sorted(values)
    index = min(len(ordered) - 1, max(0, round((len(ordered) - 1) * percentile)))
    return ordered[index]


def _detail_pagination_audit(connection: sqlite3.Connection) -> dict[str, Any]:
    page_rows = connection.execute(
        "SELECT page_url, base_url, page_number, page_count FROM document_pages ORDER BY base_url, page_number"
    ).fetchall()
    pages_by_base: dict[str, list[sqlite3.Row]] = {}
    for row in page_rows:
        pages_by_base.setdefault(row["base_url"], []).append(row)
    frontier = {
        row["url"]: row["status"]
        for row in connection.execute("SELECT url, status FROM frontier WHERE kind = 'detail'")
    }
    documents = {
        row["source_url"]: json.loads(row["data_json"])
        for row in connection.execute("SELECT source_url, data_json FROM documents")
    }

    gaps: list[dict[str, Any]] = []
    missing_page_count = 0
    frontier_missing_count = 0
    frontier_non_done_count = 0
    unmaterialized_count = 0
    paginated_document_count = 0
    for base_url, rows in sorted(pages_by_base.items()):
        page_count = max(int(row["page_count"]) for row in rows)
        if page_count > 1:
            paginated_document_count += 1
        actual_numbers = {int(row["page_number"]) for row in rows}
        expected_numbers = set(range(1, page_count + 1))
        missing_numbers = sorted(expected_numbers - actual_numbers)
        expected_urls = [_detail_page_url(base_url, number) for number in range(1, page_count + 1)]
        missing_frontier_urls = [url for url in expected_urls if url not in frontier]
        non_done_frontier_urls = [url for url in expected_urls if url in frontier and frontier[url] != "done"]
        document = documents.get(base_url)
        document_page_numbers = [int(item.get("page_number", 0)) for item in (document or {}).get("source_pages", [])]
        document_complete = bool(
            document
            and int(document.get("page_count") or 0) == page_count
            and document_page_numbers == list(range(1, page_count + 1))
        )
        missing_page_count += len(missing_numbers)
        frontier_missing_count += len(missing_frontier_urls)
        frontier_non_done_count += len(non_done_frontier_urls)
        if not document_complete:
            unmaterialized_count += 1
        if missing_numbers or missing_frontier_urls or non_done_frontier_urls or not document_complete:
            gaps.append(
                {
                    "base_url": base_url,
                    "expected_page_count": page_count,
                    "stored_page_numbers": sorted(actual_numbers),
                    "missing_page_numbers": missing_numbers,
                    "missing_frontier_urls": missing_frontier_urls,
                    "non_done_frontier_urls": non_done_frontier_urls,
                    "logical_document_complete": document_complete,
                }
            )
    return {
        "document_page_count": len(page_rows),
        "logical_document_count": len(pages_by_base),
        "paginated_document_count": paginated_document_count,
        "incomplete_document_count": len(gaps),
        "missing_page_count": missing_page_count,
        "frontier_missing_count": frontier_missing_count,
        "frontier_non_done_count": frontier_non_done_count,
        "unmaterialized_count": unmaterialized_count,
        "gaps": gaps[:200],
    }


def _raw_detail_continuations_without_frontier(
    connection: sqlite3.Connection,
    output: Path,
) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    """用独立宽松 href 规则检查原始首页，避免分类器与 validator 共因失明。"""
    frontier_urls = {row[0] for row in connection.execute("SELECT url FROM frontier")}
    missing: list[dict[str, str]] = []
    errors: list[dict[str, str]] = []
    rows = connection.execute(
        """
        SELECT p.page_url, p.raw_path
        FROM document_pages p
        WHERE p.page_number = 1
        ORDER BY p.page_url
        """
    ).fetchall()
    for row in rows:
        path = output / row["raw_path"]
        if not path.is_file():
            errors.append({"source_url": row["page_url"], "error": f"缺少原始响应 {row['raw_path']}"})
            continue
        try:
            text = gzip.decompress(path.read_bytes()).decode("utf-8", errors="replace")
        except OSError as exc:
            errors.append({"source_url": row["page_url"], "error": f"gzip 读取失败: {exc}"})
            continue
        for match in re.finditer(r"(?i)href\s*=\s*['\"]([^'\"<>]+)['\"]", text):
            target = canonicalize_url(match.group(1), row["page_url"])
            target_path = urllib.parse.urlsplit(target).path
            is_current = re.fullmatch(r"/(?:article|book)/\d+_\d+\.html", target_path)
            is_legacy = re.fullmatch(r"/(?:jichu|dianji)/[^/]+/\d+_\d+\.html", target_path)
            if (is_current or is_legacy) and target not in frontier_urls:
                missing.append({"source_url": row["page_url"], "target_url": target})
    unique = {(item["source_url"], item["target_url"]): item for item in missing}
    return [unique[key] for key in sorted(unique)], errors


def validate_corpus(output: Path, *, verify_checksums: bool = False) -> dict[str, Any]:
    database = output / "crawl.sqlite3"
    if not database.exists():
        raise FileNotFoundError(f"缺少状态库: {database}")
    connection = sqlite3.connect(database)
    connection.row_factory = sqlite3.Row
    integrity = connection.execute("PRAGMA integrity_check").fetchone()[0]
    page_status = dict(connection.execute("SELECT status, COUNT(*) FROM frontier GROUP BY status").fetchall())
    resource_status = dict(connection.execute("SELECT status, COUNT(*) FROM resources GROUP BY status").fetchall())
    section_counts = dict(connection.execute("SELECT section, COUNT(*) FROM documents GROUP BY section").fetchall())
    missing_files = []
    for row in connection.execute("SELECT source_url, html_path, markdown_path FROM documents"):
        for key in ("html_path", "markdown_path"):
            if not (output / row[key]).is_file():
                missing_files.append({"source_url": row["source_url"], "path": row[key]})
    for row in connection.execute("SELECT url, local_path FROM resources WHERE status = 'done'"):
        if not row["local_path"] or not (output / row["local_path"]).is_file():
            missing_files.append({"resource_url": row["url"], "path": row["local_path"]})
    orphan_edges = connection.execute(
        "SELECT COUNT(*) FROM edges e LEFT JOIN frontier f ON f.url = e.target_url WHERE f.url IS NULL"
    ).fetchone()[0]
    invalid_duplicate_aliases = connection.execute(
        """
        SELECT COUNT(*)
        FROM documents d
        LEFT JOIN documents canonical ON canonical.source_url = d.duplicate_of
        WHERE d.duplicate_of IS NOT NULL
          AND (
              canonical.source_url IS NULL
              OR canonical.content_sha256 <> d.content_sha256
              OR canonical.duplicate_of IS NOT NULL
          )
        """
    ).fetchone()[0]
    expected_duplicate_aliases = connection.execute(
        """
        SELECT COALESCE(SUM(item_count - 1), 0)
        FROM (SELECT COUNT(*) AS item_count FROM documents GROUP BY content_sha256 HAVING COUNT(*) > 1)
        """
    ).fetchone()[0]
    stored_duplicate_aliases = connection.execute(
        "SELECT COUNT(*) FROM documents WHERE duplicate_of IS NOT NULL"
    ).fetchone()[0]
    missing_page_records = connection.execute(
        """
        SELECT COUNT(*) FROM frontier f LEFT JOIN document_pages p ON p.page_url = f.url
        WHERE f.kind = 'detail' AND f.status = 'done' AND p.page_url IS NULL
        """
    ).fetchone()[0]
    unscanned_saved_details = connection.execute(
        "SELECT COUNT(*) FROM document_pages WHERE page_number = 1 AND pagination_scanned = 0"
    ).fetchone()[0]
    detail_pagination = _detail_pagination_audit(connection)
    raw_missing_continuations, raw_scan_errors = _raw_detail_continuations_without_frontier(connection, output)
    missing_sitemap = connection.execute(
        """
        SELECT COUNT(*) FROM sitemap_entries s LEFT JOIN frontier f ON f.url = s.url
        WHERE f.url IS NULL
        """
    ).fetchone()[0]
    unavailable_lists = connection.execute(
        "SELECT COUNT(*) FROM frontier WHERE kind = 'list' AND status IN ('unavailable', 'denied')"
    ).fetchone()[0]
    category_counts: dict[str, int] = {}
    missing_categories: dict[str, list[str]] = {}
    for section, expected in EXPECTED_CATEGORY_SLUGS.items():
        discovered = {
            row[0]
            for row in connection.execute(
                """
                SELECT category_slug FROM frontier
                WHERE kind = 'list' AND section_hint = ? AND category_slug IS NOT NULL
                """,
                (section,),
            )
        }
        category_counts[section] = len(discovered)
        missing_categories[section] = sorted(expected - discovered)
    elapsed = [row[0] for row in connection.execute("SELECT elapsed_ms FROM frontier WHERE elapsed_ms IS NOT NULL")]
    content_bytes = sum(path.stat().st_size for path in output.rglob("*") if path.is_file())
    checksums_ok = True
    checksum_errors = []
    checksum_path = output / "files.sha256"
    if verify_checksums and checksum_path.exists():
        for line in checksum_path.read_text(encoding="utf-8").splitlines():
            digest, relpath = line.split("  ", 1)
            path = output / relpath
            if not path.is_file() or sha256_bytes(path.read_bytes()) != digest:
                checksums_ok = False
                checksum_errors.append(relpath)
    hard_failures = {
        "sqlite_integrity": integrity != "ok",
        "pending_or_fetching_pages": page_status.get("pending", 0) + page_status.get("fetching", 0),
        "failed_pages": page_status.get("failed", 0),
        "pending_resources": resource_status.get("pending", 0),
        "failed_resources": resource_status.get("failed", 0),
        "missing_sections": [section for section in ("jichu", "dianji") if section_counts.get(section, 0) == 0],
        "missing_files": len(missing_files),
        "orphan_edges": orphan_edges,
        "invalid_duplicate_aliases": invalid_duplicate_aliases,
        "duplicate_alias_count_mismatch": abs(expected_duplicate_aliases - stored_duplicate_aliases),
        "done_details_without_page_records": missing_page_records,
        "incomplete_detail_documents": detail_pagination["incomplete_document_count"],
        "detail_page_sequence_gaps": detail_pagination["missing_page_count"],
        "detail_pages_missing_from_frontier": detail_pagination["frontier_missing_count"],
        "detail_pages_not_done": detail_pagination["frontier_non_done_count"],
        "unmaterialized_detail_documents": detail_pagination["unmaterialized_count"],
        "unscanned_saved_details": unscanned_saved_details,
        "raw_detail_links_without_frontier": len(raw_missing_continuations),
        "raw_detail_scan_errors": len(raw_scan_errors),
        "sitemap_entries_without_frontier": missing_sitemap,
        "unavailable_list_pages": unavailable_lists,
        "missing_expected_categories": {section: slugs for section, slugs in missing_categories.items() if slugs},
        "checksum_errors": len(checksum_errors),
    }
    passed = not any(bool(value) for value in hard_failures.values()) and checksums_ok
    unavailable_count = page_status.get("unavailable", 0) + page_status.get("denied", 0)
    unavailable_count += sum(
        resource_status.get(key, 0) for key in ("unavailable", "denied", "invalid", "skipped_external")
    )
    report = {
        "schema_version": SCHEMA_VERSION,
        "checked_at": utc_now(),
        "decision": "PASS_WITH_UNAVAILABLE" if passed and unavailable_count else ("PASS" if passed else "FAIL"),
        "hard_failures": hard_failures,
        "page_status": page_status,
        "resource_status": resource_status,
        "section_document_counts": section_counts,
        "root_category_counts": category_counts,
        "document_count": sum(section_counts.values()),
        "duplicate_aliases": {
            "expected": expected_duplicate_aliases,
            "stored": stored_duplicate_aliases,
            "invalid": invalid_duplicate_aliases,
        },
        "detail_pagination": detail_pagination,
        "raw_detail_links_without_frontier": raw_missing_continuations[:200],
        "raw_detail_scan_error_details": raw_scan_errors[:200],
        "unavailable_count": unavailable_count,
        "missing_file_details": missing_files[:100],
        "checksum_error_details": checksum_errors[:100],
        "performance": {
            "page_latency_ms_p50": int(statistics.median(elapsed)) if elapsed else 0,
            "page_latency_ms_p95": _percentile(elapsed, 0.95),
            "page_latency_ms_max": max(elapsed, default=0),
            "output_bytes": content_bytes,
        },
    }
    connection.close()
    return report


def _build_checksums(output: Path) -> int:
    rows = []
    for path in sorted(output.rglob("*")):
        if not path.is_file() or path.name == "files.sha256":
            continue
        rows.append(f"{sha256_bytes(path.read_bytes())}  {path.relative_to(output).as_posix()}\n")
    _atomic_write(output / "files.sha256", "".join(rows).encode())
    return len(rows)


def _write_output_readme(output: Path) -> None:
    text = """# 算准网基础/典籍本地语料

本目录由 `scripts/suanzhun-corpus-crawl.py` 生成，UTF-8 编码。`crawl.sqlite3` 是增量状态与追溯关系真相源；
`records/` 为结构化正文，`content/` 为 HTML/Markdown，`media/` 为内容寻址资源，`manifests/` 与 `reports/` 用于复核。

```text
content/<section>/<category>/   按逻辑文章聚合的 HTML 与 Markdown 正文
media/<sha256-prefix>/          内容寻址媒体
raw/pages/                      URL 哈希命名的 gzip 原始响应
records/documents.ndjson        一篇文章一条的聚合正文记录
manifests/document-pages.ndjson 每个物理详情页的来源、顺序、原始响应与正文哈希
manifests/page-resources.ndjson 物理详情页到媒体/附件的追溯映射
manifests/                      页面、链接、资源及运行清单
reports/                        完整性、重复、失败与不可用明细
files.sha256                    全目录文件校验清单
```

分页文章在 `records/documents.ndjson` 中保持一篇一条，并按 `source_pages[].page_number` 聚合；
清噪后为空的可访问末页仍保留物理页证据，但不会把分页导航注入正文。

```bash
.venv/bin/python scripts/suanzhun-corpus-crawl.py \
  --output infra/runtime/local-state/exports/suanzhun-corpus \
  --allow-external-media
.venv/bin/python scripts/suanzhun-corpus-crawl.py \
  --output infra/runtime/local-state/exports/suanzhun-corpus \
  --validate-only
```

该语料只作来源可追溯的内部研究参考；版权归原站及原作者，未完成人工版权审查前不得作为生产数据、公开再发布或模型训练授权依据。
重复执行同一命令会复用已完成页面，只刷新到期列表/详情并重试失败项；使用 `--force-refresh` 可强制刷新。
代理 DNS 把已核验公网媒体映射为保留地址时，才用 `--external-media-host <host>` 显式放行，不得使用通配主机。
"""
    _atomic_write(output / "README.md", text.encode())


def run_crawl(args: argparse.Namespace) -> int:
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    if args.validate_only:
        report = validate_corpus(output, verify_checksums=True)
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0 if report["decision"].startswith("PASS") else 2

    store = CrawlStore(output / "crawl.sqlite3")
    run_id = dt.datetime.now(dt.UTC).strftime("%Y%m%dT%H%M%S%fZ")
    options = vars(args).copy()
    options["output"] = str(output)
    store.connection.execute(
        "INSERT INTO runs(run_id, started_at, status, options_json) VALUES (?, ?, 'running', ?)",
        (run_id, utc_now(), json_dumps(options)),
    )
    _prepare_frontier(
        store,
        force_refresh=args.force_refresh,
        refresh_resources=args.refresh_resources,
    )
    recovered_pages, recovered_urls = _recover_frontier_from_saved_details(store, output)
    if recovered_pages:
        print(
            f"[迁移] 重新解析旧详情首页 {recovered_pages} 页，恢复待抓 URL {recovered_urls} 条",
            flush=True,
        )
    fetcher = Fetcher(
        delay_seconds=args.delay_seconds,
        timeout_seconds=args.timeout_seconds,
        max_attempts=args.max_attempts,
        max_page_bytes=args.max_page_bytes,
    )
    exit_code = 2
    try:
        robots, sitemap_count = _load_robots_and_sitemap(store, fetcher, output)
        print(f"[发现] sitemap 纳入目标 URL {sitemap_count} 条", flush=True)
        page_count = _crawl_pages(store, fetcher, output, robots, max_pages=args.max_pages)
        materialized_documents, incomplete_documents = _materialize_all_documents(store, output)
        resource_count = _fetch_resources(
            store,
            fetcher,
            output,
            robots,
            allow_external=args.allow_external_media,
            external_host_allowlist=set(args.external_media_host),
            max_resource_bytes=args.max_resource_bytes,
            max_resources=args.max_resources,
        )
        counts = _export_records(store, output)
        _write_output_readme(output)
        store.connection.execute(
            "UPDATE runs SET finished_at = ?, status = 'finished', summary_json = ? WHERE run_id = ?",
            (
                utc_now(),
                json_dumps(
                    {
                        **counts,
                        "processed_pages": page_count,
                        "processed_resources": resource_count,
                        "http_requests": fetcher.request_count,
                        "http_retries": fetcher.retry_count,
                        "recovered_saved_pages": recovered_pages,
                        "recovered_urls": recovered_urls,
                        "materialized_documents": materialized_documents,
                        "incomplete_documents": incomplete_documents,
                    }
                ),
                run_id,
            ),
        )
        store.connection.commit()
        preliminary = validate_corpus(output)
        _write_json(output / "reports/completeness.json", preliminary)
        manifest = {
            "schema_version": SCHEMA_VERSION,
            "generated_at": utc_now(),
            "source": {
                "site": BASE_URL,
                "roots": list(ROOT_URLS),
                "robots": ROBOTS_URL,
                "sitemap": SITEMAP_URL,
            },
            "scope": ["基础", "典籍"],
            "counts": counts,
            "run": {
                "run_id": run_id,
                "http_requests": fetcher.request_count,
                "http_retries": fetcher.retry_count,
                "processed_pages": page_count,
                "processed_resources": resource_count,
                "recovered_saved_pages": recovered_pages,
                "recovered_urls": recovered_urls,
                "materialized_documents": materialized_documents,
                "incomplete_documents": incomplete_documents,
            },
            "completeness_decision": preliminary["decision"],
            "rights_boundary": {
                "purpose": "reference_only",
                "review_required": True,
                "distribution_not_allowed": True,
            },
        }
        _write_json(output / "manifest.json", manifest)
    except BaseException as exc:
        with contextlib.suppress(sqlite3.Error):
            store.connection.execute(
                "UPDATE runs SET finished_at = ?, status = 'failed', summary_json = ? WHERE run_id = ?",
                (utc_now(), json_dumps({"error_type": type(exc).__name__}), run_id),
            )
            store.connection.commit()
        raise
    finally:
        fetcher.close()
        store.close()

    checksum_count = _build_checksums(output)
    report = validate_corpus(output, verify_checksums=True)
    _write_json(output / "reports/completeness.json", report)
    # 完整性报告变化后重新生成校验清单，保证最终目录自洽。
    checksum_count = _build_checksums(output)
    report = validate_corpus(output, verify_checksums=True)
    print(
        f"[完成] 决策={report['decision']} 文档={report['document_count']} "
        f"不可用={report['unavailable_count']} 校验文件={checksum_count}",
        flush=True,
    )
    exit_code = 0 if report["decision"].startswith("PASS") else 2
    return exit_code


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("infra/runtime/local-state/exports/suanzhun-corpus"),
        help="输出目录",
    )
    parser.add_argument("--validate-only", action="store_true", help="只校验现有输出，不访问网络")
    parser.add_argument("--force-refresh", action="store_true", help="强制重新抓取已完成页面与资源")
    parser.add_argument("--refresh-resources", action="store_true", help="只重新排队已发现资源，不刷新页面")
    parser.add_argument("--allow-external-media", action="store_true", help="下载正文引用的公开外站媒体")
    parser.add_argument(
        "--external-media-host",
        action="append",
        default=[],
        help="显式允许的外部媒体主机；可重复传入，用于受控代理环境",
    )
    parser.add_argument("--delay-seconds", type=float, default=0.35, help="同一下载器请求间隔秒数")
    parser.add_argument("--timeout-seconds", type=float, default=20.0, help="单次请求超时秒数")
    parser.add_argument("--max-attempts", type=int, default=4, help="单个请求最大尝试次数")
    parser.add_argument("--max-pages", type=int, default=10000, help="单次最多处理页面数")
    parser.add_argument("--max-resources", type=int, default=10000, help="单次最多处理资源数")
    parser.add_argument("--max-page-bytes", type=int, default=10 * 1024 * 1024, help="页面响应体上限")
    parser.add_argument("--max-resource-bytes", type=int, default=50 * 1024 * 1024, help="资源响应体上限")
    return parser


def main() -> int:
    args = build_argument_parser().parse_args()
    if args.delay_seconds < 0 or args.max_attempts < 1 or args.max_pages < 1 or args.max_resources < 1:
        raise SystemExit("请求间隔不得为负，重试/页面/资源上限必须为正整数")
    return run_crawl(args)


if __name__ == "__main__":
    raise SystemExit(main())
