from __future__ import annotations

import gzip
import importlib.util
import json
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT_PATH = ROOT / "scripts" / "suanzhun-corpus-crawl.py"


def _load_module():
    spec = importlib.util.spec_from_file_location("suanzhun_corpus_crawl", SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"无法加载抓取器模块: {SCRIPT_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _persist_page(crawler, store, output, page, raw_path):
    crawler._save_document_page(store, page, raw_path)
    crawler._materialize_document(store, output, page.base_url or page.source_url)
    crawler._rebuild_duplicate_aliases(store)
    store.connection.commit()


def test_url_classification_and_canonicalization_cover_current_and_legacy_routes():
    crawler = _load_module()

    assert crawler.canonicalize_url("http://SUANZHUN.net/jichu/#top") == "https://www.suanzhun.net/jichu/"
    assert crawler.canonicalize_url("https://www.suanzhun.net/book/3030.html?utm_source=test") == (
        "https://www.suanzhun.net/book/3030.html"
    )

    assert crawler.classify_url("https://www.suanzhun.net/jichu/").kind == "list"
    assert crawler.classify_url("https://www.suanzhun.net/jichu/changshi/index_15.html").kind == "list"
    assert crawler.classify_url("https://www.suanzhun.net/article/3032.html").kind == "detail"
    assert crawler.classify_url("https://www.suanzhun.net/book/3030.html").section_hint == "dianji"
    assert crawler.classify_url("https://www.suanzhun.net/dianji/ditiansui/361.html").kind == "detail"
    assert crawler.classify_url("https://www.suanzhun.net/bazipaipan/").kind == "ignore"

    current_page = crawler.classify_url("https://www.suanzhun.net/book/2163_38.html")
    assert current_page.kind == "detail"
    assert current_page.base_url == "https://www.suanzhun.net/book/2163.html"
    assert current_page.page_number == 38

    article_page = crawler.classify_url("https://www.suanzhun.net/article/2488_2.html")
    assert article_page.kind == "detail"
    assert article_page.base_url == "https://www.suanzhun.net/article/2488.html"
    assert article_page.page_number == 2

    legacy_page = crawler.classify_url("https://www.suanzhun.net/dianji/jinxiangmishu/208_7.html")
    assert legacy_page.kind == "detail"
    assert legacy_page.base_url == "https://www.suanzhun.net/dianji/jinxiangmishu/208.html"
    assert legacy_page.page_number == 7


def test_list_page_discovers_categories_pagination_and_details_without_other_columns():
    crawler = _load_module()
    html = b"""
    <!doctype html><html><body>
      <nav>
        <a href="/jichu/changshi/">\xe5\xb8\xb8\xe8\xaf\x86</a>
        <a href="/dianji/ditiansui/">\xe6\xbb\xb4\xe5\xa4\xa9\xe9\xab\x93</a>
        <a href="/bazipaipan/">\xe6\x8e\x92\xe7\x9b\x98</a>
      </nav>
      <article class="box">
        <div class="list"><h2><a href="/article/12.html">A</a></h2></div>
        <div class="list"><h2><a href="/book/13.html">B</a></h2></div>
        <div class="posts-nav"><a class="page-numbers" href="index_2.html">2</a></div>
      </article>
    </body></html>
    """

    page = crawler.parse_page(html, "https://www.suanzhun.net/jichu/")

    assert page.page_type == "list"
    assert set(page.target_urls) == {
        "https://www.suanzhun.net/article/12.html",
        "https://www.suanzhun.net/book/13.html",
        "https://www.suanzhun.net/dianji/ditiansui/",
        "https://www.suanzhun.net/jichu/changshi/",
        "https://www.suanzhun.net/jichu/index_2.html",
    }
    assert "https://www.suanzhun.net/bazipaipan/" not in page.target_urls


def test_detail_extraction_keeps_semantics_and_removes_navigation_and_recommendations():
    crawler = _load_module()
    html = """
    <!doctype html><html><head>
      <meta name="description" content="正文摘要">
    </head><body>
      <article class="box">
        <div class="breadcrumbs">
          <a href="/">首页</a> &gt;
          <a href="/jichu/">基础</a> &gt;
          <a href="/jichu/caiguan/">财官</a> &gt; 正文
        </div>
        <h1 class="singletitle">官杀混杂测试</h1>
        <div align="center">日期:2026.07.14 发布者:算准网</div>
        <div class="content-text">
          开场<br><br>
          <h2>第一节</h2>
          <p>段落 <strong>重点</strong>。</p>
          <blockquote>原文引用</blockquote>
          <ul><li>条目一</li><li>条目二</li></ul>
          <table><tr><th>干</th><th>支</th></tr><tr><td>甲</td><td>子</td></tr></table>
          <img src="/uploads/chart.png" alt="命盘图">
          <a href="/uploads/source.pdf">附件</a>
          <p class="p2"></p>
          <div class="bdf"><a href="/article/11.html">上一篇</a></div>
          <div class="related"><h3>相关文章</h3><a href="/article/14.html">推荐文</a></div>
        </div>
      </article>
    </body></html>
    """.encode()

    page = crawler.parse_page(html, "https://www.suanzhun.net/article/12.html")

    assert page.page_type == "detail"
    assert page.in_scope is True
    assert page.section == "jichu"
    assert page.category_slug == "caiguan"
    assert page.category_title == "财官"
    assert page.title == "官杀混杂测试"
    assert page.publisher == "算准网"
    assert page.published_at == "2026-07-14"
    assert page.description == "正文摘要"
    assert page.headings == [{"level": 2, "text": "第一节"}]

    assert "第一节" in page.body_html
    assert "<table>" in page.body_html
    assert "命盘图" in page.body_html
    assert "上一篇" not in page.body_html
    assert "相关文章" not in page.body_html
    assert "推荐文" not in page.body_text
    assert "## 第一节" in page.body_markdown
    assert "- 条目一" in page.body_markdown
    assert "| 干 | 支 |" in page.body_markdown

    assert page.media_urls == ["https://www.suanzhun.net/uploads/chart.png"]
    assert page.attachment_urls == ["https://www.suanzhun.net/uploads/source.pdf"]
    assert "https://www.suanzhun.net/article/11.html" in page.target_urls
    assert "https://www.suanzhun.net/article/14.html" in page.target_urls


def test_detail_pagination_expands_hidden_intermediate_pages_and_keeps_logical_identity():
    crawler = _load_module()
    html = """
    <article class="box">
      <div class="breadcrumbs"><a href="/">首页</a> &gt; <a href="/dianji/">典籍</a> &gt;
        <a href="/dianji/qitadanpian/">其他单篇</a> &gt; 正文</div>
      <h1 class="singletitle">多页正文</h1>
      <div class="content-text">第一页正文</div>
      <div class="posts-nav">
        <span>1/6</span>
        <a href="/book/2163_2.html">2</a>
        <a href="/book/2163_3.html">3</a>
        <a href="/book/2163_6.html">6</a>
      </div>
    </article>
    """.encode()

    page = crawler.parse_page(html, "https://www.suanzhun.net/book/2163.html")

    assert page.base_url == "https://www.suanzhun.net/book/2163.html"
    assert page.page_number == 1
    assert page.page_count == 6
    assert {f"https://www.suanzhun.net/book/2163_{number}.html" for number in range(2, 7)}.issubset(page.target_urls)
    assert page.record_id == "book-2163"

    continuation = crawler.parse_page(
        html.replace(b"1/6", b"2/6"),
        "https://www.suanzhun.net/book/2163_2.html",
    )
    assert continuation.base_url == page.base_url
    assert continuation.page_number == 2
    assert continuation.page_count == 6
    assert continuation.record_id == page.record_id


def test_metadata_parser_does_not_read_author_labels_from_the_article_body():
    crawler = _load_module()
    html = """
    <article class="box">
      <div class="breadcrumbs"><a href="/">首页</a> &gt; <a href="/dianji/">典籍</a> &gt;
        <a href="/dianji/qitadanpian/">其他单篇</a> &gt; 正文</div>
      <h1 class="singletitle">正文伪元数据</h1>
      <div align="center">日期:2026.07.15 来源:算准网</div>
      <div class="content-text">
        <p>作者：李虚中是正文讨论对象，不是本页署名。</p>
      </div>
    </article>
    """.encode()

    page = crawler.parse_page(html, "https://www.suanzhun.net/book/42.html")

    assert page.author is None
    assert page.publisher == "算准网"
    assert page.source_name == "算准网"


def test_detail_scope_uses_breadcrumbs_instead_of_assuming_every_article_is_target():
    crawler = _load_module()
    html = """
    <article class="box">
      <div class="breadcrumbs"><a href="/">首页</a> &gt; <a href="/other/">其它</a> &gt; 正文</div>
      <h1 class="singletitle">越界文章</h1>
      <div class="content-text">不应纳入</div>
    </article>
    """.encode()

    page = crawler.parse_page(html, "https://www.suanzhun.net/article/99.html")

    assert page.page_type == "detail"
    assert page.in_scope is False
    assert page.section is None


def test_content_paths_are_deterministic_and_windows_safe():
    crawler = _load_module()
    html = """
    <article class="box">
      <div class="breadcrumbs"><a href="/">首页</a> &gt; <a href="/dianji/">典籍</a> &gt;
        <a href="/dianji/ditiansui/">滴天髓</a> &gt; 正文</div>
      <h1 class="singletitle">滴天髓：甲/乙？*</h1>
      <div class="content-text">正文</div>
    </article>
    """.encode()
    page = crawler.parse_page(html, "https://www.suanzhun.net/book/42.html")

    html_path, markdown_path = crawler.build_content_relpaths(page)

    assert html_path.parent.as_posix() == "content/dianji/ditiansui"
    assert html_path.suffix == ".html"
    assert markdown_path.suffix == ".md"
    assert not any(char in html_path.name for char in '<>:"/\\|?*')
    assert html_path.stem.startswith("book-42--")


def test_incremental_refresh_never_marks_a_document_as_its_own_duplicate(tmp_path):
    crawler = _load_module()
    html = """
    <article class="box">
      <div class="breadcrumbs"><a href="/">首页</a> &gt; <a href="/jichu/">基础</a> &gt;
        <a href="/jichu/changshi/">常识</a> &gt; 正文</div>
      <h1 class="singletitle">增量刷新</h1>
      <div class="content-text">稳定正文</div>
    </article>
    """.encode()
    page = crawler.parse_page(html, "https://www.suanzhun.net/article/42.html")
    store = crawler.CrawlStore(tmp_path / "crawl.sqlite3")
    try:
        _persist_page(crawler, store, tmp_path, page, "raw/pages/example.html.gz")
        _persist_page(crawler, store, tmp_path, page, "raw/pages/example.html.gz")
        row = store.connection.execute(
            "SELECT duplicate_of FROM documents WHERE source_url = ?", (page.source_url,)
        ).fetchone()
        assert row["duplicate_of"] is None

        duplicate_page = crawler.parse_page(html, "https://www.suanzhun.net/article/43.html")
        _persist_page(crawler, store, tmp_path, duplicate_page, "raw/pages/duplicate.html.gz")
        rows = store.connection.execute(
            "SELECT source_url, duplicate_of, html_path FROM documents ORDER BY source_url"
        ).fetchall()
        assert rows[1]["duplicate_of"] == page.source_url
        assert rows[0]["html_path"] != rows[1]["html_path"]

        _persist_page(crawler, store, tmp_path, page, "raw/pages/example.html.gz")
        rows = store.connection.execute("SELECT source_url, duplicate_of FROM documents ORDER BY source_url").fetchall()
        assert rows[0]["duplicate_of"] is None
        assert rows[1]["duplicate_of"] == rows[0]["source_url"]
    finally:
        store.close()


def test_paginated_detail_pages_are_materialized_as_one_ordered_logical_document(tmp_path):
    crawler = _load_module()

    def parse(number: int, body: str):
        suffix = "" if number == 1 else f"_{number}"
        html = f"""
        <article class="box">
          <div class="breadcrumbs"><a href="/">首页</a> &gt; <a href="/dianji/">典籍</a> &gt;
            <a href="/dianji/qitadanpian/">其他单篇</a> &gt; 正文</div>
          <h1 class="singletitle">聚合测试</h1>
          <div align="center">日期:2026.07.15 来源:算准网</div>
          <div class="content-text">{body}</div>
          <div class="posts-nav"><span>{number}/3</span><a href="/book/88_3.html">3</a></div>
        </article>
        """.encode()
        return crawler.parse_page(html, f"https://www.suanzhun.net/book/88{suffix}.html")

    store = crawler.CrawlStore(tmp_path / "crawl.sqlite3")
    try:
        _persist_page(crawler, store, tmp_path, parse(1, "第一页"), "raw/pages/1.html.gz")
        assert store.connection.execute("SELECT COUNT(*) FROM documents").fetchone()[0] == 0

        _persist_page(crawler, store, tmp_path, parse(3, "第三页"), "raw/pages/3.html.gz")
        assert store.connection.execute("SELECT COUNT(*) FROM documents").fetchone()[0] == 0

        _persist_page(crawler, store, tmp_path, parse(2, "第二页"), "raw/pages/2.html.gz")
        row = store.connection.execute("SELECT * FROM documents").fetchone()
        record = crawler.json.loads(row["data_json"])

        assert row["source_url"] == "https://www.suanzhun.net/book/88.html"
        assert store.connection.execute("SELECT COUNT(*) FROM document_pages").fetchone()[0] == 3
        assert store.connection.execute("SELECT COUNT(*) FROM documents").fetchone()[0] == 1
        assert record["page_count"] == 3
        assert [item["page_number"] for item in record["source_pages"]] == [1, 2, 3]
        assert [item["source_url"] for item in record["source_pages"]] == [
            "https://www.suanzhun.net/book/88.html",
            "https://www.suanzhun.net/book/88_2.html",
            "https://www.suanzhun.net/book/88_3.html",
        ]
        assert record["body_text"].index("第一页") < record["body_text"].index("第二页")
        assert record["body_text"].index("第二页") < record["body_text"].index("第三页")
    finally:
        store.close()


def test_empty_final_source_page_is_preserved_after_navigation_noise_is_removed(tmp_path):
    crawler = _load_module()
    base_html = """
    <article class="box">
      <div class="breadcrumbs"><a href="/">首页</a> &gt; <a href="/dianji/">典籍</a> &gt;
        <a href="/dianji/qitadanpian/">其他单篇</a> &gt; 正文</div>
      <h1 class="singletitle">站点空末页</h1>
      <div class="content-text">真实正文</div>
      <div class="posts-nav"><span>1/2</span><a href="/book/90_2.html">2</a></div>
    </article>
    """.encode()
    final_html = """
    <article class="box">
      <div class="breadcrumbs"><a href="/">首页</a> &gt; <a href="/dianji/">典籍</a> &gt;
        <a href="/dianji/qitadanpian/">其他单篇</a> &gt; 正文</div>
      <h1 class="singletitle">站点空末页</h1>
      <div class="content-text">
        <p class="p2"><a title="Page">2/2</a><div class="bdf">上一篇</div></p>
      </div>
    </article>
    """.encode()
    first = crawler.parse_page(base_html, "https://www.suanzhun.net/book/90.html")
    final = crawler.parse_page(final_html, "https://www.suanzhun.net/book/90_2.html")
    assert final.page_number == 2
    assert final.page_count == 2
    assert final.body_text == ""

    store = crawler.CrawlStore(tmp_path / "crawl.sqlite3")
    try:
        _persist_page(crawler, store, tmp_path, first, "raw/pages/1.html.gz")
        _persist_page(crawler, store, tmp_path, final, "raw/pages/2.html.gz")
        record = json.loads(store.connection.execute("SELECT data_json FROM documents").fetchone()[0])
        assert record["page_count"] == 2
        assert len(record["source_pages"]) == 2
        assert record["body_text"] == "真实正文"
    finally:
        store.close()


def test_validator_rejects_a_missing_detail_continuation_page(tmp_path):
    crawler = _load_module()

    def parse(number: int):
        suffix = "" if number == 1 else f"_{number}"
        html = f"""
        <article class="box">
          <div class="breadcrumbs"><a href="/">首页</a> &gt; <a href="/dianji/">典籍</a> &gt;
            <a href="/dianji/qitadanpian/">其他单篇</a> &gt; 正文</div>
          <h1 class="singletitle">断层测试</h1>
          <div class="content-text">第 {number} 页</div>
          <div class="posts-nav"><span>{number}/3</span><a href="/book/99_3.html">3</a></div>
        </article>
        """.encode()
        return crawler.parse_page(html, f"https://www.suanzhun.net/book/99{suffix}.html")

    store = crawler.CrawlStore(tmp_path / "crawl.sqlite3")
    try:
        for number in (1, 3):
            page = parse(number)
            _persist_page(crawler, store, tmp_path, page, f"raw/pages/{number}.html.gz")
            store.add_url(page.source_url)
            store.connection.execute(
                "UPDATE frontier SET status = 'done', raw_path = ? WHERE url = ?",
                (f"raw/pages/{number}.html.gz", page.source_url),
            )
        store.connection.commit()
    finally:
        store.close()

    report = crawler.validate_corpus(tmp_path)

    assert report["decision"] == "FAIL"
    assert report["hard_failures"]["incomplete_detail_documents"] == 1
    assert report["detail_pagination"]["missing_page_count"] == 1
    assert report["detail_pagination"]["gaps"][0]["missing_page_numbers"] == [2]


def test_v1_documents_are_backfilled_as_unscanned_page_one_records(tmp_path):
    crawler = _load_module()
    database = tmp_path / "crawl.sqlite3"
    connection = sqlite3.connect(database)
    connection.execute(
        """
        CREATE TABLE documents (
            source_url TEXT PRIMARY KEY, record_id TEXT NOT NULL UNIQUE,
            section TEXT NOT NULL, category_slug TEXT NOT NULL, title TEXT,
            content_sha256 TEXT NOT NULL, duplicate_of TEXT, html_path TEXT NOT NULL,
            markdown_path TEXT NOT NULL, data_json TEXT NOT NULL, extracted_at TEXT NOT NULL
        )
        """
    )
    record = {
        "schema_version": "suanzhun-corpus.v1",
        "record_id": "book-7",
        "section": "dianji",
        "category": {"slug": "qitadanpian", "title": "其他单篇"},
        "title": "旧文档",
        "source_url": "https://www.suanzhun.net/book/7.html",
        "body_text": "旧正文",
        "body_html": "旧正文",
        "body_markdown": "旧正文\n",
        "raw_path": "raw/pages/old.html.gz",
    }
    connection.execute(
        "INSERT INTO documents VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (
            record["source_url"],
            record["record_id"],
            record["section"],
            record["category"]["slug"],
            record["title"],
            "old-hash",
            None,
            "content/old.html",
            "content/old.md",
            json.dumps(record, ensure_ascii=False),
            "2026-07-15T00:00:00+00:00",
        ),
    )
    connection.commit()
    connection.close()

    store = crawler.CrawlStore(database)
    try:
        row = store.connection.execute("SELECT * FROM document_pages").fetchone()
        assert row["page_url"] == record["source_url"]
        assert row["base_url"] == record["source_url"]
        assert row["page_number"] == 1
        assert row["page_count"] == 1
        assert row["pagination_scanned"] == 0
    finally:
        store.close()


