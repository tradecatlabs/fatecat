# Repo Evidence

- 当前目录：`/home/lenovo/.projects/fatecat`。
- 当前分支：`main...origin/main`。
- 当前 worktree：任务开始时 `git status --short --branch` 无未提交文件。
- 上一实际任务：`0048-measurement-infrastructure-telegram-bot-live-smoke`。
- 当前阻断事实：0048 缺少真实 `FATE_BOT_TOKEN`，Telegram Bot live smoke 仍为 `Blocked`。
- 主路线图：`docs/reference-materials/roadmap/测算基础设施100%实现计划.md`。

# External Research Sources

| Source | URL | FateCat usage |
| --- | --- | --- |
| CNCF Cloud Native Definition | https://www.cncf.io/about/who-we-are/ | 解耦、可观测、自动化的总体基础设施原则 |
| OpenAPI Specification | https://spec.openapis.org/oas/latest.html | HTTP API 机器可读契约 |
| AsyncAPI Specification | https://www.asyncapi.com/docs/reference/specification/latest | webhook/job/event 机器可读契约 |
| CloudEvents | https://cloudevents.io/ | 事件信封统一 |
| Kubernetes Controllers | https://kubernetes.io/docs/concepts/architecture/controller/ | spec/status 与 reconciliation 控制面 |
| Backstage System Model | https://backstage.io/docs/features/software-catalog/system-model/ | Component/API/Resource catalog 模型 |
| Terraform Providers | https://developer.hashicorp.com/terraform/language/providers | provider 版本锁定和配置模型 |
| Temporal Durable Execution | https://docs.temporal.io/evaluate/understanding-temporal | durable job、event history、retry/recovery |
| OpenTelemetry Signals | https://opentelemetry.io/docs/concepts/signals/ | traces/metrics/logs/baggage |
| Google SRE SLO | https://sre.google/sre-book/service-level-objectives/ | SLI/SLO/error budget |
| OWASP API Security Top 10 | https://owasp.org/API-Security/editions/2023/en/0x11-t10/ | API security regression |
| NIST SSDF | https://csrc.nist.gov/pubs/sp/800/218/final | 安全开发和供应链沟通 |
| NIST AI RMF | https://www.nist.gov/itl/ai-risk-management-framework | AI/Agent 风险治理 |
| SLSA v1.2 | https://slsa.dev/spec/v1.2/ | provenance/attestation |
| CycloneDX | https://cyclonedx.org/specification/overview/ | SBOM/service dependency model |
| GitHub artifact attestations | https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations | container digest/attestation/verify |

# Change Boundary

允许修改：

- `docs/reference-materials/roadmap/测算基础设施100%实现计划.md`
- `governance/tasks/0049-measurement-infrastructure-100-deep-research-implementation-plan/*`
- `governance/tasks/INDEX.md`

禁止修改：

- 业务源码
- CI workflow
- 真实 secret
- release artifact
- 外部账号配置

# Critical Assumption

本任务只补计划，不替代后续 `MI-NEXT-*` 实现。任何外部平台、真实 token、registry attestation、OIDC/SIEM、监控平台结论都必须继续标记为未完成或外部连通验证待执行。

# Constraints Matrix

| 约束 | 处理 |
| --- | --- |
| 必须基于当前 worktree | 先执行 `git status --short --branch` 并读取现有路线图/任务索引。 |
| 必须查询相关资料 | 使用一手/官方资料链接，并在任务上下文中登记。 |
| 不得伪造生产完成 | 路线图只写计划、缺口和完成判定，不写外部平台已通过。 |
| 0048 仍被 token 阻断 | 明确继续 Blocked，不用计划文档掩盖。 |
| 不制造平行事实源 | 只补主路线图 `0.5`，任务包记录本轮证据。 |

# Risk Matrix

| 风险 | 等级 | 控制 |
| --- | --- | --- |
| 把“计划”误读为“已完成” | 高 | 所有外部证据继续标记待执行或后续实现。 |
| 外部资料泛化过度 | 中 | 只提取基础设施同构能力，不照搬无关产品形态。 |
| 文档漂移 | 中 | 主路线图作为唯一长期计划入口，任务包只做证据。 |
| 阻断项被隐藏 | 高 | 0048 Bot token、registry attestation、OIDC/SIEM、监控告警均显式保留缺口。 |

# Assumptions and Falsification

- 假设：FateCat 的 100% 目标是基础设施成熟度，而不是预测命中率或功能数量。
- 证伪方式：如果后续 MI-NEXT 任务无法直接按路线图创建和验收，则说明本计划仍不够具体。
- 调试模式: Optional

# Critical Ambiguities

- 是否优先做 registry attestation 还是 durable runtime：本计划建议在 0048 阻断时先做可独立推进的 registry attestation。
- 生产身份、监控、SIEM 具体平台尚未确定：保持平台无关 contract，后续任务绑定真实平台时再细化。

# Debug Evidence Contract

Not Required。本任务不是 bug 修复；失败只可能来自文档契约校验不通过。

# Task Package Context Map

- TP-01.01：读取仓库现状、任务索引、0048 阻断和 contracts 资源。
- TP-02.01：调研并记录外部资料链接。
- TP-03.01：更新主路线图。
- TP-04.01：运行校验并回填状态。
