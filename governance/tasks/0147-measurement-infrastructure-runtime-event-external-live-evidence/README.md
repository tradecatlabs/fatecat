# Task Overview
- Task ID: `0147`
- Slug: `measurement-infrastructure-runtime-event-external-live-evidence`
- Objective: `执行 0143 后续 0147：基于当前 main HEAD 和 /tmp/fatecat-local-ci-0147-c539c29 的 runtime/event artifacts，推进 runtime/event external live evidence；本地收口 Postgres job store/worker lease/job worker/external worker restart/heartbeat polling/public webhook live、multi-replica runtime、runtime proof pack、event contract/replay/DLQ 的 readiness 与阻断清单；真实完成必须由 operator 提供外部 Postgres、public webhook、多副本运行和事件平台 proof-ref/live proof，不得伪造生产 live、不得保存 DSN/token/secret/raw URL/生产日志/用户输入/报告正文。`
- Status: `Blocked`

## In Scope
- 基于 current HEAD `c539c292c08fee1c8d9767ee0be05bbfbfc77a01` 重新执行 quick local CI，刷新 runtime/event 证据。
- 记录 runtime backend、Postgres dry-run、Postgres live smoke preflight、multi-replica runtime、runtime proof pack 的本地 readiness。
- 记录 event contract、CloudEvents/AsyncAPI、event replay、dead-letter baseline、webhook outbox/redelivery/lease smoke 的本地 readiness。
- 标出 4 个相关 external validation work items：`runtime.postgres_live`、`runtime.public_webhook_live`、`runtime.multi_replica_live`、`event_platform.live`。
- 保持 100% infrastructure non-claim：本地 dry-run/contract/smoke 不能替代真实外部 Postgres、公网 webhook、多副本 soak 或事件平台 proof。

## Out of Scope
- 不连接真实 Postgres、Temporal、Redis、外部 broker 或公网 webhook endpoint。
- 不执行真实多副本 24h soak、不证明 exactly-once。
- 不上传 proof-ref bundle/live-proof bundle。
- 不保存 DSN、token、secret、raw URL、生产日志、trace payload、用户输入、报告正文或 webhook secret。
- 不关闭 0144/0145/0146/0148/0149 的外部 proof/live work items。
- 不把 local-ci passed、contract baseline、allow-missing blocked smoke 写成 runtime/event live complete。

## Task Package Tree
```text
0147-measurement-infrastructure-runtime-event-external-live-evidence
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
| 0143 next leaf | 0147 对应 runtime/event external live evidence。 |
| Runtime infrastructure | Postgres live smoke、worker lease、restart、heartbeat/polling、公网 webhook 和多副本 runtime proof 需要外部 proof。 |
| Event infrastructure | CloudEvents/AsyncAPI、event replay、DLQ 本地 contract 已有；真实 event platform/live webhook 仍需 proof。 |
| Current local evidence | quick local CI 对 current HEAD `c539c29...` 通过，runtime/event 本地 gates 均 passed 或 blocked-as-expected。 |
| Public live boundary | Postgres live 系列、multi-replica、公网 webhook 和 event platform 仍为 external pending/blocked。 |
| 100% gate | certification `canClaim100Percent=false` 保持阻断。 |

## Task Package Overview
| TP | Name | Status | Evidence |
| --- | --- | --- | --- |
| TP-01 | Current HEAD runtime/event evidence refresh | Done | `/tmp/fatecat-local-ci-0147-c539c29`, focused regression `389 passed` |
| TP-02 | Postgres runtime live proof | Blocked | dry-run passed; live smoke preflights blocked |
| TP-03 | Multi-replica and public webhook live proof | Blocked | multi-replica gate passed locally; live evidence pending |
| TP-04 | Event platform replay/DLQ live proof | Blocked | event contract gate passed; external event platform proof missing |
| TP-05 | Runtime/event proof bundle and certification refresh | Blocked | 4 related work items pending, certification blocked |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