def test_validator_independently_detects_raw_continuation_links_missing_from_frontier(tmp_path):
    crawler = _load_module()
    html = """
    <article class="box">
      <div class="breadcrumbs"><a href="/">首页</a> &gt; <a href="/dianji/">典籍</a> &gt;
        <a href="/dianji/qitadanpian/">其他单篇</a> &gt; 正文</div>
      <h1 class="singletitle">独立门禁</h1>
      <div class="content-text">第一页</div>
    </article>
    """.encode()
    raw_with_hidden_link = html.replace(b"</article>", b'<a href="/book/77_2.html">2</a></article>')
    raw_path = Path("raw/pages/base.html.gz")
    (tmp_path / raw_path).parent.mkdir(parents=True)
    (tmp_path / raw_path).write_bytes(gzip.compress(raw_with_hidden_link, mtime=0))

    page = crawler.parse_page(html, "https://www.suanzhun.net/book/77.html")
    store = crawler.CrawlStore(tmp_path / "crawl.sqlite3")
    try:
        _persist_page(crawler, store, tmp_path, page, raw_path.as_posix())
        store.add_url(page.source_url)
        store.connection.execute(
            "UPDATE frontier SET status = 'done', raw_path = ? WHERE url = ?",
            (raw_path.as_posix(), page.source_url),
        )
        store.connection.commit()
    finally:
        store.close()

    report = crawler.validate_corpus(tmp_path)

    assert report["decision"] == "FAIL"
    assert report["hard_failures"]["raw_detail_links_without_frontier"] == 1
    assert report["raw_detail_links_without_frontier"][0]["target_url"] == ("https://www.suanzhun.net/book/77_2.html")


