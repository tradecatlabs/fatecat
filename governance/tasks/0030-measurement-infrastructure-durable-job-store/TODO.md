# Execution Checklist
[x] TP-01.01 | P0 | 盘点 report job manager、API、metrics、文档和测试 | Verify: `rg -n "ReportJobManager|report_job_manager|Idempotency-Key|fatecat_report_job" domains/experience-delivery/services/fatecat-delivery/src tests docs/reference-materials contracts` | Gate: 现有内存边界和缺口明确 | Parallelizable: No
[x] TP-01.02 | P0 | 回填任务契约、风险和验证计划 | Verify: `validate_task_docs.py --phase decompose` | Gate: 任务文档无占位符且任务树可解析 | Parallelizable: No
[x] TP-02.01 | P0 | 新增 ReportJobStore 抽象、memory store 和 SQLite store | Verify: `rg -n "class ReportJobStore|class SQLiteReportJobStore|sqlite3" domains/experience-delivery/services/fatecat-delivery/src/report_jobs.py` | Gate: store 抽象存在且无新增依赖 | Parallelizable: No
[x] TP-02.02 | P0 | 接入 ReportJobManager 持久化、重建恢复、幂等和取消 | Verify: `rg -n "_load_persisted_jobs|_persist_locked|任务执行器已重启|idempotency" domains/experience-delivery/services/fatecat-delivery/src/report_jobs.py` | Gate: 任务状态写入 store，active rebuild 明确失败 | Parallelizable: No
[x] TP-02.03 | P0 | 接入 main.py 环境变量、metadata、metrics 和 production-readiness | Verify: `rg -n "FATE_REPORT_JOB_STORE|FATE_REPORT_JOB_DB_PATH|reportJobStore|report_job_store_backend_info" domains/experience-delivery/services/fatecat-delivery/src/main.py scripts/production-readiness.sh` | Gate: runtime 可发现且生产预检有边界 | Parallelizable: No
[x] TP-03.01 | P0 | 新增 SQLite 持久化、幂等、取消和重建失败回归 | Verify: `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py -k 'sqlite_report_job_store or markdown_report_job or ready_and_metrics or metadata_and_reports'` | Gate: focused tests 通过 | Parallelizable: No
[x] TP-03.02 | P0 | 更新 env example、API 文档、registry、roadmap 和 AGENTS | Verify: `rg -n "FATE_REPORT_JOB_STORE|SQLite job store|report_job_store_backend_info|memory/sqlite" docs/reference-materials contracts infra/environments domains/experience-delivery/services/fatecat-delivery/AGENTS.md` | Gate: 文档同步且不夸大能力 | Parallelizable: No
[x] TP-04.01 | P0 | 执行 JSON、focused tests、shell syntax、ruff/format、secret scan、quick CI 和 diff check | Verify: `bash scripts/local-ci.sh --profile quick && git diff --check` | Gate: 本地门禁全部通过 | Parallelizable: No
[x] TP-04.02 | P0 | 回填 closeout 状态、全任务树验证和 closeout packet | Verify: `validate_task_docs.py --phase closeout && validate_tasks_tree.py --phase auto && build_task_closeout.py` | Gate: 0030 closeout 和全任务树校验通过 | Parallelizable: No

说明：
- 每一行必须绑定 `TP-XX(.YY...)`。
- 不允许出现无归属 TODO。
