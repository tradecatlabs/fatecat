# Post-0094 100% 测算基础设施深度调研与完整实现计划

## 1. 结论

FateCat 距离 100% 测算基础设施，当前主要缺口已经不是“有没有更多术数模块”，而是四类基础设施闭环：

1. 核心质量闭环：八字/紫微需要更大匿名 corpus、全文报告 diff、evidence coverage、冲突/反证解释。
2. 外部生产闭环：真实 Bot、公开 API/HF、Webhook、OIDC、SIEM、OTel、Vault/KMS、多副本运行仍需要外部连通证据。
3. 开发者闭环：公开 SDK/package、developer portal、sandbox token issuer/revocation、兼容 changelog 仍需生产级发布。
4. 审计闭环：每个 release commit 都要重新聚合 current release proof 和 audit bundle，不能沿用旧提交证据。

100% 的定义不是预测准确率 100%，也不是术数体系数量 100%，而是：能力可发现、接口可接入、任务可恢复、事件可订阅、质量可回归、运行可观测、安全可证明、发布可验证、审计可交接。

## 2. 当前仓库事实

| 事实 | 证据 | 对计划的影响 |
| --- | --- | --- |
| 当前基准提交 | `git rev-parse HEAD` -> `e34418ca01dbae2f01a81a0c9bf3fc32e5615ef5` | 0095 计划基于 0094 之后的当前 `main`。 |
| 0093 已完成 | `governance/tasks/0093-measurement-infrastructure-cli-capability-command-baseline/STATUS.md` | CLI capability command baseline 已进入本地交付面。 |
| 0094 已完成 | `governance/tasks/0094-measurement-infrastructure-cli-skill-semantic-diff-expansion/STATUS.md` | CLI/Skill semantic evidence 已补入 multi-surface parity。 |
| 主路线图已有 100% living plan | `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` | 本任务只追加 post-0094 刷新，不新建平行真相源。 |
| 核心质量资产已有基础 | `contracts/fate/evaluations/core-quality-corpus.json`、`report-diff-policy.json`、`mingli-bench-gate.json` | 下一阶段应扩容 corpus/report diff，而不是重建评测框架。 |
| 外部 live 仍未完全闭合 | 主路线图的 Bot、OIDC、SIEM、OTel、Vault/KMS、多副本项均标注外部待验证 | 不允许在计划中写成 production live passed。 |

## 3. 外部基础设施同构资料

| 领域 | 一手资料 | 基础设施共同能力 | FateCat 对应要求 |
| --- | --- | --- | --- |
| HTTP API 契约 | OpenAPI Specification: https://spec.openapis.org/oas/latest.html | 机器可读接口、schema、错误、示例、版本 | `/api/v1/*`、OpenAPI release artifact、错误码、SDK 示例、changelog。 |
| 异步 API 契约 | AsyncAPI Specification: https://www.asyncapi.com/docs/reference/specification/latest | 消息、channel、operation、event schema | report job、webhook、evaluation、release 事件必须有契约。 |
| 事件信封 | CloudEvents: https://cloudevents.io/ | `id/source/type/subject/time/data` 等事件元数据标准化 | job/webhook/evaluation/release 事件统一 envelope，支持审计和 replay。 |
| 控制面 | Kubernetes Controllers: https://kubernetes.io/docs/concepts/architecture/controller/ | desired/current state 与 reconciliation | capability/provider/release/security/evaluation 要有 spec/status、drift scanner、promotion/deprecation。 |
| 软件目录 | Backstage System Model: https://backstage.io/docs/features/software-catalog/system-model/ | Component/API/Resource/System 可发现 | Capability、Provider、Dataset、EvaluationRun、SecurityControl、DeliverySurface 进入 catalog/registry。 |
| Provider 生态 | Terraform Providers: https://developer.hashicorp.com/terraform/language/providers | provider 版本、来源、配置、生命周期 | bazi/ziwei/almanac/meihua provider 需要 engineVersion、source/license、health、compat matrix。 |
| 持久工作流 | Temporal Durable Execution: https://docs.temporal.io/evaluate/understanding-temporal | event history、恢复、重试、长流程可靠状态 | CalculationJob 需要 external backend、worker lease、heartbeat、restart recovery。 |
| 可观测 | OpenTelemetry Signals: https://opentelemetry.io/docs/concepts/signals/ | traces、metrics、logs 统一 | API -> job -> provider -> report 要有 trace、metrics、structured logs、backend evidence。 |
| SRE | Google SRE SLO: https://sre.google/sre-book/service-level-objectives/ | SLI/SLO/error budget 管可靠性 | availability、latency、job success、provider failure、alert/runbook。 |
| 交付效能 | DORA metrics: https://dora.dev/guides/dora-metrics-four-keys/ | deployment frequency、lead time、change failure、MTTR | release gate、rollback drill、current commit CI、change failure 记录。 |
| API 安全 | OWASP API Security Top 10 2023: https://owasp.org/API-Security/editions/2023/en/0x11-t10/ | 授权、认证、资源消耗、库存、配置风险 | OIDC/RBAC、tenant isolation、rate/body limit、API inventory、negative tests。 |
| 安全开发 | NIST SSDF SP 800-218: https://csrc.nist.gov/pubs/sp/800/218/final | 安全开发、供应链保护、漏洞响应 | secret scan、dependency review、release evidence、incident response。 |
| AI 风险治理 | NIST AI RMF: https://www.nist.gov/itl/ai-risk-management-framework | AI 风险识别、治理、评测、监控 | AI/Agent 只能解释结构化结果，禁止确定性断语和高风险替代建议。 |
| 供应链安全 | SLSA v1.2: https://slsa.dev/spec/v1.2/ | provenance、build integrity、artifact proof | current commit CI、container digest、attestation verify、provenance。 |
| SBOM | CycloneDX Specification: https://cyclonedx.org/specification/overview/ | 组件、服务、依赖、关系、license 可机器读 | release SBOM、data/vendor SBOM、dependency graph、license/export policy。 |
| Artifact attestation | GitHub Artifact Attestations: https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations | build provenance 和 artifact identity 可验证 | 每个 release commit 需要 workflow、digest、attestation verify、证据 URL。 |
| 幂等与 Webhook | Stripe idempotent requests（docs.stripe.com/api/idempotent_requests）和 webhooks（docs.stripe.com/webhooks） | 幂等、防重复副作用、签名、重试、事件历史 | report job idempotency、webhook signature、retry/outbox、event audit。 |

