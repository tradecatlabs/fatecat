# Repo Evidence
| Source | Evidence |
| --- | --- |
| `git status --short --branch` | `main...origin/main` clean after 0081 push, then 0082 implementation creates tracked diff |
| `governance/tasks/INDEX.md` | 0081 Done；0048 Bot live remains Blocked |
| `contracts/fate/observability/otel-slo-evidence-contract.json` | 0064 只覆盖 collector/SLO dry-run contract baseline |
| `scripts/otel-collector-slo-gate.py` | dry-run gate 不能证明真实 trace backend、metrics backend、alert route 或 incident drill |
| `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` | OTel backend、SLO dashboard、alert live、incident drill 仍属外部连通验证 |
| `scripts/local-ci.sh` | quick profile 已有 observability dry-run gates，可接入 staged backend/SLO artifact |

# Constraints Matrix
| Constraint | Handling |
| --- | --- |
| 不伪造 live | gate 默认 pending；live evidence 只有完整脱敏 proof refs 才允许通过 |
| 不泄露秘密 | 拒绝 token/secret/password/raw URL/生产 payload 等敏感片段 |
| 不重写 0064 | 新增独立 staged gate，0064 继续保持 dry-run collector/SLO gate |
| 不新增外部依赖 | 只用 Python 标准库和现有门禁模式 |
| 不扩大业务面 | 不改报告生成、业务 API、collector runtime 或外部平台配置 |

# Change Boundary
- Allowed: `contracts/fate/observability/`、`scripts/otel-backend-slo-gate.py/.sh`、`scripts/local-ci.sh`、`tests/regression/`、`docs/reference-materials/`、`governance/tasks/0082-*`、`scripts/AGENTS.md`、`tests/AGENTS.md`。
- Read-only context: 0064 dry-run contract/gate、0081 runtime evidence pattern、roadmap、observability registry。
- Forbidden: 真实 backend 连接、真实 URL/secret 入仓、生产 trace/metrics/logs 入仓、将 pending 写成 production live。

# Risk Matrix
| Risk | Mitigation |
| --- | --- |
| staged evidence 被误读成真实 live | summary 和 docs 明确 `外部连通验证待执行` |
| operator 提供 fake proof refs | gate 拒绝 localhost、placeholder、debug exporter、sample 等伪证片段 |
| proof refs 泄露外部系统 URL 或 token | gate 对输入和输出做敏感片段扫描 |
| 0064 dry-run 与 0082 live 边界混淆 | registry/schema invariant 明确 staged gate 不代表真实 collector/runtime/backend 已完成 |

# Assumptions and Falsification
- Assumption: 下一个有价值切片是 backend/SLO staged evidence gate，而不是继续写自然语言 pending 清单。
- Falsifier: 如果已有 gate 能校验真实 trace backend、metrics backend、SLO dashboard、alert route、error budget 和 incident drill proof refs，则本任务应收缩为 registry/docs 接线。
- Assumption: live proof refs 只保存 `evidence://`、`artifact://`、`ci-artifact://` 等脱敏句柄。
- Falsifier: 如果生产审计必须保存真实 dashboard/alert URL，则应另开受保护外部证据仓，不能放进本 repo。

# Critical Ambiguities
- 当前没有真实 OTel collector runtime、trace backend、metrics backend、alert platform、生产流量窗口或 incident drill 权限。
- 本任务只能证明 contract/gate/schema/local-ci artifact 可工作；真实 live 仍需 operator 后续提供外部环境证据。

# Debug Evidence Contract
- 调试模式: Optional

Not required. 本任务是新增 evidence tooling，不是 bugfix；若 gate、CI 或 regression 失败，则记录失败命令、根因、修复和回归证据。

# Task Package Context Map
| Node ID | Context |
| --- | --- |
| TP-01.01 | observability registry、0064 dry-run contract/gate、roadmap、local-ci |
| TP-01.02 | pending/live/non-claim、privacy boundary、external validation boundary |
| TP-02.01 | live evidence required fields、proof ref allowlist、backend type allowlist |
| TP-02.02 | negative cases、sensitive scan、raw URL rejection |
| TP-03.01 | `scripts/otel-backend-slo-gate.py/.sh` |
| TP-03.02 | `contracts/fate/observability/*`、`scripts/local-ci.sh`、AGENTS、docs |
| TP-04.01 | `tests/regression/test_otel_backend_slo_gate.py` |
| TP-04.02 | syntax、focused pytest、ruff、secret scan、quick CI、task validators |
| TP-05.01 | closeout docs and external pending list |
| TP-05.02 | git/CI delivery evidence boundary |
