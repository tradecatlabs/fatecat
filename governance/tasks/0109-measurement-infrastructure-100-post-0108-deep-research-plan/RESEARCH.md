# Post-0108 深度调研

## 当前仓库事实

| Item | Evidence | Meaning |
| --- | --- | --- |
| Current branch | `git status --short --branch` -> `## main...origin/main` plus local task docs changes | 本轮只分析当前 `main` worktree，不切分支。 |
| Current HEAD | `git rev-parse HEAD` -> `4d4abe2edab118e661382cbcd6d0bd244591d3a1` | 0108 任务包提交已在当前 HEAD。 |
| Current commit | `git log -1 --oneline` -> `4d4abe2 docs: add current release artifact proof task` | 本轮计划基于 0108 任务包之后的状态。 |
| Current remote runs | `gh run view 28675408793` / `gh run view 28675409943` | Container run `28675409943` 已 `success`；Acceptance run `28675408793` 的 `Run acceptance gate` step 已 `success`，但 workflow/job 在本次取证时仍为 `in_progress`，`Post Checkout` step 未 terminal。 |
| Task index hygiene | `governance/tasks/INDEX.md` tail | 0108 在 INDEX 中存在重复行，一行 `Done`、一行 `In Progress`；这是后续 release proof 和任务治理的近因盲区。 |
| Scope | User request + `$auto-tasks` | 本任务只做调研、计划与任务树落盘，不实现业务代码、不触发生产 live、不伪造外部验证。 |

## 外部资料版本快照

| 领域 | 官方资料 | 2026-07-04 取证结果 | FateCat 映射 |
| --- | --- | --- | --- |
| HTTP API contract | https://spec.openapis.org/oas/latest.html | Latest 页面标注 OpenAPI Specification v3.2.0 / Version 3.2.0。 | API 机器契约、错误码、示例、SDK 生成和兼容策略以 OAS 3.2.0 为目标口径。 |
| Async API contract | https://www.asyncapi.com/docs/reference/specification/latest | Latest 页面为 AsyncAPI 3.1.0。 | job、webhook、evaluation、release 事件以 AsyncAPI 3.1.0 描述。 |
| Event envelope | https://cloudevents.io/ | CloudEvents 是事件元数据标准入口。 | webhook/job/evaluation/release event 必须统一 envelope，而不是每个渠道自造字段。 |
| Control plane | https://kubernetes.io/docs/concepts/architecture/controller/ | Controller 模式以 desired/current state 和控制循环收敛系统状态。 | Capability、Provider、ReleaseGate、EvaluationRun 需要 spec/status 与 drift reconciliation。 |
| Durable execution | https://docs.temporal.io/evaluate/understanding-temporal | Temporal 强调 durable execution、event history、crash recovery。 | CalculationJob/ReportJob 需要 event history、lease、retry、restart recovery、replay 和 external backend evidence。 |
| Observability | https://opentelemetry.io/docs/concepts/signals/ | OpenTelemetry signals 覆盖 traces、metrics、logs、baggage、profiles。 | API -> job -> provider -> report 必须能用 traceId/requestId 串联，且接入外部 OTel backend。 |
| SRE | https://sre.google/sre-book/service-level-objectives/ | SLI/SLO/error budget 用于驱动可靠性管理和发布取舍。 | FateCat 需要 p95/p99、job success、provider success、error budget、alert 和 incident drill。 |
| API security | https://owasp.org/API-Security/editions/2023/en/0x11-t10/ | OWASP API Security 2023 覆盖 BOLA、资源消耗、敏感业务流、SSRF 和不安全 API 消费。 | API 需要 authz negative tests、rate limit/body limit、inventory、SSRF 防护、第三方 API 消费策略。 |
| Secure SDLC | https://csrc.nist.gov/pubs/sp/800/218/final | NIST SP 800-218 SSDF v1.1 是安全软件开发框架。 | secure defaults、secret scan、dependency/source gate、漏洞响应、release evidence 必须进入门禁。 |
| AI risk | https://www.nist.gov/itl/ai-risk-management-framework | AI RMF 1.0 正在修订；2026 年新增 critical infrastructure profile concept note。 | FateCat 的 Agent/LLM 解释层必须有风险分级、免责声明、高风险建议禁止和输出扫描。 |
| Supply chain | https://slsa.dev/spec/v1.2/ | SLSA v1.2 是当前供应链保证口径。 | release proof 需绑定 source、builder、digest、provenance、attestation verify。 |
| SBOM | https://cyclonedx.org/specification/overview/ | CycloneDX 当前版本 1.7，覆盖 components、services、dependencies、formulation、declarations、citations。 | FateCat 需要 code/vendor/data/service SBOM，且能表达典籍、vendor、provider 和 release artifact 来源。 |
| Artifact attestation | https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations | GitHub artifact attestations 用于建立 build provenance，容器镜像以 digest 作为 subject。 | Container release workflow 必须输出 registry digest、artifact attestation、SBOM/provenance 和 verify command。 |

