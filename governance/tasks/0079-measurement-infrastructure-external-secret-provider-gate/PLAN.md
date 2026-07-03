# Planning Summary

0079 的目标是把“外部 Vault/KMS 仍未完成”从文档说明推进为机器可验证的证据契约和反伪造门禁。它不做真实外部集成，也不引入 Vault SDK；正确切片是先固定 live evidence schema、拒绝伪证、接入 quick CI，并让后续真实外部 secret manager 验证能通过同一入口提交脱敏证据。

# Lifecycle Gates

禁止跳过任何 gate；如果某个 gate 失败，0079 不能标记 Done。

| Phase | Gate | Status |
| --- | --- | --- |
| SPEC | 范围限定为 secret provider evidence gate，不声明 live passed | Done |
| PLAN | 任务树和验收写入 0079 文档 | Done |
| BUILD | contract、gate、registry/schema/policy、local-ci、tests/docs | Done |
| TEST | focused tests、security gates、quick CI | Done |
| REVIEW | 不把 local Fernet 写成 external Vault/KMS | Done |
| SHIP | commit/push/CI evidence | Done |

# Future-Optimal Contract

- target end state: FateCat 的生产 secret 生命周期由外部 secret provider/Vault/KMS 管理，并能用脱敏 evidence 证明 key reference、rotation、access audit 和 application injection。
- real constraints: 当前没有真实外部 secret manager 权限；live evidence 只能标记外部连通验证待执行。
- inertia constraints: 已有本地 Fernet codec 仍作为 local encrypted-at-rest baseline，不能重写为假的外部 provider。
- kill list: local Fernet 伪装 Vault/KMS、env var 伪装 secret manager、placeholder proof 伪装 live evidence、gate summary 输出 secret。
- proof point: `external-secret-provider-gate` 能拒绝伪造 evidence，并进入 quick local-ci。
- falsifier: fake `local_fernet` evidence 被 gate 接受，或 contract/registry 没有被 production-security gate 覆盖。
- migration slice: 在 security control plane 上新增 secret provider 资源和门禁，为后续真实外部 live evidence 铺路。
- rejected short-term patches: 只改 roadmap；只在 runtime backend 写 blockedClaims；引入外部 SDK 但无法验证。

# Ponytail Contract

- existence check: 0077/0078 后外部 Vault/KMS 是明确 P0 缺口；只靠文本 blockedClaim 不足以形成生产安全准入。
- selected ladder rung: 项目内 gate + JSON contract，复用既有 security-externalization gate 模式。
- skipped scope: 真实 Vault/KMS SDK、生产凭证、外部账号、真实 key rotation。
- ceiling / upgrade path: 后续提供真实 provider 后，在同一 evidence schema 下执行 live check。
- do-not-simplify: 反伪造负例、脱敏扫描、local-ci artifact 和 external pending 口径不能省略。
- minimal runnable check: gate summary + focused pytest + production-security gate + quick CI。
- complexity review owner: `auto-review` security/document-drift/future-optimal-drift。

# Document-Driven Contract

- Operating model update: not needed；项目定位不变。
- Toolchain model update: local-ci 新增 secret provider gate artifact。
- Process update: production-security gate 需要认识 secret provider control。
- Source-of-truth updates: security contract/schema/registry/policy、operations docs、roadmap、task docs。
- Local README/AGENTS impact: `scripts/AGENTS.md`、`contracts/fate/security/AGENTS.md`。
- Contract/catalog/schema impact: `contracts/fate/security/*`。
- ADR/Gate/module-context impact: not needed；沿用 security gate 模式。
- Documentation exemption reason: 无。
- Validation evidence: focused tests、quick CI、task validators。

# Simplest Path

新增 `contracts/fate/security/external-secret-provider-contract.json`，新增 `scripts/external-secret-provider-gate.py/.sh` 复用 existing gate style；更新 `security-control.schema.json` 支持 `secret_provider`；在 `registry.json` 登记 `control.external_secret_provider_kms`；让 `production-security-gate.py` 和 `local-ci.sh` 执行该 gate；增加 regression tests 验证 contract、负例、脱敏和 registry 接线。

# Split Strategy

- Contract 先落地，保证 live evidence schema 和 negative cases 可被机器验证。
- Security control/gate 再接线，保证 registry、policy 和 production-security gate 一致。
- local-ci 与 tests 随后接入，避免 contract 成为孤立文档。
- docs/AGENTS 最后同步，明确 external Vault/KMS live evidence 仍待真实外部环境。

# Execution Waves

| Wave | Leaves | Purpose | Status |
| --- | --- | --- | --- |
| 1 | TP-01.01, TP-01.02 | 现状复核 | Done |
| 2 | TP-02.01, TP-02.02 | Contract | Done |
| 3 | TP-03.01, TP-03.02, TP-03.03 | Gate wiring | Done |
| 4 | TP-04.01, TP-04.02 | Tests/docs | Done |
| 5 | TP-05.01, TP-05.02 | Verify/ship | Done |

# Runtime Workflow Contract

| Field | Value |
| --- | --- |
| allowed tools | `rg`、`sed`、`apply_patch`、pytest、ruff、local-ci、git/gh |
| forbidden actions | 不读取真实 secret、不接外部 Vault/KMS、不声明 live passed、不修改业务算法 |
| required evidence | gate summary、focused tests、production-security gate、quick CI、task validators、Git/CI evidence |
| stop condition | 缺真实 secret provider 权限只阻止 live path，不阻止本地 contract/gate baseline |

# Next Executable Leaves

| Node ID | Action |
| --- | --- |
| - | - |

# Dependency Graph

```text
TP-01.01 -> TP-01.02 -> TP-02.01 -> TP-02.02 -> TP-03.01 -> TP-03.02 -> TP-03.03 -> TP-04.01 -> TP-04.02 -> TP-05.01 -> TP-05.02
```

# Rollback Protocol

- 删除 `contracts/fate/security/external-secret-provider-contract.json`。
- 删除 `scripts/external-secret-provider-gate.py/.sh` 和对应 regression tests。
- 恢复 security schema/registry/policy、production-security gate、local-ci、docs/AGENTS 和任务索引。
