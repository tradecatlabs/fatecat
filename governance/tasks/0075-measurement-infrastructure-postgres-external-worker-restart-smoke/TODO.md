# Execution Checklist

[x] TP-01 | P0 | PRECHECK：边界、数据流和执行语义审查 | Verify: current repo facts、runtime backend contract、0074 closeout 和 roadmap 已确认 | Gate: 明确 crash/restart external backend worker 与 exactly-once、webhook live、Vault/KMS 的边界 | Parallelizable: No
[x] TP-02 | P0 | IMPLEMENT：ReportJobManager job execution lease 接线 | Verify: `_run_job()` 执行前 claim，terminal 后 release，memory/sqlite 兼容 | Gate: claim 失败不执行 task；现有本地 recovery smoke 不回归 | Parallelizable: No
[x] TP-03 | P0 | IMPLEMENT：Postgres external worker restart smoke | Verify: scripts/postgres-external-worker-restart-smoke.py 与 .sh 已新增并通过语法检查 | Gate: blocked preflight 和 real Postgres smoke 都能产生脱敏 JSON | Parallelizable: No
[x] TP-04 | P0 | VERIFY：契约、文档、AGENTS、local-ci 与回归测试接线 | Verify: runtime backend contract/gate/local-ci/docs/AGENTS/tests 已接线 | Gate: backend.postgres.status=planned 且 implementationStatus=external_worker_restart_smoke_baseline | Parallelizable: Yes
[x] TP-05 | P0 | CLOSEOUT：验证、审查、提交推送和远端 CI 证据 | Verify: syntax、blocked preflight、real Postgres smoke、focused tests、local-ci、task validators；remote CI pending commit/push | Gate: 本地证据齐全且仍不声明 production ready | Parallelizable: No
