# Acceptance Checklist

# Global Standards
- [x] 不声明 FateCat 已达到 100% 测算基础设施。
- [x] 不把 0149 synthetic tests 写成真实专家评审。
- [x] 不把 local-ci 或 dry-run 写成 production live。
- [x] 所有外部账号、token、DSN、Bot、OIDC、SIEM、OTel、Vault/KMS、Postgres live 均保持 pending。
- [x] 最终 certification 仍以 `canClaim100Percent=true` 为唯一完成信号。

# Task Package Checklists
## Fact and source baseline

### TP-01.01 Current repo evidence
- [x] Current commit recorded.
- [x] Remote Acceptance run recorded.
- [x] 0149 blocked reason recorded.
- [x] local CI artifact path recorded.
Verify: CONTEXT repo evidence table.
Gate: facts match current git/GitHub evidence.

### TP-01.02 Official source matrix
- [x] Kubernetes controller source mapped.
- [x] OpenAPI and AsyncAPI source mapped.
- [x] OpenTelemetry and SRE source mapped.
- [x] OWASP, SLSA, OpenSSF and CNCF source mapped.
Verify: CONTEXT external source matrix.
Gate: each source maps to a FateCat requirement.

## Gap matrix

### TP-02.01 Certification blocked baseline
- [x] `status=blocked` recorded.
- [x] `canClaim100Percent=false` recorded.
- [x] domain count and blocker count recorded.
Verify: certification baseline command.
Gate: no passed claim while blockers remain.

### TP-02.02 Non-forgeable evidence categories
- [x] Core quality external evidence category listed.
- [x] Production live proof category listed.
- [x] SRE/security/developer/runtime category listed.
- [x] Release/audit/certification category listed.
Verify: PLAN and roadmap.
Gate: categories produce concrete closure gates.

## Remaining task tree

### TP-03.01 100 percent task tree
- [x] External proof/live closure included.
- [x] Core quality review/benchmark closure included.
- [x] Final release proof included.
- [x] Independent audit and certification included.
Verify: PLAN dependency graph and roadmap section.
Gate: tree is complete enough to drive next tasks.

### TP-03.02 Next executable tasks
- [x] Local next task separated from external operator tasks.
- [x] 0151 candidate does not bypass external proof/live.
- [x] Final certification kept after accepted evidence only.
Verify: PLAN next executable leaves.
Gate: no external blocker is hidden by planning task.

## Documentation and validation

### TP-04.01 Roadmap and task package
- [x] Roadmap post-0149 section added.
- [x] 0150 task package filled.
Verify: `rg` markers.
Gate: no template placeholders remain after decompose validation.

### TP-04.02 Local validation
- [x] Task docs validation passed.
- [x] Roadmap marker check passed.
- [x] Certification baseline command passed.
- [x] `git diff --check` passed.
Verify: terminal evidence.
Gate: no local validation failure remains.
