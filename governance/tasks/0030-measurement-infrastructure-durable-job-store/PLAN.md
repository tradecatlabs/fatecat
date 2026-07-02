# Planning Summary
本轮把 report job 运行面从“只在当前进程内可见”推进为“默认内存、可选 SQLite、本地可验证持久状态”的 baseline。目标是先建立 job store 边界和可验证持久语义，不把任务扩大成分布式 workflow 平台。

# Lifecycle Gates
- SPEC：确认只做 single-instance durable state baseline。
- PLAN：任务树、风险、out-of-scope、验证命令落盘。
- BUILD：实现 store 抽象、SQLite backend、main 配置、metadata、metrics、production-readiness。
- TEST：focused tests、observability/security smoke、JSON、shell syntax、ruff、format、secret scan、quick CI、diff check。
- REVIEW：检查默认 memory 不回归，SQLite 不夸大为分布式任务系统，文档/registry 同步。
- SHIP：task validators、全任务树验证和 closeout packet 通过。
- 不得跳过 gate。

# Simplest Path
复用现有 `ReportJobManager` 状态机和 worker thread，只把状态读写抽到 store；SQLite 用标准库 `sqlite3`。不引入新依赖，不重写 API，不改 Web UI。

# Split Strategy
先实现 runtime store，再补可观测/配置/预检，最后补测试和文档。

# Execution Waves
| Wave | Nodes | Purpose |
| --- | --- | --- |
| Wave 1 | TP-01 | 现状和任务契约 |
| Wave 2 | TP-02 | runtime store 与服务配置 |
| Wave 3 | TP-03 | tests/docs/registry |
| Wave 4 | TP-04 | 验证与 closeout |

# Runtime Workflow Contract
- 默认：`FATE_REPORT_JOB_STORE=memory`，现有内存队列行为不变。
- SQLite：`FATE_REPORT_JOB_STORE=sqlite`，`FATE_REPORT_JOB_DB_PATH` 指向本地 SQLite 文件。
- manager 提交任务后持久化 queued/running/succeeded/failed/cancelled/expired 状态。
- manager 重建时加载 SQLite 中任务；旧 queued/running 被标记为 failed，错误为“任务执行器已重启，未完成任务已终止”。
- `Idempotency-Key` 在 SQLite backend 中跨 manager 保留。

# Next Executable Leaves
- TP-04.01：执行完整本地门禁。
- TP-04.02：回填 closeout 和 closeout packet。

# Dependency Graph
```text
TP-01.01 -> TP-01.02 -> TP-02.01 -> TP-02.02 -> TP-02.03 -> TP-03.01 -> TP-03.02 -> TP-04.01 -> TP-04.02
```

# Future-Optimal Contract
Target end state: 长报告和多 provider 流程最终由可靠任务控制面管理，具备 durable state、idempotency、retry、webhook、observability、external backend 和 release gate。

Real constraints: 当前只有单进程 worker 和 FastAPI API；不能引入外部服务依赖；必须保持默认公开服务行为兼容。

Inertia constraints: 旧内存队列实现不能决定最终 job store 模型；“SQLite 能持久化”也不能被误写成分布式任务系统。

Kill list: “只有内存任务也能生产可靠”“SQLite 等同多副本任务系统”“running callable 可跨进程继续执行”。

Proof point: SQLite backend 回归证明 finished/cancelled/idempotency 可跨 manager 查询，active job 重建后会失败而不是伪继续执行。

Falsifier: 默认 memory 行为回归、SQLite 重建无法查询 succeeded/cancelled job、或多副本 production-readiness 允许本地 job store。

Migration slice: 本轮完成 memory/sqlite store baseline；后续接 webhook、retry、external backend 和 restart recovery drill。

Rejected short-term patches: 不只改文档；不把 `_jobs` pickle 到文件；不引入未配置的 Redis/Celery；不伪造 crash 后继续执行。

# Ponytail Contract
Existence check: durable job store 是 MI-03 的直接缺口，report job 已是公开 API surface，必须有可验证状态持久化 baseline。

Selected ladder rung: 项目内直接实现薄 store 抽象，复用标准库 SQLite，不新增第三方依赖。

Skipped scope: webhook、retry、external backend、distributed lock、job event history、物理清理过期行。

Ceiling / upgrade path: 多副本、跨进程执行、长链路 retry 或外部调用出现时，升级到 external backend。

Do-not-simplify: 默认兼容、幂等键、取消语义、TTL、失败恢复语义、隐私边界必须保留。

Minimal runnable check: SQLite store tests、API contract tests、production-readiness syntax、quick CI。

Complexity review owner: auto-review/reliability/document-drift/ponytail-complexity。

# Documentation Impact
Operating model update: not needed；项目定位不变。

Toolchain model update: not needed；未新增命令入口。

Process update: updated；production-readiness 增加 report job store 配置门禁。

Source-of-truth updates: updated；API 文档、roadmap、observability/security registry、env examples 和 AGENTS 已同步。

Local README/AGENTS impact: updated；`fatecat-delivery/AGENTS.md` 已更新 `report_jobs.py` 边界。

Contract/catalog/schema impact: updated；observability/security registry 增加 job store 字段和 envVars。

ADR/Gate/module-context impact: not needed；本任务是 MI-03 局部 runtime baseline，不改变顶层架构。

Documentation exemption reason: 不新增 ADR；external backend 选型时再记录架构决策。

Validation evidence: 见 `STATUS.md`。

# Rollback Protocol
- 恢复 `report_jobs.py` 到纯内存实现。
- 恢复 `main.py` 中 `FATE_REPORT_JOB_STORE`、`FATE_REPORT_JOB_DB_PATH`、metadata/metrics 改动。
- 恢复 production-readiness、env examples、observability/security registry、API 文档、roadmap、AGENTS、tests 和 0030 任务文档。
- 不影响 capability/provider/report/evaluation/security 既有资源切片。
