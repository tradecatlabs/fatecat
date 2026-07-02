# Execution Checklist

[x] TP-01 | P0 | PRECHECK：边界、数据流和并发语义审查 | Verify: current repo facts、runtime backend contract、0072 closeout 和 roadmap 已确认 | Gate: 明确 job execution lease 与 outbox lease、exactly-once、production ready 的边界 | Parallelizable: No
[x] TP-02 | P0 | IMPLEMENT：Postgres job execution lease 接口与实现 | Verify: report_jobs.py 新接口和 Postgres 实现通过语法与 focused tests | Gate: duplicate claim、wrong owner release、expiry reclaim、terminal unclaimable 均可被脚本验证 | Parallelizable: No
[x] TP-03 | P0 | IMPLEMENT：Job worker lease smoke 脚本与 wrapper | Verify: scripts/postgres-job-worker-lease-smoke.py 与 .sh 已新增并通过语法检查 | Gate: blocked preflight 和 real Postgres smoke 都能产生脱敏 JSON | Parallelizable: No
[x] TP-04 | P0 | VERIFY：契约、文档、AGENTS、local-ci 与回归测试接线 | Verify: runtime backend contract/gate/local-ci/docs/AGENTS/tests 已接线 | Gate: backend.postgres.status=planned 且 implementationStatus=job_worker_lease_smoke_baseline | Parallelizable: Yes
[x] TP-05 | P0 | CLOSEOUT：验证、审查、提交推送和远端 CI 证据 | Verify: syntax、blocked preflight、real Postgres smoke、focused tests、local-ci、secret scan、task validators、remote CI | Gate: 本地和远端证据齐全且仍不声明 production ready | Parallelizable: No
