# Post-0072 100% 基础设施深度调研与完整实现计划

## Research Question

FateCat 要达到 100% 测算基础设施，还差什么？这里的 100% 不是预测命中率，也不是术数模块数量，而是基础设施成熟度：开发者能接入、Agent 能调用、任务能恢复、事件能订阅、报告能回归、结论能追溯、运行能观测、安全能证明、发布能验证、审计能交接。

## Current Facts

| Fact | Evidence | Meaning |
| --- | --- | --- |
| 0071 已完成 | `governance/tasks/INDEX.md` 中 0071 为 `Done` | Postgres migration/job live smoke baseline 已进入计划事实。 |
| 0072 已完成 | `governance/tasks/INDEX.md` 中 0072 为 `Done` | Postgres worker lease negative smoke 已交付，但不能写成 job execution worker lease 或 exactly-once。 |
| 当前 worktree 不干净 | `git status --short --branch` 显示多个 modified/untracked 文件 | 本计划只记录事实，不做发布结论。 |
| 100% 路线图已有历史段落 | 主路线图已有 0.5、0.6、0.8 | 本任务追加 0.9 作为最新 living plan，不删除历史。 |

## Source Matrix

| 领域 | 一手资料 | 基础设施能力 | FateCat 同构要求 |
| --- | --- | --- | --- |
| API contract | OpenAPI Specification: `https://spec.openapis.org/oas/latest.html` | 机器可读接口、schema、版本、示例 | 发布版 OpenAPI、错误码、changelog、SDK/package、兼容性测试。 |
| Async API | AsyncAPI Specification: `https://www.asyncapi.com/docs/reference/specification/latest` | 消息和事件接口可机器消费 | job/webhook/evaluation/release event 需要 AsyncAPI 或等价 contract。 |
| Event envelope | CloudEvents: `https://cloudevents.io/` | 事件元数据标准化 | 统一 `id/source/type/subject/time/data`，并绑定 requestId/traceId。 |
| Control plane | Kubernetes Controllers: `https://kubernetes.io/docs/concepts/architecture/controller/` | desired/current state 和 reconciliation | Capability/Provider/ReleaseGate 要有 spec/status、drift scanner 和准入状态。 |
| Provider ecosystem | Terraform Providers: `https://developer.hashicorp.com/terraform/language/providers` | provider 版本、配置、依赖和锁定 | 每个测算体系必须声明 providerId、engineVersion、source/license、health、deprecation。 |
| Durable workflow | Temporal Durable Execution: `https://docs.temporal.io/evaluate/understanding-temporal` | 长流程状态持久、失败恢复、event history | CalculationJob 需要 external backend、event history、retry/timeout、worker lease、crash recovery。 |
| Database coordination | PostgreSQL `SELECT ... FOR UPDATE SKIP LOCKED`: `https://www.postgresql.org/docs/current/sql-select.html` | 多 worker 竞争安全 claim | Postgres outbox/job claim 需要并发 negative smoke、错误 owner release negative、lease expiry reclaim。 |
| Observability | OpenTelemetry Signals: `https://opentelemetry.io/docs/concepts/signals/` | traces、metrics、logs 统一 | API -> job -> provider -> report 的 trace/span、指标、结构化日志和 backend evidence。 |
| SRE | Google SRE SLO: `https://sre.google/sre-book/service-level-objectives/` | SLI/SLO、error budget、告警 | latency、availability、job success、provider failure、error budget burn alert。 |
| Platform engineering | CNCF Platform Engineering Maturity Model: `https://tag-app-delivery.cncf.io/whitepapers/platform-eng-maturity-model/` | 平台作为产品，强调自助、治理、反馈和度量 | FateCat 必须让开发者/Agent 自助发现能力、看状态、接入和验证。 |
| Cloud native | CNCF Cloud Native Definition: `https://www.cncf.io/about/who-we-are/` | 松耦合、弹性、可管理、可观测和自动化 | 不能把 Web/API/Bot/Skill、provider、job、report 写成互相耦合的脚本集合。 |
| API security | OWASP API Security Top 10 2023: `https://owasp.org/API-Security/editions/2023/en/0x11-t10/` | 授权、认证、资源消耗、库存风险 | OIDC/RBAC、tenant isolation、rate/body limit、API inventory、negative tests。 |
| Secure development | NIST SSDF SP 800-218: `https://csrc.nist.gov/pubs/sp/800/218/final` | 安全开发、供应链、漏洞响应 | secret scan、dependency review、release evidence、incident response、security control registry。 |
| AI risk | NIST AI RMF: `https://www.nist.gov/itl/ai-risk-management-framework` | AI 风险治理 | AI/Agent 只能解释结构化结果，不自行重算命盘，不输出高风险替代建议。 |
| Supply chain | SLSA v1.2: `https://slsa.dev/spec/v1.2/` | provenance、attestation、供应链等级 | current commit CI、container digest、artifact attestation、source/vendor/data provenance。 |
| SBOM | CycloneDX: `https://cyclonedx.org/specification/overview/` | 组件、依赖、服务和关系可机器读取 | release SBOM、data/vendor SBOM、dependency graph、license/export policy。 |
| Artifact proof | GitHub Artifact Attestations: `https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations` | build provenance 和 artifact verify | 每个 release commit 重新生成并验证 attestation，不复用旧 commit 证据。 |
| External API idempotency | Stripe Idempotent requests and webhooks docs，路径为 `https://docs.stripe.com/api/idempotent_requests` 与 `https://docs.stripe.com/webhooks` | 幂等、异步事件、签名、重试 | report job idempotency、webhook signature、retry/outbox、event audit。 |

