# Acceptance Checklist

# Global Standards
- [x] 不执行真实外部 live。
- [x] 不上传或伪造 proof-ref/live/human-review bundle。
- [x] 不把 readiness audit 写成 certification passed。
- [x] 输出必须拒绝 raw URL 和敏感赋值片段。

# Task Package Checklists

## SPEC
- [x] Scope limited to readiness audit, not live execution.
- [x] Existing external validation and human review gates identified.
- [x] 100% non-claim preserved.

## PLAN
- [x] TP-01..TP-05 task tree defined.
- [x] Dependencies and validation plan defined.
- [x] Rollback boundary defined.

## BUILD
- [x] `contracts/fate/audit/external-evidence-submission-readiness-audit.json` added.
- [x] `scripts/external-evidence-submission-readiness-audit.py` added.
- [x] `scripts/external-evidence-submission-readiness-audit.sh` added.
- [x] `tests/regression/test_external_evidence_submission_readiness_audit.py` added.
- [x] `scripts/local-ci.sh` generates JSON/Markdown artifacts.
- [x] local-ci summary includes readiness audit paths.

## TEST
- [x] Targeted pytest passed.
- [x] CLI smoke passed.
- [x] local-ci quick or focused chain passed.
- [x] task docs validation passed.
- [x] `git diff --check` passed.

## REVIEW
- [x] Output keeps blocked semantics with pending evidence.
- [x] Sensitive/raw URL rejection covered.
- [x] AGENTS and roadmap synchronized.

## SHIP
- [ ] Commit created.
- [ ] Push to `origin/main` completed.
- [ ] Remote Acceptance passed for pushed commit.

## Leaf Nodes
### TP-01.01 Existing contracts
- [x] Existing proof/live/operator/human/certification contracts read.
Verify: source scripts/contracts were inspected.
Gate: readiness audit reuses existing summaries and does not duplicate live validators.

### TP-01.02 local-ci chain
- [x] local-ci artifact order and summary insertion point identified.
Verify: `scripts/local-ci.sh` run order reviewed.
Gate: readiness audit runs after all required input artifacts are generated.

### TP-02.01 Task package
- [x] 0151 task package materialized.
Verify: `governance/tasks/0151-*` exists.
Gate: task package contains no template placeholders.

### TP-02.02 Output contract
- [x] readiness audit output and non-claim policy defined.
Verify: `contracts/fate/audit/external-evidence-submission-readiness-audit.json`.
Gate: pending/live/human/certification blockers remain visible.

### TP-03.01 Contract/script/wrapper
- [x] audit contract, Python script and shell wrapper added.
Verify: three files exist and wrapper calls Python entrypoint.
Gate: CLI writes JSON and Markdown without network calls.

### TP-03.02 Regression tests
- [x] regression tests added.
Verify: `tests/regression/test_external_evidence_submission_readiness_audit.py`.
Gate: blocked, synthetic all-green, CLI and sensitive rejection cases covered.

### TP-03.03 local-ci wiring
- [x] local-ci run step and summary artifacts wired.
Verify: `scripts/local-ci.sh` includes run step and summary env keys.
Gate: output JSON/Markdown paths are included in local-ci summary.

### TP-04.01 AGENTS and roadmap
- [x] AGENTS and roadmap updated.
Verify: `rg` markers in AGENTS and roadmap.
Gate: new script/contract/test can be discovered from directory docs.

### TP-04.02 Task docs
- [x] task docs filled.
Verify: `validate_task_docs.py --phase decompose`.
Gate: no placeholders or required-section errors remain.

### TP-05.01 Validation
- [x] validation commands passed.
Verify: pytest, CLI smoke, ruff, task docs validation and diff check.
Gate: no local validation failure remains.

### TP-05.02 Git delivery
- [ ] commit, push and remote Acceptance completed.
Verify: git log/status and GitHub Actions run.
Gate: pushed commit has successful remote Acceptance.
