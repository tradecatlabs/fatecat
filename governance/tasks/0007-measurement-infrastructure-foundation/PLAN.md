# Planning Summary
以“先版本基线、再协议、再执行器、再样板、最后 API”的顺序推进，避免定位文档和运行时实现长期脱节。

# Lifecycle Gates
- 本任务必须按 `SPEC -> PLAN -> BUILD -> TEST -> REVIEW -> SHIP` 顺序推进，任何阶段不得跳过 gate；未满足 gate 时只能回到对应前置节点补证据。
- SPEC：本 README / CONTEXT / PLAN 已记录目标、边界和风险。
- PLAN：五阶段任务树与验收标准已落盘。
- BUILD：每阶段修改必须有对应测试或治理证据。
- TEST：至少运行 focused tests 和 `bash scripts/local-ci.sh --profile quick`。
- REVIEW：执行一致性扫描，确认旧“预测能力”主口径不回潮。
- SHIP：提交并推送当前分支；远端 CI 结果另行记录。

# Simplest Path
复用现有 `CapabilityExecutor`、`ReportJobManager`、`/ready`、`/metrics`、rate limiter 和 registry loader；只补缺失字段、provider map 和兼容 API 别名。

# Split Strategy
- Commit 1：定位基线、路线图、文档治理和任务容器。
- Commit 2：协议/执行器/API 基线和测试。
- Commit 3：如有必要，补审查/治理 closeout。

# Execution Waves
- Wave 1：TP-01，定位基线。
- Wave 2：TP-02 + TP-03，协议与执行器。
- Wave 3：TP-04 + TP-05，生产样板与 API。
- Wave 4：验证、提交、推送。

# Runtime Workflow Contract
- 不切换分支。
- 不执行 destructive git 操作。
- 每个阶段结束前运行最小验证。
- 若 quick CI 失败，先修复失败再继续提交。

# Next Executable Leaves
- TP-01.02
- TP-01.03
- TP-02.01

# Dependency Graph
- TP-01 -> TP-02 -> TP-03 -> TP-04 -> TP-05

# Rollback Protocol
- 恢复 `INDEX.md` 当前任务行
- 恢复本任务目录到初始化状态
- 不得影响其他任务目录
