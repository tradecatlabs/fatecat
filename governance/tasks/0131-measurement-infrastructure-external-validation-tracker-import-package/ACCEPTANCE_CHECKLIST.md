# Acceptance Checklist

## Leaf Nodes

### TP-01 scope and tracker import boundary confirmation

Verify: roadmap 6.25 and existing issue export script reviewed.

Gate: scope does not require real external credentials or tracker permissions.

- [x] Scope confirmed.
- [x] Evidence chain confirmed.

### TP-02 tracker import package contract/script/wrapper

Verify: contract, Python builder and shell wrapper exist.

Gate: generator does not execute external live calls, does not create issues, does not execute `gh`, and rejects sensitive/raw URL output.

- [x] Contract added.
- [x] Builder added.
- [x] Wrapper added.

### TP-03 local-ci artifact and regression wiring

Verify: local-ci has a tracker import package step and focused pytest includes the tracker import package test.

Gate: summary artifact paths are exposed.

- [x] local-ci step added.
- [x] regression wiring added.

### TP-04 AGENTS/roadmap/task index sync

Verify: scripts/audit/tests AGENTS, roadmap and task index mention the tracker import package.

Gate: documentation does not claim issue creation or live completion.

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

# Global Standards

- [x] Scope and external blockers are explicit.
- [x] No real external live request is executed.
- [x] No real issue tracker API request is executed.
- [x] No secret, DSN, raw URL, report body or user input is copied.
- [x] Documentation sync paths are identified.
- [x] Validation gates have current evidence.
- [x] Git delivery and remote CI evidence are delegated to outer delivery flow.

# Task Package Checklists

| Node | Checklist |
| --- | --- |
| TP-01 | [x] scope confirmed; [x] upstream evidence chain confirmed; [x] no-live boundary confirmed |
| TP-02 | [x] contract added; [x] builder added; [x] wrapper added; [x] kind validation added; [x] sensitive/raw URL rejection added |
| TP-03 | [x] local-ci run step added; [x] summary artifact added; [x] focused regression added |
| TP-04 | [x] scripts AGENTS synced; [x] audit contract AGENTS synced; [x] tests AGENTS synced; [x] roadmap synced; [x] task index synced |
| TP-05 | [x] focused pytest passed; [x] ruff passed; [x] format passed; [x] secret scan passed; [x] task docs passed; [x] quick CI passed |
| TP-06 | [x] commit/push delegated to outer flow; [x] remote CI observation delegated to outer flow |

# Contract Checks

- [x] Contract declares required inputs and output fields.
- [x] Contract declares privacy boundary and non-claims.
- [x] Builder validates input `kind`.
- [x] Builder emits manifest, README, command text and body files.
- [x] Raw URL and sensitive assignment are rejected.

# Gate Checks

- [x] Focused pytest passed.
- [x] Ruff and format passed.
- [x] Secret scan passed.
- [x] Task docs validation passed.
- [x] Quick local CI passed.
- [x] Remote Acceptance/Container CI handled by outer delivery flow.
