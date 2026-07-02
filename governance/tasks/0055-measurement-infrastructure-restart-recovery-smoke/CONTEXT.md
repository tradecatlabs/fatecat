# Task Context

## Repo Evidence

- 当前分支：`main`
- 最新提交：`505a00d feat: add webhook callback retry trail`
- 0052 已完成 report job event history 首切片。
- 0053 已完成 report job 本地 retry/timeout policy 首切片。
- 0054 已完成本地 webhook callback retry/outbox trail 首切片。
- roadmap 当前仍列出 `restart recovery smoke`、`persistent callback outbox` 和 `external backend` 为 `MI-NEXT-03` 剩余缺口。
- `tests/regression/test_api_contracts.py` 已有 SQLite manager rebuild 行为测试，但尚无独立 smoke 脚本或 local-ci 门禁。
- 当前 workflow 只有 `workflow_dispatch`，push 不自动产生 GitHub Actions run；本地验证必须如实记录。

## Constraints Matrix

| 约束 | 处理方式 |
| --- | --- |
| 不伪装成跨进程继续执行 | smoke 只证明未完成任务在 manager rebuild 后被显式标记 failed。 |
| 不新增外部 runtime | 复用 `SQLiteReportJobStore` 和 `ReportJobManager`。 |
| 不泄露用户输入 | smoke 输出只含 job status、event types、布尔检查和隐私说明。 |
| quick CI 应可重复 | 使用临时目录 SQLite 文件，不依赖全局 runtime DB。 |
| 不能破坏现有 unit tests | 脚本只新增独立入口，不改 report job 状态机。 |

## Change Boundary

允许修改：

- `scripts/report-job-restart-recovery-smoke.py`
- `scripts/report-job-restart-recovery-smoke.sh`
- `scripts/local-ci.sh`
- `tests/regression/test_report_job_restart_recovery_smoke.py`
- API/roadmap/scripts AGENTS 文档。
- `governance/tasks/0055-*` 和 `governance/tasks/INDEX.md`。

不允许修改：

- 命理计算核心、provider、report markdown 结构。
- report job 状态机语义，除非 smoke 暴露真实 bug。
- external backend、持久 callback outbox、多副本 worker。
- Web HTML 视觉、Bot 文案或生产 secret。

## Risk Matrix

| 风险 | 影响 | 控制 |
| --- | --- | --- |
| smoke 误导为任务可恢复继续执行 | 审计风险 | 文档写明当前语义是 restart-safe failure，不是 resume execution。 |
| 测试线程未释放 | flaky 或资源泄漏 | task 使用 Event，manager rebuild 后立即释放原任务线程。 |
| 输出泄露用户输入 | 隐私风险 | summary 不输出 input_summary、Markdown、姓名、地区或 DB path secret。 |
| local-ci 变慢 | 开发体验下降 | smoke 使用单个临时 SQLite 文件和短超时。 |

## Assumptions and Falsification

- 假设：restart recovery 的本地最小验收是 manager rebuild 后旧 `running` / `queued` job 变为 failed 并写入 `job.recovered_failed`。
  - 推翻条件：设计要求未完成任务可继续执行，则必须进入 external backend 任务，不能用本地 SQLite smoke 代替。
- 假设：独立 smoke 比只靠 pytest 更适合进入 release gate。
  - 推翻条件：local-ci 执行时间或稳定性不可接受，则保留 pytest，smoke 改为 manual gate。
- 假设：同一 idempotency key 在 rebuild 后仍返回既有 failed job 是正确行为。
  - 推翻条件：产品要求重启后相同幂等键可新建任务，则需修改 idempotency 语义并另建任务。

## Critical Ambiguities

- external backend 具体选型仍未决策。
- restart 后是否要自动重新排队未完成任务属于后续 external backend 范围。
- 多副本锁和生产 worker 心跳不在本任务内。

## Debug Evidence Contract

- 调试模式: Optional
- 若 smoke 暴露 rebuild 行为不稳定，必须记录最小复现、根因、修复和回归证据。

## Task Package Context Map

| Node ID | Context |
| --- | --- |
| TP-01.01 | 读取 roadmap、0054、report job 源码、SQLite rebuild tests 和 local-ci。 |
| TP-02.01 | 新增 restart recovery Python smoke 与 shell wrapper。 |
| TP-02.02 | 修改 `scripts/local-ci.sh` 接入 quick。 |
| TP-03.01 | 新增 `tests/regression/test_report_job_restart_recovery_smoke.py`。 |
| TP-03.02 | 修改 API 文档、roadmap、scripts AGENTS 和 INDEX。 |
| TP-04.01 | 运行 validators、pytest、ruff、local-ci 和 git 检查。 |
