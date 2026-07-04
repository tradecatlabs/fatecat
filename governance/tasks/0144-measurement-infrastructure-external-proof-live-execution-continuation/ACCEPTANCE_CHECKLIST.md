# Acceptance Checklist

# Global Standards
- [x] Current local evidence is bound to current HEAD `abab9268...`.
- [x] Local readiness is not claimed as live completion.
- [x] Proof-ref and live-proof accepted counts remain explicitly 0.
- [x] Real credentials are not stored.
- [x] 100% certification remains blocked.

# Task Package Checklists
## Current evidence refresh

### TP-01.01 Current HEAD local-ci
- [x] local-ci quick passed.
- [x] external validation artifact root recorded.
Verify: `test -f /tmp/fatecat-local-ci-0144-abab926/local-ci-summary.json || test -d /tmp/fatecat-local-ci-0144-abab926`.
Gate: evidence root exists and regression output showed `389 passed`.

## Operator readiness

### TP-02.01 Operator packet ready
- [x] workItems=22.
- [x] runbooks=22.
- [x] operatorSteps=22.
- [x] operatorCommands=104.
Verify: `jq '{status, summary}' /tmp/fatecat-local-ci-0144-abab926/external-validation-operator-execution-packet.json`.
Gate: status is `operator_action_required`.

## Proof-ref execution

### TP-03.01 Proof-ref bundle accepted
- [ ] 22 proof-ref bundles submitted by operator.
- [ ] proof-ref gate accepted all work items.
Verify: `jq '.summary' <accepted-proof-ref-gate-json>`.
Gate: `acceptedProofRefs=22`.

## Live proof execution

### TP-04.01 Live proof bundle accepted
- [ ] 22 live proof bundles submitted by operator.
- [ ] live proof gate accepted all work items.
Verify: `jq '.summary' <accepted-live-proof-gate-json>`.
Gate: `acceptedLiveProofs=22`.

## Closure and certification

### TP-05.01 Certification refresh
- [ ] closure evidence summary unblocked.
- [ ] independent audit result accepted.
- [ ] measurement infrastructure certification passed.
Verify: `jq '.certificationGate' <certification-json>`.
Gate: `canClaim100Percent=true`.
