# Post-0105 深度调研

## 当前事实

| Item | Evidence | Meaning |
| --- | --- | --- |
| Current branch | `git status --short --branch` -> `## main...origin/main` | 本轮只分析当前 `main` worktree。 |
| Current HEAD | `git log -1 --oneline` -> `e146d05 test: add evaluation trend audit evidence` | 0105 已提交并推送到 `origin/main`。 |
| Remote CI visibility | `gh run list --commit HEAD --limit 10 --json ...` -> `[]` | 当前 HEAD 没有可见 GitHub Actions run；不能声明 current commit 远端 CI 已通过。 |
| Workflow trigger model | `.github/workflows/acceptance.yml`、`container.yml`、`evaluation-nightly.yml`、`hf-space-deploy.yml` 均为 `workflow_dispatch`，nightly 另有 schedule | 仓库故意不在 push 自动跑 Acceptance/Container；远端证据必须手动触发或由发布流程生成。 |
| 0104 | `governance/tasks/0104-.../STATUS.md` 和 local-ci artifact | EvaluationRun trend gate 已有本地门禁。 |
| 0105 | `governance/tasks/0105-.../STATUS.md` | current audit bundle 已纳入 `evidence.evaluation_trend_gate`。 |

## 官方资料版本快照

| 领域 | 官方资料 | 当前事实 | FateCat 映射 |
| --- | --- | --- | --- |
| HTTP API contract | https://spec.openapis.org/oas/latest.html | Latest 版本为 OpenAPI Specification v3.2.0，页面标注 Version 3.2.0。 | API artifact、schema、错误码、示例、SDK 生成和兼容策略必须对齐 OAS 3.2 口径。 |
| Async API contract | https://www.asyncapi.com/docs/reference/specification/latest | latest 跳转到 AsyncAPI 3.1.0。 | job/webhook/evaluation/release events 的机器契约应继续以 AsyncAPI 3.1 为目标口径。 |
| Event envelope | https://cloudevents.io/ | CloudEvents 是事件元数据标准入口。 | webhook、job terminal、evaluation 和 release event 保持 CloudEvents envelope。 |
| Control plane | https://kubernetes.io/docs/concepts/architecture/controller/ | Kubernetes controllers 通过控制循环管理期望状态和当前状态。 | Capability、Provider、ReleaseGate、EvaluationRun 需要 desired/current/status 与 drift reconciliation。 |
| Software catalog | https://backstage.io/docs/features/software-catalog/system-model/ | Backstage system model 用 Component/API/Resource/System 表达平台目录。 | catalog/registry 必须能发现 Capability、Provider、Dataset、DeliverySurface、SecurityControl。 |
| Durable execution | https://docs.temporal.io/evaluate/understanding-temporal | Temporal durable execution 将 workflow 状态保存为 event history。 | CalculationJob/ReportJob 需要 event history、retry、lease、restart recovery 和 external backend evidence。 |
| Observability | https://opentelemetry.io/docs/concepts/signals/ | OpenTelemetry signals 覆盖 traces、metrics、logs、baggage 等。 | API -> job -> provider -> report 需要 trace/metric/log 关联，外部 backend 证据仍待执行。 |
| Delivery metrics | https://dora.dev/guides/dora-metrics/ | DORA 当前五项软件交付指标包括 change lead time、deployment frequency、failed deployment recovery time、change fail rate、deployment rework rate。 | FateCat 需要 release/evaluation trend，不只记录单次测试通过。 |
| Supply chain | https://slsa.dev/spec/v1.2/ | SLSA v1.2 是当前计划使用的供应链等级口径。 | release artifact 必须绑定 provenance、builder、source、digest、verification command。 |
| SBOM | https://cyclonedx.org/specification/overview/ | CycloneDX 当前版本 1.7，可表达 components、services、dependencies、formulation、declarations、citations。 | FateCat 的 code/vendor/data/service 供应链应向 CycloneDX 1.7 口径升级。 |
| Artifact attestation | https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations | GitHub artifact attestations 用于建立 build provenance。 | current release proof 必须绑定 GitHub Actions run URL、head SHA、digest 和 attestation verify。 |
| SLO | https://sre.google/sre-book/service-level-objectives/ | Google SRE 以 SLO/SLI/error budget 管理可靠性。 | FateCat 需要真实 SLO dashboard、alert route 和 incident drill 证据，不能只靠本地 rules。 |

