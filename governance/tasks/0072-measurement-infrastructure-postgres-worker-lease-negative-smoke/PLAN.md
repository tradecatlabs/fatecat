# Planning Summary

0072 收口 Postgres durable runtime 的下一块不可伪造证据：在 0071 真实数据库 schema/job/outbox/config live smoke 之后，用真实或一次性 Postgres 验证 webhook outbox lease 在多 worker 竞争下具备 duplicate claim 负例、错误 owner release 负例和 lease expiry reclaim。它提升 external backend 可信度，但仍不等于 job execution worker lease、exactly-once、公网 webhook live 或外部 Vault/KMS。

# Lifecycle Gates

禁止跳过任何 gate；如果某个 gate 失败，0072 不能标记 Done。

| Phase | Gate | Status |
| --- | --- | --- |
| SPEC | 明确本任务只覆盖 Postgres webhook outbox worker lease negative smoke | Done |
| PLAN | 任务树、边界、non-claims 和验证命令写入任务包 | Done |
| BUILD | 脚本、wrapper、contract、local-ci、docs 和测试接线完成 | Done |
| TEST | 语法、blocked preflight、real Postgres smoke、focused tests、local-ci 和 validators 执行 | Done |
| REVIEW | 确认不泄露 secret、不夸大 production ready | Done |
| SHIP | 本地可提交；远端 CI 在 commit/push 后刷新 | Pending |

# Future-Optimal Contract

- target end state: `CalculationJob` durable runtime 具备 external backend、worker coordination、event history、retry/outbox、webhook callback、secret lifecycle 和审计证据。
- real constraints: 当前只有 disposable/真实 Postgres smoke；缺公网 webhook receiver、外部 Vault/KMS、生产多副本 worker 和 exactly-once 证明。
- inertia constraints: 不能把 SQLite local lease 或 Postgres outbox lease smoke 扩大解释成 job execution worker lease。
- kill list: DSN 泄露、allow-missing 伪通过、production ready 夸大、exactly-once 伪声明。
- proof point: real Postgres smoke 输出 `status=passed`，所有 duplicate claim winner count 为 1，shipGate 仍 blocked。
- falsifier: summary 出现 raw DSN/secret，或 race 中 winner count 不是 1。
- migration slice: 完成后下一任务转入 job execution worker lease 或 public webhook live。

# Simplest Path

复用既有 `PostgresReportJobStore` 和 webhook outbox claim/release API，不新增生产 worker 抽象；新增一个独立 smoke 脚本和 wrapper，并把证据路径接入 runtime backend gate、local-ci 和文档。

# Split Strategy

- TP-01：确认 0071 后缺口和本任务 non-claims。
- TP-02：实现 worker lease negative smoke。
- TP-03：同步 contract、docs、AGENTS 和 regression。
- TP-04：执行验证、closeout 和交付。

# Execution Waves

| Wave | Leaves | Purpose | Status |
| --- | --- | --- | --- |
| 1 | TP-01 | 锁定边界和证据目标 | Done |
| 2 | TP-02 | 实现脚本和 wrapper | Done |
| 3 | TP-03 | Contract/docs/tests 接线 | Done |
| 4 | TP-04 | 验证和 closeout | Done |

# Runtime Workflow Contract

| Field | Value |
| --- | --- |
| allowed tools | `rg`、`sed`、`python -m py_compile`、`bash -n`、`pytest`、Docker Postgres、local-ci、task validators |
| forbidden actions | 不切分支、不删除数据、不输出 DSN/secret、不把 blocked artifact 写成 passed、不声明 external backend production ready |
| required evidence | blocked preflight JSON、real Postgres smoke JSON、focused tests、local-ci quick、task docs validator |
| stop condition | 无法获取 Postgres 时仍可完成 allow-missing preflight，但 real smoke 未跑时不得 closeout；本轮已使用一次性 Postgres 跑通。 |

# Next Executable Leaves

| Node ID | Action |
| --- | --- |
| None | 0072 本地任务已完成；后续执行 Git 交付和远端 CI。 |

# Dependency Graph

```text
TP-01 -> TP-02 -> TP-03 -> TP-04
```

# Rollback Protocol

- 删除 `scripts/postgres-worker-lease-smoke.py` 和 `.sh`。
- 恢复 runtime backend contract、schema、registry、gate、local-ci 和 focused tests 中的 worker lease smoke 接线。
- 恢复 operations docs、roadmap、AGENTS 和 task index。
- 不回滚 0071 Postgres live smoke baseline。
