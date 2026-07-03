# Repo Evidence

| Evidence | Observation |
| --- | --- |
| `contracts/fate/delivery/runtime-backends.json` | `backend.postgres` 是 planned external candidate，仍阻断 production/multi-replica/exactly-once。 |
| `scripts/postgres-worker-heartbeat-polling-smoke.py` | 证明 worker heartbeat/polling baseline，不证明长期多副本生产运行。 |
| `contracts/fate/security/external-secret-provider-contract.json` | 0079 已建立 external secret provider evidence gate，但 live evidence 仍待外部执行。 |
| `scripts/local-ci.sh` | quick CI 已有 runtime/backend/security/artifact 编排，可接入新 gate。 |
| `tests/regression/test_runtime_backend_gate.py` | 可扩展为 registry 接线防回潮测试。 |

# Constraints Matrix

| Constraint | Decision |
| --- | --- |
| 无真实多副本环境 | 本任务只做 evidence contract/gate 和 external pending。 |
| 不能声明 exactly-once | Contract 明确禁止 `exactlyOnceClaim=true`。 |
| 不连接外部系统 | Gate 默认只读 tracked JSON；可选 live evidence 只验证脱敏结构。 |
| 不增加 runtime worker 复杂度 | 复用既有 gate/contract 模式，不新增调度器或外部依赖。 |
| 文档驱动 | runtime registry、delivery registry、operations docs、roadmap、AGENTS、task docs 同步。 |

# Change Boundary

- 允许新增 `contracts/fate/delivery/multi-replica-runtime-contract.json`。
- 允许新增 `scripts/multi-replica-runtime-gate.py` 和 `.sh`。
- 允许修改 runtime backend registry、delivery registry、runtime-backend-gate、local-ci、roadmap、operations docs、AGENTS、task docs 和 regression tests。
- 不修改 report job 执行语义、不修改 Postgres adapter、不启动真实外部服务、不修改命理算法。

# Risk Matrix

| Risk | Impact | Mitigation |
| --- | --- | --- |
| 单副本/短 smoke 被误写为多副本 live | 生产准入失真 | negative cases 拒绝单副本和短时间证据。 |
| SQLite local baseline 被误写为 external backend | 多副本结论错误 | gate 强制 backend 为 `backend.postgres`。 |
| no duplicate 被误写为 exactly-once | 可靠性承诺过高 | contract 明确禁止 exactlyOnceClaim。 |
| summary 泄露敏感值 | 安全事故 | gate 检查 sensitive fragments，只允许 evidence refs。 |
| contract 成为孤立文档 | 治理漂移 | 接入 runtime registry、local-ci 和 regression tests。 |

# Assumptions and Falsification

- Assumption: 当前没有真实多副本 runtime 环境、外部 metrics backend、公网 webhook passed evidence 或外部 secret provider live evidence。
- Assumption: 长期多副本初始生产证据至少需要 2 副本、24h、100 个完成任务和 no duplicate terminal job 证据。
- Falsifier: gate 接受 `replicaCount=1`、短运行、`backend.sqlite` 或 `exactlyOnceClaim=true`。
- Falsifier: `backend.postgres` 被改成 production ready。
- Falsifier: local-ci 没有执行 multi-replica gate。

# Critical Ambiguities

- 真实多副本运行环境、部署平台和监控平台尚未指定；本任务只定义证据引用字段。
- 真实 exactly-once 是否要追求尚未决策；本任务只允许证明“未观察到重复终态 job”。
- Public webhook 和 external secret provider live evidence 仍需要独立外部验证。

# Debug Evidence Contract

- 调试模式: Optional

若 gate、focused tests 或 CI 失败，记录最小失败命令、根因、修复和回归证据；不得把失败环境写成 live evidence 通过。

# Task Package Context Map

| Node ID | Context |
| --- | --- |
| TP-01.01 | roadmap、runtime backend registry、0078/0079 task facts。 |
| TP-01.02 | delivery registry、local-ci、runtime-backend-gate、tests。 |
| TP-02.01 | `multi-replica-runtime-contract.json`。 |
| TP-02.02 | negative evidence cases and live evidence schema。 |
| TP-03.01 | `runtime-backends.json`、`registry.json`。 |
| TP-03.02 | `multi-replica-runtime-gate.py/.sh`。 |
| TP-03.03 | `local-ci.sh` and summary artifact map。 |
| TP-04.01 | `tests/regression/test_multi_replica_runtime_gate.py` and related runtime tests。 |
| TP-04.02 | roadmap、operations docs、delivery/scripts/tests AGENTS。 |
| TP-05.01 | focused gates、ruff/format、secret scan、quick CI。 |
| TP-05.02 | task closeout、Git/GitHub delivery evidence。 |
