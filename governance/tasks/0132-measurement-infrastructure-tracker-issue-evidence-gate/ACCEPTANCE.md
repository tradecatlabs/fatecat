# Task-Level Acceptance

- `external-validation-tracker-issue-evidence-gate.py` consumes 0131 tracker import package JSON and validates `kind`.
- Optional issue evidence bundle must have `kind=fatecat.external_validation_tracker_issue_evidence_bundle` and source package sha256 binding.
- Output JSON has `kind=fatecat.external_validation_tracker_issue_evidence_gate` and required fields.
- Without evidence, `status=external_connectivity_pending` and `issueEvidenceGate.status=blocked`.
- With complete valid evidence, `issueEvidenceGate.status=passed` but `shipGate.status=blocked`.
- Raw URL, token, secret, DSN, private key and placeholder markers are rejected from input and output.
- `local-ci.sh --profile quick` generates tracker issue evidence gate artifact after tracker import package.

# Validation Plan

| Gate | Command | Expected |
| --- | --- | --- |
| Syntax | `.venv/bin/python -m py_compile scripts/external-validation-tracker-issue-evidence-gate.py` | pass |
| Focused pytest | `.venv/bin/python -m pytest -q tests/regression/test_external_validation_tracker_issue_evidence_gate.py` | pass |
| Ruff | `.venv/bin/python -m ruff check scripts/external-validation-tracker-issue-evidence-gate.py tests/regression/test_external_validation_tracker_issue_evidence_gate.py` | pass |
| Format | `.venv/bin/python -m ruff format --check scripts/external-validation-tracker-issue-evidence-gate.py tests/regression/test_external_validation_tracker_issue_evidence_gate.py` | pass |
| Secret scan | `bash scripts/secret-scan.sh --output-json /tmp/fatecat-secret-scan-external-validation-tracker-issue-evidence-gate-0132.json` | `findingCount=0` |
| Task docs | `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0132-measurement-infrastructure-tracker-issue-evidence-gate --phase closeout` | pass |
| Quick CI | `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-external-validation-tracker-issue-evidence-gate-0132-postcommit` | pass |

# Review Gate

- Future-optimal drift: task must advance tracker issue evidence binding instead of duplicating issue export/import package.
- Ponytail complexity: one bounded gate and wrapper only; no new tracker client, platform or storage layer.
- Document drift: AGENTS, roadmap and task index must mention new contract/script/test.
- Security/privacy: no raw URL, secret assignment, DSN, report body or user data in output.

# Runtime Verification Gate

- Direct smoke on local tracker import package must output `status=external_connectivity_pending`, `issueEvidenceGate=blocked` and `shipGate=blocked` without evidence.
- local-ci quick must generate JSON artifact path in `summary.json.artifacts.externalValidationTrackerIssueEvidenceGate`.

# Ship Readiness

- Focused gates pass.
- Task docs closeout validation passes.
- Post-commit quick CI passes on current HEAD.
- Remote Acceptance and Container CI pass on pushed commit.

# Task Package Acceptance

- All TP leaves are marked done only after their evidence exists.
- `STATUS.md` and `ACCEPTANCE_CHECKLIST.md` must match actual validation state.
- Remaining external live, issue creation action and independent audit blockers must stay explicit.

# Anti-Goals

- No real issue creation.
- No external tracker API call.
- No `gh` execution.
- No production live passed claim.
- No 100% certification claim.
- No external credentials, production endpoint, user report body or raw URL copied.
