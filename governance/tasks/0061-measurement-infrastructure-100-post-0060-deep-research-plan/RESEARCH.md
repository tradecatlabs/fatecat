# Post-0060 100% 基础设施深度调研

## Research Question

FateCat 要从“测算报告服务”真正升级为“测算基础设施”，还缺什么？答案不能按术数模块数量判断，而要按成熟基础设施的共同结构判断：资源可发现、接口可接入、任务可恢复、事件可订阅、质量可回归、运行可观测、安全可证明、发布可验证、审计可交接。

## Source Matrix

| 领域 | 一手资料 | 基础设施能力 | FateCat 同构要求 |
| --- | --- | --- | --- |
| HTTP API | OpenAPI Specification: `https://spec.openapis.org/oas/latest.html` | 机器可读接口、schema、版本、示例 | `/api/v1/*`、错误码、示例、SDK、changelog 必须可发布 |
| 异步 API | AsyncAPI Specification: `https://www.asyncapi.com/docs/reference/specification/latest` | 事件和消息接口机器可读 | job/webhook/evaluation/release event 需要 AsyncAPI 或等价 schema |
| 事件信封 | CloudEvents: `https://cloudevents.io/` | `id/source/type/subject/time/data` 等元数据统一 | webhook/job/evaluation/release 事件统一 envelope |
| 持久工作流 | Temporal Durable Execution: `https://docs.temporal.io/evaluate/understanding-temporal` | 状态持久、失败恢复、长流程可回放 | CalculationJob external backend、event history、retry/timeout、worker lease |
| 数据库协调 | PostgreSQL row locking / `SKIP LOCKED`: `https://www.postgresql.org/docs/current/sql-select.html` | 多 worker 安全 claim 待处理任务 | Postgres 是下一阶段 external backend 首选候选之一 |
| 可观测 | OpenTelemetry Signals: `https://opentelemetry.io/docs/concepts/signals/` | traces、metrics、logs 统一 | API -> job -> provider -> report 的 traceId/span 和指标 |
| SRE | Google SRE SLO: `https://sre.google/sre-book/service-level-objectives/` | SLI/SLO、error budget、告警 | availability、latency、job success、provider failure、alert evidence |
| API 安全 | OWASP API Security Top 10 2023: `https://owasp.org/API-Security/editions/2023/en/0x11-t10/` | 认证、授权、资源消耗、库存风险 | RBAC/OIDC、rate limit、API inventory、negative tests |
| 安全开发 | NIST SSDF SP 800-218: `https://csrc.nist.gov/pubs/sp/800/218/final` | 安全开发、供应链、漏洞响应 | secret scan、dependency review、release evidence、incident response |
| AI 风险 | NIST AI RMF: `https://www.nist.gov/itl/ai-risk-management-framework` | AI 系统风险管理 | LLM 只做解释层，不重算命盘，不输出高风险替代建议 |
| 供应链 | SLSA v1.2: `https://slsa.dev/spec/v1.2/` | provenance、attestation、构建可信度 | container digest、artifact attestation、SBOM、source/vendor/data provenance |
| SBOM | CycloneDX: `https://cyclonedx.org/specification/overview/` | 组件、依赖、服务关系机器可读 | release/data/vendor SBOM 和 export policy |
| 控制面 | Kubernetes Controllers: `https://kubernetes.io/docs/concepts/architecture/controller/` | desired/current state、reconciliation | capability/provider/release gate status 与 drift scanner |
| Provider 生态 | Terraform Providers: `https://developer.hashicorp.com/terraform/language/providers` | provider 版本化、配置化、锁定化 | bazi/ziwei/almanac/meihua provider source/license/version health |
| 软件目录 | Backstage System Model: `https://backstage.io/docs/features/software-catalog/system-model/` | Component/API/Resource/System 可发现 | Capability、Provider、Dataset、EvaluationRun、SecurityControl 等进入 catalog |

## Current FateCat Baseline

