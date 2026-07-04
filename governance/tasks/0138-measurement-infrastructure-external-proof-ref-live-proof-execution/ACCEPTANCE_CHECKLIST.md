# Acceptance Checklist

# Global Standards
- [x] Evidence is tied to current HEAD.
- [x] Evidence stores redacted refs and hashes only.
- [x] No proof-ref/live proof/certification/audit completion is claimed.
- [ ] All 22 proof refs are accepted.
- [ ] All 22 live proofs are accepted.

# Task Package Checklists
## TP-01 Current External Validation Input Chain

Verify: source hashes are present in readiness matrix.
Gate: current HEAD binding.
- [x] Current input artifacts identified.

## TP-02 Issue/Runbook/Proof-Ref Readiness Matrix

Verify: matrix has 22 work items and 22 tracker refs.
Gate: redacted readiness evidence.
- [x] Matrix generated.

## TP-03 Execute Proof-Ref Runbooks

Verify: proof-ref gate accepts 22 proof refs.
Gate: external-validation-proof-ref-gate.
- [ ] Awaiting real external proof-ref bundle.

## TP-04 Execute Live Proof Validation

Verify: live proof gate accepts 22 live proofs.
Gate: external-validation-live-proof-gate.
- [ ] Awaiting accepted proof refs and live evidence bundle.

## TP-05 Re-Run Closure/Certification/Audit Chain

Verify: closure/certification/audit no longer blocked by proof/live missing.
Gate: certification and audit rehearsal.
- [ ] Awaiting TP-03 and TP-04.

## TP-06 Ship-Readiness Claim Check

Verify: final 100% claim criteria are all proven.
Gate: final ship gate.
- [ ] Awaiting certification and independent third-party audit.
