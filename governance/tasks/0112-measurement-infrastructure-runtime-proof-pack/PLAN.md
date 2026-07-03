# Planning Summary
0112 是 W2 runtime proof pack 聚合切片。正确终态不是新建另一个 runtime backend，也不是复制已有 gate 逻辑，而是把既有 runtime backend、public webhook、external secret provider 和 multi-replica evidence gate 统一成一个上层 proof pack。

# Lifecycle Gates
不得跳过 gate；任一 gate 缺少文件、命令或明确豁免证据时，本任务不能 closeout。

| Gate | Exit Criteria | Status |
| --- | --- | --- |
| SPEC | 明确聚合范围和非 live 边界 | Done |
| PLAN | 拆成契约、gate、CI/audit 接线、测试和交付 | Done |
| BUILD | 新增 runtime proof contract/gate/test/local-ci 接入 | Done |
| TEST | runtime proof gate、targeted pytest、ruff/format 和 quick CI 通过 | Done |
| REVIEW | 确认没有把 pending external 写成 live passed | Done |
| SHIP | 提交推送后记录证据 | Done |

# Simplest Path
1. 只新增 runtime proof pack 契约和 schema。
2. Python gate 导入现有 runtime/secret/multi-replica gate。
3. local-ci 先生成 public webhook allow-missing summary，再调用 runtime proof gate。
4. certification/current-audit bundle 只消费 runtime proof summary，不读取真实外部值。

# Split Strategy
| Node | Split Reason |
| --- | --- |
| TP-01 | 先识别现有子 gate，避免重复造轮子。 |
| TP-02 | 再落 runtime proof pack contract/schema。 |
| TP-03 | 通过脚本、local-ci、certification 和 audit bundle 接线变成可验证门禁。 |
| TP-04 | 用测试和文档锁住 pending/live/negative 语义。 |
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
- Allowed tools: `rg`, `sed`, `jq`, `pytest`, `ruff`, `bash scripts/runtime-proof-gate.sh`, `bash scripts/local-ci.sh`, `apply_patch`, `git`.
- Forbidden actions: production deployment, branch switch, rebase, reset, real secret access, production database access, live webhook receiver setup.
- Evidence: runtime proof JSON, pytest output, ruff output, task docs validator, local-ci output, git status.

# Next Executable Leaves
| Node ID | Action |
| --- | --- |
| - | - |

# Dependency Graph
```text
TP-01 -> TP-02 -> TP-03 -> TP-04 -> TP-05
```

# Rollback Protocol
- Remove `contracts/fate/delivery/runtime-proof-pack.json`, `schemas/runtime-proof.schema.json`, `scripts/runtime-proof-gate.*` and `tests/regression/test_runtime_proof_gate.py`.
- Remove local-ci, certification and current-audit-bundle runtime proof wiring.
- Revert delivery/scripts AGENTS, roadmap and 0112 task index/docs.
