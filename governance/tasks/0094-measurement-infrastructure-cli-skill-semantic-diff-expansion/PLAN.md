# Planning Summary
0094 把 0090 的 multi-surface gate 从“API/Web/Bot Markdown 同源 + CLI/Skill not_in_scope”升级为“API/Web/Bot Markdown hash 同源 + CLI/Skill non-Markdown evidence surfaces”。核心不是扩大 hash 比较范围，而是让 CLI/Skill 各自用正确形态证明同源链路。

# Lifecycle Gates
| Gate | Requirement | Result |
| --- | --- | --- |
| SPEC | 明确 CLI/Skill 是 non-Markdown evidence surfaces。 | Done |
| PLAN | 拆成现状复核、脚本扩展、契约文档测试、验证 closeout。 | Done |
| BUILD | 扩展脚本、contract、registry、docs、AGENTS、tests。 | Done |
| TEST | semantic diff gate、focused pytest、ruff、secret scan、local-ci quick 已通过。 | Done |
| REVIEW | 检查不保存正文、不假称 live、不把 CLI 加入 Markdown hash。 | Done |
| SHIP | 提交推送前必须 clean worktree 和本地 quick 证据。 | Done |

不得跳过 gate；任一 SPEC/PLAN/BUILD/TEST/REVIEW/SHIP gate 缺证据时，0094 不得 closeout。

# Simplest Path
1. 保持现有 API/Web/Bot Markdown renderers 不变。
2. 复用 0093 `capability-cli-smoke.py` 作为 CLI evidence。
3. 使用 tracked Skill 文档静态 snippets 作为 Skill command chain evidence，不依赖本机绝对 validator。
4. 只更新 contract/test/docs，不新增新的基础设施抽象。

# Split Strategy
| Package | Scope |
| --- | --- |
| TP-01 | 复核现状和可复用材料。 |
| TP-02 | 实现 CLI/Skill evidence surfaces。 |
| TP-03 | 更新契约、文档、测试。 |
| TP-04 | 验证、closeout、Git 交付。 |

# Execution Waves
| Wave | Nodes | Notes |
| --- | --- | --- |
| Wave 1 | TP-01 | 只读复核。 |
| Wave 2 | TP-02 | 修改脚本。 |
| Wave 3 | TP-03 | 修改 contract/docs/tests。 |
| Wave 4 | TP-04 | 验证与交付。 |

# Runtime Workflow Contract
```text
multi-surface-semantic-diff.sh
  -> API/Web/Bot Markdown surfaces
     -> normalized markdown semantic hash equality
  -> CLI evidence surface
     -> capability-cli-smoke.run_smoke()
     -> CapabilityExecutor/provider registry proof
  -> Agent Skill evidence surface
     -> SKILL.md + references/commands.md + references/io-contract.md snippets
     -> canonical command chain proof
  -> hash-only / key-only JSON evidence
```

# Next Executable Leaves
| Node ID | Action |
| --- | --- |
| TP-04.02 | 运行 local-ci quick、secret scan、task validator |
| TP-04.03 | 回填最终状态、提交推送 |

# Dependency Graph
```text
TP-01.01 -> TP-01.02 -> TP-02.01 -> TP-02.02 -> TP-03.01 -> TP-03.02 -> TP-03.03 -> TP-04.01 -> TP-04.02 -> TP-04.03
```

# Rollback Protocol
- 恢复 `INDEX.md` 当前任务行
- 恢复本任务目录到初始化状态
- 不得影响其他任务目录
