# Plan

## Planning Summary
本任务把发布前最后一段证据从散落脚本升级为 `ReleaseGate` 资源和 `live-release-gate` JSON 输出。当前切片只完成本地可验证 baseline；真实外部 live evidence 仍是下一阶段需要凭证才能完成的工作。

# Lifecycle Gates
| Phase | Gate | Status |
| --- | --- | --- |
| SPEC | 明确 live release required evidence | Done |
| PLAN | 任务树与变更边界成文 | Done |
| BUILD | contract、script、API 暴露和 local-ci 接入 | Done |
| TEST | JSON、shell、ruff、pytest、脚本 dry run | Done |
| REVIEW | 不伪造 live evidence，自审 `shipGate=blocked` | Done |
| SHIP | closeout packet 生成；真实 release 仍 external pending | Done |

禁止跳过任何 gate；真实外部证据缺失时必须保持 `shipGate=blocked`，不得用本地合同通过替代 live release 通过。

# Simplest Path
使用本仓已有 shell/Python gate 模式和 JSON registry，不引入新依赖、不接真实外部系统；所有真实外部证据通过参数或环境变量传入。

# Split Strategy
- `TP-01` 先盘点，不写代码。
- `TP-02` 建契约。
- `TP-03` 建执行器并接入已有 gate。
- `TP-04` 做回归和 API 暴露。
- `TP-05` 做文档与 closeout。

# Execution Waves
| Wave | Nodes | Status |
| --- | --- | --- |
| 1 | TP-01.01 | Done |
| 2 | TP-02.01, TP-02.02 | Done |
| 3 | TP-03.01, TP-03.02 | Done |
| 4 | TP-04.01, TP-04.02 | Done |
| 5 | TP-05.01, TP-05.02 | Done |

# Runtime Workflow Contract
- allowed_tools: shell read/verify、apply_patch、pytest、ruff、auto-tasks validation scripts。
- forbidden_actions: push、真实外部 live 调用、输出真实 secret、删除历史任务证据。
- expected_output_schema: ReleaseGate JSON、任务 closeout packet。
- evidence_required: 命令输出、测试结果、文档路径、contract 路径。
- stop_conditions: 本地 gate 失败且无法定位；真实外部凭证缺失仅记录 pending，不停止本地 baseline。

# Next Executable Leaves
- None. 本地 baseline 已完成；真实 live release 验证依赖外部凭证和环境。

# Dependency Graph
```text
TP-01.01
  -> TP-02.01 -> TP-02.02
  -> TP-03.01 -> TP-03.02
  -> TP-04.01 -> TP-04.02
  -> TP-05.01 -> TP-05.02
```

# Rollback Protocol
- 移除 `scripts/live-release-gate.py` / `.sh` 调用时，必须同步移除 `local-ci.sh`、`public-release-gate.sh`、delivery registry、resource schema、测试和文档引用。
- 不回滚 0038 及更早基础设施任务。
