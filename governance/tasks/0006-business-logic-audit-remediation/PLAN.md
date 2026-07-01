# Planning Summary
按 REVIEW-0001 的 BLOCK/WARN 顺序修复：先冻结治理与基线，再断开 fate-core 到 delivery 的反向依赖，然后修业务选项语义，统一入口真相源，补坐标校验，最后做 release gate 和审计 closeout。
- 编译节点总数: 24
- 叶子执行项: 18
- 执行波次数: 11
- 当前任务必须遵守 `SPEC -> PLAN -> BUILD -> TEST -> REVIEW -> SHIP`

# Lifecycle Gates
- 本任务必须按 `SPEC -> PLAN -> BUILD -> TEST -> REVIEW -> SHIP` 顺序推进，任何阶段不得跳过 gate；未满足 gate 时只能回到对应前置节点补证据。
- SPEC：确认 REVIEW-0001 finding、当前 dirty governance 状态和本任务边界。
- PLAN：任务树、依赖、验收命令和 ready leaves 落盘。
- BUILD：按 P0 finding 先后修复，不先做报告包装。
- TEST：每个 finding 对应至少一个测试或结构 scan。
- REVIEW：用 auto-review 复核 future-optimal-drift、ponytail-complexity、contract、architecture。
- SHIP：local-ci quick、治理 strict、REVIEW-0001 closeout 全部通过后才提交。

# Simplest Path
不大重写、不换主链。先用显式 422 阻止未实现语义造成假结果；领域边界先迁移现有 integration 到 fate-core adapter/provider；入口一致性优先复用已有 CapabilityExecutor/calculate_pure_analysis。

# Split Strategy
按 REVIEW-0001 finding 分包：PRECHECK、F-001、F-002/F-003、F-004、F-005、VERIFY/CLOSEOUT。每个包只处理一个业务风险面，并以测试和 scan 证明完成。

# Execution Waves
- Wave 1: TP-01.01, TP-01.02
- Wave 2: TP-01.03
- Wave 3: TP-02.01, TP-03.01, TP-05.01
- Wave 4: TP-02.02, TP-03.02, TP-03.03, TP-05.02
- Wave 5: TP-02.03, TP-03.04
- Wave 6: TP-04.01
- Wave 7: TP-04.02
- Wave 8: TP-04.03
- Wave 9: TP-06.01
- Wave 10: TP-06.02
- Wave 11: TP-06.03

# Runtime Workflow Contract
- workflow artifact 必须存入任务目录，而不是只留在聊天上下文。
- worker 只能消费当前 packet 的最小上下文、允许工具、禁止动作、证据要求和停止条件。
- verifier / 自审必须独立挑战关键发现，不能把 worker 自评当作验收。
- integrator / closeout 必须报告 verified、rejected、unresolved、failed、not-covered。
- 全局停止条件: 迁移 adapter 后基础排盘或紫微报告无法通过现有 golden/API 回归。
- 全局停止条件: 发现非默认业务选项已有外部契约必须支持但当前实现无法证明正确。
- 全局停止条件: Bot 用户命令格式需要破坏性修改。
- 全局停止条件: 治理索引脚本继续批量改写 archive 文件且原因不清。
- 需要审批: 删除公开 API 字段或改变字段名称。
- 需要审批: 删除兼容 facade 或历史 import 路径。
- 需要审批: 引入新生产依赖。
- 需要审批: 把 lunar/DST/late midnight 真实实现纳入本轮，而不是先 422 拒绝。

# Next Executable Leaves
- TP-01.01 | Wave 1 | Depends On: 无 | Gate: 无业务源码 dirty diff；治理变更清单完整记录。
- TP-01.02 | Wave 1 | Depends On: 无 | Gate: 每个 finding 有当前失败证据或说明已被其他变更修复。

# Dependency Graph
TP-01.01 -> TP-01.03
TP-01.02 -> TP-01.03
TP-01.03 -> TP-02.01
TP-01.03 -> TP-02.02
TP-02.01 -> TP-02.02
TP-01.03 -> TP-02.03
TP-02.02 -> TP-02.03
TP-01.03 -> TP-03.01
TP-01.03 -> TP-03.02
TP-03.01 -> TP-03.02
TP-01.03 -> TP-03.03
TP-03.01 -> TP-03.03
TP-01.03 -> TP-03.04
TP-03.02 -> TP-03.04
TP-03.03 -> TP-03.04
TP-02.01 -> TP-04.01
TP-02.02 -> TP-04.01
TP-02.03 -> TP-04.01
TP-03.01 -> TP-04.01
TP-03.02 -> TP-04.01
TP-03.03 -> TP-04.01
TP-03.04 -> TP-04.01
TP-02.01 -> TP-04.02
TP-02.02 -> TP-04.02
TP-02.03 -> TP-04.02
TP-03.01 -> TP-04.02
TP-03.02 -> TP-04.02
TP-03.03 -> TP-04.02
TP-03.04 -> TP-04.02
TP-04.01 -> TP-04.02
TP-02.01 -> TP-04.03
TP-02.02 -> TP-04.03
TP-02.03 -> TP-04.03
TP-03.01 -> TP-04.03
TP-03.02 -> TP-04.03
TP-03.03 -> TP-04.03
TP-03.04 -> TP-04.03
TP-04.02 -> TP-04.03
TP-01.03 -> TP-05.01
TP-01.03 -> TP-05.02
TP-05.01 -> TP-05.02
TP-02.01 -> TP-06.01
TP-02.02 -> TP-06.01
TP-02.03 -> TP-06.01
TP-03.01 -> TP-06.01
TP-03.02 -> TP-06.01
TP-03.03 -> TP-06.01
TP-03.04 -> TP-06.01
TP-04.01 -> TP-06.01
TP-04.02 -> TP-06.01
TP-04.03 -> TP-06.01
TP-05.01 -> TP-06.01
TP-05.02 -> TP-06.01
TP-02.01 -> TP-06.02
TP-02.02 -> TP-06.02
TP-02.03 -> TP-06.02
TP-03.01 -> TP-06.02
TP-03.02 -> TP-06.02
TP-03.03 -> TP-06.02
TP-03.04 -> TP-06.02
TP-04.01 -> TP-06.02
TP-04.02 -> TP-06.02
TP-04.03 -> TP-06.02
TP-05.01 -> TP-06.02
TP-05.02 -> TP-06.02
TP-06.01 -> TP-06.02
TP-02.01 -> TP-06.03
TP-02.02 -> TP-06.03
TP-02.03 -> TP-06.03
TP-03.01 -> TP-06.03
TP-03.02 -> TP-06.03
TP-03.03 -> TP-06.03
TP-03.04 -> TP-06.03
TP-04.01 -> TP-06.03
TP-04.02 -> TP-06.03
TP-04.03 -> TP-06.03
TP-05.01 -> TP-06.03
TP-05.02 -> TP-06.03
TP-06.02 -> TP-06.03

# Rollback Protocol
- 恢复 `INDEX.md` 当前任务行
- 恢复本任务目录到初始化状态
- 不得影响其他任务目录
