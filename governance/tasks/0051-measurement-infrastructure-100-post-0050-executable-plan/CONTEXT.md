# Repo Evidence

- 当前目录：`/home/lenovo/.projects/fatecat`。
- 当前分支：`main...origin/main`。
- 当前任务事实：0048 Telegram Bot live smoke 因缺真实 `FATE_BOT_TOKEN` 保持 Blocked。
- 当前 release 事实：0050 已完成一次 GHCR digest、GitHub artifact attestation 和 verify gate；后续每个 release commit 仍需重跑。
- 当前文档事实：主路线图为 `docs/reference-materials/roadmap/测算基础设施100%实现计划.md`。

# User Request

用户要求使用 `auto-tasks` 深度调研、查询相关资料，并制作 FateCat 达到 100% 测算基础设施所需的完整实现计划。

# Current Repository Facts

- `governance/tasks/0048-measurement-infrastructure-telegram-bot-live-smoke/` 仍为 Blocked，原因是当前环境缺少真实 `FATE_BOT_TOKEN`。
- `governance/tasks/0050-measurement-infrastructure-registry-attestation/` 已完成一次 GHCR digest、GitHub artifact attestation 和 verify gate。
- 主路线图为 `docs/reference-materials/roadmap/测算基础设施100%实现计划.md`。
- FateCat 当前定位为面向 Agent 与应用开发者的测算基础设施。

# External Research Lines

- API 契约：OpenAPI。
- 异步事件：AsyncAPI、CloudEvents。
- 控制面：Kubernetes controller pattern。
- Provider 生态：Terraform provider pattern。
- 持久运行：Temporal durable execution 与 retry policy。
- 可观测：OpenTelemetry traces/metrics/logs。
- SRE：SLO、error budget、incident/runbook。
- 安全：OWASP API Security、NIST SSDF、OIDC/IdP、SIEM。
- 供应链：SLSA、CycloneDX、GitHub artifact attestations。
- AI 风险治理：NIST AI RMF。

# Constraints Matrix

| 约束 | 处理 |
| --- | --- |
| 本任务只做计划 | 不改业务代码、不新增服务、不配置外部平台 |
| 不能伪造 100% | 路线图明确外部 live evidence 待执行 |
| 不能重复路线图 | 复用主路线图，新增 `0.6`，不新建平行 roadmap |
| 0050 已完成 | registry attestation 从待办移出 immediate next list |
| 0048 仍阻断 | Bot live 继续标为缺真实 token |
| 新功能不能绕过协议 | 所有新体系必须进入 capability/provider/evidence/evaluation 控制面 |

# Change Boundary

允许修改：

- `docs/reference-materials/roadmap/测算基础设施100%实现计划.md`
- `governance/tasks/0051-measurement-infrastructure-100-post-0050-executable-plan/*`
- `governance/tasks/INDEX.md`

禁止修改：

- 业务测算源码
- API 行为
- CI workflow
- 真实 secret 和 `.env`
- 0050 远端 workflow 历史事实

# Risk Matrix

| 风险 | 等级 | 控制 |
| --- | --- | --- |
| 把计划误读为已完成 | 高 | 在 roadmap 和任务包中显式写“本任务只做计划” |
| 旧 0.5 immediate next 与 post-0050 状态冲突 | 中 | 更新 0.5.4，把 MI-NEXT-02 移出待执行 |
| 外部资料泛泛引用 | 中 | 只引用基础设施官方/一手资料 URL |
| 任务树过大不可执行 | 中 | 拆成 MI-NEXT-03 到 MI-NEXT-10 |

# Assumptions and Falsification

- 假设：post-0050 下一步应该优先 durable runtime，而不是先新增术数功能。
- 证伪方式：若生产接入必须先交付 SDK/portal 或某个外部平台权限已就绪，则执行顺序可调整，但不能跳过 evidence/live gate。
- 调试模式: Optional

# Critical Ambiguities

- 外部监控、SIEM、OIDC 具体供应商未定：路线图只定义能力和证据，不绑定供应商。
- durable runtime 是否引入 Temporal 等成熟平台未定：MI-NEXT-03 需要先做 external backend decision。
- SDK 是正式发布包还是 installable examples 未定：MI-NEXT-09 负责定界。

# Debug Evidence Contract

本任务是规划任务，调试为 Optional。若 validator 失败，必须记录失败字段、修复方式和复跑结果。

# Task Package Context Map

- TP-01.01：读取路线图、任务索引、0050 状态和未提交 diff。
- TP-02.01：调研并归纳外部 infra 同构资料。
- TP-03.01：更新主路线图 `0.6`。
- TP-03.02：新建 0051 任务文档并更新任务索引。
- TP-04.01：运行任务文档、任务树和 diff 校验。

# Source Of Truth

- 计划真相源：`docs/reference-materials/roadmap/测算基础设施100%实现计划.md`
- 任务索引：`governance/tasks/INDEX.md`
- release gate：`contracts/fate/delivery/release-gate.json`
- capability/provider 资源：`contracts/fate/capabilities/registry.json`、`contracts/fate/providers/registry.json`
