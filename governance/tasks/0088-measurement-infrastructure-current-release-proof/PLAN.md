# Planning Summary

0088 converts release proof from scattered manual facts into a reusable current-commit gate. The minimum useful slice is a script that can run in two modes: local-contract for CI-safe pending output, and required-current-release for actual GitHub/GHCR evidence verification.

# Lifecycle Gates

SPEC -> PLAN -> BUILD -> TEST -> REVIEW -> SHIP 不得跳过 gate；任一阶段缺少证据时，后续阶段只能记录为 pending，不能声明完成。

| Phase | Gate |
| --- | --- |
| SPEC | Roadmap, release-gate and current remote state inspected. |
| PLAN | Current proof scope excludes production API/HF/Bot live. |
| BUILD | Script uses GitHub CLI/GHCR official surfaces and redacts sensitive output. |
| TEST | Focused regression, local proof, secret scan and quick CI pass. |
| REVIEW | No historical proof or local imageId accepted as current registry proof. |
| SHIP | Current commit acceptance, container workflow, attestation and current proof pass. |

# Simplest Path

- Add one script pair.
- Add one regression file.
- Register command in existing ReleaseGate resources.
- Use existing container workflow, rollback drill and GitHub attestation.

# Split Strategy

- TP-01/02 define scope and anti-overclaim.
- TP-03 implements script and contracts.
- TP-04 validates locally.
- TP-05 obtains remote release proof for the new commit.

# Execution Waves

| Wave | Nodes |
| --- | --- |
| W1 | TP-01, TP-02 |
| W2 | TP-03 |
| W3 | TP-04 |
| W4 | TP-05 |

# Runtime Workflow Contract

- Local mode: `current-release-proof.sh --skip-remote --output-json <path>` returns pending/blocked evidence without remote calls.
- Required mode: `current-release-proof.sh --require-current-release --rollback-evidence-path <rollback.json> --output-json <path>` requires current commit acceptance, container run, GHCR digest, attestation, release artifact and rollback evidence.
- Output kind: `fatecat.current_release_proof`.
- Side effects: none locally; remote proof depends on separately triggered GitHub Actions container workflow.

# Next Executable Leaves

| Node ID | Action |
| --- | --- |
| TP-03 | Finish script/contract/docs/regression implementation. |

# Dependency Graph

```text
TP-01 -> TP-02 -> TP-03 -> TP-04 -> TP-05
```

# Rollback Protocol

- Remove `scripts/current-release-proof.py/.sh`.
- Remove release-gate and registry command entries.
- Remove regression and AGENTS/task docs references.
- Existing `live-release-gate`, container workflow and release artifacts remain unchanged.

# Plan

## TP-01 SPEC

- Confirm 0088 is next roadmap node after 0087.
- Confirm no current commit container run exists before implementation.

## TP-02 PLAN

- Define required evidence IDs.
- Keep production API/HF/Bot live outside 0088.

## TP-03 BUILD

- Implement current release proof script.
- Add release-gate/registry entries.
- Add focused tests and docs.

## TP-04 TEST

- Focused pytest.
- Local proof contract.
- ruff/format/secret scan.
- quick CI.

## TP-05 SHIP

- Commit and push.
- Trigger remote acceptance and container workflow `push_image=true`.
- Generate rollback evidence.
- Run required current-release-proof gate.
