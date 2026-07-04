# Task-Level Acceptance
Full 0138 acceptance requires all 22 work items to have accepted proof refs and accepted live proofs. Current package acceptance is partial: TP-01/TP-02 are complete, while TP-03 through TP-06 remain blocked by external execution requirements.

# Validation Plan
| Validation | Command / Evidence | Current Result |
| --- | --- | --- |
| Readiness matrix | `evidence/EXTERNAL_PROOF_LIVE_READINESS_MATRIX.json` | 22 work items, 22 tracker refs |
| Proof-ref gate current state | `/tmp/fatecat-local-ci-0137-closeout/external-validation-proof-ref-gate.json` | accepted 0, pending 22 |
| Live proof gate current state | `/tmp/fatecat-local-ci-0137-closeout/external-validation-live-proof-gate.json` | accepted 0, pending 22 |
| Secret/raw URL check | `rg ... governance/tasks/0138.../evidence` | No findings before docs fill |
| Task doc validation | `validate_task_docs.py --phase decompose` | Passed |
| Proof-ref gate current pending state | `bash scripts/external-validation-proof-ref-gate.sh --work-queue-json /tmp/fatecat-local-ci-0137-closeout/external-validation-closure-work-queue.json --output-json /tmp/fatecat-0138-proof-ref-gate.json` | Passed gate execution; `external_connectivity_pending`, accepted 0, pending 22 |
| Live proof gate current pending state | `bash scripts/external-validation-live-proof-gate.sh ... --output-json /tmp/fatecat-0138-live-proof-gate.json` | Passed gate execution; `external_connectivity_pending`, accepted 0, pending 22 |
| Secret scan | `bash scripts/secret-scan.sh --output-json /tmp/fatecat-secret-scan-0138.json` | Passed; findingCount 0 |
| Focused regression | `.venv/bin/python -m pytest -q tests/regression/test_external_validation_proof_ref_gate.py tests/regression/test_external_validation_live_proof_gate.py tests/regression/test_production_live_delivery_evidence_bundle.py tests/regression/test_measurement_infrastructure_certification.py tests/regression/test_external_validation_closure_evidence_summary.py` | Passed; 35 tests passed |

# Review Gate
- Confirm the task does not claim live proof completion.
- Confirm proof-ref and live proof execution remain distinct.
- Confirm evidence stores only redacted refs, hash values, credential names and pending reasons.

# Runtime Verification Gate
Future runtime verification commands after operator evidence arrives:

```bash
bash scripts/external-validation-proof-ref-gate.sh \
  --work-queue-json <work-queue-json> \
  --evidence-json <proof-ref-bundle-json> \
  --output-json <proof-ref-gate-json>

bash scripts/external-validation-live-proof-gate.sh \
  --work-queue-json <work-queue-json> \
  --proof-ref-gate-json <proof-ref-gate-json> \
  --category-runbooks-json <category-runbooks-json> \
  --live-evidence-json <live-evidence-bundle-json> \
  --output-json <live-proof-gate-json>
```

# Ship Readiness
- Current 0138 state: not ship-ready.
- `shipGate` must remain blocked until proof-ref, live proof, certification and third-party audit are accepted.

# Task Package Acceptance
| TP | Acceptance |
| --- | --- |
| TP-01 | Source artifacts and current commit are identified. |
| TP-02 | Matrix contains 22 work items and 22 tracker refs. |
| TP-03 | Blocked until proof-ref gate accepts 22 proof refs. |
| TP-04 | Blocked until live proof gate accepts 22 live proofs. |
| TP-05 | Blocked until closure/certification/audit consume accepted proof/live gates. |
| TP-06 | Blocked until final 100% claim criteria are proven. |

## TP-01 Current External Validation Input Chain

Acceptance: current local-ci artifacts and 0137 tracker evidence are identified and hashed.

## TP-02 Issue/Runbook/Proof-Ref Readiness Matrix

Acceptance: matrix maps every work item to issue ref, runbook and pending reason without raw URLs or secret values.

## TP-03 Execute Proof-Ref Runbooks

Acceptance: `external-validation-proof-ref-gate.sh` accepts all 22 proof refs.

## TP-04 Execute Live Proof Validation

Acceptance: `external-validation-live-proof-gate.sh` accepts all 22 live proofs.

## TP-05 Re-Run Closure/Certification/Audit Chain

Acceptance: closure evidence summary and certification are no longer blocked by missing proof/live evidence.

## TP-06 Ship-Readiness Claim Check

Acceptance: certification and independent third-party audit support any 100% claim.

# Anti-Goals
- 不得虚构证据
- 不得越权补全未确认信息
- 不得把 readiness matrix 写成 proof-ref accepted
- 不得把 tracker issue existence 写成 live proof accepted
