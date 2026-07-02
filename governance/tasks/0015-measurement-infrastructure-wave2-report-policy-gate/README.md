# Task Overview
- Task ID: `0015`
- Slug: `measurement-infrastructure-wave2-report-policy-gate`
- Objective: `实现 Report policyGate 与 forbidden claims scanner，把 capability 报告交付结果纳入最小风险断语门禁。`
- Status: `In Progress`

## In Scope
- 在 `fate_core.capabilities` 增加通用 Report policy gate helper，扫描生成报告摘要中的禁止性断语。
- 在 capability API 的 `report` envelope 中加入 `policyGate`，并明确扫描范围、排除字段和匹配结果。
- 更新 `report.schema.json`、测试、API 文档和 100% 路线图。
- 运行 capability/report/API 相关回归、quick CI、governance/task validators 和 diff check。

## Out of Scope
- 不修改八字、紫微、黄历、梅花等计算核心。
- 不重写 Markdown 报告生成器。
- 不做完整 report snapshot gate。
- 不做真实生产域名、Bot live smoke 或外部连通验证。
- 不提交、不推送、不清理其他未提交任务切片。

## Task Package Tree
```text
ROOT
├── TP-01 契约与边界
│   ├── TP-01.01 定义 report policy gate scope
│   └── TP-01.02 更新 schema 契约
├── TP-02 实现
│   ├── TP-02.01 增加 forbidden claims scanner
│   └── TP-02.02 接入 capability report envelope
├── TP-03 回归与文档
│   ├── TP-03.01 增加 scanner 与 API 回归测试
│   └── TP-03.02 更新文档和路线图
└── TP-04 验证与收口
    ├── TP-04.01 运行本地门禁
    └── TP-04.02 收口任务文档
```

## Requirement Alignment
- 对齐用户目标：FateCat 要成为测算基础设施，不只是命理工具合集。
- 对齐 0014 剩余项：`report.schema.json` 明确把 forbidden claims scanner 标记为后续门禁，本任务将其落地。
- 对齐风险边界：命理/测算输出不得出现确定未来、医疗法律金融替代、恐吓式断语等高风险表达。
- 对齐工程原则：先做最小可执行 gate，不把所有策略治理一次性扩成重型合规模块。

## Task Package Overview
| ID | Name | Type | Priority | Depends On | Verify |
| --- | --- | --- | --- | --- | --- |
| TP-01.01 | 定义 policy scope | SPEC | P0 | none | `rg -n "policyGate|forbidden" contracts/fate/capabilities docs/reference-materials governance/tasks/0015-measurement-infrastructure-wave2-report-policy-gate` |
| TP-01.02 | 更新 report schema | PLAN/BUILD | P0 | TP-01.01 | `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py -k 'report or policy or capability'` |
| TP-02.01 | 增加 scanner helper | BUILD | P0 | TP-01.02 | `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py -k 'policy'` |
| TP-02.02 | 接入 report envelope | BUILD | P0 | TP-02.01 | `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py -k 'capability and report'` |
| TP-03.01 | 增加回归测试 | TEST | P0 | TP-02.02 | `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py tests/regression/test_capability_protocol.py -k 'policy or report or capability or metadata or openapi'` |
| TP-03.02 | 更新文档路线图 | GOVERN | P1 | TP-03.01 | `rg -n "policyGate|forbidden claims|禁止性断语" docs/reference-materials contracts/fate/capabilities governance/tasks/0015-measurement-infrastructure-wave2-report-policy-gate` |
| TP-04.01 | 本地门禁 | TEST | P0 | TP-03.02 | `bash scripts/local-ci.sh --profile quick && python3 governance/tools/validate_governance_package.py --project-root . --strict && git diff --check` |
| TP-04.02 | closeout | SHIP | P0 | TP-04.01 | `validate_task_docs.py --phase closeout && validate_tasks_tree.py --phase auto` |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
