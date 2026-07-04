# Task-Level Acceptance

- `external-validation-issue-export.py` consumes the four required JSON artifacts and validates their `kind`.
- Output JSON has `kind=fatecat.external_validation_issue_export` and required fields.
- Output Markdown has tracker-readable issue index and issue bodies.
- `status=operator_action_required` may indicate package generation success, but `issueGate.status` must remain `blocked` while pending work items, issue creation, live evidence or independent audit result are missing.
- Raw URL, token, secret, DSN and private key markers are rejected from output.
- `local-ci.sh --profile quick` generates JSON and Markdown artifacts after closure evidence summary.

# Validation Plan

| Gate | Command | Expected |
| --- | --- | --- |
| Syntax | `.venv/bin/python -m py_compile scripts/external-validation-issue-export.py` | pass |
| Focused pytest | `.venv/bin/python -m pytest -q tests/regression/test_external_validation_issue_export.py` | pass |
| Ruff | `.venv/bin/python -m ruff check scripts/external-validation-issue-export.py tests/regression/test_external_validation_issue_export.py` | pass |
| Format | `.venv/bin/python -m ruff format --check scripts/external-validation-issue-export.py tests/regression/test_external_validation_issue_export.py` | pass |
| Secret scan | `bash scripts/secret-scan.sh --output-json /tmp/fatecat-secret-scan-external-validation-issue-export-0130.json` | `findingCount=0` |
| Task docs | `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0130-measurement-infrastructure-external-validation-issue-export --phase closeout` | pass |
| Quick CI | `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-external-validation-issue-export-0130-postcommit` | pass |

# Review Gate

- Future-optimal drift: task must advance external validation execution readiness instead of creating a cosmetic duplicate summary.
- Ponytail complexity: one bounded generator and wrapper only; no new tracker client, platform or storage layer.
- Document drift: AGENTS, roadmap and task index must mention new contract/script/test.
- Security/privacy: no raw URL, secret assignment, DSN, report body or user data in output.

# Runtime Verification Gate

- Issue export smoke on local artifacts must output `status=operator_action_required` and `issueGate=blocked`.
- local-ci quick must generate `external-validation-issue-export.json` and `EXTERNAL_VALIDATION_ISSUE_EXPORT.md`.

# Ship Readiness

- Focused gates pass.
- Task docs closeout validation passes.
- Post-commit quick CI passes on current HEAD.
- Remote Acceptance and Container CI pass on pushed commit.

# Task Package Acceptance

- All TP leaves are marked done only after their evidence exists.
- `STATUS.md` and `ACCEPTANCE_CHECKLIST.md` must match actual validation state.
- Remaining external live, issue creation and independent audit blockers must stay explicit.

# Anti-Goals

- No real issue creation.
- No external tracker API call.
- No production live passed claim.
- No 100% certification claim.
- No external credentials, production endpoint, user report body or raw URL copied.
