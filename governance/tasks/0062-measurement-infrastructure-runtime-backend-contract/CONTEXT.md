# Repo Evidence

| Evidence | Current Fact |
| --- | --- |
| `git status --short --branch` | 0062 start: clean at `main...origin/main` after 0061 push; 0062 skeleton added by task script. |
| `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` | 0061 推荐 0062 从 runtime backend contract 开始。 |
| `docs/reference-materials/operations/测算基础设施 API 接入.md` | Report job store 已说明 memory/sqlite；external backend 仍缺。 |
| `contracts/fate/delivery/registry.json` | 已登记 DeliverySurface 与 ReleaseGate；0062 前没有 RuntimeBackend。 |
| `contracts/fate/capabilities/schemas/resource.schema.json` | 已有 CalculationJob resource；0062 前没有 RuntimeBackend resource。 |

# Constraints Matrix

| Constraint | Impact |
| --- | --- |
| 只做 contract baseline | 不实现 Postgres/Temporal adapter。 |
| 不伪造 external backend | Postgres 必须保持 `status=planned` / `implementationStatus=contract_baseline`。 |
| 不保存 secret | registry 只保存 env var 名，不保存 DSN、token、password。 |
| 单切片可验收 | 只新增 gate、schema、registry、测试和文档。 |
| quick CI 可执行 | gate 必须不依赖真实数据库或公网。 |

# Change Boundary

允许修改：

- `contracts/fate/delivery/*`
- `contracts/fate/capabilities/schemas/resource.schema.json`
- `scripts/runtime-backend-gate.*`
- `scripts/local-ci.sh`
- `scripts/AGENTS.md`
- `tests/regression/test_runtime_backend_gate.py`
- `tests/regression/test_capability_protocol.py`
- `docs/reference-materials/operations/测算基础设施 API 接入.md`
- `docs/reference-materials/roadmap/测算基础设施100%实现计划.md`
- `governance/tasks/0062-*` 与 `governance/tasks/INDEX.md`

禁止修改：

- ReportJobStore 行为实现。
- Web/Bot/API runtime 行为。
- 真实环境变量、`.env`、secret、token 或 DSN。

# Risk Matrix

| Risk | Mitigation |
| --- | --- |
| contract gate 被误读成 production backend | schema、registry、docs、gate limits 全部写明不实现 adapter。 |
| Redis queue 被误用为 source of truth | gate 强制 `backend.redis_queue` 为 `not_selected` + `auxiliary_only`。 |
| SQLite single replica 被误称 distributed | gate 强制 `single_replica_only` 且 `multiReplicaReady=false`。 |
| registry 泄露 DSN/secret | gate 扫描常见 DSN/private key/secret assignment pattern。 |
| local-ci 漏掉新 gate | quick CI 新增 runtime backend gate artifact。 |

# Assumptions and Falsification

- Assumption: Postgres 是第一阶段 external backend 的最小成熟路径，Temporal 暂做 future workflow orchestrator。
- Falsifier: 如果后续 production platform 已强制提供 Temporal/queue as source of truth，则需要 ADR 改选型。
- Assumption: 本轮只需 contract gate，不需要外部 DB smoke。
- Falsifier: 如果代码允许 `FATE_REPORT_JOB_STORE=postgres` 静默 fallback 或伪成功，后续实现任务必须先修 fail-fast。

# Critical Ambiguities

- Postgres adapter 的具体 driver、migration tool、pooling 和 lock strategy 仍待后续实现任务。
- 外部数据库 smoke 需要真实数据库或一次性测试容器策略；本任务不决定。
- Temporal 是否引入取决于后续流程复杂度，不作为当前 ReportJobStore adapter。

# Debug Evidence Contract

- 调试模式: Optional
- 若 gate 或 local-ci failure 暴露 contract 矛盾，记录到 `STATUS.md`，必要时升级为 DEBUG.md。

# Task Package Context Map

| Node | Context |
| --- | --- |
| TP-01.01 | 0061 RESEARCH、roadmap 0.8、delivery registry、job store docs、data-supply-chain gate style。 |
| TP-02.01 | RuntimeBackend schema/registry/resource schema。 |
| TP-02.02 | delivery registry/AGENTS。 |
| TP-03.01 | `scripts/runtime-backend-gate.py` / `.sh`。 |
| TP-03.02 | `tests/regression/test_runtime_backend_gate.py`、`test_capability_protocol.py`。 |
| TP-03.03 | `scripts/local-ci.sh` artifact and focused regression list。 |
| TP-04.01 | API doc、roadmap、scripts AGENTS、INDEX。 |
| TP-04.02 | validators、py_compile、pytest、ruff、secret scan、quick local CI。 |
