# Post-0076 100% 基础设施深度调研

## Research Question

FateCat 要达到 100% 测算基础设施，还差什么？这里的 100% 不是预测准确率、术数模块数量或单次 smoke 成功，而是基础设施成熟度：能力可发现、接口可接入、任务可恢复、事件可订阅、质量可回归、运行可观测、安全可证明、发布可验证、审计可交接。

## Current Facts

| Fact | Evidence | Meaning |
| --- | --- | --- |
| 0076 已完成 | `governance/tasks/0076-measurement-infrastructure-postgres-public-webhook-live-smoke/STATUS.md` | 已有 public webhook live smoke gate 和 blocked preflight，不等于 live passed。 |
| 当前主路线图已有 0.9 | `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` | 需要追加 0.10，而不是新建平行路线图。 |
| runtime backend contract 仍有 production 缺口 | `contracts/fate/delivery/runtime-backends.json` | Postgres backend 仍缺外部 Vault/KMS、公网 webhook passed、heartbeat/polling、长期多副本和 exactly-once 证据。 |
| 后续实现不能被外部凭证卡死 | 当前环境没有真实 token/endpoint/生产平台权限 | 能本地做的先做；外部项明确标记 `外部连通验证待执行`。 |

## Source Matrix

| Field | Primary Source | Infrastructure Lesson | FateCat Requirement |
| --- | --- | --- | --- |
| API contract | OpenAPI Specification: https://spec.openapis.org/oas/latest.html | API 必须机器可读、可版本化、可生成客户端 | OpenAPI release artifact、错误码、changelog、SDK smoke。 |
| Async API | AsyncAPI Specification: https://www.asyncapi.com/docs/reference/specification/latest | 异步消息也需要 schema、channel、operation、message | job/webhook/evaluation/release events 需要 AsyncAPI 或等价 contract。 |
| Event envelope | CloudEvents: https://cloudevents.io/ | 事件 envelope 标准化后才能跨系统路由和审计 | 统一 `id/source/type/subject/time/data`，绑定 requestId/traceId。 |
| Control plane | Kubernetes Controllers: https://kubernetes.io/docs/concepts/architecture/controller/ | 基础设施以 desired/current 和 reconciliation 管资源 | capability/provider/release gate 需要 spec/status、drift scanner。 |
| Provider ecosystem | Terraform Providers: https://developer.hashicorp.com/terraform/language/providers | provider 独立版本、来源、配置和生命周期 | bazi/ziwei/almanac/meihua provider 需要 engineVersion、source/license、health、deprecation。 |
| Durable runtime | Temporal Durable Execution: https://docs.temporal.io/evaluate/understanding-temporal | 长流程必须有持久状态、event history、恢复和重试 | CalculationJob 需要 external backend、worker lease、heartbeat、restart recovery、retry/timeout。 |
| Observability | OpenTelemetry Signals: https://opentelemetry.io/docs/concepts/signals/ | traces/metrics/logs 是生产可运维性的共同语言 | API -> job -> provider -> report 需要 trace、metrics、structured logs 和 backend evidence。 |
| SRE | Google SRE SLO: https://sre.google/sre-book/service-level-objectives/ | 可靠性需要 SLI/SLO/error budget，而不是口头稳定 | latency、availability、job success、provider failure、error budget、alert/runbook。 |
| Delivery metrics | DORA Metrics: https://dora.dev/guides/dora-metrics-four-keys/ | 发布成熟度要看部署频率、变更前置时间、失败率、恢复时间 | release gate、rollback drill、CI evidence、change failure 和 MTTR 记录。 |
| Platform engineering | CNCF Platform Engineering Maturity Model: https://tag-app-delivery.cncf.io/whitepapers/platform-eng-maturity-model/ | 平台是产品，强调自助、治理、反馈和度量 | 开发者/Agent 能自助发现、接入、验证和观测 capability。 |
| Software catalog | Backstage System Model: https://backstage.io/docs/features/software-catalog/system-model/ | 组件、API、资源、系统需要可发现目录 | Capability、Provider、Dataset、EvaluationRun、SecurityControl、DeliverySurface 进入 catalog/registry。 |
| API security | OWASP API Security Top 10 2023: https://owasp.org/API-Security/editions/2023/en/0x11-t10/ | API 风险集中在授权、认证、资源消耗、库存和配置 | OIDC/RBAC、tenant isolation、rate/body limit、API inventory、negative tests。 |
| Secure development | NIST SSDF SP 800-218: https://csrc.nist.gov/pubs/sp/800/218/final | 安全开发必须覆盖开发、保护、响应和供应链 | secret scan、dependency review、release evidence、incident response、security control registry。 |
| Supply chain | SLSA v1.2: https://slsa.dev/spec/v1.2/ | provenance、build integrity 和 artifact 证明是发布底线 | current commit CI、container digest、attestation verify、provenance。 |
| SBOM | CycloneDX Specification: https://cyclonedx.org/specification/overview/ | 组件、依赖、服务和关系应机器可读 | release SBOM、data/vendor SBOM、dependency graph、license/export policy。 |
| Idempotency/webhooks | Stripe idempotency and webhooks: https://docs.stripe.com/api/idempotent_requests, https://docs.stripe.com/webhooks | 幂等、签名、重试和事件历史是外部副作用治理核心 | report job idempotency、webhook signature、retry/outbox、event audit。 |

