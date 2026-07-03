# Task-Level Acceptance
| Requirement | Acceptance |
| --- | --- |
| Remote acceptance for final HEAD | Acceptance workflow has `status=completed`, `conclusion=success`, `headSha` equals final HEAD. |
| Remote container release for final HEAD | Container workflow with `push_image=true` has `status=completed`, `conclusion=success`, `headSha` equals final HEAD. |
| Release artifacts | GitHub Actions artifact `fatecat-release-artifacts-<full-sha>` exists. |
| Registry digest | GHCR image tag `<short-sha>` resolves to `sha256:<64 hex>`. |
| Attestation | GitHub Actions attestation verify passes in container workflow/current-release-proof. |
| Rollback | Dry-run rollback evidence has `kind=fatecat.rollback_drill_evidence`, `status=passed`, `productionRollbackExecuted=false`, commit matches final HEAD. |
| Aggregated proof | `current-release-proof.sh --require-current-release` exits 0 and `proofGate.status=pass`. |

# Validation Plan
| Validation | Command | Expected |
| --- | --- | --- |
| Task docs validator | `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0108-measurement-infrastructure-current-release-artifact-proof --phase closeout` | Pass before commit. |
| Acceptance dispatch | `gh workflow run acceptance.yml --ref main -f reason=current-release-proof-0108-final` | Run appears for final HEAD. |
| Container release dispatch | `gh workflow run container.yml --ref main -f push_image=true` | Run appears for final HEAD and publishes image. |
| Rollback evidence | `bash scripts/rollback-drill.sh --output-json /tmp/fatecat-rollback-drill-0108.json --release-artifacts-dir <downloaded-or-local-artifacts-dir>` | `status=passed`. |
| Release proof | `bash scripts/current-release-proof.sh --require-current-release --acceptance-run-id <id> --container-run-id <id> --rollback-evidence-path /tmp/fatecat-rollback-drill-0108.json --output-json /tmp/fatecat-current-release-proof-0108.json` | Exit 0, proof gate pass. |

# Review Gate
- Confirm no post-proof commit is made.
- Confirm GHCR digest and attestation are for final HEAD short tag.
- Confirm rollback remains dry-run and does not claim production traffic switched.
- Confirm production API/HF/Bot/OIDC/SIEM/OTel/Vault/KMS live remain out of scope.

# Runtime Verification Gate
Remote release proof is required. Local task validators are necessary but not sufficient.

# Ship Readiness
Ship readiness for 0108 means `current-release-proof --require-current-release` passes for final HEAD and no further commit invalidates the evidence.

# Task Package Acceptance
| Node ID | Acceptance |
| --- | --- |
| TP-01.01 | Pre-0108 release proof gap is recorded. |
| TP-01.02 | Container workflow release path is inspected. |
| TP-02.01 | 0108 task package is committed and pushed before dispatch. |
| TP-02.02 | Final HEAD is clean before dispatch. |
| TP-03.01 | Acceptance dispatched for final HEAD. |
| TP-03.02 | Container dispatched with `push_image=true` for final HEAD. |
| TP-04.01 | Both workflows reach terminal success. |
| TP-04.02 | Artifacts/digest/attestation verified. |
| TP-05.01 | Rollback dry-run evidence generated. |
| TP-05.02 | Aggregated current release proof passes. |

# Anti-Goals
- 不得修改 `governance/tasks/` 以外路径
- 不得虚构证据
- 不得越权补全未确认信息
