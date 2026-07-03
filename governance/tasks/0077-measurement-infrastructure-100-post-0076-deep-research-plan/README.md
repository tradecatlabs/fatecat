# Task Overview
- Task ID: `0077`
- Slug: `measurement-infrastructure-100-post-0076-deep-research-plan`
- Objective: `基于当前 main worktree、0076 Postgres public webhook live smoke gate 已完成事实，以及 OpenAPI、AsyncAPI、CloudEvents、Kubernetes Controller、Terraform Provider、Temporal、OpenTelemetry、Google SRE、DORA、OWASP、NIST、SLSA、CycloneDX、CNCF 平台工程、Backstage、Stripe 等外部一手资料，刷新 FateCat 达到 100% 测算基础设施所需的完整实现计划、任务树、执行顺序、外部阻断项和不可伪造证据口径；本任务只落盘调研与计划，不把未外部验证的能力写成生产完成。`
- Status: `Done`

## In Scope
- 调研成熟基础设施领域的一手资料，并提炼 FateCat 的同构能力要求。
- 对照当前仓库已完成任务、contracts、roadmap 和交付证据，刷新 100% 缺口。
- 在主路线图追加 post-0076 最新实现计划。
- 将本任务目录回填为可复核的 planning-only 任务包。

## Out of Scope
- 不实现业务代码。
- 不接入真实外部 token、生产数据库、公网 webhook、IdP、SIEM、OTel backend、Vault/KMS。
- 不声明 100% 已完成，不把 dry-run、本地 smoke 或 contract gate 写成 live 证据。
- 不新增六爻、奇门、大六壬等新术数 production capability。

## Task Package Tree
```text
TP-01 复核仓库事实和任务现状
  TP-01.01 复核 Git/worktree 与 0076 closeout 事实
  TP-01.02 复核既有路线图、需求文档、contracts 和任务索引
TP-02 外部基础设施同构调研
  TP-02.01 汇总 API、事件、工作流、控制面、可观测、安全、供应链、平台工程一手资料
  TP-02.02 抽象 FateCat 100% 基础设施同构能力
TP-03 形成完整实现计划
  TP-03.01 定义 100% 完成门禁和失败判定
  TP-03.02 拆分 MI-100 资源域、任务树和执行顺序
  TP-03.03 区分本地可执行任务和外部连通验证待执行任务
TP-04 落盘和校验
  TP-04.01 更新主路线图最新章节
  TP-04.02 回填 0077 任务文档和 RESEARCH.md
  TP-04.03 运行任务文档校验和基础 grep 检查
```

## Requirement Alignment
- 用户要求：使用 `auto-tasks`，深度调研并制作实现 100% 基础设施所需的完整实现计划。
- 仓库定位：FateCat 是面向 Agent 与应用开发者的测算基础设施，核心是统一能力协议、可复现计算核心、证据化解释层和多端交付接口。
- 最新事实：0076 只证明 Postgres public webhook live smoke gate 已建立；真实公网 webhook live passed evidence、外部 Vault/KMS、heartbeat/polling worker、长期多副本运行、exactly-once、Bot live、OIDC、SIEM、OTel backend 仍未完成。

## Task Package Overview
| Node ID | Title | Status | Verify |
| --- | --- | --- | --- |
| TP-01.01 | Git/worktree 与 0076 事实复核 | Done | `git status --short --branch`、0076 `STATUS.md` |
| TP-01.02 | 既有计划和契约复核 | Done | `docs/reference-materials/roadmap/测算基础设施100%实现计划.md`、`contracts/fate/delivery/runtime-backends.json` |
| TP-02.01 | 外部一手资料调研 | Done | `RESEARCH.md` Source Matrix |
| TP-02.02 | 同构能力抽象 | Done | `RESEARCH.md` Synthesis |
| TP-03.01 | 完成门禁和失败判定 | Done | 主路线图 `0.10.5`、`0.10.6` |
| TP-03.02 | MI-100 任务树和顺序 | Done | 主路线图 `0.10.3`、`0.10.4` |
| TP-03.03 | 外部阻断项标注 | Done | `RESEARCH.md` External Validation Pending |
| TP-04.01 | 更新主路线图 | Done | `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` |
| TP-04.02 | 回填任务文档 | Done | 当前任务目录无占位符 |
| TP-04.03 | 校验 | Done | `validate_task_docs.py --phase decompose` |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
