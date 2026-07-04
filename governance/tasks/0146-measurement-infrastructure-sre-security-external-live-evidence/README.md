# Task Overview
- Task ID: `0146`
- Slug: `measurement-infrastructure-sre-security-external-live-evidence`
- Objective: `执行 0143 后续 0146：基于当前 main HEAD 和 /tmp/fatecat-local-ci-0146-aea19ff 的 SRE/security artifacts，推进 SRE/security external live evidence；本地收口 OTel collector/backend/SLO/alert、OIDC/IdP、SIEM/immutable audit、external secret provider/Vault/KMS、retention cleanup 的 readiness 与阻断清单；真实完成必须由 operator 提供外部平台 proof-ref/live proof，不得伪造公网 live、不得保存 token/secret/DSN/raw URL/生产日志/trace payload。`
- Status: `Blocked`

## In Scope
- 基于 current HEAD `aea19ff4b060d30306cf65e008c3ba170f4f1df7` 重新执行 quick local CI，刷新 SRE/security 证据。
- 记录 observability SLO、trace SLO、OTel collector、OTel backend staged gate 的本地 readiness。
- 记录 production security、security externalization、external secret provider、retention production cleanup staged gate 的本地 readiness。
- 标出 6 个相关 external validation work items：`observability.otel_slo_live`、`security.external_secret_provider`、`security.externalization_live`、`security.identity_oidc`、`security.retention_cleanup_live`、`security.siem_audit`。
- 保持 100% infrastructure non-claim：本地 dry-run/staged gates 不能替代真实外部平台 proof。

## Out of Scope
- 不连接真实 OTel collector/backend、Prometheus/Grafana/Datadog/New Relic/Honeycomb 等外部平台。
- 不连接真实 OIDC/IdP、SIEM、不可变审计存储、Vault/KMS/secret manager。
- 不执行生产 retention cleanup 删除动作。
- 不保存 token、secret、DSN、raw URL、生产日志、trace payload、报告正文、真实用户输入或生产删除证明。
- 不关闭 0144/0145/0147/0148/0149 的外部 proof/live work items。
- 不把 local-ci passed、dry-run contract ready、negative evidence rejected 写成 SRE/security live complete。

## Task Package Tree
```text
0146-measurement-infrastructure-sre-security-external-live-evidence
├── README.md
├── CONTEXT.md
├── PLAN.md
├── ACCEPTANCE.md
├── ACCEPTANCE_CHECKLIST.md
├── TODO.md
└── STATUS.md
```

## Requirement Alignment
| Requirement | Alignment |
| --- | --- |
| 0143 next leaf | 0146 对应 SRE/security external live evidence。 |
| SRE infrastructure | OTel collector/backend、trace/SLO、alert route、error budget 和 incident drill 需要外部平台 proof。 |
| Security infrastructure | OIDC/IdP、SIEM/immutable audit、Vault/KMS、retention cleanup 需要外部平台 proof。 |
| Current local evidence | quick local CI 对 current HEAD `aea19ff...` 通过，SRE/security 本地 gates 均 passed。 |
| Public live boundary | 所有相关 gate 的 live evidence status 仍为 `外部连通验证待执行` 或 ship gate `blocked`。 |
| 100% gate | certification `canClaim100Percent=false` 保持阻断。 |

## Task Package Overview
| TP | Name | Status | Evidence |
| --- | --- | --- | --- |
| TP-01 | Current HEAD SRE/security evidence refresh | Done | `/tmp/fatecat-local-ci-0146-aea19ff`, focused regression `389 passed` |
| TP-02 | Observability/OTel/SLO live proof | Blocked | local SLO/OTel gates passed; external backend/SLO proof missing |
| TP-03 | Identity/SIEM/security externalization proof | Blocked | production security and externalization gates passed; OIDC/SIEM proof missing |
| TP-04 | Secret provider and retention cleanup proof | Blocked | external secret/retention staged gates passed; Vault/KMS/cleanup proof missing |
| TP-05 | SRE/security proof bundle and certification refresh | Blocked | 6 related work items pending, certification blocked |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