## Resource Maturity Matrix

| Resource Domain | Current | 100% Target | Next Proof |
| --- | --- | --- | --- |
| Capability Control Plane | registry/executor/profiles 已有；planned 能力可拒绝 | spec/status、admission、promotion、deprecation、drift scanner 全部自动化 | capability/provider drift scanner + promotion gate |
| Provider Platform | bazi/ziwei/almanac/meihua production provider baseline | provider trace、dependency health、source/license drift、compatibility matrix、rollback | provider trace span + source/license drift report |
| CalculationJob Durable Runtime | memory/sqlite + Postgres adapter/live smoke；0072 worker lease 正在本地推进 | job execution worker lease、crash restart、多副本协调、公网 webhook、external secret provider、at-least-once + idempotent delivery | 完成 0072 后，做 job execution worker lease + crash recovery smoke |
| Event Platform | CloudEvents/AsyncAPI baseline 已有 | producer/consumer contract tests、event versioning、dead-letter、replay/audit | event compatibility smoke + webhook consumer fixture |
| Report/Evidence | policyGate、snapshotGate、evidenceRefs baseline | 全文 golden diff、evidence coverage、broken-ref fail-fast、counter-evidence | report diff runner + evidence coverage gate |
| Core Quality | 八字/紫微 L4 代表样本 | 大规模匿名 corpus、MingLi-Bench runner、人审抽样、趋势报告 | corpus expansion + external benchmark runner |
| Developer Platform | OpenAPI/example/sandbox baseline | 发布 SDK/package、developer portal、sandbox token、fixed snapshot、compat changelog | SDK smoke + portal docs smoke |
| Observability/SRE | local OTel-compatible span、SLO/alert rules | OTel SDK/collector/exporter/backend、dashboards、error budget、alert live、incident drill | collector live or staged backend evidence |
| Security/Privacy | token/RBAC/secret scan/audit_event/retention policy baseline | OIDC/IdP、tenant isolation、SIEM/immutable audit、retention cleaner、privacy/LLM scanner | OIDC/SIEM external evidence contract -> live smoke |
| Supply Chain/Release | local artifacts + GHCR/attestation baseline existed for prior commit | every release commit has digest、SBOM/provenance、attestation verify、rollback drill | current commit release proof run |
| Multi-Surface Delivery | Web/API/Bot/CLI/Skill registry | semantic diff across surfaces、Bot live、HF/API live、Markdown copy snapshot | multi-surface semantic diff smoke |
| Audit Handoff | generator/dry-run baseline | one-command audit bundle with evidence index, pending externals, risk register, third-party review | audit bundle for current commit |

## Complete Implementation Tree

