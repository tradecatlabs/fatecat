# Execution Checklist

[x] TP-01.01 | P0 | 复核 0074/0075/0076 既有 runtime 证据和缺口 | Verify: 任务文档和 contract 已读取 | Gate: 不重复旧 smoke、不夸大旧证据 | Parallelizable: No
[x] TP-01.02 | P0 | 复核 report_jobs.py manager/store 改动点 | Verify: `rg`/`sed` 已定位关键函数 | Gate: 改动面限定到 manager/store | Parallelizable: No
[x] TP-02.01 | P0 | 为 ReportJobStore 增加 renew_job_execution_lease 默认接口 | Verify: py_compile/focused tests | Gate: memory/sqlite 默认行为不破坏 | Parallelizable: No
[x] TP-02.02 | P0 | 为 PostgresReportJobStore 增加 owner/status 受限 renew SQL | Verify: smoke/static tests | Gate: wrong owner 不能续租 | Parallelizable: No
[x] TP-03.01 | P0 | 增加 DB polling，把外部 queued/running replayable jobs 入内存队列 | Verify: smoke seeded queued job | Gate: 不重复入队、不执行无 payload job | Parallelizable: No
[x] TP-03.02 | P0 | 增加执行中 heartbeat thread 和 renewal failure event | Verify: smoke long task duplicate claim blocked | Gate: heartbeat stop 无泄漏 | Parallelizable: No
[x] TP-03.03 | P0 | 增加 lease expiry backoff，claim 失败后不忙等 | Verify: smoke/static tests | Gate: queue worker 不 tight loop | Parallelizable: No
[x] TP-04.01 | P0 | 新增 postgres-worker-heartbeat-polling-smoke.py/.sh | Verify: py_compile/bash -n/allow-missing | Gate: summary 脱敏且 nonClaims 完整 | Parallelizable: No
[x] TP-04.02 | P0 | 接入 local-ci preflight artifact | Verify: local-ci artifact contains smoke | Gate: 缺 DSN 时 blocked 不失败 quick CI | Parallelizable: No
[x] TP-04.03 | P0 | 更新 runtime backend contract/schema/gate/docs/AGENTS | Verify: runtime-backend-gate + docs tests | Gate: contract 不宣称 production ready | Parallelizable: No
[x] TP-05.01 | P0 | 增加 regression tests | Verify: pytest focused | Gate: 覆盖 allow-missing 和 wiring | Parallelizable: No
[x] TP-05.02 | P0 | 运行 focused gates、ruff/format 和 quick CI | Verify: commands pass | Gate: 失败必须修复或记录 blocker | Parallelizable: No
[x] TP-05.03 | P0 | 回填任务 closeout、提交、推送并记录 CI | Verify: git status/commit/push/CI | Gate: worktree clean and evidence recorded | Parallelizable: No

说明：
- 每一行后续必须绑定 `TP-XX(.YY...)`
- 不允许出现无归属 TODO