## 100% 的新定义

这里的 100% 不是“预测准确率 100%”，也不是“所有术数功能都做完”。它是基础设施完备度：

- 能力资源化：所有体系都是 `Capability`，有状态、成熟度、可见性、provider、测试门禁和风险策略。
- 执行同源化：Web/API/Bot/CLI/Skill/HF 不自行拼核心结果，全部通过同一 executor/profile。
- 计算可复现：核心 provider 声明来源、版本、deterministic、输入契约、数据版本和 golden。
- 解释可审计：关键结论有 evidence、ruleId、source、basis、weight、confidence、conflict/counter-evidence。
- 运行可恢复：job 有幂等、event history、lease、retry、timeout、restart recovery、callback/outbox。
- 交付可证明：当前 release commit 有远端 CI、digest、SBOM/provenance、attestation verify、rollback drill。
- 生产可运营：health/ready/metrics/traces/logs/SLO/alerts/runbook/incident drill 不停留在本地样例。
- 安全可复核：OIDC/RBAC、rate limit、secret externalization、SIEM、retention、privacy regression、AI risk policy 全闭合。
- 审计可交接：第三方能按 Git、CI、artifact、contract、registry、script、runbook 逐项复核。

## 资源缺口矩阵

| Resource | 当前状态 | 100% 目标 | 下一切片 |
| --- | --- | --- | --- |
| `ReleaseArtifact` | 0108 已提交 release proof 任务包；Container final-head run 已 success；Acceptance gate step 已 success 但 workflow/job 取证时仍 in progress；INDEX 有 0108 重复状态。 | 每个 release commit 有 Acceptance/Container success、GHCR digest、SBOM/provenance、GitHub attestation verify、rollback drill、clean git。 | Release proof finalizer：清理 0108 状态漂移，等待/验证 Acceptance，生成 current-release-proof。 |
| `Capability` | bazi/ziwei/almanac/meihua 已进入 capability 思路；planned 能力已有登记。 | 所有 production/experimental/planned 能力都有 spec/status、admission、promotion、deprecation、drift。 | Capability control-plane reconciliation gate。 |
| `Provider` | 有 provider metadata、source/license drift trend 和成熟开源复用口径。 | 每个 provider 有 lockfile、health、trace span、license/source trend、compat matrix、rollback/deprecation。 | Provider lifecycle controller。 |
| `CalculationJob` | SQLite/Postgres/job/webhook/retry/recovery/lease/heartbeat 等本地和 staged gate 已有。 | 真实外部 backend、多副本长期运行、exactly-once 边界、公网 webhook passed、外部 secret live。 | External runtime proof pack。 |
| `Evidence` | evidence coverage trend、rule depth、classics index、broken-ref gate 已有。 | 冲突分类、反证模板、覆盖率阈值、人工抽样、人审签名和趋势回退 fail-fast。 | Evidence conflict/counter-evidence gate。 |
| `EvaluationRun` | runner/history/trend/current audit bundle 已有。 | 远端 current commit artifact、external benchmark runner、nightly 趋势、failure taxonomy、dashboard。 | Remote evaluation artifact + MingLi-Bench runner。 |
| `DeliverySurface` | 多端 semantic diff 覆盖 Web/API/Bot dry-run/CLI/Skill/HF 合同的一部分。 | Web/API/Bot/CLI/Skill/HF 全部 live 或明确 pending；Markdown/JSON 同源快照。 | Live parity proof pack。 |
| `SecurityControl` | RBAC、secret scan、retention、OIDC/SIEM staged gate、本地 privacy regression 已有。 | 真实 IdP/OIDC、SIEM/immutable audit、tenant isolation live、retention scheduler、AI output scanner。 | External security proof pack。 |
| `ObservabilitySignal` | OTel-compatible local span、SLO/alert rules、staged evidence contract 已有。 | OTel collector/backend、trace query URL、SLO dashboard、alert route、incident drill。 | External OTel/SRE proof pack。 |
| `DeveloperPlatform` | OpenAPI/export/docs smoke、SDK baseline metadata、sandbox contract 已有。 | 发布版 SDK/package、developer portal、sandbox token issuer/revocation、API changelog、examples CI。 | Public DX release baseline。 |
| `AuditHandoff` | current audit bundle、release proof、risk register、pending external list 多次扩展。 | 一键审计包可由第三方独立复核，所有 pending 有 owner、证据路径、关闭条件。 | Third-party audit rehearsal。 |

