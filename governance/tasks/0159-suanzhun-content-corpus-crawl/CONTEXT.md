# Repo Evidence
- 仓库根为 /home/lenovo/.projects/fatecat，任务容器为 governance/tasks/0159-suanzhun-content-corpus-crawl
- scripts 是可重复工具入口，infra/runtime/local-state/exports 是 Git 忽略的本地输出边界，tests/regression 是仓库级回归入口
- tools/reference-repos/web 只适合小型解析 fixture；整站未审全文不应进入 tracked vendor 快照或 canonical data-products
- robots.txt 允许 jichu、dianji、article、book；sitemap 当前共 943 个唯一 URL，其中 /dianji/ 906、/jichu/ 32
- 当前详情正文位于 .content-text，但 HTML 会把上一篇/下一篇和相关文章误嵌进正文节点，必须按结构标记裁剪

# Constraints Matrix
- Target end state: 单一 SQLite 抓取状态真相源驱动原始证据、规范化正文、媒体和审计导出，可恢复且可增量
- Real constraints: 公开可访问边界、robots、站点负载、版权/分发限制、动态页面漂移、本地磁盘
- Inertia constraints: 旧 sitemap 路径、当前新详情路径和历史页面形状不得迫使系统维护两套抓取器
- Kill list: 一次性 wget 镜像、仅信 sitemap、仅抓入口首页、静默丢弃 404/解析异常、无来源纯文本堆放
- Existence check: 用户要求可重复全量交付，持续抓取脚本和状态库必须存在；生产业务抽象与新服务不应存在
- Selected ladder rung: project-native scripts + Python 标准库 + 已有成熟 httpx/BeautifulSoup 能力；不引入 Scrapy 平台或浏览器集群
- Do-not-simplify: robots、限速、失败证据、内容/链接闭包、版权边界和原始响应追溯不可删除

# Change Boundary
- 允许新增 scripts/suanzhun-corpus-crawl.py、tests/regression/test_suanzhun_corpus_crawl.py 和必要的 AGENTS/治理/任务文档
- 允许实际输出到 infra/runtime/local-state/exports/suanzhun-corpus，但不追踪全文和数据库
- 禁止修改 fate-core、delivery 服务、生产 contracts 或 canonical classics 内容

# Risk Matrix
- 站点正文可能为现代原创或混合转载，输出只作本地 reference_only，禁止默认公开分发或生产依赖
- 旧 sitemap 含 404，完整性必须区分 unavailable 与 retry_exhausted
- 页面 HTML 非严格闭合且正文多用 br 表达段落，需同时保留清洗 HTML 与文本视图
- 详情和媒体规模未知，必须设置页面上限、流式写盘和单主机限速，避免内存和站点压力
- 站点结构继续变化
- fixture 与真实站点漂移
- 异常 HTML
- 重试风暴
- 磁盘增长
- 站点限流
- 网络中断
- 动态发布造成审计时漂移
- 文档漂移
- 把本地抓取完成过度声明成版权或事实认证

# Assumptions and Falsification
- 基础正文的当前详情 URL 主要为 /article/<id>.html，典籍正文主要为 /book/<id>.html 与 /dianji/<category>/<id>.html；实际分类以面包屑验证
- 没有作者时保留 publisher/source 或 null，不从标题猜作者
- Proof point: 全量运行后分页、详情、媒体和 sitemap 交叉闭包无未解释缺口，输出校验通过
- Falsifier: 发现正文由 JavaScript 才能加载、存在未授权访问层或分页无法由静态链接闭合时重新规划

# Critical Ambiguities
- 关联文章只纳入经目标页面发现且路径/面包屑属于基础或典籍的公开详情；跨到其他栏目只记录外链，不扩大抓取范围
- sitemap 只作为补漏与审计输入，不把已失效 URL 计为可访问详情页
- 正文原始语义以站点 DOM 为准；纯文本编号不会被无证据提升为新的 HTML 标题层级

# Debug Evidence Contract
- 调试模式: Required
- 若任务属于 bugfix / regression / flaky / crash / CI-only failure，必须切到 `Required`
- `Required` 时必须在当前任务目录创建并维护 `DEBUG.md`
- `DEBUG.md` 必须覆盖复现、观察、假设、实验、根因、修复、回归证据

# Task Package Context Map
## TP-01
- Step Key: `discover_scope`
- 标题: 锁定抓取边界与数据契约
- 类型: `分析`
- 目标: 用真实站点证据确定 URL 类型、栏目闭包、正文边界、输出 schema、版权与停止条件
- 父节点: `ROOT`
- 子节点: 无
- 依赖步骤 Key: 无
- 依赖节点 ID: 无
- 输入: 用户需求；本地截图；目标入口；项目治理与目录边界
- 输出: 稳定抓取规格；URL/字段/输出契约；风险与停止条件
- 允许工具: read-only filesystem；HTTP GET；governance context bundle
- 禁止动作: 写业务代码；绕过访问控制
- 证据要求: robots 响应；sitemap 计数；DOM selector 证据
- 停止条件: robots 禁止或目标需认证
- 风险: 站点结构继续变化
- 备注: 无

## Repair Wave Context

### TP-08
- 标题: 固化详情续页漏抓根因与 RED 契约
- 依赖节点: TP-07
- 输出: `DEBUG.md`；详情分页与元数据 RED 回归
- Gate: 根因由只读最小实验确认，RED 失败原因与 756 页现场证据一致

### TP-09
- 标题: 实现逐页存证与逻辑文章聚合
- 依赖节点: TP-08
- 输出: 分页识别与推导；`document_pages`；逻辑文章聚合；独立分页完整性门禁
- Gate: 页面与逻辑文章职责分离，`1..N` 序列有唯一约束，不新增平行真相源

