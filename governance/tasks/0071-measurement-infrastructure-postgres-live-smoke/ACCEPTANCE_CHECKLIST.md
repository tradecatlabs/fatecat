# Acceptance Checklist

## Global Standards

- [x] 变更只服务 MI-100.02 Durable Runtime 的 Postgres live smoke 切片。
- [x] 所有新增脚本都有明确职责，不新增第二套任务系统。
- [x] evidence JSON 不输出 DSN、用户名、密码、callback URL、webhook secret、报告正文或用户输入。
- [x] 文档和 contract 不宣称 production ready、生产多副本 worker、exactly-once、公网 webhook live 或外部 Vault/KMS 完成。
- [x] 验证命令真实执行，失败不伪造成通过。

## Task Package Checklists

## TP-01.01 Boundary Review

Verify: `git status`、`rg`、existing 0070 docs、runtime backend contract。

Gate: 0071 只增加 live evidence path，不改变默认 backend 和 store 抽象。

- [x] 0070 adapter baseline 已复核，Postgres 仍是 planned external candidate。

## TP-02.01 Postgres Live Smoke Tool

Verify: py_compile、real disposable Docker Postgres smoke。

Gate: live smoke 必须通过现有 `PostgresReportJobStore` 执行 schema/job/event/outbox/config 路径。

- [x] `scripts/postgres-job-store-live-smoke.py` 与 `.sh` 已新增。
- [x] real Docker Postgres smoke 通过，summary `status=passed`、`checks=16`、`shipGate.status=blocked`。

## TP-02.02 Production Readiness Evidence Gate

Verify: production-readiness 正负命令。

Gate: `FATE_REPORT_JOB_STORE=postgres` 不得只靠 `FATE_REPORT_JOB_POSTGRES_LIVE_VERIFIED=1` 通过。

- [x] 缺 `FATE_REPORT_JOB_POSTGRES_LIVE_EVIDENCE` 时 fail-fast。
- [x] 使用 passed evidence JSON 时 static readiness 通过，但外部 API/Bot live 仍标记待执行。

## TP-02.03 Runtime Backend Contract Sync

Verify: `bash scripts/runtime-backend-gate.sh --output-json /tmp/fatecat-runtime-backend-0071.json`。

Gate: contract 允许 `live_smoke_baseline`，但 Postgres `status` 仍是 `planned`。

- [x] Runtime backend gate 通过，checks=92。
- [x] `runtime-backends.json`、schema、delivery registry 已同步。

## TP-03.01 Regression Tests

Verify: focused pytest。

Gate: missing DSN、privacy、script wiring、contract、production-readiness docs 均有覆盖。

- [x] `tests/regression/test_postgres_job_store_live_smoke.py` 已新增并通过。
- [x] focused regression `32 passed`。

## TP-03.02 Missing Environment Preflight

Verify: `bash scripts/postgres-job-store-live-smoke.sh --allow-missing --output-json /tmp/fatecat-postgres-job-store-live-smoke-0071-blocked.json`。

Gate: 无 DSN 时退出 0 且 status=blocked，不伪造 passed。

- [x] blocked artifact 已生成，reason 为 missing env。

## TP-03.03 Disposable Postgres Live Smoke

Verify: Docker Postgres + live smoke command。

Gate: passed artifact 不含 raw DSN、callback URL、webhook secret 或报告正文。

- [x] `/tmp/fatecat-postgres-job-store-live-smoke-0071.json` 已生成，16 checks passed。
- [x] marker check 未发现 raw DSN、callback host、webhook shared value 或报告正文。

## TP-04.01 Documentation Sync

Verify: `rg` 和 diff review。

Gate: AGENTS、operations docs、roadmap、task index 口径一致。

- [x] `scripts/AGENTS.md`、delivery AGENTS、contract AGENTS、operations docs、roadmap 已同步。
- [x] 旧的 0060 durable runtime 文档漂移已修正到 0071 live smoke baseline。

## TP-04.02 Closeout Validation

Verify: local-ci quick、secret scan、task validators、remote CI after push。

Gate: 本地 quick CI 和任务 validators 通过；远端 CI 在提交推送后刷新。

- [x] quick local-ci 通过，focused regression `193 passed in 82.83s`。
- [x] secret scan 通过，findingCount=0。
- [x] 任务文档进入 closeout 状态。
