# Acceptance Checklist

## Global Standards

- [x] 变更只服务 MI-100.01 Durable Runtime 的 Postgres adapter 切片。
- [x] 所有新增文件都有明确职责，不增加无用抽象。
- [x] 不输出真实 DSN、token、secret、password、私钥、证书或用户报告正文。
- [x] 文档不宣称 external backend live verified、production ready、exactly-once 或真实多副本 worker 完成。
- [x] 验证命令真实执行，失败不伪造成通过。

## Task Package Checklists

## TP-01.01 Existing Store and Contract Review

Verify: `sed` / `rg` / `json.tool` 复核 `ReportJobStore`、SQLite store、runtime backend contract 和配置门禁。

Gate: Postgres adapter 必须贴合现有 store 接口，不新增第二套任务系统。

- [x] 现有接口、SQLite 行为和 0062 contract baseline 已复核。

## TP-02.01 Postgres SQL Helper

Verify: `bash scripts/postgres-job-store-dry-run.sh --output-json /tmp/fatecat-postgres-job-store-dry-run-0070.json`。

Gate: required tables、indexes、upsert、claim/release SQL 全部存在。

- [x] Postgres DDL/helper 覆盖 required tables、indexes、upsert、claim/release。

## TP-02.02 Postgres Report Job Store

Verify: `.venv/bin/python -m py_compile domains/experience-delivery/services/fatecat-delivery/src/report_jobs.py` 和 focused regression。

Gate: `PostgresReportJobStore` 实现 `ReportJobStore` 方法，`psycopg` 保持 optional dependency。

- [x] `PostgresReportJobStore` 已实现 job/event/outbox/config persistence 方法。

## TP-02.03 Runtime Configuration

Verify: focused regression 和 `production-readiness.sh` negative checks。

Gate: `FATE_REPORT_JOB_STORE=postgres` 缺 DSN 或缺 live verification 必须 fail-fast，不允许 silent fallback。

- [x] `main.py` 与 `production-readiness.sh` 已接入 postgres store 配置和 fail-fast。

## TP-03.01 Postgres Dry Run Smoke

Verify: `bash scripts/postgres-job-store-dry-run.sh --output-json /tmp/fatecat-postgres-job-store-dry-run-0070.json`。

Gate: JSON 输出 `status=passed` 且 `shipGate.status=blocked`，不含真实 DSN/secret。

- [x] Dry-run smoke 已生成机器可读 JSON 并保留 external live blocked。

## TP-03.02 Regression Tests

Verify: `.venv/bin/python -m pytest -q tests/regression/test_runtime_backend_gate.py tests/regression/test_postgres_job_store_adapter.py tests/regression/test_capability_protocol.py`。

Gate: SQL、optional dependency、隐私、配置 fail-fast 和 contract 状态均有测试覆盖。

- [x] Regression tests 已新增并通过。

## TP-03.03 Local CI and Contract Gate

Verify: `bash scripts/runtime-backend-gate.sh --output-json /tmp/fatecat-runtime-backend-0070.json` 和 `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0070`。

Gate: runtime backend gate 识别 adapter baseline，local-ci summary 暴露 `artifacts.postgresJobStoreDryRun`。

- [x] local-ci 与 runtime backend contract/gate 已接入。

## TP-04.01 Documentation Sync

Verify: `git diff -- docs contracts scripts domains governance/tasks`。

Gate: AGENTS、roadmap、operations docs 和任务索引不得宣称 external live、production ready、exactly-once 或多副本 worker 完成。

- [x] AGENTS、roadmap、operations docs、任务索引和任务文档已同步。

## TP-04.02 Closeout Validation

Verify: `validate_task_docs.py --phase closeout`、`validate_tasks_tree.py --phase auto`、focused validation 和 quick local-ci。

Gate: 本地 quick CI 和任务 validators 通过；Git 交付和远端 CI 在提交推送后作为外部交付证据刷新，不写成本提交内的既成事实。

- [x] 本地 focused validation、secret scan、quick local-ci 和任务文档 closeout 已完成。
