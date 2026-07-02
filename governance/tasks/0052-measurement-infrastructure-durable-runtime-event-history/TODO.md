# Execution Checklist

[x] TP-01.01 | P0 | 读取既有 job store、webhook baseline、API 文档、roadmap 与当前 diff | Verify: `rg` / `sed` 读取相关文件 | Gate: event history 切片边界明确 | Parallelizable: Yes
[x] TP-02.01 | P0 | 增加 ReportJobEvent 模型、memory/sqlite event store 和状态机事件写入 | Verify: focused pytest + py_compile | Gate: 状态变化可写入事件历史 | Parallelizable: No
[x] TP-02.02 | P0 | 在 API CalculationJob 响应中暴露 CalculationJobEvent | Verify: focused API contract test | Gate: `events` 字段存在且结构稳定 | Parallelizable: No
[x] TP-03.01 | P0 | 增加 report job event history、SQLite persistence 和隐私回归断言 | Verify: `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py -k 'report_job or sqlite_report_job_store'` | Gate: 成功、重建、recovery failed、隐私断言通过 | Parallelizable: No
[x] TP-03.02 | P0 | 更新 API 文档、roadmap、delivery AGENTS 和任务索引 | Verify: `git diff -- docs governance domains/experience-delivery/services/fatecat-delivery/AGENTS.md` | Gate: 文档口径不夸大能力 | Parallelizable: No
[x] TP-04.01 | P0 | 运行 focused tests、任务文档校验、lint/hygiene 与 git 检查 | Verify: pytest、validators、ruff/py_compile、`git diff --check` | Gate: 全部通过且无活动 blocker | Parallelizable: No