| 资源 | 当前事实 | 仍缺什么 |
| --- | --- | --- |
| Capability | 已有 registry、profiles、production/planned 区分和 executor baseline | promotion/drift 自动化、跨端执行强一致证明 |
| Provider | bazi/ziwei/almanac/meihua 已接 provider protocol | trace span、dependency/source/license drift、真实外部健康探测 |
| CalculationJob | memory/sqlite、idempotency、cancel、event history、retry/timeout、webhook outbox、restart recovery、replayable recovery、encrypted local config vault、SQLite local lease | external backend、生产分布式 worker lease、真实 crash/restart、真实 webhook live |
| Report | JSON/Markdown、policyGate、snapshotGate、default bazi profile baseline | 全文 golden diff、人审导出、多端 semantic diff |
| Evidence | evidenceRefs、rule indexes、policy gate baseline | coverage report、broken-ref fail-fast、counter-evidence 自动解释 |
| Dataset | data-supply-chain registry、canonical/classics/vendor 分层 | 大规模匿名 corpus、法律复核、长期 dataset versioning |
| EvaluationRun | runner/history/diff/dashboard/nightly baseline | 长期结果库、外部 benchmark runner、趋势告警 |
| DeliverySurface | Web/API/Bot/CLI/Skill registry | Bot live、SDK package、developer portal、public sandbox token |
| SecurityControl | RBAC、secret scan、audit_event、retention policy、OWASP mapping baseline | OIDC/IdP、SIEM、不可变审计、retention cleaner、租户隔离 |
| ObservabilitySignal | health/ready/metrics/requestId、OTel-compatible span log、SLO/alert rules baseline | OTel SDK/collector/exporter、trace backend、real error budget |
| ReleaseArtifact | local release artifacts、GHCR digest/attestation 曾对 0050 运行过 | 每个 release commit 复跑、签名验证、审计聚合 |
| AuditHandoff | 分散在任务 closeout | 一键聚合 markdown/json、证据索引、外部 pending 清单 |

## Target End State

```text
Client / Agent / Web / Bot / CLI / Skill
  -> OpenAPI / SDK / Auth / Rate Limit
  -> Capability Control Plane
  -> CalculationJob Durable Runtime
  -> Provider Adapter + Mature Engine + Data Source
  -> Evidence Builder + Report Builder
  -> Evaluation + Observability + Security + Supply Chain + Release Gates
  -> AuditHandoff
```

FateCat 100% 成立条件：

- 所有 production capability 都必须通过同一 executor、provider protocol、policy gate、evidence gate 和 report profile。
- 所有异步副作用都有 event history、idempotency、retry/timeout、outbox、签名、审计和恢复策略。
- 所有外部依赖都有真实证据或明确标记外部连通验证待执行。
- 所有核心测算质量都有 golden、snapshot、benchmark、coverage 和人工复核边界。
- 所有发布结论都能从 Git、CI、artifact、contract、registry、script output 逐项复核。

## Complete Implementation Tree

