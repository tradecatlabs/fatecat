# Task Overview
- Task ID: `0018`
- Slug: `measurement-infrastructure-wave5-observability-resources`
- Objective: `把现有 health、ready、metrics、requestId 和结构化日志能力资源化为 Observability 发现层，提供 schema、registry、API 入口、文档和回归测试。`
- Status: `In Progress`

## In Scope
- 新增 Observability 资源契约，覆盖现有 health、ready、metrics、requestId、结构化日志和后续 trace/span 口径。
- 建立 `contracts/fate/observability/` 注册表和 schema。
- 暴露 `/observability` 与 `/observability/{signal_id}` 发现 API，并在 `/metadata` 中挂载入口。
- 更新 API 文档、100% 路线图、contracts 目录说明和回归测试。
- 完成任务文档 closeout、quick CI 和契约回归。

## Out of Scope
- 不引入 OpenTelemetry SDK、Prometheus client、外部 collector、dashboard 或告警系统。
- 不修改已有 `/metrics` 文本格式的指标值语义。
- 不做真实生产 p95/p99、SLO、alert rule 或外部监控连通验证。
- 不提交、不推送。

## Task Package Tree
```text
ROOT
├── TP-01 Observability 边界
│   ├── TP-01.01 现有观测能力盘点
│   └── TP-01.02 任务契约与文档字段
├── TP-02 资源契约
│   ├── TP-02.01 ObservabilitySignal schema
│   ├── TP-02.02 observability registry
│   └── TP-02.03 resource schema 扩展
├── TP-03 API 发现层
│   ├── TP-03.01 list/detail API
│   └── TP-03.02 metadata/OpenAPI 链接
├── TP-04 测试与文档
│   ├── TP-04.01 contract/API 回归测试
│   └── TP-04.02 文档与路线图
└── TP-05 验证与收口
    ├── TP-05.01 本地门禁
    └── TP-05.02 closeout
```

## Requirement Alignment
- 对齐 `测算基础设施100%实现计划.md` 的 IMP-09：trace、metric、log 三类观测必须可发现、可审计、可验证。
- 对齐成熟基础设施同构：OpenTelemetry 把观测拆成 traces、metrics、logs；SRE 把可观测性连接到 SLO 和排障。本任务先把 FateCat 已有 signals 资源化。
- 对齐当前代码事实：`main.py` 已有 `X-Request-ID`、结构化 JSON 日志、Prometheus 文本 `/metrics`、`/health`、`/ready`、队列和并发指标，但缺 schema/registry/API 发现层。
- 对齐克制边界：本轮只登记和发现，不引入外部 collector 或存储。

## Task Package Overview
| ID | Name | Type | Priority | Depends On | Verify |
| --- | --- | --- | --- | --- | --- |
| TP-01.01 | 现有观测能力盘点 | SPEC | P0 | none | `rg -n "X-Request-ID|/metrics|_log_structured|/ready|/health" domains/experience-delivery/services/fatecat-delivery/src/main.py tests/regression/test_api_contracts.py` |
| TP-01.02 | 任务契约与文档字段 | PLAN | P0 | TP-01.01 | `validate_task_docs.py --phase decompose` |
| TP-02.01 | ObservabilitySignal schema | BUILD | P0 | TP-01.02 | `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py -k 'observability or resource'` |
| TP-02.02 | observability registry | BUILD | P0 | TP-02.01 | `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py -k observability` |
| TP-02.03 | resource schema 扩展 | BUILD | P0 | TP-02.02 | `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py -k resource` |
| TP-03.01 | list/detail API | BUILD | P0 | TP-02.03 | `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py -k observability` |
| TP-03.02 | metadata/OpenAPI 链接 | BUILD | P0 | TP-03.01 | `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py -k 'metadata or openapi or observability'` |
| TP-04.01 | contract/API 回归测试 | TEST | P0 | TP-03.02 | `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py tests/regression/test_api_contracts.py -k 'observability or resource or metadata or openapi'` |
| TP-04.02 | 文档与路线图 | GOVERN | P1 | TP-04.01 | `rg -n "ObservabilitySignal|/observability|trace/metric/log|观测" docs contracts governance/tasks/0018-measurement-infrastructure-wave5-observability-resources` |
| TP-05.01 | 本地门禁 | TEST | P0 | TP-04.02 | `bash scripts/local-ci.sh --profile quick` |
| TP-05.02 | closeout | SHIP | P0 | TP-05.01 | `validate_task_docs.py --phase closeout && validate_tasks_tree.py --phase auto` |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
