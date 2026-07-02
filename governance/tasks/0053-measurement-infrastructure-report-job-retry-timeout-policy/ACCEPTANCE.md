# Task-Level Acceptance

本任务完成必须满足：

- 默认 report job 行为保持：`maxAttempts=1`，timeout disabled。
- 显式配置 `maxAttempts>1` 时，retryable exception 会重试，最终成功保留 result。
- `ReportJobNonRetryableError` 不重试，并在事件中标记 non-retryable。
- 显式配置 `attemptTimeoutSeconds>0` 时，超时 attempt 会进入 failed 或 retry，事件可见。
- API `CalculationJob` payload 暴露 `attempts`、`maxAttempts`、`attemptTimeoutSeconds`、`retryBackoffSeconds`。
- SQLite store 兼容并持久化 policy 字段和 attempt count。
- 文档明确 timeout 当前不是生产硬中断，callback retry/outbox 和 external backend 仍未完成。

# Validation Plan

| 验证项 | 命令 | 期望 |
| --- | --- | --- |
| focused report job tests | `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py -k 'report_job or sqlite_report_job_store'` | pass |
| webhook smoke | `.venv/bin/python -m pytest -q tests/regression/test_webhook_smoke.py` | pass |
| syntax | `python3 -m py_compile domains/experience-delivery/services/fatecat-delivery/src/report_jobs.py domains/experience-delivery/services/fatecat-delivery/src/main.py` | pass |
| ruff | `.venv/bin/ruff format --check ... && .venv/bin/ruff check ...` | pass |
| task docs | `validate_task_docs.py --phase closeout` | pass at closeout |
| task tree | `validate_tasks_tree.py --phase auto` | pass |
| quick local CI | `bash scripts/local-ci.sh --profile quick` | pass before ship |

# Review Gate

| 维度 | Gate |
| --- | --- |
| 正确性 | retry、non-retryable、timeout 和默认路径都有测试。 |
| 可读性 | policy 与 attempt handling 集中在 `report_jobs.py`。 |
| 架构 | 不新增外部 runtime，不破坏 store 抽象。 |
| 安全 | events 不包含姓名、出生地区、Markdown、请求体、secret 或原始异常文本。 |
| 性能 | retry 有 max attempts；timeout disabled by default；无无限循环。 |

# Runtime Verification Gate

- 本地可验证：memory/sqlite、event history、retry policy、timeout status baseline。
- 外部连通验证待执行：production external backend、hard timeout、callback outbox、multi-worker lock。

# Ship Readiness

- 所有 TODO 勾选。
- `STATUS.md` 全节点 Done。
- 验证命令写入 Recent Evidence。
- worktree clean after commit/push。

# Task Package Acceptance

- 任务文档无占位符。
- `TODO.md` 只包含叶子节点。
- `INDEX.md` 新增 0053。
- 文档不夸大为 MI-NEXT-03 完成。

# Anti-Goals

- 不声明测算基础设施 100%。
- 不声明生产硬 timeout、callback retry/outbox 或 external backend 完成。
- 不新增预测体系。