```text
MI-100 FateCat 测算基础设施 100%
  MI-100.01 Durable Runtime
    MI-100.01.01 Postgres job execution worker lease
    MI-100.01.02 crash/restart recovery with external backend
    MI-100.01.03 public webhook live delivery smoke
    MI-100.01.04 external Vault/KMS or secret manager provider
    MI-100.01.05 delivery semantics: at-least-once + idempotency + duplicate negative tests
  MI-100.02 Control Plane
    MI-100.02.01 capability/provider spec-status reconciliation
    MI-100.02.02 drift scanner for registry vs runtime behavior
    MI-100.02.03 promotion/deprecation automation
    MI-100.02.04 planned/experimental negative execution gates
  MI-100.03 Event Platform
    MI-100.03.01 event version compatibility matrix
    MI-100.03.02 webhook consumer contract fixture
    MI-100.03.03 dead-letter and replay policy
    MI-100.03.04 event audit and trace linkage
  MI-100.04 Provider Platform
    MI-100.04.01 provider trace spans
    MI-100.04.02 dependency/source/license drift scanner
    MI-100.04.03 provider compatibility matrix
    MI-100.04.04 provider rollback and deprecation runbook
  MI-100.05 Core Quality and Evaluation
    MI-100.05.01 bazi corpus expansion
    MI-100.05.02 ziwei corpus expansion
    MI-100.05.03 full report golden diff
    MI-100.05.04 evidence coverage and broken-ref fail-fast
    MI-100.05.05 MingLi-Bench runner and no-leak policy
    MI-100.05.06 conflict explainer and counter-evidence templates
  MI-100.06 Developer Platform
    MI-100.06.01 release OpenAPI artifact and compatibility changelog
    MI-100.06.02 SDK package or installable examples
    MI-100.06.03 sandbox token service
    MI-100.06.04 developer portal smoke
  MI-100.07 Observability and SRE
    MI-100.07.01 OTel SDK instrumentation
    MI-100.07.02 collector/exporter config
    MI-100.07.03 trace backend evidence
    MI-100.07.04 SLO dashboard and error budget
    MI-100.07.05 alert dry/live evidence and incident drill
  MI-100.08 Security and Privacy
    MI-100.08.01 OIDC/IdP integration
    MI-100.08.02 tenant/authz negative tests
    MI-100.08.03 external SIEM or immutable audit storage
    MI-100.08.04 retention cleaner
    MI-100.08.05 privacy and LLM-output scanner
  MI-100.09 Multi-Surface Parity
    MI-100.09.01 Web/API/Bot/CLI/Skill semantic diff
    MI-100.09.02 Markdown copy snapshot
    MI-100.09.03 Bot live report diff
    MI-100.09.04 public demo privacy guard
  MI-100.10 Supply Chain and Release Proof
    MI-100.10.01 current commit remote CI
    MI-100.10.02 container digest/signature/attestation
    MI-100.10.03 SBOM/provenance verification
    MI-100.10.04 rollback drill
  MI-100.11 Audit Package
    MI-100.11.01 audit handoff markdown/json
    MI-100.11.02 evidence bundle index
    MI-100.11.03 risk register and external pending list
    MI-100.11.04 third-party audit dry-run
```

## Recommended Execution Order

| Order | Task | Why | Minimum Evidence |
| --- | --- | --- | --- |
| 1 | Postgres job execution worker lease | 0072 只覆盖 webhook outbox claim，生产还需要 job execution lease | 多 worker job claim negative、lease expiry、crash/restart |
| 2 | Public webhook live smoke | callback 是外部副作用，必须真实公网验证签名/重试/隐私 | disposable receiver URL、signed event verified、secret redacted |
| 3 | External secret provider | 本地 Fernet 不等于生产密钥生命周期 | Vault/KMS/secret manager dry-run + live evidence |
| 4 | OTel backend and SLO | 无 trace backend 和 error budget 就没有生产可运维性 | collector/exporter config、trace backend link、SLO evidence |
| 5 | OIDC/SIEM/retention | 公开服务需要真实身份和审计闭环 | IdP evidence、SIEM event evidence、retention cleaner smoke |
| 6 | Core corpus and benchmark | 基础设施不能只稳定运行，还要稳定正确 | bazi/ziwei corpus、MingLi-Bench runner、report diff |
| 7 | Developer platform release | 基础设施必须让第三方开发者可接入 | SDK/package smoke、developer portal docs smoke、sandbox token |
| 8 | Current release proof | 每个 release commit 都需要不可伪造证据 | current commit CI、digest、SBOM/provenance、attestation verify |
| 9 | Audit package | 100% 结论要能给第三方复核 | audit bundle markdown/json、risk register、pending external list |

## 100% Completion Gates

- 所有 production capability 必须通过同一个 executor、provider protocol、policy gate、evidence gate 和 report profile。
- 所有异步 job 必须有 durable backend、event history、idempotency、retry/timeout、outbox、签名、审计和恢复策略。
- 所有外部依赖必须有真实证据；没有证据只能写“外部连通验证待执行”。
- 所有核心测算质量必须有 golden、snapshot、benchmark、coverage、人审边界和差异报告。
- 所有发布结论必须能从 Git、CI、artifact、contract、registry、script output 逐项复核。
- 所有安全边界必须覆盖认证、授权、租户隔离、限流、secret scan、SIEM、retention 和隐私回归。

## Failure Conditions

以下任一成立，就不能声明 FateCat 达到 100% 基础设施：

- 0072 或任何 outbox lease smoke 被写成 job execution worker lease、exactly-once 或生产完成。
- dry-run、本地 smoke、contract gate 被写成真实 live。
- external backend、Bot live、OIDC、SIEM、OTel backend、Vault/KMS、公网 webhook 无证据却写成完成。
- 新术数能力绕过 capability/provider/evidence/report 协议进入默认报告。
- 八字/紫微只靠少量代表样本，没有 corpus、全文 diff、evidence coverage 或人审边界。
- release artifact 没有 current commit 的 CI、digest、SBOM/provenance 和 attestation verification。
- 审计包无法从 Git、CI、artifact、contract、registry、script output 逐项复核。
