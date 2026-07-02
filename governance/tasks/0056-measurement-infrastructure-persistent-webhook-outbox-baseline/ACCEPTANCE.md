# Task-Level Acceptance

本任务完成必须满足：

- SQLite backend 能持久保存 webhook outbox record。
- outbox record 能记录 pending、succeeded、failed、attempts、maxAttempts、signatureMode、targetHostHash 和安全边界。
- webhook dispatch 成功和失败都能更新 outbox record。
- manager rebuild 后仍能读取 outbox record。
- API 返回 `webhookOutbox` 脱敏摘要。
- summary/API/events 不包含 Markdown 正文、姓名、出生地区、webhook URL、webhook secret、token、DSN 或真实生产路径。
- quick local CI 执行 webhook outbox smoke。
- 文档明确当前是本地 persistent outbox baseline，不是公网 live callback、重启自动重投或 external backend。

# Validation Plan

| 验证项 | 命令 | 期望 |
| --- | --- | --- |
| smoke CLI | `bash scripts/webhook-outbox-smoke.sh --output-json /tmp/webhook-outbox-smoke.json` | pass |
| focused test | `.venv/bin/python -m pytest -q tests/regression/test_webhook_outbox_smoke.py tests/regression/test_api_contracts.py::test_sqlite_webhook_outbox_persists_success_and_failure_records` | pass |
| syntax | `python3 -m py_compile scripts/webhook-outbox-smoke.py` | pass |
| ruff | `.venv/bin/ruff format --check ... && .venv/bin/ruff check ...` | pass |
| task docs | `validate_task_docs.py --phase closeout` | pass at closeout |
| task tree | `validate_tasks_tree.py --phase auto` | pass |
| quick local CI | `bash scripts/local-ci.sh --profile quick` | pass before ship |

# Actual Evidence

| 验证项 | 命令 | 结果 |
| --- | --- | --- |
| smoke CLI | `bash scripts/webhook-outbox-smoke.sh --output-json /tmp/webhook-outbox-smoke.json` | passed，16 checks |
| focused tests | `.venv/bin/python -m pytest -q tests/regression/test_webhook_outbox_smoke.py tests/regression/test_api_contracts.py` | passed，72 tests |
| ruff | `.venv/bin/ruff format --check ... && .venv/bin/ruff check ...` | passed |
| secret scan | `python3 scripts/secret-scan.py --output-json /tmp/fatecat-secret-scan-0056.json` | passed，findingCount 0 |
| quick local CI | `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0056-final` | passed，144 regression tests，evidence `/tmp/fatecat-local-ci-0056-final` |

# Review Gate

| 维度 | Gate |
| --- | --- |
| 正确性 | succeeded/failed outbox、attempt count、rebuild load 都有检查。 |
| 可读性 | outbox record 字段少而明确，API 输出不含内部对象。 |
| 架构 | 不新增 runtime，不改 report job 主状态机。 |
| 安全 | 不保存或输出 secret、正文、姓名、出生地区、完整 URL。 |
| 性能 | 每个 terminal webhook 只写少量 SQLite record。 |

# Runtime Verification Gate

- 本地可验证：SQLite outbox record、dispatch update、manager rebuild、API summary、privacy boundary。
- 外部连通验证待执行：真实公网 webhook、external backend、自动重投 worker、multi-worker lock、production worker restart。

# Ship Readiness

- 所有 TODO 勾选。
- `STATUS.md` 全节点 Done。
- 验证命令写入 Recent Evidence。
- worktree clean after commit/push。

# Task Package Acceptance

- 任务文档无占位符。
- `TODO.md` 只包含叶子节点。
- `INDEX.md` 新增 0056。
- 文档不夸大为 MI-NEXT-03 完成。

# Anti-Goals

- 不声明测算基础设施 100%。
- 不声明 external backend、分布式 worker、生产级自动重投或真实 webhook live smoke 完成。
