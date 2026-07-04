# Acceptance

# Task-Level Acceptance

- `third-party-audit-rehearsal.json` required inputs include tracker import package, tracker issue evidence template and tracker issue evidence gate.
- Rehearsal generator validates expected kind for all three tracker artifacts.
- Rehearsal evidence index includes direct tracker import/template/gate entries.
- Rehearsal auditor checklist includes direct tracker import/template/gate checks.
- Local CI passes tracker artifact paths into third-party audit rehearsal.
- Rehearsal remains blocked while tracker issue creation/evidence/live/audit evidence is missing.

# Validation Plan

| Gate | Command | Expected |
| --- | --- | --- |
| Focused pytest | `.venv/bin/python -m pytest -q tests/regression/test_third_party_audit_rehearsal.py` | pass |
| Ruff | `.venv/bin/python -m ruff check scripts/third-party-audit-rehearsal.py tests/regression/test_third_party_audit_rehearsal.py` | pass |
| Format | `.venv/bin/python -m ruff format --check scripts/third-party-audit-rehearsal.py tests/regression/test_third_party_audit_rehearsal.py` | pass |
| Secret scan | `bash scripts/secret-scan.sh --output-json /tmp/fatecat-secret-scan-third-party-rehearsal-tracker-evidence-bridge-0135.json` | `findingCount=0` |
| Task docs | `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0135-measurement-infrastructure-third-party-rehearsal-tracker-evidence-bridge --phase closeout` | pass |
| Quick CI | `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-third-party-rehearsal-tracker-evidence-bridge-0135` | pass |

# Review Gate

- Future-optimal drift: task must close audit rehearsal evidence blindness, not create another summary outside rehearsal.
- Ponytail complexity: no new script, storage or tracker API client.
- Document drift: roadmap, AGENTS and task index must match implementation.
- Security/privacy: no raw URL, token, secret, DSN, report body or user data in rehearsal output.

# Runtime Verification Gate

- Direct rehearsal build on local-ci style artifacts must include tracker import/template/gate under evidence index.
- Blocked tracker evidence must produce `rehearsalGate=blocked`.
- Missing tracker evidence must fail rehearsal generation.

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
