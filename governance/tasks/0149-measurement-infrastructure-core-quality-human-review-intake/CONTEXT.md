# Repo Evidence
| Evidence | Observation |
| --- | --- |
| Start branch/HEAD | `main...origin/main`, HEAD `9c58d385c5910dfe6aefd51bc3d9f3a2d8b8d561` |
| Previous task | `0148-measurement-infrastructure-100-post-0147-deep-research-plan` completed and remote Acceptance passed. |
| Existing quality corpus | `contracts/fate/evaluations/core-quality-corpus.json` already defines bazi/ziwei anonymous fixtures and rubric reference. |
| Existing rubric | `contracts/fate/evaluations/professional-quality-rubric.json` defines 8 dimensions and human review boundary, but had no machine intake gate. |
| Existing benchmark | `scripts/mingli-bench-gate.py` outputs aggregate-only MingLi-Bench baseline and no-leak boundary; it does not accept external expert benchmark results. |
| Existing certification | `scripts/measurement-infrastructure-certification.py` had `core_quality` domain, but did not require human review/external benchmark evidence. |
| New local slice | Added `core-quality-human-review-gate` contract/script/tests and wiring. |

# Constraints Matrix
| Constraint | Handling |
| --- | --- |
| Human/external evidence unavailable | Gate defaults to blocked, exits 0 for local-ci, and records pending statuses. |
| Privacy | Reject raw URL, secret-like assignments, benchmark question/answer/result fields and report body fields. |
| Current commit binding | Accepted bundle must match expected commit. |
| Rubric completeness | Accepted bundle must cover all professional rubric dimensions. |
| Benchmark boundary | Only aggregate benchmark evidence is accepted; per-question detail is forbidden. |
| Certification boundary | This gate can block `core_quality`; it cannot by itself certify 100% infrastructure. |

# Change Boundary
- Added:
  - `contracts/fate/evaluations/core-quality-human-review-gate.json`
  - `scripts/core-quality-human-review-gate.py`
  - `scripts/core-quality-human-review-gate.sh`
  - `tests/regression/test_core_quality_human_review_gate.py`
  - `governance/tasks/0149-measurement-infrastructure-core-quality-human-review-intake/*`
- Updated:
  - `contracts/fate/evaluations/registry.json`
  - `contracts/fate/evaluations/AGENTS.md`
  - `contracts/fate/audit/measurement-infrastructure-certification.json`
  - `scripts/measurement-infrastructure-certification.py`
  - `scripts/local-ci.sh`
  - `scripts/AGENTS.md`
  - `tests/AGENTS.md`
  - `tests/regression/test_measurement_infrastructure_certification.py`
  - `docs/reference-materials/roadmap/测算基础设施100%实现计划.md`
  - `governance/tasks/INDEX.md`

# Risk Matrix
| Risk | Impact | Mitigation |
| --- | --- | --- |
| Fake expert proof | False professional quality claim | Require artifact refs, sha256, commit binding and all rubric dimensions; default blocked. |
| Privacy leakage | Expert/user/benchmark details leak into repo | Reject raw URL, secret markers, question/answer/results and report body fragments. |
| Benchmark overclaim | Aggregate accuracy mistaken for 100% correctness | Non-claims and release boundary explicitly forbid professional ability / prediction accuracy 100%. |
| Certification bypass | Core quality passes without human evidence | certification core_quality domain now consumes `core-quality-human-review-gate.json`. |
| Local-ci breakage | Default pending gate could fail normal development | Script exits 0 when structure is valid but gate is blocked-as-expected. |

# Assumptions and Falsification
| Assumption | Falsifier |
| --- | --- |
| A structural intake gate is the correct next local step before real human review. | If a real expert evidence bundle is provided now, TP-04 can move from blocked to accepted using the new gate. |
| The gate must not store review bodies or benchmark rows. | Any accepted bundle containing forbidden fragments fails tests and gate validation. |
| Certification should treat missing human review as a core_quality blocker. | If product scope explicitly removes professional quality claim from 100% certification, this gate can be demoted from certification input through a separate ADR. |

# Critical Ambiguities
- Expert reviewer identity and trust process are external and not available in the repo.
- External benchmark corpus and accepted aggregate artifact are not yet provided.
- no-leak signoff artifact is not yet provided.
- These are real blockers for TP-04, not blockers for the local intake infrastructure.

# Debug Evidence Contract
- 调试模式: Optional
- This task is a feature/gate implementation, not a bugfix. If any gate/test fails after implementation, convert the failing command into DEBUG.md evidence.

# Task Package Context Map
| Node | Context |
| --- | --- |
| TP-01.01 | Existing core quality corpus, professional rubric, MingLi-Bench gate and certification domain. |
| TP-02.01 | Contract, Python gate and shell wrapper. |
| TP-02.02 | Negative validation for raw URL, sensitive assignment, commit mismatch and missing rubric dimension. |
| TP-03.01 | Evaluation registry, local-ci artifact summary and AGENTS wiring. |
| TP-03.02 | Certification domain and certification regression fixture. |
| TP-04.01 | Requires future expert rubric disposition bundle. |
| TP-04.02 | Requires future external benchmark aggregate and no-leak signoff. |
| TP-05.01 | JSON validation, pytest, local-ci and task docs validation. |
| TP-05.02 | Git commit, push and remote Acceptance. |
