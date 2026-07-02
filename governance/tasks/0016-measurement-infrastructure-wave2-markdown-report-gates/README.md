# Task Overview
- Task ID: `0016`
- Slug: `measurement-infrastructure-wave2-markdown-report-gates`
- Objective: `把 Markdown 同步报告、异步报告任务和 Web 报告结果接入统一 policyGate 与 snapshotGate，补齐多端报告正文最小发布门禁。`
- Status: `In Progress`

## In Scope
- 扩展 `fate_core.capabilities.report_policy`，新增 Markdown 正文 policy gate 和 heading snapshot gate。
- 同步 `/api/v1/report/markdown` 返回 `policyGate` 与 `snapshotGate`。
- 标准异步 `/api/v1/report/jobs` 成功结果返回 `policyGate` 与 `snapshotGate`。
- Web 异步 `/api/v1/report/jobs/web` 成功结果返回 `policyGate` 与 `snapshotGate`。
- 更新 schema、API 文档、100% 路线图、任务文档和回归测试。

## Out of Scope
- 不修改八字/紫微算法结论。
- 不改变 Markdown 正文内容。
- 不实现 NLP 审核、人工审核后台、远程策略服务。
- 不做真实生产域名、token、Bot live smoke。
- 不提交、不推送。

## Task Package Tree
```text
ROOT
├── TP-01 契约与任务边界
│   ├── TP-01.01 定义 Markdown gate 范围
│   └── TP-01.02 更新 report schema 文档口径
├── TP-02 Helper 实现
│   ├── TP-02.01 Markdown policyGate
│   └── TP-02.02 Markdown snapshotGate
├── TP-03 多端接入
│   ├── TP-03.01 同步 Markdown API 接入
│   ├── TP-03.02 标准异步 job 接入
│   └── TP-03.03 Web 异步 job 接入
├── TP-04 测试与文档
│   ├── TP-04.01 回归测试
│   └── TP-04.02 文档与路线图
└── TP-05 验证与收口
    ├── TP-05.01 本地门禁
    └── TP-05.02 closeout
```

## Requirement Alignment
- 对齐 0015 剩余差距：0015 只扫描 capability Report envelope 摘要，本任务扩展到用户可见 Markdown 正文。
- 对齐基础设施目标：报告正文必须有机器可读 policy 与结构快照，不能只靠人工看测试。
- 对齐多端一致性：同步 API、异步 API、Web 任务都必须返回同源 gate 结果。

## Task Package Overview
| ID | Name | Type | Priority | Depends On | Verify |
| --- | --- | --- | --- | --- | --- |
| TP-01.01 | 定义 Markdown gate 范围 | SPEC | P0 | none | `rg -n "markdown.*policyGate|snapshotGate" governance/tasks/0016-measurement-infrastructure-wave2-markdown-report-gates` |
| TP-01.02 | 更新 schema 口径 | PLAN | P0 | TP-01.01 | `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py -k 'policy or snapshot or report'` |
| TP-02.01 | Markdown policyGate helper | BUILD | P0 | TP-01.02 | `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py -k 'policy'` |
| TP-02.02 | Markdown snapshotGate helper | BUILD | P0 | TP-02.01 | `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py -k 'snapshot'` |
| TP-03.01 | 同步 Markdown API 接入 | BUILD | P0 | TP-02.02 | `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py -k 'markdown and gate'` |
| TP-03.02 | 标准异步 job 接入 | BUILD | P0 | TP-03.01 | `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py -k 'job and gate'` |
| TP-03.03 | Web 异步 job 接入 | BUILD | P0 | TP-03.02 | `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py -k 'web and gate'` |
| TP-04.01 | 回归测试 | TEST | P0 | TP-03.03 | `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py tests/regression/test_capability_protocol.py -k 'policy or snapshot or report or markdown or job'` |
| TP-04.02 | 文档与路线图 | GOVERN | P1 | TP-04.01 | `rg -n "policyGate|snapshotGate|Markdown 正文" docs/reference-materials contracts/fate/capabilities governance/tasks/0016-measurement-infrastructure-wave2-markdown-report-gates` |
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
