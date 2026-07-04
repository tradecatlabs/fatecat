# Task Overview

本任务执行 `MI-100.A.01 closure owner work queue`：把 0116/0117 已生成的 external validation closure plan 聚合为 owner/category 工作队列，补齐 `status`、`assignee`、`proofRef`、`lastCheckedAt`、`staleReason` 和 `closeConditionResult`，让后续外部 live 证据可以逐项推进。

## In Scope

- 新增 `contracts/fate/audit/external-validation-closure-work-queue.json`。
- 新增 `scripts/external-validation-closure-work-queue.py` 与 shell wrapper。
- 接入 `scripts/local-ci.sh` quick 证据产物与 summary artifact。
- 新增 regression tests，覆盖 contract、分组、脱敏、非法输入和文档接线。
- 更新目录级 `AGENTS.md` 与主路线图。

## Out of Scope

- 不连接真实 API、HF Space、Telegram Bot、Postgres、OIDC、SIEM、OTel、Vault/KMS、developer portal 或第三方审计系统。
- 不验证 `proofRef` 真实性。
- 不把 pending external validation、work queue 或 local-ci dry-run 写成 100% 完成。
- 不修改综合八字、紫微或业务 provider 算法。

## Task Package Tree

```text
TP-01 SPEC   复核 MI-100.A.01 边界与现有 closure plan
TP-02 BUILD  新增 closure work queue contract/script/local-ci wiring
TP-03 TEST   新增 regression tests 并跑针对性门禁
TP-04 DOCS   更新 AGENTS、roadmap、任务包和索引
TP-05 SHIP   运行 quick CI、提交、推送并观察远端 CI
```

## Requirement Alignment

- 用户要求：继续推进 100% 测算基础设施计划，优先关闭当前可本地落地的外部验证控制面缺口。
- 主路线图要求：`MI-100.A.01 closure owner work queue` 必须把 closure categories 变成可追踪队列。
- 不可伪造口径：生成队列只代表可分派，不代表外部 live 通过。

## Task Package Overview

本任务是外部 live 闭环之前的控制面切片。正确完成后，audit/current bundle 产生的 pending occurrence 能通过 closure gate 变成 closure plan，再通过 work queue gate 变成 owner/category work item。所有 work item 初始 `proofRef=""`，因此 ship/certification 仍保持 blocked。

## Reading Order

1. `docs/reference-materials/roadmap/测算基础设施100%实现计划.md`
2. `contracts/fate/audit/external-validation-closure.json`
3. `scripts/external-validation-closure-gate.py`
4. `contracts/fate/audit/external-validation-closure-work-queue.json`
5. `scripts/external-validation-closure-work-queue.py`
6. `tests/regression/test_external_validation_closure_work_queue.py`
