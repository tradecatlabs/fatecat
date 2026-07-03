# Post-0098 100% 测算基础设施深度调研与完整实现计划

## 1. 结论

FateCat 要达到 100% 测算基础设施，剩余工作不是继续堆更多预测体系，而是把现有八字、紫微、黄历、梅花和未来 capability 统一放进基础设施资源模型中治理。

这里的 100% 只表示工程基础设施成熟度：

- 能力可发现：Capability、Provider、Dataset、EvaluationRun、DeliverySurface、SecurityControl、ObservabilitySignal、ReleaseArtifact、AuditHandoff 都有 registry/schema/status。
- 计算可复现：生产 capability 只能通过统一 executor/provider/protocol 执行，planned 能力拒绝执行。
- 解释可审计：报告 evidence、规则索引、冲突裁决、反证说明和 policy gate 可回归。
- 运行可恢复：CalculationJob、Webhook、event history、retry/outbox、lease、heartbeat、external backend 可证明。
- 生产可观测：OpenTelemetry traces、metrics、logs、SLO/error budget、alert/runbook 有真实或 staged evidence。
- 安全可证明：OIDC/RBAC/SIEM/retention/secret provider/privacy regression 有负例和证据口径。
- 发布可验证：current commit CI、container digest、SBOM/provenance、attestation、rollback drill、audit bundle 可复核。

100% 不是预测准确率 100%，也不是术数功能数量 100%。任何确定性命中断言或生产 live 通过声明都必须有真实证据，否则统一写 `外部连通验证待执行`。

## 2. 当前仓库事实

| 事实 | 证据 | 对计划的影响 |
| --- | --- | --- |
| 当前分支 | `git status --short --branch` -> `## main...origin/main` | 计划只针对当前分支/current worktree。 |
| 当前基准提交 | `eee30ece7da5fa580eb970db11e3b7e559727a56` / `eee30ec test: add event consumer replay contracts` | 0099 基于 0097 后，且 0098 在当前 worktree 中。 |
| 当前 worktree | `contracts/fate/security/*`、`scripts/local-ci.sh`、0098 task docs、0099 task docs等修改/新增 | 0098 本地 closeout 已通过；后续需做版本控制收口和下一波任务。 |
| 0096 已完成 | `governance/tasks/0096-*` | Core corpus/report diff 首轮扩容已完成。 |
| 0097 已完成 | `governance/tasks/0097-*`，commit `eee30ec` | Event consumer/replay contract 首轮已完成。 |
| 0098 本地 closeout | `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0098-final-pass` -> 275 passed | Retention production cleanup staged gate 本地可验证；外部 scheduler/Postgres/SIEM live 仍待执行。 |
| 主路线图存在 | `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` | 0099 只追加 post-0098 delta，不新建第二路线图。 |

## 3. 外部基础设施同构资料

