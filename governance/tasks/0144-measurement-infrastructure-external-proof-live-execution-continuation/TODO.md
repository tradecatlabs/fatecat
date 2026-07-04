# Execution Checklist
[x] TP-01.01 | P0 | Refresh current HEAD local-ci external validation artifacts | Verify: `test -f /tmp/fatecat-local-ci-0144-abab926/external-validation-closure-gate.json && test -f /tmp/fatecat-local-ci-0144-abab926/external-validation-live-proof-gate.json` | Gate: local-ci quick passed and artifact root exists | Parallelizable: Yes
[x] TP-02.01 | P0 | Record operator readiness summary | Verify: `jq '{status, summary}' /tmp/fatecat-local-ci-0144-abab926/external-validation-operator-execution-packet.json` | Gate: operatorSteps=22 and status=operator_action_required | Parallelizable: Yes
[ ] TP-03.01 | P0 | Submit and verify 22 proof-ref bundles | Verify: `bash scripts/external-validation-proof-ref-gate.sh --work-queue-json /tmp/fatecat-local-ci-0144-abab926/external-validation-closure-work-queue.json --evidence-json <proof-ref-bundle-json> --output-json <proof-ref-gate-json>` | Gate: acceptedProofRefs=22 | Parallelizable: No
[ ] TP-04.01 | P0 | Submit and verify 22 live proof bundles | Verify: `bash scripts/external-validation-live-proof-gate.sh --work-queue-json /tmp/fatecat-local-ci-0144-abab926/external-validation-closure-work-queue.json --proof-ref-gate-json <accepted-proof-ref-gate-json> --category-runbooks-json /tmp/fatecat-local-ci-0144-abab926/external-validation-category-runbooks.json --live-evidence-json <live-proof-bundle-json> --output-json <live-proof-gate-json>` | Gate: acceptedLiveProofs=22 | Parallelizable: No
[ ] TP-05.01 | P0 | Rerun closure summary, certification and audit rehearsal after proof/live accepted | Verify: `bash scripts/measurement-infrastructure-certification.sh --evidence-dir <accepted-evidence-dir> --require-certified --output-json <certification-json>` | Gate: certification canClaim100Percent=true after independent audit accepted | Parallelizable: No

说明：
- 每一行后续必须绑定 `TP-XX(.YY...)`
- 不允许出现无归属 TODO
