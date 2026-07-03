# Planning Summary

0117 follows 0116 directly. 0116 made all external pending occurrences actionable but left 184 of 390 items in manual triage. Manual triage at that size is not a usable audit closure plan. The correct next slice is to expand profiles for known infrastructure domains while preserving a real manual bucket for genuinely unknown items.

# Lifecycle Gates
不得跳过 gate；任一 gate 缺少命令、文件或明确豁免证据时，本任务不能 closeout。

| Gate | Exit Criteria | Status |
| --- | --- | --- |
| SPEC | Define profile expansion target and non-live boundary | Done |
| PLAN | Split into sample, classify, test, validate, ship | Done |
| BUILD | Add profiles and tests | Done |
| TEST | Targeted pytest, smoke, ruff/format, local-ci quick | Done |
| REVIEW | Check blocked semantics and manual preservation | Done |
| SHIP | Commit and push | Pending |

# Simplest Path
1. Sample manual triage paths/excerpts from 0116 artifact.
2. Add specific profiles before governance policy fallback.
3. Add governance policy guardrail profile for anti-overclaim text.
4. Keep a manual unknown test sample.
5. Validate and ship.

# Split Strategy
| Node | Split Reason |
| --- | --- |
| TP-01 | Understand remaining manual items before changing classifier. |
| TP-02 | Implement profile expansion in one script. |
| TP-03 | Prove behavior with regression and smoke. |
| TP-04 | Close docs and git delivery. |

# Execution Waves
| Wave | Leaves |
| --- | --- |
| W1 | TP-01 |
| W2 | TP-02 |
| W3 | TP-03 |
| W4 | TP-04 |

# Runtime Workflow Contract
- Allowed tools: `jq`, `rg`, `pytest`, `ruff`, `bash scripts/external-validation-closure-gate.sh`, `bash scripts/local-ci.sh`, `apply_patch`, `git`.
- Forbidden actions: production live validation, secret access, branch switch, rebase, reset.
- Evidence: before/after manual triage counts, targeted pytest, local-ci quick, secret scan, task docs validator.

# Next Executable Leaves
| Node ID | Action |
| --- | --- |
| - | No remaining executable leaves in this task package. |

# Dependency Graph
```text
TP-01 -> TP-02 -> TP-03 -> TP-04
```

# Rollback Protocol
- Revert profile additions in `scripts/external-validation-closure-gate.py`.
- Revert added test expectations.
- Remove 0117 roadmap and task index entry.

# Closeout Evidence
| Evidence | Result |
| --- | --- |
| Ruff | `.venv/bin/python -m ruff check scripts/external-validation-closure-gate.py tests/regression/test_external_validation_closure_gate.py` -> passed. |
| Format | `.venv/bin/python -m ruff format --check scripts/external-validation-closure-gate.py tests/regression/test_external_validation_closure_gate.py` -> passed. |
| Focused pytest | `.venv/bin/python -m pytest -q tests/regression/test_external_validation_closure_gate.py tests/regression/test_current_audit_bundle.py tests/regression/test_audit_handoff.py` -> 11 passed. |
| Closure smoke | `bash scripts/external-validation-closure-gate.sh --pending-external-json /tmp/fatecat-local-ci-external-validation-closure-0116/current-audit-bundle/pending-external-validations.json --output-json /tmp/fatecat-external-validation-closure-profile-expansion-0117.json` -> `status=passed`, `shipGate=blocked`, `total=390`, `manualTriage=1`, `categories=22`. |
| Secret scan | `bash scripts/secret-scan.sh --output-json /tmp/fatecat-secret-scan-0117.json` -> `findingCount=0`. |
| Task docs | `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0117-measurement-infrastructure-external-validation-closure-profile-expansion --phase decompose` -> passed. |
| Final quick CI | `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-post-0117-infra-plan-final` -> passed; 300 focused regression tests passed; current closure gate `total=402`, `manualTriage=1`, `shipGate=blocked`. |
