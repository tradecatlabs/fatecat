# Acceptance Checklist

# Global Standards
- [x] 任务目标、范围、out-of-scope 和风险边界已落盘。
- [x] 默认 memory 后端保持兼容。
- [x] SQLite backend 可跨 manager 查询 succeeded/cancelled job 和 idempotency key。
- [x] active job 重建后标记 failed，不伪造继续执行。
- [x] metadata/metrics/production-readiness 暴露或校验 backend。
- [x] docs/registry/env examples/AGENTS 已同步。
- [x] quick CI、secret scan、diff check、task validators 和 closeout packet 全部通过。

# Task Package Checklists

## TP-01.01 盘点 job 运行面
- [x] Verify: `rg -n "ReportJobManager|report_job_manager|Idempotency-Key|fatecat_report_job" domains/experience-delivery/services/fatecat-delivery/src tests docs/reference-materials contracts`
- [x] Gate: 内存队列、幂等、取消、metrics 和文档缺口已确认。

## TP-01.02 回填任务契约
- [x] Verify: `validate_task_docs.py --phase decompose`
- [x] Gate: 任务树、store 边界和验证计划已落盘。

## TP-02.01 新增 store 抽象和 SQLite store
- [x] Verify: `rg -n "class ReportJobStore|class SQLiteReportJobStore|sqlite3|report_jobs" domains/experience-delivery/services/fatecat-delivery/src/report_jobs.py`
- [x] Gate: memory/sqlite 后端对象存在，未新增第三方依赖。

## TP-02.02 接入 manager 持久化和重建恢复
- [x] Verify: `rg -n "_load_persisted_jobs|_persist_locked|任务执行器已重启|idempotency" domains/experience-delivery/services/fatecat-delivery/src/report_jobs.py`
- [x] Gate: submit/run/cancel/expire 均持久化状态。

## TP-02.03 接入 main 配置、metadata、metrics 和 production-readiness
- [x] Verify: `rg -n "FATE_REPORT_JOB_STORE|FATE_REPORT_JOB_DB_PATH|reportJobStore|report_job_store_backend_info" domains/experience-delivery/services/fatecat-delivery/src/main.py scripts/production-readiness.sh`
- [x] Gate: 默认 memory；sqlite 可配置；多副本本地 store 被拒绝。

## TP-03.01 新增 SQLite 回归测试
- [x] Verify: `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py -k 'sqlite_report_job_store or markdown_report_job or ready_and_metrics or metadata_and_reports'`
- [x] Gate: SQLite finished/cancelled/active rebuild 和既有 job tests 通过。

## TP-03.02 更新文档和 registry
- [x] Verify: `rg -n "FATE_REPORT_JOB_STORE|SQLite job store|report_job_store_backend_info|memory/sqlite" docs/reference-materials contracts infra/environments domains/experience-delivery/services/fatecat-delivery/AGENTS.md`
- [x] Gate: 文档不夸大多副本或 webhook/retry 能力。

## TP-04.01 执行本地门禁
- [x] Verify: `bash scripts/local-ci.sh --profile quick && git diff --check`
- [x] Gate: quick CI 和 diff check 通过。

## TP-04.02 回填 closeout
- [x] Verify: `validate_task_docs.py --phase closeout && validate_tasks_tree.py --phase auto && build_task_closeout.py`
- [x] Gate: 0030 closeout 和全任务树校验通过。
