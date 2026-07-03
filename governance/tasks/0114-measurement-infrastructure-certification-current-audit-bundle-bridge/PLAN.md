# Planning Summary
0114 是 certification evidence bridge 的第二刀。0113 解决了 final current release proof sidecar；0114 解决 final current audit bundle sidecar，避免 certification audit domain 被 stale local-ci bundle 锁死。

# Lifecycle Gates
不得跳过 gate；任一 gate 缺少命令、文件或明确豁免证据时，本任务不能 closeout。

| Gate | Exit Criteria | Status |
| --- | --- | --- |
| SPEC | 明确 audit bundle sidecar 只覆盖 audit domain 逻辑文件 | Done |
| PLAN | 拆成脚本、契约、测试、文档和交付 | Done |
| BUILD | 新增 CLI 参数、override 映射和 source metadata 复用 | Done |
| TEST | targeted pytest、CLI smoke、ruff/format 和任务文档校验通过 | Done |
| REVIEW | 确认 audit sidecar 不绕过 release/live 阻断 | Done |
| SHIP | 提交推送并复核状态 | Pending |

# Simplest Path
1. 在 certification script 中增加 `--current-audit-bundle-json`。
2. 复用现有 `evidence_overrides` map。
3. 将 sidecar 映射到逻辑路径 `current-audit-bundle/current-audit-bundle.json`。
4. 保持 `current-release-proof.json` 和 `live-release-gate.json` 独立。
5. 更新 contract/test/docs，证明语义不漂移。

# Split Strategy
| Node | Split Reason |
| --- | --- |
| TP-01 | 先确认 stale audit bundle 盲区。 |
| TP-02 | 最小代码切片：sidecar 参数和 override 映射。 |
| TP-03 | 测试、契约、AGENTS 和路线图同步。 |
| TP-04 | 验证、审查、提交推送。 |

# Execution Waves
| Wave | Leaves |
| --- | --- |
| W1 | TP-01 |
| W2 | TP-02 |
| W3 | TP-03 |
| W4 | TP-04 |

# Next Executable Leaves
| Node ID | Action |
| --- | --- |
| TP-04 | Commit, push and verify remote state. |

# Runtime Workflow Contract
- Allowed tools: `rg`, `sed`, `jq`, `pytest`, `ruff`, `bash scripts/measurement-infrastructure-certification.sh`, `bash scripts/current-audit-bundle.sh`, `apply_patch`, `git`.
- Forbidden actions: production deployment, branch switch, rebase, reset, real secret access, production database access, live webhook setup.
- Evidence: targeted pytest output, certification sidecar output JSON, final audit bundle smoke, ruff output, task docs validator, secret scan, git status.

# Dependency Graph
```text
TP-01 -> TP-02 -> TP-03 -> TP-04
```

# Rollback Protocol
- Remove `--current-audit-bundle-json` argument and override mapping from `scripts/measurement-infrastructure-certification.py`.
- Remove new tests from `tests/regression/test_measurement_infrastructure_certification.py`.
- Revert contract, AGENTS, roadmap and task index edits.
