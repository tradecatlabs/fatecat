# Execution Checklist

[x] TP-01.01 | P0 | 复核 ReportJobStore 接口、SQLite 行为和 runtime backend contract | Verify: sed/rg/json tool | Gate: Postgres adapter 贴合现有接口 | Parallelizable: No
[x] TP-02.01 | P0 | 新增 Postgres DDL 与 SQL helper | Verify: dry-run SQL checks | Gate: required tables/indexes/upsert/claim/release 存在 | Parallelizable: No
[x] TP-02.02 | P0 | 新增 PostgresReportJobStore 可选适配层 | Verify: py_compile + unit tests | Gate: implements store methods | Parallelizable: No
[x] TP-02.03 | P0 | 接入 main.py 配置和 production-readiness fail-fast | Verify: focused tests | Gate: no silent fallback | Parallelizable: No
[x] TP-03.01 | P0 | 新增 Postgres store dry-run smoke | Verify: smoke JSON | Gate: status passed + shipGate blocked | Parallelizable: Yes
[x] TP-03.02 | P0 | 新增 regression tests | Verify: pytest | Gate: SQL/privacy/config covered | Parallelizable: Yes
[x] TP-03.03 | P0 | 接入 local-ci 与 runtime backend contract | Verify: local-ci grep + gate | Gate: postgresJobStoreDryRun artifact 可发现 | Parallelizable: Yes
[x] TP-04.01 | P0 | 同步 AGENTS、roadmap 和任务索引 | Verify: docs diff | Gate: 不夸大 external live | Parallelizable: Yes
[x] TP-04.02 | P0 | 运行 focused validation、quick local-ci、任务校验并收口证据 | Verify: commands | Gate: 本地 quick CI 和 validators 通过 | Parallelizable: No

说明：
- 每一行后续必须绑定 `TP-XX(.YY...)`
- 不允许出现无归属 TODO
