# Task-Level Acceptance
0151 is complete when the readiness audit is executable, tested, wired into local-ci, documented, and delivered with remote Acceptance evidence.

# Task Package Acceptance
| Block | Command / Evidence | Expected |
| --- | --- | --- |
| Contract and script tests | `python -m pytest -q tests/regression/test_external_evidence_submission_readiness_audit.py` | pass |
| Script smoke | `bash scripts/external-evidence-submission-readiness-audit.sh ...` with synthetic fixtures or local-ci outputs | writes JSON and Markdown |
| local-ci wiring | `rg -n "external evidence submission readiness audit|FATE_LOCAL_CI_EXTERNAL_EVIDENCE_SUBMISSION_READINESS_AUDIT" scripts/local-ci.sh` | markers found |
| Docs wiring | `rg -n "external-evidence-submission-readiness-audit|test_external_evidence_submission_readiness_audit|External evidence submission readiness audit" scripts/AGENTS.md contracts/fate/audit/AGENTS.md tests/AGENTS.md docs/reference-materials/roadmap/测算基础设施100%实现计划.md` | markers found |
| Task docs | `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0151-measurement-infrastructure-external-evidence-submission-readiness-audit --phase closeout` | pass |
| Formatting/static | `ruff check`, `ruff format --check`, `git diff --check` | pass |
| Git delivery | commit pushed to `origin/main` and GitHub Acceptance for pushed commit passed | pass |

# Global Acceptance Standards
- Readiness audit output must keep `submissionReadinessGate.status=blocked` when proof/live/human/certification evidence is pending.
- Output must not include raw URL, token, secret, password, DSN, private key, report body, user input or production logs.
- Operator packet readiness must not override certification gate.
- Synthetic all-green test may pass only when all upstream gate summaries are explicitly accepted/passed.

# Validation Plan
1. Run targeted regression.
2. Run script smoke through CLI.
3. Run local-ci quick or at minimum the focused local-ci chain if full quick is too slow before commit.
4. Validate task docs.
5. Run diff/format/static gates.
6. Commit, push, trigger/watch GitHub Acceptance.

# Review Gate
- Self-review source for overclaim terms like `100% achieved`, `live passed` or `production ready` in 0151 outputs.
- Confirm every new file is referenced by relevant AGENTS or roadmap.

# Runtime Verification Gate
- local-ci quick should generate `external-evidence-submission-readiness-audit.json` and Markdown under its output dir.
- Summary JSON should expose both artifact paths.

# Ship Readiness
- Ship is allowed only after local validation passes, worktree is clean after commit, push succeeds and remote Acceptance passes.

# Anti-Goals
- Do not connect to external systems.
- Do not create or accept real evidence bundles inside this task.
- Do not change certification semantics.
