# Task-Level Acceptance

- `third-party-audit-rehearsal.py` consumes the five required JSON artifacts and validates their `kind`.
- Output JSON has `kind=fatecat.third_party_audit_rehearsal` and required fields.
- Output Markdown has auditor-readable status, evidence index, checklist, pending external items, non-claims and final conclusion.
- `status=passed` may indicate package generation success, but `rehearsalGate.status` must remain `blocked` while external pending items or independent audit result are missing.
- Raw URL, token, secret, DSN and private key markers are rejected from output.
- `local-ci.sh --profile quick` generates JSON and Markdown artifacts after certification.

# Validation Plan

| Gate | Command | Expected |
| --- | --- | --- |
| Syntax | `.venv/bin/python -m py_compile scripts/third-party-audit-rehearsal.py` | pass |
| Focused pytest | `.venv/bin/python -m pytest -q tests/regression/test_third_party_audit_rehearsal.py tests/regression/test_measurement_infrastructure_certification.py` | pass |
| Ruff | `.venv/bin/python -m ruff check scripts/third-party-audit-rehearsal.py tests/regression/test_third_party_audit_rehearsal.py` | pass |
| Format | `.venv/bin/python -m ruff format --check scripts/third-party-audit-rehearsal.py tests/regression/test_third_party_audit_rehearsal.py` | pass |
| Secret scan | `bash scripts/secret-scan.sh --output-json /tmp/fatecat-secret-scan-third-party-audit-rehearsal-0129.json` | `findingCount=0` |
| Task docs | `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0129-measurement-infrastructure-third-party-audit-rehearsal --phase closeout` | pass |
| Quick CI | `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-third-party-audit-rehearsal-0129-postcommit` | pass |

# Review Gate

- Future-optimal drift: task must advance MI-100.G.04 instead of creating a cosmetic report.
- Ponytail complexity: one bounded generator and wrapper only; no new platform or storage layer.
- Document drift: AGENTS, roadmap and task index must mention new contract/script/test.
- Security/privacy: no raw URL, secret assignment, DSN, report body or user data in output.

# Runtime Verification Gate

- Rehearsal smoke on existing local-ci artifacts must output `status=passed` and `rehearsalGate=blocked`.
- local-ci quick must generate `third-party-audit-rehearsal.json` and `THIRD_PARTY_AUDIT_REHEARSAL.md`.

# Ship Readiness

- Focused gates pass.
- Task docs closeout validation passes.
- Post-commit quick CI passes on current HEAD.
- Remote Acceptance and Container CI pass on pushed commit.

# Task Package Acceptance

- All TP leaves are marked done only after their evidence exists.
- `STATUS.md` and `ACCEPTANCE_CHECKLIST.md` must match actual validation state.
- Remaining external live and independent audit blockers must stay explicit.

# Anti-Goals

- No third-party audit passed claim.
- No production live passed claim.
- No 100% certification claim.
- No external credentials, production endpoint, user report body or raw URL copied.
