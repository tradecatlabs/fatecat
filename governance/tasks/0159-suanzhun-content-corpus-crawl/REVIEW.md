# 算准网语料抓取修复审查

## Verdict

- Decision: PASS（任务 0159 范围）
- Depth: deep
- Scope: correctness, security, reliability, migration, performance, architecture, build-release, repo-hygiene, test-quality, future-optimal-drift, ponytail-complexity, document-drift
- Blocking findings in scope: 0
- Active warnings in scope: 0
- Repository-wide note: 工作区另一个八字任务文件触发 `ponytail-complexity`，共享 `.venv` 另有 `click` 版本漂移；二者不属于 0159 修改边界，未擅自修改。0159 文件级 principle scan 与独立 clean data-extra 环境均 PASS。

## Spec Compliance

- 当前/旧式详情续页由 `base_url/page_number/page_count` 建模；从可见末页推导完整 `1..N`，物理页与逻辑文章不再混为一体。
- 756 个已知续页全部进入 `done`，其中当前 `/article|book/` 路由 563、旧分类层级路由 193；138 篇分页文章无序列缺口。
- 4100 个物理详情页聚合为 3344 篇逻辑文章，其中基础 960、典籍 2384；逐页原始响应、页码、正文哈希和来源 URL 可追溯。
- 7 个清噪后为空的真实末页保留物理页证据，不向正文注入分页导航；25 个旧 sitemap 404 保持 unavailable。
- 资源 17 条：3 个 done、3 个 robots denied、11 个不可公开解析或原文无效地址；`failures.ndjson` 为 0，`unavailable.ndjson` 为 39。

## Findings

### RESOLVED-01：详情续页发现与验证共因失明

- Severity: BLOCK（已修复）
- Evidence: `DEBUG.md` E1/E2；`classify_url()`、`_expand_detail_pagination()`、`document_pages`、`_raw_detail_continuations_without_frontier()`。
- Impact: 首轮报告在 756 个页面缺失时假 PASS，正文少约 124.6 万字符。
- Fix: 物理页身份与唯一约束、完整页序列推导、逻辑文章聚合、原始 href 独立门禁和 v1 原位迁移。
- Validation: 修复前 5 项预期 RED；修复后目标 pytest 15 passed；真实分页缺口和原始 href 漏入 frontier 均为 0。

### RESOLVED-02：资源处理上限可留下 pending 却不阻止完成

- Severity: BLOCK（已修复）
- Evidence: `validate_corpus()` 现在将 `resource_status.pending` 纳入 hard failures；新增 pending-resource 回归。
- Impact: `--max-resources` 小于资源队列时可能产生第二种假完成。
- Fix: `pending_resources > 0` 直接返回 FAIL，不将处理预算当作完成证据。
- Validation: 目标 fixture 明确断言 decision FAIL 与 `pending_resources=1`；真实语料为 0。

### RESOLVED-03：结构性边界错误被重复请求

- Severity: WARN（已修复）
- Evidence: `Fetcher.fetch()` 将 `ValueError` 与瞬时 `HTTPError/OSError` 分流。
- Impact: 私网边界、重定向或体积超限属于确定性失败，重复四次只会制造请求和重试风暴。
- Fix: 结构性错误一次失败并保留真实 attempts；瞬时错误仍有限指数退避。
- Validation: 新回归证明结构性错误仅调用一次、attempts=1、retry_count=0。

### RESOLVED-04：链接清单全量驻留内存

- Severity: WARN（已修复）
- Evidence: `_export_records()` 以 SQLite cursor generator 流式写 `links.ndjson`，计数独立查询。
- Impact: 当前约 19.5 万条链接尚可，但 10× 数据会放大峰值内存。
- Fix: 不新增框架，只流式迭代最大清单；页面和资源小集合保持直接代码。
- Validation: 最终导出和 11046 项文件校验和通过。

## Security And Reliability

- robots 必须成功读取后才抓取；404 按标准视为无规则，其他读取失败立即中止。
- 页面限定 `www.suanzhun.net`；外站媒体默认关闭，启用后校验公开 HTTP(S) 地址，重定向每跳复核，显式主机白名单只用于已人工核验的代理 DNS 失真环境。
- 请求、重定向、响应体、页面、资源、超时和重试均有上限；不存在无界并发、无限重试或静默吞错。
- HTML 删除脚本、表单、iframe、嵌入对象、推荐和相邻导航，URL 属性只保留 HTTP(S)；正文文件使用原子替换。
- SQLite 为单一状态真相源；v1 仅原位增加物理页证据并从已保存 raw 恢复发现，不重建第二套状态库。

