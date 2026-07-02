# Task-Level Acceptance

- RuntimeBackend schema 存在，并声明 required fields、allowed backend/status/production eligibility/invariants。
- RuntimeBackend registry 登记 memory、sqlite、postgres、temporal、redis_queue。
- Delivery registry 和 resource schema 链接 RuntimeBackend。
- Gate CLI 可输出 `kind=fatecat.runtime_backend_gate` 的 JSON，且 status 为 passed。
- Gate 强制 Postgres 为 planned candidate，不声明 implemented/production_ready。
- Gate 强制 SQLite 为 single_replica_only，不声明 multiReplicaReady。
- Gate 强制 Redis queue 为 not_selected + auxiliary_only，不作为 source_of_truth。
- Gate summary、registry、docs 不包含真实 DSN、token、secret、password、private key。
- quick local CI 包含 runtime backend gate artifact。
- 文档明确本轮不实现真实 external backend。

# Validation Plan

| 验证项 | 命令 | 期望 |
| --- | --- | --- |
| syntax | `python3 -m py_compile scripts/runtime-backend-gate.py` | pass |
| gate CLI | `bash scripts/runtime-backend-gate.sh --output-json /tmp/fatecat-runtime-backend-gate.json` | pass |
| focused tests | `.venv/bin/python -m pytest -q tests/regression/test_runtime_backend_gate.py tests/regression/test_capability_protocol.py -k "runtime_backend or delivery_surface_schema"` | pass |
| ruff | `.venv/bin/python -m ruff check ... && .venv/bin/python -m ruff format --check ...` | pass |
| secret scan | `bash scripts/secret-scan.sh --output-json /tmp/fatecat-secret-scan-0062.json` | pass |
| task docs | `validate_task_docs.py --phase closeout` | pass |
| task tree | `validate_tasks_tree.py --phase auto` | pass |
| quick local CI | `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0062` | pass |

# Review Gate

| 维度 | Gate |
| --- | --- |
| 正确性 | Registry 与 gate 对 Postgres/SQLite/Redis/Temporal 的状态一致。 |
| 安全 | 不保存 DSN、secret、token、password 或 production log。 |
| 架构 | RuntimeBackend 是 delivery/runtime 资源，不污染命理核心。 |
| 可维护 | Gate 使用无外部依赖 Python，local-ci 可重复执行。 |
| 不夸大 | 文档和 gate limits 明确 contract baseline 不等于 external backend 已生产。 |

# Runtime Verification Gate

- 本地可验证：schema/registry/gate/test/local-ci。
- 外部连通验证待执行：Postgres adapter、真实 external DB、Temporal service、Redis service、生产分布式 worker lease、真实 crash/restart、多副本、exactly-once。

# Ship Readiness

- TODO 全部勾选。
- STATUS 全节点 Done。
- 验证命令写入 Recent Evidence。
- 工作树提交推送后应 clean。

# Task Package Acceptance

- 0062 任务文档无占位符。
- `INDEX.md` 0062 状态同步。
- `ACCEPTANCE_CHECKLIST.md` 覆盖所有叶子节点。

# Anti-Goals

- 不实现真实 Postgres/Temporal/Redis adapter。
- 不连接真实数据库或服务。
- 不声明 external backend、生产级分布式 worker lease、exactly-once 或公网 webhook live delivery 已完成。
