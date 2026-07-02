# Task-Level Acceptance

本任务完成必须满足：

- SQLite backend 能持久保存可选 `task_payload`。
- `ReportJobManager` 能用注册的 factory 重建 queued/running 任务 callable。
- 可重建任务在新 manager 中重新入队并最终成功完成。
- 无 payload 或无 factory 的 active 任务继续标记 failed，并追加 `job.recovered_failed`。
- Web 报告任务和标准 Markdown 报告任务传入可重建 payload。
- payload/API/smoke summary 不包含 webhook secret、完整 webhook URL、Markdown 正文、token、DSN 或生产路径。
- quick local CI 执行 replayable recovery smoke。
- 文档明确当前是本地 replayable baseline，不是 external backend、分布式 worker 或 exactly-once。

# Validation Plan

| 验证项 | 命令 | 期望 |
| --- | --- | --- |
| smoke CLI | `bash scripts/report-job-replayable-recovery-smoke.sh --output-json /tmp/report-job-replayable-recovery-smoke.json` | pass |
| focused test | `.venv/bin/python -m pytest -q tests/regression/test_report_job_replayable_recovery_smoke.py tests/regression/test_api_contracts.py` | pass |
| syntax | `python3 -m py_compile domains/experience-delivery/services/fatecat-delivery/src/report_jobs.py scripts/report-job-replayable-recovery-smoke.py` | pass |
| ruff | `.venv/bin/ruff format --check ... && .venv/bin/ruff check ...` | pass |
| secret scan | `python3 scripts/secret-scan.py --output-json /tmp/fatecat-secret-scan-0057.json` | pass |
| task docs | `validate_task_docs.py --phase closeout` | pass at closeout |
| task tree | `validate_tasks_tree.py --phase auto` | pass |
| quick local CI | `bash scripts/local-ci.sh --profile quick` | pass before ship |

# Actual Evidence

| 验证项 | 命令 | 结果 |
| --- | --- | --- |
| smoke CLI | `bash scripts/report-job-replayable-recovery-smoke.sh --output-json /tmp/report-job-replayable-recovery-smoke.json` | passed，8 checks |
| focused tests | `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py tests/regression/test_report_job_replayable_recovery_smoke.py tests/regression/test_report_job_restart_recovery_smoke.py tests/regression/test_webhook_outbox_smoke.py` | passed，77 tests |
| ruff | `.venv/bin/ruff format --check ... && .venv/bin/ruff check ...` | passed |
| secret scan | `python3 scripts/secret-scan.py --output-json /tmp/fatecat-secret-scan-0057.json` | passed，findingCount 0 |
| task docs | `validate_task_docs.py --phase decompose` | passed |
| task tree | `validate_tasks_tree.py --phase auto --format markdown` | passed，57 valid / 0 invalid |
| quick local CI | `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0057` | passed，147 regression tests，evidence `/tmp/fatecat-local-ci-0057` |

# Review Gate

| 维度 | Gate |
| --- | --- |
| 正确性 | replayable job 成功恢复；non-replayable job 仍安全失败。 |
| 可读性 | payload/factory 语义明确，不隐藏魔法序列化。 |
| 架构 | 不引入外部 runtime，不破坏现有 manager/store 边界。 |
| 安全 | 不持久化 secret、完整 URL、报告正文或真实用户隐私。 |
| 性能 | manager 重建只恢复有限 active job；无额外热路径全量重算。 |

# Runtime Verification Gate

- 本地可验证：SQLite task payload、factory requeue、manager rebuild、success/failure event、privacy boundary。
- 外部连通验证待执行：external backend、multi-worker lock、production worker restart、真实 webhook live smoke。

# Ship Readiness

- 所有 TODO 勾选。
- `STATUS.md` 全节点 Done。
- 验证命令写入 Recent Evidence。
- worktree clean after commit/push。

# Task Package Acceptance

- 任务文档无占位符。
- `TODO.md` 只包含叶子节点。
- `INDEX.md` 新增 0057。
- 文档不夸大为 MI-NEXT-03 完成。

# Anti-Goals

- 不声明测算基础设施 100%。
- 不声明 external backend、分布式 worker、exactly-once、生产级自动重投或真实 webhook live smoke 完成。
