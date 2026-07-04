# Task-Level Acceptance

| Requirement | Evidence |
| --- | --- |
| Contract/schema exists | `contracts/fate/audit/external-validation-live-proof-gate.json` and `contracts/fate/audit/schemas/external-validation-live-evidence.schema.json` |
| CLI gate exists | `scripts/external-validation-live-proof-gate.py` and `.sh` |
| No live evidence mode stays blocked | Gate summary has `liveProofStatus=external_connectivity_pending` and `shipGate.status=blocked` |
| Redacted live evidence fixture accepted | Regression test proves `live_gate_accepted_all_work_items` for bound fixture |
| Fake/unbound evidence rejected | Regression tests reject missing proof-ref, raw URL and placeholder |
| Certification sees live proof status | `measurement-infrastructure-certification.py` audit domain requires `external-validation-live-proof-gate.json` |
| Trend dashboard consumes live proof | Regression test proves category live pending count drops for accepted live proof |
| Local CI includes artifact | `scripts/local-ci.sh` generates and records `external-validation-live-proof-gate.json` |

# Validation Plan

```bash
.venv/bin/python -m pytest -q tests/regression/test_external_validation_live_proof_gate.py tests/regression/test_external_validation_closure_trend_dashboard.py tests/regression/test_measurement_infrastructure_certification.py
.venv/bin/python -m ruff check scripts/external-validation-live-proof-gate.py tests/regression/test_external_validation_live_proof_gate.py scripts/external-validation-closure-trend-dashboard.py tests/regression/test_external_validation_closure_trend_dashboard.py scripts/measurement-infrastructure-certification.py tests/regression/test_measurement_infrastructure_certification.py
.venv/bin/python -m ruff format --check scripts/external-validation-live-proof-gate.py tests/regression/test_external_validation_live_proof_gate.py scripts/external-validation-closure-trend-dashboard.py tests/regression/test_external_validation_closure_trend_dashboard.py scripts/measurement-infrastructure-certification.py tests/regression/test_measurement_infrastructure_certification.py
bash scripts/secret-scan.sh --output-json /tmp/fatecat-secret-scan-live-proof-gate-0123.json
bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-external-validation-live-proof-gate-0123
```

# Review Gate

- No code path may convert proof-ref schema accepted directly into category live passed.
- Summary must not contain raw URL, token/secret/DSN/private key markers, production logs or report body.
- Even full live proof acceptance must not set 100% certification passed by itself.

# Runtime Verification Gate

No long-running runtime is introduced. The shell wrapper must run with repo `.venv/bin/python` or `python3` fallback and produce deterministic JSON output under explicit paths.

# Ship Readiness

Ready only when targeted tests, ruff, secret scan, real artifact chain, quick local CI, commit, push and remote CI observation complete.

# Task Package Acceptance

## TP-01 Scope And Upstream Artifact Confirmation

Accepted when task is anchored to MI-100.A.05 and does not depend on real credentials.

## TP-02 Contract Schema Script Wrapper

Accepted when contract/schema/script/wrapper exist and targeted tests prove pending/accepted/rejected paths.

## TP-03 Wiring

Accepted when local-ci, certification, closure trend dashboard, AGENTS and roadmap reference the new gate.

## TP-04 Validation

Accepted when local gates pass and generated evidence remains blocked rather than over-claiming.

## TP-05 Delivery

Accepted when commit is pushed and remote CI results are recorded.

# Anti-Goals

- Do not execute real production API/HF/Bot/Postgres/OIDC/SIEM/OTel/Vault/KMS calls in this task.
- Do not save real endpoint URLs, credentials, DSNs, logs or report body.
- Do not claim third-party audit or 100% measurement infrastructure completion.
