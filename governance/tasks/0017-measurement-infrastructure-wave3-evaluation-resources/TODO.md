# Execution Checklist
[x] TP-01.01 | P0 | 盘点 data-products、MingLi-Bench runner、golden tests 与 API 缺口 | Verify: `find domains/fate-analysis/data-products -maxdepth 4 -type f` | Gate: 已确认 Dataset/EvaluationRun 当前只有枚举没有资源层。 | Parallelizable: No
[x] TP-01.02 | P0 | 回填 0017 任务契约与文档字段 | Verify: `validate_task_docs.py --phase decompose` | Gate: 任务文档无占位符且依赖图可解析。 | Parallelizable: No
[x] TP-02.01 | P0 | 新增 Dataset schema | Verify: `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py -k 'dataset or evaluation'` | Gate: Dataset 必填字段、usageRole、本地可验证性和隐私边界有测试断言。 | Parallelizable: No
[x] TP-02.02 | P0 | 新增 EvaluationRun schema | Verify: `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py -k 'evaluation'` | Gate: EvaluationRun 必填字段、datasetIds、commands 和 gateType 有测试断言。 | Parallelizable: No
[x] TP-02.03 | P0 | 扩展 resource schema | Verify: `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py -k 'resource'` | Gate: resource schema 包含 datasetResourceFields 和 evaluationRunResourceFields。 | Parallelizable: No
[x] TP-03.01 | P0 | 登记节气、八字、紫微 golden Dataset | Verify: `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py -k 'evaluation or dataset'` | Gate: registry 覆盖关键 golden 数据集并标记 evaluation_only。 | Parallelizable: No
[x] TP-03.02 | P0 | 登记 MingLi-Bench benchmark Dataset | Verify: `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py -k 'evaluation or dataset'` | Gate: MingLi-Bench 标记 offline/evaluation_only/requires_reference_repo。 | Parallelizable: No
[x] TP-03.03 | P0 | 登记 quick CI / golden / benchmark EvaluationRun | Verify: `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py -k 'evaluation'` | Gate: EvaluationRun links、commands、releaseRequired 和外部验证口径明确。 | Parallelizable: No
[x] TP-04.01 | P0 | 新增 `/evaluations` list/detail API | Verify: `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py -k 'evaluation'` | Gate: canonical 与 alias 返回一致，detail 可按 id 查询。 | Parallelizable: No
[x] TP-04.02 | P0 | 更新 `/metadata` 与 OpenAPI 断言 | Verify: `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py -k 'metadata or openapi or evaluation'` | Gate: metadata developer links 和 OpenAPI paths 包含 evaluations。 | Parallelizable: No
[x] TP-05.01 | P0 | 补 contract/API 回归测试 | Verify: `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py tests/regression/test_api_contracts.py -k 'evaluation or dataset or resource or metadata or openapi'` | Gate: focused tests 全部通过。 | Parallelizable: No
[x] TP-05.02 | P1 | 更新 API 文档、路线图和 contracts AGENTS | Verify: `rg -n "EvaluationRun|Dataset|/evaluations|评测资源" docs contracts governance/tasks/0017-measurement-infrastructure-wave3-evaluation-resources` | Gate: 人类文档与 API/契约一致。 | Parallelizable: No
[x] TP-06.01 | P0 | 执行本地门禁 | Verify: `bash scripts/local-ci.sh --profile quick && git diff --check` | Gate: quick CI 和 diff check 通过。 | Parallelizable: No
[x] TP-06.02 | P0 | 回填 closeout 状态和验证证据 | Verify: `validate_task_docs.py --phase closeout && validate_tasks_tree.py --phase auto` | Gate: 0017 closeout 和全任务树校验通过。 | Parallelizable: No

说明：
- 每一行后续必须绑定 `TP-XX(.YY...)`
- 不允许出现无归属 TODO
