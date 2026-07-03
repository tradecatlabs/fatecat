# Post-0091 100% 基础设施深度调研

## Research Question

FateCat 要达到 100% 测算基础设施，还差什么？这里的 100% 不是预测准确率、术数模块数量或单次 smoke 成功，而是基础设施成熟度：能力可发现、接口可接入、任务可恢复、事件可订阅、质量可回归、运行可观测、安全可证明、发布可验证、审计可交接。

## Current Facts

| Fact | Evidence | Meaning |
| --- | --- | --- |
| 0091 已完成本地 retention cleanup baseline | `governance/tasks/0091-measurement-infrastructure-retention-cleanup-baseline/STATUS.md` | 只证明本地 SQLite records/report jobs 清理基线，不证明生产 scheduler、Postgres production cleanup live 或外部 SIEM retention。 |
| 当前 HEAD | `git rev-parse HEAD` -> `44cbeddc1d9aaf6dda3fe6b2d306eb27cdd97296` | 0092 规划基于 0091 后当前提交。 |
| 当前远端 CI | Acceptance `28657479378` success；Container `28657481029` success | 0091 的远端 CI 已验证，但 0092 文档变更尚未提交验证。 |
| 当前主路线图已有 0.10 | `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` | 本任务追加 0.11，不新建平行路线图。 |
| 审计和发布证据已有生成器契约 | `contracts/fate/audit/current-bundle.json`、`contracts/fate/audit/handoff.json` | 100% 最终判断应由 current release proof + audit bundle 聚合，而不是聊天结论。 |

## Source Matrix

