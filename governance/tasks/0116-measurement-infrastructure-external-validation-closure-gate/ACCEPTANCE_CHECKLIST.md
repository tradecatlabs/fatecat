# Acceptance Checklist

# Global Standards
- [x] Future-optimal target end state recorded.
- [x] Ponytail existence check recorded.
- [x] No production secret or external live claim is introduced.

# Task Package Checklists
- [x] TP-01 pending occurrence blind spot confirmed.
- [x] TP-02 contract and closure gate implemented.
- [x] TP-03 local-ci/tests/docs wired.
- [x] TP-04 validation and delivery complete.

## TP-01 Pending Occurrence Blind Spot
Verify: `/tmp/fatecat-current-audit-bundle-finalizer-0115/pending-external-validations.json` sample inspection.
Gate: occurrence list has no owner/credential/closure fields and no external live claim.
- [x] Pending external list blind spot identified.

## TP-02 Closure Contract And Gate
Verify: `contracts/fate/audit/external-validation-closure.json` and `scripts/external-validation-closure-gate.py`.
Gate: output remains blocked when pending items exist.
- [x] Contract and gate implemented.

## TP-03 Local CI Tests Docs
Verify: local-ci, tests, AGENTS and roadmap contain closure gate wiring.
Gate: docs do not claim live evidence is closed.
- [x] Wiring and docs completed.

## TP-04 Validation And Delivery
Verify: targeted pytest, CLI smoke, ruff, format, secret scan, task docs validator, local-ci quick, git push.
Gate: clean pushed branch with no failing local validation.
- [x] Validation and delivery complete.

- [x] Contract file exists: `contracts/fate/audit/external-validation-closure.json`.
- [x] Script files exist: `scripts/external-validation-closure-gate.sh` and `.py`.
- [x] Each closure item has `owner`.
- [x] Each closure item has `credentialDependencies`.
- [x] Each closure item has `requiredEvidence`.
- [x] Each closure item has `verificationCommands`.
- [x] Each closure item has `closureCondition`.
- [x] Unknown occurrence becomes `manual_triage`.
- [x] Output has blocked ship gate while pending items exist.
- [x] Output redacts sensitive assignment markers.
- [x] local-ci runs closure gate after current audit bundle.
- [x] local-ci summary includes `externalValidationClosureGate`.
- [x] `scripts/AGENTS.md` documents the script.
- [x] `contracts/fate/audit/AGENTS.md` documents the contract.
- [x] `tests/AGENTS.md` documents the regression test.
- [x] Roadmap section 6.11 is present.
- [x] Targeted pytest passed.
- [x] CLI smoke passed.
- [x] Ruffle passed.
- [x] Format check passed.
- [x] Secret scan passed.
- [x] Task docs validator passed.
- [x] local-ci quick passed.
