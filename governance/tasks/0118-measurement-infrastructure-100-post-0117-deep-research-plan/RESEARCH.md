# Post-0117 100% 测算基础设施深度调研与完整实现计划

## 1. 结论

0116/0117 之后，FateCat 的 100% 路线发生了一个关键变化：外部待验证项已经从散落文本变成了可分类、可分派、可关闭的 closure plan resource。下一阶段不应该继续“找有哪些外部 pending”，而应该按资源域关闭证据链。

100% 测算基础设施的定义保持不变：不是预测准确率 100%，不是术数模块数量 100%，而是一个面向 Agent 与应用开发者的基础设施系统达到以下能力：

- 能力可发现：Capability、Provider、Dataset、EvaluationRun、DeliverySurface、SecurityControl、ReleaseArtifact、AuditHandoff 都可登记和查询。
- 接口可接入：OpenAPI、AsyncAPI、错误码、SDK 示例、sandbox、changelog 可用。
- 执行可恢复：CalculationJob 有幂等、event history、retry/timeout、lease、heartbeat、outbox、restart recovery。
- 质量可回归：八字/紫微有 corpus、report diff、evidence coverage、benchmark、趋势和 failure taxonomy。
- 运行可观测：health、ready、metrics、logs、trace、SLO、alert、runbook、incident drill 有证据。
- 安全可证明：OIDC/RBAC、tenant authz、secret externalization、SIEM、retention、privacy/AI output policy 可验证。
- 发布可证明：current commit CI、container digest、SBOM/provenance、attestation verify、rollback drill 可追溯。
- 审计可交接：audit bundle、risk register、external closure plan 和 third-party rehearsal 可复核。

## 2. 外部基础设施同构资料

