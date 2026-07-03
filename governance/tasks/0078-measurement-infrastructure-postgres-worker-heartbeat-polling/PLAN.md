# Planning Summary

0078 执行 post-0076 后第一个本地可执行 P0 实现切片：为 Postgres report job worker 补齐 heartbeat/renew 和 DB polling，使长任务执行期间 lease 可续约、manager 启动后能轮询外部 seeded queued/running replayable jobs，并通过 Postgres smoke 证明 stuck job recovery 与 duplicate claim 防护仍成立。

# Lifecycle Gates

禁止跳过任何 gate；如果某个 gate 失败，0078 不能标记 Done。

| Phase | Gate | Status |
| --- | --- | --- |
| SPEC | 范围限定为 worker heartbeat/polling，不声明生产 ready | Done |
| PLAN | 任务树和验收写入 0078 文档 | Done |
| BUILD | Store renew、manager polling/heartbeat、smoke、contract/docs/tests | Done |
| TEST | focused tests、runtime backend gate、allow-missing smoke、quick CI | Done |
| REVIEW | 不过度声明 exactly-once/public webhook live/Vault-KMS | Done |
| SHIP | commit/push/CI evidence | Done |

# Future-Optimal Contract

- target end state: CalculationJob worker runtime 具备 external backend polling、lease heartbeat、restart recovery、event history、idempotent delivery 和 audit evidence。
- real constraints: 真实长期多副本、public webhook passed、Vault/KMS、exactly-once 需要外部环境和后续任务。
- inertia constraints: 现有 manager 是 Thread/Queue 实现，不因此引入 heavyweight orchestrator；也不让旧内存队列阻止 external backend polling。
- kill list: 单次 restart smoke 伪装长期 worker、lease primitive 伪装 heartbeat、polling 缺失导致外部 queued job 永远不执行。
- proof point: Postgres heartbeat/polling smoke 能证明长任务 renew、外部 queued job polling、stuck running job recovery。
- falsifier: smoke 无法阻止错误 worker 在长任务 lease 原 TTL 后抢占，或无法执行 manager 启动后的外部 queued job。
- migration slice: 在现有 Postgres adapter 上补 worker hardening，为后续长期多副本运行和 release proof 铺路。
- rejected short-term patches: 不只更新文档，不只调整 sleep，不用单次 restart smoke 替代 polling，不把 exactly-once 写进 contract。

# Ponytail Contract

- existence check: 0077 0.10 队列明确 0078 是下一个本地可执行 P0 缺口。
- selected ladder rung: 项目内直接实现，复用现有 Postgres adapter、Thread、Queue 和 smoke pattern。
- skipped scope: Temporal/Celery/Redis Queue、production deployment、external secrets、real webhook endpoint。
- ceiling / upgrade path: 当需要长期多副本 SLA、严格 exactly-once 或复杂 workflow 时，应引入 dedicated orchestrator 或 queue backend。
- do-not-simplify: lease owner isolation、blocked summary 脱敏、外部验证待执行口径不能省略。
- minimal runnable check: allow-missing smoke + focused pytest + runtime backend gate + quick CI。
- complexity review owner: `auto-review` document-drift/future-optimal-drift/ponytail-complexity。

# Document-Driven Contract

- Operating model update: not needed；项目定位不变。
- Toolchain model update: updated if local-ci adds a new smoke artifact.
- Process update: not needed；仍按 existing smoke/gate/local-ci 流程。
- Source-of-truth updates: runtime backend contract、operations docs、task docs。
- Local README/AGENTS impact: scripts/domain/contracts docs touched if behavior changes。
- Contract/catalog/schema impact: runtime backend contract/gate/schema if implementationStatus changes。
- ADR/Gate/module-context impact: not needed unless new runtime concept escapes current module.
- Documentation exemption reason: 无。
- Validation evidence: focused tests、quick CI、task validators。

# Simplest Path

在 `ReportJobStore` 增加 no-op renew 接口，在 `PostgresReportJobStore` 增加 owner/status 限定 renew SQL；`ReportJobManager` 用轻量 daemon heartbeat thread 续租执行中的 job，并在 worker loop 空闲时定期 poll store 中带 payload 的 queued/running jobs。

# Split Strategy

- Store primitive 先落地，确保 renew 语义清晰。
- Manager 再接 polling 和 heartbeat。
- Smoke 用真实/一次性 Postgres 验证；无 DSN 时 blocked summary。
- Contract/docs/tests 最后统一接线并跑 gates。

# Execution Waves

| Wave | Leaves | Purpose | Status |
| --- | --- | --- | --- |
| 1 | TP-01.01, TP-01.02 | 现状复核 | Done |
| 2 | TP-02.01, TP-02.02 | Store primitive | Done |
| 3 | TP-03.01, TP-03.02, TP-03.03 | Manager runtime hardening | Done |
| 4 | TP-04.01, TP-04.02, TP-04.03 | Smoke/contract/docs | Done |
| 5 | TP-05.01, TP-05.02, TP-05.03 | Tests/closeout/Git | Done |

# Runtime Workflow Contract

| Field | Value |
| --- | --- |
| allowed tools | `rg`、`sed`、`apply_patch`、pytest、ruff、local-ci、git/gh |
| forbidden actions | 不改业务算法、不读取真实 secret、不伪造 live evidence、不声明 exactly-once |
| required evidence | smoke blocked summary、focused tests、runtime backend gate、task validators、Git/CI evidence |
| stop condition | 真实 DSN/endpoint 缺失时只阻止 live path，不阻止 allow-missing/local-ci baseline |

# Next Executable Leaves

| Node ID | Action |
| --- | --- |
| - | - |

# Dependency Graph

```text
TP-01.01 -> TP-01.02 -> TP-02.01 -> TP-02.02 -> TP-03.01 -> TP-03.02 -> TP-03.03 -> TP-04.01 -> TP-04.02 -> TP-04.03 -> TP-05.01 -> TP-05.02 -> TP-05.03
```

# Rollback Protocol

- 恢复 `report_jobs.py` 中 renew/polling/heartbeat 相关改动。
- 删除 `scripts/postgres-worker-heartbeat-polling-smoke.py` 和 `.sh`。
- 恢复 runtime backend contract/local-ci/docs/tests 相关接线。
- 恢复 `governance/tasks/INDEX.md` 中 0078 行和任务目录。
