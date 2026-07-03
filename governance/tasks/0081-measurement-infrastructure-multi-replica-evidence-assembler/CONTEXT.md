# Repo Evidence
| Source | Evidence |
| --- | --- |
| `git status --short --branch` | `main...origin/main` clean after 0080 push |
| `governance/tasks/INDEX.md` | 0080 Done; 0048 Bot live remains Blocked |
| `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` | 真实 webhook live passed、外部 Vault/KMS live passed、长期多副本运行 live evidence 和 exactly-once 仍未完成 |
| `contracts/fate/delivery/multi-replica-runtime-contract.json` | 0080 gate 定义 live evidence required fields、minimums、negative cases 和 exactly-once non-claim |
| `scripts/multi-replica-runtime-gate.py` | 可验证 optional `--evidence-json`，但当前没有受控 evidence 生成入口 |
| `scripts/local-ci.sh` | quick profile 已运行 `multi-replica runtime gate`，可接入 assembler artifact |

# Constraints Matrix
| Constraint | Handling |
| --- | --- |
| 不伪造 live | assembler 默认 pending；live 必须显式 `--ack-external-live` |
| 不泄露秘密 | 拒绝敏感片段；不输出 DSN、token、secret、URL、私钥或报告正文 |
| 不重造 gate | assembler 输出交给 `multi-replica-runtime-gate` 验证 |
| 不扩大业务面 | 不改报告生成、worker 执行、数据库 adapter |
| 不新增依赖 | 只用 Python 标准库和现有脚本 |

# Change Boundary
- Allowed: `scripts/` assembler、`tests/regression/`、`docs/reference-materials/`、`governance/tasks/0081-*`、`scripts/AGENTS.md`、`tests/AGENTS.md`、`local-ci.sh`。
- Read-only context: 0080 contract/gate、runtime registry、roadmap。
- Forbidden: 真实 DSN/secret 入仓、业务逻辑重写、外部服务连接、默认生产 ready 声明。

# Risk Matrix
| Risk | Mitigation |
| --- | --- |
| operator 手写 fake proof refs | assembler 不能证明真实性，只能强制字段和红线；最终 live 仍需外部审计 |
| pending 被误读成通过 | summary 明确 `externalConnectivity=外部连通验证待执行` |
| sensitive proof ref 泄露 | 输入/输出敏感片段扫描 |
| exactly-once overclaim | 禁止 `exactlyOnceClaim`，只允许 no duplicate terminal job observation |

# Assumptions and Falsification
- Assumption: 下一个有价值切片是 evidence assembler，而不是新增另一个自然语言计划。
- Falsifier: 如果已有脚本能生成 0080 可消费的脱敏 multi-replica evidence，则本任务应收缩为文档接线。
- Assumption: proof refs 用 `evidence://...`、`artifact://...`、`s3://redacted/...`、`gs://redacted/...`、`ci-artifact://...` 等脱敏句柄，不保存真实 URL。
- Falsifier: 若生产审计要求必须保存实际 URL，则应另开受保护外部证据仓，不入本 repo。

# Critical Ambiguities
- 当前没有真实多副本环境、外部 webhook、Vault/KMS 或 metrics backend 权限；live 只能由 operator 后续提供证据。
- 0081 不解决 exactly-once，只把 exactly-once non-claim 写进生成器与测试。

# Debug Evidence Contract
- 调试模式: Optional

Not required. 本任务是新增 evidence tooling，不是 bugfix；若 gate 或 CI 回归失败，则记录失败命令、根因、修复和回归证据。

# Task Package Context Map
| Node ID | Context |
| --- | --- |
| TP-01.01 | roadmap、0080 contract/gate、task index |
| TP-01.02 | 0080 required fields、nonClaims、privacyBoundary |
| TP-02.01 | CLI schema、proof ref allowlist、timestamp ordering |
| TP-02.02 | negative cases、secret scan、gate reuse |
| TP-03.01 | `scripts/multi-replica-runtime-evidence-assembler.py/.sh` |
| TP-03.02 | `scripts/local-ci.sh`、`scripts/AGENTS.md`、roadmap/docs |
| TP-04.01 | `tests/regression/test_multi_replica_runtime_evidence_assembler.py` |
| TP-04.02 | focused gates、quick CI、task validators |
| TP-05.01 | closeout docs |
| TP-05.02 | git/CI delivery evidence boundary |
