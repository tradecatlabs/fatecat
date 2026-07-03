# Planning Summary

0116 的目标不是关闭外部 live，而是把所有外部待验证项变成可关闭资源。当前 occurrence list 是审计扫描结果，不是执行计划；本切片新增 closure gate，把它转换成 owner/凭证/证据/命令/关闭条件完整的 audit closure plan。

# Lifecycle Gates
不得跳过 gate；任一 gate 缺少命令、文件或明确豁免证据时，本任务不能 closeout。

| Gate | Exit Criteria | Status |
| --- | --- | --- |
| SPEC | 明确 closure plan 只计划关闭，不证明 live | Done |
| PLAN | 拆成 contract、script、local-ci、test、docs | Done |
| BUILD | closure gate 与 local-ci 接线完成 | Done |
| TEST | targeted pytest、CLI smoke、local-ci quick、ruff/format 通过 | Done |
| REVIEW | 确认隐私边界和 non-claim 没有漂移 | Done |
| SHIP | 提交推送并记录远端状态 | In Progress |

# Simplest Path
1. 读取 current audit bundle 的 `pending-external-validations.json`。
2. 用关键词 profile 将 occurrence 分到 release/runtime/security/observability/developer/audit/manual 类别。
3. 为每项输出 owner、credentialDependencies、requiredEvidence、verificationCommands、closureCondition。
4. 任何 pending item 存在时，`shipGate.status=blocked`。
5. 接入 local-ci 和回归测试。

# Split Strategy
| Node | Split Reason |
| --- | --- |
| TP-01 | 先确认 occurrence 清单不可分派。 |
| TP-02 | 单独实现 contract 和 generator。 |
| TP-03 | 单独处理 local-ci、测试和文档接线。 |
| TP-04 | 单独收敛验证、审查和版本控制。 |

# Execution Waves
| Wave | Leaves |
| --- | --- |
| W1 | TP-01 |
| W2 | TP-02 |
| W3 | TP-03 |
| W4 | TP-04 |

# Dependency Graph
```text
TP-01 -> TP-02 -> TP-03 -> TP-04
```

# Next Executable Leaves
| Node ID | Action |
| --- | --- |
| - | - |

# Runtime Workflow Contract
- Allowed tools: `rg`, `sed`, `jq`, `pytest`, `ruff`, `bash scripts/external-validation-closure-gate.sh`, `bash scripts/local-ci.sh`, `apply_patch`, `git`.
- Forbidden actions: production deployment, branch switch, rebase, reset, real secret access, production database access, live webhook setup.
- Evidence: targeted pytest output, closure CLI smoke, ruff/format, task docs validator, secret scan, local-ci quick, git status.

# Document-Driven Fields
| Field | Value |
| --- | --- |
| Operating model update | not needed: project positioning unchanged. |
| Toolchain model update | not needed: no new external tool. |
| Process update | updated: local-ci now emits external validation closure gate artifact. |
| Source-of-truth updates | updated: audit contract, scripts/tests AGENTS, roadmap. |
| Local README/AGENTS impact | updated: `scripts/AGENTS.md`, `contracts/fate/audit/AGENTS.md`, `tests/AGENTS.md`. |
| Contract/catalog/schema impact | updated: `contracts/fate/audit/external-validation-closure.json`. |
| ADR/Gate/module-context impact | not needed: follows existing audit gate pattern. |
| Documentation exemption reason | no exemption for changed contract/docs. |
| Validation evidence | targeted pytest passed; CLI smoke passed; ruff/format passed; secret scan passed; task docs validator passed; local-ci quick passed. |

# Rollback Protocol
- Remove `scripts/external-validation-closure-gate.sh` and `.py`.
- Remove `contracts/fate/audit/external-validation-closure.json`.
- Remove local-ci gate call and summary artifact entry.
- Remove `tests/regression/test_external_validation_closure_gate.py`.
- Revert AGENTS, roadmap and task index edits.
