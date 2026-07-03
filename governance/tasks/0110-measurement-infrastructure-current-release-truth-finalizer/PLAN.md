# Planning Summary
0110 是 0109 W0 的执行收口任务。正确终态是：仓库不再带 0108 重复状态，最终 main HEAD 已推送，且最终 release proof 由当前 HEAD 的远端 Acceptance、Container release、remote artifact、GHCR digest、attestation verify step 与 dry-run rollback evidence 共同证明。

# Lifecycle Gates
不得跳过 gate；任一 gate 缺少文件、命令或明确豁免证据时，本任务不能 closeout。

| Gate | Exit Criteria | Status |
| --- | --- | --- |
| SPEC | 明确本任务只处理 W0 release truth finalizer | Done |
| PLAN | 拆出索引修复、提交推送、远端 workflow、proof 聚合 | Done |
| BUILD | 任务包与 INDEX 修复落盘 | Done |
| TEST | 任务文档校验、占位符扫描、git diff check | Done |
| REVIEW | 不把本地 acceptance、dry-run rollback、workflow dispatch 写成 production passed | Done |
| SHIP | 交给提交后远端 proof；最终证据不写回 Git | Done |

# Simplest Path
1. 只修正 `INDEX.md` 中的 0108 重复状态。
2. 新增 0110 任务包记录 W0 finalizer。
3. 提交推送后重新触发远端 proof。
4. 最终 proof 不写回 Git，只在交付汇报中给 run URL、digest 和 JSON 路径。

# Split Strategy
| Node | Split Reason |
| --- | --- |
| TP-01 | 先清理仓库状态漂移，避免审计看到重复真相。 |
| TP-02 | 再固定最终 HEAD，避免 proof 绑定旧提交。 |
| TP-03 | 远端 CI/release 是当前 release truth 的核心证据。 |
| TP-04 | rollback 与 current-release-proof 聚合最终闭环。 |

# Execution Waves
| Wave | Leaves |
| --- | --- |
| W1 | TP-01 |
| W2 | TP-02 |
| W3 | TP-03 |
| W4 | TP-04 |

# Runtime Workflow Contract
- Allowed tools: `git`, `gh workflow run`, `gh run view`, `scripts/release-artifacts.sh`, `scripts/rollback-drill.sh`, `scripts/current-release-proof.sh`, `auto-tasks` validators.
- Forbidden actions: branch switch, rebase, reset, production rollback, secret access, production traffic switch.
- Evidence: final HEAD, workflow URLs, container digest, remote artifact, attestation step, rollback JSON, current-release-proof JSON.

# Next Executable Leaves
| Node ID | Action |
| --- | --- |
| - | - |

# Dependency Graph
```text
TP-01 -> TP-02 -> TP-03 -> TP-04
```

# Rollback Protocol
- Restore the removed duplicate row only if the finalizer itself is abandoned before commit.
- Do not revert unrelated tasks or previous commits.
