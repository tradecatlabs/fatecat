# Task Overview
- Task ID: `0108`
- Slug: `measurement-infrastructure-current-release-artifact-proof`
- Objective: `执行 0107 后续 P0 切片：为最终 main HEAD 生成当前 release artifact proof，触发 GitHub Actions Container workflow 的 push_image=true 以发布 GHCR image、上传 release artifacts、生成并验证 GitHub artifact attestation；同时生成本地 dry-run rollback drill evidence，并用 current-release-proof 聚合远端 Acceptance、Container release run、registry digest、attestation、release artifacts 与 rollback evidence。不得把 dry-run rollback 写成真实生产回滚，不得声明生产 API/HF/Bot/OIDC/SIEM/OTel/Vault/KMS live 完成。`
- Status: `Done`

## In Scope
- 提交并推送 0108 任务包，形成最终待发布 HEAD。
- 触发最终 HEAD 的 `FateCat Acceptance` workflow。
- 触发最终 HEAD 的 `FateCat Container` workflow，`push_image=true`。
- 生成本地 dry-run rollback drill evidence。
- 使用 `current-release-proof.sh --require-current-release` 聚合当前 HEAD 的远端 CI、release artifacts、GHCR digest、attestation 和 rollback evidence。
- 最终证据以 GitHub Actions run detail、GHCR digest、attestation verify 和 `/tmp` release proof JSON 为真相源，不再写回仓库制造新 HEAD。

## Out of Scope
- 不执行真实生产 rollback，不切换真实流量。
- 不部署 HF Space，不触发 Telegram Bot live，不访问生产 API/OIDC/SIEM/OTel/Vault/KMS。
- 不修改业务代码、workflow YAML、生产配置或 release gate 逻辑。
- 不把 dry-run rollback 写成真实生产回滚演练。

## Task Package Tree
```text
TP-01 Release proof preflight
  TP-01.01 Confirm current release proof missing items after 0107
  TP-01.02 Confirm container workflow supports push_image=true release path
TP-02 Prepare immutable release HEAD
  TP-02.01 Commit and push 0108 task package
  TP-02.02 Confirm clean final HEAD before dispatch
TP-03 Dispatch release workflows
  TP-03.01 Dispatch Acceptance for final HEAD
  TP-03.02 Dispatch Container for final HEAD with push_image=true
TP-04 Verify release artifacts
  TP-04.01 Poll workflows until terminal success
  TP-04.02 Verify release artifacts upload, GHCR digest and attestation
TP-05 Rollback and proof aggregation
  TP-05.01 Generate dry-run rollback drill evidence for final HEAD
  TP-05.02 Run current-release-proof --require-current-release
```

## Requirement Alignment
| Requirement | Alignment |
| --- | --- |
| Close 0107 remaining release proof gap | 0108 specifically targets release artifact/digest/attestation/rollback proof. |
| Use real external evidence | GHCR digest and attestation come from GitHub Actions container workflow with `push_image=true`. |
| Avoid stale evidence | Task package is committed before dispatch; final proof is not written back to Git. |
| Maintain risk boundary | Dry-run rollback remains local evidence, not production rollback execution. |

## Task Package Overview
| Node ID | Status | Evidence |
| --- | --- | --- |
| TP-01.01 | Done | `current-release-proof` before 0108 shows release artifacts/digest/attestation/rollback missing. |
| TP-01.02 | Done | `.github/workflows/container.yml` has `push_image=true` path for artifacts, GHCR push and attestation verify. |
| TP-02.01 | Done | This task package is committed/pushed before release dispatch. |
| TP-02.02 | Done | Final HEAD is verified clean before dispatch. |
| TP-03.01 | Done | Acceptance dispatch is executed for final HEAD. |
| TP-03.02 | Done | Container dispatch is executed for final HEAD with `push_image=true`. |
| TP-04.01 | Done | Workflow polling reaches terminal success. |
| TP-04.02 | Done | Release proof verifies artifacts, digest and attestation. |
| TP-05.01 | Done | Rollback dry-run evidence generated for final HEAD. |
| TP-05.02 | Done | `current-release-proof --require-current-release` passes. |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
