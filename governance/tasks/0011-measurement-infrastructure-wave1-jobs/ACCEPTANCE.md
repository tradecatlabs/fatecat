# Task-Level Acceptance
- 同一 `Idempotency-Key` 在 TTL 生命周期内返回同一 job。
- job 状态支持 `cancelled`。
- cancel API 可用。
- job payload 暴露 `CalculationJob` resource links。
- metrics 包含 cancelled job 计数。
- 文档说明单进程/TTL/不能强杀 running 线程边界。

# Validation Plan
| 验证项 | 命令 |
| --- | --- |
| 定向 job/API | `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py -k 'report_job or metadata or openapi'` |
| 综合定向 | `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py tests/regression/test_api_contracts.py -k 'capability or metadata or openapi or error or report_job'` |
| Lint | `.venv/bin/ruff check domains/experience-delivery/services/fatecat-delivery/src/main.py domains/experience-delivery/services/fatecat-delivery/src/report_jobs.py tests/regression/test_api_contracts.py tests/regression/test_capability_protocol.py` |
| Format | `.venv/bin/ruff format --check ...` |
| Type | `.venv/bin/mypy domains/fate-analysis/services/fate-core/src/fate_core` |
| Quick CI | `bash scripts/local-ci.sh --profile quick` |
| Governance | `python3 governance/tools/validate_governance_package.py --project-root . --strict` |
| Task docs | `validate_task_docs.py --phase closeout`、`validate_tasks_tree.py --phase auto` |

# Review Gate
- 不引入跨进程幂等虚假承诺。
- 不改变报告内容。
- 不新增无界队列或无界重试。
- cancel 后不得输出已取消任务的 result。

# Runtime Verification Gate
- API tests 覆盖 idempotency、cancel、resource links。
- quick CI 覆盖现有报告 job 行为回归。

# Ship Readiness
- quick CI、governance strict、task validators 通过后 closeout。

# Task Package Acceptance
| Node | Acceptance |
| --- | --- |
| TP-01 | job manager lifecycle 正确 |
| TP-02 | API 暴露 resource/cancel |
| TP-03 | tests/docs/schema 同步 |
| TP-04 | 本地门禁通过 |

# Anti-Goals
- 不实现 Redis/RQ/Celery
- 不得虚构证据
- 不得越权补全未确认信息
