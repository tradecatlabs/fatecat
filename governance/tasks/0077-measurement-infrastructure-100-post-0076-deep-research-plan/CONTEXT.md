# Repo Evidence
| Evidence | Observation |
| --- | --- |
| `git status --short --branch` | 当前分支为 `main...origin/main`，本任务开始时只有任务索引与 0077 骨架未提交。 |
| `governance/tasks/INDEX.md` | 0070-0076 已为 Done；0076 后仍缺真实公网 webhook live passed、外部 Vault/KMS、heartbeat/polling worker、长期多副本运行和 exactly-once。 |
| `governance/tasks/0076-measurement-infrastructure-postgres-public-webhook-live-smoke/STATUS.md` | 0076 完成的是 live smoke gate 和 blocked preflight；真实 DSN + 公网 endpoint 的 live passed 仍是外部连通验证待执行。 |
| `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` | 已有 0.9 post-0076 计划；本任务追加 0.10，把后续实现顺序重新压成可执行队列。 |
| `contracts/fate/delivery/runtime-backends.json` | Postgres backend 仍不具备 production ready、exactly-once、外部 Vault/KMS 或长期多副本证据。 |

# Constraints Matrix
| Constraint | Decision |
| --- | --- |
| 只允许分析当前分支和当前 worktree | 不切分支、不 rebase、不合并、不改历史。 |
| planning-only | 不改业务代码、不新增 runtime script、不跑外部 live smoke。 |
| 外部资料必须可追溯 | 只使用官方/一手资料链接，或明确作为仓库事实。 |
| 不伪造生产证据 | dry-run、本地 smoke、blocked preflight、contract gate 均不能写成 live passed。 |
| 文档驱动 | 主路线图是长期真相源，0077 任务目录是本轮调研证据与任务包。 |

# Change Boundary
- 允许修改：`governance/tasks/INDEX.md`、`governance/tasks/0077-measurement-infrastructure-100-post-0076-deep-research-plan/`、`docs/reference-materials/roadmap/测算基础设施100%实现计划.md`。
- 不修改：业务源码、contracts、scripts、tests、CI、运行环境和 secret。

# Risk Matrix
| Risk | Impact | Mitigation |
| --- | --- | --- |
| 计划重复漂移 | 后续执行者不知道看 0.9 还是新文档 | 主路线图只追加 0.10，0077 明确引用主路线图。 |
| 把 gate 写成 live | 审计会判定伪证 | 所有外部项统一写 `外部连通验证待执行`。 |
| 继续堆术数模块 | 偏离基础设施目标 | 0.10 明确新功能先暂停，先完成 infra closure。 |
| 任务过大 | 后续无法执行 | 0.10 把任务切成 0078+ 可创建的顺序队列。 |

# Assumptions and Falsification
- Assumption: FateCat 的 100% 指“基础设施成熟度 100%”，不是预测命中率 100% 或术数模块数量 100%。
- Assumption: 当前无真实外部 token、生产 DSN、公网 webhook、IdP、SIEM、OTel backend、Vault/KMS 权限。
- Falsifier: 用户提供真实外部环境和凭证后，public webhook live、Bot live、OIDC/SIEM/OTel/Vault/KMS 可前置执行并改写优先级。
- Falsifier: 如果后续 `validate_task_docs.py` 或主路线图 grep 发现 0076 被写成 production ready，本任务必须重开。

# Critical Ambiguities
- 无会改变本轮 planning-only 路径的关键歧义。
- 后续实现优先级存在外部条件分支：如果提供真实公网 webhook/DSN 或 Bot token，则 live evidence 任务可优先于 worker heartbeat/polling；否则先做本地可执行的 worker heartbeat/polling 和 provider drift/corpus 等切片。

# Debug Evidence Contract
- 调试模式: Optional

本任务不是 bugfix。若文档校验或链接检查失败，记录失败命令、原因和修复路径；不得伪造校验通过。

# Task Package Context Map
| Node ID | Context |
| --- | --- |
| TP-01.01 | `git status --short --branch`、0076 `STATUS.md`、当前任务索引。 |
| TP-01.02 | 主路线图、需求文档、runtime backend contract、execution playbook。 |
| TP-02.01 | OpenAPI、AsyncAPI、CloudEvents、Kubernetes Controller、Terraform Provider、Temporal、OpenTelemetry、Google SRE、DORA、OWASP、NIST、SLSA、CycloneDX、CNCF、Backstage、Stripe 官方资料。 |
| TP-02.02 | 外部资料到 FateCat resource/domain/gate 的同构映射。 |
| TP-03.01 | 100% 完成门禁和失败判定。 |
| TP-03.02 | 0078+ 后续实现任务队列。 |
| TP-03.03 | 外部连通验证待执行清单。 |
| TP-04.01 | 主路线图 0.10。 |
| TP-04.02 | 当前任务文档和 `RESEARCH.md`。 |
| TP-04.03 | 校验命令和结果。 |
