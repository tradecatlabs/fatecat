# Acceptance Checklist

# Global Standards
- [x] 明确不改生产算法和报告正文。
- [x] 明确不执行外部模型、token、Bot、线上服务。
- [x] 明确 Dataset/EvaluationRun 的隐私、用途、本地可验证性和风险边界。
- [x] 新增 schema、registry、API、docs、tests。
- [x] 运行 focused tests、lint、format、type check、quick CI。
- [x] closeout validators 通过。

# Task Package Checklists
## TP-01.01 asset inventory

Verify: `find domains/fate-analysis/data-products -maxdepth 4 -type f`

Gate: 已确认 Dataset/EvaluationRun 当前只有枚举没有资源层。

- [x] 已完成：盘点 data-products、golden tests、MingLi-Bench runner 和 API 缺口。

## TP-01.02 task contract

Verify: `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0017-measurement-infrastructure-wave3-evaluation-resources --phase decompose`

Gate: 任务文档无占位符且依赖图可解析。

- [x] 已回填：任务文档字段、依赖图、验收清单和状态表。

## TP-02.01 Dataset schema

Verify: `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py -k 'dataset or evaluation'`

Gate: Dataset 必填字段、usageRole、本地可验证性和隐私边界有测试断言。

- [x] 已完成：新增 Dataset schema，并由 protocol tests 覆盖。

## TP-02.02 EvaluationRun schema

Verify: `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py -k 'evaluation'`

Gate: EvaluationRun 必填字段、datasetIds、commands 和 gateType 有测试断言。

- [x] 已完成：新增 EvaluationRun schema，并由 protocol tests 覆盖。

## TP-02.03 resource schema

Verify: `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py -k 'resource'`

Gate: resource schema 包含 datasetResourceFields 和 evaluationRunResourceFields。

- [x] 已完成：resource schema 已补 Dataset/EvaluationRun 字段。

## TP-03.01 golden datasets

Verify: `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py -k 'evaluation or dataset'`

Gate: registry 覆盖关键 golden 数据集并标记 evaluation_only。

- [x] 已完成：registry 已登记节气、八字、紫微 golden Dataset。

## TP-03.02 benchmark datasets

Verify: `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py -k 'evaluation or dataset'`

Gate: MingLi-Bench 标记 offline/evaluation_only/requires_reference_repo。

- [x] 已完成：registry 已登记 MingLi-Bench offline benchmark Dataset。

## TP-03.03 evaluation runs

Verify: `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py -k 'evaluation'`

Gate: EvaluationRun links、commands、releaseRequired 和外部验证口径明确。

- [x] 已完成：registry 已登记 quick CI、solar terms golden、MingLi-Bench offline EvaluationRun。

## TP-04.01 evaluation API

Verify: `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py -k 'evaluation'`

Gate: canonical 与 alias 返回一致，detail 可按 id 查询。

- [x] 已完成：新增 `/evaluations` 和 `/api/v1/evaluations` list/detail API。

## TP-04.02 metadata and OpenAPI

Verify: `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py -k 'metadata or openapi or evaluation'`

Gate: metadata developer links 和 OpenAPI paths 包含 evaluations。

- [x] 已完成：metadata 和 OpenAPI 测试覆盖 evaluation links/paths。

## TP-05.01 regression tests

Verify: `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py tests/regression/test_api_contracts.py -k 'evaluation or dataset or resource or metadata or openapi'`

Gate: focused tests 全部通过。

- [x] 已通过：protocol focused 2 passed；API focused 3 passed。

## TP-05.02 docs

Verify: `rg -n "EvaluationRun|Dataset|/evaluations|评测资源" docs contracts governance/tasks/0017-measurement-infrastructure-wave3-evaluation-resources`

Gate: 人类文档与 API/契约一致。

- [x] 已完成：API 文档、100% 路线图、contracts AGENTS 已同步。

## TP-06.01 local gates

Verify: `bash scripts/local-ci.sh --profile quick && git diff --check`

Gate: quick CI 和 diff check 通过。

- [x] 已通过：quick CI 69 passed；ruff/mypy/diff check 通过。

## TP-06.02 task closeout

Verify: `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0017-measurement-infrastructure-wave3-evaluation-resources --phase closeout`

Gate: 0017 closeout 和全任务树校验通过。

- [x] 已完成：closeout 状态和验证证据已回填。
