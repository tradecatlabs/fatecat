# Planning Summary
0101 是 0099 计划中的 Wave A A2：在已有 release/audit/provider/core/security/SRE/runtime/developer gate 之上增加一个只读聚合层。正确终态不是再造一套门禁，而是把现有机器可读证据聚成一个 certification dry-run summary，让任何人一眼看到哪些域 passed、blocked、pending 或 failed。

# Lifecycle Gates
不得跳过 gate；每个 gate 都必须有文件或命令证据。

| Gate | Exit Criteria |
| --- | --- |
| SPEC | 明确 certification 只消费 local-ci evidence，不连接外部系统，不声明 100%。 |
| PLAN | 任务树、范围、风险、验证命令和 rollback protocol 写入任务包。 |
| BUILD | contract、CLI/wrapper、local-ci 接线、AGENTS/docs 更新完成。 |
| TEST | smoke、focused pytest、ruff、quick local-ci、secret scan、diff check 通过或如实记录失败。 |
| REVIEW | 自审 blocked/pending/failed 语义、隐私边界、任务文档和索引一致性。 |
| SHIP | closeout validator 通过，commit/push 完成，远端状态如实记录。 |

# Simplest Path
1. 复用已有 gate JSON，不解析日志、不调用外部 live。
2. 用静态 `DOMAIN_SPECS` 映射分域和证据文件，避免引入新 registry。
3. 缺证据直接 `failed`，外部待执行保持 `blocked/pending`，全部 passed 才可声明 `canClaim100Percent=true`。
4. 通过 local-ci 输出 artifact，供 release/audit 后续复核。

# Split Strategy
| Node | Split Reason |
| --- | --- |
| TP-01 | 先锁定 100% 认证边界，防止实现时过度声明。 |
| TP-02 | 代码实现与接线集中在最小文件集。 |
| TP-03 | 验证独立，能快速发现语义和格式问题。 |
| TP-04 | closeout 与版本控制单独处理，避免证据文件自己漂移。 |

# Execution Waves
| Wave | Leaves | Parallelizable |
| --- | --- | --- |
| W1 | TP-01.01, TP-01.02 | Yes |
| W2 | TP-02.01 | No |
| W3 | TP-02.02, TP-03.01 | Yes |
| W4 | TP-03.02 | No |
| W5 | TP-04.01, TP-04.02 | No |

# Runtime Workflow Contract
- 允许工具：`rg`、`sed`、`pytest`、`ruff`、项目脚本、`git`。
- 禁止动作：切换分支、删除外部证据、修改真实凭证、伪造外部 live evidence。
- 输出：contract JSON、certification summary JSON、local-ci artifact、任务 closeout 文档。
- 失败策略：结构性失败先修脚本或测试；外部 pending 不修成 passed，只如实保留。

# Next Executable Leaves
- 当前 ready：TP-03.02、TP-04.01。
- TP-04.02 依赖 TP-03.02 和 TP-04.01 通过。

# Dependency Graph
```text
TP-01.01 -> TP-01.02 -> TP-02.01 -> TP-02.02 -> TP-03.02 -> TP-04.01 -> TP-04.02
TP-02.01 -> TP-03.01 -> TP-03.02
```

# Rollback Protocol
- 删除 `measurement-infrastructure-certification` contract/script/test 和 local-ci 接线。
- 恢复相关 `AGENTS.md`、roadmap/API 文档、`governance/tasks/INDEX.md` 当前任务行。
- 不触碰已提交的 0100 provider drift trend gate。
