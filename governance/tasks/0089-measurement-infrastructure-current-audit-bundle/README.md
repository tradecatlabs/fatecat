# Task Overview
- Task ID: `0089`
- Slug: `measurement-infrastructure-current-audit-bundle`
- Objective: `为当前 commit 建立可交给第三方复核的 current audit bundle，聚合 current release proof、audit handoff、dry-run、release artifacts、rollback drill、evidence index、risk register 和 pending external validations。`
- Status: `Done`

## In Scope

- 新增 `contracts/fate/audit/current-bundle.json`，定义 current audit bundle 的输入证据、输出结构、required/local 模式和隐私边界。
- 新增 `scripts/current-audit-bundle.py/.sh`，从当前 commit 证据生成 Markdown/JSON 审计包、evidence index、risk register 和 pending external validations。
- 将 rollback drill、current release proof local contract 和 current audit bundle 接入 `scripts/local-ci.sh` quick profile summary。
- 新增 `tests/regression/test_current_audit_bundle.py`，覆盖 local blocked bundle、required 模式拒绝 local-contract 伪证、synthetic passed proof、AGENTS/local-ci wiring。
- 更新 scripts/contracts/tests AGENTS、roadmap 和 task index。

## Out of Scope

- 不替代真实第三方审计。
- 不执行真实生产 API/HF/Bot live smoke。
- 不执行真实生产回滚。
- 不保存 GitHub token、registry token、secret、DSN、用户报告正文、真实生产日志或真实用户输入。
- 不把 local-contract/current audit bundle `blocked` 写成 100% production passed。

## Future-Optimal Task Contract

| Field | Value |
| --- | --- |
| Target end state | 每个 release commit 都能一键生成当前提交审计交接包，审计人员可从 Git、CI、release proof、SBOM/provenance、rollback dry-run、risk register 和外部待验证项逐项复核。 |
| Real constraints | 第三方审计、生产 API/HF/Bot、OIDC/SIEM、外部监控和真实生产回滚依赖外部账号/凭证/授权；本地 quick CI 不能依赖远端网络。 |
| Inertia constraints | 0068 audit handoff、0069 dry-run、0088 current release proof 已存在，不能复制成第二套不一致审计流程。 |
| Wrong concept / wrong boundary | 把分散的任务文档、历史 CI、local-contract proof 或 dry-run rollback 当成当前提交生产审计通过。 |
| Kill list | 人工口头列证据；缺少 current commit 校验的审计包；不列外部待验证项的“完美”交付材料。 |
| Proof point | `current-audit-bundle.sh --require-current-release` 在 final HEAD 远端 release proof 完整后输出 `auditGate=passed`，local mode 在外部证据未齐时只能 blocked。 |
| Falsifier | bundle 接受旧 commit 证据、遗漏 pending external validations、输出敏感 marker、或 required 模式接受 local-contract proof。 |
| Migration slice | 先把已有 release/audit/rollback 证据聚合成 current audit bundle；未来再接第三方审计签名、生产 live evidence 和外部审计平台。 |
| Rejected short-term patches | 不在 README 手写一份不可复现审计总结；不把 `auditGate=blocked` 改字为 passed。 |
| Future-optimal review owner | `auto-review: future-optimal-drift` |

## Ponytail Task Contract

| Field | Value |
| --- | --- |
| Existence check | 0088 已有 current release proof，但第三方审计仍需一份当前 commit 的完整 evidence index、risk register 和 pending external list；该对象是 100% 测算基础设施审计闭环所必需。 |
| Selected ladder rung | project-native script + existing audit/release artifacts；自研只做证据编排、校验和脱敏输出。 |
| Skipped scope | 第三方审计签署、生产 API/HF/Bot live、真实回滚执行、外部 SIEM/OIDC/监控 live。 |
| Ceiling / upgrade path | 后续可增加 signed auditor attestation、production live evidence refs、external audit portal upload 和 immutable evidence store。 |
| Do-not-simplify | 不泄露凭证；不跳过 current HEAD 校验；不吞掉 required evidence failure；不隐藏外部待验证项。 |
| Minimal runnable check | `bash scripts/current-audit-bundle.sh --output-dir <dir> ...` |
| Complexity review owner | `auto-review: ponytail-complexity` |

## Document-Driven Task Contract

| Field | Value |
| --- | --- |
| Operating model update | not needed：基础设施定位不变。 |
| Toolchain model update | updated：新增 current audit bundle generator 并接入 `local-ci.sh`。 |
| Process update | updated：release/audit closeout 需要 current audit bundle。 |
| Source-of-truth updates | updated：audit contract、scripts/tests/contracts AGENTS、roadmap、task index。 |
| Local README/AGENTS impact | updated：scripts/tests/contracts AGENTS。 |
| Contract/catalog/schema impact | updated：新增 `contracts/fate/audit/current-bundle.json`。 |
| ADR/Gate/module-context impact | not needed：沿用 AuditHandoff/ReleaseGate 资源模型。 |
| Documentation exemption reason | none。 |
| Validation evidence | focused pytest、ruff、secret scan、quick CI 和 post-push required current audit bundle。 |

## Task Package Tree

```text
TP-01 SPEC: 识别 0088 后 current audit handoff 缺口
TP-02 PLAN: 定义 current audit bundle 输入、输出、gate 和 no-overclaim
TP-03 BUILD: 实现 contract、generator、local-ci wiring、docs 和 regression
TP-04 TEST: 运行 focused pytest、ruff、secret scan、quick CI
TP-05 SHIP: commit/push，触发远端 CI，生成 required current audit bundle
```

## Key Deliverables

- `contracts/fate/audit/current-bundle.json`
- `scripts/current-audit-bundle.py`
- `scripts/current-audit-bundle.sh`
- `tests/regression/test_current_audit_bundle.py`
- `scripts/local-ci.sh`

## Requirement Alignment

| Requirement | Implementation |
| --- | --- |
| current commit audit handoff | bundle validates supplied evidence commit fields against current HEAD |
| evidence index | output `evidence-index.json` and Markdown Evidence Index section |
| risk register | output `risk-register.json` and Markdown Risk Register section |
| pending external list | reuses audit handoff `pendingExternalValidations` |
| no overclaim | local mode produces blocked; required mode fails unless current release proof/local CI/evidence pass |
| privacy | forbidden marker scan rejects token/secret/password/private key markers |

## Task Package Overview

| Node ID | Title | Status | Acceptance |
| --- | --- | --- | --- |
| TP-01 | SPEC | Done | 0088 后缺少当前 commit 审计 bundle 聚合器 |
| TP-02 | PLAN | Done | local/required 模式和 no-overclaim 边界定义 |
| TP-03 | BUILD | Done | contract、generator、wiring、docs、tests implemented |
| TP-04 | TEST | Done | local validation passed before commit |
| TP-05 | SHIP | Done | final remote proof and required audit bundle generated after commit/push |

## Reading Order

1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
