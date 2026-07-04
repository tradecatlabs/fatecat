# Acceptance Checklist

## Leaf Nodes

### TP-01 certification tracker issue evidence blind spot confirmation

Verify: certification and local-ci tracker artifacts reviewed.

Gate: scope does not require real external credentials or tracker permissions.

- [x] Blind spot confirmed.
- [x] Evidence chain confirmed.

### TP-02 certification contract and aggregator bridge

Verify: certification contract and Python aggregator include tracker import/template/gate.

Gate: `operator_action_required` is not treated as passed.

- [x] Contract updated.
- [x] Aggregator updated.
- [x] Blocked marker updated.

### TP-03 regression coverage

Verify: focused pytest includes tracker chain assertions.

Gate: current audit sidecar cannot bypass tracker issue evidence blockers.

- [x] Required evidence assertions updated.
- [x] Blocked fixture updated.
- [x] Sidecar regression updated.

### TP-04 AGENTS/roadmap/task index sync

Verify: scripts/audit/tests AGENTS, roadmap and task index mention the certification tracker bridge.

Gate: documentation does not claim issue creation, evidence acceptance or live completion.

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
| TP-01 | [x] certification gap confirmed; [x] local-ci tracker artifacts confirmed; [x] no-live boundary confirmed |
| TP-02 | [x] contract updated; [x] aggregator updated; [x] blocked markers updated |
| TP-03 | [x] focused regression updated; [x] blocked fixture updated; [x] sidecar no-bypass assertion added |
| TP-04 | [x] scripts AGENTS synced; [x] audit contract AGENTS synced; [x] tests AGENTS synced; [x] roadmap synced; [x] task index synced |
| TP-05 | [x] focused pytest passed; [x] ruff passed; [x] format passed; [x] secret scan passed; [x] task docs passed; [x] quick CI passed |
| TP-06 | [x] commit/push delegated to outer flow; [x] remote CI observation delegated to outer flow |

# Contract Checks

- [x] Contract declares tracker import package as required evidence.
- [x] Contract declares tracker issue evidence template as required evidence.
- [x] Contract declares tracker issue evidence gate as required evidence.
- [x] Contract declares blocked gate fields for package/template/issue evidence gates.

# Gate Checks

- [x] Focused pytest passed.
- [x] Ruff and format passed.
- [x] Secret scan passed.
- [x] Task docs validation passed.
- [x] Quick local CI passed.
- [x] Remote Acceptance/Container CI handled by outer delivery flow.

