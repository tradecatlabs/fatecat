# Acceptance Checklist

# Global Standards
- [x] No placeholder remains in task docs.
- [x] No external live evidence is claimed without real evidence.
- [x] Evidence output is summary-only and no sensitive data is copied.
- [x] Focused regression and smoke/generation commands are recorded with true result.
- [x] Task docs validator passes for closeout.

# Task Package Checklists
## TP-01.01
Verify: `rg -n "evaluation.*trend|evidence_coverage_trend|local-ci-output-dir" scripts/current-audit-bundle.py tests/regression/test_current_audit_bundle.py scripts/local-ci.sh`

Gate: 0104 trend gate audit bundle gap is confirmed.

- [x] Current audit bundle only had evidence coverage trend before this task.
- [x] 0104 INDEX status drift identified.

## TP-01.02
Verify: `sed -n '1,60p' scripts/current-audit-bundle.py`

Gate: Mapping fields are clear and summary-only.

- [x] `evidence.evaluation_trend_gate` mapping defined.
- [x] `trendFindings` must be empty.

## TP-02.01
Verify: `rg -n "evidence.evaluation_trend_gate|fatecat.evaluation_trend_gate" scripts/current-audit-bundle.py`

Gate: current audit bundle can consume trend artifact.

- [x] Artifact spec added.

## TP-02.02
Verify: `.venv/bin/python -m pytest -q tests/regression/test_current_audit_bundle.py`

Gate: Regression asserts evidence index contains evaluation trend item.

- [x] Test fixture generates evaluation trend gate smoke artifact.
- [x] Test asserts `latestStatus=passed`.

## TP-02.03
Verify: `rg -n "evaluation trend gate|0105|evidence.evaluation_trend_gate" contracts docs governance/tasks scripts tests`

Gate: Contract/docs/task index are synchronized.

- [x] Audit contract updated.
- [x] Audit AGENTS updated.
- [x] Roadmap updated.
- [x] 0104 INDEX status fixed.

## TP-03.01
Verify: `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0105-measurement-infrastructure-current-audit-bundle-evaluation-trend --phase closeout`

Gate: validators and focused checks pass.

- [x] Task docs validator passed.
- [x] Focused tests passed.
- [x] Current bundle generation passed.
- [x] Ruff check/format passed.
- [x] Secret scan passed.
- [x] Diff whitespace check passed.

## TP-03.02
Verify: `git status --short --branch`

Gate: scoped diff clear and delivery evidence recorded.

- [x] STATUS/TODO/Checklist closeout synchronized.
- [x] Git delivery evidence recorded in final delivery output if commit/push is performed.
