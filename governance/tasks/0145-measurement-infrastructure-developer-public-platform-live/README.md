# Task Overview
- Task ID: `0145`
- Slug: `measurement-infrastructure-developer-public-platform-live`
- Objective: `执行 0143/0144 后续 0145：基于当前 main HEAD 和 /tmp/fatecat-local-ci-0145-81dd574 的 developer docs/platform/portal/sandbox artifacts，推进 developer public platform live；本地收口 public portal、SDK package、sandbox token issuer-revocation、API changelog 的 readiness 与阻断清单；真实完成必须由 operator 提供 public developer portal、发布 SDK/package、sandbox token issuer/revocation live evidence，不得伪造公网 live 或保存 token/secret/raw URL。`
- Status: `Blocked`

## In Scope
- 基于 current HEAD `81dd574101c842506d1765d544882b0953cff235` 重新执行 quick local CI，刷新 developer platform 证据。
- 记录 developer docs smoke、developer platform gate、developer portal gate、sandbox access gateway gate 的本地 readiness。
- 明确 public developer portal、SDK/package registry、sandbox token issuer/revocation 和 public changelog 仍是外部 live 阻断。
- 将 developer_platform.live work item 与 0143/0144 external proof/live 阻断链路绑定。
- 保持 100% infrastructure non-claim：本地通过只证明契约和示例 ready，不能证明公网开发者平台可用。

## Out of Scope
- 不发布 PyPI/npm/其他 package registry 包。
- 不启动真实公网 developer portal。
- 不创建、保存或展示真实 sandbox token、secret、raw URL、生产账号、真实用户输入或报告正文。
- 不执行真实 production API/HF/Bot/webhook/OIDC/SIEM/OTel/Vault/KMS live 操作。
- 不关闭 0144 的 22 个外部 proof/live work items。
- 不把 local-ci passed、contract ready、example ready 写成 developer public platform live complete。

## Task Package Tree
```text
0145-measurement-infrastructure-developer-public-platform-live
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
| 0143 next leaf | 0145 对应 developer public platform live。 |
| 0144 continuity | 0145 继承 external proof/live 非伪造口径，并专门拆出 developer_platform.live。 |
| Developer infrastructure | OpenAPI、SDK 示例、sandbox、token、changelog 必须让外部开发者不读源码即可接入。 |
| Current local evidence | quick local CI 对 current HEAD `81dd574...` 通过，developer 本地 gates 均 passed。 |
| Public live boundary | portal external status、SDK publish、live sandbox token service 仍为 false/not implemented。 |
| 100% gate | certification `canClaim100Percent=false` 保持阻断。 |

## Task Package Overview
| TP | Name | Status | Evidence |
| --- | --- | --- | --- |
| TP-01 | Current HEAD developer evidence refresh | Done | `/tmp/fatecat-local-ci-0145-81dd574`, focused regression `389 passed` |
| TP-02 | Public portal readiness | Blocked | `externalPortalLive=false`, portal external status `not_implemented` |
| TP-03 | SDK/package release readiness | Blocked | `sdkPackageCandidates=4`, `publishedSdkPackages=0`, package registry `not_published` |
| TP-04 | Sandbox token issuer/revocation readiness | Blocked | local gateway executable, live public token service `false` |
| TP-05 | API changelog and final public proof | Blocked | local changelog entries present, public live proof missing |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
