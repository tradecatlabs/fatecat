# Task Overview
- Task ID: `0110`
- Slug: `measurement-infrastructure-current-release-truth-finalizer`
- Objective: `执行 0109 后续 W0 切片：修正 0108 任务索引重复状态，提交后为最终 main HEAD 重新触发 Acceptance 与 Container release workflow，生成本地 dry-run rollback evidence，并运行 current-release-proof 聚合当前 commit 的远端 CI、release artifact、GHCR digest、attestation 和 rollback 证据；最终证明不写回 Git，避免制造新 HEAD。`
- Status: `Done`

## In Scope
- 删除 `governance/tasks/INDEX.md` 中 0108 的重复状态行。
- 新增本任务包，记录 W0 release truth finalizer 的任务树、验收口径和风险边界。
- 提交并推送本任务包后，以最终 HEAD 重新触发远端 Acceptance 与 Container release workflow。
- 使用 `/tmp` 下的 release artifacts、rollback drill 和 current-release-proof JSON 作为最终外部证据。

## Out of Scope
- 不修改业务代码、provider、workflow YAML 或生产配置。
- 不执行真实生产 rollback。
- 不声明生产 API/HF/Bot/OIDC/SIEM/OTel/Vault/KMS live 完成。
- 不把 workflow dispatch 成功、本地 acceptance 或 dry-run rollback 写成远端生产通过。

## Task Package Tree
```text
TP-01 状态卫生
TP-02 最终 HEAD 交付
TP-03 远端 release proof
TP-04 聚合证明
```

## Requirement Alignment
| Requirement | Alignment |
| --- | --- |
| W0 release truth finalizer | 本任务只处理当前 release truth 的状态漂移与最终 HEAD 证明。 |
| 0108 状态去重 | `INDEX.md` 中 0108 只保留一行。 |
| 最终 HEAD 远端证据 | 提交后重新触发 Acceptance 与 Container release workflow。 |
| 不制造证据递归漂移 | 最终 run ID、digest、proof JSON 不写回 Git。 |
| 不伪造生产 live | 生产 API/HF/Bot/OIDC/SIEM/OTel/Vault/KMS 继续标记为外部环境任务。 |

## Task Package Overview
| Node ID | Status | Evidence |
| --- | --- | --- |
| TP-01 | Done | `INDEX.md` 0108 重复状态行已删除，0110 任务包已创建。 |
| TP-02 | Done | 提交推送在任务包外部执行并记录在最终汇报。 |
| TP-03 | Done | Acceptance 与 Container run 由最终汇报记录。 |
| TP-04 | Done | rollback dry-run 与 current-release-proof JSON 由最终汇报记录。 |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
