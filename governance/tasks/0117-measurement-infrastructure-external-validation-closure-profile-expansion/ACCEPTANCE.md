# Task-Level Acceptance
- Closure gate on 0116 local-ci pending list reduces manual triage from 184 to 1.
- `manual_triage` still exists for the explicit unknown fixture.
- `shipGate.status` remains `blocked`.
- New categories have owner and evidence commands through the same `ClosureProfile` structure.
- Tests and local validation pass.

# Validation Plan
| Check | Command | Expected |
| --- | --- | --- |
| Targeted pytest | `.venv/bin/python -m pytest -q tests/regression/test_external_validation_closure_gate.py` | pass |
| Closure smoke | `bash scripts/external-validation-closure-gate.sh --pending-external-json /tmp/fatecat-local-ci-external-validation-closure-0116/current-audit-bundle/pending-external-validations.json --output-json /tmp/fatecat-external-validation-closure-profile-expansion-0117.json` | `manualTriage=1`, `shipGate=blocked` |
| Ruffle | `.venv/bin/python -m ruff check scripts/external-validation-closure-gate.py tests/regression/test_external_validation_closure_gate.py` | pass |
| Format | `.venv/bin/python -m ruff format --check scripts/external-validation-closure-gate.py tests/regression/test_external_validation_closure_gate.py` | pass |
| Secret scan | `bash scripts/secret-scan.sh --output-json /tmp/fatecat-secret-scan-0117.json` | pass |
| Task docs | `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0117-measurement-infrastructure-external-validation-closure-profile-expansion --phase decompose` | pass |
| Quick CI | `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-post-0117-infra-plan-final` | passed; 300 focused regression tests passed |

# Review Gate
- Confirm broad keywords do not capture evaluation/provider/release incorrectly.
- Confirm governance policy guardrail is not treated as live evidence.

# Runtime Verification Gate
- Closure smoke must run on a real current-audit-bundle pending list.

# Ship Readiness
- Worktree clean after commit.
- Push current branch.

# Task Package Acceptance
- Task docs validator passes closeout after final index/roadmap updates.

# Anti-Goals
- No external connectivity closure.
- No production readiness claim.
- No real credential use.
