# Acceptance Checklist

# Global Standards

- [x] 任务边界明确：0078 只做 worker heartbeat/polling hardening。
- [x] 旧证据边界明确：0074/0075/0076 不被夸大。
- [x] Store renew、manager polling、heartbeat、backoff 均已实现。
- [x] Smoke、tests、contract、docs、local-ci 均已接线。
- [x] 外部待验证项未被伪造成完成。
- [x] 任务文档 closeout validator 通过。

# Task Package Checklists

## TP-01 现状复核与任务定界

Verify: 0074/0075/0076 docs、runtime backend contract、`report_jobs.py` 已读取。

Gate: 不重复旧 smoke，不把旧证据写成 production ready。

- [x] TP-01.01 已复核既有 runtime 证据和缺口。
- [x] TP-01.02 已定位 manager/store 改动点。

## TP-01.01 复核 0074/0075/0076 既有 runtime 证据和缺口

Verify: task docs and contract inspected.

Gate: 0078 scope does not include public webhook live passed, Vault/KMS, exactly-once.

- [x] 已确认 0075 不证明 heartbeat/polling。
- [x] 已确认 0076 不证明 live passed。

## TP-01.02 复核 report_jobs.py manager/store 改动点

Verify: `rg` and `sed` located store/manager functions.

Gate: implementation can be limited to `report_jobs.py`.

- [x] Store claim/release paths located.
- [x] Manager worker loop and recovery paths located.

## TP-02 Store heartbeat primitive

Verify: py_compile and focused tests.

Gate: renew interface exists and Postgres renew respects lease owner.

- [x] TP-02.01 Base store renew no-op complete.
- [x] TP-02.02 Postgres renew SQL complete.

## TP-02.01 为 ReportJobStore 增加 renew_job_execution_lease 默认接口

Verify: py_compile.

Gate: memory/sqlite behavior unchanged.

- [x] Default method returns safe no-op result.

## TP-02.02 为 PostgresReportJobStore 增加 owner/status 受限 renew SQL

Verify: smoke/static tests.

Gate: wrong owner cannot renew or steal lease.

- [x] SQL limits by `job_id`, `lease_owner`, `status='running'`.

## TP-03 Manager polling/heartbeat

Verify: smoke demonstrates polling and heartbeat.

Gate: external queued/recoverable jobs execute without submit; long task lease renewed.

- [x] TP-03.01 DB polling complete.
- [x] TP-03.02 heartbeat thread complete.
- [x] TP-03.03 claim backoff complete.

## TP-03.01 增加 DB polling，把外部 queued/running replayable jobs 入内存队列

Verify: smoke seeded queued job is executed by already started manager.

Gate: only jobs with task payload and registered factory are admitted.

- [x] Polling implementation complete.

## TP-03.02 增加执行中 heartbeat thread 和 renewal failure event

Verify: long task duplicate claim blocked after original TTL.

Gate: heartbeat is stopped in finally.

- [x] Heartbeat implementation complete.

## TP-03.03 增加 lease expiry backoff，claim 失败后不忙等

Verify: static/focused tests.

Gate: worker does not tight-loop when claim fails.

- [x] Backoff implementation complete.

## TP-04 Smoke、contract 和 docs

Verify: smoke, local-ci, runtime backend gate.

Gate: no overclaim.

- [x] TP-04.01 smoke added.
- [x] TP-04.02 local-ci connected.
- [x] TP-04.03 contract/docs updated.

## TP-04.01 新增 postgres-worker-heartbeat-polling-smoke.py/.sh

Verify: py_compile, bash -n, allow-missing.

Gate: summary redacted and nonClaims complete.

- [x] Smoke script complete.

## TP-04.02 接入 local-ci preflight artifact

Verify: quick CI artifact contains worker heartbeat polling blocked summary.

Gate: no DSN needed for default local-ci.

- [x] local-ci wiring complete.

## TP-04.03 更新 runtime backend contract/schema/gate/docs/AGENTS

Verify: runtime-backend-gate and docs tests.

Gate: contract status advances only to heartbeat/polling smoke baseline.

- [x] contract/docs wiring complete.

## TP-05 Tests and closeout

Verify: focused tests, quick CI, task validators, git/CI evidence.

Gate: no failing required checks.

- [x] TP-05.01 regression tests complete.
- [x] TP-05.02 validation gates complete.
- [x] TP-05.03 closeout and Git delivery complete.

## TP-05.01 增加 regression tests

Verify: pytest focused.

Gate: tests cover allow-missing and wiring.

- [x] Regression tests added.

## TP-05.02 运行 focused gates、ruff/format 和 quick CI

Verify: command output.

Gate: failures fixed or explicitly blocked.

- [x] Validation commands completed.

## TP-05.03 回填任务 closeout、提交、推送并记录 CI

Verify: git status/commit/push/CI evidence.

Gate: worktree clean and remote evidence recorded.

- [x] Task docs closed.
- [x] Commit pushed.
