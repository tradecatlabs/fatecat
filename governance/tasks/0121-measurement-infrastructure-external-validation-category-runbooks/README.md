# Task Overview

0121 执行 `MI-100.A.03 external validation runbook per category`：把 0120 的 proof-ref evidence upload contract 继续提升为每个 external validation category 的 operator runbook。

该任务只做本地控制面。runbook ready 不等于 production live passed；真实 production API、HF Space、Telegram Bot、Postgres、OIDC、SIEM、OTel、Vault/KMS、developer portal 和第三方审计仍必须由后续 category live gate 提供外部证据。

## In Scope

- 新增 category runbooks contract。
- 新增 category runbooks gate Python generator 与 shell wrapper。
- 覆盖当前 22 个 external validation category。
- 接入 local-ci quick artifact。
- 接入 measurement infrastructure certification 的 audit domain。
- 增加 regression tests、AGENTS、roadmap 和任务索引。

## Out of Scope

- 不执行真实外部 live validation。
- 不发送真实通知、不连接外部 issue tracker。
- 不保存真实 token、secret、DSN、raw URL、生产日志 payload 或用户报告正文。
- 不声明 FateCat 已达到 100% 测算基础设施。

## Task Package Tree

```text
TP-01 scope and category confirmation
TP-02 contract/script/certification wiring
TP-03 regression/local-ci wiring
TP-04 validation gates
TP-05 delivery and remote CI observation
```

## Requirement Alignment

| Requirement | Implementation |
| --- | --- |
| 每类验证有 runbook | `external-validation-category-runbooks.py` 覆盖 22 个 category |
| 指明执行资料 | runbook 输出 requiredCredentials、operatorCommands、proofRefArtifactPattern |
| 指明失败处理 | runbook 输出 failureRollback |
| 指明关闭条件 | runbook 输出 closureCondition |
| 不伪造 live | `shipGate.status=blocked` 保持不变 |

## Task Package Overview

本任务补齐 “work queue -> proof-ref -> category runbook -> category live gate” 中的 runbook 层。它让后续 operator 能按 category 采集真实外部 evidence，同时给审计人员一个可复核的操作目录。

## Reading Order

1. `PLAN.md`
2. `CONTEXT.md`
3. `ACCEPTANCE.md`
4. `TODO.md`
5. `STATUS.md`
6. `ACCEPTANCE_CHECKLIST.md`
