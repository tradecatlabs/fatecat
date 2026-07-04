# Acceptance Checklist

## Leaf Nodes

### TP-01 rehearsal tracker blind spot confirmation

Verify: rehearsal script and contract reviewed.

Gate: no external tracker or credential is needed.

- [x] Blind spot confirmed.
- [x] Local-only scope confirmed.

### TP-02 contract and CLI input bridge

Verify: contract and script expose tracker import/template/gate inputs.

Gate: expected `kind` values are checked.

- [x] Contract updated.
- [x] Script parser updated.
- [x] Input validation updated.

### TP-03 rehearsal evidence/checklist bridge

Verify: evidence index and auditor checklist include tracker chain.

Gate: blocked/operator-action statuses do not pass rehearsal.

- [x] Evidence index updated.
- [x] Checklist updated.
- [x] Blocking items updated.

### TP-04 local-ci and documentation sync

Verify: local-ci, AGENTS, roadmap and task index mention 0135.

Gate: docs do not claim issue creation, live proof or third-party audit completion.

- [x] local-ci invocation updated.
- [x] AGENTS updated.
- [x] Roadmap updated.
- [x] Task index updated.

### TP-05 validation gates

Verify: focused pytest, ruff, format, secret scan, task docs and quick CI pass.

Gate: all validation commands pass.

- [x] Focused pytest passed.
- [x] Ruff and format passed.
- [x] Secret scan passed.
- [x] Task docs passed.
- [x] Quick CI passed.

### TP-06 commit/push and remote CI observation

Verify: git status clean, push complete, remote Acceptance/Container success.

Gate: current commit CI passed.

- [x] Commit/push delegated to outer delivery flow.
- [x] Remote CI observation delegated to outer delivery flow.

## Global Standards

- [x] Scope and external blockers are explicit.
- [x] No real external live request is executed.
- [x] No real issue tracker API request is executed.
- [x] No secret, DSN, raw URL, report body or user input is copied.
- [x] Documentation sync paths are updated.
- [x] Validation gates have current evidence.
- [x] Git delivery and remote CI evidence are delegated to outer delivery flow.

## Task Package Checklists

| Node | Checklist |
| --- | --- |
| TP-01 | [x] rehearsal blind spot confirmed; [x] no-live boundary confirmed |
| TP-02 | [x] contract updated; [x] CLI updated; [x] expected kinds checked |
| TP-03 | [x] evidence index updated; [x] checklist updated; [x] blocked semantics preserved |
| TP-04 | [x] local-ci synced; [x] scripts/audit/tests AGENTS synced; [x] roadmap synced; [x] task index synced |
| TP-05 | [x] focused pytest passed; [x] ruff passed; [x] format passed; [x] secret scan passed; [x] task docs passed; [x] quick CI passed |
| TP-06 | [x] commit/push delegated to outer flow; [x] remote CI observation delegated to outer flow |

## Contract Checks

- [x] Contract declares tracker import package as required input.
- [x] Contract declares tracker issue evidence template as required input.
- [x] Contract declares tracker issue evidence gate as required input.
- [x] Contract declares expected kinds for all tracker artifacts.

## Gate Checks

- [x] Focused pytest passed.
- [x] Ruff and format passed.
- [x] Secret scan passed.
- [x] Task docs validation passed.
- [x] Quick local CI passed.
- [x] Remote Acceptance/Container CI handled by outer delivery flow.
