# Task-Level Acceptance

本任务完成必须满足：

- 独立 smoke 能创建临时 SQLite report job store，并验证 manager rebuild 后旧 running job 被标记为 `failed`。
- summary 包含 `job.recovered_failed` event evidence。
- summary 不包含 Markdown 正文、姓名、出生地区、token、secret、DSN 或真实生产路径。
- shell wrapper 可运行并写出 JSON summary。
- quick local CI 执行 restart recovery smoke。
- 文档明确当前是 restart-safe failure baseline，不是任务继续执行或 external backend。

# Validation Plan

| 验证项 | 命令 | 期望 |
| --- | --- | --- |
| smoke CLI | `bash scripts/report-job-restart-recovery-smoke.sh --output-json /tmp/report-job-restart-recovery-smoke.json` | pass |
| focused test | `.venv/bin/python -m pytest -q tests/regression/test_report_job_restart_recovery_smoke.py` | pass |
| syntax | `python3 -m py_compile scripts/report-job-restart-recovery-smoke.py` | pass |
| ruff | `.venv/bin/ruff format --check scripts/report-job-restart-recovery-smoke.py tests/regression/test_report_job_restart_recovery_smoke.py && .venv/bin/ruff check ...` | pass |
| task docs | `validate_task_docs.py --phase closeout` | pass at closeout |
| task tree | `validate_tasks_tree.py --phase auto` | pass |
| quick local CI | `bash scripts/local-ci.sh --profile quick` | pass before ship |

# Review Gate

| 维度 | Gate |
| --- | --- |
| 正确性 | running job rebuild、event history、idempotency behavior 都有检查。 |
| 可读性 | smoke 入口自包含，输出 JSON 可读。 |
| 架构 | 不新增 runtime，不改 report job 状态机。 |
| 安全 | summary 不输出用户输入、正文、secret、DSN 或全局 DB 路径。 |
| 性能 | 使用临时 SQLite、短等待、无网络。 |

# Runtime Verification Gate

- 本地可验证：SQLite manager rebuild、`job.recovered_failed` event、idempotency lookup。
- 外部连通验证待执行：external backend、任务继续执行、multi-worker lock、production worker restart。

# Ship Readiness

- 所有 TODO 勾选。
- `STATUS.md` 全节点 Done。
- 验证命令写入 Recent Evidence。
- worktree clean after commit/push。

# Task Package Acceptance

- 任务文档无占位符。
- `TODO.md` 只包含叶子节点。
- `INDEX.md` 新增 0055。
- 文档不夸大为 MI-NEXT-03 完成。

# Anti-Goals

- 不声明测算基础设施 100%。
- 不声明 external backend、分布式 worker 或任务 resume execution 完成。
