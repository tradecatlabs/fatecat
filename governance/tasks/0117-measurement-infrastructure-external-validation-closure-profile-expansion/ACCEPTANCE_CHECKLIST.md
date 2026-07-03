# Acceptance Checklist

# Global Standards
- [x] Future-optimal target recorded.
- [x] Ponytail existence check recorded.
- [x] No live overclaim introduced.

# Task Package Checklists
- [x] TP-01 sampled 0116 manual triage.
- [x] TP-02 expanded classifier profiles.
- [x] TP-03 validation complete.
- [x] TP-04 delivery complete.

## TP-01 Manual Triage Analysis
Verify: `jq` path/excerpt samples from 0116 closure artifact.
Gate: identify known domains without changing code first.
- [x] Manual items sampled.

## TP-02 Profile Expansion
Verify: `scripts/external-validation-closure-gate.py`.
Gate: no external live connection.
- [x] Profiles added.

## TP-03 Validation
Verify: targeted pytest, closure smoke, ruff, format, secret scan, local-ci quick.
Gate: `manualTriage=1`, `shipGate=blocked`.
- [x] Validation complete.

## TP-04 Delivery
Verify: task docs validator, commit, push, remote status when triggered.
Gate: clean branch.
- [x] Delivery complete.
