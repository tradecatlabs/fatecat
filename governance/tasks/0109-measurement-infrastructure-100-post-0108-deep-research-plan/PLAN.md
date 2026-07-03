# Planning Summary
0109 是 post-0108 的路线图刷新。当前仓库已经有较完整的 local CI、audit bundle、evaluation trend、provider/source/license drift、multi-surface semantic diff 和 release artifact proof 任务包；但真正的 100% 基础设施仍卡在两类证据：current release truth 状态漂移，以及真实外部生产平台证据。

# Lifecycle Gates
不得跳过 gate；任一 gate 缺少文件、命令或明确豁免证据时，本任务不能 closeout。

| Gate | Exit Criteria | Status |
| --- | --- | --- |
| SPEC | 明确本任务只做 post-0108 调研与计划 | Done |
| PLAN | 输出官方资料矩阵、资源模型、执行波次和不可伪造口径 | Done |
| BUILD | 更新 `RESEARCH.md`、任务包和主路线图 | Done |
| TEST | 任务文档校验、占位符扫描和引用检查通过 | Done |
| REVIEW | 没有把 Acceptance `in_progress`、dry-run、staged gate 写成 production passed | Done |
| SHIP | 规划可作为 W0 release truth finalizer 输入 | Done |

# Simplest Path
1. 复用主路线图，不新建第二份路线图。
2. 只记录外部资料版本和 FateCat 映射，不实现协议升级。
3. 把 0108 release proof 状态漂移写成 W0 P0 缺口。
4. 把下一步切成可执行任务：release truth finalizer -> control plane -> external proof packs -> core quality -> DX/provider -> live parity -> audit.

# Split Strategy
| Node | Split Reason |
| --- | --- |
| TP-01 | 先确认外部资料版本和当前仓库事实，防止计划引用过期标准或旧状态。 |
| TP-02 | 再确认 100% 的资源模型和不可伪造边界。 |
| TP-03 | 用资料和仓库事实更新执行波次与优先级。 |
| TP-04 | 落盘、校验和自审，避免任务包半成品。 |

# Execution Waves
| Wave | Leaves |
| --- | --- |
| W1 | TP-01.01、TP-01.02 |
| W2 | TP-02.01、TP-02.02 |
| W3 | TP-03.01、TP-03.02 |
| W4 | TP-04.01、TP-04.02 |

# Runtime Workflow Contract
- Allowed tools: `rg`, `sed`, `curl`, `git`, `gh run list`, `auto-tasks` validators, `apply_patch`.
- Forbidden actions: branch switch, rebase, push, workflow trigger, production secret access, deployment, runtime code edits.
- Evidence: file diff, validator output, placeholder scan, source links in `RESEARCH.md`, GitHub run snapshot.
- Failure policy: if a source/version cannot be verified, mark it as uncertain instead of asserting; if remote run is not terminal success, mark it pending/in_progress.

# Next Executable Leaves
| Node ID | Action |
| --- | --- |
| - | - |

# Dependency Graph
```text
TP-01.01 -> TP-02.01
TP-01.02 -> TP-02.01
TP-02.01 -> TP-02.02 -> TP-03.01 -> TP-03.02 -> TP-04.01 -> TP-04.02
```

# Rollback Protocol
- 恢复 `INDEX.md` 当前任务行。
- 删除本任务目录。
- 恢复主路线图 Post-0108 追加段。
- 不得影响其他任务目录或业务代码。
