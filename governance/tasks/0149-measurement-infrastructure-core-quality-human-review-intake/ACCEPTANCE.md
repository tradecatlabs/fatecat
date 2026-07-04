# Task-Level Acceptance
This task is accepted for the local infrastructure slice when:

- A machine-readable contract exists for core quality human review evidence.
- The gate defaults to blocked when no external evidence bundle is supplied.
- The gate accepts a redacted synthetic bundle in tests and rejects raw URL, sensitive assignments, commit mismatch and missing rubric dimensions.
- The gate is wired into evaluation registry, local-ci summary and certification core_quality domain.
- Documentation records that actual expert review and external benchmark evidence remain blocked.
- Tests and task docs validation pass.

The full 0149 external evidence objective remains blocked until a real redacted expert/benchmark/no-leak bundle is supplied and accepted.

# Validation Plan
| Validation | Command | Expected |
| --- | --- | --- |
| JSON syntax | `python3 -m json.tool contracts/fate/evaluations/core-quality-human-review-gate.json` | valid JSON |
| Gate default pending | `bash scripts/core-quality-human-review-gate.sh --output-json /tmp/core-quality-human-review-gate.json` | exit 0, gate blocked-as-expected |
| Focused tests | `PYTHONPATH=domains/fate-analysis/services/fate-core/src python3 -m pytest -q tests/regression/test_core_quality_human_review_gate.py tests/regression/test_measurement_infrastructure_certification.py` | passed |
| Task docs | `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0149-measurement-infrastructure-core-quality-human-review-intake --phase decompose` | `ok: true` |
| Quick local CI | `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0149-final` | passed |
| Remote Acceptance | `gh run view 28717205411 --json headSha,status,conclusion,url` | success for `6e99cf24bb086d0ee73418feea0a3e21bf48cd9c` |

# Review Gate
- PASS if local intake infrastructure is complete and external evidence remains honestly blocked.
- WARN if accepted synthetic bundle tests are mistaken for real expert review.
- BLOCK if any code path stores reviewer identity, real case data, question/answer/result fields or report body.

# Runtime Verification Gate
Runtime external verification is out of scope. Correct local runtime state:

```text
coreQualityHumanReviewGate.status = passed
coreQualityHumanReviewGate.humanReviewGate.status = blocked
certification.core_quality = blocked until accepted external bundle exists
```

# Ship Readiness
The local infrastructure slice can ship after validation, commit, push and remote Acceptance. The complete 0149 evidence closure cannot ship until TP-04.01 and TP-04.02 are accepted.

# Task Package Acceptance
| Node | Acceptance |
| --- | --- |
| TP-01.01 | Existing quality gates inspected and missing intake gate identified. |
| TP-02.01 | Contract, Python gate and shell wrapper added. |
| TP-02.02 | Negative tests cover raw URL, sensitive assignment, commit mismatch and missing dimension. |
| TP-03.01 | Registry, local-ci and AGENTS mention new gate. |
| TP-03.02 | Certification requires `core-quality-human-review-gate.json`. |
| TP-04.01 | Remains blocked until real expert disposition bundle exists. |
| TP-04.02 | Remains blocked until external benchmark aggregate and no-leak signoff exist. |
| TP-05.01 | Local validation passes. |
| TP-05.02 | Commit `6e99cf2` pushed and remote Acceptance `28717205411` completed successfully. |

# Anti-Goals
- 不得伪造专家评审或外部 benchmark。
- 不得把 synthetic test bundle 写成真实 accepted evidence。
- 不得保存敏感信息、真实用户数据、benchmark 明细或报告正文。
