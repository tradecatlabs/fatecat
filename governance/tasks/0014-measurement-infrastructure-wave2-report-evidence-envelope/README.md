# Task Overview
- Task ID: `0014`
- Slug: `measurement-infrastructure-wave2-report-evidence-envelope`
- Objective: `执行测算基础设施 100% 实现计划 IMP-05 的第一个切片：新增 Report schema 和 evidence reference 契约，并让 capability 执行响应携带统一 Report resource envelope，包含 profile、format、sections、evidenceRefs、links 与风险边界；不重写 Markdown 生成器或具体算法。`
- Status: `Done`

## In Scope
- 新增 `report.schema.json`，声明 Report resource、section、format、evidenceRefs 和风险边界。
- 增强 `evidence.schema.json` 与 `output.schema.json`，把 evidence references 和 report envelope 纳入输出契约。
- capability 执行 API 响应增加统一 `report` envelope。
- `/reports` 和 schema refs 暴露 report schema。
- 更新 API 回归测试、API 接入文档、100% 实现计划和 0014 任务文档。

## Out of Scope
- 不重写 Markdown 生成器。
- 不改变默认 Markdown 结构。
- 不改八字/紫微/黄历/梅花算法结果。
- 不实现完整 snapshot gate 或 forbidden claims scanner。
- 不新增外部存储或 report persistence。

## Task Package Tree
```text
TP-01 report-evidence-contract
├── TP-01.01 add-report-schema
└── TP-01.02 update-output-and-evidence-schema
TP-02 capability-report-envelope
├── TP-02.01 build-report-resource-envelope
└── TP-02.02 expose-report-schema-links
TP-03 tests-and-docs
├── TP-03.01 add-report-envelope-regression
└── TP-03.02 update-api-docs-and-roadmap
TP-04 validation-closeout
├── TP-04.01 run-local-gates
└── TP-04.02 close-task-docs
```

## Requirement Alignment
- 对齐 IMP-05：报告与 Evidence 层。
- 延续 0010-0013：Capability、Provider、Job 已资源化，本轮把执行结果中的 Report 资源摘要补齐。
- 本轮只做 API envelope 和 schema，不改报告内容生成。

## Task Package Overview
| Node | Scope | Proof |
| --- | --- | --- |
| TP-01 | Report/evidence schema | `contracts/fate/capabilities/schemas/report.schema.json` |
| TP-02 | Capability response envelope | `main.py` |
| TP-03 | 回归和文档 | `test_api_contracts.py`、`test_capability_protocol.py`、API 文档、100% 计划 |
| TP-04 | 验证和收口 | pytest、ruff、mypy、quick CI、task validators |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
