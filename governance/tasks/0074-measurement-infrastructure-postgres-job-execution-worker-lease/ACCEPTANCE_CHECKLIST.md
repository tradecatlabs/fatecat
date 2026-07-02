# Acceptance Checklist

# Global Standards

- [x] 任务边界明确：只证明 Postgres job execution worker lease primitive。
- [x] 外部生产未验证项明确保留：exactly-once、公网 webhook live、外部 Vault/KMS、production ready。
- [x] 隐私边界明确：summary 不输出 DSN、用户名、密码、callback URL、secret、报告正文或用户输入。
- [x] 默认 memory/sqlite 行为保持兼容。
- [x] Contract、docs、AGENTS、local-ci 和 tests 同口径。

# Task Package Checklists

## TP-01 PRECHECK：边界、数据流和并发语义审查

Verify: current repo facts、runtime backend contract、0072 closeout 和 roadmap 已确认。

Gate: 明确 job execution lease 与 outbox lease、exactly-once、生产 ready 的边界。

- [x] 确认当前无 job execution claim/release 接口。
- [x] 确认 0072 只覆盖 outbox lease。
- [x] 记录 high-risk engineering fields。

## TP-02 IMPLEMENT：Postgres job execution lease 接口与实现

Verify: `report_jobs.py` 新接口和 Postgres 实现通过语法与 focused tests。

Gate: duplicate claim、wrong owner release、expiry reclaim、terminal unclaimable 均可被脚本验证。

- [x] `ReportJobStore` 新增 job claim/release 默认接口。
- [x] `PostgresReportJobStore` 原子 claim queued/running job。
- [x] wrong owner release 不清除 active lease。
- [x] terminal job 不可 claim。

## TP-03 IMPLEMENT：Job worker lease smoke 脚本与 wrapper

Verify: `scripts/postgres-job-worker-lease-smoke.py` 与 `.sh` 已新增并通过语法检查。

Gate: blocked preflight 和 real Postgres smoke 都能产生脱敏 JSON。

- [x] `--allow-missing` blocked preflight 实现。
- [x] duplicate claim negative check 实现。
- [x] wrong owner release negative check 实现。
- [x] lease expiry reclaim check 实现。
- [x] terminal job unclaimable check 实现。
- [x] `_safe_summary` 敏感值拦截实现。

## TP-04 VERIFY：契约、文档、AGENTS、local-ci 与回归测试接线

Verify: runtime backend contract/gate/local-ci/docs/AGENTS/tests 已接线。

Gate: `backend.postgres.status=planned`，`implementationStatus=job_worker_lease_smoke_baseline`。

- [x] RuntimeBackend contract/schema/gate 已同步。
- [x] local-ci quick 已加入 preflight artifact。
- [x] operations docs、roadmap、AGENTS 已同步。
- [x] focused regression 已新增。

## TP-05 CLOSEOUT：验证、审查、提交推送和远端 CI 证据

Verify: syntax、blocked preflight、real Postgres smoke、focused tests、local-ci、secret scan、task validators、remote CI。

Gate: 本地和远端证据齐全；仍不声明 production ready。

- [x] 语法检查通过。
- [x] blocked preflight 通过。
- [x] real Postgres smoke 通过。
- [x] focused tests 通过。
- [x] local-ci quick 通过。
- [x] task docs closeout validator 通过。
- [x] commit/push 和远端 CI evidence 完成。
