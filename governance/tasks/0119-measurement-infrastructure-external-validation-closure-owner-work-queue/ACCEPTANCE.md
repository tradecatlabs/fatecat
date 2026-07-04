# Task-Level Acceptance

| Acceptance | Evidence |
| --- | --- |
| Work queue contract exists | `contracts/fate/audit/external-validation-closure-work-queue.json` |
| Work queue script exists | `scripts/external-validation-closure-work-queue.py` |
| Wrapper exists | `scripts/external-validation-closure-work-queue.sh` |
| local-ci writes artifact | `scripts/local-ci.sh` has `externalValidationClosureWorkQueue` |
| Regression tests pass | targeted pytest passes |
| No fake live | output `shipGate.status=blocked` when work items exist |

# Validation Plan

| Validation | Command | Expected |
| --- | --- | --- |
| Targeted pytest | `.venv/bin/python -m pytest -q tests/regression/test_external_validation_closure_gate.py tests/regression/test_external_validation_closure_work_queue.py` | pass |
| Ruff check | `.venv/bin/python -m ruff check scripts/external-validation-closure-work-queue.py tests/regression/test_external_validation_closure_work_queue.py` | pass |
| Ruff format | `.venv/bin/python -m ruff format --check scripts/external-validation-closure-work-queue.py tests/regression/test_external_validation_closure_work_queue.py` | pass |
| Real gate chain | `bash scripts/external-validation-closure-gate.sh ... && bash scripts/external-validation-closure-work-queue.sh ...` | pass with blocked ship gate |
| Quick CI | `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-closure-work-queue-0119-final` | pass |

Recent evidence:

- Targeted pytest: 10 passed.
- Secret scan: `status=passed`, `findingCount=0`.
- Real gate chain: 404 current quick-CI occurrences produce 22 work items; `shipGate.status=blocked`.
- Quick CI: `status=passed`; focused regression `305 passed`.

# Review Gate

- Work queue cannot include raw pending excerpt.
- Work queue cannot include token/secret/DSN assignment markers.
- Work queue cannot claim proofRef validated.
- Work queue cannot set closeConditionResult to passed.

# Runtime Verification Gate

The gate is local-only. External live validation remains:

> 外部连通验证待执行

# Ship Readiness

Ship readiness requires:

- local quick CI passed.
- commit and push performed after this task package is written.
- remote CI observed after push, or failure recorded in final delivery response.

# Task Package Acceptance

- Task docs validate with `validate_task_docs.py --phase closeout`.
- `governance/tasks/INDEX.md` includes task 0119.
- Roadmap includes post-0119 status and next step.

# Anti-Goals

- Do not implement proof-ref schema in this task.
- Do not create external dashboard or owner notification.
- Do not connect production systems.
- Do not claim FateCat is 100% infrastructure complete.