| Field | Primary Source | Infrastructure Lesson | FateCat Requirement |
| --- | --- | --- | --- |
| API contract | OpenAPI Specification latest: https://spec.openapis.org/oas/latest.html | API 必须机器可读、可版本化、可生成客户端；当前 latest 入口指向 OpenAPI 3.2.0。 | OpenAPI release artifact、错误码、changelog、SDK/package smoke、兼容策略。 |
| Async API | AsyncAPI Specification latest: https://www.asyncapi.com/docs/reference/specification/latest | 异步消息也需要 schema、channel、operation、message；当前 latest 为 3.1.0。 | job/webhook/evaluation/release events 需要 AsyncAPI 或等价 contract tests。 |
| Event envelope | CloudEvents: https://cloudevents.io/ | 事件 envelope 标准化后才能跨系统路由和审计。 | 统一 `id/source/type/subject/time/data`，绑定 requestId/traceId，支持 replay/DLQ 证据。 |
| Control plane | Kubernetes Controllers: https://kubernetes.io/docs/concepts/architecture/controller/ | 基础设施以 desired/current state 和 reconciliation 管资源。 | capability/provider/release/security/evaluation 需要 spec/status、drift scanner、promotion/deprecation。 |
| Provider ecosystem | Terraform Providers: https://developer.hashicorp.com/terraform/language/providers | provider 独立版本、来源、配置和生命周期。 | bazi/ziwei/almanac/meihua provider 需要 engineVersion、source/license、health、drift、compat matrix。 |
| Durable runtime | Temporal Durable Execution: https://docs.temporal.io/evaluate/understanding-temporal | 长流程必须有持久状态、event history、恢复和重试。 | CalculationJob 需要 external backend、worker lease、heartbeat、restart recovery、retry/timeout。 |
| Observability | OpenTelemetry Signals: https://opentelemetry.io/docs/concepts/signals/ | traces/metrics/logs 是生产可运维性的共同语言。 | API -> job -> provider -> report 需要 trace、metrics、structured logs 和 backend evidence。 |
| SRE | Google SRE SLO: https://sre.google/sre-book/service-level-objectives/ | 可靠性需要 SLI/SLO/error budget，而不是口头稳定。 | latency、availability、job success、provider failure、error budget、alert/runbook。 |
| Delivery metrics | DORA Metrics: https://dora.dev/guides/dora-metrics-four-keys/ | 发布成熟度要看部署频率、变更前置时间、失败率、恢复时间。 | release gate、rollback drill、change failure 和 MTTR 记录。 |
| Platform engineering | CNCF Platform Engineering Maturity Model: https://tag-app-delivery.cncf.io/whitepapers/platform-eng-maturity-model/ | 平台是产品，强调自助、治理、反馈和度量。 | 开发者/Agent 能自助发现、接入、验证和观测 capability。 |
| Software catalog | Backstage System Model: https://backstage.io/docs/features/software-catalog/system-model/ | 组件、API、资源、系统需要可发现目录。 | Capability、Provider、Dataset、EvaluationRun、SecurityControl、DeliverySurface 进入 catalog/registry。 |
| API security | OWASP API Security Top 10 2023: https://owasp.org/API-Security/editions/2023/en/0x11-t10/ | API 风险集中在授权、认证、资源消耗、库存和配置。 | OIDC/RBAC、tenant isolation、rate/body limit、API inventory、negative tests。 |
| Secure development | NIST SSDF SP 800-218: https://csrc.nist.gov/pubs/sp/800/218/final | 安全开发必须覆盖开发、保护、响应和供应链。 | secret scan、dependency review、release evidence、incident response、security control registry。 |
| Supply chain | SLSA v1.2: https://slsa.dev/spec/v1.2/ | provenance、build integrity 和 artifact 证明是发布底线。 | current commit CI、container digest、attestation verify、provenance。 |
| SBOM | CycloneDX Specification: https://cyclonedx.org/specification/overview/ | 组件、依赖、服务和关系应机器可读。 | release SBOM、data/vendor SBOM、dependency graph、license/export policy。 |
| Artifact attestation | GitHub Artifact Attestations: https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations | build provenance 和 artifact identity 需要可验证命令。 | 每个 release commit 需要远端 workflow、digest、attestation verify 和证据 URL。 |
| Idempotency and webhook events | [Stripe idempotent requests](https://docs.stripe.com/api/idempotent_requests) and [Stripe webhook events](https://docs.stripe.com/webhooks) | 幂等、签名、重试和事件历史是外部副作用治理核心。 | report job idempotency、webhook signature、retry/outbox、event audit。 |

## Synthesis

成熟基础设施的共同点不是功能多，而是把复杂领域压成资源、契约、控制面和证据闭环。FateCat 的正确终态应按以下资源域组织：

| Domain | 100% Meaning | Current Post-0091 Gap |
| --- | --- | --- |
| Capability Control Plane | 所有能力通过 registry/executor/policy/evidence gate 执行 | 生产能力已资源化，但 CLI/Skill 交付仍需补入同源验证；planned 能力继续拒绝执行。 |
| Provider Platform | 每个测算体系像 provider 一样被版本化和治理 | 已有 drift scanner baseline；仍需长期 dependency/source/license 趋势和人工许可复核。 |
| Durable Runtime | 异步 job 可恢复、可重试、可审计、可多副本运行 | 已有 SQLite/Postgres 多项本地基线；仍需真实公网 webhook passed、外部 secret live、长期多副本 live 和生产 cleanup。 |
| Event Platform | job/webhook/evaluation/release event 可订阅、可版本化、可回放 | 已有契约和示例；仍需 producer/consumer contract tests、DLQ/replay 策略和真实投递证据。 |
| Report/Evidence | 报告和结论依据可回归、可解释、可审计 | 0090 已做多端语义 diff baseline；仍缺 CLI/Skill diff、全文 golden、冲突反证自然语言化。 |
| Core Quality | 八字/紫微不只稳定运行，还能稳定正确 | 0085 已做 aggregate gate；仍需更大匿名 corpus、人审抽样、边界样本扩容和报告全文 diff。 |
| Developer Platform | 不读源码也能接入 | 已有本地 portal/SDK readiness/sandbox gateway baseline；仍需公网 portal、发布版 SDK、公网 token issuer/revocation。 |
| Delivery Surface | Web/API/Bot/CLI/Skill 同源输出 | API/Web/Bot dry-run semantic diff 已有；CLI capability command、CLI/Skill diff 和 Bot live 仍缺。 |
| Observability/SRE | 有真实 trace backend、SLO、alert 和 incident drill | 已有本地/契约 gate；仍需 OTel backend live、alert live、error budget 和 incident drill。 |
| Security/Privacy | 公开服务默认安全，审计可追踪 | 0091 完成本地 retention cleanup；仍需 OIDC/IdP、SIEM/不可变审计、生产 retention scheduler、Postgres production cleanup live。 |
| Supply Chain/Release | 每个 release commit 有不可伪造 artifact proof | 0088/0089 已有 current proof/audit bundle；每个后续 release commit 仍需重跑远端 CI、digest、attestation、audit bundle。 |
| Audit Handoff | 第三方能逐项复核 | 0089 已有 current audit bundle generator；最终仍需所有 live evidence 关闭或显式 pending。 |

## Recommended Next Task Queue

| Order | Suggested Task | Why | Evidence Required |
| --- | --- | --- | --- |
| 0093 | CLI capability command baseline | 不依赖外部平台，补 D9 多端交付最明显本地缺口 | CLI 调用统一 executor/provider，bazi/ziwei/almanac/meihua JSON 输出，planned capability 拒绝，smoke/local-ci。 |
| 0094 | CLI/Skill semantic diff expansion | 0090 只覆盖 API/Web/Bot dry-run，CLI/Skill 仍是 parity 空洞 | API/Web/Bot/CLI/Skill normalized semantic hash 对齐；不保存完整报告正文。 |
| 0095 | Bazi/Ziwei corpus/report diff expansion | 这是测算质量地基，不能只靠代表样本 | 匿名 corpus manifest、全文 report diff、evidence coverage、冲突/反证 explainability。 |
| 0096 | Retention production cleanup staged gate | 0091 只做本地 SQLite cleanup，生产仍缺 scheduler/Postgres/SIEM retention 证据 | Postgres cleanup dry/live gate、scheduler proof contract、external SIEM/log retention pending/live evidence。 |
| 0097 | Event platform consumer/replay contract tests | 事件已有契约，但还缺消费者兼容和重放策略 | CloudEvents/AsyncAPI producer-consumer tests、DLQ/replay contract、negative cases。 |
| 0098 | External live evidence pack | 如果用户提供真实凭证，应集中收集 live 证据 | Bot token、公网 webhook、IdP、SIEM、OTel backend、Vault/KMS、多副本运行 evidence。 |
| 0099 | Current release proof rerun | 每个 release commit 都要重新证明 | Acceptance/Container URL、digest、attestation verify、SBOM/provenance、rollback drill。 |
| 0100 | Current audit bundle rerun | 100% 结论必须可交给第三方复核 | current audit bundle required mode passed，pending external list 与 risk register 对齐。 |

If real `FATE_REPORT_JOB_DATABASE_URL` + public HTTPS webhook endpoint, real `FATE_BOT_TOKEN`, IdP/SIEM/OTel/Vault credentials, or a multi-replica production window is provided, the corresponding live evidence task can jump ahead of 0093. Without those, any “live passed” claim remains blocked.

## External Validation Pending

统一标记为：`外部连通验证待执行`。

- Telegram Bot live smoke：需要真实 `FATE_BOT_TOKEN`。
- Public webhook live passed：需要真实 Postgres DSN 和公网 HTTPS receiver。
- Vault/KMS/secret manager：需要外部账号、key、审计日志和 rotation 权限。
- OIDC/IdP：需要真实 IdP client、issuer、audience、JWKS 和权限策略。
- SIEM/immutable audit：需要外部 ingestion endpoint、retention policy 和查询证据。
- OTel backend：需要 collector/exporter/backend URL、trace 查询链接和 SLO dashboard。
- 长期多副本运行：需要真实多副本部署和持续运行窗口。
- Retention production cleanup：需要生产 scheduler、Postgres cleanup live 和 SIEM/log retention 证据。
- exactly-once：当前不声明；后续只能声明 at-least-once + idempotency，除非有严格端到端去重和外部副作用证明。

## Conclusion

Post-0091 之后，FateCat 的下一步不应优先新增术数模块，而应补齐多端交付同源、核心质量 corpus、生产 retention、事件平台兼容和外部 live 证据。只有当本地可执行门禁与外部不可伪造证据都闭合后，才可以谨慎声明达到 100% 测算基础设施。
