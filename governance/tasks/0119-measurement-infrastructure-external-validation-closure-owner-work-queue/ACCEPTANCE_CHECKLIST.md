# Acceptance Checklist

# Global Standards

- [x] Scope is limited to external validation closure owner work queue.
- [x] No production token, secret, DSN, private key or external account data is required.
- [x] Work queue is a blocked local control-plane artifact, not live proof.
- [x] No retired path fallback is introduced.

# Task Package Checklists

## TP-01 SPEC

- [x] Verify: `rg -n "MI-100.A.01 closure owner work queue" docs/reference-materials/roadmap/测算基础设施100%实现计划.md`
- [x] Gate: roadmap/source contract confirms next local slice.

## TP-02 BUILD

- [x] Verify: `rg -n "external-validation-closure-work-queue" contracts scripts`
- [x] Gate: contract/script/wrapper/local-ci wiring exists.

## TP-03 TEST

- [x] Verify: `.venv/bin/python -m pytest -q tests/regression/test_external_validation_closure_gate.py tests/regression/test_external_validation_closure_work_queue.py`
- [x] Gate: targeted regression passes.

## TP-04 LOCAL GATES

- [x] Verify: `bash scripts/external-validation-closure-work-queue.sh --closure-plan-json /tmp/fatecat-closure-gate-0119.json --output-json /tmp/fatecat-closure-work-queue-0119.json`
- [x] Verify: `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-closure-work-queue-0119-final`
- [x] Gate: quick CI includes work queue artifact and remains blocked only for external live/certification non-claims.

## TP-05 SHIP

- [x] Verify: `git status --short --branch`
- [x] Gate: local ship package ready; remote CI observation happens after commit/push and is not prewritten into repo docs.
