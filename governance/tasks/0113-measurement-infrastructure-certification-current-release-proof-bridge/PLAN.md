# Planning Summary
0113 是 certification evidence bridge 切片。正确终态不是重新跑一套认证系统，而是让现有 certification aggregator 支持一个明确、可追踪、可审计的 sidecar release proof 输入。

# Lifecycle Gates
不得跳过 gate；任一 gate 缺少命令、文件或明确豁免证据时，本任务不能 closeout。

| Gate | Exit Criteria | Status |
| --- | --- | --- |
| SPEC | 明确 sidecar 只覆盖 current-release-proof，不覆盖 live gate | Done |
| PLAN | 拆成脚本、契约、测试、文档和交付 | Done |
| BUILD | 新增 CLI 参数、override 记录和 summary 字段 | Done |
| TEST | targeted pytest、CLI smoke、ruff/format 和任务文档校验通过 | Done |
| REVIEW | 确认 sidecar 不绕过生产 live 阻断 | Done |
| SHIP | 提交推送并复核状态 | Done |

# Simplest Path
1. 在 certification script 中增加 `--current-release-proof-json`。
2. 用一个小型 `evidence_overrides` map 映射逻辑文件名到 Path。
3. `_evaluate_domain()` 优先读取 override path，并记录 source。
4. 保持 `live-release-gate.json` 仍从 evidence dir 读取。
5. 更新 contract/test/docs，证明语义不漂移。

# Split Strategy
| Node | Split Reason |
| --- | --- |
| TP-01 | 先确认盲区，避免误把 release live 和 release proof 合并。 |
| TP-02 | 最小代码切片：sidecar 参数和 override evidence source。 |
| TP-03 | 测试、契约和路线图同步，避免文档漂移。 |
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
| - | - |

# Runtime Workflow Contract
- Allowed tools: `rg`, `sed`, `jq`, `pytest`, `ruff`, `bash scripts/measurement-infrastructure-certification.sh`, `apply_patch`, `git`.
- Forbidden actions: production deployment, branch switch, rebase, reset, real secret access, production database access, live webhook setup.
- Evidence: targeted pytest output, certification sidecar output JSON, ruff output, task docs validator, secret scan, git status.

# Dependency Graph
```text
TP-01 -> TP-02 -> TP-03 -> TP-04
```

# Rollback Protocol
- Remove `--current-release-proof-json` argument and override logic from `scripts/measurement-infrastructure-certification.py`.
- Remove new tests from `tests/regression/test_measurement_infrastructure_certification.py`.
- Revert contract, roadmap and task index edits.
