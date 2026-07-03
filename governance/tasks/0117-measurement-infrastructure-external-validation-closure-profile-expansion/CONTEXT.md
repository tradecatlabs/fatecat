# Repo Evidence
- 调试模式: `Optional`

| Evidence | Result |
| --- | --- |
| Current branch | `main` at `55741be` before 0117 edits. |
| 0116 closure artifact | `/tmp/fatecat-local-ci-external-validation-closure-0116/external-validation-closure-gate.json` reported `total=390`, `manualTriage=184`. |
| 0117 first smoke | `/tmp/fatecat-external-validation-closure-profile-expansion-0117.json` reported `manualTriage=1` after profile expansion. |

# Constraints Matrix
| Constraint | Handling |
| --- | --- |
| No external credentials | Only local classification logic changes. |
| No live overclaim | `shipGate.status` remains blocked when pending items exist. |
| Preserve unknowns | Test fixture keeps one unknown item and expects `manual_triage`. |
| Current branch only | No branch switch or destructive git. |

# Change Boundary
| In Boundary | Out of Boundary |
| --- | --- |
| closure profile categories and tests | production live smoke |
| roadmap/task docs | secret handling or external account setup |

# Risk Matrix
| Risk | Impact | Mitigation |
| --- | --- | --- |
| Over-broad keyword misclassifies unrelated item | Audit routing noise | Targeted test caught broad `registry`; replaced with narrower release keywords. |
| Manual triage hidden entirely | Unknowns lost | Regression test keeps unknown sample. |
| Policy marker seen as live item | False ownership | Dedicated governance policy guardrail category. |

# Assumptions and Falsification
| Assumption | Falsifier |
| --- | --- |
| 0116 manual triage mostly policy and known infra domains. | Sample shows actual unknown external systems not covered. |
| Keyword profiles are sufficient for closure plan routing. | Auditor requires explicit registry-driven classifier. |

# Critical Ambiguities
- `governance.external_validation_policy_guardrail` is not a live task; it means the pending phrase itself is a required anti-overclaim marker.

# Debug Evidence Contract
- If classification regression fails, include failing category, excerpt and target profile.
- Do not include secret values, full report text or production logs.

# Task Package Context Map
| File | Reason |
| --- | --- |
| `scripts/external-validation-closure-gate.py` | classifier source. |
| `tests/regression/test_external_validation_closure_gate.py` | classifier regression. |
| `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` | roadmap source of truth. |
