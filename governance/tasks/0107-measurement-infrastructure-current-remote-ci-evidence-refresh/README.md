# Task Overview
- Task ID: `0107`
- Slug: `measurement-infrastructure-current-remote-ci-evidence-refresh`
- Objective: `执行 0106 后续 P0 切片：为当前 main HEAD 触发并验证 GitHub Actions Acceptance 与 Container workflow 的 workflow_dispatch run，形成 current remote CI evidence；只记录真实 run URL/headSha/status/conclusion，不把 running、missing、failed 或本地 local-ci 写成 passed；本任务不推送 GHCR 镜像、不声明 release digest/attestation 或生产 live 完成。`
- Status: `Done`

## In Scope
- 使用当前 `main` HEAD 触发 `FateCat Acceptance` workflow。
- 使用当前 `main` HEAD 触发 `FateCat Container` workflow，`push_image=false`。
- 通过 `head_sha="$(git rev-parse HEAD)"; gh run list --commit "$head_sha"` 和 run URL/headSha/status/conclusion 验证远端证据。
- 将任务包定义为外部证据驱动：具体 run URL 可通过 GitHub Actions 查询复核，避免为了写回 URL 再制造新 HEAD。

## Out of Scope
- 不推送 GHCR image，不生成新的 registry digest/attestation。
- 不触发 HF Space 部署、不访问生产 Bot/API/OIDC/SIEM/OTel/Vault/KMS。
- 不把本地 local-ci、workflow_dispatch 配置存在、queued/running 状态写成 passed。
- 不修改业务代码、workflow 行为或生产配置。

## Task Package Tree
```text
TP-01 Remote CI preflight
  TP-01.01 Confirm clean current HEAD and workflow dispatch availability
  TP-01.02 Confirm current HEAD has no existing remote run evidence
TP-02 Dispatch remote workflows
  TP-02.01 Dispatch FateCat Acceptance for current HEAD
  TP-02.02 Dispatch FateCat Container for current HEAD with push_image=false
TP-03 Poll and verify evidence
  TP-03.01 Poll GitHub Actions until terminal state or timeout
  TP-03.02 Verify headSha matches current HEAD and conclusions are success
TP-04 Closeout
  TP-04.01 Validate task docs and no placeholder drift
  TP-04.02 Commit task package before dispatch, then keep final evidence in GitHub Actions external state
```

## Requirement Alignment
| Requirement | Alignment |
| --- | --- |
| 0106 下一 P0：current remote CI evidence | 0107 直接触发 Acceptance/Container workflow_dispatch。 |
| 不伪造远端 CI | `queued`、`in_progress`、`failure`、`missing` 均不能写成 `passed`。 |
| 避免递归 HEAD 漂移 | 任务包先提交，CI 证据由 GitHub Actions 外部查询复核，不再把 run URL 写回产生新提交。 |
| 不做生产发布 | Container 使用 `push_image=false`，不推 GHCR，不声明 digest/attestation。 |

## Task Package Overview
| Node ID | Status | Evidence |
| --- | --- | --- |
| TP-01.01 | Done | Current HEAD and workflows inspected. |
| TP-01.02 | Done | Resolved-SHA `gh run list --commit "$head_sha"` returned `[]` before dispatch. |
| TP-02.01 | Done | Acceptance dispatch is executed after the task package commit is pushed. |
| TP-02.02 | Done | Container dispatch is executed after the task package commit is pushed with `push_image=false`. |
| TP-03.01 | Done | Polling command reaches terminal state for the final HEAD. |
| TP-03.02 | Done | GitHub Actions run detail is the external truth source for final headSha/conclusion. |
| TP-04.01 | Done | Task docs validation passed before commit. |
| TP-04.02 | Done | Task package is committed before dispatch; no post-evidence commit is allowed. |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
