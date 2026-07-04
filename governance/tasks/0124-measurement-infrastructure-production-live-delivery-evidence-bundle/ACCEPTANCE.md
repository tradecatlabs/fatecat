# Task-Level Acceptance

| Requirement | Evidence |
| --- | --- |
| Contract exists | `contracts/fate/audit/production-live-delivery-evidence-bundle.json` |
| CLI assembler exists | `scripts/production-live-delivery-evidence-bundle.py` and `.sh` |
| Pending mode safe | No live summary produces `external_connectivity_pending` and no live proofs |
| Live fixture accepted | Regression proves five delivery categories emit live proofs and chain through 0123 live proof gate |
| Sensitive input rejected | Regression rejects `token=` marker in input summary |
| Output no raw URL | Regression confirms raw URL in input live-release-gate is not copied to bundle |
| local-ci wired | `scripts/local-ci.sh` generates bundle and passes it to live proof gate |
| Bot runbook executable | Telegram category uses `live-release-gate.sh --run-live-bot --output-json` |

# Validation Plan

```bash
.venv/bin/python -m pytest -q tests/regression/test_production_live_delivery_evidence_bundle.py tests/regression/test_external_validation_live_proof_gate.py tests/regression/test_external_validation_category_runbooks.py
.venv/bin/python -m ruff check scripts/production-live-delivery-evidence-bundle.py tests/regression/test_production_live_delivery_evidence_bundle.py scripts/external-validation-category-runbooks.py
.venv/bin/python -m ruff format --check scripts/production-live-delivery-evidence-bundle.py tests/regression/test_production_live_delivery_evidence_bundle.py scripts/external-validation-category-runbooks.py
bash scripts/secret-scan.sh --output-json /tmp/fatecat-secret-scan-production-live-delivery-0124.json
bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-production-live-delivery-0124
```

# Review Gate

- No output JSON may contain raw `http://` / `https://` URL.
- No output JSON may contain token/secret/password/DSN/private key markers.
- No local-contract, dry-run or pending summary may become live proof.
- `delivery.multi_surface_live` requires both multi-surface semantic diff passed and API/HF/Bot live checks passed.

# Runtime Verification Gate

No long-running runtime is introduced. The shell wrapper must use repo `.venv/bin/python` or `python3` fallback and write deterministic JSON to explicit output paths.

# Ship Readiness

Ready only when targeted tests, ruff, secret scan, real artifact chain, quick local CI, commit, push and remote CI observation complete.

# Task Package Acceptance

## TP-01 Scope Confirmation

Accepted when `MI-100.B` categories are confirmed and no real credentials are required for this local slice.

## TP-02 Contract Script Wrapper

Accepted when contract/script/wrapper exist and tests cover pending/live/rejected paths.

## TP-03 Wiring

Accepted when local-ci, live proof gate, AGENTS and roadmap reference the assembler.

## TP-04 Validation

Accepted when local gates pass and generated evidence remains blocked without real summaries.

## TP-05 Delivery

Accepted when commit is pushed and remote CI result is recorded.

# Anti-Goals

- Do not execute real production API/HF/Bot/Postgres/webhook calls in this task.
- Do not save real endpoint URLs, credentials, DSNs, logs or report body.
- Do not claim third-party audit or 100% measurement infrastructure completion.
