# Planning Summary
保留首轮历史证据，在同一 SQLite 真相源内补建详情分页实体、逻辑文章聚合与独立闭合门禁，再增量补抓、交叉审计、同步治理并重新审查。
- 编译节点总数: 11
- 叶子执行项: 11
- 执行波次数: 11
- 当前任务必须遵守 `SPEC -> PLAN -> BUILD -> TEST -> REVIEW -> SHIP`

# Lifecycle Gates
- 所有阶段必须按 `SPEC -> PLAN -> BUILD -> TEST -> REVIEW -> SHIP` 顺序闭合，不得跳过 gate。
- SPEC: 真实站点、截图、robots、sitemap、详情结构和版权边界已记录
- PLAN: 数据模型、发现闭包、恢复模型、输出结构和失败分类已确定
- BUILD: 抓取器只写显式 output 目录并通过离线测试
- TEST: 离线回归与全量内置校验均通过
- REVIEW: correctness/security/reliability/performance/document drift 审查无 BLOCK
- SHIP: 输出清单、失败明细、复跑命令、回滚/清理路径和任务 closeout 可复核

# Simplest Path
复用项目 scripts 入口、httpx 与 BeautifulSoup，在一个直接脚本中组合发现、抓取、抽取、导出和校验；不创建服务、队列、插件系统或通用爬虫框架。

# Split Strategy
按可独立验收的证据切片拆分；网站发现、解析测试、实现、全量副作用运行、完整性审计、文档治理和最终审查严格显式依赖。

# Execution Waves
- Wave 1: TP-01
- Wave 2: TP-02
- Wave 3: TP-03
- Wave 4: TP-04
- Wave 5: TP-05
- Wave 6: TP-06
- Wave 7: TP-07
- Wave 8: TP-08
- Wave 9: TP-09
- Wave 10: TP-10
- Wave 11: TP-11

# Runtime Workflow Contract
- workflow artifact 必须存入任务目录，而不是只留在聊天上下文。
- worker 只能消费当前 packet 的最小上下文、允许工具、禁止动作、证据要求和停止条件。
- verifier / 自审必须独立挑战关键发现，不能把 worker 自评当作验收。
- integrator / closeout 必须报告 verified、rejected、unresolved、failed、not-covered。
- 全局预算: 单主机默认最多 1 个并发请求，页面上限 10000，单资源大小有限制
- 全局预算: 瞬时错误最多 4 次尝试，指数退避并尊重 Retry-After
- 全局停止条件: robots 明确禁止目标路径
- 全局停止条件: 出现登录、验证码或访问控制
- 全局停止条件: 目标站持续 403/429/5xx 且有限重试耗尽
- 全局停止条件: 页面上限触发或输出磁盘不可写
- TP-01: tools=read-only filesystem;HTTP GET;governance context bundle; forbidden=写业务代码;绕过访问控制; evidence=robots 响应;sitemap 计数;DOM selector 证据; budget=仅少量探测请求; stop=robots 禁止或目标需认证
- TP-02: tools=apply_patch;pytest; forbidden=在测试中访问公网; evidence=red/green 命令输出; budget=秒级离线测试; stop=规格仍有阻塞歧义
- TP-03: tools=apply_patch;python;pytest;ruff; forbidden=修改生产服务;引入通用爬虫平台; evidence=测试输出;lint 输出;CLI smoke; budget=页面上限与资源大小上限可配置; stop=需要绕过访问控制才能继续
- TP-04: tools=crawler CLI;process polling; forbidden=无界并发;抓取非目标栏目; evidence=运行日志;manifest;failure ledger; budget=单并发;默认请求间隔不低于 0.25 秒;最大 10000 页; stop=429/403 持续;页面上限;磁盘不可写
- TP-05: tools=crawler validate;sqlite read-only queries;filesystem hash; forbidden=人工删除失败行以造绿; evidence=validator summary;counts;hash verification; budget=O(files + links) 本地审计; stop=存在不可解释抓取缺口
- TP-06: tools=apply_patch;governance tools;task validators; forbidden=把运行态全文写入 governance; evidence=governance strict output;task validation output; budget=只更新 owning sources; stop=owner/source-of-truth 不明确
- TP-07: tools=auto-review;task closeout tools;read-only git diff; forbidden=无证据声明完整或合法分发; evidence=review findings;task validator;closeout packet; budget=只审查任务范围; stop=存在 BLOCK finding
- TP-08: tools=read-only probes;apply_patch;pytest;DEBUG validator; forbidden=直接补抓 URL 造绿; evidence=最小实验;RED 输出;DEBUG hypothesize; budget=离线秒级; stop=根因与现场证据冲突
- TP-09: tools=apply_patch;pytest;ruff;migration smoke; forbidden=平行状态库;把续页导出成独立文章; evidence=GREEN;SQLite migration;缺页门禁; budget=单脚本和既有依赖; stop=无法保持 v1 原位恢复
- TP-10: tools=crawler CLI;sqlite3;sha256sum;jq; forbidden=删除失败行;复用分类器作为唯一审计来源; evidence=756 续页;4100 物理页;3344 文章;hash; budget=单并发增量抓取; stop=活动失败或未解释缺口
- TP-11: tools=auto-review;governance/task validators;apply_patch; forbidden=保留旧假 PASS;扩大到其他任务; evidence=DEBUG conclude;GATE-0002;REVIEW;closeout packet; budget=只更新 owning source; stop=任务范围 BLOCK

# Next Executable Leaves
- 无；11 个叶子节点全部完成。

# Dependency Graph
TP-01 -> TP-02
TP-02 -> TP-03
TP-03 -> TP-04
TP-04 -> TP-05
TP-05 -> TP-06
TP-06 -> TP-07
TP-07 -> TP-08
TP-08 -> TP-09
TP-09 -> TP-10
TP-10 -> TP-11

# Rollback Protocol
- 恢复 `INDEX.md` 当前任务行
- 恢复本任务目录到初始化状态
- 不得影响其他任务目录