## Post-0105 结论

0104/0105 解决的是质量趋势和审计证据的近因盲区：EvaluationRun trend gate 已能进入 current audit bundle。下一层缺口不再是“本地脚本少一个 artifact”，而是“当前提交远端证据和外部生产平台证据仍未闭合”。

## 资源成熟度矩阵

| Resource | Current | 100% Requirement | Next Slice |
| --- | --- | --- | --- |
| ReleaseArtifact | 本地 release proof/audit bundle/gate artifacts 已多次扩展；当前 HEAD 无可见 Actions run。 | 每个 release commit 有 Acceptance/Container run URL、digest、attestation verify、rollback drill。 | 0107 current remote CI evidence refresh。 |
| EvaluationRun | runner/history/diff/dashboard/nightly/trend gate/current bundle evidence 已有。 | 远端 current commit artifact、长期趋势、external benchmark summary 和 failure taxonomy。 | Remote evaluation artifact ingestion。 |
| Evidence | evidence coverage trend 与 evaluation trend 已进入 current audit bundle。 | 冲突解释、counter-evidence、规则来源断链和趋势回退全部 fail-fast。 | 继续扩规则深度和冲突裁决。 |
| Core Bazi/Ziwei | L4/corpus/report diff/evidence gate baseline 已有。 | 大规模匿名 golden、节气边界、紫微典型格局、人审抽样。 | Core corpus expansion wave。 |
| Runtime | SQLite/Postgres/lease/heartbeat/webhook gate baseline 已有。 | 真实公网 webhook passed、外部 Vault/KMS、长期多副本、exactly-once 边界。 | External live wave。 |
| SecurityControl | RBAC/secret scan/retention/OIDC-SIEM staged gate baseline 已有。 | 真实 IdP/SIEM/retention scheduler/tenant isolation live。 | External security live wave。 |
| ObservabilitySignal | local spans、OTel staged gate、SLO contract baseline 已有。 | OTel collector/backend、trace query、SLO dashboard、alert live、incident drill。 | External OTel/SRE wave。 |
| DeliverySurface | Web/API/Bot/CLI/Skill/HF contracts 与多端 semantic diff baseline 已有。 | 真实 Bot/API/HF live parity、public developer portal、SDK package、sandbox issuer。 | DX/live wave。 |
| AuditHandoff | current audit bundle 已聚合 gate artifacts。 | 第三方审计独立复核、外部 pending 全闭合或带 owner。 | Audit dry-run plus third-party handoff。 |

## 后续执行波次

| Wave | Priority | Task | Done Definition |
| --- | --- | --- | --- |
| A | P0 | Current remote CI evidence refresh | 手动触发或捕获当前 commit Acceptance/Container run，更新 release proof/audit bundle，不把 running/absent 写成 passed。 |
| A | P0 | Remote evaluation artifact integration | evaluation-nightly current commit artifact 可被 trend gate 和 audit bundle 引用。 |
| A | P0 | Core quality deep corpus expansion | bazi/ziwei 增加匿名边界样本、summary-only report diff 和 evidence coverage trend。 |
| B | P0 | Production live proof | Bot/API/HF/webhook/OIDC/SIEM/OTel/Vault/KMS/multi-replica live 逐项拿真实证据。 |
| C | P1 | Developer platform public release | developer portal、SDK/package、sandbox issuer/revocation 和 changelog 可供外部开发者使用。 |
| D | P0 | Third-party audit handoff | 外部审计人员可按 Git、CI、artifact、contract、registry、script 逐项复核。 |

## 不可伪造口径

- `gh run list --commit HEAD` 返回空时，远端 CI current commit 只能标为 missing/pending。
- `workflow_dispatch` 存在只证明“可以触发”，不证明“已经通过”。
- local-ci passed 只证明本机门禁，不替代 GitHub Actions。
- current audit bundle passed 只证明审计包结构和本地 evidence 齐备，不替代第三方审计。
- external live 没有真实 token、账号、域名、receiver、trace backend 或 SIEM query 时，统一写 `外部连通验证待执行`。
