# Task Overview
- Task ID: `0081`
- Slug: `measurement-infrastructure-multi-replica-evidence-assembler`
- Objective: `执行 0080 之后的本地可执行 P0 durable runtime 切片：新增长期多副本 runtime 脱敏 evidence assembler，生成可被 multi-replica runtime gate 消费的 evidence JSON，并强制 operator attestation、proof refs、红线字段和敏感值防护；无真实多副本环境时只输出 pending，不声明 live passed、production ready 或 exactly-once。`
- Status: `Done`

## In Scope
- 新增 `multi-replica-runtime-evidence-assembler` 脚本，生成 `kind=fatecat.multi_replica_runtime_evidence` JSON。
- 复用 `multi-replica-runtime-gate` 作为最终验收，不另起一套判定逻辑。
- 支持 pending 模式和显式 external live 模式；live 模式必须要求 operator attestation、run id、started/finished 时间、证明引用和红线字段。
- 防止 evidence JSON 输出 DSN、token、secret、webhook URL、报告正文或真实用户输入。
- 更新 runtime/delivery 文档、quick CI artifact、回归测试和任务 closeout。

## Out of Scope
- 不启动真实 24h 多副本 soak。
- 不连接真实 Postgres、webhook receiver、Vault/KMS 或监控平台。
- 不声明 production ready、exactly-once 或 public webhook/external secret provider live passed。
- 不修改 ReportJobManager、PostgresReportJobStore 或业务报告逻辑。

## Task Package Tree
```text
TP-01 SPEC: 证据链缺口复核
  TP-01.01 复核 0080 contract/gate 与 roadmap 剩余缺口
  TP-01.02 定义 assembler live/pending 边界
TP-02 PLAN: 证据装配器设计
  TP-02.01 设计 CLI 输入、输出 schema 和防敏感值策略
  TP-02.02 定义 0080 gate 复用路径和反伪造负例
TP-03 BUILD: 代码与接线
  TP-03.01 新增 assembler Python 与 shell wrapper
  TP-03.02 接入 local-ci artifact、scripts AGENTS 和 docs
TP-04 TEST: 回归与门禁
  TP-04.01 增加 assembler regression tests
  TP-04.02 运行 focused gates、ruff/format、secret scan、quick CI 和任务校验
TP-05 REVIEW/SHIP: 收口交付
  TP-05.01 回填 closeout 与剩余外部验证项
  TP-05.02 明确 git/CI 交付证据外置边界
```

## Requirement Alignment
| Requirement | Implementation |
| --- | --- |
| 100% infra 要证据可复核 | assembler 生成标准 evidence JSON，并交给 gate 校验 |
| 不伪造外部 live | 默认 pending；live 需要显式 ack 和完整 proof refs |
| 不泄露敏感信息 | 输入/输出做敏感片段扫描，summary 不保存真实值 |
| 任务树推进 | 本任务按 SPEC -> PLAN -> BUILD -> TEST -> REVIEW -> SHIP 执行 |

## Task Package Overview
| Node ID | Title | Status | Acceptance |
| --- | --- | --- | --- |
| TP-01 | SPEC | Done | 缺口和边界来自 repo evidence |
| TP-01.01 | 复核 0080 | Done | roadmap/contract/gate 已读取 |
| TP-01.02 | 定义边界 | Done | pending/live/non-claim 明确 |
| TP-02 | PLAN | Done | CLI/schema/gate reuse 明确 |
| TP-02.01 | CLI/schema | Done | 输出能被 0080 gate 消费 |
| TP-02.02 | 反伪造 | Done | fake/secret/overclaim 失败 |
| TP-03 | BUILD | Done | 代码、CI、文档接线完成 |
| TP-03.01 | assembler 脚本 | Done | wrapper + Python 可执行 |
| TP-03.02 | CI/docs 接线 | Done | local-ci、AGENTS、roadmap 更新 |
| TP-04 | TEST | Done | 回归和门禁通过 |
| TP-04.01 | regression tests | Done | 覆盖 pending/live/secret/negative |
| TP-04.02 | validation gates | Done | focused gates + quick CI |
| TP-05 | REVIEW/SHIP | Done | closeout 完成；git/CI 由交付 closeout 记录 |
| TP-05.01 | closeout | Done | 文档无占位、无 overclaim |
| TP-05.02 | git/CI boundary | Done | 任务包不预声明 commit/push/remote CI；真实证据由外层交付汇报记录 |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
