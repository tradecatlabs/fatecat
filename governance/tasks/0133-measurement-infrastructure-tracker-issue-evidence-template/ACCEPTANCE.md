# Task-Level Acceptance

- `external-validation-tracker-issue-evidence-template.py` consumes 0131 tracker import package JSON and validates `kind`.
- Output JSON has `kind=fatecat.external_validation_tracker_issue_evidence_bundle_template` and required fields.
- Output contains `bundleSkeleton.kind=fatecat.external_validation_tracker_issue_evidence_bundle`.
- Template pre-fills `workItemId`, `issueTemplateId`, `bodySha256`, required labels and source package sha.
- Template keeps `readyToSubmitToGate=false` and `templateGate.status=operator_action_required`.
- Filling skeleton with sanitized issue refs and hashes can be accepted by 0132 gate.
- Raw URL, token, secret, DSN, private key and placeholder markers are rejected from input and output.
- `local-ci.sh --profile quick` generates tracker issue evidence template artifacts after tracker import package.

# Validation Plan

| Gate | Command | Expected |
| --- | --- | --- |
| Syntax | `.venv/bin/python -m py_compile scripts/external-validation-tracker-issue-evidence-template.py` | pass |
| Focused pytest | `.venv/bin/python -m pytest -q tests/regression/test_external_validation_tracker_issue_evidence_template.py` | pass |
| Ruff | `.venv/bin/python -m ruff check scripts/external-validation-tracker-issue-evidence-template.py tests/regression/test_external_validation_tracker_issue_evidence_template.py` | pass |
| Format | `.venv/bin/python -m ruff format --check scripts/external-validation-tracker-issue-evidence-template.py tests/regression/test_external_validation_tracker_issue_evidence_template.py` | pass |
| Secret scan | `bash scripts/secret-scan.sh --output-json /tmp/fatecat-secret-scan-external-validation-tracker-issue-evidence-template-0133.json` | `findingCount=0` |
| Task docs | `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0133-measurement-infrastructure-tracker-issue-evidence-template --phase closeout` | pass |
| Quick CI | `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-external-validation-tracker-issue-evidence-template-0133-postcommit` | pass |

# Review Gate

- Future-optimal drift: task must reduce operator evidence mismatch risk without bypassing issue evidence gate.
- Ponytail complexity: one bounded generator and wrapper only; no new tracker client, platform or storage layer.
- Document drift: AGENTS, roadmap and task index must mention new contract/script/test.
- Security/privacy: no raw URL, secret assignment, DSN, report body or user data in output.

# Runtime Verification Gate

- Direct smoke on local tracker import package must output `status=operator_action_required`, `templateGate=operator_action_required` and `readyToSubmitToGate=false`.
- local-ci quick must generate JSON/Markdown artifact paths in `summary.json.artifacts.externalValidationTrackerIssueEvidenceTemplate*`.

# Ship Readiness

- Focused gates pass.
- Task docs closeout validation passes.
- Post-commit quick CI passes on current HEAD.
- Remote Acceptance and Container CI pass on pushed commit.

# Task Package Acceptance

- All TP leaves are marked done only after their evidence exists.
- `STATUS.md` and `ACCEPTANCE_CHECKLIST.md` must match actual validation state.
- Remaining external live, issue creation action, filled evidence bundle and independent audit blockers must stay explicit.

# Anti-Goals

- No real issue creation.
- No external tracker API call.
- No `gh` execution.
- No tracker evidence accepted claim.
- No production live passed claim.
- No 100% certification claim.
- No external credentials, production endpoint, user report body or raw URL copied.
