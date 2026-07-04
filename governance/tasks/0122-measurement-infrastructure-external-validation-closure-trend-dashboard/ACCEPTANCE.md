# Task-Level Acceptance

| Acceptance | Evidence |
| --- | --- |
| Closure trend dashboard contract exists | `contracts/fate/audit/external-validation-closure-trend-dashboard.json` |
| Closure trend dashboard gate exists | `scripts/external-validation-closure-trend-dashboard.py` |
| Wrapper exists | `scripts/external-validation-closure-trend-dashboard.sh` |
| local-ci writes artifact | `scripts/local-ci.sh` has `externalValidationClosureTrendDashboard` |
| Certification consumes dashboard | `scripts/measurement-infrastructure-certification.py` audit domain requires `external-validation-closure-trend-dashboard.json` |
| Regression tests cover dashboard | `tests/regression/test_external_validation_closure_trend_dashboard.py` |
| No fake live | output `alertGate.status=blocked` and `shipGate.status=blocked` when alerts exist |

# Validation Plan

| Validation | Command | Expected |
| --- | --- | --- |
| Targeted pytest | `.venv/bin/python -m pytest -q tests/regression/test_external_validation_closure_trend_dashboard.py tests/regression/test_measurement_infrastructure_certification.py` | pass |
| Ruff check | `.venv/bin/python -m ruff check scripts/external-validation-closure-trend-dashboard.py tests/regression/test_external_validation_closure_trend_dashboard.py tests/regression/test_measurement_infrastructure_certification.py scripts/measurement-infrastructure-certification.py` | pass |
| Ruff format | `.venv/bin/python -m ruff format --check scripts/external-validation-closure-trend-dashboard.py tests/regression/test_external_validation_closure_trend_dashboard.py tests/regression/test_measurement_infrastructure_certification.py scripts/measurement-infrastructure-certification.py` | pass |
| Real gate chain | `bash scripts/external-validation-closure-trend-dashboard.sh --closure-plan-json <closure> --work-queue-json <queue> --proof-ref-gate-json <proof> --category-runbooks-json <runbooks> --output-json <tmp>` | pass with blocked ship gate |
| Secret scan | `bash scripts/secret-scan.sh --output-json <tmp>` | pass |
| Quick CI | `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-closure-trend-dashboard-0122` | pass |

# Review Gate

- Dashboard must fail if a work item category has no runbook.
- Dashboard output cannot include raw URL, token/secret/DSN/private-key markers.
- Dashboard must include owner/category/status aggregation.
- Alert ready cannot unlock production ship gate.
- Alert delivery mode must remain `local_dry_run_only`.

# Runtime Verification Gate

The gate is local-only. External live validation remains:

> 外部连通验证待执行

# Ship Readiness

Ship readiness requires local quick CI passed, clean task docs, a prepared commit package, and remote CI observation after push.

# Task Package Acceptance

## TP-01 Scope Confirmation

Verify: `rg -n "MI-100.A.04 closure trend dashboard and stale owner alert" docs/reference-materials/roadmap/测算基础设施100%实现计划.md`

Gate: scope stays at local dashboard/stale alert summary.

## TP-02 Contract And Gate

Verify: `rg -n "external-validation-closure-trend-dashboard" contracts scripts`

Gate: script keeps `alertGate.status=blocked` and `shipGate.status=blocked` when alerts exist.

## TP-03 Regression And Local-CI

Verify: `.venv/bin/python -m pytest -q tests/regression/test_external_validation_closure_trend_dashboard.py tests/regression/test_measurement_infrastructure_certification.py`

Gate: owner/category/status aggregation, missing runbook rejection, privacy and wiring covered.

## TP-04 Validation

Verify: `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-closure-trend-dashboard-0122`

Gate: quick CI passed and certification remains blocked without live evidence.

## TP-05 Delivery Package

Verify: `git status --short --branch`

Gate: remote CI result is not written into the repository before post-push observation.

# Anti-Goals

- Do not implement real notification sending in this task.
- Do not connect external services.
- Do not save raw URL, secret, token, DSN or private key material.
- Do not claim 100% infrastructure completion.
