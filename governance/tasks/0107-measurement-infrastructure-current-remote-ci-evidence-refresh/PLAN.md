# Planning Summary
0107 closes the immediate post-0106 remote evidence gap by triggering GitHub Actions for the current pushed `main` HEAD. The task package is committed before dispatch; final pass/fail evidence remains in GitHub Actions so the tested SHA remains the final SHA.

# Lifecycle Gates
不得跳过 gate；任一 workflow 没有 terminal success 时，不能把 current remote CI evidence 写成 passed。

| Gate | Exit Criteria | Status |
| --- | --- | --- |
| SPEC | Scope limited to remote Acceptance/Container dispatch, no GHCR publish | Done |
| PLAN | Dispatch/poll/verify/timeout rules written | Done |
| BUILD | Task package and INDEX prepared | Done |
| TEST | Task docs validator and placeholder scan pass | Done |
| REVIEW | No false CI/release/live claims | Done |
| SHIP | Commit/push task package, dispatch workflows, report external evidence | Done |

# Simplest Path
1. Commit the 0107 task package first.
2. Dispatch `acceptance.yml` on `main`.
3. Dispatch `container.yml` on `main` with `push_image=false`.
4. Poll `head_sha="$(git rev-parse HEAD)"; gh run list --commit "$head_sha"` and `gh run view` until both target workflows reach terminal states.
5. Treat success only when `headSha == git rev-parse HEAD`, `status == completed`, and `conclusion == success`.

# Split Strategy
| Node | Split Reason |
| --- | --- |
| TP-01 | Preflight prevents dispatching against dirty or wrong HEAD. |
| TP-02 | Dispatch is separated from polling so trigger failures are visible. |
| TP-03 | Poll/verify owns evidence quality and anti-forgery checks. |
| TP-04 | Closeout handles docs commit and external evidence boundary. |

# Execution Waves
| Wave | Leaves |
| --- | --- |
| W1 | TP-01.01、TP-01.02、TP-04.01 |
| W2 | TP-04.02 |
| W3 | TP-02.01、TP-02.02 |
| W4 | TP-03.01、TP-03.02 |

# Runtime Workflow Contract
Allowed tools: `git`, `gh workflow run`, `gh run list`, `gh run view`, `auto-tasks` validators, `rg`.

Forbidden actions: branch switch, rebase, force push, `push_image=true`, HF deploy, production secret access, runtime code edits.

Evidence contract: run URL, workflow name, headSha, status, conclusion and createdAt are authoritative. Local output is not a substitute.

# Next Executable Leaves
| Node ID | Action |
| --- | --- |
| - | - |

# Dependency Graph
```text
TP-01.01 -> TP-01.02 -> TP-04.01 -> TP-04.02
TP-04.02 -> TP-02.01 -> TP-03.01 -> TP-03.02
TP-04.02 -> TP-02.02 -> TP-03.01
```

# Rollback Protocol
- 恢复 `INDEX.md` 当前任务行
- 恢复本任务目录到初始化状态
- 不得影响其他任务目录
