# Task Overview
- Task ID: `0011`
- Slug: `measurement-infrastructure-wave1-jobs`
- Objective: `执行测算基础设施 100% 实现计划 Wave 1 的第二个切片：在现有报告任务队列上补 Idempotency-Key、cancelled 状态、取消 API、job resource links 和对应回归测试。`
- Status: `Done`

## In Scope
- 在现有单进程 report job manager 上增加 `Idempotency-Key` 去重。
- 增加 `cancelled` 状态和取消 API。
- 在 job payload 中暴露 `CalculationJob` resource links。
- 更新 metrics、resource schema、API 接入文档和 100% 计划状态。
- 增加 API/协议回归测试。

## Out of Scope
- 不引入 Redis/RQ/Celery。
- 不承诺跨进程、跨重启幂等。
- 不强杀 running 线程；取消 running job 后只丢弃结果并保持 `cancelled`。
- 不改变报告计算内容。

## Task Package Tree
```text
TP-01 job-manager-lifecycle
├── TP-01.01 add-idempotency-key
└── TP-01.02 add-cancelled-status
TP-02 job-api-resource
├── TP-02.01 expose-job-resource-links
└── TP-02.02 add-cancel-api
TP-03 tests-and-docs
├── TP-03.01 add-job-regression-tests
└── TP-03.02 update-docs-and-schema
TP-04 validation-and-closeout
├── TP-04.01 run-local-gates
└── TP-04.02 close-task-docs
```

## Requirement Alignment
- 对齐 100% 实现计划 IMP-04：Job 状态机与事件系统。
- 本轮只做 Wave 1 最小切片：幂等、cancelled、cancel API、links 和 tests。
- 保留现有有界内存队列边界，后续再升级为通用 job store。

## Task Package Overview
| Node | Scope | Proof |
| --- | --- | --- |
| TP-01 | job manager 状态机 | `report_jobs.py` |
| TP-02 | job API resource | `main.py` |
| TP-03 | 回归与文档 | `test_api_contracts.py`、API 接入文档、resource schema |
| TP-04 | 验证与收口 | pytest、ruff、mypy、quick CI、task validators |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
