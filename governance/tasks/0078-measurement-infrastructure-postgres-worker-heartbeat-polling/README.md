# Task Overview

- Task ID: `0078`
- Slug: `measurement-infrastructure-postgres-worker-heartbeat-polling`
- Objective: `执行 0077 之后的首个本地可执行 P0 实现切片：为 Postgres report job worker 增加 job execution lease heartbeat/renew、DB polling、lease expiry backoff 与 stuck job recovery 的可验证 smoke，并接入 runtime backend contract、local-ci 和回归测试；无真实 DSN/psycopg/Postgres 时输出 blocked preflight，不声明 exactly-once、长期多副本生产 ready、公网 webhook live passed 或外部 Vault/KMS。`
- Status: `Done`

## In Scope

- `ReportJobStore` 增加 job execution lease renew/heartbeat 接口。
- `PostgresReportJobStore` 使用现有 lease columns 实现 renew SQL。
- `ReportJobManager` 支持 worker 空闲时从持久 store polling queued/running replayable jobs。
- `ReportJobManager` 支持执行中 heartbeat，防止长任务 lease 在任务未完成时被其他 worker 抢占。
- 新增 Postgres heartbeat/polling smoke、shell wrapper、regression tests、local-ci artifact 和 runtime backend contract/docs 更新。

## Out of Scope

- 不声明 exactly-once。
- 不声明长期多副本生产 ready。
- 不执行真实公网 webhook live passed。
- 不接入外部 Vault/KMS。
- 不引入 Temporal、Celery、Redis Queue 或其他新 runtime dependency。

## Task Package Tree

```text
TP-01 现状复核与任务定界
  TP-01.01 复核 0074/0075/0076 既有 runtime 证据和缺口
  TP-01.02 复核 report_jobs.py manager/store 改动点
TP-02 Store heartbeat primitive
  TP-02.01 为 ReportJobStore 增加 renew_job_execution_lease 默认接口
  TP-02.02 为 PostgresReportJobStore 增加 owner/status 受限 renew SQL
TP-03 Manager polling/heartbeat
  TP-03.01 增加 DB polling，把外部 queued/running replayable jobs 入内存队列
  TP-03.02 增加执行中 heartbeat thread 和 renewal failure event
  TP-03.03 增加 lease expiry backoff，claim 失败后不忙等
TP-04 Smoke、contract 和 docs
  TP-04.01 新增 postgres-worker-heartbeat-polling-smoke.py/.sh
  TP-04.02 接入 local-ci preflight artifact
  TP-04.03 更新 runtime backend contract/schema/gate/docs/AGENTS
TP-05 Tests and closeout
  TP-05.01 增加 regression tests
  TP-05.02 运行 focused gates、ruff/format 和 quick CI
  TP-05.03 回填任务 closeout、提交、推送并记录 CI
```

## Requirement Alignment

- 0077 `0.10.3` 推荐下一步是 `0078 Postgres worker heartbeat/polling hardening`。
- 0075 只证明 expired lease 后一次 restart recovery；仍不能证明长期 worker runtime。
- 0076 只证明 public webhook live smoke gate；真实外部 live passed 仍待执行。
- 本任务补齐本地可执行的 worker runtime hardening，不越界声明生产 ready。

## Task Package Overview

| Node ID | Title | Status | Verify |
| --- | --- | --- | --- |
| TP-01.01 | 既有 runtime 证据和缺口复核 | Done | 0074/0075/0076 docs 与 runtime backend contract |
| TP-01.02 | report_jobs.py 改动点复核 | Done | `rg` + `sed` 读取 manager/store 关键路径 |
| TP-02.01 | Store renew 默认接口 | Done | py_compile + focused tests |
| TP-02.02 | Postgres renew SQL | Done | smoke/static tests |
| TP-03.01 | DB polling | Done | smoke 验证外部 seeded queued job 被执行 |
| TP-03.02 | Heartbeat thread | Done | smoke 验证长任务期间错误 worker 不能抢占 |
| TP-03.03 | Lease expiry backoff | Done | static/focused tests 验证非 Postgres backend 不轮询且 Postgres claim 失败不会 busy loop |
| TP-04.01 | Postgres smoke | Done | allow-missing + optional live smoke |
| TP-04.02 | local-ci 接入 | Done | local-ci artifact |
| TP-04.03 | contract/docs 接线 | Done | runtime backend gate + docs tests |
| TP-05.01 | regression tests | Done | pytest focused |
| TP-05.02 | validation gates | Done | focused gates + quick CI |
| TP-05.03 | closeout/git/CI | Done | commit/push + remote CI evidence |

## Reading Order

1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
