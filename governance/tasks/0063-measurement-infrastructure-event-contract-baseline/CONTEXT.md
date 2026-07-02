# Repo Evidence

| Evidence | Observation |
| --- | --- |
| `git status --short --branch` | 起始状态为 `## main...origin/main`，0062 已提交推送。 |
| `governance/tasks/0061.../RESEARCH.md` | 明确列出 `0063 CloudEvents/AsyncAPI baseline`，要求 event schema、examples、docs smoke。 |
| `contracts/fate/delivery/registry.json` | 已有 DeliverySurface、ReleaseGate、RuntimeBackend registry，适合承载 AsyncEvent registry link。 |
| `contracts/fate/capabilities/schemas/resource.schema.json` | 已有资源模型，需要新增 `AsyncEvent` 字段与不变量。 |
| `domains/experience-delivery/services/fatecat-delivery/src/report_jobs.py` | 已有 `ReportJobEvent`、job lifecycle、webhook outbox 事件历史。 |
| `domains/experience-delivery/services/fatecat-delivery/src/webhook_callbacks.py` | 已有 `report_job.terminal` webhook payload 和 HMAC header。 |
| 官方资料 | CloudEvents 必备上下文字段为 `id/source/specversion/type`；AsyncAPI 3.1 以 `channels`、`operations` 和 messages 描述消息接口。 |

# Constraints Matrix

| Constraint | Decision |
| --- | --- |
| 当前切片 | 只做 event contract baseline、gate、tests、docs。 |
| 禁止伪造 | 不声明外部 broker、公网 webhook live delivery、事件平台生产可用。 |
| 隐私 | 示例只能用 synthetic job id，不包含 webhook URL、secret、token、用户输入、出生地区、报告正文或生产日志。 |
| 依赖 | 不引入 AsyncAPI/CloudEvents Python 依赖；用 JSON contract + 本地 gate 校验。 |
| 写入范围 | `contracts/fate/delivery`、resource schema、scripts、tests、docs、task docs。 |

# Change Boundary

- 允许：新增 event schema、registry、AsyncAPI 风格文档、示例、gate、测试、local-ci artifact、文档。
- 禁止：改运行时投递逻辑、改 report job 数据库 schema、接真实外部服务、改 API 行为、接 broker。

# Risk Matrix

| Risk | Impact | Mitigation |
| --- | --- | --- |
| 把静态契约误读为生产事件平台 | 基础设施口径夸大 | registry/gate/docs 明确 `contract_baseline` 与外部连通待验证。 |
| 示例泄露真实隐私或凭证 | 安全事故 | gate 扫描 synthetic examples，secret scan 二次覆盖。 |
| registry 与 AsyncAPI 文档漂移 | 开发者接入错误 | event-contract-gate 校验 channel/operation/message 双向映射。 |
| CloudEvents 字段不完整 | 下游无法标准化消费 | gate 强制 `id/source/specversion/type`。 |

# Assumptions and Falsification

- 假设：本轮不需要完整 AsyncAPI 生态校验器，项目内静态 gate 足够证明 baseline。
- 证伪：若后续要公开发布 SDK 或自动生成消费者代码，则需要引入 AsyncAPI 官方/成熟验证器或生成器。
- 假设：job/webhook/evaluation/release 是当前最小事件域集合。
- 证伪：若新增 provider drift、audit handoff 或 security events 成为生产入口，需要扩展 event registry 并更新 gate。

# Critical Ambiguities

- 无阻塞歧义。真实 receiver/broker 需要外部资源，但不是本轮 contract baseline 的前置条件。

# Debug Evidence Contract

- 调试模式: Optional
- 调试模式：Optional。
- 若 gate、JSON、pytest 或 local-ci 失败，需要记录失败命令、根因和回归验证到 `STATUS.md`；不要求单独 `DEBUG.md`，除非出现非平凡 runtime bug。

# Future-Optimal / Ponytail / Document-Driven Contract

| Field | Value |
| --- | --- |
| Target end state | FateCat 异步事件作为基础设施资源可发现、可版本化、可审计，并能被 future subscriber 或 developer SDK 消费。 |
| Real constraints | 当前没有真实 receiver、broker、外部事件平台或公网回调日志。 |
| Inertia constraints | 现有 webhook payload 旧字段不能决定最终事件契约；本轮只做兼容基线。 |
| Kill list | 自然语言事件说明、无 schema 示例、把 webhook outbox 当成外部事件平台。 |
| Proof point | `event-contract-gate` 证明 registry、AsyncAPI、examples、resource schema 链接一致。 |
| Falsifier | gate 允许缺 CloudEvents 必备字段、示例含敏感值，或 webhook live 仍被写成已完成。 |
| Migration slice | 0063 提供静态事件契约，后续 live webhook/broker/SDK 可复用该 contract。 |
| Existence check | 0061 明确 0063 是开发者平台与事件平台的 P0 缺口；已有 job/webhook/evaluation/release 事件事实需要机器契约。 |
| Selected ladder rung | project-native JSON contract + direct gate；不引入新 broker 或生成器依赖。 |
| Skipped scope | 真正运行时 event bus、subscriber API、SDK 生成、外部 broker、live receiver。 |
| Ceiling / upgrade path | 对外发布事件 SDK 或接 broker 时升级为官方 AsyncAPI validator/generator。 |
| Source-of-truth updates | contracts、delivery AGENTS、scripts AGENTS、API docs、roadmap。 |

# Task Package Context Map

| Node | Context |
| --- | --- |
| TP-01.01 | 仓库事实、0061 计划、CloudEvents/AsyncAPI 官方资料。 |
| TP-02.01 | `contracts/fate/delivery/events.json`、`events.asyncapi.json`、examples。 |
| TP-02.02 | `contracts/fate/capabilities/schemas/resource.schema.json`、`contracts/fate/delivery/registry.json`、AGENTS。 |
| TP-03.01 | `scripts/event-contract-gate.py` / `.sh`。 |
| TP-03.02 | `tests/regression/test_event_contract_gate.py`、`test_capability_protocol.py`。 |
| TP-03.03 | `scripts/local-ci.sh` summary artifact。 |
| TP-04.01 | API docs、roadmap、task index。 |
| TP-04.02 | focused tests、validators、lint/hygiene、quick local CI。 |
