# Planning Summary

0074 执行 0.9 计划的首个 P0 能力：Postgres job execution worker lease。0072 已证明 webhook outbox 的 duplicate claim 负例，但报告 job 本身仍由进程内队列取出执行，Postgres adapter 没有 queued/running job 的跨 worker claim/release primitive。本任务补齐最小 job lease primitive 和可重复 smoke，为后续 crash/restart external backend worker 做准备。

# Lifecycle Gates

禁止跳过任何 gate；如果某个 gate 失败，0074 不能标记 Done。

| Phase | Gate | Status |
| --- | --- | --- |
| SPEC | 明确本任务只覆盖 Postgres job execution worker lease primitive | Done |
| PLAN | 任务树、边界、high-risk fields、non-claims 和验证命令写入任务包 | Done |
| BUILD | Store 接口、Postgres 实现、smoke、wrapper、contract、local-ci、docs 和 tests 完成 | Done |
| TEST | 语法、blocked preflight、real Postgres smoke、focused tests、local-ci 和 validators 执行 | Done |
| REVIEW | 确认不泄露 secret、不夸大 production ready、不引入无用抽象 | Done |
| SHIP | commit/push，刷新远端 CI evidence | Done |

# Future-Optimal Contract

- target end state: `CalculationJob` durable runtime 具备 external backend、worker coordination、event history、retry/outbox、webhook callback、secret lifecycle、observability 和审计证据。
- real constraints: 只有 disposable/真实 Postgres 可本地证明 primitive；公网 webhook、外部 Vault/KMS、生产多副本和 exactly-once 不在当前环境内。
- inertia constraints: 现有 manager 进程内 queue 不能作为分布式事实；0072 outbox lease 不能别名成 job lease。
- kill list: docs-only job lease、sleep-based lock、allow-missing 伪通过、production ready 夸大、exactly-once 伪声明。
- proof point: real Postgres smoke 输出 `status=passed`，duplicate claim winner count 为 1，wrong owner release blocked，expiry reclaim true，terminal unclaimable true。
- falsifier: 任一 race 出现两个 winner、terminal job 被 claim、wrong owner release 清掉 active lease、summary 出现敏感值。
- migration slice: 本轮新增 Postgres job lease primitive；下一轮实现 crash/restart external backend worker。
- rejected short-term patches: 不引入 Temporal/Redis，不改默认 manager 执行模型，不用进程锁模拟 DB worker。

# Ponytail Contract

- existence check: 0.9 路线图明确下一步是 job execution worker lease；这是 external durable runtime 的必要 primitive。
- selected ladder rung: 复用 Postgres 条件更新能力和现有 `ReportJobStore` 抽象，项目内薄适配。
- skipped scope: heartbeat/renew、crash worker、exactly-once、公网 webhook、Vault/KMS、production deployment。
- ceiling / upgrade path: 仅有 primitive 仍不能 production ready；后续需要 worker 从 DB claim 并执行、crash restart、续租、幂等语义和外部 live。
- do-not-simplify: owner-matched release、terminal non-claim、sensitive summary protection、blocked preflight 不可删除。
- minimal runnable check: focused tests + disposable Postgres smoke + local-ci quick。
- complexity review owner: `auto-review`。

# Simplest Path

在现有 `ReportJobStore` 上增加 `claim_job_for_execution(job, lease_owner, lease_seconds)` 与 `release_job_execution_lease(job_id, lease_owner)`；默认 store 返回原 job / no-op 以保持兼容，Postgres store 使用 `UPDATE report_jobs ... WHERE job_id/status/lease` + `RETURNING` 原子 claim。新增 smoke 脚本验证 primitive，不改 `ReportJobManager` 从队列取任务的现有执行路径。

# Split Strategy

- TP-01：PRECHECK，确认边界和数据流。
- TP-02：IMPLEMENT，补 Store/Postgres job lease。
- TP-03：IMPLEMENT，补 smoke 脚本和 wrapper。
- TP-04：VERIFY，接入 contract/docs/tests/local-ci。
- TP-05：CLOSEOUT，跑验证、审查、提交推送和远端 CI。

# Execution Waves

| Wave | Leaves | Purpose | Status |
| --- | --- | --- | --- |
| 1 | TP-01 | 锁定边界和 proof target | Done |
| 2 | TP-02 | 实现 Store/Postgres primitive | Done |
| 3 | TP-03 | 实现 smoke 工具 | Done |
| 4 | TP-04 | 接线 contract/docs/tests/local-ci | Done |
| 5 | TP-05 | 验证和交付 | Done |

# Runtime Workflow Contract

| Field | Value |
| --- | --- |
| allowed tools | `rg`、`sed`、`python -m py_compile`、`bash -n`、`pytest`、Docker Postgres、local-ci、task validators、git/gh after auto-github |
| forbidden actions | 不切分支、不删除数据、不输出 DSN/secret、不把 blocked artifact 写成 passed、不声明 production ready/exactly-once |
| required evidence | blocked preflight JSON、real Postgres smoke JSON、focused tests、local-ci quick、secret scan、task docs validator、remote CI |
| stop condition | 无法获取 Postgres 时不得 closeout；必须使用一次性 Docker Postgres 或真实 DSN 跑 real smoke。 |

# Next Executable Leaves

| Node ID | Action |
| --- | --- |
| - | 无剩余本地 executable leaf；远端 CI evidence 在 commit/push 后刷新。 |

# Dependency Graph

```text
TP-01 -> TP-02 -> TP-03 -> TP-04 -> TP-05
```

# Rollback Protocol

- 删除 `scripts/postgres-job-worker-lease-smoke.py` 和 `.sh`。
- 恢复 `report_jobs.py` 中 job lease 接口/SQL/columns。
- 恢复 runtime backend contract/schema/gate/local-ci/docs/tests 中 job worker lease 接线。
- 保留 0070-0072 已完成的 Postgres adapter/live/outbox lease baseline。
