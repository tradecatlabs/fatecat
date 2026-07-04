# Planning Summary
把 0152 做成低风险本地可执行切片：先对齐仓库事实和外部基础设施模式，再新增 core quality 人审 evidence bundle 模板，最后刷新路线图和验证链路。模板只降低人工提交摩擦，不改变 gate blocked 结论。
- 编译节点总数: 15
- 叶子执行项: 10
- 执行波次数: 7
- 当前任务必须遵守 `SPEC -> PLAN -> BUILD -> TEST -> REVIEW -> SHIP`

# Lifecycle Gates
- SPEC: 明确 template-only、operator-action-required、external verification pending；不得跳过 gate。
- PLAN: 任务树、验证命令、non-claim 和 falsifier 写入任务包；不得跳过 gate。
- BUILD: 只实现模板/说明/测试/local-ci 文档接线，不扩大到真实外部执行；不得跳过 gate。
- TEST: 证明模板不会被真实 gate 接受，local-ci quick 通过；不得跳过 gate。
- REVIEW: 检查敏感信息、伪证、文档漂移、路线图夸大；不得跳过 gate。
- SHIP: git clean、提交推送、远端 CI 当前 commit；不得跳过 gate。

# Simplest Path
复用现有 core-quality-human-review-gate 与 professional rubric；新增一个 template generator 输出 JSON/Markdown；测试模板被 gate 拒绝；local-ci 只保存模板和 blocked gate summary。

# Split Strategy
按资料对齐、契约设计、实现接线、文档计划、验证交付拆包；所有叶子节点能独立验证。

# Execution Waves
- Wave 1: TP-01.01, TP-01.02
- Wave 2: TP-02.01, TP-02.02
- Wave 3: TP-03.01
- Wave 4: TP-03.02
- Wave 5: TP-04.01, TP-04.02
- Wave 6: TP-05.01
- Wave 7: TP-05.02

# Runtime Workflow Contract
- workflow artifact 必须存入任务目录，而不是只留在聊天上下文。
- worker 只能消费当前 packet 的最小上下文、允许工具、禁止动作、证据要求和停止条件。
- verifier / 自审必须独立挑战关键发现，不能把 worker 自评当作验收。
- integrator / closeout 必须报告 verified、rejected、unresolved、failed、not-covered。

# Next Executable Leaves
- TP-01.01 | Wave 1 | Depends On: 无 | Gate: 仓库事实来自命令输出，未脑补外部证据。
- TP-01.02 | Wave 1 | Depends On: 无 | Gate: 调研使用一手资料 URL，且只映射要求，不宣称外部 live 完成。

# Dependency Graph
TP-01.01 -> TP-02.01
TP-01.02 -> TP-02.01
TP-01.01 -> TP-02.02
TP-01.02 -> TP-02.02
TP-02.01 -> TP-03.01
TP-02.02 -> TP-03.01
TP-02.01 -> TP-03.02
TP-02.02 -> TP-03.02
TP-03.01 -> TP-03.02
TP-03.01 -> TP-04.01
TP-03.02 -> TP-04.01
TP-03.01 -> TP-04.02
TP-03.02 -> TP-04.02
TP-04.01 -> TP-05.01
TP-04.02 -> TP-05.01
TP-04.01 -> TP-05.02
TP-04.02 -> TP-05.02
TP-05.01 -> TP-05.02

# Rollback Protocol
- 恢复 `INDEX.md` 当前任务行
- 恢复本任务目录到初始化状态
- 不得影响其他任务目录
