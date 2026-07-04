# Task-Level Acceptance

Accepted when all of the following are true:

- `contracts/fate/audit/independent-audit-result.json` declares input/output/non-claim/privacy boundaries.
- `scripts/independent-audit-result-gate.py` can output pending by default and accept a valid redacted signed result bundle.
- Invalid raw URL, sensitive assignment, placeholder proof and commit mismatch are rejected.
- `scripts/third-party-audit-rehearsal.py` consumes independent audit result gate and no longer hardcodes the independent result checklist item.
- `scripts/local-ci.sh --profile quick` generates `independent-audit-result-gate.json` and passes it into third-party audit rehearsal.
- Regression and quick local-ci pass.

# Validation Plan
| Validation | Command / Evidence | Expected |
| --- | --- | --- |
| Focused regression | `.venv/bin/python -m pytest -q tests/regression/test_independent_audit_result_gate.py tests/regression/test_third_party_audit_rehearsal.py` | 13 tests pass. |
| Gate smoke | `bash scripts/independent-audit-result-gate.sh --output-json /tmp/fatecat-independent-audit-result-gate-0140.json` | Pending/blocked gate output. |
| Local quick CI | `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0140` | quick profile passes. |
| Secret boundary | local-ci secret scan | findingCount 0. |

# Validation Results
| Validation | Command / Evidence | Result |
| --- | --- | --- |
| Focused regression | `.venv/bin/python -m pytest -q tests/regression/test_independent_audit_result_gate.py tests/regression/test_third_party_audit_rehearsal.py` | Passed, 13 tests. |
| Gate smoke | `bash scripts/independent-audit-result-gate.sh --output-json /tmp/fatecat-independent-audit-result-gate-0140.json` | Passed; pending/blocked output. |
| Local quick CI | `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0140` | Passed; 388 tests. |
| Pending gate artifact | `evidence/INDEPENDENT_AUDIT_RESULT_GATE_PENDING.json` | `status=external_audit_result_pending`, `auditResultGate.status=blocked`. |
| Rehearsal artifact | `evidence/THIRD_PARTY_AUDIT_REHEARSAL_WITH_INDEPENDENT_GATE.json` | `evidenceInputs=9`, `rehearsalGate.status=blocked`. |

# Review Gate
- Review should verify that accepted independent audit result intake does not change `shipGate.status=blocked`.
- Review should verify no raw URL, token, secret, DSN, webhook secret, production log, report body or user input is stored.
- Review should verify AGENTS/roadmap/index are synchronized with the new contract and script.

# Runtime Verification Gate
- Runtime live checks were not executed in this task.
- `shipGate` remains blocked by design.
- `外部连通验证待执行` remains for real third-party audit result and production live proof.

# Ship Readiness
- Local control-plane slice is shippable after tests and CI.
- Production 100% is not shippable from this task alone.
- Remaining ship blockers are real proof-ref, live proof, independent audit execution and final certification.

# Task Package Acceptance
| TP | Acceptance |
| --- | --- |
| TP-01 | Rehearsal gap identified and documented. |
| TP-02 | Contract/gate implemented and tested. |
| TP-03 | Rehearsal/local-ci consume gate output. |
| TP-04 | Regression/docs/local-ci passed. |
| TP-05 | Evidence copied and task docs validate. |

# Anti-Goals
- 不伪造审计结果。
- 不绕过 certification。
- 不把 accepted intake 写成 production ready。
