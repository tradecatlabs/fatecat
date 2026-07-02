# Task-Level Acceptance

本任务完成必须满足：

- SQLite webhook outbox 支持 atomic claim/release lease。
- 同一条 failed/pending outbox 在 lease 未过期时不能被第二个 owner claim。
- release 后其他 owner 可以 claim。
- Manager redelivery 必须先 claim；claim 失败不得 dispatch。
- redelivery 完成后 release lease。
- API `webhookOutbox[]` payload 不新增 lease owner、lease acquired/expires 内部字段。
- Smoke summary 不包含 webhook URL、secret、报告正文、姓名、出生地区、token、DSN 或生产路径。
- 文档明确当前只是本地 SQLite lease baseline，不是 external backend、生产级分布式 worker lease、多副本锁、真实公网 live smoke 或 exactly-once。

# Validation Plan

| 验证项 | 命令 | 期望 |
| --- | --- | --- |
| smoke CLI | `bash scripts/webhook-outbox-lease-smoke.sh --output-json /tmp/webhook-outbox-lease-smoke.json` | pass |
| focused test | `.venv/bin/python -m pytest -q tests/regression/test_webhook_outbox_lease_smoke.py tests/regression/test_api_contracts.py::test_sqlite_webhook_outbox_claim_release_lease_prevents_double_claim tests/regression/test_api_contracts.py::test_sqlite_webhook_outbox_lease_payload_stays_internal` | pass |
| syntax | `python3 -m py_compile domains/experience-delivery/services/fatecat-delivery/src/report_jobs.py scripts/webhook-outbox-lease-smoke.py` | pass |
| ruff | `.venv/bin/ruff format --check ... && .venv/bin/ruff check ...` | pass |
| secret scan | `bash scripts/secret-scan.sh --output-json /tmp/fatecat-secret-scan-0060.json` | pass |
| task docs | `validate_task_docs.py --phase closeout` | pass |
| task tree | `validate_tasks_tree.py --phase auto` | pass |
| quick local CI | `bash scripts/local-ci.sh --profile quick` | pass before ship |

# Review Gate

| 维度 | Gate |
| --- | --- |
| 正确性 | atomic claim 防止第二 owner 同时领取；release 后可重新领取。 |
| 可读性 | lease 逻辑在 store/manager 内部，边界清楚。 |
| 架构 | 不把内部 lease 字段加入公开 API payload。 |
| 安全 | summary/events 不包含 URL、secret、报告正文或用户输入。 |
| 性能 | claim 是单条 outbox conditional update，不引入全表锁设计。 |

# Runtime Verification Gate

- 本地可验证：claim/release、claim conflict、manager redelivery once、payload internal field boundary、privacy boundary。
- 外部连通验证待执行：external backend、真实 webhook live smoke、生产多副本 worker lease、exactly-once。

# Ship Readiness

- 所有 TODO 勾选。
- `STATUS.md` 全节点 Done。
- 验证命令写入 Recent Evidence。
- worktree clean after commit/push。

# Task Package Acceptance

- 任务文档无占位符。
- `TODO.md` 只包含叶子节点。
- `INDEX.md` 新增 0060。
- 文档不夸大为 MI-NEXT-03 完成。

# Anti-Goals

- 不声明测算基础设施 100%。
- 不声明 external backend、生产级分布式 worker lease、多副本锁、exactly-once、真实公网 webhook live smoke、外部 Vault/KMS 或生产密钥生命周期完成。