| 领域 | 官方/事实标准资料 | 提炼出的基础设施能力 | FateCat 对应要求 |
| --- | --- | --- | --- |
| 平台工程 | CNCF Platform Engineering Maturity Model: https://tag-app-delivery.cncf.io/whitepapers/platform-eng-maturity-model/ | 平台作为产品，自助能力、治理、反馈、度量和持续改进 | FateCat 要把 capability、provider、job、report、audit、DX 做成可自助、可度量、可治理的平台能力。 |
| 云原生 | CNCF Cloud Native Definition: https://www.cncf.io/about/who-we-are/ | 松耦合、弹性、可观测、自动化 | 计算、解释、交付、评测、观测、安全、发布必须解耦且自动化。 |
| HTTP API | OpenAPI Specification: https://spec.openapis.org/oas/latest.html | 机器可读 API、schema、错误、示例、版本 | `/api/v1/*`、OpenAPI artifact、错误码、SDK 示例、兼容 changelog。 |
| 异步 API | AsyncAPI Specification: https://www.asyncapi.com/docs/reference/specification/latest | 消息、channel、operation、event schema | report job、webhook、evaluation、release event 需要机器可读契约。 |
| 事件信封 | CloudEvents: https://cloudevents.io/ | 标准事件元数据，便于路由、审计、replay | job/webhook/evaluation/release 事件统一 envelope，支持 DLQ/replay。 |
| 控制面 | Kubernetes Controllers: https://kubernetes.io/docs/concepts/architecture/controller/ | spec/status、desired/current reconciliation | capability/provider/release/security/evaluation 需要 desired spec、runtime status、drift scanner。 |
| 软件目录 | Backstage System Model: https://backstage.io/docs/features/software-catalog/system-model/ | Component/API/Resource/System 可发现 | Capability、Provider、Dataset、EvaluationRun、DeliverySurface、SecurityControl 等进入 catalog/registry。 |
| Provider 生态 | Terraform Providers: https://developer.hashicorp.com/terraform/language/providers | provider 版本、配置、来源、生命周期 | bazi/ziwei/almanac/meihua provider 要有 engineVersion、source/license、health、compat matrix、deprecation。 |
| 持久工作流 | Temporal Durable Execution: https://docs.temporal.io/evaluate/understanding-temporal | event history、长流程恢复、重试、状态可靠 | CalculationJob 需要 external backend、worker lease、heartbeat、restart recovery 和非重试错误分类。 |
| 可观测 | OpenTelemetry Signals: https://opentelemetry.io/docs/concepts/signals/ | traces、metrics、logs 统一 | API -> job -> provider -> report 链路要有 trace、metrics、logs 和 backend evidence。 |
| SRE | Google SRE SLO: https://sre.google/sre-book/service-level-objectives/ | SLI/SLO/error budget | availability、latency、job success、provider success、alert/runbook。 |
| 交付效能 | DORA Four Keys: https://dora.dev/guides/dora-metrics-four-keys/ | 部署频率、变更前置时间、失败率、恢复时间 | release gate、rollback drill、current commit CI、change failure/MTTR evidence。 |
| API 安全 | OWASP API Security Top 10 2023: https://owasp.org/API-Security/editions/2023/en/0x11-t10/ | 授权、认证、资源消耗、库存、配置风险 | OIDC/RBAC、tenant isolation、rate limit、body limit、API inventory、negative tests。 |
| 安全开发 | NIST SSDF SP 800-218: https://csrc.nist.gov/pubs/sp/800/218/final | 安全开发、漏洞减少、供应链沟通 | secret scan、dependency review、release evidence、vulnerability response、audit handoff。 |
| AI 风险治理 | NIST AI RMF: https://www.nist.gov/itl/ai-risk-management-framework | AI 风险识别、治理、评测、监控 | AI/Agent 只能解释结构化测算结果，禁止高风险替代建议和确定性恐吓断语。 |
| 供应链 | SLSA v1.2: https://slsa.dev/spec/v1.2/ | provenance、build integrity、artifact proof | current commit CI、container digest、attestation verify、provenance。 |
| SBOM | CycloneDX Specification: https://cyclonedx.org/specification/overview/ | 组件、服务、依赖、关系、license 可机器读 | release SBOM、data/vendor SBOM、service dependency graph、license/export policy。 |
| Artifact 证明 | GitHub Artifact Attestations: https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations | build provenance 和 artifact identity 可验证 | 每个 release commit 需要 workflow、digest、attestation verify、证据 URL。 |
| 幂等与 Webhook | [Stripe Idempotent Requests](https://docs.stripe.com/api/idempotent_requests)；[Stripe Webhooks](https://docs.stripe.com/webhooks) | 幂等、防重复副作用、签名、重试、事件历史 | report job idempotency、webhook signature、retry/outbox、event audit。 |

## 4. 资源成熟度矩阵

| Resource | 当前状态 | 100% 目标 | 剩余关键任务 |
| --- | --- | --- | --- |
| Capability | registry/executor/profile 已有，planned 拒绝执行 | 全 production capability 统一 executor/policy/evidence/report profile | certification aggregator dry-run、promotion/deprecation gate。 |
| Provider | provider protocol、dependency smoke、lifecycle/drift baseline 已有 | 版本锁、source/license 长期趋势、compat matrix、trace span、人审许可 | provider/source/license long-running drift trend。 |
| CalculationJob | SQLite/Postgres/job/webhook/recovery 多个 baseline 已有 | 多副本长期运行、真实公网 webhook、external secret、exactly-once 边界 | external live Wave B：webhook、Vault/KMS、multi-replica。 |
| Event | 0097 已补 consumer/replay/DLQ contract baseline | 真实 broker/consumer 兼容、replay 操作审计、DLQ 处置闭环 | staged broker evidence、consumer contract live。 |
| ReportProfile | Markdown policy/snapshot、多端语义 diff 已有 | 全文结构 diff、人审抽样、profile 兼容策略 | report-diff 扩容、semantic hash、review artifact。 |
| Evidence | evidenceRefs、规则索引、broken-ref gate 已有 | coverage 量化、冲突裁决、反证解释自然语言化 | evidence coverage trend、counter-evidence fixtures。 |
| Dataset | data supply chain、core corpus baseline 已有 | 大规模匿名 corpus、历法/紫微/八字边界、人审分层 | corpus expansion、license/legal review。 |
| EvaluationRun | runner/history/dashboard/nightly baseline 已有 | current commit nightly artifact、外部 benchmark aggregate、趋势库 | MingLi-Bench aggregate refresh、quality trend store。 |
| DeliverySurface | Web/API/Bot/CLI/Skill registry 与本地 parity 已有 | 真实 Bot/API/HF live parity、SDK/package、developer portal | external live + DX waves。 |
| ObservabilitySignal | health/ready/metrics/logs/local spans/SLO rules/staged OTel 已有 | OTel collector/backend、SLO dashboard、alert live、incident drill | OTel backend live、alert route evidence。 |
| SecurityControl | RBAC、secret scan、audit、retention、OWASP baseline；0098 staged cleanup local closeout passed | OIDC/IdP、SIEM、retention scheduler、tenant isolation live | OIDC/SIEM/retention external live。 |
| ReleaseArtifact | release artifact、digest/attestation baseline exists from earlier tasks | 每个 release commit 重新证明 digest/SBOM/provenance/rollback | current release proof rerun after dirty worktree is committed。 |
| AuditHandoff | audit generator/dry-run baseline 已有 | 第三方能逐项复核，pending external list 完整 | current audit bundle rerun after release proof。 |

## 5. Post-0098 完整实现计划

### Wave 0：当前状态收口

| Order | Task | Goal | Evidence |
| --- | --- | --- | --- |
| 0.1 | Finish 0098 local closeout | 完成 retention production cleanup staged gate final validation 和 task closeout | quick local-ci、secret scan、task validator。 |
| 0.2 | Current worktree hygiene | 对 0098/0099 做版本控制收口 | clean git status 或明确分批 commit plan。 |

### Wave A：本地可推进，不依赖外部账号

| Order | Task | Goal | Evidence |
| --- | --- | --- | --- |
| A1 | Provider/source/license long-running drift trend | 防止 provider、source manifest、license status 随时间漂移 | trend summary、provider trace refs、license review pending list、negative tests。 |
| A2 | 100% certification aggregator dry-run | 聚合 release、audit、external pending、core quality、security/SRE 为总门禁 | certification JSON，区分 passed/blocked/pending/in-progress。 |
| A3 | Evidence coverage trend | 把 evidence broken-ref 从点状 gate 升级为覆盖率趋势 | coverage summary、counter-evidence cases、conflict explanation checks。 |
| A4 | Current audit bundle refresh | 基于最新 commits 重新聚合审计包 | audit markdown/json、risk register、external pending list。 |

### Wave B：需要外部环境后执行

| Order | Task | Dependency | Non-fake Evidence |
| --- | --- | --- | --- |
| B1 | Telegram Bot live smoke | `FATE_BOT_TOKEN` | `get_me`/live command output，不输出 token。 |
| B2 | Public API/HF live smoke | public URL / HF Space | TLS/CORS/token/response evidence。 |
| B3 | Public webhook live passed | Postgres DSN + HTTPS receiver | signed delivery、receiver proof ref、outbox terminal state。 |
| B4 | OTel backend/SLO/alert live | collector/exporter/backend | trace query link、dashboard proof、alert route proof。 |
| B5 | OIDC/SIEM/retention live | IdP/SIEM/scheduler | issuer/JWKS/RBAC proof、SIEM ingestion/query proof、retention run proof。 |
| B6 | Vault/KMS + multi-replica runtime live | external secret manager + deployment window | key lifecycle、access audit、多副本 heartbeat/lease evidence。 |

### Wave C：开发者平台产品化

| Order | Task | Goal | Evidence |
| --- | --- | --- | --- |
| C1 | Public developer portal | 外部开发者不读源码即可接入 | portal smoke、OpenAPI artifact、examples links。 |
| C2 | SDK/package public release | 形成可安装 SDK 或官方 examples 包 | package publish/install smoke、version changelog。 |
| C3 | Sandbox token issuer/revocation | 受控体验环境 | issuer/revocation proof、scope/rate limit/audit tests。 |

### Wave D：发布审计闭环

| Order | Task | Goal | Evidence |
| --- | --- | --- | --- |
| D1 | Current release proof rerun | 每个 release commit 重新证明发布链路 | GitHub Actions URL、digest、attestation verify、rollback drill。 |
| D2 | Third-party audit dry-run | 外部审计前自检证据完整性 | audit checklist、evidence index、unknowns list。 |
| D3 | Third-party audit handoff | 让审计人员逐项复核 | 独立复核结果；未验证项不隐藏。 |

## 6. 递归任务树

```text
MI-100 FateCat 100% 测算基础设施
  MI-100.00 当前状态收口
    MI-100.00.01 Finish 0098 local closeout
    MI-100.00.02 Current worktree hygiene
  MI-100.A 本地控制面与质量闭环
    MI-100.A.01 Provider/source/license drift trend
    MI-100.A.02 Certification aggregator dry-run
    MI-100.A.03 Evidence coverage trend
    MI-100.A.04 Current audit bundle refresh
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
    MI-100.D.02 Third-party audit dry-run
    MI-100.D.03 Third-party audit handoff
```

## 7. 不可伪造完成标准

FateCat 只有在以下全部成立时，才能声明“100% 测算基础设施”：

- 当前 worktree clean，所有 100% 相关切片已提交推送，远端 CI 对当前 commit 通过。
- 所有 production capability 通过统一 executor/provider/policy/evidence/report profile。
- 八字/紫微 core corpus、report diff、evidence coverage、冲突/反证门禁通过，且不保存真实用户隐私样本。
- Web/API/Bot/CLI/Skill 具备同源验证；真实 Bot/API/HF live 不能由 dry-run 替代。
- CalculationJob 多副本、Webhook、外部 secret、retry/recovery/retention 有真实或明确 pending 的证据。
- OIDC/SIEM/OTel/SLO/alert/retention 等外部项有真实平台证据；没有证据则必须写 `外部连通验证待执行`。
- 每个 release commit 重新产出 release proof、artifact、attestation、rollback drill 和 audit bundle。
- 第三方审计包能从 Git、CI、contract、registry、script output 和 external proof ref 逐项复核。

## 8. 下一步

完成 0098/0099 版本控制收口后，按本地 Wave A 执行：

1. Provider/source/license long-running drift trend。
2. 100% certification aggregator dry-run。
3. Evidence coverage trend。
4. Current audit bundle refresh。

这些都不依赖外部账号，能继续把基础设施成熟度往前推；外部 live wave 保持待执行，直到真实凭证和平台就绪。
