# Planning Summary
0046 是发布收口任务。正确路径是先证明当前 dirty worktree 的边界，再用本地门禁验证，再提交推送，再获取远端 CI 当前 commit 证据，最后更新 closeout。不能把“已有大量改动”直接等同于“可以发布”。

# Lifecycle Gates
| Phase | Gate | Status |
| --- | --- | --- |
| SPEC | release clean state 与 remote CI 目标明确 | Done |
| PLAN | 任务树和风险边界明确 | Done |
| BUILD | 仅允许文档回填和证据脚本运行 | Done |
| TEST | 本地门禁待执行 | Done |
| REVIEW | diff/sensitive/clean state 待审 | Done |
| SHIP | commit/push/CI evidence 待执行 | Pending |

禁止跳过任何 gate；不得把本地 dirty tree 直接推断为 release-ready。

# Simplest Path
不拆分支、不改历史。先分类审计，再优先跑 quick CI；如果本地门禁通过，则按当前基础设施主题提交并推送 `main`，随后读取 GitHub Actions 当前 commit run。

# Split Strategy
- TP-01 证明能否提交。
- TP-02 证明本地质量。
- TP-03 形成远端交付。
- TP-04 证明远端 CI。
- TP-05 收口证据。

# Execution Waves
| Wave | Nodes | Status |
| --- | --- | --- |
| 1 | TP-01.01 | In Progress |
| 1 | TP-01.01 | Done |
| 2 | TP-02.01 | Done |
| 3 | TP-03.01 | In Progress |
| 4 | TP-04.01 | Pending |
| 5 | TP-05.01 | Pending |

# Runtime Workflow Contract
- risk_level: high
- affected_flows: git history, release gate, CI, docs/tasks/contracts/scripts/tests
- state_changes: commit and push if gates pass
- side_effects: remote GitHub branch update and CI run
- rollback: non-destructive revert commit if needed; no force push
- required_tests: task tree, diff check, local-ci quick, live-release-gate, GitHub Actions status

# Next Executable Leaves
TP-03.01

# Dependency Graph
```text
TP-01.01 -> TP-02.01 -> TP-03.01 -> TP-04.01 -> TP-05.01
```

# Rollback Protocol
- 恢复 `INDEX.md` 当前任务行
- 恢复本任务目录到初始化状态
- 不得影响其他任务目录
