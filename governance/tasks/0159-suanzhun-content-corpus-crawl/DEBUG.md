# 算准网详情续页漏抓调试记录

## Bug

- 标题：详情页 `_N.html` 续页未进入抓取闭包，完整性门禁产生假通过
- 症状：现有交付只有 3584 个页面实体；独立现场审计确认 138 篇文章共有 756 个可访问续页未入库，缺少约 124.6 万正文字符；另有 3 条作者字段被正文中的“作者：”污染。
- 首次发现位置 / 时间：2026-07-15，任务 0159 完成后的独立缺失检查。

## Environment

- 仓库 / 模块：`/home/lenovo/.projects/fatecat`；`scripts/suanzhun-corpus-crawl.py`
- 运行环境：Linux；Python 3；本地输出 `infra/runtime/local-state/exports/suanzhun-corpus`
- 依赖 / 版本：项目 `.venv` 内 `httpx`、`beautifulsoup4`；解析器使用 Python `html.parser`
- 配置差异：缺失与限速、代理和外部媒体无关；当前数据库中详情续页数量为 0。

## Reproduction

1. 加载抓取器并分类 `/book/2163_2.html`、`/article/2488_2.html`、`/dianji/jinxiangmishu/208_2.html`。
2. 从已保存的 `/book/2163.html` 原始响应读取分页链接，再调用当前 `parse_page()`。
3. 查询 `frontier` 中 `_N.html` 详情 URL，并用含正文“作者：”的最小 fixture 调用 `parse_page()`。

## Observations

- O1：三个当前/旧式续页 URL 都被 `classify_url()` 判为 `ignore`。
- O2：`/book/2163.html` 原始响应能找到 6 个可见续页 token，但 `parse_page().target_urls` 中续页为 0；`frontier` 中续页也为 0。
- O3：现场逐页探测得到 756/756 个续页 HTTP 200、正文非空、页码连续；其中当前路由 563 页、旧路由 193 页。
- O4：当前 `_metadata()` 扫描整个 `article` 的前 1500 字，正文 fixture 的“作者：正文中的人物介绍”被错误写入 `author`。
- O5：当前 validator 只检查已经进入 `frontier` 的目标；被分类器忽略的 URL 不会成为待校验对象，因此旧报告可在真实缺页时返回 `PASS_WITH_UNAVAILABLE`。

## Hypotheses

### H1: URL 语法契约遗漏续页后缀，导致发现、状态和校验共同失明（ROOT HYPOTHESIS）

- Supports：详情正则只接受 `<id>.html`；最小实验中三类 `_N.html` 都是 `ignore`；原始 HTML 有链接而解析结果和 frontier 均为 0。
- Conflicts：无；现场 HTTP 探测排除了续页不存在或不可访问。
- Test：不改生产代码，仅比较原始 HTML 中续页 token、分类结果、解析目标和 frontier 计数。

### H2: 续页由 JavaScript 动态生成，静态抓取器无法发现

- Supports：若分页 DOM 不含真实链接，静态解析会漏抓。
- Conflicts：已保存原始响应中直接存在续页 href，现场直接 GET 756/756 成功。
- Test：在 gzip 原始响应中搜索 `_N.html`，并与渲染后 DOM 无关的 HTTP GET 对照。

### H3: 续页已抓取但被内容去重或导出层合并隐藏

- Supports：现有系统支持 `duplicate_of`，理论上可能只在最终导出丢失。
- Conflicts：`frontier` 中续页计数为 0，说明缺失发生在内容去重之前。
- Test：直接查询 SQLite `frontier`、`documents` 和 `edges`，不依赖 NDJSON 导出。

## Experiments

### E1

- Hypothesis：H1
- Change：不修改代码；运行只读分类、原始响应解析和 SQLite 计数探针。
- Expected：若 H1 成立，原始响应存在续页 token，但分类为 `ignore`、解析目标为 0、frontier 为 0。
- Result：三类续页均为 `ignore`；`RAW_CONTINUATION_TOKENS=6`、`PARSED_CONTINUATIONS=0`、`FRONTIER_CONTINUATIONS=0`。
- Verdict：confirmed
- Revert：无变更，无需回滚。

### E2

- Hypothesis：H3
- Change：不修改代码；逐页现场探测并按文章核对页码、正文和页内哈希。
- Expected：若是导出隐藏，状态库应已有对应 URL；若是真漏抓，现场页面存在但状态库不存在。
- Result：现场 756/756 个页面成功且每篇页码连续、正文非空、批内不重复；状态库无对应 URL。
- Verdict：rejected
- Revert：无变更，无需回滚。

## Root Cause

- 原始触发是详情 URL 正则只接受 `<id>.html` 而拒绝 `<id>_<page>.html`；`_target_links()` 又以同一分类器作为准入边界，导致续页在发现时被静默丢弃。完整性门禁复用已被裁剪的 frontier，没有独立验证“详情页分页序列闭合”，因此同一错误同时污染发现证据和验收证据。作者污染是相邻但独立的边界错误：元数据解析越过头部边界扫描了正文。