## 4. 100% 资源成熟度矩阵

| Resource | 当前 post-0094 状态 | 100% 目标 | 下一步证据 |
| --- | --- | --- | --- |
| Capability | registry/executor/profile 已有，planned 能力拒绝执行 | 所有生产体系统一 executor/policy/evidence/report profile，promotion/deprecation 自动化 | provider/capability drift 和 admission gate 持续通过。 |
| Provider | provider protocol、health、dependency smoke、drift scanner baseline 已有 | source/license/dependency 长期趋势、compat matrix、人审许可复核 | drift report、license review、trace evidence。 |
| CalculationJob | SQLite/Postgres 多项本地和 live smoke baseline 已有 | 多副本长期运行、生产 secret lifecycle、真实公网投递、严格幂等边界 | multi-replica live evidence、public webhook live passed、Vault/KMS live。 |
| Event | CloudEvents/AsyncAPI 风格 contract baseline 已有 | producer/consumer compatibility、DLQ/replay、event history 可审计 | consumer/replay contract tests。 |
| ReportProfile | Markdown policy/snapshot、多端语义 diff 已有 | 全文 diff、跨端同源、报告结构演进策略、人审抽样 | report diff gate、semantic hash、snapshot artifact。 |
| Evidence | evidenceRefs、规则索引、broken-ref baseline 已有 | coverage 量化、反证解释、冲突裁决自然语言化 | evidence coverage summary、counter-evidence fixtures。 |
| Dataset | data supply chain manifest、core corpus baseline 已有 | 更大匿名 corpus、节气/紫微/八字边界覆盖、人审样本分层 | corpus manifest、coverage matrix、no-leak gate。 |
| EvaluationRun | runner/history/dashboard/nightly baseline 已有 | 当前 commit nightly artifact、外部 benchmark aggregate、趋势库 | evaluation summary、MingLi-Bench aggregate gate。 |
| DeliverySurface | Web/API/Bot/CLI/Skill registry 和本地 diff baseline 已有 | 真实 live parity、Bot live、public HF/API live、SDK examples | live smoke、multi-surface diff、SDK smoke。 |
| ObservabilitySignal | health/ready/metrics/logs/local spans/SLO rules baseline 已有 | OTel collector/backend、trace 查询、alert live、error budget | OTel backend/SLO staged evidence。 |
| SecurityControl | RBAC、secret scan、audit、retention、OWASP baseline 已有 | OIDC/IdP、SIEM、生产 retention scheduler、tenant isolation live | OIDC/SIEM/retention live evidence。 |
| ReleaseArtifact | local release artifacts、current proof/audit baseline 已有 | 每个 release commit digest、SBOM/provenance、attestation verify、rollback drill | current release proof rerun。 |
| AuditHandoff | audit generator/dry-run baseline 已有 | 第三方能逐项复核所有证据和 pending external list | current audit bundle rerun + external pending closure。 |

## 5. Post-0094 完整实现计划

### Wave A：本地可继续推进，不依赖外部账号

| 顺序 | 建议任务 | 目标 | 验收证据 |
| --- | --- | --- | --- |
| Next-01 | 八字/紫微 corpus/report diff expansion | 扩大核心质量回归集，不保存真实用户隐私或完整报告正文 | corpus manifest、coverage matrix、report diff policy、focused pytest、quick CI。 |
| Next-02 | Event platform consumer/replay contract tests | 让 CloudEvents/AsyncAPI 不只停在 schema，补消费者兼容和 replay/DLQ 策略 | producer/consumer tests、replay examples、negative cases。 |
| Next-03 | Retention production cleanup staged gate | 把 0091 本地 SQLite retention 推进到 Postgres/scheduler/SIEM 证据口径 | staged gate、blocked/live summary、anti-forgery tests。 |
| Next-04 | Provider/source/license long-running drift trend | 防止 provider registry、source manifest、license status 与实际运行漂移 | drift trend summary、provider trace source refs、license review pending list。 |
| Next-05 | 100% certification aggregator dry-run | 把 release proof、audit bundle、external pending、core quality、security/SRE 汇总成一个总门禁 | certification JSON，必须区分 passed/blocked/pending。 |

