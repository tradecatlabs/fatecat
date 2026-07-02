# Task Overview
- Task ID: `0010`
- Slug: `measurement-infrastructure-wave1-resources`
- Objective: `执行测算基础设施 100% 实现计划 Wave 1 的首批切片：补资源 schema、capability 详情 API、标准错误码入口、API contract tests，并保持任务树和文档可验收。`
- Status: `Done`

## In Scope
- 新增 capability resource schema 与 error schema。
- 新增标准错误码字典。
- 新增 `/capabilities/{capability_id}` 和 `/errors` 发现入口。
- 更新 `/metadata` developer discovery。
- 更新 API 接入文档和 100% 实现计划状态。
- 增加协议/API 回归测试。
- 跑定向 pytest、ruff、mypy、quick CI、任务文档校验。

## Out of Scope
- 不实现 `Idempotency-Key` 与通用 job 状态机。
- 不实现 provider protocol 和 bazi/ziwei adapter。
- 不改变命理算法、报告内容或默认 Markdown 结构。
- 不执行真实生产域名、真实 token、Bot live smoke。

## Task Package Tree
```text
TP-01 resource-contracts
├── TP-01.01 add-resource-schema
└── TP-01.02 add-error-catalog
TP-02 developer-api
├── TP-02.01 add-capability-detail-endpoint
└── TP-02.02 add-errors-endpoint
TP-03 tests-and-docs
├── TP-03.01 add-contract-regression-tests
└── TP-03.02 update-developer-docs
TP-04 validation-and-closeout
├── TP-04.01 run-local-gates
└── TP-04.02 close-task-docs
```

## Requirement Alignment
- 对齐 `测算基础设施100%实现计划.md` Wave 1：资源模型、schema、API 发现、错误码。
- 对齐用户目标：以任务树为执行框架，逐项推进并自检。
- 本轮是首批可落地切片，不把 100% 全部主线伪装成已完成。

## Task Package Overview
| Node | Scope | Proof |
| --- | --- | --- |
| TP-01 | 资源和错误契约 | `resource.schema.json`、`error.schema.json`、`errors.json` |
| TP-02 | 开发者 API 发现 | `/capabilities/{id}`、`/errors` |
| TP-03 | 回归与文档 | `test_api_contracts.py`、`test_capability_protocol.py`、API 接入文档 |
| TP-04 | 验证与收口 | pytest、ruff、mypy、quick CI、task validators |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
