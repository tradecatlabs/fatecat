# Task Overview
- Task ID: `0098`
- Slug: `measurement-infrastructure-retention-production-cleanup-staged-gate`
- Objective: `执行 0095 Wave A Next-03：在 0091 本地 SQLite retention cleanup baseline 和 0083 OIDC/SIEM/retention staged evidence gate 之上，新增本地可验证的 retention production cleanup staged gate；聚合 production scheduler、Postgres production cleanup、SIEM/log retention 三类证据口径，默认无外部环境时输出 blocked/pending summary，提供反伪造负例，拒绝 raw URL、placeholder proof、缺 smoke summary、production_deleted marker 或敏感值；不连接真实 Postgres、scheduler、SIEM，不执行生产删除，不声明 live passed。`
- Status: `Done`

## In Scope
- 新增 `contracts/fate/security/retention-production-cleanup-staged.json`。
- 新增 `scripts/retention-production-cleanup-gate.py/.sh`。
- 新增 `tests/regression/test_retention_production_cleanup_gate.py`。
- 接入 `production-security-policy.json`、`security/registry.json`、`local-ci.sh` 和相关 AGENTS / API / roadmap 文档。

## Out of Scope
- 不连接真实 Postgres、scheduler、SIEM、WORM 或云日志平台。
- 不执行生产删除。
- 不声明 retention live passed、production ready 或 exactly-once。
- 不保存真实 DSN、endpoint、token、secret、用户输入、报告正文、生产日志或真实删除结果。

## Task Package Tree
```text
TP-01 复核 retention 现状
  TP-01.01 读取 0091、0083、retention/security contracts、scripts、tests
TP-02 新增 staged contract/gate
  TP-02.01 新增 retention production cleanup staged contract
  TP-02.02 新增 gate 脚本与 shell wrapper
TP-03 接线与测试
  TP-03.01 接入 registry/policy/local-ci/AGENTS/docs
  TP-03.02 新增 regression 正向、live fixture 与负向测试
TP-04 验证与收口
  TP-04.01 运行 focused gate/tests、secret scan、quick local-ci 和 task closeout validator
```

## Requirement Alignment
| Requirement | Alignment |
| --- | --- |
| scheduler/Postgres/SIEM 三类证据 | contract 中 `requiredEvidenceAreas` 明确三类证据字段与 proof-ref。 |
| 默认 blocked/pending | gate 无 evidence 时输出 `shipGate=blocked` 与 `外部连通验证待执行`。 |
| 反伪造 | contract/gate 拒绝 raw URL、缺 smoke summary、production_deleted marker 和敏感片段。 |
| 不执行生产删除 | gate 只读 JSON evidence，不连接外部服务，不执行 cleanup。 |

## Task Package Overview
| Node ID | Status | Evidence |
| --- | --- | --- |
| TP-01.01 | Done | Existing retention/security files inspected. |
| TP-02.01 | Done | staged contract added. |
| TP-02.02 | Done | gate script and wrapper added. |
| TP-03.01 | Done | registry/policy/local-ci/AGENTS/docs wired. |
| TP-03.02 | Done | focused pytest 18 passed. |
| TP-04.01 | Done | final gate/tests/secret scan/quick local-ci/closeout validator passed. |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
