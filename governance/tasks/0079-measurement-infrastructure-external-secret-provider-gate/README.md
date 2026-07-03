# Task Overview

- Task ID: `0079`
- Slug: `measurement-infrastructure-external-secret-provider-gate`
- Objective: `执行 0078 之后的本地可执行 P0 安全基础设施切片：把 webhook encrypted config vault 从本地 Fernet baseline 推进为外部 secret provider / Vault / KMS 证据契约和反伪造门禁；接入 security registry、production-security gate、local-ci、回归测试和文档。无真实外部 secret manager 权限时只输出外部连通验证待执行，不声明外部 Vault/KMS、生产密钥生命周期或 public multi-replica ready 已完成。`
- Status: `Done`

## In Scope

- 新增外部 secret provider evidence contract。
- 新增 `external-secret-provider-gate`，验证契约、registry、policy、反伪造负例和可选 live evidence。
- 在 `SecurityControl` registry/schema/policy 中登记 `secret_provider` 控制。
- 接入 quick local-ci summary artifact 与 focused regression tests。
- 更新 roadmap、operations docs、AGENTS 与任务 closeout。

## Out of Scope

- 不接入真实 HashiCorp Vault、AWS KMS、GCP KMS、Azure Key Vault 或其他外部 secret manager。
- 不保存真实 secret、token、DSN、endpoint、KMS key ARN/URL、webhook URL 或 callback secret。
- 不声明 external Vault/KMS 已生产可用。
- 不声明 exactly-once、长期多副本生产 ready 或 public webhook live passed。

## Task Package Tree

```text
TP-01 现状复核与任务定界
  TP-01.01 复核 0059/0078 本地 vault 与 runtime 缺口
  TP-01.02 复核 security registry/schema/gate 接线点
TP-02 外部 secret provider 契约
  TP-02.01 新增 external-secret-provider evidence contract
  TP-02.02 新增反伪造负例与 live evidence schema
TP-03 Security control/gate 接线
  TP-03.01 更新 SecurityControl schema/registry/policy
  TP-03.02 新增 external-secret-provider-gate.py/.sh
  TP-03.03 接入 production-security gate 与 local-ci artifact
TP-04 Tests and docs
  TP-04.01 增加 regression tests
  TP-04.02 更新 roadmap、operations docs 和 AGENTS
TP-05 Verify/closeout/ship
  TP-05.01 运行 focused gates、ruff/format 和 quick CI
  TP-05.02 回填任务 closeout、提交、推送并记录 CI
```

## Requirement Alignment

- 0077/0078 之后仍缺外部 Vault/KMS、生产密钥生命周期、public webhook live passed、长期多副本和 exactly-once。
- 0059 已证明本地 Fernet encrypted config vault，但明确不证明外部 Vault/KMS。
- 本任务把“不能伪造外部 secret lifecycle”落成机器门禁，为后续真实外部 secret manager live evidence 留入口。

## Task Package Overview

| Node ID | Title | Status | Verify |
| --- | --- | --- | --- |
| TP-01.01 | 本地 vault 与 runtime 缺口复核 | Done | 0059/0078 docs 与 code |
| TP-01.02 | security 接线点复核 | Done | schema/registry/gate/local-ci |
| TP-02.01 | evidence contract | Done | contract JSON + gate |
| TP-02.02 | negative/live schema | Done | regression tests |
| TP-03.01 | schema/registry/policy | Done | production-security gate |
| TP-03.02 | external secret provider gate | Done | gate summary |
| TP-03.03 | local-ci 接入 | Done | quick CI artifact |
| TP-04.01 | regression tests | Done | pytest focused |
| TP-04.02 | docs/AGENTS | Done | grep + docs tests |
| TP-05.01 | validation gates | Done | focused gates + quick CI |
| TP-05.02 | closeout/git/CI | Done | git status/commit/push/CI |

## Reading Order

1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
