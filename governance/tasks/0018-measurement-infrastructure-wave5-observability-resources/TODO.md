# Execution Checklist
[x] TP-01.01 | P0 | 盘点 health、ready、metrics、requestId 和结构化日志现状 | Verify: `rg -n "X-Request-ID|/metrics|_log_structured|/ready|/health" domains/experience-delivery/services/fatecat-delivery/src/main.py tests/regression/test_api_contracts.py` | Gate: 已确认现有 signals 与缺失发现层。 | Parallelizable: No
[x] TP-01.02 | P0 | 回填 0018 任务契约与文档字段 | Verify: `validate_task_docs.py --phase decompose` | Gate: 任务文档无占位符且依赖图可解析。 | Parallelizable: No
[x] TP-02.01 | P0 | 新增 ObservabilitySignal schema | Verify: `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py -k 'observability or resource'` | Gate: 必填字段、signalType、status、privacyBoundary 和 externalConnectivity 有测试断言。 | Parallelizable: No
[x] TP-02.02 | P0 | 新增 observability registry | Verify: `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py -k observability` | Gate: registry 覆盖 available 与 planned signals。 | Parallelizable: No
[x] TP-02.03 | P0 | 扩展 resource schema | Verify: `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py -k resource` | Gate: resource schema 包含 observabilitySignalResourceFields。 | Parallelizable: No
[x] TP-03.01 | P0 | 新增 `/observability` list/detail API | Verify: `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py -k observability` | Gate: canonical 与 alias 返回一致，detail 可按 id 查询。 | Parallelizable: No
[x] TP-03.02 | P0 | 更新 `/metadata` 与 OpenAPI 断言 | Verify: `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py -k 'metadata or openapi or observability'` | Gate: metadata developer links 和 OpenAPI paths 包含 observability。 | Parallelizable: No
[x] TP-04.01 | P0 | 补 contract/API 回归测试 | Verify: `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py tests/regression/test_api_contracts.py -k 'observability or resource or metadata or openapi'` | Gate: focused tests 全部通过。 | Parallelizable: No
[x] TP-04.02 | P1 | 更新 API 文档、路线图和 contracts AGENTS | Verify: `rg -n "ObservabilitySignal|/observability|trace/metric/log|观测" docs contracts governance/tasks/0018-measurement-infrastructure-wave5-observability-resources` | Gate: 人类文档与 API/契约一致。 | Parallelizable: No
[x] TP-05.01 | P0 | 执行本地门禁 | Verify: `bash scripts/local-ci.sh --profile quick && git diff --check` | Gate: quick CI 和 diff check 通过。 | Parallelizable: No
[x] TP-05.02 | P0 | 回填 closeout 状态和验证证据 | Verify: `validate_task_docs.py --phase closeout && validate_tasks_tree.py --phase auto` | Gate: 0018 closeout 和全任务树校验通过。 | Parallelizable: No

说明：
- 每一行后续必须绑定 `TP-XX(.YY...)`
- 不允许出现无归属 TODO
