# Acceptance Checklist

# Global Standards
- [x] 明确不引入外部监控平台。
- [x] 明确不改 `/metrics` 现有指标语义。
- [x] 明确 ObservabilitySignal 的 available/planned 边界。
- [x] 新增 schema、registry、API、docs、tests。
- [x] 运行 focused tests、lint、format、type check、quick CI。
- [x] closeout validators 通过。

# Task Package Checklists
## TP-01.01 observability inventory

Verify: `rg -n "X-Request-ID|/metrics|_log_structured|/ready|/health" domains/experience-delivery/services/fatecat-delivery/src/main.py tests/regression/test_api_contracts.py`

Gate: 已确认现有 signals 与缺失发现层。

- [x] 已完成：盘点 health、ready、metrics、requestId 和结构化日志。

## TP-01.02 task contract

Verify: `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0018-measurement-infrastructure-wave5-observability-resources --phase decompose`

Gate: 任务文档无占位符且依赖图可解析。

- [x] 已回填：任务文档字段、依赖图、验收清单和状态表。

## TP-02.01 ObservabilitySignal schema

Verify: `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py -k 'observability or resource'`

Gate: 必填字段、signalType、status、privacyBoundary 和 externalConnectivity 有测试断言。

- [x] 已完成：新增 ObservabilitySignal schema，并由 protocol tests 覆盖。

## TP-02.02 observability registry

Verify: `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py -k observability`

Gate: registry 覆盖 available 与 planned signals。

- [x] 已完成：新增 observability registry，覆盖 available 与 planned signals。

## TP-02.03 resource schema

Verify: `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py -k resource`

Gate: resource schema 包含 observabilitySignalResourceFields。

- [x] 已完成：resource schema 已补 ObservabilitySignal 字段。

## TP-03.01 observability API

Verify: `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py -k observability`

Gate: canonical 与 alias 返回一致，detail 可按 id 查询。

- [x] 已完成：新增 `/observability` 和 `/api/v1/observability` list/detail API。

## TP-03.02 metadata and OpenAPI

Verify: `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py -k 'metadata or openapi or observability'`

Gate: metadata developer links 和 OpenAPI paths 包含 observability。

- [x] 已完成：metadata 和 OpenAPI 测试覆盖 observability links/paths。

## TP-04.01 regression tests

Verify: `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py tests/regression/test_api_contracts.py -k 'observability or resource or metadata or openapi'`

Gate: focused tests 全部通过。

- [x] 已通过：focused contract/API 9 passed。

## TP-04.02 docs

Verify: `rg -n "ObservabilitySignal|/observability|trace/metric/log|观测" docs contracts governance/tasks/0018-measurement-infrastructure-wave5-observability-resources`

Gate: 人类文档与 API/契约一致。

- [x] 已完成：API 文档、100% 路线图、contracts AGENTS 已同步。

## TP-05.01 local gates

Verify: `bash scripts/local-ci.sh --profile quick && git diff --check`

Gate: quick CI 和 diff check 通过。

- [x] 已通过：quick CI 70 passed；ruff/mypy/diff check 通过。

## TP-05.02 task closeout

Verify: `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0018-measurement-infrastructure-wave5-observability-resources --phase closeout`

Gate: 0018 closeout 和全任务树校验通过。

- [x] 已完成：closeout 状态和验证证据已回填。
