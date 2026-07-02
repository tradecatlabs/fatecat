# Task Context

## Repo Evidence

- 当前分支：`main`
- 最新提交：`f63cc60 feat: add webhook outbox persistence baseline`
- 0055 已完成 SQLite manager rebuild 的 restart-safe failure smoke：无 callable 的旧 active job 会安全标记为 failed。
- 0056 已完成 SQLite persistent webhook outbox record baseline。
- roadmap 当前仍列出 `external backend`、`生产级分布式 worker lease` 和 `跨进程 webhook 自动重投` 为 `MI-NEXT-03` 剩余缺口。
- `report_jobs.py` 当前 `_ReportJob.task` 是 Python callable；SQLite 重建时默认无法恢复执行。
- Web/Markdown report job 的输入来自结构化表单 / `BaziRequest`，可通过 `task_payload` 和 factory 重建 callable。

## Constraints Matrix

| 约束 | 处理方式 |
| --- | --- |
| 不序列化 Python callable | 只持久化 dict 型 `task_payload`，重建时通过注册 factory 创建 callable。 |
| 不保存 webhook secret | `task_payload` 不包含 webhook URL、webhook secret 或 callback 配置。 |
| 不保存报告正文 | payload 只保存执行输入，不保存 Markdown result。 |
| 兼容 0055 | 缺 payload 或缺 factory 的 active job 继续 `job.recovered_failed`。 |
| quick CI 可重复 | smoke 使用临时 SQLite 和固定 factory，不访问公网。 |
| 默认 behavior 稳定 | memory store 兼容；无 payload 的旧任务仍按旧逻辑安全失败。 |

## Change Boundary

允许修改：

- `domains/experience-delivery/services/fatecat-delivery/src/report_jobs.py`
- `domains/experience-delivery/services/fatecat-delivery/src/main.py`
- `scripts/report-job-replayable-recovery-smoke.py`
- `scripts/report-job-replayable-recovery-smoke.sh`
- `scripts/local-ci.sh`
- `tests/regression/test_api_contracts.py`
- `tests/regression/test_report_job_replayable_recovery_smoke.py`
- API/roadmap/scripts/tests AGENTS 文档。
- `governance/tasks/0057-*` 和 `governance/tasks/INDEX.md`。

不允许修改：

- 命理计算核心、provider、report markdown 结构。
- webhook URL 校验策略或 secret 存储策略。
- external backend、生产多副本 worker lease、真实公网 webhook live smoke。
- Web HTML 视觉、Bot 文案或生产 secret。

## Risk Matrix

| 风险 | 影响 | 控制 |
| --- | --- | --- |
| replayable baseline 被误读成分布式 worker | 审计风险 | 文档和 smoke boundary 写明只是本地 SQLite + factory baseline。 |
| payload 泄露 secret 或报告正文 | 安全风险 | payload 不接 webhook 配置；smoke/secret scan 检查 summary 脱敏。 |
| 破坏 0055 安全失败语义 | 可靠性风险 | regression 同时覆盖 non-replayable active job failed。 |
| manager init 自动启动恢复任务引入竞态 | 稳定性风险 | 只有恢复到队列的任务才启动 worker；focused tests 锁住。 |
| SQLite migration 影响旧 DB | 升级风险 | 使用 `_ensure_column`，只新增可空列。 |

## Assumptions and Falsification

- 假设：Web/Markdown 生产报告任务可以通过结构化 payload 重建执行。
  - 推翻条件：任务需要不可序列化上下文、真实 request 对象或 secret 才能执行，则必须回退到 failed 或升级 external backend。
- 假设：本地 SQLite replayable recovery 是 external backend 前的合理台阶。
  - 推翻条件：要求多副本抢占、exactly-once 或跨机器恢复，则必须引入 worker lease / external backend，本任务不冒充。
- 假设：payload 保存用户提交的报告输入是任务恢复必要状态。
  - 推翻条件：后续 privacy policy 要求输入不可落库，则必须改为 encrypted payload 或外部 secret/data vault。

## Critical Ambiguities

- external backend 具体选型仍未决策。
- 生产 worker lease、抢占锁、租约续期和幂等投递不在本任务内。
- webhook 自动重投需要持久 callback config 与 secret 加密方案，仍未决策。

## Debug Evidence Contract

- 调试模式: Optional
- 若 replayable recovery 与 restart-safe failure 语义冲突，必须记录最小复现、根因、修复和回归证据。

## Task Package Context Map

| Node ID | Context |
| --- | --- |
| TP-01.01 | 读取 roadmap、0055/0056、report job 源码、API submit 路径和测试。 |
| TP-02.01 | 修改 report job store 和 SQLite schema。 |
| TP-02.02 | 修改 manager 重建恢复逻辑。 |
| TP-02.03 | 修改 Web/Markdown submit 路径。 |
| TP-03.01 | 新增 replayable recovery smoke。 |
| TP-03.02 | 新增 regression tests。 |
| TP-03.03 | 修改 `scripts/local-ci.sh`。 |
| TP-04.01 | 修改文档、AGENTS 和 INDEX。 |
| TP-04.02 | 运行 validators、pytest、ruff、secret scan、local-ci 和 git 检查。 |
