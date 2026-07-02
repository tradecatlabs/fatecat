# Task-Level Acceptance
- 默认 `memory` report job backend 行为不回归。
- 新增 `SQLiteReportJobStore`，使用标准库 SQLite，不新增依赖。
- SQLite backend 能跨 manager 查询 succeeded job 的 metadata、result、input summary 和 idempotency key。
- SQLite backend 能跨 manager 查询 cancelled job。
- manager 重建时旧 `queued/running` job 被标记为 failed，并保留明确错误原因。
- `Idempotency-Key` 在 SQLite backend 中跨 manager 生效。
- `/metadata` 暴露 `quality.reportJobStore`。
- `/metrics` 暴露 `fatecat_report_job_store_backend_info{backend="memory|sqlite"}`。
- production-readiness 校验 `FATE_REPORT_JOB_STORE`、job queue/workers/TTL，并拒绝多副本本地 job store。
- 文档明确 SQLite 不是分布式任务系统。

# Validation Plan
| 验证项 | 命令 |
| --- | --- |
| JSON 格式 | `python3 -m json.tool contracts/fate/observability/registry.json >/dev/null && python3 -m json.tool contracts/fate/security/registry.json >/dev/null` |
| shell syntax | `bash -n scripts/production-readiness.sh` |
| focused tests | `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py -k 'sqlite_report_job_store or markdown_report_job or ready_and_metrics or metadata_and_reports'` |
| observability/security tests | `.venv/bin/python -m pytest -q tests/regression/test_observability_smoke.py tests/regression/test_security_smoke.py tests/regression/test_api_contracts.py -k 'observability or security or retention or sqlite_report_job_store or ready_and_metrics or metadata_and_reports'` |
| ruff | `.venv/bin/python -m ruff check domains/experience-delivery/services/fatecat-delivery/src/report_jobs.py domains/experience-delivery/services/fatecat-delivery/src/main.py tests/regression/test_api_contracts.py scripts/observability-smoke.py` |
| format | `.venv/bin/python -m ruff format --check domains/experience-delivery/services/fatecat-delivery/src/report_jobs.py domains/experience-delivery/services/fatecat-delivery/src/main.py tests/regression/test_api_contracts.py scripts/observability-smoke.py` |
| secret scan | `bash scripts/secret-scan.sh --output-json /tmp/fatecat-secret-scan-0030.json && python3 -m json.tool /tmp/fatecat-secret-scan-0030.json >/dev/null` |
| quick CI | `bash scripts/local-ci.sh --profile quick` |
| whitespace | `git diff --check` |
| closeout | `validate_task_docs.py --phase closeout && validate_tasks_tree.py --phase auto && build_task_closeout.py` |

# Review Gate
- 默认 backend 必须仍为 `memory`。
- SQLite backend 文档不得声明多副本、分布式队列或跨进程继续执行。
- queued/running 重建后必须失败，不得停留在误导性 running 状态。
- production-readiness 必须拒绝 replicas > 1 且 store 是 memory/sqlite。
- 运行态 DB 路径不得进入 tracked source。

# Runtime Verification Gate
- `test_sqlite_report_job_store_persists_finished_jobs_and_idempotency` 必须通过。
- `test_sqlite_report_job_store_persists_cancelled_jobs` 必须通过。
- `test_sqlite_report_job_store_marks_active_jobs_failed_after_rebuild` 必须通过。
- `test_markdown_report_job_*` 既有测试必须继续通过。

# Ship Readiness
- 当前任务完成后可声明：report job 具备默认 memory / 可选 SQLite 单副本本地持久状态 baseline。
- 不可声明：webhook、retry、external backend、多副本任务系统、crash 后继续执行、生产重启演练已完成。

# Task Package Acceptance
| Node | Acceptance |
| --- | --- |
| TP-01 | 现状、范围和风险已落盘。 |
| TP-02 | runtime store、main 配置、metrics、metadata、production-readiness 已实现。 |
| TP-03 | tests/docs/registry/env examples/AGENTS 已同步。 |
| TP-04 | quick CI、validators、closeout packet 通过。 |

# Anti-Goals
- 不接 webhook。
- 不实现 retry。
- 不接 Redis/Celery/RQ/Temporal。
- 不把 SQLite 写成多副本任务系统。
