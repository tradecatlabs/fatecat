# Task-Level Acceptance

- Postgres report job execution lease 支持 owner/status 受限 renew。
- ReportJobManager 执行长任务时能按 heartbeat interval 续约 lease。
- ReportJobManager 启动后即使没有 `submit()`，也能通过 polling 执行持久 store 中带 task payload 的 queued/recoverable running job。
- Claim 失败不会 busy loop。
- 新 smoke 支持真实 DSN live path，也支持 `--allow-missing` blocked preflight。
- Contract/docs/tests/local-ci 接线后仍明确 non-claims：不证明 exactly-once、长期多副本生产 ready、公网 webhook live passed、外部 Vault/KMS。

# Validation Plan

| Validation | Command / Evidence | Expected |
| --- | --- | --- |
| Python syntax | `.venv/bin/python -m py_compile domains/experience-delivery/services/fatecat-delivery/src/report_jobs.py scripts/postgres-worker-heartbeat-polling-smoke.py` | exit 0 |
| Shell syntax | `bash -n scripts/postgres-worker-heartbeat-polling-smoke.sh scripts/local-ci.sh` | exit 0 |
| Blocked preflight | `bash scripts/postgres-worker-heartbeat-polling-smoke.sh --allow-missing --output-json /tmp/fatecat-worker-heartbeat-polling.json` | status blocked, no secret |
| Runtime backend gate | `bash scripts/runtime-backend-gate.sh` | exit 0 |
| Focused pytest | targeted regression tests for smoke/runtime contract | exit 0 |
| Formatting/lint | `ruff check` and `ruff format --check` focused or quick CI | exit 0 |
| Task docs | `validate_task_docs.py --phase closeout` and `validate_tasks_tree.py --phase auto` | exit 0 |

# Validation Evidence

| Validation | Result |
| --- | --- |
| Python syntax | passed: `.venv/bin/python -m py_compile domains/experience-delivery/services/fatecat-delivery/src/report_jobs.py scripts/postgres-worker-heartbeat-polling-smoke.py` |
| Shell syntax | passed: `bash -n scripts/postgres-worker-heartbeat-polling-smoke.sh scripts/local-ci.sh` |
| Blocked preflight | passed: `bash scripts/postgres-worker-heartbeat-polling-smoke.sh --allow-missing --output-json /tmp/fatecat-worker-heartbeat-polling.json` produced blocked summary without DSN |
| Runtime backend gate | passed: `bash scripts/runtime-backend-gate.sh --output-json /tmp/fatecat-runtime-backend-gate.json` |
| Focused pytest | passed: 48 runtime/Postgres tests and 86 report-job related tests |
| Formatting/lint | passed: focused `ruff check` and `ruff format --check` |
| Quick CI | passed: `bash scripts/local-ci.sh --profile quick`, evidence `/tmp/fatecat-local-ci-20260703101004` |

# Review Gate

- document-drift: runtime backend contract、operations docs、AGENTS、task docs 与实现一致。
- future-optimal-drift: 不把现有 Thread/Queue patch 写成终态 orchestrator。
- ponytail-complexity: 不引入新 runtime dependency。
- evidence-integrity: allow-missing/blocked/live path 区分清楚。

# Runtime Verification Gate

- 无 DSN：blocked summary 是通过项，但只能证明工具可用和隐私边界。
- 有 DSN：smoke 必须证明 heartbeat renew、DB polling、stuck running recovery、duplicate claim blocked、lease cleared after terminal。
- 没有真实 DSN 时必须写 `外部连通验证待执行`，不得伪造 live passed。

# Ship Readiness

- 所有 TODO leaf 完成。
- 代码、脚本、测试、docs、contract 和 task docs 均通过验证。
- Git diff 不含 secret、DSN、报告正文或真实非北京地区示例。
- commit/push 后记录远端 CI 或明确 CI 待执行。

# Task Package Acceptance

| Node ID | Acceptance |
| --- | --- |
| TP-01.01 | 0074/0075/0076 缺口已记录，不重复实现旧 smoke。 |
| TP-01.02 | `report_jobs.py` 改动点已确认。 |
| TP-02.01 | Base store renew no-op 不破坏 memory/sqlite。 |
| TP-02.02 | Postgres renew SQL 只允许当前 owner 续租 running job。 |
| TP-03.01 | 外部 queued/running replayable jobs 可被 polling 入队。 |
| TP-03.02 | 长任务执行期间 heartbeat 能防止过期 lease 被抢占。 |
| TP-03.03 | claim 失败后不会 tight loop。 |
| TP-04.01 | 新 smoke 包含 live path、blocked path、脱敏 summary 和 nonClaims。 |
| TP-04.02 | local-ci 生成 allow-missing artifact。 |
| TP-04.03 | contract/docs/AGENTS 与新 baseline 一致。 |
| TP-05.01 | regression tests 覆盖 smoke and wiring。 |
| TP-05.02 | focused gates and quick CI pass。 |
| TP-05.03 | closeout、commit、push、CI evidence 完成。 |

# Anti-Goals

- 不声明 production ready。
- 不声明 exactly-once。
- 不声明 public webhook live passed。
- 不声明 external Vault/KMS。
- 不输出真实 DSN、token、secret、callback URL、报告正文或用户隐私样例。
