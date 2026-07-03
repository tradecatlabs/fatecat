# Planning Summary
0108 promotes release proof from “remote CI only” to “remote release artifact proof” for the final main HEAD. It publishes the delivery image to GHCR through GitHub Actions, verifies artifact attestation, generates dry-run rollback evidence, and validates all required current-release-proof checks.

# Lifecycle Gates
不得跳过 gate；`current-release-proof --require-current-release` 不通过时，0108 不能声明完成。

| Gate | Exit Criteria | Status |
| --- | --- | --- |
| SPEC | Scope limited to release artifact proof, not production live | Done |
| PLAN | Commit-before-dispatch and proof aggregation strategy defined | Done |
| BUILD | Task package and INDEX prepared | Done |
| TEST | Task docs validators pass | Done |
| REVIEW | No false production rollback/live claims | Done |
| SHIP | Final HEAD has Acceptance success, Container publish success, digest, attestation, rollback evidence and current-release-proof pass | Done |

# Simplest Path
1. Commit/push this 0108 task package.
2. Trigger Acceptance for final HEAD.
3. Trigger Container workflow with `push_image=true` for final HEAD.
4. Poll both runs to terminal success.
5. Generate rollback drill evidence in `/tmp` for final HEAD.
6. Run `current-release-proof.sh --require-current-release` with run IDs and rollback evidence.
7. Do not commit after proof collection.

# Split Strategy
| Node | Split Reason |
| --- | --- |
| TP-01 | Preflight proves 0108 is necessary and safe. |
| TP-02 | Freezes final HEAD before external release evidence. |
| TP-03 | Separates dispatch from verification. |
| TP-04 | Verifies remote artifacts, digest and attestation. |
| TP-05 | Adds rollback evidence and aggregated release proof. |

# Execution Waves
| Wave | Leaves |
| --- | --- |
| W1 | TP-01.01、TP-01.02 |
| W2 | TP-02.01、TP-02.02 |
| W3 | TP-03.01、TP-03.02 |
| W4 | TP-04.01、TP-04.02 |
| W5 | TP-05.01、TP-05.02 |

# Runtime Workflow Contract
Allowed tools: `git`, `gh workflow run`, `gh run list`, `gh run view`, `gh attestation verify` via workflow, project release scripts, `auto-tasks` validators.

Forbidden actions: branch switch, rebase, force push, production rollback execution, HF deploy, Bot live, production secret reads, runtime code edits.

Evidence contract: release workflow run URL, acceptance run URL, registry digest, attestation verification, release artifact upload, rollback drill JSON and current-release-proof JSON.

# Next Executable Leaves
| Node ID | Action |
| --- | --- |
| - | - |

# Dependency Graph
```text
TP-01.01 -> TP-01.02 -> TP-02.01 -> TP-02.02
TP-02.02 -> TP-03.01 -> TP-04.01
TP-02.02 -> TP-03.02 -> TP-04.01
TP-04.01 -> TP-04.02 -> TP-05.01 -> TP-05.02
```

# Rollback Protocol
- 恢复 `INDEX.md` 当前任务行
- 恢复本任务目录到初始化状态
- 不得影响其他任务目录
