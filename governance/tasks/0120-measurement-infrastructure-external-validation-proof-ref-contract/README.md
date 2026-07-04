# Task Overview

0120 执行 `MI-100.A.02 proof-ref schema and evidence upload contract`：把 0119 的 external validation owner/category work queue 继续提升为可上传、可校验、可审计的脱敏 proof-ref 证据合同。

该任务只做本地控制面。proof-ref schema accepted 不等于生产 live passed；真实 production API、HF Space、Telegram Bot、Postgres、OIDC、SIEM、OTel、Vault/KMS、developer portal 和第三方审计仍必须由后续 category live gate 提供外部证据。

## In Scope

- 新增 proof-ref contract 与 JSON schema。
- 新增 proof-ref gate Python verifier 与 shell wrapper。
- 接入 local-ci quick artifact。
- 接入 measurement infrastructure certification 的 audit domain。
- 增加 regression tests、AGENTS、roadmap 和任务索引。

## Out of Scope

- 不创建 evidence upload API、dashboard、数据库、通知系统或 issue tracker integration。
- 不连接真实外部服务。
- 不保存真实 token、secret、DSN、raw URL、生产日志 payload 或用户报告正文。
- 不声明 FateCat 已达到 100% 测算基础设施。

## Task Package Tree

```text
TP-01 scope confirmation
TP-02 contract/schema/script/certification wiring
TP-03 regression/local-ci wiring
TP-04 validation gates
TP-05 delivery and remote CI observation
```

## Requirement Alignment

| Requirement | Implementation |
| --- | --- |
| 证据可上传 | `external-validation-proof-ref.schema.json` 定义脱敏 bundle |
| 证据可复核 | `external-validation-proof-ref-gate.py` 校验 commit、work queue hash、occurrenceIds 和 artifact hash |
| 隐私不泄露 | raw URL、token/secret/DSN/private-key marker 被拒绝 |
| 不伪造 live | `shipGate.status=blocked` 保持不变 |
| 进入 certification | audit domain 现在同时要求 current audit bundle 与 proof-ref gate |

## Task Package Overview

本任务补齐 “work queue -> proof-ref -> category live gate” 中间层。它让未来 operator 可以提交脱敏证据句柄，同时给审计人员一个可复核的结构化输入。

## Reading Order

1. `PLAN.md`
2. `CONTEXT.md`
3. `ACCEPTANCE.md`
4. `TODO.md`
5. `STATUS.md`
6. `ACCEPTANCE_CHECKLIST.md`