## Correctness And Migration

- `UNIQUE(base_url,page_number)` 与 page-count check 阻止同一逻辑文章的页码冲突。
- 只有 `1..N` 齐全才物化逻辑文章；`source_pages` 顺序、frontier done 状态、原始 href 和重复别名均由 validator 交叉检查。
- 元数据只扫描正文节点之前的头部；3 条现场作者污染样本均恢复为 null，独立查询污染与可疑作者均为 0。
- v1 副本 smoke：3344 个旧文档回填为未扫描 page-1，从 raw 恢复 756 个待抓 URL，SQLite integrity 为 `ok`；真实增量未重抓已完成首页。
- 重复别名按内容哈希和最小 URL 确定性重建：expected=657、stored=657、invalid=0。

## Performance Review

- Scale: `V=4340` frontier 页面、`P=4100` 物理详情页、`D=3344` 逻辑文章、`E≈19.5 万` 链接、输出约 382.6 MB。
- Complexity: 网络发现与导出为 `O(V + E + B)`，详情聚合为 `O(P + B_body)`；独立原始 href 审计和校验和为 `O(B_raw + B_output)`。SQLite 主键/索引承担 URL、页码和内容查重。
- Memory: 页面抓取、原始 href 审计和正文聚合以单页面/单文章为上限；最大链接清单已改为流式。校验和仍逐文件读取，受单页 10 MB/单资源 50 MB 上限约束。
- Hot path: 网络 I/O；实测 p50 95 ms、p95 145 ms、max 2881 ms。`--validate-only` 含 382 MB 校验和约 2.8 秒。
- Immediate: 已消除链接清单全量内存和结构性错误重试；无需再引入并发或缓存。
- Measure first: 若规模达到 10× 或校验超过维护窗口，分别 profile raw 扫描、SHA-256 与 SQLite 导出；100× 时再考虑分块校验和/分片清单。礼貌单并发是当前正确权衡。
- Rollback: 代码回滚不破坏 v1 文档；运行输出可整体删除后复跑，或保留 SQLite 继续增量恢复。

## Audit Case Consumption

- `CASE-0001`：完成声明必须有独立运行证据；本次晋升项目 GATE-0002。
- `CASE-0003`：旧 Done/REVIEW/closeout 被新证据失效后，任务重开并重新收口。
- `CASE-0008`：验证器不能只消费生产路径裁剪后的证据；新增未裁剪 raw href 门禁。
- `CASE-0007`：依赖未变化；独立 `/tmp/fatecat-suanzhun-deps-venv` 中 50 个包兼容，bs4/httpx 可导入且 CLI 可启动。
- 修复采样见 `AUDIT_CASE_SAMPLING.md`，项目规则见 `GATE-0002`。

## Document Drift

- 已同步输出 README、`scripts/AGENTS.md`、`tests/AGENTS.md`、本地状态 AGENTS、scripts module context、本地工具入口、任务 DEBUG/验收/状态/审查和 GATE-0002。
- 未修改生产服务、公共 API、contracts、catalog、canonical classics 或 CI；运行全文继续由 `.gitignore` 排除。
- 项目未启用 operating-model 四件套；本次只更新已有 owning source，不新建平行文档体系。

## Evidence

- `.venv/bin/python -m pytest -q tests/regression/test_suanzhun_corpus_crawl.py`: 15 passed。
- `.venv/bin/python -m ruff check scripts/suanzhun-corpus-crawl.py tests/regression/test_suanzhun_corpus_crawl.py`: PASS。
- `--validate-only`: PASS_WITH_UNAVAILABLE；全部 hard failures 为 0。
- `sqlite3`: integrity `ok`；续页 756；分页基址 138；页序列缺口、来源页数不匹配、未扫描和作者污染均为 0。
- `sha256sum -c --quiet files.sha256`: PASS；清单 11046 项。
- `check-structure.sh`、`check-source-hygiene.sh`、scoped principle gate、governance strict/health：PASS。
- `git check-ignore -v`: SQLite 和正文 NDJSON 均命中 `infra/runtime/local-state/exports/` 忽略规则。

## Unknowns And Rights Boundary

- 技术完整性不证明文章观点真实、传统命理准确或版权授权。
- 本地语料保持 `reference_only/review_required/distribution_not_allowed`；人工版权审查前不得公开再发布、晋升生产 canonical 数据或宣称具备训练授权。
- 仓库级八字任务 principle finding 与共享 `.venv` click 漂移由各自 owner 处理，不影响本任务独立 clean-env 与范围验收，也不得被本任务顺手修改。
