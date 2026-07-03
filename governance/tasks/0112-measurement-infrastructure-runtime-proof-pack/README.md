# Task Overview
- Task ID: `0112`
- Slug: `measurement-infrastructure-runtime-proof-pack`
- Objective: `执行 0111 后续 W2 切片：新增 runtime proof pack 聚合契约与 gate，把 runtime backend、Postgres public webhook live、external secret provider、multi-replica runtime 和 exactly-once 非声明边界统一为可审计 runtime proof 资源；复用既有子 gate，不连接真实外部系统，不保存生产凭证、DSN、URL、报告正文或用户输入，并接入 local-ci、certification 和 current audit bundle。`
- Status: `Done`

## In Scope
- 新增 `contracts/fate/delivery/runtime-proof-pack.json` 与 `schemas/runtime-proof.schema.json`。
- 新增 `scripts/runtime-proof-gate.py/.sh`。
- 新增 `tests/regression/test_runtime_proof_gate.py`。
- 将 runtime proof gate 接入 `scripts/local-ci.sh`、`measurement-infrastructure-certification.py` 和 current audit bundle artifact index。
- 更新 delivery/scripts AGENTS、路线图和任务索引。

## Out of Scope
- 不连接真实 Postgres、Webhook receiver、Vault/KMS、监控平台或 Bot。
- 不声明 production ready、外部 live passed 或 exactly-once。
- 不替代 `postgres-public-webhook-live-smoke`、`external-secret-provider-gate` 或 `multi-replica-runtime-gate` 的子系统判断。
- 不保存真实 DSN、URL、token、secret、报告正文、用户输入或生产日志。

## Task Package Tree
```text
TP-01 运行时证据事实扫描
TP-02 runtime proof pack 契约落盘
TP-03 聚合 gate 与 local-ci/certification/audit 接入
TP-04 回归测试与文档同步
TP-05 验证、提交推送与交付证据
```

## Requirement Alignment
| Requirement | Alignment |
| --- | --- |
| W2 Runtime proof | 聚合 external backend、public webhook、external secret provider、multi-replica 和 exactly-once 边界。 |
| 复用成熟/既有 gate | 只调用已有 runtime/backend/secret/multi-replica gate，不重写子系统逻辑。 |
| 不伪造 live | 默认 `runtimeProofStatus=external_connectivity_pending`，`shipGate.status=blocked`。 |
| 审计可追踪 | local-ci、certification、current audit bundle 都能看到 runtime proof artifact。 |

## Task Package Overview
| Node ID | Status | Evidence |
| --- | --- | --- |
| TP-01 | Done | 扫描 runtime/security/observability/delivery 现有契约与 gate。 |
| TP-02 | Done | `runtime-proof-pack.json` 与 schema 已新增。 |
| TP-03 | Done | gate、local-ci、certification 和 audit bundle 已接线。 |
| TP-04 | Done | 回归测试、AGENTS、路线图已同步。 |
| TP-05 | Done | 本地验证通过；提交推送由最终交付执行。 |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
