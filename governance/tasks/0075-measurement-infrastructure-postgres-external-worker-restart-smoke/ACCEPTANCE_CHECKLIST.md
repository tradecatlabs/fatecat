# Acceptance Checklist

# Global Standards

- [x] 任务边界明确：只证明 expired lease external backend worker restart smoke。
- [x] 外部生产未验证项明确保留：exactly-once、公网 webhook live、外部 Vault/KMS、production ready。
- [x] 隐私边界明确：summary 不输出 DSN、用户名、密码、callback URL、secret、报告正文或用户输入。
- [x] 默认 memory/sqlite 行为保持兼容。
- [x] Contract、docs、AGENTS、local-ci 和 tests 同口径。

# Task Package Checklists

## TP-01 PRECHECK：边界、数据流和执行语义审查

Verify: current repo facts、runtime backend contract、0074 closeout 和 roadmap 已确认。

Gate: 明确 crash/restart external backend worker 与 exactly-once、webhook live、Vault/KMS 的边界。

- [x] 确认 manager `_run_job()` 当前未 claim-before-execute。
- [x] 确认 0074 只覆盖 job lease primitive。
- [x] 修正 0074 INDEX 状态漂移。
- [x] 记录 high-risk engineering fields。

## TP-02 IMPLEMENT：ReportJobManager job execution lease 接线

Verify: `_run_job()` 执行前 claim，terminal 后 release，memory/sqlite 兼容。

Gate: claim 失败不执行 task；现有本地 recovery smoke 不回归。

- [x] Manager 拥有稳定 lease owner。
- [x] `_run_job()` claim-before-execute。
- [x] claim 失败时 task 不执行。
- [x] terminal success/failure/cancel path release owner lease。

## TP-03 IMPLEMENT：Postgres external worker restart smoke

Verify: `scripts/postgres-external-worker-restart-smoke.py` 与 `.sh` 已新增并通过语法检查。

Gate: blocked preflight 和 real Postgres smoke 都能产生脱敏 JSON。

- [x] `--allow-missing` blocked preflight 实现。
- [x] stale running job + expired lease fixture 实现。
- [x] two-manager recovery execution check 实现。
- [x] duplicate execution blocked check 实现。
- [x] `_safe_summary` 敏感值拦截实现。

## TP-04 VERIFY：契约、文档、AGENTS、local-ci 与回归测试接线

Verify: runtime backend contract/gate/local-ci/docs/AGENTS/tests 已接线。

Gate: `backend.postgres.status=planned`，`implementationStatus=external_worker_restart_smoke_baseline`。

- [x] RuntimeBackend contract/schema/gate 已同步。
- [x] local-ci quick 已加入 preflight artifact。
- [x] operations docs、roadmap、AGENTS 已同步。
- [x] focused regression 已新增。

## TP-05 CLOSEOUT：验证、审查、提交推送和远端 CI 证据

Verify: syntax、blocked preflight、real Postgres smoke、focused tests、local-ci、task validators、remote CI。

Gate: 本地和远端证据齐全；仍不声明 production ready。

- [x] 语法检查通过。
- [x] blocked preflight 通过。
- [x] real Postgres smoke 通过。
- [x] focused tests 通过。
- [x] local-ci quick 通过。
- [x] task docs closeout validator 通过。
- [ ] commit/push 和远端 CI evidence 完成。