### Wave B：需要外部环境后执行

| 顺序 | 建议任务 | 依赖 | 不能伪造的证据 |
| --- | --- | --- | --- |
| Live-01 | Telegram Bot live smoke | 真实 Bot 凭证 | live smoke output，不输出凭证。 |
| Live-02 | Public API/HF live smoke | 真实公开域名或 Space | TLS/CORS/token/response evidence。 |
| Live-03 | Public webhook live passed | Postgres DSN + 公网 HTTPS receiver | signed event delivery、outbox terminal status、receiver proof ref。 |
| Live-04 | OTel backend/SLO live | Collector/exporter/backend 权限 | trace query link、SLO dashboard、alert route evidence。 |
| Live-05 | OIDC/SIEM/retention live | IdP、SIEM、scheduler 权限 | issuer/JWKS/RBAC proof、SIEM ingestion/query proof、retention run proof。 |
| Live-06 | Vault/KMS and multi-replica runtime live | secret manager、多副本部署窗口 | key lifecycle、access audit、多副本 heartbeat/lease evidence。 |

### Wave C：开发者平台产品化

| 顺序 | 建议任务 | 目标 | 验收证据 |
| --- | --- | --- | --- |
| DX-01 | Public developer portal | 外部开发者不读源码即可接入 | portal smoke、OpenAPI artifact、examples links。 |
| DX-02 | SDK/package release baseline to public channel | 形成可安装 SDK 或官方 examples 包 | package dry/live publish evidence、install smoke。 |
| DX-03 | Sandbox token issuer/revocation | 提供受控体验环境 | token issuer/revocation proof、scope/rate limit/audit tests。 |

### Wave D：发布与审计闭环

| 顺序 | 建议任务 | 目标 | 验收证据 |
| --- | --- | --- | --- |
| Ship-01 | Current release proof rerun | 每个 release commit 重新证明 CI、digest、attestation、rollback | GitHub Actions URL、digest、attestation verify、rollback drill。 |
| Ship-02 | Current audit bundle rerun | 生成第三方可复核交接包 | audit markdown/json、risk register、pending external validations。 |
| Ship-03 | Third-party audit dry/live handoff | 让外部审计人员按证据复核 | 独立复核结果，未验证项不隐藏。 |

## 6. 递归任务树

```text
MI-100 FateCat 100% 测算基础设施
  MI-100.A 本地质量与平台闭环
    MI-100.A.01 八字/紫微 corpus/report diff expansion
    MI-100.A.02 Event consumer/replay contract tests
    MI-100.A.03 Retention production cleanup staged gate
    MI-100.A.04 Provider/source/license drift trend
    MI-100.A.05 Certification aggregator dry-run
  MI-100.B 外部生产连通闭环
    MI-100.B.01 Telegram Bot live smoke
    MI-100.B.02 Public API/HF live smoke
    MI-100.B.03 Public webhook live passed
    MI-100.B.04 OTel backend/SLO/alert live
    MI-100.B.05 OIDC/SIEM/retention live
    MI-100.B.06 Vault/KMS and multi-replica runtime live
  MI-100.C 开发者平台
    MI-100.C.01 Public developer portal
    MI-100.C.02 SDK/package public release
    MI-100.C.03 Sandbox token issuer/revocation
  MI-100.D 发布审计
    MI-100.D.01 Current release proof rerun
    MI-100.D.02 Current audit bundle rerun
    MI-100.D.03 Third-party audit handoff
```

## 7. 不可伪造完成标准

FateCat 只有在以下全部成立时，才能声明“100% 测算基础设施”：

- 当前 worktree clean，所有 100% 相关切片已提交推送，远端 CI 对当前 commit 通过。
- 所有 production capability 通过统一 executor/provider/policy/evidence/report profile。
- 八字/紫微 core corpus、report diff、evidence coverage 和冲突/反证门禁通过。
- Web/API/Bot/CLI/Skill 具备同源验证；真实 Bot/API/HF live 不能由 dry-run 替代。
- CalculationJob 多副本、Webhook、外部 secret、retry/recovery/retention 有真实或明确 pending 的证据。
- OIDC/SIEM/OTel/SLO/alert/retention 等外部项有真实平台证据；没有证据则必须写 `外部连通验证待执行`。
- 每个 release commit 重新产出 release proof、artifact、attestation、rollback drill 和 audit bundle。
- 第三方审计包能从 Git、CI、contract、registry、script 输出和外部 proof ref 逐项复核。

## 8. 下一步建议

不等外部账号时，下一步应执行 `八字/紫微 corpus/report diff expansion`。这是当前最像“基础设施质量地基”的本地可执行任务：它不依赖生产凭证，但会直接提升测算基础设施的核心可信度。
