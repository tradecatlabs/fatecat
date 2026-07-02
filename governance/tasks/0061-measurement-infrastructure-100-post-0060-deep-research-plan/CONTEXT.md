# Repo Evidence

| Evidence | Current Fact |
| --- | --- |
| `git status --short --branch` | `## main...origin/main`，0061 开始前工作树干净。 |
| `git log -5 --oneline --decorate` | 最新提交为 `6b3d5cd test: wait for webhook delivery event`，远端 `origin/main` 同步。 |
| `governance/tasks/INDEX.md` | 0060 已 Done；0061 已由 `materialize_task_docs.py` 初始化为 In Progress。 |
| `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` | 已有 post-0060 计划，但缺一份面向后续执行的更细资源成熟度矩阵和任务树。 |
| `contracts/fate/*` | 已存在 capabilities、delivery、evaluations、observability、security、data-supply-chain 等资源契约。 |

# Constraints Matrix

| Constraint | Impact |
| --- | --- |
| 当前任务只做计划 | 不修改业务代码，不新增运行逻辑。 |
| 用户要求深度调研 | 计划必须引用成熟基础设施范式，不能只写主观路线。 |
| 不伪造外部证据 | 外部 Bot、webhook、OIDC、SIEM、OTel backend、Vault/KMS、审计均只能写待验证或后续任务。 |
| 当前分支不切换 | 所有改动保留在 `main` 当前 worktree。 |
| 任务包可校验 | 所有占位符必须清空，TODO/STATUS 与任务树一致。 |

# Change Boundary

允许修改：

- `governance/tasks/0061-measurement-infrastructure-100-post-0060-deep-research-plan/*`
- `governance/tasks/INDEX.md`
- `docs/reference-materials/roadmap/测算基础设施100%实现计划.md`

禁止修改：

- 业务代码、API 行为、数据库 schema、Web UI、Bot 逻辑。
- 真实 `.env`、secret、token、生产配置或运行态数据。
- 已完成任务目录的历史证据，除非只是引用。

# Risk Matrix

| Risk | Mitigation |
| --- | --- |
| 把计划写成已完成事实 | 所有缺口都写成后续任务或外部连通验证待执行。 |
| 100% 口径误解成预测准确率 | 明确 100% 是基础设施成熟度，不是命中率。 |
| 任务树过大导致无法执行 | 按 P0/P1/P2 和 0062 起候选切片排序。 |
| 忽略当前已有能力造成重复建设 | 先复核 0009-0060 事实，计划只补剩余缺口。 |
| 外部资料过时或二手转述 | 优先引用官方规格、官方文档和一手资料。 |

# Assumptions and Falsification

- Assumption: FateCat 成为基础设施的核心瓶颈是生产闭环、资源治理和审计证据，而不是新增更多术数功能。
- Falsifier: 如果 production path 仍可绕过 capability/provider/report/evidence/policy gate，则基础设施口径不成立。
- Assumption: 后续最快路径是先 durable runtime external backend，再事件契约、外部观测、安全平台和 developer platform。
- Falsifier: 如果外部生产发布必须先接入 OIDC/网关/平台约束，则 MI-NEXT 优先级需要按部署环境重排。
- Assumption: 0061 是规划任务，不需要跑完整 local-ci。
- Falsifier: 如果文档任务引入脚本、schema 或业务代码变更，则必须升级验证范围。

# Critical Ambiguities

- External backend 选型尚未执行：Postgres、Temporal、Redis Queue 的最终落地需单独任务决策和 smoke。
- 公网 webhook live 需要真实可访问接收端和回调日志；当前环境未提供。
- 外部 Vault/KMS、OIDC/IdP、SIEM、OTel backend 依赖真实账号和权限。
- 八字/紫微 corpus 扩容需要匿名样本、人审边界和资料授权复核。

# Debug Evidence Contract

- 调试模式: Optional
- 本任务是 planning/research，不修复运行时缺陷；如果 validator 或文档链接失败，记录到 `STATUS.md` 即可。

# Task Package Context Map

| Node | Context |
| --- | --- |
| TP-01.01 | `git status`、`git log`、roadmap、INDEX、0060 任务事实。 |
| TP-02.01 | OpenAPI、AsyncAPI、CloudEvents、Temporal、OpenTelemetry、Google SRE、OWASP、SLSA、NIST、Kubernetes、Terraform、Backstage。 |
| TP-02.02 | FateCat resource model：Capability、Provider、CalculationJob、Report、Evidence、Dataset、EvaluationRun、DeliverySurface、SecurityControl、ObservabilitySignal、ReleaseArtifact、AuditHandoff。 |
| TP-03.01 | `RESEARCH.md`。 |
| TP-03.02 | `docs/reference-materials/roadmap/测算基础设施100%实现计划.md`。 |
| TP-03.03 | 后续 0062+ 候选任务树和证据口径。 |
| TP-04.01 | README/CONTEXT/PLAN/ACCEPTANCE/TODO/STATUS/CHECKLIST。 |
| TP-04.02 | task validators、关键词检查、git 状态。 |