| 领域 | 官方资料 | 基础设施共同能力 | FateCat 对应要求 |
| --- | --- | --- | --- |
| API contract | OpenAPI Specification: https://spec.openapis.org/oas/latest.html | 机器可读 HTTP API、schema、示例、版本兼容 | OpenAPI 3.2 口径、标准错误、SDK 示例、兼容 changelog。 |
| Async API | AsyncAPI Specification: https://www.asyncapi.com/docs/reference/specification/v3.1.0 | 消息、channel、operation、event schema | job/webhook/evaluation/release 事件必须机器可读。 |
| Event envelope | CloudEvents: https://cloudevents.io/ | 统一事件元数据 | `id/source/type/subject/time/data` + requestId/traceId。 |
| Control plane | Kubernetes Controllers: https://kubernetes.io/docs/concepts/architecture/controller/ | desired/current state、reconciliation、controller loop | capability/provider/release/evaluation/security 的 spec/status 和 drift scanner。 |
| Software catalog | Backstage System Model: https://backstage.io/docs/features/software-catalog/system-model/ | Component/API/Resource/System 可发现 | FateCat resource catalog 和 owner/maturity/status。 |
| Provider ecosystem | Terraform Providers: https://developer.hashicorp.com/terraform/language/providers | provider 来源、版本、配置、生命周期 | provider lock、health、source/license、compat matrix、deprecation。 |
| Durable execution | Temporal Durable Execution: https://docs.temporal.io/evaluate/understanding-temporal | event history、恢复、重试、长流程状态 | CalculationJob durable backend、worker lease、restart recovery。 |
| Observability | OpenTelemetry Signals: https://opentelemetry.io/docs/concepts/signals/ | traces、metrics、logs 统一 | API -> job -> provider -> report trace 和 metrics/logs。 |
| SRE | Google SRE SLO: https://sre.google/sre-book/service-level-objectives/ | SLI/SLO/error budget 管可靠性 | availability、latency、job success、provider success、error budget 和 alert。 |
| Delivery metrics | DORA metrics: https://dora.dev/guides/dora-metrics-four-keys/ | deployment frequency、lead time、change failure、MTTR | release gate、rollback drill、incident/change failure 记录。 |
| API security | OWASP API Security Top 10 2023: https://owasp.org/API-Security/editions/2023/en/0x11-t10/ | 授权、认证、资源消耗、配置和库存风险 | OIDC/RBAC、tenant isolation、rate/body limit、API inventory、negative tests。 |
| Secure software | NIST SSDF SP 800-218: https://csrc.nist.gov/pubs/sp/800/218/final | 安全开发、漏洞减少、供应链沟通 | secret scan、dependency review、release evidence、incident response。 |
| AI governance | NIST AI RMF: https://www.nist.gov/itl/ai-risk-management-framework | AI 风险治理、评测、监控 | Agent 只解释结构化测算结果，禁止确定性恐吓和高风险替代建议。 |
| Supply chain | SLSA v1.2: https://slsa.dev/spec/v1.2/ | build integrity、provenance、attestation | current commit release proof、builder identity、provenance。 |
| SBOM | CycloneDX Specification: https://cyclonedx.org/specification/overview/ | 组件、服务、依赖、license 和关系可机器读 | release/data/vendor SBOM 和 license/export policy。 |
| Artifact attestations | GitHub Artifact Attestations: https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations | artifact identity/provenance 可验证 | 每个 release commit 重新生成和验证 attestation。 |
| Idempotency/webhooks | [Stripe Idempotent Requests](https://docs.stripe.com/api/idempotent_requests) and [Stripe Webhooks](https://docs.stripe.com/webhooks) | 幂等、签名、重试、事件审计 | report job idempotency、webhook signature、retry/outbox、delivery audit。 |

## 3. Post-0117 当前状态

| Domain | 当前事实 | 100% 缺口 |
| --- | --- | --- |
| External validation closure | 0116 已生成 closure plan；0117 把 manual triage 从 184 降到 1；post-0118 当前清单 `total=402`、`manualTriage=1` | 还没有真实关闭生产 API/HF/Bot/Postgres/OIDC/SIEM/OTel/Vault/KMS/developer portal/第三方审计。 |
| Certification | 支持 release proof、audit bundle、live gate sidecar 和 closure gate | `canClaim100Percent=false` 必须保持，直到所有外部证据闭合。 |
| Control plane | Capability/Provider/ReleaseGate/EvaluationRun resource gate baseline 已有 | 还缺 controller-style reconciliation、owner workflow、promotion/deprecation 自动化。 |
| Runtime | runtime proof pack、Postgres/webhook/worker/secret/multi-replica gates 已有 | 真实公网 webhook、外部 secret live、长期多副本 live 和 exactly-once 非声明边界仍待外部证据。 |
| Core quality | corpus、report diff、evaluation trend、evidence coverage trend baseline 已有 | 还需更大八字/紫微 corpus、人审抽样、benchmark 持续趋势和自然语言冲突解释质量。 |
| Developer platform | API/docs/SDK baseline 有本地门禁 | 还缺公开 portal、发布 SDK/package、sandbox issuer/revocation live。 |
| Observability/SRE | OTel/SLO staged gate 和本地 signals baseline 已有 | 还缺真实 collector/backend、trace query、dashboard、alert route、incident drill。 |
| Security/privacy | RBAC/OWASP/secret scan/retention/security externalization gates 已有 | 还缺 OIDC/IdP、SIEM、immutable audit、tenant authz live、production retention scheduler。 |
| Release proof | current release proof bridge 和 release artifact proof 已有 | 每个最终 release commit 仍需重新跑远端 CI、digest、attestation、rollback。 |
| Audit | current audit bundle、risk register、pending external list、closure plan 已有 | 还缺第三方审计人员独立复核和所有 pending external closure evidence。 |

## 4. 完整实现波次

| Wave | Priority | 目标 | 下一步任务 | 不可伪造证据 |
| --- | --- | --- | --- | --- |
| MI-100.A | P0 | External closure execution | 把 0117 closure categories 转成 owner work queue、proof-ref schema、external validation runbook | 每个 occurrence 的 owner、credentialDependencies、requiredEvidence、verificationCommands、closureCondition；真实 live 缺失时保持 blocked。 |
| MI-100.B | P0 | Production live delivery | API/HF/Bot/Webhook live smoke | 真实 URL/token/receiver proof；dry-run 不可替代。 |
| MI-100.C | P0 | Runtime live proof | Postgres external backend、public webhook、Vault/KMS、多副本 24h runtime | redacted live evidence JSON、gate accepted、无 exactly-once overclaim。 |
| MI-100.D | P0 | Observability/SRE live | OTel collector/backend、trace query、SLO dashboard、alert、incident drill | trace backend link、dashboard proof、alert proof、incident report。 |
| MI-100.E | P0 | Security/privacy live | OIDC/IdP、SIEM、immutable audit、retention scheduler、tenant authz | IdP issuer/JWKS proof、SIEM ingestion/query proof、retention proof。 |
| MI-100.F | P0 | Core quality scale | 八字/紫微 corpus 扩容、report diff、evidence coverage、benchmark trend | anonymous corpus manifest、summary-only diff、coverage trend、failure taxonomy。 |
| MI-100.G | P1 | Developer platform | developer portal、SDK/package、sandbox issuer/revocation | install smoke、docs smoke、token issue/revoke smoke。 |
| MI-100.H | P1 | Provider platform | provider trace、compat matrix、source/license/vendor SBOM | provider lifecycle gate、drift trend、CycloneDX artifacts、license review pending list。 |
| MI-100.I | P0 | Release proof current commit | 当前最终 commit 的 remote CI、container digest、SBOM/provenance、attestation、rollback | GitHub Actions URL、digest、attestation verify、rollback JSON。 |
| MI-100.J | P0 | Audit/certification closeout | current audit bundle、certification、external closure evidence、third-party rehearsal | audit handoff markdown/json、risk register、closure summary、third-party review notes。 |

## 5. 递归任务树

```text
MI-100 FateCat 100% 测算基础设施
  MI-100.A External Validation Closure Execution
    MI-100.A.01 closure owner work queue
    MI-100.A.02 proof-ref schema and evidence upload contract
    MI-100.A.03 external validation runbook per category
    MI-100.A.04 closure trend dashboard and stale owner alert
  MI-100.B Production Live Delivery
    MI-100.B.01 production API/HF live smoke
    MI-100.B.02 Telegram Bot live smoke
    MI-100.B.03 public webhook live delivery smoke
    MI-100.B.04 multi-surface live parity diff
  MI-100.C Runtime Live Proof
    MI-100.C.01 Postgres external backend production drill
    MI-100.C.02 Vault/KMS secret provider live
    MI-100.C.03 multi-replica 24h runtime live
    MI-100.C.04 idempotency and duplicate terminal negative proof
  MI-100.D Observability and SRE
    MI-100.D.01 OTel collector/exporter live
    MI-100.D.02 trace backend query proof
    MI-100.D.03 SLO/error budget dashboard
    MI-100.D.04 alert route and incident drill
  MI-100.E Security and Privacy
    MI-100.E.01 OIDC/IdP integration
    MI-100.E.02 tenant authz negative tests
    MI-100.E.03 SIEM or immutable audit storage
    MI-100.E.04 production retention scheduler
    MI-100.E.05 privacy and AI-output policy enforcement
  MI-100.F Core Quality and Evaluation
    MI-100.F.01 bazi corpus expansion wave
    MI-100.F.02 ziwei corpus expansion wave
    MI-100.F.03 full report summary-diff trend
    MI-100.F.04 evidence coverage and broken-ref trend
    MI-100.F.05 benchmark runner and human review protocol
  MI-100.G Developer Platform
    MI-100.G.01 public developer portal
    MI-100.G.02 SDK/package release
    MI-100.G.03 sandbox token issuer and revocation
    MI-100.G.04 compatibility changelog and deprecation policy
  MI-100.H Provider Platform
    MI-100.H.01 provider trace span and dependency health
    MI-100.H.02 source/license/vendor SBOM
    MI-100.H.03 provider compatibility matrix
    MI-100.H.04 provider promotion/deprecation automation
  MI-100.I Supply Chain and Release Proof
    MI-100.I.01 current commit remote CI
    MI-100.I.02 container digest and attestation
    MI-100.I.03 SBOM/provenance verification
    MI-100.I.04 rollback drill evidence
  MI-100.J Audit and Certification
    MI-100.J.01 current audit bundle rerun
    MI-100.J.02 certification aggregator with all sidecars
    MI-100.J.03 external closure evidence summary
    MI-100.J.04 third-party audit rehearsal
```

## 6. 推荐下一步

不提供外部凭证时，下一步应先执行 `MI-100.A.01 closure owner work queue`。理由：

- 0117 已把 pending items 基本分类完；下一步自然是让分类变成可追踪工作队列。
- 它不需要外部凭证，但能直接降低后续 live 闭环的组织成本。
- 它会为 API/HF/Bot/Postgres/OIDC/SIEM/OTel/Vault/KMS/developer portal/third-party audit 的真实关闭提供统一 proof-ref 和 owner 状态。

如果用户提供真实外部资源，则按下面插队：

1. 有 `FATE_BOT_TOKEN`：先跑 Telegram Bot live。
2. 有生产 API/HF URL/token：先跑 production live release gate。
3. 有 Postgres DSN + 公网 receiver：先跑 public webhook live。
4. 有 Vault/KMS：先跑 external secret provider live。
5. 有 OIDC/SIEM/OTel：先跑对应 staged live gate。

## 7. 不可伪造完成标准

- `manualTriage=1` 不等于外部 pending 已关闭。
- `shipGate=blocked` 必须保持，直到真实外部证据闭合。
- `canClaim100Percent=false` 必须保持，直到 certification 所有 domain 都 passed。
- local-ci、dry-run、staged gate、contract gate、allow-missing blocked summary 不能替代 production live。
- 任何真实 token、secret、DSN、webhook secret、private key 不得写入仓库、报告、日志或审计包。
- 第三方审计结论不能由本地 dry-run 冒充。