def test_validator_rejects_resources_left_pending_by_a_processing_limit(tmp_path):
    crawler = _load_module()
    store = crawler.CrawlStore(tmp_path / "crawl.sqlite3")
    try:
        store.connection.execute(
            "INSERT INTO resources(url, kind, source_url) VALUES (?, 'media', ?)",
            (
                "https://www.suanzhun.net/images/pending.jpg",
                "https://www.suanzhun.net/book/77.html",
            ),
        )
        store.connection.commit()
    finally:
        store.close()

    report = crawler.validate_corpus(tmp_path)

    assert report["decision"] == "FAIL"
    assert report["hard_failures"]["pending_resources"] == 1


def test_fetcher_does_not_retry_structural_boundary_errors(monkeypatch):
    crawler = _load_module()
    fetcher = crawler.Fetcher(
        delay_seconds=0,
        timeout_seconds=1,
        max_attempts=4,
        max_page_bytes=1024,
    )
    calls = 0

    def reject(_url, _max_bytes):
        nonlocal calls
        calls += 1
        raise ValueError("响应实际体积超过上限")

    monkeypatch.setattr(fetcher, "_single", reject)
    try:
        result = fetcher.fetch("https://www.suanzhun.net/jichu/")
    finally:
        fetcher.close()

    assert calls == 1
    assert result.attempts == 1
    assert result.error == "ValueError: 响应实际体积超过上限"
    assert fetcher.retry_count == 0