## Fix

- 不变量 owner：URL 分类与详情分页模型；元数据头部解析边界；完整性校验器。
- 最早坏状态：续页 href 在 `_target_links()` 之前被 `classify_url()` 判为 `ignore`。
- 已实施修复：识别当前与旧式续页语法并规范化逻辑文章基址/页码；从分页末页推导完整 `2..N` 序列；在 `document_pages` 逐页存证、按逻辑文章有序聚合；validator 同时检查页序列、聚合覆盖、重复别名和未经过分类器裁剪的原始 href；元数据只扫描正文之前的头部。
- Rejected guard locations：不在导出层补猜正文，不用一次性 URL 清单绕过发现模型，不把每个续页冒充独立文章。
- Ponytail fix scope：复用现有 SQLite、解析器和验证入口，只增加分页实体表与直接 helper，不引入新爬虫框架、队列或并发层。
- Why no broader framework：故障属于单站稳定 URL/DOM 契约，现有脚本是正确 owner。
- Ceiling / upgrade path：若未来出现章节 API 或 JavaScript 游标分页，再以新的实测契约升级；本轮不提前泛化。

## Regression Evidence

- RED：修复前收集 10 项，5 passed / 5 failed；失败点依次是续页仍为 `ignore`、缺少分页身份字段、正文污染作者、未聚合分页、续页解析越界，均与确认根因一致。
- GREEN：`.venv/bin/python -m pytest -q tests/regression/test_suanzhun_corpus_crawl.py` 为 15 passed；`.venv/bin/python -m ruff check scripts/suanzhun-corpus-crawl.py tests/regression/test_suanzhun_corpus_crawl.py` 为 PASS；新增资源 pending 假通过与结构性错误重试回归。
- 迁移：原 v1 数据库副本原位回填 3344 个 page-1 记录，从已存原始响应恢复 756 个待抓续页；未重抓已完成首页，SQLite integrity 为 `ok`。
- 真实增量：续页 756/756 为 `done`，其中当前 `/article|book/` 路由 563、旧分类层级路由 193；138 篇分页文章共形成 4100 个物理详情页和 3344 篇逻辑文章。
- 完整性：详情页序列缺口、frontier 缺失/非 done、未聚合文章、未扫描旧详情、原始 href 未入 frontier、重复别名错误、checksum error 均为 0；`files.sha256` 11046 项通过。
- 元数据：现场 3 条污染样本均恢复为 null；独立查询 `author_pollution=0`、`suspicious_author=0`。
- 边界：7 个可访问末页在清除分页导航后正文为空，仍以物理页证据保留，不向逻辑正文注入噪声；25 个旧 sitemap 详情为 404 unavailable，不伪装为成功或活动失败。

## Defense-in-Depth

- Invariant owner：分类器负责可抓 URL 语法；分页模型负责 `1..N` 闭合；validator 负责独立拒绝不闭合状态。
- Earliest bad state：页面 href 进入目标过滤时。
- Boundary where invalid state entered：`_target_links()` 调用 `classify_url()` 的范围过滤边界。
- Chosen guard：结构化 `base_url/page_number/page_count` + SQLite 唯一约束 + validator 序列检查。
- Rejected guard locations：仅改最终 NDJSON、仅手工补抓 756 URL、仅增加报告文案。
- Adjacent variant tested：当前 `article/book` 与旧式 `jichu/dianji/category/id_N.html`；正文中伪元数据。
- Residual downstream fallback：无；不以缺省值隐藏不完整文章。

## Failed Nodes

- 不适用；当前任务未启用原子执行图。

## First Invalid Node

- 语义上为原 TP-02 的分页解析契约：测试只覆盖列表分页，未覆盖详情续页。

## Upstream Lineage

- 现场详情 href → URL 分类 → `_target_links()` → frontier → documents → completeness validator。

## Downstream Blast Radius

- 756 个页面、138 篇文章、约 124.6 万正文字符；3 条作者元数据；完成声明与 REVIEW 证据失真。

## Lowest Common Refinement Ancestor

- 任务 0159 的“详情和分页完整闭包”验收契约。

## Repair Boundary

- 抓取脚本、离线回归、0159 任务证据、相关治理验证入口；不修改生产服务或 canonical 数据。

## Frozen Nodes

- robots、限速、HTTP 重试、资源公网校验、版权边界与现有列表分页逻辑保持不变。

## Invalidated Nodes

- TP-02 至 TP-07 的“详情分页已完整”和最终 PASS 证据需要重新验证；历史执行事实保留，不改写为未发生。

## Reverification Required

- 新回归测试、目标 lint、增量全量运行、分页闭合报告、内容/资源/哈希审计、治理 strict、独立 review、任务 closeout。
