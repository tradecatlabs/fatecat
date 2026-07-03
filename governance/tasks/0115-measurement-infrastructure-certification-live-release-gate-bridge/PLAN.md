# Planning Summary
0115 是 certification evidence bridge 的第三刀。0113 解决 final current release proof sidecar；0114 解决 final current audit bundle sidecar；0115 解决 final live release gate sidecar，避免 certification release domain 被 stale local-ci live gate 锁住。

# Lifecycle Gates
不得跳过 gate；任一 gate 缺少命令、文件或明确豁免证据时，本任务不能 closeout。

| Gate | Exit Criteria | Status |
| --- | --- | --- |
| SPEC | 明确 live gate sidecar 只覆盖 release domain 的 live gate 逻辑文件 | Done |
| PLAN | 拆成脚本、契约、测试、文档和交付 | Done |
| BUILD | 新增 CLI 参数、override 映射和 source metadata 复用 | Done |
| TEST | targeted pytest、CLI smoke、ruff/format 和任务文档校验通过 | Done |
| REVIEW | 确认 live sidecar 不绕过 release proof/audit/live 阻断 | Done |
| SHIP | 提交推送并复核状态 | Done |

# Simplest Path
1. 在 certification script 中增加 `--live-release-gate-json`。
2. 复用现有 `evidence_overrides` map。
3. 将 sidecar 映射到逻辑路径 `live-release-gate.json`。
4. 保持 `current-release-proof.json` 和 `current-audit-bundle/current-audit-bundle.json` 独立。
5. 更新 contract/test/docs，证明语义不漂移。

# Split Strategy
| Node | Split Reason |
| --- | --- |
| TP-01 | 先确认 stale live gate 盲区。 |
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
| - | - |

# Runtime Workflow Contract
- Allowed tools: `rg`, `sed`, `jq`, `pytest`, `ruff`, `bash scripts/measurement-infrastructure-certification.sh`, `bash scripts/live-release-gate.sh`, `apply_patch`, `git`.
- Forbidden actions: production deployment, branch switch, rebase, reset, real secret access, production database access, live webhook setup.
- Evidence: targeted pytest output, live gate sidecar output JSON, certification sidecar output JSON, ruff output, task docs validator, secret scan, git status.

# Dependency Graph
```text
TP-01 -> TP-02 -> TP-03 -> TP-04
```

# Document-Driven Fields
| Field | Value |
| --- | --- |
| Operating model update | not needed: no project purpose or operating model change. |
| Toolchain model update | not needed: no new tool, only one optional argument on an existing gate. |
| Process update | not needed: certification process remains aggregator-only. |
| Source-of-truth updates | updated: certification contract, scripts/audit AGENTS and roadmap. |
| Local README/AGENTS impact | updated: `scripts/AGENTS.md` and `contracts/fate/audit/AGENTS.md`. |
| Contract/catalog/schema impact | updated: `contracts/fate/audit/measurement-infrastructure-certification.json`. |
| ADR/Gate/module-context impact | not needed: exact-path sidecar bridge follows 0113/0114 precedent. |
| Documentation exemption reason | no exemption for changed contract/docs; all owning docs are in scope. |
| Validation evidence | targeted pytest, local-ci quick, CLI sidecar smoke, docs validator, ruff and secret scan passed. |

# Rollback Protocol
- Remove `--live-release-gate-json` argument and override mapping from `scripts/measurement-infrastructure-certification.py`.
- Remove new tests from `tests/regression/test_measurement_infrastructure_certification.py`.
- Revert contract, AGENTS, roadmap and task index edits.
