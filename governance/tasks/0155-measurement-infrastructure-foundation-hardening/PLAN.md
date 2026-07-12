# Planning Summary
先把可交付对象收敛为可独立运行的最小闭包，再统一计算真相源和渠道健康语义，随后补自动 CI、供应链与治理门禁，最后用性能和质量证据收口。
- 编译节点总数: 7
- 叶子执行项: 7
- 执行波次数: 7
- 当前任务必须遵守 `SPEC -> PLAN -> BUILD -> TEST -> REVIEW -> SHIP`

# Lifecycle Gates
以下 gate 不得跳过；任一阶段失败必须回到对应切片修复并重新验证。

- SPEC：目标终态、真实约束、外部门禁和兼容边界明确
- PLAN：七个切片、验证命令、回滚路径和文档影响已登记
- BUILD：实现只进入已登记模块，不扩展业务体系
- TEST：定向回归、clean-room smoke、quick CI 和卫生门禁通过
- REVIEW：correctness/security/reliability/performance/architecture/document drift 无 BLOCK
- SHIP：语义提交、推送、当前提交 CI 证据和外部待验证项明确

# Simplest Path
复用 Python importlib.resources、现有 CapabilityExecutor、GitHub Actions 与现有 gate 脚本；删除整仓复制和双引擎默认值等错误概念，不新增平行框架。

# Split Strategy
按独立失败边界拆成七个串行可验证切片，每个切片先补失败测试，再做最小实现并更新对应契约。

# Execution Waves
- Wave 1: TP-01
- Wave 2: TP-02
- Wave 3: TP-03
- Wave 4: TP-04
- Wave 5: TP-05
- Wave 6: TP-06
- Wave 7: TP-07

# Runtime Workflow Contract
- workflow artifact 必须存入任务目录，而不是只留在聊天上下文。
- worker 只能消费当前 packet 的最小上下文、允许工具、禁止动作、证据要求和停止条件。
- verifier / 自审必须独立挑战关键发现，不能把 worker 自评当作验收。
- integrator / closeout 必须报告 verified、rejected、unresolved、failed、not-covered。

# Next Executable Leaves
- 无新的 Not Started 叶子；当前活动节点为 TP-04 与 TP-07。

# Dependency Graph
TP-01 -> TP-02
TP-02 -> TP-03
TP-03 -> TP-04
TP-04 -> TP-05
TP-05 -> TP-06
TP-06 -> TP-07

# Rollback Protocol
- 分发资源变化可回滚到上一版 manifest，禁止同时维护新旧资源发现逻辑。
- 八字引擎迁移通过兼容接口委托 capability 回滚，不恢复双引擎默认分支。
- Telegram 分层 readiness 可恢复为渠道 disabled，但不得掩盖渠道状态。
- CI 触发变化可单独回滚，不改写已经发布的提交历史。
