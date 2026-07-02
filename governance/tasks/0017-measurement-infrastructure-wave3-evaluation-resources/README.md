# Task Overview
- Task ID: `0017`
- Slug: `measurement-infrastructure-wave3-evaluation-resources`
- Objective: `把已有 golden、benchmark 与评测入口资源化为 Dataset / EvaluationRun 发现层，提供 schema、registry、API 入口、文档和回归测试。`
- Status: `In Progress`

## In Scope
- 新增 Dataset / EvaluationRun 资源契约，覆盖现有 golden、benchmark、local-ci 和 MingLi-Bench 离线 runner。
- 建立 `contracts/fate/evaluations/` 注册表和 schema，不改变现有算法结果。
- 暴露 `/evaluations` 与 `/evaluations/{evaluation_id}` 发现 API，并在 `/metadata` 中挂载入口。
- 更新 API 文档、100% 路线图、contracts 目录说明和回归测试。
- 完成任务文档 closeout、quick CI 和契约回归。

## Out of Scope
- 不运行外部模型、真实线上服务、真实 token 或 Bot live smoke。
- 不把 MingLi-Bench 标准答案、question_id 或 scoring result 注入生产计算路径。
- 不修改八字、紫微、黄历、梅花的计算逻辑或报告正文。
- 不实现评测 UI、长期评测数据库、外部 dashboard、Webhook 或 CI 远端实跑。
- 不提交、不推送。

## Task Package Tree
```text
ROOT
├── TP-01 评测资源边界
│   ├── TP-01.01 资产盘点与资源映射
│   └── TP-01.02 任务契约与文档字段
├── TP-02 资源契约
│   ├── TP-02.01 Dataset schema
│   ├── TP-02.02 EvaluationRun schema
│   └── TP-02.03 resource schema 扩展
├── TP-03 Evaluation registry
│   ├── TP-03.01 golden dataset entries
│   ├── TP-03.02 benchmark dataset entries
│   └── TP-03.03 evaluation run entries
├── TP-04 API 发现层
│   ├── TP-04.01 list/detail API
│   └── TP-04.02 metadata/OpenAPI 链接
├── TP-05 测试与文档
│   ├── TP-05.01 contract/API 回归测试
│   └── TP-05.02 文档与路线图
└── TP-06 验证与收口
    ├── TP-06.01 本地门禁
    └── TP-06.02 closeout
```

## Requirement Alignment
- 对齐 `测算基础设施100%实现计划.md` 的 IMP-01 和 IMP-08：Dataset 与 EvaluationRun 不能只停留在资源类型枚举，必须有 schema、registry、API 和测试。
- 对齐 `测算基础设施需求文档.md` 的 REQ-EVAL 与 REQ-DATA：golden、benchmark、典籍和评测入口必须可追溯、可复核、可区分生产/评测用途。
- 对齐基础设施同构调研：参考 Kubernetes resource、OpenTelemetry signals、SRE SLO、API 幂等和评测驱动质量闭环，FateCat 需要把评测资产做成稳定发现资源。
- 对齐隐私边界：所有数据集条目必须说明匿名/测试/评测用途，不得引入真实用户隐私样例。

## Task Package Overview
| ID | Name | Type | Priority | Depends On | Verify |
| --- | --- | --- | --- | --- | --- |
| TP-01.01 | 资产盘点与资源映射 | SPEC | P0 | none | `find domains/fate-analysis/data-products -maxdepth 4 -type f` |
| TP-01.02 | 任务契约与文档字段 | PLAN | P0 | TP-01.01 | `validate_task_docs.py --phase decompose` |
| TP-02.01 | Dataset schema | BUILD | P0 | TP-01.02 | `pytest tests/regression/test_capability_protocol.py -k 'dataset or evaluation'` |
| TP-02.02 | EvaluationRun schema | BUILD | P0 | TP-02.01 | `pytest tests/regression/test_capability_protocol.py -k 'evaluation'` |
| TP-02.03 | resource schema 扩展 | BUILD | P0 | TP-02.02 | `pytest tests/regression/test_capability_protocol.py -k 'resource'` |
| TP-03.01 | golden dataset entries | BUILD | P0 | TP-02.03 | `pytest tests/regression/test_capability_protocol.py -k 'evaluation or dataset'` |
| TP-03.02 | benchmark dataset entries | BUILD | P0 | TP-03.01 | `pytest tests/regression/test_capability_protocol.py -k 'evaluation or dataset'` |
| TP-03.03 | evaluation run entries | BUILD | P0 | TP-03.02 | `pytest tests/regression/test_capability_protocol.py -k 'evaluation'` |
| TP-04.01 | list/detail API | BUILD | P0 | TP-03.03 | `pytest tests/regression/test_api_contracts.py -k 'evaluation'` |
| TP-04.02 | metadata/OpenAPI 链接 | BUILD | P0 | TP-04.01 | `pytest tests/regression/test_api_contracts.py -k 'metadata or openapi or evaluation'` |
| TP-05.01 | contract/API 回归测试 | TEST | P0 | TP-04.02 | `pytest tests/regression/test_capability_protocol.py tests/regression/test_api_contracts.py -k 'evaluation or dataset or resource or metadata or openapi'` |
| TP-05.02 | 文档与路线图 | GOVERN | P1 | TP-05.01 | `rg -n "EvaluationRun|Dataset|/evaluations|评测资源" docs contracts governance/tasks/0017-measurement-infrastructure-wave3-evaluation-resources` |
| TP-06.01 | 本地门禁 | TEST | P0 | TP-05.02 | `bash scripts/local-ci.sh --profile quick` |
| TP-06.02 | closeout | SHIP | P0 | TP-06.01 | `validate_task_docs.py --phase closeout && validate_tasks_tree.py --phase auto` |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
