# Planning Summary
0106 是 post-0105 的路线图刷新。0104/0105 已把 EvaluationRun trend gate 和 current audit bundle evidence 接起来；当前真正暴露出的下一缺口是 current HEAD 没有可见远端 GitHub Actions run，因此 release proof 仍不能声明完成。本任务只落盘调研与计划，后续实现应先补 current remote CI evidence refresh，再推进外部 live。

# Lifecycle Gates
不得跳过 gate；任一 gate 缺少文件、命令或明确豁免证据时，本任务不能 closeout。

| Gate | Exit Criteria | Status |
| --- | --- | --- |
| SPEC | 明确本任务只做 post-0105 调研与计划 | Done |
| PLAN | 输出资料矩阵、资源成熟度、执行波次和不可伪造口径 | Done |
| BUILD | 更新 `RESEARCH.md`、任务包和主路线图 | Done |
| TEST | 任务文档校验、占位符扫描和引用检查通过 | Done |
| REVIEW | 没有把 remote CI absent、external live pending 写成 passed | Done |
| SHIP | 规划可作为 0107 或下一实现任务输入 | Done |

# Simplest Path
1. 复用主路线图，不新建第二份路线图。
2. 只记录外部资料版本和 FateCat 映射，不实现协议升级。
3. 把 `gh run list --commit HEAD` 空结果写成 P0 缺口。
4. 把下一步切成可执行任务：current remote CI evidence -> remote evaluation artifact -> core quality deep corpus -> external live。

# Split Strategy
| Node | Split Reason |
| --- | --- |
| TP-01 | 先确认外部资料版本，防止计划引用过期标准。 |
| TP-02 | 再确认仓库事实，防止规划覆盖真实缺口。 |
| TP-03 | 用资料和仓库事实更新资源成熟度与执行波次。 |
| TP-04 | 落盘、校验和自审，避免任务包半成品。 |

# Execution Waves
| Wave | Leaves |
| --- | --- |
| W1 | TP-01.01、TP-02.01、TP-02.02 |
| W2 | TP-01.02、TP-03.01 |
| W3 | TP-03.02、TP-04.01 |
| W4 | TP-04.02 |

# Runtime Workflow Contract
- Allowed tools: `rg`, `sed`, `git`, `gh run list`, `auto-tasks` validators, `apply_patch`.
- Forbidden actions: branch switch, rebase, push, workflow trigger, production secret access, deployment, runtime code edits.
- Evidence: file diff, validator output, placeholder scan, source links in `RESEARCH.md`.
- Failure policy: if a source/version cannot be verified, mark it as uncertain instead of asserting.

# Next Executable Leaves
| Node ID | Action |
| --- | --- |
| - | - |

# Dependency Graph
```text
TP-01.01 -> TP-01.02 -> TP-03.01
TP-02.01 -> TP-03.01
TP-02.02 -> TP-03.01
TP-03.01 -> TP-03.02 -> TP-04.01 -> TP-04.02
```

# Rollback Protocol
- 恢复 `INDEX.md` 当前任务行
- 恢复本任务目录到初始化状态
- 不得影响其他任务目录
