# Planning Summary
0096 implements the first local executable slice after the post-0094 plan: strengthen the core quality corpus and report diff gate. The smallest useful improvement is to expand the weaker ziwei basic fixture from 4 to 8 anonymous cases, then make the gate prove coverage tags and summary-only report diff policy.

# Lifecycle Gates
| Gate | Requirement | Result |
| --- | --- | --- |
| SPEC | Scope limited to evaluation contracts, fixtures, gates, tests and docs. | Done |
| PLAN | Split into fixture, manifest/policy, gate/test and docs. | Done |
| BUILD | Ziwei fixture, manifest, policy, gate, tests and docs updated. | Done |
| TEST | Core-quality gate and focused pytest pass. | Done |
| REVIEW | No production provider change, no real user data, no full report body. | Done |
| SHIP | Task docs closeout and validators pass. | Done |

不得跳过 gate；任一 SPEC/PLAN/BUILD/TEST/REVIEW/SHIP gate 缺证据时，0096 不得 closeout。

# Simplest Path
1. Preserve existing core-quality gate.
2. Add fields to existing manifest/policy instead of new scripts.
3. Expand the smallest weak fixture: `ziwei/golden/cases.json`.
4. Reuse focused pytest and L4 smoke.

# Split Strategy
| Package | Scope |
| --- | --- |
| TP-01 | Read current state. |
| TP-02 | Update fixture and contracts. |
| TP-03 | Update gate and tests. |
| TP-04 | Update docs and task package. |
| TP-05 | Validate. |

# Execution Waves
| Wave | Nodes |
| --- | --- |
| 1 | TP-01.01 |
| 2 | TP-02.01, TP-02.02 |
| 3 | TP-03.01, TP-03.02 |
| 4 | TP-04.01 |
| 5 | TP-05.01 |

# Runtime Workflow Contract
```text
core-quality-corpus-gate.sh
  -> core-quality-corpus.json
  -> report-diff-policy.json
  -> evaluation registry
  -> bazi/ziwei synthetic fixture files
  -> machine-readable summary JSON
```

# Next Executable Leaves
| Node ID | Action |
| --- | --- |
| - | - |

# Dependency Graph
```text
TP-01.01 -> TP-02.01
TP-01.01 -> TP-02.02
TP-02.01 -> TP-03.01
TP-02.02 -> TP-03.01
TP-03.01 -> TP-03.02
TP-03.02 -> TP-04.01
TP-04.01 -> TP-05.01
```

# Future-Optimal Task Contract
| Field | Value |
| --- | --- |
| Target end state | Core quality is a contract-backed, privacy-safe, reproducible evaluation resource, not ad hoc samples. |
| Real constraints | Existing contracts/gate/local-ci; no real user data; no provider algorithm change. |
| Inertia constraints | Existing min counts and simple count checks must not cap future quality gates. |
| Wrong concept / wrong boundary | Treating 4 ziwei samples as sufficient core quality proof. |
| Kill list | Remove the weak minZiweiGoldenCases=4 threshold. |
| Proof point | Gate passes with ziwei min 8, coverage tags and summary-only report diff checks. |
| Falsifier | Gate/test fails or stores full report body. |
| Migration slice | Incremental contract/gate expansion without new runtime surface. |
| Rejected short-term patches | Do not only change doc wording; do not add unchecked fixture rows. |
| Future-optimal review owner | `auto-review` future-optimal-drift. |

# Ponytail Task Contract
| Field | Value |
| --- | --- |
| Existence check | The 0095 plan identifies core corpus/report diff as next quality foundation; existing gate has a concrete weak threshold. |
| Selected ladder rung | Project-native contract/gate/test extension. |
| Skipped scope | Expert review, true full-text diff, external benchmark, provider algorithm work. |
| Ceiling / upgrade path | When corpus grows beyond static fixtures, add reviewer sampling, trend storage and artifact diff. |
| Do-not-simplify | Privacy/no-full-report-body/no-production-provider-read boundaries. |
| Minimal runnable check | `core-quality-corpus-gate.sh` and focused pytest. |
| Complexity review owner | `auto-review` ponytail-complexity. |

# Document-Driven Task Contract
| Field | Value |
| --- | --- |
| Operating model update | not needed: infrastructure positioning unchanged. |
| Toolchain model update | not needed: no new command. |
| Process update | not needed: no workflow change. |
| Source-of-truth updates | updated: contracts, fixture, registry, AGENTS, roadmap, task docs. |
| Local README/AGENTS impact | updated: evaluation/data-products/scripts/tests AGENTS. |
| Contract/catalog/schema impact | updated: evaluation contracts and registry metadata; schema unchanged. |
| ADR/Gate/module-context impact | not needed: existing gate extended in place. |
| Documentation exemption reason | No additional long-term docs needed beyond roadmap and AGENTS. |
| Validation evidence | core quality gate, focused pytest, task validator. |

# Rollback Protocol
- Restore changed fixture/contract/gate/test/docs files.
- Restore `governance/tasks/INDEX.md` 0096 row.
- Re-run `core-quality-corpus-gate.sh` and focused pytest.
