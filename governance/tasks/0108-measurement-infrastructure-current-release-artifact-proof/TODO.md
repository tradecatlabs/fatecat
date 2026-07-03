# Execution Checklist
[x] TP-01.01 | P0 | Confirm current release proof missing items after 0107 | Verify: pre-0108 current-release-proof | Gate: release artifacts/digest/attestation/rollback missing | Parallelizable: Yes
[x] TP-01.02 | P0 | Confirm container workflow supports push_image=true release path | Verify: inspect container.yml | Gate: upload/push/attest/verify path exists | Parallelizable: Yes
[x] TP-02.01 | P0 | Commit and push 0108 task package | Verify: git status/log | Gate: clean before dispatch | Parallelizable: No
[x] TP-02.02 | P0 | Confirm clean final HEAD before dispatch | Verify: git rev-parse HEAD | Gate: final SHA locked | Parallelizable: No
[x] TP-03.01 | P0 | Dispatch Acceptance for final HEAD | Verify: gh workflow run acceptance.yml | Gate: run appears for final SHA | Parallelizable: Yes
[x] TP-03.02 | P0 | Dispatch Container for final HEAD with push_image=true | Verify: gh workflow run container.yml -f push_image=true | Gate: run appears for final SHA | Parallelizable: Yes
[x] TP-04.01 | P0 | Poll workflows until terminal success | Verify: gh run list/view | Gate: both completed success | Parallelizable: No
[x] TP-04.02 | P0 | Verify release artifacts upload, GHCR digest and attestation | Verify: current-release-proof | Gate: artifact/digest/attestation pass | Parallelizable: No
[x] TP-05.01 | P0 | Generate dry-run rollback drill evidence for final HEAD | Verify: rollback-drill.sh | Gate: status passed, productionRollbackExecuted false | Parallelizable: No
[x] TP-05.02 | P0 | Run current-release-proof --require-current-release | Verify: current-release-proof JSON | Gate: proofGate pass | Parallelizable: No

说明：
- 每一行后续必须绑定 `TP-XX(.YY...)`
- 不允许出现无归属 TODO
