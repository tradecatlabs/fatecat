# Task-Level Acceptance

本任务完成必须满足：

- SQLite backend 能查询 pending/failed webhook outbox record。
- `ReportJobManager` 能通过注入的 delivery resolver 重建 callback 配置并重投 outbox。
- 可重投 outbox 在新 manager 中最终成功时更新为 `succeeded`，并追加 redelivery 相关事件。
- 未提供 resolver 或 resolver 返回空时，不自动投递、不泄露配置，outbox 保持可审计状态。
- resolver 抛异常时，不调用 dispatcher，不泄露异常原文，并记录可审计的 `webhook.redelivery_failed`。
- smoke/API/test summary 不包含 webhook secret、完整 webhook URL、Markdown 正文、token、DSN 或生产路径。
- quick local CI 执行 webhook outbox redelivery smoke。
- 文档明确当前是本地 redelivery baseline，不是 external backend、分布式 worker、真实公网 live smoke 或 exactly-once。

# Validation Plan

| 验证项 | 命令 | 期望 |
| --- | --- | --- |
| smoke CLI | `bash scripts/webhook-outbox-redelivery-smoke.sh --output-json /tmp/webhook-outbox-redelivery-smoke.json` | pass |
| focused test | `.venv/bin/python -m pytest -q tests/regression/test_webhook_outbox_redelivery_smoke.py tests/regression/test_api_contracts.py` | pass |
| syntax | `python3 -m py_compile domains/experience-delivery/services/fatecat-delivery/src/report_jobs.py scripts/webhook-outbox-redelivery-smoke.py` | pass |
| ruff | `.venv/bin/ruff format --check ... && .venv/bin/ruff check ...` | pass |
| secret scan | `python3 scripts/secret-scan.py --output-json /tmp/fatecat-secret-scan-0058.json` | pass |
| task docs | `validate_task_docs.py --phase closeout` | pass at closeout |
| task tree | `validate_tasks_tree.py --phase auto` | pass |
| quick local CI | `bash scripts/local-ci.sh --profile quick` | pass before ship |

# Actual Evidence

| 验证项 | 命令 | 结果 |
| --- | --- | --- |
| smoke CLI | `bash scripts/webhook-outbox-redelivery-smoke.sh --output-json /tmp/webhook-outbox-redelivery-smoke.json` | passed，13 checks |
| focused tests | `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py tests/regression/test_webhook_outbox_smoke.py tests/regression/test_webhook_outbox_redelivery_smoke.py tests/regression/test_report_job_replayable_recovery_smoke.py tests/regression/test_report_job_restart_recovery_smoke.py` | passed，82 tests |
| ruff | `.venv/bin/ruff format ... && .venv/bin/ruff check ...` | passed |
| secret scan | `bash scripts/secret-scan.sh --output-json /tmp/fatecat-secret-scan-0058.json` | passed，findingCount 0 |
| task docs | `validate_task_docs.py --phase decompose` | passed |
| task tree | `validate_tasks_tree.py --phase auto --format markdown` | passed，58 valid / 0 invalid |
| quick local CI | `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0058-final` | passed，152 regression tests |

# Review Gate

| 维度 | Gate |
| --- | --- |
| 正确性 | redelivery success 通过；resolver missing 不误投；resolver error 转成脱敏失败事件。 |
| 可读性 | resolver/redelivery 语义明确，不隐藏 secret 持久化。 |
| 架构 | 不引入外部 runtime，不破坏现有 manager/store 边界。 |
| 安全 | 不持久化 secret、完整 URL、报告正文或真实用户隐私。 |
| 性能 | manager 重建只扫描有限 pending/failed outbox；无额外热路径全量操作。 |

# Runtime Verification Gate

- 本地可验证：SQLite outbox 查询、resolver redelivery、manager rebuild、success/missing resolver event、privacy boundary。
- 外部连通验证待执行：external backend、multi-worker lock、真实 webhook live smoke、secret encryption/rotation。

# Ship Readiness

- 所有 TODO 勾选。
- `STATUS.md` 全节点 Done。
- 验证命令写入 Recent Evidence。
- worktree clean after commit/push。

# Task Package Acceptance

- 任务文档无占位符。
- `TODO.md` 只包含叶子节点。
- `INDEX.md` 新增 0058。
- 文档不夸大为 MI-NEXT-03 完成。

# Anti-Goals

- 不声明测算基础设施 100%。
- 不声明 external backend、分布式 worker、exactly-once、生产级 encrypted secret storage 或真实 webhook live smoke 完成。
