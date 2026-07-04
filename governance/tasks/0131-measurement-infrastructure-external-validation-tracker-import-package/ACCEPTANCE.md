# Task-Level Acceptance

- `external-validation-tracker-import-package.py` consumes 0130 issue export JSON and validates `kind`.
- Output JSON has `kind=fatecat.external_validation_tracker_import_package` and required fields.
- Package directory contains `README.md`, `import-manifest.json`, `gh-issue-create-commands.txt` and `issues/*.md`.
- `status=operator_action_required` may indicate package generation success, but `packageGate.status` must remain `blocked` while real tracker creation, live evidence or independent audit result are missing.
- Raw URL, token, secret, DSN and private key markers are rejected from input and output.
- `local-ci.sh --profile quick` generates tracker import package artifacts after issue export.

# Validation Plan

| Gate | Command | Expected |
| --- | --- | --- |
| Syntax | `.venv/bin/python -m py_compile scripts/external-validation-tracker-import-package.py` | pass |
| Focused pytest | `.venv/bin/python -m pytest -q tests/regression/test_external_validation_tracker_import_package.py` | pass |
| Ruff | `.venv/bin/python -m ruff check scripts/external-validation-tracker-import-package.py tests/regression/test_external_validation_tracker_import_package.py` | pass |
| Format | `.venv/bin/python -m ruff format --check scripts/external-validation-tracker-import-package.py tests/regression/test_external_validation_tracker_import_package.py` | pass |
| Secret scan | `bash scripts/secret-scan.sh --output-json /tmp/fatecat-secret-scan-external-validation-tracker-import-package-0131.json` | `findingCount=0` |
| Task docs | `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0131-measurement-infrastructure-external-validation-tracker-import-package --phase closeout` | pass |
| Quick CI | `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-external-validation-tracker-import-package-0131-postcommit` | pass |

# Review Gate

- Future-optimal drift: task must advance external validation issue creation readiness instead of creating a cosmetic duplicate summary.
- Ponytail complexity: one bounded generator and wrapper only; no new tracker client, platform or storage layer.
- Document drift: AGENTS, roadmap and task index must mention new contract/script/test.
- Security/privacy: no raw URL, secret assignment, DSN, report body or user data in output.

# Runtime Verification Gate

- Tracker import package smoke on local artifacts must output `status=operator_action_required` and `packageGate=blocked`.
- local-ci quick must generate JSON, Markdown and package directory artifacts.

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
- No `gh` execution.
- No production live passed claim.
- No 100% certification claim.
- No external credentials, production endpoint, user report body or raw URL copied.
