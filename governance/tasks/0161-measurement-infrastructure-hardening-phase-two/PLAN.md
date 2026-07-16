# Planning Summary
先锁公开投影和 capability 语义，再优化确定性热路径并接入独立评测；随后拆分职责、补异步观测和公开分发闭包，最后执行隔离审查与仓库卫生收口。
- 编译节点总数: 8
- 叶子执行项: 8
- 执行波次数: 4
- 当前任务必须遵守 `SPEC -> PLAN -> BUILD -> TEST -> REVIEW -> SHIP`

# Lifecycle Gates
- 所有阶段必须按 SPEC -> PLAN -> BUILD -> TEST -> REVIEW -> SHIP 顺序闭合，不得跳过 gate。
- SPEC: 八项问题、排除项、真实约束、终态和回滚边界已记录
- PLAN: 每项拥有输入、输出、验证、证据和依赖
- BUILD: 先建立失败测试或基线，再实施最小行为变更
- TEST: 定向回归、benchmark、clean-room smoke 和 quick CI 通过
- REVIEW: correctness/reliability/performance/architecture/license/document drift 无 BLOCK
- SHIP: 文档、任务、提交和工作树状态一致

# Simplest Path
复用现有 renderer、CapabilityExecutor、lunar-python、Prometheus、wheel/skill 导出和 release gate，只增加能被测试直接证明必要的薄层。

# Split Strategy
按独立失败边界拆成八个纵向切片；公开字段和成熟度契约先行，性能/评测/复杂度/观测/分发可在契约稳定后推进，最终统一 closeout。

# Execution Waves
- Wave 1: TP-01
- Wave 2: TP-02, TP-03, TP-04
- Wave 3: TP-05, TP-06, TP-07
- Wave 4: TP-08

# Runtime Workflow Contract
- workflow artifact 必须存入任务目录，而不是只留在聊天上下文。
- worker 只能消费当前 packet 的最小上下文、允许工具、禁止动作、证据要求和停止条件。
- verifier / 自审必须独立挑战关键发现，不能把 worker 自评当作验收。
- integrator / closeout 必须报告 verified、rejected、unresolved、failed、not-covered。

# Next Executable Leaves
- TP-01 | Wave 1 | Depends On: 无 | Gate: 公开输出只含允许字段，结构化证据无损

# Dependency Graph
TP-01 -> TP-02
TP-01 -> TP-03
TP-01 -> TP-04
TP-02 -> TP-05
TP-04 -> TP-05
TP-04 -> TP-06
TP-04 -> TP-07
TP-03 -> TP-08
TP-05 -> TP-08
TP-06 -> TP-08
TP-07 -> TP-08

# Rollback Protocol
- 恢复 `INDEX.md` 当前任务行
- 恢复本任务目录到初始化状态
- 不得影响其他任务目录
