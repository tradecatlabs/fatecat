# Task Overview

0129 执行 `MI-100.G.04 third-party audit rehearsal`：在 0128 closure evidence summary 之后，新增第三方审计预演包，把 current audit bundle、audit dry-run、current release proof、measurement infrastructure certification 和 external validation closure evidence summary 聚合成审计人员可复核的 checklist、证据索引、阻断项和外部待验证项。

该任务不执行真实 production API、HF Space、Telegram Bot、Postgres、OIDC、SIEM、OTel、Vault/KMS、developer portal、SDK 发布、sandbox token 或第三方审计请求，不读取或保存真实 URL、token、secret、DSN、webhook secret、chat id、生产日志、用户输入或报告正文。它只生成本地审计预演包。

## In Scope

- 新增 third-party audit rehearsal contract。
- 新增 Python generator 与 shell wrapper。
- 消费 current audit bundle、audit dry-run、current release proof、certification 和 closure evidence summary。
- 输出 JSON/Markdown 预演包。
- 接入 `scripts/local-ci.sh --profile quick`，在 certification 后生成 rehearsal artifact。
- 增加 regression tests、AGENTS、roadmap 和任务索引。

## Out of Scope

- 不执行真实外部 live 请求。
- 不生成或上传 proof-ref/live proof。
- 不附加独立审计人员签名结果。
- 不关闭 production live、third-party audit 或 certification 阻断。
- 不声明 FateCat 已达到 100% 测算基础设施。

## Task Package Tree

```text
TP-01 scope and audit rehearsal evidence chain confirmation
TP-02 third-party audit rehearsal contract/script/wrapper
TP-03 local-ci artifact and regression wiring
TP-04 AGENTS/roadmap/task index sync
TP-05 validation gates
TP-06 delivery and remote CI observation
```

## Requirement Alignment

| Requirement | Implementation |
| --- | --- |
| 第三方审计前需要单一预演包 | `third-party-audit-rehearsal.py` 输出 JSON/Markdown |
| 不伪造第三方审计通过 | `rehearsalGate.status` 在外部证据或独立审计缺失时保持 `blocked` |
| 证据必须绑定当前审计链路 | 输入包含 current audit bundle、audit dry-run、release proof、certification、closure summary |
| 输出不得泄露 URL/token/DSN | 只输出路径、hash、状态、计数、owner/category/workItemId；测试覆盖 raw URL 拒绝 |
| local-ci 必须可复核 | quick profile 生成 rehearsal artifact 并写入 summary |

## Task Package Overview

本任务把“第三方审计 rehearsal”从口头流程变成机器可重复生成的交接件。它不是审计结论，而是审计前置材料：说明当前哪些证据已生成、哪些 gate 阻断、哪些外部 work item 需要真实 proof。

## Reading Order

1. `CONTEXT.md`
2. `PLAN.md`
3. `ACCEPTANCE.md`
4. `TODO.md`
5. `STATUS.md`
6. `ACCEPTANCE_CHECKLIST.md`