```text
MI-100 FateCat 测算基础设施 100%
  MI-100.01 Durable Runtime
    MI-100.01.01 external backend contract and migration smoke
    MI-100.01.02 Postgres job store adapter with claim/release
    MI-100.01.03 distributed worker lease and crash recovery smoke
    MI-100.01.04 public webhook live delivery smoke
    MI-100.01.05 external Vault/KMS secret provider
  MI-100.02 Event Platform
    MI-100.02.01 CloudEvents envelope schema
    MI-100.02.02 AsyncAPI document for job/webhook/evaluation/release events
    MI-100.02.03 event compatibility and example smoke
  MI-100.03 Observability and SRE
    MI-100.03.01 OTel SDK instrumentation
    MI-100.03.02 collector/exporter config
    MI-100.03.03 trace backend evidence
    MI-100.03.04 SLO dashboard and error budget
    MI-100.03.05 alert dry/live evidence and incident drill
  MI-100.04 Security and Privacy
    MI-100.04.01 OIDC/IdP integration
    MI-100.04.02 tenant/authz negative tests
    MI-100.04.03 external SIEM or immutable audit storage
    MI-100.04.04 retention cleaner
    MI-100.04.05 privacy and LLM-output scanner
  MI-100.05 Developer Platform
    MI-100.05.01 OpenAPI release artifact and compatibility changelog
    MI-100.05.02 SDK package or installable examples
    MI-100.05.03 sandbox token service
    MI-100.05.04 developer portal smoke
  MI-100.06 Provider Platform
    MI-100.06.01 provider trace spans
    MI-100.06.02 dependency/source/license drift scanner
    MI-100.06.03 provider compatibility matrix
    MI-100.06.04 promotion/deprecation automation
  MI-100.07 Core Quality
    MI-100.07.01 bazi corpus expansion
    MI-100.07.02 ziwei corpus expansion
    MI-100.07.03 full report golden diff
    MI-100.07.04 evidence coverage and broken-ref fail-fast
    MI-100.07.05 MingLi-Bench runner and no-leak policy
    MI-100.07.06 conflict explainer and counter-evidence templates
  MI-100.08 Multi-Surface Parity
    MI-100.08.01 Web/API/Bot/CLI/Skill semantic diff
    MI-100.08.02 Markdown copy snapshot
    MI-100.08.03 Bot live report diff
    MI-100.08.04 public demo privacy guard
  MI-100.09 Release Proof
    MI-100.09.01 current commit remote CI
    MI-100.09.02 container digest/signature/attestation
    MI-100.09.03 SBOM/provenance verification
    MI-100.09.04 rollback drill
  MI-100.10 Audit Package
    MI-100.10.01 audit handoff markdown/json
    MI-100.10.02 evidence bundle index
    MI-100.10.03 risk register and external pending list
    MI-100.10.04 third-party audit dry-run
```

## Recommended Next Slices

| Next Task | Why | Minimum Deliverable | Cannot Fake |
| --- | --- | --- | --- |
| 0062 durable runtime external backend contract | 当前最大 P0 缺口 | RuntimeBackend registry/schema/gate，选 Postgres 为首个 adapter path，Temporal 为长流程 future orchestrator | 不能声明 external backend 已生产 |
| 0063 CloudEvents/AsyncAPI baseline | webhook/job 已形成事件，需要机器契约 | event schema、examples、docs smoke | 不能只写自然语言事件说明 |
| 0064 OTel collector/SLO adapter plan | observability 还停在本地语义 baseline | collector config、trace smoke dry-run、SLO evidence contract | 不能伪造 trace backend |
| 0065 security externalization | 公开服务需要真实身份和审计边界 | OIDC/SIEM/retention cleaner implementation plan + negative tests | 不能用本地 token 代替 IdP |
| 0066 core quality corpus expansion | 测算基础设施的专业地基 | corpus manifest、bazi/ziwei sample expansion、full report diff policy | 不能使用真实用户隐私样例 |
| 0067 developer platform | 外部开发者接入还不够 | SDK/package baseline、sandbox token contract、API changelog | 不能把 docs smoke 说成发布 SDK |
| 0068 audit handoff generator | 100% 需要第三方可复核 | audit bundle markdown/json generator | 不能遗漏 pending external validations |

## Failure Conditions

以下任一成立，就不能声明 FateCat 达到 100% 基础设施：

- 生产路径绕过 capability executor、provider protocol、policy gate、evidence gate 或 report profile。
- external backend、Bot live、OIDC、SIEM、OTel backend、Vault/KMS 等外部项无证据却写成已完成。
- release artifact 没有 current commit 的 CI、digest、SBOM/provenance 和 attestation verification。
- 八字/紫微只靠代表样本，没有 corpus、全文 diff、evidence coverage 或人审边界。
- 新术数 capability 直接混入默认综合八字报告，绕过 capability 协议和独立输出。
- 审计包无法从 Git、CI、artifact、contract、registry、script output 逐项复核。
