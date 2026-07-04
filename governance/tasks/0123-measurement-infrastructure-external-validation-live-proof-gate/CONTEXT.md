# Repo Evidence

- Current branch before work: `main...origin/main`.
- Previous completed slice: `0122-measurement-infrastructure-external-validation-closure-trend-dashboard`.
- Related upstream artifacts: `external-validation-closure-work-queue.json`, `external-validation-proof-ref-gate.json`, `external-validation-category-runbooks.json`, `external-validation-closure-trend-dashboard.json`.
- Related scripts before this task: `scripts/external-validation-proof-ref-gate.py`, `scripts/external-validation-category-runbooks.py`, `scripts/external-validation-closure-trend-dashboard.py`, `scripts/measurement-infrastructure-certification.py`.
- First targeted regression evidence: 25 tests passed for live proof gate, closure trend dashboard and certification.

# Constraints Matrix

| Constraint | Decision |
| --- | --- |
| No real external credential in repo | Only redacted evidence handles, hashes and command hashes are stored |
| No over-claim | No live evidence keeps `external_connectivity_pending`; accepted live proof still leaves audit/certification review blocked |
| Current capability goal | This is infrastructure evidence plumbing, not a new divination capability |
| Local CI compatibility | New gate must run without external environment |

# Change Boundary

In scope files are limited to audit contracts/schema, local scripts, regression tests, local-ci/certification wiring, AGENTS docs, roadmap and this task package. No production API behavior, provider algorithm, report renderer or user-facing report text is changed.

# Risk Matrix

| Risk | Mitigation |
| --- | --- |
| Proof-ref accepted is mistaken for live passed | Separate live proof gate and explicit non-claims |
| Operator evidence leaks endpoint or secret | Raw URL and sensitive marker rejection |
| Future live proof cannot close trend dashboard | Optional live proof input reduces category live pending count |
| Certification misses new gate | Audit domain required evidence includes `external-validation-live-proof-gate.json` |

# Assumptions and Falsification

- Assumption: live evidence should be represented as a redacted JSON bundle, not as raw production logs. Falsifier: a future external auditor requires original logs; then the original logs must stay outside Git and only their redacted proofRef/hash enters this repo.
- Assumption: work item, proof-ref and runbook are the correct binding points. Falsifier: a new closure model groups by a different external resource; then the gate must be extended without weakening current binding checks.

# Critical Ambiguities

No implementation-blocking ambiguity remains. Real credentials and endpoints are still unavailable, but this task only builds the intake and verification layer for future live evidence.

# Debug Evidence Contract

- 调试模式: `Optional`
- No runtime defect is being fixed. Any failure in this task must produce command output, rejected fixture and regression evidence before closeout.

# Task Package Context Map

## TP-01 Scope And Upstream Artifact Confirmation

Confirms 0123 is the `MI-100.A.05` bridge after proof-ref/category runbook/trend dashboard and before production live delivery.

## TP-02 Contract Schema Script Wrapper

Adds live proof contract, live evidence schema, Python gate and shell wrapper.

## TP-03 Wiring

Connects local-ci, certification, closure trend dashboard, AGENTS docs and roadmap.

## TP-04 Validation

Runs ruff, targeted pytest, secret scan, real artifact chain and quick CI.

## TP-05 Delivery

Commits, pushes and observes remote CI.
