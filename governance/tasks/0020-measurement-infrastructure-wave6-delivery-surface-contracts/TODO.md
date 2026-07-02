# Execution Checklist
[x] TP-01.01 | P0 | 盘点 Web/API/Bot/CLI/Skill 输出链路和一致性测试 | Verify: `rg -n "reportSystem|generate_full_report|build_web_report_result|Telegram|Bot|CLI|Skill|/web|/api/v1/report" apps ai domains contracts docs references scripts tests` | Gate: 已确认现有交付面与缺失发现层。 | Parallelizable: No
[x] TP-01.02 | P0 | 回填 0020 任务契约与文档字段 | Verify: `validate_task_docs.py --phase decompose` | Gate: 任务文档无占位符且依赖图可解析。 | Parallelizable: No
[x] TP-02.01 | P0 | 新增 DeliverySurface schema | Verify: `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py -k 'surface or resource'` | Gate: 必填字段、surfaceType、status、externalConnectivity 和 invariants 有测试断言。 | Parallelizable: No
[x] TP-02.02 | P0 | 新增 delivery registry | Verify: `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py -k surface` | Gate: registry 覆盖 available、partial 与 manual surfaces。 | Parallelizable: No
[x] TP-02.03 | P0 | 扩展 resource schema 与 contracts AGENTS | Verify: `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py -k resource` | Gate: resource schema 包含 deliverySurfaceResourceFields。 | Parallelizable: No
[x] TP-03.01 | P0 | 新增 `/surfaces` list/detail API | Verify: `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py -k surface` | Gate: canonical 与 alias 返回一致，detail 可按 id 查询。 | Parallelizable: No
[x] TP-03.02 | P0 | 更新 `/metadata` 与 OpenAPI 断言 | Verify: `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py -k 'metadata or openapi or surface'` | Gate: metadata developer links 和 OpenAPI paths 包含 surfaces。 | Parallelizable: No
[x] TP-04.01 | P0 | 补 contract/API/entrypoint 回归测试 | Verify: `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py tests/regression/test_api_contracts.py tests/regression/test_entrypoint_consistency.py -k 'surface or resource or metadata or openapi or entrypoint'` | Gate: focused tests 全部通过。 | Parallelizable: No
[x] TP-04.02 | P1 | 更新 API 文档、路线图和 contracts AGENTS | Verify: `rg -n "DeliverySurface|/surfaces|surface\\.telegram_bot|surface\\.cli|外部连通验证待执行" docs contracts governance/tasks/0020-measurement-infrastructure-wave6-delivery-surface-contracts` | Gate: 人类文档与 API/契约一致。 | Parallelizable: No
[x] TP-05.01 | P0 | 执行本地门禁 | Verify: `bash scripts/local-ci.sh --profile quick && git diff --check` | Gate: quick CI 和 diff check 通过。 | Parallelizable: No
[x] TP-05.02 | P0 | 回填 closeout 状态和验证证据 | Verify: `validate_task_docs.py --phase closeout && validate_tasks_tree.py --phase auto` | Gate: 0020 closeout 和全任务树校验通过。 | Parallelizable: No

说明：
- 每一行后续必须绑定 `TP-XX(.YY...)`
- 不允许出现无归属 TODO
