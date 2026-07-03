# Repo Evidence
| Source | Evidence |
| --- | --- |
| `git status --short --branch` | `main...origin/main` clean after 0083 push, then 0084 implementation creates tracked diff |
| `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` | 0084 是 Provider drift scanner，本地可执行 |
| `scripts/provider-lifecycle-gate.py` | 已校验 versionLock、lifecycle、source/license/resource manifest、promotionGate、deprecation 和 vendor production permission |
| `scripts/provider-dependency-smoke.py` | 已通过统一 `CapabilityExecutor` 执行 production provider 脱敏固定样例 |
| `domains/fate-analysis/services/fate-core/src/fate_core/capabilities/executor.py` | provider validate/calculate 外层已有 `trace_span` |
| `contracts/fate/observability/registry.json` | `signal.provider_report_traces` 已登记 provider/report trace spans |
| `tools/reference-repos/vendor_sources.json` | vendor production dependency、licenseStatus、snapshotSha256 和 usageRole 是供应链真相源 |

# Constraints Matrix
| Constraint | Handling |
| --- | --- |
| 不重复 provider 模型 | scanner 复用 runtime provider metadata、lifecycle gate、dependency smoke 和 vendor manifest |
| 不伪造外部 live | 只输出本地 drift report，保留 `外部连通验证待执行` |
| 不泄露隐私 | scanner summary 不写样例 payload、姓名、出生地区、报告正文、token、secret、DSN |
| 不新增外部依赖 | 只使用 Python 标准库、现有 `CapabilityExecutor` 和现有脚本 |
| 不做法律结论 | licenseStatus 只按 manifest 机器检查，人工法律复核仍待执行 |

# Change Boundary
- Allowed: `contracts/fate/capabilities/`、`scripts/provider-drift-scanner.py/.sh`、`scripts/local-ci.sh`、`tests/regression/`、`docs/reference-materials/operations/`、`docs/reference-materials/roadmap/`、`governance/tasks/0084-*`、AGENTS。
- Read-only context: provider lifecycle gate、provider dependency smoke、CapabilityExecutor、vendor manifest、observability trace signal。
- Forbidden: 真实公网依赖、外部 trace backend、法务许可判断、生产账号、真实用户数据。

# Risk Matrix
| Risk | Mitigation |
| --- | --- |
| drift report 被误读成公网 live | summary 和 docs 明确 external connectivity pending |
| scanner 只做静态 manifest | 捕获本地 provider.validate/provider.calculate spans，并执行 dependency smoke |
| source/license 漂移未被发现 | 对 source/runtime/contract/test/license refs 和 vendor refs 做路径与 manifest 校验 |
| 报告泄露样例值 | 契约列出 forbidden fragments，scanner 最后做 summary privacy assertion |

# Assumptions and Falsification
- Assumption: 0084 的最小正确切片是 drift scanner，而不是接公网 provider live smoke。
- Falsifier: 如果已有门禁能同时对比 lifecycle、dependency smoke、trace spans、source refs、license refs 和 vendor refs，则本任务应收缩为文档接线。
- Assumption: production provider 的外部依赖状态由 vendor manifest 和 smoke 共同证明。
- Falsifier: 如果 production provider 依赖真实 SaaS/API，则需要另开 live smoke 和 secret 管理任务，不能放进本地 scanner。

# Critical Ambiguities
- 当前没有真实公网外部依赖、外部 trace backend、人工法律许可复核或跨版本升级流程。
- 本任务只证明本地 drift 可检测；真实 live 和法律结论仍需外部证据。

# Debug Evidence Contract
- 调试模式: Optional

Not required. 本任务是 provider tooling hardening，不是 bugfix；若 scanner、CI 或 regression 失败，则记录失败命令、根因、修复和回归证据。

# Task Package Context Map
| Node ID | Context |
| --- | --- |
| TP-01.01 | provider lifecycle gate、dependency smoke、registry、vendor manifest、roadmap |
| TP-01.02 | dependency/source/license/trace drift boundary |
| TP-02.01 | provider drift contract fields and forbidden fragments |
| TP-02.02 | trace spans、dependency refs、source refs、license evidence、vendor metadata |
| TP-03.01 | `scripts/provider-drift-scanner.py/.sh` |
| TP-03.02 | `contracts/fate/capabilities/*`、`scripts/local-ci.sh`、AGENTS、operations docs、roadmap |
| TP-04.01 | `tests/regression/test_provider_drift_scanner.py` and `test_capability_protocol.py` |
| TP-04.02 | JSON、scanner、pytest、ruff、secret scan、quick CI、task validators |
| TP-05.01 | closeout docs and external pending list |
| TP-05.02 | git/CI delivery evidence boundary |
