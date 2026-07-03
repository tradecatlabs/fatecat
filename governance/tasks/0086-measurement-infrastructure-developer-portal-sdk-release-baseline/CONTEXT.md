# Repo Evidence
| Source | Evidence |
| --- | --- |
| `git status --short --branch` | `main...origin/main` clean before 0086 implementation |
| `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` | 0086 is Developer portal and SDK release baseline |
| `contracts/fate/developer/developer-platform.json` | 0067 baseline existed but fixed snapshot and portal gate were not present |
| `scripts/developer-docs-smoke.py` | existing OpenAPI/sandbox/examples smoke was available for reuse |
| `scripts/developer-platform-gate.py` | existing SDK/package baseline, sandbox token and changelog gate was available for reuse |
| `contracts/fate/developer/sandbox.json` | two local deterministic 北京/测试 sandbox fixtures existed |

# Constraints Matrix
| Constraint | Handling |
| --- | --- |
| 不伪造 SDK 发布 | `packageRegistryStatus=not_published` and `publishEvidence=null` remain required |
| 不伪造公网 portal | `externalPortalStatus=not_implemented` remains required |
| 不伪造 sandbox token live | `liveSandboxTokenService=false` remains required |
| 不保存响应正文 | snapshot stores digest and stable shape only |
| 不保存真实地区/用户/凭证 | privacy scan rejects known forbidden fragments and secret-looking values |

# Change Boundary
- Allowed: `contracts/fate/developer/*`、`docs/reference-materials/developer/*`、`docs/reference-materials/operations/*`、`scripts/developer-portal-gate.*`、`scripts/local-ci.sh`、`tests/regression/test_developer_portal_gate.py`、AGENTS、task docs、roadmap。
- Read-only context: production capability execution, report generation logic, public deployment scripts。
- Forbidden: publishing package registries, adding real tokens, changing production API semantics, storing report bodies.

# Risk Matrix
| Risk | Mitigation |
| --- | --- |
| local baseline 被误读为公网发布 | contract/gate summary hard-codes externalPortalLive=false and publishedSdkPackages=0 |
| snapshot 泄露报告正文 | only digest and stable shape are stored |
| dynamic response timestamp breaks snapshot | gate removes `/meta/calculatedAt` before digest |
| SDK smoke 依赖 Node 不稳定 | Node syntax runs when available; otherwise shape-only fallback is recorded |
| docs drift | API changelog, AGENTS, operations docs and roadmap updated |

# Debug Evidence Contract
- 调试模式: Optional

本任务是 release baseline hardening；若 gate、CI 或 regression 失败，需要记录失败命令、根因和回归证据。

# Assumptions and Falsification

- Assumption: 0086 的正确切片是本地 release-readiness baseline，不是外部公网发布。
- Falsifier: 如果 gate summary 声称 PyPI/npm、公网 portal 或 sandbox token live 已完成，本任务失败。
- Assumption: snapshot 可通过删除 `/meta/calculatedAt` 后稳定 hash。
- Falsifier: 如果 digest 仍非确定性，必须缩小 snapshot 到结构断言或调整动态字段清单。

# Critical Ambiguities

- 公网 developer portal、package registry publication 和 public sandbox token issuer 不在本任务内。
- Node 语法检查在本地可执行；若外部 runner 缺 Node，gate 使用 shape-only fallback，不把它写成 registry install smoke。

# Task Package Context Map
| Node ID | Context |
| --- | --- |
| TP-01.01 | developer platform、sandbox、examples、docs smoke、roadmap |
| TP-02.01 | portal/sdk/snapshot/no-overclaim boundary |
| TP-03.01 | contracts and docs deliverables |
| TP-04.01 | developer portal gate |
| TP-04.02 | local-ci、tests、AGENTS、docs、changelog |
| TP-05.01 | syntax、gate、pytest、quick CI |
| TP-05.02 | no remote CI pre-claim boundary |
