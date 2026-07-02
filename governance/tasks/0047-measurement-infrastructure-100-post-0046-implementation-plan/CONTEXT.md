# Repo Evidence

- 当前目录：`/home/lenovo/.projects/fatecat`。
- 当前分支：`main...origin/main`。
- 当前提交：`2b3f4c8`。
- 当前 worktree：任务开始时 `git status --short --branch` 显示 clean。
- 0046 已完成 release clean、commit、push 和任务 closeout。
- Container workflow 对当前提交 `2b3f4c8` 已通过：`https://github.com/tradecatlabs/fatecat/actions/runs/28575853017`。
- Acceptance workflow 对 baseline 提交 `2b3f4c8` 已通过：`https://github.com/tradecatlabs/fatecat/actions/runs/28575852876`。
- 主路线图：`docs/reference-materials/roadmap/测算基础设施100%实现计划.md`。
- Release gate contract：`contracts/fate/delivery/release-gate.json`。

# External Research Sources

本任务使用的一手资料类型：

- OpenAPI Specification：API contract、schema、示例、版本。
- Stripe idempotent requests / webhooks：幂等和异步事件交付。
- Temporal durable execution / retry policies：长流程恢复和声明式重试。
- Kubernetes controllers：desired/current state reconciliation。
- Terraform providers：provider source、version、plugin lifecycle。
- Backstage system model：Component/API/Resource/System catalog。
- OpenTelemetry signals：traces、metrics、logs。
- Google SRE SLO：SLO、SLI、error budget。
- DORA Four Keys：交付效能指标。
- SLSA / CycloneDX：provenance、attestation、SBOM。
- OWASP API Security Top 10 / NIST SSDF：API 安全、供应链和安全开发。
- CloudEvents：事件 envelope 标准化。

# Constraints Matrix

| 约束 | 处理 |
| --- | --- |
| 用户要求深度调研并制作完整实现计划 | 刷新主路线图和任务包 |
| 当前任务不做业务实现 | 不改源码、不引入新脚本、不改 API 行为 |
| 不能伪造生产证据 | Acceptance 使用真实 GitHub Actions 成功证据；Bot、registry、OIDC/SIEM/monitoring 等外部项保持 pending |
| 已有 0009-0046 任务链 | 复用现有证据，不重新发明路线图 |
| 任务编号会继续增长 | 路线图使用 `MI-NEXT-*` 表达未来切片，不绑定尚未创建的目录编号 |

# Change Boundary

允许修改：

- `governance/tasks/0047-measurement-infrastructure-100-post-0046-implementation-plan/*`
- `governance/tasks/INDEX.md`
- `docs/reference-materials/roadmap/测算基础设施100%实现计划.md`

禁止修改：

- 业务源码
- provider 计算逻辑
- API 行为
- Git 历史或远端状态

# Risk Matrix

| 风险 | 等级 | 控制 |
| --- | --- | --- |
| 把计划写成已完成 | 高 | 所有外部项显式标注 pending 或外部验证待执行 |
| 把 remote Acceptance 状态写错 | 高 | 只记录真实 run URL、commit 和 conclusion |
| 未来任务编号漂移 | 中 | 使用 `MI-NEXT-*` 作为逻辑任务树 |
| 计划重复已有 0045 | 中 | 本轮只做 post-0046 状态刷新 |
| 外部资料不是一手来源 | 中 | 优先官方规范、官方文档和标准组织 |

# Assumptions and Falsification

- 假设：FateCat 的最高定位是测算基础设施，而非单一排盘工具或内容站。
- 假设：100% 的定义是公开生产基础设施闭环，不是本地 baseline。
- 可证伪条件：如果用户把 100% 定义改为“本地可审计即可”，则 Bot live、OIDC/SIEM、registry attestation 可降级为可选。
- 可证伪条件：如果生产环境不提供真实 token、Bot、registry、OIDC、SIEM 或监控权限，则相关任务不能完成，只能保留外部连通验证待执行。
- 调试模式: Optional

# Critical Ambiguities

- 真实 `FATE_BOT_TOKEN` 是否可用：当前未知。
- registry、签名、attestation 使用 GHCR、Docker Hub 还是其他 registry：当前未定。
- OIDC/IdP、SIEM、监控平台具体选型：当前未定。
- 第三方审计是否要求法律版权意见：当前未定。

# Debug Evidence Contract

Not Required。本任务是规划和文档刷新，不处理具体 bug。

# Task Package Context Map

- TP-01.01：当前仓库与远端 CI 事实复核。
- TP-02.01：外部基础设施资料同构调研。
- TP-03.01：主路线图 post-0046 刷新。
- TP-04.01：校验和 closeout。
