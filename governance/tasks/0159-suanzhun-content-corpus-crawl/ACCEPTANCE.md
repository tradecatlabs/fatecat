# Task-Level Acceptance
- 目标栏目导航分类、分页和可访问详情页全部进入 URL 映射，未成功项具有明确终态和失败证据
- 每条正文包含标题、正文、层级、作者或来源、发布时间、原始链接、分类、哈希和本地文件引用；缺失字段显式为 null 而非猜测
- 正文噪声清除且原始响应可回查，媒体资源具有来源页、本地路径、MIME、大小和 sha256
- 同一命令可断点续跑、增量刷新并重新生成确定性清单和完整性报告
- 自动测试、输出校验、任务文档校验、治理校验和最终审查有真实证据
- approved plan 已成功编译为递归任务树
- 叶子节点数量: 11
- 当前可立即执行叶子节点: 无；全部完成

# Validation Plan
- 用离线 HTML fixture 覆盖列表分页、当前/旧详情续页、隐藏中间页、物理页聚合、元数据隔离、缺页和原始 href 独立门禁
- 运行抓取器内置 validate，校验数据库/NDJSON/文件/hash/映射/失败终态、详情 `1..N` 序列与聚合一致性
- 以 sitemap、入口导航、分页闭包、详情链接闭包和媒体引用闭包做交叉完整性核对
- 运行目标 pytest、ruff、任务文档 strict 校验和 governance strict 校验
- bugfix / regression / flaky 任务必须把 DEBUG.md 的回归证据串到 Recent Evidence
- TP-01 | Verify: 任务 CONTEXT/PLAN 包含截图、robots、sitemap、入口、详情和旧路径实测证据 | Gate: 不存在会改变实现路径的未决范围歧义
- TP-02 | Verify: pytest 先出现目标缺失红灯，完成实现后全部转绿 | Gate: 测试不访问公网且覆盖正负边界
- TP-03 | Verify: 目标 pytest 与 ruff 通过，--help 和 --validate-only 可执行 | Gate: 无无界队列、无静默失败、所有输出限定在显式目录
- TP-04 | Verify: 抓取命令正常退出且 manifest 记录 complete 或明确 residual failures | Gate: robots 允许、页面上限未触发、无活动 transient failure
- TP-05 | Verify: --validate-only 通过，completeness.json 无未解释 dangling target URL 或 active failure | Gate: 可访问目标与失效/拒绝/失败状态严格区分
- TP-06 | Verify: 结构检查、governance index 重建与 strict validate 通过 | Gate: 文档描述与实际 CLI、路径和验证证据一致
- TP-07 | Verify: review 无 BLOCK，任务 closeout validator 和 closeout packet 通过 | Gate: 所有叶子完成、Recent Evidence 非空、无活动 blocker
- TP-08 | Verify: DEBUG hypothesize 与 RED 契约通过 | Gate: 根因和 756 页现场证据一致
- TP-09 | Verify: 目标 pytest/ruff 全绿，v1 原位迁移和缺页拒绝通过 | Gate: 页面与逻辑文章职责分离且无平行真相源
- TP-10 | Verify: 756 个续页完成，序列缺口 0，3344 篇逻辑文档完整，校验和通过 | Gate: 内置与独立审计同时通过
- TP-11 | Verify: DEBUG conclude、review、governance、task closeout 全部通过 | Gate: 防假闭包规则落到 owning source 且无 BLOCK

# Review Gate
- 正确性: URL 分类、正文边界、去重、增量状态和完整性统计一致
- 安全: 不访问禁止路径、不跟随私网 URL、不泄露用户数据、不绕过访问控制
- 可靠性: 有限重试、断点续跑、原子文件写入、失败终态和校验
- 性能: O(V+E) 发现、流式写盘、索引去重、单主机有界速率和磁盘预算
- 文档: scripts/tests AGENTS、工具验证入口和任务证据与最终实现同步

# Runtime Verification Gate
- [x] 每个 tool/action 结果都有可回指证据或明确未执行原因。
- [x] 高风险动作没有由 worker/agent 自我批准；审批状态可追踪。
- [x] compaction / resume 后目标、计划、修改文件、审批状态和验证项未丢失。
- [x] verifier / 自审已检查关键发现是否有证据支持。
- [x] closeout 明确 coverage gaps、failed packets 和 unresolved questions。
- [x] TP-01: 输出格式 `任务规格与发现证据`；证据要求：robots 响应;sitemap 计数;DOM selector 证据
- [x] TP-02: 输出格式 `pytest regression suite`；证据要求：red/green 命令输出
- [x] TP-03: 输出格式 `single CLI crawler with SQLite state and exports`；证据要求：测试输出;lint 输出;CLI smoke
- [x] TP-04: 输出格式 `corpus output tree`；证据要求：运行日志;manifest;failure ledger
- [x] TP-05: 输出格式 `audit reports`；证据要求：validator summary;counts;hash verification
- [x] TP-06: 输出格式 `documentation sync evidence`；证据要求：governance strict output;task validation output
- [x] TP-07: 输出格式 `PASS/WARN/BLOCK review and closeout packet`；证据要求：review findings;task validator;closeout packet
- [x] TP-08: 输出格式 `DEBUG root-cause and RED evidence`；证据要求：最小实验;RED 输出;hypothesize validator
- [x] TP-09: 输出格式 `v2 physical-page and logical-document model`；证据要求：GREEN 测试;ruff;迁移 smoke
- [x] TP-10: 输出格式 `incremental corpus and independent audit`；证据要求：分页计数;SQLite 对账;files.sha256
- [x] TP-11: 输出格式 `gate, review and closeout packet`；证据要求：DEBUG conclude;governance strict/health;review;closeout

