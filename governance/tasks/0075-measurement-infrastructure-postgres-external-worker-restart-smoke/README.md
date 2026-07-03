# Task Overview

- Task ID: `0075`
- Slug: `measurement-infrastructure-postgres-external-worker-restart-smoke`
- Objective: 执行 MI-100.01 Durable Runtime 的 crash/restart external backend worker 切片：在 0074 Postgres job execution worker lease primitive 之后，将 `ReportJobManager` 执行路径接入 job execution lease，并新增真实或一次性 Postgres smoke，证明带 `task_payload` 的 stale running job 在 worker crash、lease expiry、restart 后可由 external backend 恢复执行，且两个 manager 并发恢复时只有一个执行成功；不得声明 exactly-once、公网 webhook live、外部 Vault/KMS 或 production ready。
- Status: `Done`

## In Scope

- 让 `ReportJobManager._run_job()` 在执行前通过 `ReportJobStore.claim_job_for_execution()` 获取 job execution lease。
- 为 manager 增加内部 job execution lease owner / TTL，默认保持 memory/sqlite 兼容。
- 新增 Postgres external worker restart smoke：用一次性 schema、真实 Postgres 连接、两个 manager、stale running job 和 task factory 验证恢复执行。
- 同步 runtime backend contract、schema/gate/local-ci、operations docs、roadmap、AGENTS 和 regression tests。
- 修正 `0074` 在 `governance/tasks/INDEX.md` 的状态漂移。

## Out of Scope

- 不实现 exactly-once。
- 不实现公网 webhook live smoke。
- 不接入外部 Vault/KMS 或生产 secret manager。
- 不实现长期 heartbeat/renew、后台 DB polling worker 或 Temporal worker。
- 不声明 production ready 或 multi-replica ready。

## Task Package Tree

```text
TP-01 PRECHECK：边界、数据流和执行语义审查
TP-02 IMPLEMENT：ReportJobManager job execution lease 接线
TP-03 IMPLEMENT：Postgres external worker restart smoke
TP-04 VERIFY：契约、文档、AGENTS、local-ci 与回归测试接线
TP-05 CLOSEOUT：验证、审查、提交推送和远端 CI 证据
```

## Requirement Alignment

| Requirement | Handling |
| --- | --- |
| crash/restart external backend worker | 用 Postgres stale running job + expired lease + 两个 manager 恢复执行 smoke 证明。 |
| job execution lease primitive 必须被真实执行路径使用 | `_run_job()` 执行前必须 claim；claim 失败不执行 task。 |
| 多 manager 只能一个执行 | smoke 的 execution count 必须为 1，persisted result 只能来自一个 manager。 |
| 不夸大生产结论 | contract、docs 和 smoke summary 保留 `shipGate.status=blocked` 与 non-claims。 |
| 隐私安全 | summary 不输出 DSN、用户名、密码、callback URL、secret、报告正文或用户输入。 |

## Task Package Overview

| Node ID | Status | Purpose |
| --- | --- | --- |
| TP-01 | Done | 锁定边界、当前代码事实、风险字段和 proof target。 |
| TP-02 | Done | 将 manager 执行路径接入 store lease。 |
| TP-03 | Done | 新增真实 Postgres crash/restart smoke。 |
| TP-04 | Done | 同步 contract/docs/tests/local-ci/AGENTS。 |
| TP-05 | Done | 跑完整验证、closeout、本地 quick CI；远端 CI 等 commit/push 后刷新。 |

## Reading Order

1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
