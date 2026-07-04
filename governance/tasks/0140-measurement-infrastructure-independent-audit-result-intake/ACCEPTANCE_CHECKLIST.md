# Acceptance Checklist

# Global Standards
- [x] No real third-party audit result is fabricated.
- [x] No raw URL, token, secret, DSN, webhook secret, report body or user input is stored.
- [x] Independent audit accepted state does not imply production 100%.
- [x] Focused regression passed.
- [x] Quick local-ci passed.

# Task Package Checklists
## TP-01 Current Rehearsal Gap
Verify: hard-coded independent result gap is identified.
Gate: current rehearsal script/test inspection.
- [x] Gap documented.

## TP-02 Independent Audit Result Intake Gate
Verify: contract and script exist.
Gate: focused regression.
- [x] Contract added.
- [x] Gate added.
- [x] Pending/accepted/rejected/negative tests added.

## TP-03 Rehearsal and Local-CI Wiring
Verify: third-party rehearsal consumes gate and local-ci produces it.
Gate: focused regression and quick local-ci.
- [x] Rehearsal wiring added.
- [x] Local-ci wiring added.

## TP-04 Regression and Documentation
Verify: AGENTS/roadmap/tests updated.
Gate: wiring tests.
- [x] scripts/contracts/tests AGENTS synchronized.
- [x] roadmap updated.
- [x] task index updated.

## TP-05 Task Evidence Closeout
Verify: task evidence files exist.
Gate: task docs validation.
- [x] Pending gate evidence copied.
- [x] Rehearsal evidence copied.
- [x] Local-ci summary copied.
