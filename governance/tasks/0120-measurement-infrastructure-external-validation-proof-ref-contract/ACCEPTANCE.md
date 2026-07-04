# Task-Level Acceptance

| Acceptance | Evidence |
| --- | --- |
| Proof-ref contract exists | `contracts/fate/audit/external-validation-proof-ref.json` |
| Proof-ref schema exists | `contracts/fate/audit/schemas/external-validation-proof-ref.schema.json` |
| Proof-ref gate exists | `scripts/external-validation-proof-ref-gate.py` |
| Wrapper exists | `scripts/external-validation-proof-ref-gate.sh` |
| local-ci writes artifact | `scripts/local-ci.sh` has `externalValidationProofRefGate` |
| Certification consumes proof-ref gate | `scripts/measurement-infrastructure-certification.py` audit domain requires `external-validation-proof-ref-gate.json` |
| Regression tests cover anti-forgery | `tests/regression/test_external_validation_proof_ref_gate.py` |
| No fake live | output `shipGate.status=blocked` even when all proof refs are schema accepted |

# Validation Plan

| Validation | Command | Expected |
| --- | --- | --- |
| Targeted pytest | `.venv/bin/python -m pytest -q tests/regression/test_external_validation_proof_ref_gate.py tests/regression/test_measurement_infrastructure_certification.py` | pass |
| Ruff check | `.venv/bin/python -m ruff check scripts/external-validation-proof-ref-gate.py tests/regression/test_external_validation_proof_ref_gate.py tests/regression/test_measurement_infrastructure_certification.py` | pass |
| Ruff format | `.venv/bin/python -m ruff format --check scripts/external-validation-proof-ref-gate.py tests/regression/test_external_validation_proof_ref_gate.py tests/regression/test_measurement_infrastructure_certification.py` | pass |
| Real gate chain | `bash scripts/external-validation-proof-ref-gate.sh --work-queue-json <latest external-validation-closure-work-queue.json> --output-json <tmp>` | pass with blocked ship gate |
| Secret scan | `bash scripts/secret-scan.sh --output-json <tmp>` | pass |
| Quick CI | `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-proof-ref-0120` | pass |

# Review Gate

- Proof-ref bundle cannot include raw URL, placeholder, local-only, dummy, token/secret/DSN/private-key markers.
- Proof-ref bundle must bind current commit, work queue hash and known occurrence IDs.
- Verification command must use approved local verifier command prefixes.
- Summary cannot copy verification command, secret values, raw URLs or report正文。
- Schema accepted cannot unlock production ship gate.

# Runtime Verification Gate

The gate is local-only. External live validation remains:

> 外部连通验证待执行

# Ship Readiness

Ship readiness requires local quick CI passed, clean task docs, a prepared commit package, and remote CI observation after push.

# Task Package Acceptance

## TP-01 Scope Confirmation

Verify: `rg -n "MI-100.A.02 proof-ref" docs/reference-materials/roadmap/测算基础设施100%实现计划.md`

Gate: scope stays at proof-ref contract/verifier.

## TP-02 Contract And Gate

Verify: `rg -n "external-validation-proof-ref" contracts scripts`

Gate: script keeps `shipGate.status=blocked`.

## TP-03 Regression And Local-CI

Verify: `.venv/bin/python -m pytest -q tests/regression/test_external_validation_proof_ref_gate.py tests/regression/test_measurement_infrastructure_certification.py`

Gate: pending, accepted bundle, raw URL rejection and wiring covered.

## TP-04 Validation

Verify: `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-proof-ref-0120`

Gate: quick CI passed and proof-ref output remains blocked without live evidence.

## TP-05 Delivery Package

Verify: `git status --short --branch`

Gate: remote CI result is not written into the repository before post-push observation.

# Anti-Goals

- Do not implement category live runbooks in this task.
- Do not connect external services.
- Do not save raw URL, secret, token, DSN or private key material.
- Do not claim 100% infrastructure completion.
