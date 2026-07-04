# Acceptance Checklist

## Leaf Nodes

### TP-01 scope and evidence chain confirmation

Verify: roadmap 6.23/7/8 and existing audit/certification scripts reviewed.

Gate: scope does not require real external credentials.

- [x] Scope confirmed.
- [x] Evidence chain confirmed.

### TP-02 contract/script/wrapper

Verify: contract, Python generator and shell wrapper exist.

Gate: generator does not execute external live calls and rejects sensitive/raw URL output.

- [x] Contract added.
- [x] Generator added.
- [x] Wrapper added.

### TP-03 local-ci artifact and regression wiring

Verify: local-ci has a rehearsal step and focused pytest includes the rehearsal test.

Gate: summary artifact path is exposed.

- [x] local-ci step added.
- [x] regression wiring added.

### TP-04 AGENTS/roadmap/task index sync

Verify: scripts/audit/tests AGENTS, roadmap and task index mention the rehearsal package.

Gate: documentation does not claim third-party audit completion.

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

- [x] Commit created.
- [x] Push complete.
- [x] Remote CI passed.

# Global Standards

- [x] Scope and external blockers are explicit.
- [x] No real external live request is executed.
- [x] No secret, DSN, raw URL, report body or user input is copied.
- [x] Documentation sync paths are identified.
- [x] Validation gates have current evidence.
- [x] Git delivery and remote CI evidence are current.

# Task Package Checklists

| Node | Checklist |
| --- | --- |
| TP-01 | [x] scope confirmed; [x] upstream evidence chain confirmed; [x] no-live boundary confirmed |
| TP-02 | [x] contract added; [x] generator added; [x] wrapper added; [x] kind validation added; [x] sensitive/raw URL rejection added |
| TP-03 | [x] local-ci run step added; [x] summary artifact added; [x] focused regression added |
| TP-04 | [x] scripts AGENTS synced; [x] audit contract AGENTS synced; [x] tests AGENTS synced; [x] roadmap synced; [x] task index synced |
| TP-05 | [x] focused pytest passed; [x] ruff passed; [x] format passed; [x] secret scan passed; [x] task docs passed; [x] quick CI passed |
| TP-06 | [x] commit created; [x] pushed to origin/main; [x] remote Acceptance success; [x] remote Container success |

# Contract Checks

- [x] Contract declares required inputs and output fields.
- [x] Contract declares privacy boundary and non-claims.
- [x] Generator validates input `kind`.
- [x] Generator emits JSON and Markdown.
- [x] Raw URL and sensitive assignment are rejected.

# Gate Checks

- [x] Focused pytest passed.
- [x] Ruff and format passed.
- [x] Secret scan passed.
- [x] Task docs validation passed.
- [x] Quick local CI passed.
- [x] Remote Acceptance/Container CI passed after push.
