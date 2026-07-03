# Task Overview
- Task ID: `0116`
- Slug: `measurement-infrastructure-external-validation-closure-gate`
- Objective: `把 current audit bundle 的 pending external validations occurrence 清单提升为可执行关闭计划门禁：为每个外部待验证项生成 owner、凭证依赖、required evidence、复核命令和关闭条件，同时保持外部 live 阻断语义不变。`
- Status: `Done`

## In Scope
- 新增 `contracts/fate/audit/external-validation-closure.json`。
- 新增 `scripts/external-validation-closure-gate.sh` / `.py`。
- 将 closure gate 接入 `scripts/local-ci.sh`，消费 current audit bundle 生成的 pending list。
- 增加回归测试，覆盖分类、manual triage、脱敏和 local-ci/docs 接线。
- 更新 scripts/audit/tests AGENTS、100% roadmap 和任务索引。

## Out of Scope
- 不连接真实 API、HF Space、Telegram Bot、Postgres、OIDC、SIEM、OTel、Vault/KMS、developer portal 或第三方审计系统。
- 不把外部连通验证改写成 passed。
- 不输出真实 token、secret、DSN、私钥、生产日志正文、用户报告正文或外部账号数据。
- 不减少 `pendingExternalValidationCount`。
- 不声明 FateCat 已达到 100% 测算基础设施。

## Task Package Tree
```text
TP-01 pending external occurrence 盲区确认
TP-02 closure plan contract 和 gate 实现
TP-03 local-ci、测试、文档和路线图接线
TP-04 验证、自审、提交推送
```

## Future-Optimal Contract
| Field | Value |
| --- | --- |
| Target End State | 每个外部待验证项都是可分派、可复核、可关闭的 audit closure resource，而不是散落在 Markdown 中的自然语言 TODO。 |
| Real Constraints | 真实生产凭证、外部账号、第三方审计和公网服务不能在本地伪造；当前只能生成关闭计划。 |
| Inertia Constraints | current audit bundle 已能列出 occurrence，但没有 owner、凭证依赖、关闭条件或复核命令。 |
| Wrong Concept / Wrong Boundary | 把 occurrence count 当成可执行交付计划。 |
| Kill List | 不新增 live smoke 伪证；不把 closure plan 写成 live evidence；不把敏感赋值写入 JSON。 |
| Proof Point | closure gate 输出每项 owner、credentialDependencies、requiredEvidence、verificationCommands、closureCondition，并在有任何待验证项时保持 `shipGate.status=blocked`。 |
| Falsifier | 任一 pending occurrence 被静默丢弃，或输出含 token/数据库 URL 敏感赋值形态、私钥标记，或 closure gate 宣称 live passed，则任务失败。 |
| Migration Slice | 只新增一个 audit closure gate，接在 current audit bundle 之后；certification 仍保持 blocked 语义。 |
| Rejected Short-Term Patches | 不在审计 Markdown 中人工补表；不硬编码当前 `/tmp` 证据；不绕过 current audit bundle。 |
| Future-Optimal Review Owner | `auto-review` document-drift + future-optimal-drift。 |

## Ponytail Contract
| Field | Value |
| --- | --- |
| Existence Check | `pending-external-validations.json` 已存在但不可分派；新增薄 gate 能降低审计交接成本，且复用现有 audit bundle。 |
| Selected Ladder Rung | 项目原生能力复用：以 current audit bundle 作为输入，输出机器可读 JSON。 |
| Skipped Scope | 不做真实外部连接、不做 secret broker、不做工单系统集成。 |
| Ceiling / Upgrade Path | 未来可把 closure items 同步到 issue tracker 或 control-plane resource registry。 |
| Do-not-simplify | 不得弱化隐私边界，不得把未分类项丢掉。 |
| Minimal Runnable Check | targeted pytest、closure CLI smoke、local-ci quick、secret scan、task docs validator。 |
| Complexity Review Owner | `auto-review` ponytail-complexity。 |

## Requirement Alignment
| Requirement | Alignment |
| --- | --- |
| 外部待验证项可分派 | 每个 closure item 输出 owner、凭证依赖、required evidence、复核命令和关闭条件。 |
| 不伪造 live | 有 pending item 时 `shipGate.status=blocked`，nonClaims 明确不证明 live。 |
| 隐私安全 | 输出仅保存脱敏 excerpt/hash，不保存真实 token、secret、DSN、私钥、生产日志正文或用户报告正文。 |
| 同构基础设施 | 将 occurrence 清单提升为机器可读 closure resource，符合 contract/control-plane/evidence gate 模式。 |

## Task Package Overview
| Node ID | Status | Evidence |
| --- | --- | --- |
| TP-01 | Done | Pending external occurrence list confirmed occurrence-only. |
| TP-02 | Done | Contract and closure gate added. |
| TP-03 | Done | local-ci, tests, AGENTS and roadmap wired. |
| TP-04 | Done | Targeted pytest, closure CLI smoke, ruff, format, secret scan, task docs validator and local-ci quick passed. |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
