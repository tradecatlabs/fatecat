# Task Overview

0128 执行 `MI-100.G.03 external closure evidence summary`：在 0119 work queue、0120 proof-ref gate、0121 category runbooks、0123 live proof gate、0127 operator packet 和 0122 trend dashboard 之后，新增外部验证关闭证据摘要，把 22 类 external validation 的 domain/category/owner/work item 关闭状态、operator step、required credential 名称、proof-ref/live 状态和 blocking items 汇总成单一审计索引。

该任务不执行真实 production API、HF Space、Telegram Bot、OIDC、SIEM、Vault/KMS、OTel、developer portal、SDK 发布或第三方审计请求，不读取或保存真实 URL、token、secret、DSN、webhook secret、chat id、生产日志、用户输入或报告正文。它只生成审计可读的关闭证据摘要。

## In Scope

- 新增 external validation closure evidence summary contract。
- 新增 Python generator 与 shell wrapper。
- 消费 work queue、proof-ref gate、category runbooks、operator packet、live proof gate 和 closure trend dashboard。
- 接入 `scripts/local-ci.sh --profile quick`，在 closure trend dashboard 后生成 summary artifact。
- 将 operator packet 与 closure evidence summary 纳入 certification audit domain。
- 增加 regression tests、AGENTS、roadmap 和任务索引。

## Out of Scope

- 不执行真实外部 live 请求。
- 不创建 proof-ref 或 live proof。
- 不上传或保存 operator 外部 artifact 原文。
- 不关闭 production live、第三方审计或 certification 阻断。
- 不声明 FateCat 已达到 100% 测算基础设施。

## Task Package Tree

```text
TP-01 scope and evidence chain confirmation
TP-02 closure evidence summary contract/script/wrapper
TP-03 local-ci and certification wiring
TP-04 AGENTS/roadmap/task index sync
TP-05 validation gates
TP-06 delivery and remote CI observation
```

## Requirement Alignment

| Requirement | Implementation |
| --- | --- |
| 审计人员不能手工拼 6 个 JSON | `external-validation-closure-evidence-summary.py` 输出单一 closure evidence summary |
| 无真实凭证时不能伪造通过 | `closureGate.status` 保持 `blocked`，只列出 pending/blocking items |
| 证据必须绑定现有链路 | source 绑定 work queue、proof-ref gate、category runbooks、operator packet、live proof gate、trend dashboard 的 sha256 |
| 输出不得泄露 URL/token/DSN | 输出只含凭证名称、状态、计数、owner/category/workItemId；测试覆盖 raw URL 拒绝 |
| certification 必须纳入新证据 | audit domain 增加 operator packet 与 closure evidence summary 必备文件 |

## Task Package Overview

本任务把外部验证关闭状态从“散落在多个 gate 产物”收束成一个可交接、可复核、可重复生成的审计索引。它不是 live smoke，也不是 evidence accepted 结论；它是第三方审计和后续 operator 执行的状态地图。

## Reading Order

1. `CONTEXT.md`
2. `PLAN.md`
3. `ACCEPTANCE.md`
4. `TODO.md`
5. `STATUS.md`
6. `ACCEPTANCE_CHECKLIST.md`
