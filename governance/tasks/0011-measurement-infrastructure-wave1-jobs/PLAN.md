# Planning Summary
在不引入外部队列的前提下，把现有报告任务队列推进成基础设施资源：支持 TTL 内幂等、cancelled 状态、取消 API 和资源 links。

# Lifecycle Gates
- SPEC：明确单进程/TTL 边界，不宣称跨进程幂等。
- PLAN：拆成 job manager、API resource、tests/docs、validation。
- BUILD：复用现有 manager，不另造 job 系统。
- TEST：定向 pytest 验证幂等和 cancel 竞态。
- REVIEW：确认没有改变报告计算与默认 Markdown。
- SHIP：不自动提交；不得跳过 gate。

# Simplest Path
在 `_ReportJob` 增加 `idempotency_key`，在 manager 增加 idempotency index 和 cancel 方法，在 API payload 增加 resource links。

# Split Strategy
- TP-01 状态机。
- TP-02 API。
- TP-03 测试与文档。
- TP-04 验证。

# Execution Waves
- Wave A：TP-01.01、TP-01.02。
- Wave B：TP-02.01、TP-02.02。
- Wave C：TP-03.01、TP-03.02。
- Wave D：TP-04.01、TP-04.02。

# Runtime Workflow Contract
- 不切分新队列后端。
- 不改变用户报告内容。
- 并发测试必须覆盖 cancel 后结果丢弃。

# Next Executable Leaves
- TP-04.01

# Dependency Graph
```text
TP-01.01 -> TP-02.01 -> TP-03.01 -> TP-04.01 -> TP-04.02
TP-01.02 -> TP-02.02 -> TP-03.01 -> TP-04.01 -> TP-04.02
TP-03.02 -> TP-04.01
```

# Rollback Protocol
- 恢复 `INDEX.md` 当前任务行
- 恢复本任务目录到初始化状态
- 不得影响其他任务目录
