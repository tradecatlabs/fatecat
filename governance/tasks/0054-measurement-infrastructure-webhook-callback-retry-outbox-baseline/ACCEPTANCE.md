# Task-Level Acceptance

本任务完成必须满足：

- 默认 webhook callback 行为保持：`maxAttempts=1`，不额外重试。
- 显式配置 `maxAttempts>1` 时，callback 第一次失败可重试，最终成功保留 `webhook.delivery_succeeded`。
- callback 全部失败时，事件历史包含每次 attempt failure、retry scheduled 和最终 `webhook.delivery_failed`。
- webhook delivery event metadata 不包含 webhook URL、secret、Markdown、姓名、出生地区、请求体或原始异常文本。
- production-readiness 校验 webhook retry env vars。
- 文档明确当前只是本地 callback retry/outbox trail baseline，跨进程持久 outbox 和 external backend 仍未完成。

# Validation Plan

| 验证项 | 命令 | 期望 |
| --- | --- | --- |
| focused webhook tests | `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py -k 'webhook or report_job'` | pass |
| webhook smoke | `.venv/bin/python -m pytest -q tests/regression/test_webhook_smoke.py` | pass |
| syntax | `python3 -m py_compile domains/experience-delivery/services/fatecat-delivery/src/report_jobs.py domains/experience-delivery/services/fatecat-delivery/src/main.py` | pass |
| ruff | `.venv/bin/ruff format --check ... && .venv/bin/ruff check ...` | pass |
| production readiness static gate | `FATE_CORS_ALLOW_ORIGINS=https://example.com FATE_API_TOKEN=<redacted-local-token> FATE_WEBHOOK_MAX_ATTEMPTS=2 FATE_WEBHOOK_RETRY_BACKOFF_SECONDS=0 bash scripts/production-readiness.sh --skip-bootstrap` | pass |
| task docs | `validate_task_docs.py --phase closeout` | pass at closeout |
| task tree | `validate_tasks_tree.py --phase auto` | pass |
| quick local CI | `bash scripts/local-ci.sh --profile quick` | pass before ship |

# Review Gate

| 维度 | Gate |
| --- | --- |
| 正确性 | retry success、final failure 和 default once 都有测试。 |
| 可读性 | webhook policy 与 attempt handling 集中在 `report_jobs.py`。 |
| 架构 | 不新增外部 runtime，不破坏 webhook dispatcher 抽象。 |
| 安全 | events 不包含 URL、secret、用户输入、报告正文或原始异常文本。 |
| 性能 | retry 有 max attempts；默认不重试；无无限循环。 |

# Runtime Verification Gate

- 本地可验证：memory/sqlite event history、webhook retry events、本地 smoke。
- 外部连通验证待执行：production persistent outbox、external backend、真实公网 webhook live smoke、multi-worker lock。

# Ship Readiness

- 所有 TODO 勾选。
- `STATUS.md` 全节点 Done。
- 验证命令写入 Recent Evidence。
- worktree clean after commit/push。

# Task Package Acceptance

- 任务文档无占位符。
- `TODO.md` 只包含叶子节点。
- `INDEX.md` 新增 0054。
- 文档不夸大为 MI-NEXT-03 完成。

# Anti-Goals

- 不声明测算基础设施 100%。
- 不声明生产持久 outbox、external backend 或 webhook live smoke 完成。
- 不新增预测体系。
