# Planning Summary

0075 执行 0.9 计划的第二个 P0 能力：crash/restart external backend worker。0074 已证明 Postgres job execution lease primitive，但 `ReportJobManager._run_job()` 仍未在真实执行路径 claim。0075 要把 manager 执行路径接入 lease，并用真实 Postgres 证明 stale running job 的 expired lease 可被 restarted manager 恢复执行，且两个 manager 竞争时只有一个执行。

# Lifecycle Gates

禁止跳过任何 gate；如果某个 gate 失败，0075 不能标记 Done。

| Phase | Gate | Status |
| --- | --- | --- |
| SPEC | 明确本任务只覆盖 expired lease external backend worker restart smoke | In Progress |
| PLAN | 任务树、边界、high-risk fields、non-claims 和验证命令写入任务包 | In Progress |
| BUILD | Manager lease 接线、smoke、wrapper、contract、local-ci、docs 和 tests 完成 | Not Started |
| TEST | 语法、blocked preflight、real Postgres smoke、focused tests、local-ci 和 validators 执行 | Not Started |
| REVIEW | 确认不泄露 secret、不夸大 production ready、不引入无用抽象 | Not Started |
| SHIP | commit/push，刷新远端 CI evidence | Not Started |

# Future-Optimal Contract

- target end state: `CalculationJob` durable runtime 具备 external backend、worker coordination、crash recovery、event history、retry/outbox、webhook callback、secret lifecycle、observability 和审计证据。
- real constraints: 只有 disposable/真实 Postgres 可本地证明 external backend worker restart；公网 webhook、外部 Vault/KMS、生产多副本和 exactly-once 不在当前环境内。
- inertia constraints: 现有 manager 本地 queue 不能作为分布式事实；0074 job lease primitive 不能别名成 crash/restart worker。
- kill list: manager 执行绕过 claim、allow-missing 伪通过、production ready 夸大、exactly-once 伪声明。
- proof point: real Postgres smoke 输出 `status=passed`，execution count 为 1，persisted status 为 succeeded，expired lease recovery true。
- falsifier: 两个 manager 都执行、job 未成功、claim 失败仍执行、summary 出现敏感值。
- migration slice: 本轮新增 claim-before-execute 和 external worker restart smoke；下一轮处理 public webhook live 或 external secret provider。
- rejected short-term patches: 不引入 Temporal/Redis，不实现 polling/heartbeat，不用进程锁模拟 DB worker。

# Ponytail Contract

- existence check: 0.9 路线图明确 0074 后下一步是 crash/restart external backend worker；这是 external durable runtime 的必要 proof。
- selected ladder rung: 复用现有 `ReportJobManager`、`ReportJobStore` 和 Postgres 条件更新，项目内薄接线。
- skipped scope: heartbeat/renew、DB polling daemon、Temporal/Redis、exactly-once、公网 webhook、Vault/KMS、production deployment。
- ceiling / upgrade path: 仅证明 expired lease restart；后续需要 heartbeat、polling、public webhook live、external secret provider 和 production deployment。
- do-not-simplify: claim-before-execute、owner-matched release、sensitive summary protection、blocked preflight 不可删除。
- minimal runnable check: focused tests + disposable Postgres smoke + local-ci quick。
- complexity review owner: `auto-review`。

# Simplest Path

在 `ReportJobManager` 中增加 manager-scoped job execution lease owner / TTL；`_run_job()` 在执行 task 前调用 `store.claim_job_for_execution()`，claim 失败直接返回，claim 成功才写 `job.running` 并执行。terminal path 释放当前 owner lease。新增 smoke 脚本 seed 一个带 payload 的 stale running Postgres job，先用 dead worker claim 一个短 lease，等待过期后启动两个 manager，同一 job 只能被一个 manager 恢复执行成功。

# Split Strategy

- TP-01：PRECHECK，确认边界和数据流。
- TP-02：IMPLEMENT，manager 执行路径接入 job lease。
- TP-03：IMPLEMENT，补 Postgres external worker restart smoke。
- TP-04：VERIFY，接入 contract/docs/tests/local-ci。
- TP-05：CLOSEOUT，跑验证、审查、提交推送和远端 CI。

# Execution Waves

| Wave | Leaves | Purpose | Status |
| --- | --- | --- | --- |
| 1 | TP-01 | 锁定边界和 proof target | In Progress |
| 2 | TP-02 | 实现 manager claim-before-execute | Not Started |
| 3 | TP-03 | 实现 smoke 工具 | Not Started |
| 4 | TP-04 | 接线 contract/docs/tests/local-ci | Not Started |
| 5 | TP-05 | 验证和交付 | Not Started |

# Runtime Workflow Contract

| Field | Value |
| --- | --- |
| allowed tools | `rg`、`sed`、`python -m py_compile`、`bash -n`、`pytest`、Docker Postgres、local-ci、task validators、git/gh after auto-github |
| forbidden actions | 不切分支、不删除数据、不输出 DSN/secret、不把 blocked artifact 写成 passed、不声明 production ready/exactly-once |
| required evidence | blocked preflight JSON、real Postgres smoke JSON、focused tests、local-ci quick、task docs validator、remote CI |
| stop condition | 无法获取 Postgres 时不得 closeout；必须使用一次性 Docker Postgres 或真实 DSN 跑 real smoke。 |

# Next Executable Leaves

| Node ID | Action |
| --- | --- |
| TP-01 | 完成 precheck 并开始 manager lease 接线。 |

# Dependency Graph

```text
TP-01 -> TP-02 -> TP-03 -> TP-04 -> TP-05
```

# Rollback Protocol

- 恢复 `ReportJobManager._run_job()` 的旧执行路径和 lease owner 字段。
- 删除 `scripts/postgres-external-worker-restart-smoke.py` 和 `.sh`。
- 恢复 runtime backend contract/schema/gate/local-ci/docs/tests 中 external worker restart 接线。
- 保留 0070-0074 已完成的 Postgres adapter/live/outbox/job lease baseline。