## Synthesis

成熟基础设施的共同点不是功能多，而是把复杂领域压成资源、契约、控制面和证据闭环。FateCat 的正确终态应按以下资源域组织：

| Domain | 100% Meaning | Current Post-0076 Gap |
| --- | --- | --- |
| Capability Control Plane | 所有能力通过 registry/executor/policy/evidence gate 执行 | 仍需 drift scanner、promotion/deprecation 自动化和跨端一致性证明。 |
| Durable Runtime | 异步 job 可恢复、可重试、可审计、可多副本运行 | 仍需 worker heartbeat/polling、真实 webhook passed、external secret provider、长期多副本和 exactly-once 边界说明。 |
| Event Platform | job/webhook/evaluation/release event 可订阅、可版本化、可回放 | 仍需 producer/consumer contract tests、DLQ/replay 策略和真实投递证据。 |
| Provider Platform | 每个测算体系像 provider 一样被版本化和治理 | 仍需 provider trace、source/license/dependency drift、compat matrix。 |
| Core Quality | 八字/紫微不只稳定运行，还能稳定正确 | 仍需大规模匿名 corpus、MingLi-Bench runner、全文 report diff、evidence coverage。 |
| Developer Platform | 不读源码也能接入 | 仍需发布 SDK/package、developer portal、sandbox token、fixed snapshot。 |
| Observability/SRE | 有真实 trace backend、SLO、alert 和 incident drill | 仍需 OTel exporter/backend、error budget、alert live/dry evidence。 |
| Security/Privacy | 公开服务默认安全，审计可追踪 | 仍需 OIDC/IdP、SIEM/不可变审计、tenant isolation、retention cleaner。 |
| Supply Chain/Release | 每个 release commit 有不可伪造 artifact proof | 仍需 current commit CI、digest、SBOM/provenance、attestation verify、rollback evidence。 |
| Audit Handoff | 第三方能逐项复核 | 仍需 current commit audit bundle、risk register、pending external list。 |

## Recommended Next Task Queue

| Order | Suggested Task | Why | Evidence Required |
| --- | --- | --- | --- |
| 0078 | Postgres worker heartbeat/polling hardening | 不依赖外部平台，补长期 worker runtime 缺口 | heartbeat renew、DB polling、lease expiry backoff、stuck job recovery smoke。 |
| 0079 | External secret provider interface and gate | 本地 Fernet 不等于生产密钥生命周期 | provider interface、dry-run、allow-missing blocked summary、live evidence contract。 |
| 0080 | OTel backend/SLO staged gate | 没有 backend evidence 就没有生产可运维性 | collector/exporter config、trace backend pending/live evidence、SLO/error budget gate。 |
| 0081 | OIDC/SIEM/retention staged gate | 公开服务需要真实身份和审计闭环 | OIDC/SIEM/retention cleaner allow-missing gate 和 live evidence contract。 |
| 0082 | Provider drift scanner | 防止 registry 写得漂亮但 runtime 漂移 | provider trace span、dependency/source/license drift report。 |
| 0083 | Core corpus and MingLi-Bench runner | 基础设施必须证明核心测算质量可回归 | bazi/ziwei corpus、benchmark runner、full report diff、no-leak policy。 |
| 0084 | Developer portal and SDK release baseline | 基础设施必须让第三方接入 | SDK/package smoke、developer docs smoke、sandbox token/fixed snapshot。 |
| 0085 | Multi-surface semantic diff | Web/API/Bot/CLI/Skill 不能各说各话 | same profile diff、Markdown copy snapshot、Bot live diff when token exists。 |
| 0086 | Current release proof | 每个 release commit 都要重新证明 | remote CI、container digest、SBOM/provenance、attestation verify、rollback evidence。 |
| 0087 | Current audit bundle | 100% 结论必须可交给第三方复核 | audit handoff markdown/json、evidence index、risk register、pending external list。 |

If real `FATE_REPORT_JOB_DATABASE_URL` + public HTTPS webhook endpoint or real `FATE_BOT_TOKEN` is provided, the corresponding live evidence task can jump ahead of 0078. Without those, any “live passed” claim remains blocked.

## External Validation Pending

统一标记为：`外部连通验证待执行`。

- Telegram Bot live smoke：需要真实 `FATE_BOT_TOKEN`。
- Public webhook live passed：需要真实 Postgres DSN 和公网 HTTPS receiver。
- Vault/KMS/secret manager：需要外部账号、key、审计日志和 rotation 权限。
- OIDC/IdP：需要真实 IdP client、issuer、audience、JWKS 和权限策略。
- SIEM/immutable audit：需要外部 ingestion endpoint、retention policy 和查询证据。
- OTel backend：需要 collector/exporter/backend URL、trace 查询链接和 SLO dashboard。
- 长期多副本运行：需要真实多副本部署和持续运行窗口。
- exactly-once：当前不声明；后续只能声明 at-least-once + idempotency，除非有严格端到端去重和外部副作用证明。

## Conclusion

后续开发方向不是继续堆更多预测体系，而是先完成基础设施闭环。新术数能力必须在 capability/provider/evidence/evaluation/security/release/audit 协议下接入；在 100% 基础设施闭环完成前，八字/紫微质量加固和生产证据闭环优先级高于新能力扩张。
