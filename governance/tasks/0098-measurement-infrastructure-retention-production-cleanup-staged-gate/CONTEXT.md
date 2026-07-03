# Repo Evidence
| Evidence | Result |
| --- | --- |
| `contracts/fate/security/retention-cleanup.json` | 本地 SQLite records/report jobs cleanup baseline。 |
| `contracts/fate/security/externalization-evidence-contract.json` | OIDC/SIEM/retention cleaner 外部化证据契约和反伪造负例。 |
| `scripts/security-externalization-gate.py` | 已验证 retentionCleaner live evidence schema。 |
| `tests/regression/test_retention_cleanup.py` | 已覆盖本地 cleanup smoke 和 registry/local-ci wiring。 |
| `tests/regression/test_production_security_gate.py` | 已覆盖 production security 和 externalization gate。 |

# Constraints Matrix
| Constraint | Handling |
| --- | --- |
| 不伪造生产清理 | 默认 `shipGate=blocked`，真实 live 仍待外部验证。 |
| 不连外部服务 | gate 只读本地 contract/evidence JSON。 |
| 不泄露敏感值 | proof refs 只允许 `evidence://`、`artifact://`、`ci-artifact://`。 |
| 不重复实现 cleanup | 0098 不改 `retention_cleanup.py`，只加 staged evidence gate。 |

# Critical Ambiguities
- 是否要真实 Postgres cleanup：不做，留给外部 live task。
- 是否要生产 scheduler：不做，只定义 proof-ref 契约。
- 是否要将 dry-run 视为生产通过：不做，shipGate 保持 blocked。

# Assumptions and Falsification
| Assumption | Falsifier |
| --- | --- |
| 0091 local cleanup baseline 可作为 staged gate 前置 | retention cleanup smoke 或 tests 失败。 |
| staged gate 应独立于 OIDC/SIEM 总 gate | local-ci 无法单独定位 retention production cleanup 证据缺口。 |
| 反伪造应先于 live 接入 | fake raw URL / production_deleted marker 被接受。 |

# Change Boundary
- 新增 security contract、gate script、wrapper、regression test。
- 更新 security registry/policy、local-ci、AGENTS、API docs、roadmap 和任务包。
- 不改数据库 schema，不改 cleanup runtime，不改生产配置。

# Risk Matrix
| Risk | Mitigation |
| --- | --- |
| staged gate 被误解为 live cleanup | summary 和文档固定 `shipGate=blocked`。 |
| evidence 泄露真实 endpoint/DSN | forbidden fragments 和 proof-ref prefix gate。 |
| local-ci 漏接线 | regression 断言 local-ci 包含 gate 和 test。 |

# Debug Evidence Contract
- 调试模式: Optional
- Not required. 本任务是 staged contract/gate 增强。

# Task Package Context Map
| Node ID | Context |
| --- | --- |
| TP-01.01 | Existing retention/security contracts and tests. |
| TP-02.01 | New staged contract. |
| TP-02.02 | New gate script and wrapper. |
| TP-03.01 | Registry, policy, local-ci, AGENTS and docs wiring. |
| TP-03.02 | Regression tests and anti-forgery cases. |
| TP-04.01 | Final validation evidence. |