# Ship Readiness
- 运行产物位于 infra/runtime/local-state/exports/suanzhun-corpus
- 回滚为删除新增脚本/测试/文档，运行数据可由 scripts/clean-runtime.sh 或删除输出目录清理
- 观察项为 request 数量、p95 延迟、重试数、状态分布、解析失败、内容重复组、媒体失败和磁盘占用

# Task Package Acceptance
## TP-01
- 标题: 锁定抓取边界与数据契约
- 验收标准:
  - 三源发现策略和目标范围过滤规则明确
  - 缺失字段和不可访问 URL 的处理明确
- Verify: 任务 CONTEXT/PLAN 包含截图、robots、sitemap、入口、详情和旧路径实测证据
- Gate: 不存在会改变实现路径的未决范围歧义
- 输出物: 稳定抓取规格；URL/字段/输出契约；风险与停止条件

## TP-02
- 标题: 建立离线解析与安全回归契约
- 验收标准:
  - 覆盖 URL canonicalization、scope、metadata、body、noise、links、media 和 filename
- Verify: pytest 先出现目标缺失红灯，完成实现后全部转绿
- Gate: 测试不访问公网且覆盖正负边界
- 输出物: tests/regression/test_suanzhun_corpus_crawl.py

## TP-03
- 标题: 实现可恢复全量抓取器
- 验收标准:
  - 支持断点续跑和增量刷新
  - 保存原始响应与规范化输出
  - 生成机器可读失败和完整性报告
- Verify: 目标 pytest 与 ruff 通过，--help 和 --validate-only 可执行
- Gate: 无无界队列、无静默失败、所有输出限定在显式目录
- 输出物: scripts/suanzhun-corpus-crawl.py

## TP-04
- 标题: 执行基础与典籍全量抓取
- 验收标准:
  - 入口、分类、分页、详情和正文媒体均有映射
  - 中断后原命令可续跑
- Verify: 抓取命令正常退出且 manifest 记录 complete 或明确 residual failures
- Gate: robots 允许、页面上限未触发、无活动 transient failure
- 输出物: infra/runtime/local-state/exports/suanzhun-corpus

## TP-05
- 标题: 审计链接、内容、媒体和失败闭包
- 验收标准:
  - 所有 record/file 引用存在且 hash 匹配
  - URL 和内容重复均有 alias 记录
  - sitemap 差异有解释
- Verify: --validate-only 通过，completeness.json 无未解释 dangling target URL 或 active failure
- Gate: 可访问目标与失效/拒绝/失败状态严格区分
- 输出物: 完整性报告；重复组；失败与不可用明细；文件 sha256 清单

## TP-06
- 标题: 同步工具链、架构与版权边界文档
- 验收标准:
  - Operating model: not needed 有具体理由
  - Toolchain/process/source-of-truth 影响有 owner 与证据
  - 版权边界明确
- Verify: 结构检查、governance index 重建与 strict validate 通过
- Gate: 文档描述与实际 CLI、路径和验证证据一致
- 输出物: AGENTS/治理/任务文档更新

## TP-07
- 标题: 完成独立审查与任务收口
- 验收标准:
  - 发现的问题已修或明确阻塞
  - 效率检查含复杂度、瓶颈、验证指标和权衡
  - 用户可按命令复跑
- Verify: review 无 BLOCK，任务 closeout validator 和 closeout packet 通过
- Gate: 所有叶子完成、Recent Evidence 非空、无活动 blocker
- 输出物: REVIEW 结论；任务 closeout packet；最终交付摘要

## TP-08
- 标题: 固化详情续页漏抓根因与 RED 契约
- 验收标准:
  - 至少三条可证伪假设和确认实验落盘
  - 覆盖当前/旧式续页、隐藏中间页、聚合、作者隔离和缺页门禁
- Verify: DEBUG.md 通过 hypothesize 校验，新增测试在修复前按预期失败
- Gate: 根因由只读最小实验确认，RED 与 756 页现场证据一致
- 输出物: DEBUG.md；详情分页与元数据 RED 回归

## TP-09
- 标题: 实现逐页存证与逻辑文章聚合
- 验收标准:
  - 续页不导出为独立文章
  - v1 page-1 文档可原位迁移并增量续跑
  - 正文作者标签不污染 metadata
- Verify: 目标 pytest 与 ruff 全绿，缺页 fixture 被 validator 拒绝
- Gate: `1..N` 序列有唯一约束和独立门禁
- 输出物: 分页识别与推导；document_pages；逻辑文章聚合；分页完整性门禁

## TP-10
- 标题: 增量补抓并独立审计详情分页闭包
- 验收标准:
  - 页面来源与聚合文档双向可追溯
  - 作者污染为 0，重复和不可用状态有解释
- Verify: 756 个续页全部终态，序列缺口为 0，3344 个逻辑文档完整，校验和通过
- Gate: 内置 validator 与独立 SQLite/文件审计同时通过
- 输出物: 增量语料；completeness；逐页/资源清单；独立审计证据

## TP-11
- 标题: 同步防复发治理并重新审查收口
- 验收标准:
  - 完成声明精确覆盖详情分页
  - 效率检查有复杂度、实测指标和升级边界
  - 同一命令可增量复跑
- Verify: DEBUG conclude、auto-review、任务 closeout、governance strict/health 全部通过
- Gate: 旧 PASS 已被新证据取代，防假闭包规则进入 owning source，最终无 BLOCK
- 输出物: 更新后的任务/治理文档；AUDIT_CASE_SAMPLING；REVIEW；TASK_CLOSEOUT_PACKET

# Anti-Goals
- 不得修改生产服务、公共 contract、canonical classics 或 CI 发布链路
- 不得虚构证据
- 不得越权补全未确认信息
