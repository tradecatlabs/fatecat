# Planning Summary
0111 是 W1 control-plane baseline。正确终态不是新起一套运行时控制器，而是先建立统一资源 envelope 和 gate：Capability、Provider、ReleaseGate、EvaluationRun 都有 `spec`、`status`、`admission`、`gate` 和 drift policy，并且 gate 能从现有真相源重新计算状态。

# Lifecycle Gates
不得跳过 gate；任一 gate 缺少文件、命令或明确豁免证据时，本任务不能 closeout。

| Gate | Exit Criteria | Status |
| --- | --- | --- |
| SPEC | 明确 W1 只做 control-plane contract/gate baseline | Done |
| PLAN | 拆成扫描、契约、gate、测试、交付 | Done |
| BUILD | 新增 control-plane registry/schema/gate/test/local-ci 接入 | Done |
| TEST | control-plane gate、targeted pytest、ruff/format 通过 | Done |
| REVIEW | 不把 control-plane pass 写成 production live pass | Done |
| SHIP | 提交推送后保留当前证据与剩余 W2+ 路线 | Done |

# Simplest Path
1. 不复制源 registry，只登记 refs、desired summaries 和 gate。
2. 用一个 Python gate 重算资源状态，发现漂移就 fail-fast。
3. 把 gate 接入 quick CI，保证后续资源漂移被本地发现。
4. 用回归测试锁住 registry envelope 与 gate 输出。

# Split Strategy
| Node | Split Reason |
| --- | --- |
| TP-01 | 先识别已有契约和 gate，避免重复造轮子。 |
| TP-02 | 再新增最小 control-plane 资源 envelope。 |
| TP-03 | 通过脚本和 local-ci 把 envelope 变成可验证门禁。 |
| TP-04 | 用测试和文档防止漂移。 |
| TP-05 | 最后提交推送并保留证据。 |

# Execution Waves
| Wave | Leaves |
| --- | --- |
| W1 | TP-01 |
| W2 | TP-02 |
| W3 | TP-03 |
| W4 | TP-04 |
| W5 | TP-05 |

# Runtime Workflow Contract
- Allowed tools: `rg`, `sed`, `jq`, `pytest`, `ruff`, `bash scripts/control-plane-gate.sh`, `apply_patch`, `git`.
- Forbidden actions: branch switch, rebase, reset, live deployment, production secret access, production rollback.
- Evidence: gate JSON, pytest output, ruff output, task docs validator, git status.

# Next Executable Leaves
| Node ID | Action |
| --- | --- |
| - | - |

# Dependency Graph
```text
TP-01 -> TP-02 -> TP-03 -> TP-04 -> TP-05
```

# Rollback Protocol
- Remove `contracts/fate/control-plane/**`, `scripts/control-plane-gate.*`, the test file and local-ci line.
- Revert `contracts/fate/AGENTS.md`, roadmap and task index updates.
- Do not revert unrelated W0 release proof commits.
