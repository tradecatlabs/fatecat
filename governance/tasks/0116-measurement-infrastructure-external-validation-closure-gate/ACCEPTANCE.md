# Acceptance

# Task-Level Acceptance

## Acceptance Criteria
- Contract exists and requires owner, credential dependencies, required evidence, verification commands and closure condition.
- Gate accepts current audit bundle pending external JSON and writes `kind=fatecat.external_validation_closure_plan`.
- Gate keeps `shipGate.status=blocked` when pending items exist.
- Gate never writes sensitive assignment markers or real secret values.
- Unknown items are retained as `manual_triage`.
- local-ci runs closure gate after current audit bundle and records artifact in summary JSON.
- Tests, docs and task index are synchronized.

# Validation Plan
| Check | Command | Expected |
| --- | --- | --- |
| Targeted pytest | `.venv/bin/python -m pytest -q tests/regression/test_external_validation_closure_gate.py tests/regression/test_current_audit_bundle.py tests/regression/test_audit_handoff.py` | pass |
| Closure smoke | `bash scripts/external-validation-closure-gate.sh --pending-external-json /tmp/fatecat-current-audit-bundle-finalizer-0115/pending-external-validations.json --output-json /tmp/fatecat-external-validation-closure-0116.json` | `status=passed`, `shipGate=blocked` |
| Ruffle | `.venv/bin/python -m ruff check scripts/external-validation-closure-gate.py tests/regression/test_external_validation_closure_gate.py` | pass |
| Format | `.venv/bin/python -m ruff format --check scripts/external-validation-closure-gate.py tests/regression/test_external_validation_closure_gate.py` | pass |
| Secret scan | `bash scripts/secret-scan.sh --output-json /tmp/fatecat-secret-scan-0116.json` | pass |
| Task docs | `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0116-measurement-infrastructure-external-validation-closure-gate --phase decompose` | pass |
| Quick CI | `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-external-validation-closure-0116` | pass |

## Evidence
| Check | Result |
| --- | --- |
| Targeted pytest | `11 passed in 10.00s` |
| Closure smoke | `status=passed`, `shipGate=blocked`, `total=383`, `manualTriage=179` on finalizer 0115 input |
| Secret scan | `status=passed`, `findingCount=0` |
| Task docs validator | `ok=true` for decompose before closeout |
| Quick CI | `300 passed in 150.62s`, output `/tmp/fatecat-local-ci-external-validation-closure-0116` |
| local-ci closure artifact | `status=passed`, `shipGate=blocked`, `total=390`, `manualTriage=184` |

# Review Gate
- Confirm closure plan does not claim external live passed.
- Confirm manual triage preserves unknown items.
- Confirm audit handoff can run while 0116 files are untracked or tracked.

# Runtime Verification Gate
- Closure CLI smoke must run on latest available finalizer pending external JSON.
- local-ci quick must produce `external-validation-closure-gate.json`.

# Ship Readiness
- Worktree must be committed and pushed after validation.
- Remote CI evidence should be checked after push when available.

# Task Package Acceptance
- Task docs validator must pass for phase `decompose`.
- Checklist and status must be updated to Done only after evidence exists.

# Anti-Goals
- This task does not prove production API, HF Space, Telegram Bot, Postgres, OIDC, SIEM, OTel, Vault/KMS, developer portal or third-party audit live connectivity.
- This task does not reduce pending external validation count.
- This task does not make FateCat 100% production infrastructure.
