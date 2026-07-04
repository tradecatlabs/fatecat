# Task Overview

0123 执行 `MI-100.A.05 external validation live proof gate`：在 proof-ref schema、category runbook 和 closure trend dashboard 之后，新增一层本地可验证的 live proof gate，用来验收 operator 后续提供的脱敏真实 live 执行摘要是否能绑定到 work item、proof-ref、category runbook、source occurrence 和当前 commit。

该任务不执行真实生产请求，也不上传真实 token、secret、DSN、URL、生产日志或用户报告正文。无 live evidence 时必须保持 `external_connectivity_pending` / `blocked`；有脱敏 live evidence bundle 时也只证明结构、绑定和反伪造边界通过，仍需第三方审计和 certification 继续阻断。

## In Scope

- 新增 external validation live proof gate contract 与 live evidence bundle schema。
- 新增 live proof gate Python generator 与 shell wrapper。
- 校验 work queue、proof-ref gate、category runbooks 与可选 live evidence bundle 的 hash/current commit/source occurrence 绑定。
- 接入 local-ci quick artifact。
- 接入 measurement infrastructure certification 的 audit domain。
- 让 closure trend dashboard 可选消费 live proof gate，避免 live proof 已接受后继续误报 category live pending。
- 增加 regression tests、AGENTS、roadmap 和任务索引。

## Out of Scope

- 不执行真实 API/HF/Bot/Postgres/OIDC/SIEM/OTel/Vault/KMS 请求。
- 不验证 hidden artifact 的真实性。
- 不发送真实通知、不连接 issue tracker。
- 不保存真实 URL、token、secret、DSN、生产日志 payload、用户输入或报告正文。
- 不替代第三方审计，不声明 FateCat 已达到 100% 测算基础设施。

## Task Package Tree

```text
TP-01 scope and upstream artifact confirmation
TP-02 live proof contract/schema/script/wrapper
TP-03 local-ci/certification/trend/docs wiring
TP-04 validation gates
TP-05 delivery and remote CI observation
```

## Requirement Alignment

| Requirement | Implementation |
| --- | --- |
| proof-ref 结构通过不能等于 live 通过 | `external-validation-live-proof-gate.py` 只接受已 schema-accepted proof-ref 对应的 live proof |
| live proof 必须绑定 runbook/source/current commit | `sourceBinding` 校验 work queue/proof-ref/runbook sha、commit 和 occurrence ids |
| 无外部凭证时继续推进但不伪造 | 默认无 `--live-evidence-json` 输出 `external_connectivity_pending` |
| summary 不泄露敏感值 | raw URL、token/secret/DSN/private key、placeholder/fake/dry-run/localhost 被拒绝 |
| certification 能看到 live proof 缺口 | audit domain required evidence 加入 `external-validation-live-proof-gate.json` |

## Task Package Overview

本任务补齐 `proof-ref schema accepted -> category live evidence accepted` 的证据层级。它让 production API/HF/Bot/webhook/OIDC/SIEM/OTel/Vault/KMS 后续真实 live smoke 的脱敏摘要可以进入统一 closure/certification 链路，同时避免 proof-ref 结构验收被误读为 live 验收。

## Reading Order

1. `PLAN.md`
2. `CONTEXT.md`
3. `ACCEPTANCE.md`
4. `TODO.md`
5. `STATUS.md`
6. `ACCEPTANCE_CHECKLIST.md`
