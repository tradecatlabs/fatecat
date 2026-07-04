# Task Overview
- Task ID: `0138`
- Slug: `measurement-infrastructure-external-proof-ref-live-proof-execution`
- Objective: `执行 0136/0137 后续 0138：基于已创建的 22 个 external validation tracker issue，逐项执行 category runbook，提交脱敏 proof-ref bundle 与 live proof bundle，使 external-validation-proof-ref-gate 和 external-validation-live-proof-gate 从 pending 进入 accepted；不得伪造生产 live、不得保存 token/secret/raw URL/用户输入。当前无真实外部凭证时，先完成 current-HEAD readiness matrix、issue/runbook/proof-ref 映射与外部阻断清单。`
- Status: `Blocked`

## In Scope
- 基于 current HEAD `a5bc4d23c57915608b1f4392c477f9d40cb81703` 复核 22 个 external validation work item。
- 复用 0137 已创建的 22 个 GitHub tracker issue ref。
- 将 work item、tracker issue、category runbook、operator step、proof-ref artifact pattern、required credential names 和 gate pending reason 建成脱敏矩阵。
- 记录 proof-ref gate 与 live proof gate 的真实当前状态。
- 明确后续必须由外部 operator 使用真实凭证执行的工作。

## Out of Scope
- 不伪造 proof-ref。
- 不伪造 live proof。
- 不执行没有真实凭证的 production API/HF/Bot/webhook/OIDC/SIEM/OTel/Vault/KMS/multi-replica live 操作。
- 不在仓库保存 token、secret、DSN、webhook secret、chat id、raw URL、生产日志、trace payload、报告正文或用户输入。
- 不关闭 measurement infrastructure certification 或 independent third-party audit。

## Task Package Tree
```text
0138-measurement-infrastructure-external-proof-ref-live-proof-execution/
├── README.md
├── CONTEXT.md
├── PLAN.md
├── ACCEPTANCE.md
├── ACCEPTANCE_CHECKLIST.md
├── TODO.md
├── STATUS.md
└── evidence/
    ├── EXTERNAL_PROOF_LIVE_BLOCKERS.json
    ├── EXTERNAL_PROOF_LIVE_READINESS_MATRIX.json
    └── ISSUE_RUNBOOK_PROOF_REF_MATRIX.md
```

## Requirement Alignment
- 对齐 0136/0137 后续 0138：从 tracker issue evidence accepted 推进到 proof-ref/live proof 执行。
- 对齐 0120/0123 gates：proof-ref 必须先被 schema 接受，live proof 才能被 live proof gate 接受。
- 对齐隐私要求：只保存脱敏 ref、hash、凭证名称和 pending reason。
- 对齐 100% 硬门槛：当前仍不能声明 100%，因为 proof-ref/live proof/certification/audit 未闭合。

## Task Package Overview
| TP | Name | Status | Evidence |
| --- | --- | --- | --- |
| TP-01 | Current external validation input chain | Done | `EXTERNAL_PROOF_LIVE_READINESS_MATRIX.json` source hashes |
| TP-02 | Issue/runbook/proof-ref readiness matrix | Done | 22 work items mapped to 22 tracker refs |
| TP-03 | Execute proof-ref runbooks | Blocked | Requires real external credentials and operator evidence |
| TP-04 | Execute live proof validation | Blocked | Requires accepted proof refs first |
| TP-05 | Re-run closure/certification/audit chain | Blocked | Requires TP-03 and TP-04 |
| TP-06 | Ship-readiness claim check | Blocked | Requires certification and third-party audit |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
