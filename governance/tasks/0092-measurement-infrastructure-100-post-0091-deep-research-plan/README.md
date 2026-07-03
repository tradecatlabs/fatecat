# Task Overview
- Task ID: `0092`
- Slug: `measurement-infrastructure-100-post-0091-deep-research-plan`
- Objective: `基于当前 main worktree、0091 retention cleanup baseline 已完成事实，以及 OpenAPI 3.2、AsyncAPI 3.1、CloudEvents、Kubernetes Controller、Terraform Provider、Temporal、OpenTelemetry、Google SRE、DORA、OWASP API Security、NIST SSDF、SLSA 1.2、CycloneDX、GitHub artifact attestations、CNCF 平台工程、Backstage、Stripe 等外部一手资料，刷新 FateCat 达到 100% 测算基础设施所需的完整实现计划、任务树、执行顺序、外部阻断项和不可伪造证据口径；本任务只落盘调研与计划，不把未外部验证的能力写成生产完成。`
- Status: `Done`

## In Scope
- 调研成熟基础设施领域的一手资料，并提炼 FateCat 的同构能力要求。
- 对照 0091 后当前仓库事实、contracts、task index、release proof、audit bundle 和 roadmap，刷新 100% 缺口。
- 在主路线图追加 Post-0091 最新实现计划，明确本地可执行任务、外部连通验证待执行任务和失败判定。
- 将本任务目录回填为可复核的 planning-only 任务包。

## Out of Scope
- 不实现业务代码。
- 不接入真实外部 token、生产数据库、公网 webhook、IdP、SIEM、OTel backend、Vault/KMS 或生产多副本环境。
- 不声明 100% 已完成，不把 dry-run、本地 smoke、allow-missing blocked summary 或 contract gate 写成 live 证据。
- 不新增六爻、奇门、大六壬、塔罗等新术数 production capability。

## Task Package Tree
```text
TP-01 复核仓库事实和 Post-0091 现状
  TP-01.01 复核 Git/worktree、HEAD、远端 CI 与 0091 closeout 事实
  TP-01.02 复核既有路线图、contracts、audit/release proof 和任务索引
TP-02 外部基础设施同构调研
  TP-02.01 汇总 API、事件、工作流、控制面、可观测、安全、供应链、平台工程一手资料
  TP-02.02 抽象 FateCat 100% 基础设施资源域
TP-03 形成完整实现计划
  TP-03.01 定义 100% 完成门禁和失败判定
  TP-03.02 拆分 Post-0091 资源域、任务队列和执行顺序
  TP-03.03 区分本地可执行任务和外部连通验证待执行任务
TP-04 落盘和校验
  TP-04.01 更新主路线图 Post-0091 章节
  TP-04.02 回填 0092 任务文档和 RESEARCH.md
  TP-04.03 运行任务文档校验和一致性检查
```

## Requirement Alignment
- 用户要求：使用 `auto-tasks`，深度调研并制作实现 100% 测算基础设施所需的完整实现计划。
- 仓库定位：FateCat 是面向 Agent 与应用开发者的测算基础设施，核心是统一能力协议、可复现计算核心、证据化解释层和多端交付接口。
- 最新事实：0091 已完成本地 SQLite records/report jobs retention cleanup baseline 并推送；当前 `44cbedd` 的 Acceptance 和 Container 远端 workflow 均为 success。
- 边界：真实 Bot live、OIDC/IdP、SIEM、OTel backend、Vault/KMS、公网 webhook passed、生产多副本、生产 scheduler 和 Postgres production cleanup 仍属外部连通验证待执行。

## Task Package Overview
| Node ID | Title | Status | Verify |
| --- | --- | --- | --- |
| TP-01.01 | Git/worktree、HEAD 和远端 CI 复核 | Done | `git status --short --branch`、`git log -1 --oneline`、`gh run list --limit 5` |
| TP-01.02 | 既有计划和契约复核 | Done | 主路线图、`contracts/fate/audit/current-bundle.json`、`contracts/fate/audit/handoff.json`、任务索引 |
| TP-02.01 | 外部一手资料调研 | Done | `RESEARCH.md` Source Matrix |
| TP-02.02 | 同构能力抽象 | Done | `RESEARCH.md` Synthesis |
| TP-03.01 | 完成门禁和失败判定 | Done | 主路线图 `0.11.5`、`0.11.6` |
| TP-03.02 | 任务队列和执行顺序 | Done | 主路线图 `0.11.3`、`0.11.4` |
| TP-03.03 | 外部阻断项标注 | Done | `RESEARCH.md` External Validation Pending |
| TP-04.01 | 更新主路线图 | Done | `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` |
| TP-04.02 | 回填任务文档 | Done | 当前任务目录无占位符，新增 `RESEARCH.md` |
| TP-04.03 | 校验 | Done | `validate_task_docs.py --phase decompose`、占位符检查 |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
