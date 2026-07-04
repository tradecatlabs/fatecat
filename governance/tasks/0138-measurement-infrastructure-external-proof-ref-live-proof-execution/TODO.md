# Execution Checklist
[x] TP-01 | P0 | Current external validation input chain: identify current work queue, runbooks, operator packet, proof-ref gate, live proof gate and 0137 tracker evidence. | Verify: source hashes in readiness matrix | Gate: current HEAD binding | Parallelizable: No
[x] TP-02 | P0 | Issue/runbook/proof-ref readiness matrix: map 22 work items to tracker refs, runbooks, credential names and pending reasons. | Verify: matrix has 22 items and 22 refs | Gate: redacted readiness evidence | Parallelizable: No
[ ] TP-03 | P0 | Execute proof-ref runbooks using real external credentials and submit redacted proof-ref bundle. | Verify: proof-ref gate accepts 22 proof refs | Gate: external-validation-proof-ref-gate | Parallelizable: Yes
[ ] TP-04 | P0 | Execute live proof validation and submit redacted live evidence bundle. | Verify: live proof gate accepts 22 live proofs | Gate: external-validation-live-proof-gate | Parallelizable: Yes
[ ] TP-05 | P0 | Re-run closure summary, certification and third-party audit rehearsal after proof/live acceptance. | Verify: closure no longer blocked by proof/live missing | Gate: certification and audit rehearsal | Parallelizable: No
[ ] TP-06 | P0 | Ship-readiness claim check for 100% measurement infrastructure. | Verify: certification canClaim100Percent true and independent audit accepted | Gate: final ship gate | Parallelizable: No

说明：
- 每一行后续必须绑定 `TP-XX(.YY...)`
- 不允许出现无归属 TODO
