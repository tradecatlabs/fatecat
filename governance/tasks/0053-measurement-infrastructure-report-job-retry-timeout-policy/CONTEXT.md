# Task Context

## Repo Evidence

- 当前分支：`main`
- 最新提交：`00ea769 feat: add report job event history`
- 0052 已完成 `CalculationJob event history` 首切片。
- roadmap 当前仍列出 `retry/timeout/non-retryable policy` 为 `MI-NEXT-03` 剩余缺口。
- report job 当前有 memory/sqlite store、TTL、cancel、idempotency、webhook baseline 和 event history。
- 当前 workflow 只有 `workflow_dispatch`，push 不自动产生 GitHub Actions run；本地验证必须如实记录。

## Constraints Matrix

| 约束 | 处理方式 |
| --- | --- |
| 默认行为不能破坏现有报告任务 | 默认 `maxAttempts=1`，timeout disabled，backoff 0。 |
| timeout 不能伪装成生产硬中断 | 文档写明当前是单进程本地任务状态 timeout baseline，底层 callable 不能被保证强杀。 |
| retry 不能重复不可重试错误 | 引入 non-retryable error 类型并写回事件证据。 |
| SQLite 旧库要兼容 | 通过 schema 增量列或默认值兼容旧 `report_jobs`。 |
| 不泄露用户输入 | events metadata 只记录 attempt、errorType、retryable、timeoutSeconds 等安全字段。 |

## Change Boundary

允许修改：

- `report_jobs.py` execution policy、状态机、SQLite schema。
- `main.py` env vars、manager 初始化、API payload。
- report job focused tests。
- production-readiness env validation。
- API/deployment/roadmap/AGENTS 文档。
- `governance/tasks/0053-*` 和 `governance/tasks/INDEX.md`。

不允许修改：

- 命理计算核心、provider、report markdown 结构。
- webhook callback retry/outbox。
- external backend 或生产部署 secret。
- Web HTML 视觉。

## Risk Matrix

| 风险 | 影响 | 控制 |
| --- | --- | --- |
| retry 导致副作用重复 | 用户收到重复外部副作用 | 当前 retry 仅作用 report job callable；默认 1 次；文档提醒生产副作用需 external backend/outbox。 |
| timeout 后底层线程继续运行 | 资源泄漏或重复计算 | 仅作为本地 baseline；timeout disabled by default；测试用短任务释放线程。 |
| 事件过度记录错误内容 | 隐私泄露 | 事件只记录 error type 和截断 message，不记录请求体/报告正文。 |
| SQLite schema 漂移 | 旧库不可读 | 增量列默认值并保留旧表读取。 |
| 误宣称 MI-NEXT-03 完成 | 审计风险 | 文档保留 callback retry/outbox、external backend、restart recovery 缺口。 |

## Assumptions and Falsification

- 假设：本切片可以把 retry/timeout policy 做成本地 baseline，不需要 external backend。
  - 推翻条件：现有状态机无法安全重试或测试证明会破坏默认路径，则缩小为 policy contract，不宣称 runtime 生效。
- 假设：timeout 采用独立 daemon attempt thread 可满足本地状态超时验证。
  - 推翻条件：测试出现不稳定或资源泄漏明显，则改成文档 contract + queued timeout，不做执行 timeout。
- 假设：report job callable 默认幂等，默认不启用 retry。
  - 推翻条件：业务侧明确不可重复执行，则默认保持 1 次，只允许显式配置 retry。

## Critical Ambiguities

- 生产硬 timeout 需要进程隔离或外部 worker，本任务不解决。
- callback retry/outbox 是否复用同一 policy：后续 0054 单独设计。
- external backend 使用 Temporal/Celery/Redis/Postgres 仍未决策。

## Debug Evidence Contract

- 调试模式: Optional
- 若 retry/timeout 测试 flaky，必须记录最小复现、根因、修复和回归证据。

## Task Package Context Map

| Node ID | Context |
| --- | --- |
| TP-01.01 | 读取 roadmap、0052、report job 源码、API 文档和 production-readiness。 |
| TP-02.01 | 修改 policy 模型、job 字段、SQLite schema 和 API serialization。 |
| TP-02.02 | 修改 `_run_job` 状态机，写入 retry/timeout/non-retryable events。 |
| TP-03.01 | 修改 `tests/regression/test_api_contracts.py`。 |
| TP-03.02 | 修改 docs、AGENTS、production-readiness 和 INDEX。 |
| TP-04.01 | 运行 validators、pytest、ruff、local-ci 和 git 检查。 |
