# Task-Level Acceptance

| Acceptance | Evidence |
| --- | --- |
| Category runbook contract exists | `contracts/fate/audit/external-validation-category-runbooks.json` |
| Category runbook gate exists | `scripts/external-validation-category-runbooks.py` |
| Wrapper exists | `scripts/external-validation-category-runbooks.sh` |
| local-ci writes artifact | `scripts/local-ci.sh` has `externalValidationCategoryRunbooks` |
| Certification consumes runbooks | `scripts/measurement-infrastructure-certification.py` audit domain requires `external-validation-category-runbooks.json` |
| Regression tests cover category coverage | `tests/regression/test_external_validation_category_runbooks.py` |
| No fake live | output `shipGate.status=blocked` when runbooks exist |

# Validation Plan

| Validation | Command | Expected |
| --- | --- | --- |
| Targeted pytest | `.venv/bin/python -m pytest -q tests/regression/test_external_validation_category_runbooks.py tests/regression/test_measurement_infrastructure_certification.py` | pass |
| Ruff check | `.venv/bin/python -m ruff check scripts/external-validation-category-runbooks.py tests/regression/test_external_validation_category_runbooks.py tests/regression/test_measurement_infrastructure_certification.py` | pass |
| Ruff format | `.venv/bin/python -m ruff format --check scripts/external-validation-category-runbooks.py tests/regression/test_external_validation_category_runbooks.py tests/regression/test_measurement_infrastructure_certification.py` | pass |
| Real gate chain | `bash scripts/external-validation-category-runbooks.sh --work-queue-json <latest external-validation-closure-work-queue.json> --output-json <tmp>` | pass with blocked ship gate |
| Secret scan | `bash scripts/secret-scan.sh --output-json <tmp>` | pass |
| Quick CI | `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-category-runbooks-0121` | pass |

# Review Gate

- Unknown category must fail.
- Runbook output cannot include raw URL, token/secret/DSN/private-key markers.
- Runbook must include required credential, operator command, proof-ref pattern, redaction, expiry, rollback and closure condition.
- Runbook ready cannot unlock production ship gate.

# Runtime Verification Gate

The gate is local-only. External live validation remains:

> 外部连通验证待执行

# Ship Readiness

Ship readiness requires local quick CI passed, clean task docs, a prepared commit package, and remote CI observation after push.

# Task Package Acceptance

## TP-01 Scope Confirmation

Verify: `rg -n "MI-100.A.03 external validation runbook per category" docs/reference-materials/roadmap/测算基础设施100%实现计划.md`

Gate: scope stays at category runbook contract/generator.

## TP-02 Contract And Gate

Verify: `rg -n "external-validation-category-runbooks" contracts scripts`

Gate: script keeps `shipGate.status=blocked`.

## TP-03 Regression And Local-CI

Verify: `.venv/bin/python -m pytest -q tests/regression/test_external_validation_category_runbooks.py tests/regression/test_measurement_infrastructure_certification.py`

Gate: category coverage, unknown category, privacy and wiring covered.

## TP-04 Validation

Verify: `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-category-runbooks-0121`

Gate: quick CI passed and certification remains blocked without live evidence.

## TP-05 Delivery Package

Verify: `git status --short --branch`

Gate: remote CI result is not written into the repository before post-push observation.

# Anti-Goals

- Do not implement stale owner alert in this task.
- Do not connect external services.
- Do not save raw URL, secret, token, DSN or private key material.
- Do not claim 100% infrastructure completion.
