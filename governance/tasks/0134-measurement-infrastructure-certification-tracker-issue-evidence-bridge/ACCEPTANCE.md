# Acceptance

# Task-Level Acceptance

- `measurement-infrastructure-certification.json` required evidence includes tracker import package, tracker issue evidence template and tracker issue evidence gate.
- Certification audit domain reads those three artifacts from evidence dir.
- `operator_action_required` gate status contributes blocking items.
- Current audit bundle sidecar cannot make audit domain pass while tracker import/template/gate are blocked.
- Synthetic full-pass fixture can still make certification pass.

# Validation Plan

| Gate | Command | Expected |
| --- | --- | --- |
| Focused pytest | `.venv/bin/python -m pytest -q tests/regression/test_measurement_infrastructure_certification.py` | pass |
| Ruff | `.venv/bin/python -m ruff check scripts/measurement-infrastructure-certification.py tests/regression/test_measurement_infrastructure_certification.py` | pass |
| Format | `.venv/bin/python -m ruff format --check scripts/measurement-infrastructure-certification.py tests/regression/test_measurement_infrastructure_certification.py` | pass |
| Secret scan | `bash scripts/secret-scan.sh --output-json /tmp/fatecat-secret-scan-certification-tracker-issue-evidence-bridge-0134.json` | `findingCount=0` |
| Task docs | `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0134-measurement-infrastructure-certification-tracker-issue-evidence-bridge --phase closeout` | pass |
| Quick CI | `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-certification-tracker-issue-evidence-bridge-0134-postcommit` | pass |

# Review Gate

- Future-optimal drift: task must close certification evidence blindness, not create another summary outside certification.
- Ponytail complexity: no new script, storage or tracker API client.
- Document drift: roadmap, AGENTS and task index must match implementation.
- Security/privacy: no raw URL, token, secret, DSN, report body or user data in certification output.

# Runtime Verification Gate

- Direct certification dry-run on a local-ci style evidence dir must include tracker import/template/gate under audit domain.
- Blocked evidence must produce `status=blocked` and `canClaim100Percent=false`.
- Missing tracker evidence must fail certification domain.

# Ship Readiness

- Focused gates pass.
- Task docs closeout validation passes.
- Post-commit quick CI passes on current HEAD.
- Remote Acceptance and Container CI pass on pushed commit.

# Task Package Acceptance

- All TP leaves are marked done only after their evidence exists.
- `STATUS.md` and `ACCEPTANCE_CHECKLIST.md` match actual validation state.
- Remaining external live, tracker issue creation, filled evidence bundle and independent audit blockers stay explicit.

# Anti-Goals

- No real issue creation.
- No external tracker API call.
- No `gh` execution.
- No tracker evidence accepted claim.
- No production live passed claim.
- No 100% certification claim.
- No external credentials, production endpoint, user report body or raw URL copied.