## 完整实现波次

| Wave | Priority | 目标 | 主要产物 | 不可伪造验收 |
| --- | --- | --- | --- | --- |
| W0 | P0 | Current release truth | 清理 0108 状态漂移、等待 Acceptance terminal、运行 current-release-proof、记录 digest/attestation/rollback dry-run | 当前 HEAD 的 Actions run URL/headSha/conclusion、GHCR digest、attestation verify、rollback JSON、git clean |
| W1 | P0 | Control plane | Capability/Provider/ReleaseGate/EvaluationRun spec-status registry、drift scanner、promotion/deprecation gate | planned 拒绝执行、status 漂移 fail-fast、registry 与 executor 对账 |
| W2 | P0 | Runtime proof | External backend、多副本 job worker、公网 webhook、external secret provider、exactly-once 边界 | 真实 endpoint/backend/receiver/secret provider 证据；无凭证则 `外部连通验证待执行` |
| W3 | P0 | Core quality | 八字/紫微大规模匿名 corpus、节气/起运/真太阳时边界、紫微格局、全文 summary diff、人审抽样 | golden diff、coverage trend、broken-ref 0、人审抽样记录、不保存真实隐私 |
| W4 | P0 | Observability/SRE | OTel collector/backend、trace query、SLO dashboard、alert route、incident drill | trace backend URL、dashboard/alert evidence、incident drill report |
| W5 | P0 | Security/privacy | OIDC/IdP、tenant authz、SIEM、retention scheduler、privacy/AI output scanner | IdP/SIEM/retention live evidence、OWASP negative tests、no-secret scan |
| W6 | P1 | Developer platform | OpenAPI 3.2 artifact、AsyncAPI 3.1 events、SDK package、developer portal、sandbox token issuer | SDK install smoke、docs smoke、sandbox issue/revoke smoke、API changelog |
| W7 | P1 | Provider platform | provider trace、compat matrix、source/license drift、vendor/data SBOM | provider lifecycle gate、CycloneDX SBOM、source/license trend |
| W8 | P0 | Multi-surface live parity | Web/API/Bot/CLI/Skill/HF 同源 semantic diff 与 live smoke | 每个 surface 的 live/dry-run 分级证据；Bot live 不能用 dry-run 替代 |
| W9 | P0 | Audit and certification | certification aggregator、audit handoff、risk register、external pending owner、third-party rehearsal | 审计包能逐项复核；第三方审计结果不能由本地 dry-run 冒充 |

## 最短下一步

1. 先做 W0：释放 0108 的 release proof 状态漂移，不要让任务索引、任务文档、GitHub Actions 状态互相打架。
2. 再做 W1：把 `Capability`、`Provider`、`ReleaseGate`、`EvaluationRun` 升级成真正的 control-plane resource，而不是散落 JSON。
3. 然后并行 W2/W4/W5：这些都依赖外部生产环境，必须准备 token、域名、receiver、IdP、SIEM、OTel backend、Vault/KMS。
4. W3 持续推进：八字/紫微核心正确性是测算基础设施的业务地基，必须扩 corpus 和 evidence。
5. W6/W7 做开发者平台和 provider 平台，最后 W8/W9 做多端 live 和审计交接。

## 不可伪造口径

- `workflow_dispatch` 命令退出 0 只证明已发起，不证明通过。
- GitHub Actions `in_progress` 不能写成 `success`。
- 本地 dry-run rollback 不能写成真实生产回滚。
- local-ci 不能替代远端 current commit CI。
- Staged gate 不能替代真实 IdP/SIEM/OTel/Vault/KMS。
- Bot dry-run 不能替代 Bot live smoke。
- 典籍/外部资料 manifest 不能替代法律/版权人工意见。
- 任何 `外部连通验证待执行` 项都必须保留 owner、凭证依赖、关闭条件和复核命令。