### TP-10
- 标题: 增量补抓并独立审计详情分页闭包
- 依赖节点: TP-09
- 输出: 更新后的本地语料、完整性报告、逐页清单、校验和与独立审计证据
- Gate: 756 个已知续页全部终态，序列缺口为 0，逻辑文档仍为 3344 篇

### TP-11
- 标题: 同步防复发治理并重新审查收口
- 依赖节点: TP-10
- 输出: Gate、`AUDIT_CASE_SAMPLING.md`、`REVIEW.md` 与 closeout packet
- Gate: 旧假 PASS 已被新证据取代，最终 review 无 BLOCK

## TP-02
- Step Key: `parser_contract_tests`
- 标题: 建立离线解析与安全回归契约
- 类型: `测试`
- 目标: 用最小 fixture 锁定分页发现、详情元数据、正文噪声裁剪、格式和媒体引用行为
- 父节点: `ROOT`
- 子节点: 无
- 依赖步骤 Key: discover_scope
- 依赖节点 ID: TP-01
- 输入: 抓取规格；脱敏最小 HTML fixture
- 输出: tests/regression/test_suanzhun_corpus_crawl.py
- 允许工具: apply_patch；pytest
- 禁止动作: 在测试中访问公网
- 证据要求: red/green 命令输出
- 停止条件: 规格仍有阻塞歧义
- 风险: fixture 与真实站点漂移
- 备注: 无

## TP-03
- Step Key: `crawler_implementation`
- 标题: 实现可恢复全量抓取器
- 类型: `开发`
- 目标: 实现 robots/限速/重试/SQLite 状态、递归发现、正文媒体抽取、去重导出和内置校验
- 父节点: `ROOT`
- 子节点: 无
- 依赖步骤 Key: parser_contract_tests
- 依赖节点 ID: TP-02
- 输入: 稳定规格；离线回归契约；项目 scripts 约定
- 输出: scripts/suanzhun-corpus-crawl.py
- 允许工具: apply_patch；python；pytest；ruff
- 禁止动作: 修改生产服务；引入通用爬虫平台
- 证据要求: 测试输出；lint 输出；CLI smoke
- 停止条件: 需要绕过访问控制才能继续
- 风险: 异常 HTML；重试风暴；磁盘增长
- 备注: 无

## TP-04
- Step Key: `full_crawl`
- 标题: 执行基础与典籍全量抓取
- 类型: `数据`
- 目标: 在有界速率下实际跑完页面和媒体闭包并持续写入可恢复状态
- 父节点: `ROOT`
- 子节点: 无
- 依赖步骤 Key: crawler_implementation
- 依赖节点 ID: TP-03
- 输入: 两个栏目入口；sitemap；抓取器
- 输出: infra/runtime/local-state/exports/suanzhun-corpus
- 允许工具: crawler CLI；process polling
- 禁止动作: 无界并发；抓取非目标栏目
- 证据要求: 运行日志；manifest；failure ledger
- 停止条件: 429/403 持续；页面上限；磁盘不可写
- 风险: 站点限流；网络中断；磁盘增长
- 备注: 无

## TP-05
- Step Key: `completeness_audit`
- 标题: 审计链接、内容、媒体和失败闭包
- 类型: `验收`
- 目标: 交叉核对导航、分页、详情、sitemap、内容哈希、文件哈希和失败终态，证明覆盖边界
- 父节点: `ROOT`
- 子节点: 无
- 依赖步骤 Key: full_crawl
- 依赖节点 ID: TP-04
- 输入: crawl.sqlite3；NDJSON manifests；raw/content/media files
- 输出: 完整性报告；重复组；失败与不可用明细；文件 sha256 清单
- 允许工具: crawler validate；sqlite read-only queries；filesystem hash
- 禁止动作: 人工删除失败行以造绿
- 证据要求: validator summary；counts；hash verification
- 停止条件: 存在不可解释抓取缺口
- 风险: 动态发布造成审计时漂移
- 备注: 无

## TP-06
- Step Key: `docs_governance`
- 标题: 同步工具链、架构与版权边界文档
- 类型: `文档`
- 目标: 更新脚本与测试目录说明、治理工具入口和任务证据，明确本地输出与分发边界
- 父节点: `ROOT`
- 子节点: 无
- 依赖步骤 Key: completeness_audit
- 依赖节点 ID: TP-05
- 输入: 最终实现；全量审计结果；项目文档契约
- 输出: AGENTS/治理/任务文档更新
- 允许工具: apply_patch；governance tools；task validators
- 禁止动作: 把运行态全文写入 governance
- 证据要求: governance strict output；task validation output
- 停止条件: owner/source-of-truth 不明确
- 风险: 文档漂移
- 备注: 无

## TP-07
- Step Key: `review_closeout`
- 标题: 完成独立审查与任务收口
- 类型: `审查`
- 目标: 按 correctness/security/reliability/performance/architecture/document lenses 审查并生成可复核 closeout
- 父节点: `ROOT`
- 子节点: 无
- 依赖步骤 Key: docs_governance
- 依赖节点 ID: TP-06
- 输入: 最终 diff；抓取产物摘要；测试/校验/治理证据
- 输出: REVIEW 结论；任务 closeout packet；最终交付摘要
- 允许工具: auto-review；task closeout tools；read-only git diff
- 禁止动作: 无证据声明完整或合法分发
- 证据要求: review findings；task validator；closeout packet
- 停止条件: 存在 BLOCK finding
- 风险: 把本地抓取完成过度声明成版权或事实认证
- 备注: 无
