# Task Overview
- Task ID: `0152`
- Slug: `measurement-infrastructure-core-quality-evidence-bundle-rehearsal`
- Objective: `基于当前 0151 readiness audit 和基础设施同构调研，落地 core_quality_human_review_bundle 提交前演练模板、hash 计算说明、no-leak checklist 和 100% 基础设施后续计划刷新；不填真实专家或 benchmark 内容，不改变 core quality gate 结论。`
- Status: `In Progress`

## In Scope
- 读取当前 worktree、0151 readiness audit、core-quality-human-review-gate 契约、professional rubric 和 local-ci 接线。
- 基于 OpenAPI、AsyncAPI、CloudEvents、Kubernetes controller、Backstage catalog、Temporal durable execution、OpenTelemetry、Google SRE、OWASP/NIST/SLSA/CycloneDX/GitHub artifact attestations 等一手资料刷新 100% 基础设施执行计划。
- 新增 core_quality_human_review_bundle 的提交前演练模板、hash 计算说明、no-leak checklist 和 operator checklist。
- 保证模板不会被 core-quality-human-review-gate 误判为真实 accepted evidence。
- 补齐回归测试、local-ci 接线、AGENTS/roadmap/任务文档同步。

## Out of Scope
- 不填写真实专家身份、真实命例、外部 benchmark 逐题内容、答案、完整报告正文或真实用户资料。
- 不执行真实专家评审、外部 benchmark、生产 API/HF/Bot/webhook、OIDC/SIEM/OTel/Vault/KMS 或第三方审计。
- 不改变八字、紫微 provider 算法，不新增术数 capability。
- 不把模板、dry-run、operator checklist 或 local-ci 结果写成 100% 基础设施完成。

## Task Package Tree
- ROOT
  ├─ TP-01 [branch] [P0] 资料与仓库事实对齐
  │  ├─ TP-01.01 [leaf] [P0] 盘点当前仓库证据链
  │  └─ TP-01.02 [leaf] [P0] 基础设施同构资料映射
  ├─ TP-02 [branch] [P0] Core quality bundle 模板契约设计
  │  ├─ TP-02.01 [leaf] [P0] 新增模板契约
  │  └─ TP-02.02 [leaf] [P0] 设计模板生成器输出
  ├─ TP-03 [branch] [P0] 实现、测试与 local-ci 接线
  │  ├─ TP-03.01 [leaf] [P0] 新增回归测试
  │  └─ TP-03.02 [leaf] [P0] 接入 local-ci artifact
  ├─ TP-04 [branch] [P0] 文档和路线图同步
  │  ├─ TP-04.01 [leaf] [P0] 刷新 100% 路线图
  │  └─ TP-04.02 [leaf] [P0] 同步 AGENTS 与任务文档
  └─ TP-05 [branch] [P0] 验证、审查与版本控制
     ├─ TP-05.01 [leaf] [P0] 执行本地验证
     └─ TP-05.02 [leaf] [P0] 提交推送并观察远端 Acceptance

## Requirement Alignment
- 目标: 基于当前 0151 readiness audit 和基础设施同构调研，落地 core_quality_human_review_bundle 提交前演练模板、hash 计算说明、no-leak checklist 和 100% 基础设施后续计划刷新；不填真实专家或 benchmark 内容，不改变 core quality gate 结论。
- approved plan 顶层步骤数: 5
- 编译后节点总数: 15
- 编译后叶子节点数: 10
- 对齐项: 用户要求使用 auto-tasks 深度调研并制作 100% 基础设施完整实现计划。
- 对齐项: 当前路线图 6.40.5 已列出 0152：Core quality evidence bundle rehearsal。
- 对齐项: 本任务把 planning refresh 和下一步可执行本地切片合并：既刷新后续计划，又提供真实外部人审前的模板/检查清单。
- 计划摘要: 把 0152 做成低风险本地可执行切片：先对齐仓库事实和外部基础设施模式，再新增 core quality 人审 evidence bundle 模板，最后刷新路线图和验证链路。模板只降低人工提交摩擦，不改变 gate blocked 结论。

## Task Package Overview
| Task Package ID | Parent | Depth | Priority | Type | Leaf | Depends On | Wave | Ready | Parallelizable | Objective |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TP-01 | ROOT | 1 | P0 | package | No | - | - | No | No | 读取 0151、core quality gate、professional rubric、local-ci 和官方基础设施资料，形成 0152 的事实边界。 |
| TP-01.01 | TP-01 | 2 | P0 | action | Yes | - | 1 | Yes | No | 确认 HEAD、0151 readiness audit、core-quality-human-review-gate、rubric 和 local-ci 接线。 |
| TP-01.02 | TP-01 | 2 | P0 | action | Yes | - | 1 | Yes | Yes | 把官方 infra 范式映射到 FateCat 100% 剩余证据链。 |
| TP-02 | ROOT | 1 | P0 | package | No | TP-01.01, TP-01.02 | - | No | No | 定义 template-only 输出、artifact hash 指南、rubric checklist、benchmark aggregate skeleton、no-leak checklist 和 gate expectation。 |
| TP-02.01 | TP-02 | 2 | P0 | action | Yes | TP-01.01, TP-01.02 | 2 | No | Yes | 新增 machine-readable template contract，明确 non-claim 和 forbidden leak policy。 |
| TP-02.02 | TP-02 | 2 | P0 | action | Yes | TP-01.01, TP-01.02 | 2 | No | Yes | 生成 JSON/Markdown 模板，包含 operator checklist、hash commands、no-leak commands 和 gate run command。 |
| TP-03 | ROOT | 1 | P0 | package | No | TP-02.01, TP-02.02 | - | No | No | 落地模板生成器、回归测试和 quick local-ci artifact，证明模板不会解除 blocked gate。 |
| TP-03.01 | TP-03 | 2 | P0 | action | Yes | TP-02.01, TP-02.02 | 3 | No | Yes | 覆盖模板字段、敏感信息防护、CLI 输出和 gate 拒绝模板。 |
| TP-03.02 | TP-03 | 2 | P0 | action | Yes | TP-02.01, TP-02.02, TP-03.01 | 4 | No | No | 让 quick local-ci 生成模板 JSON/Markdown 并继续运行 core quality gate blocked-as-expected。 |
| TP-04 | ROOT | 1 | P0 | package | No | TP-03.01, TP-03.02 | - | No | No | 刷新 100% 基础设施实现计划、AGENTS 目录说明和 0152 任务文档。 |
| TP-04.01 | TP-04 | 2 | P0 | action | Yes | TP-03.01, TP-03.02 | 5 | No | Yes | 新增 Post-0151/0152 实现计划，列出下一批任务和不可伪造证据口径。 |
| TP-04.02 | TP-04 | 2 | P0 | action | Yes | TP-03.01, TP-03.02 | 5 | No | Yes | 更新相关 AGENTS 和 0152 TODO/STATUS/ACCEPTANCE。 |
| TP-05 | ROOT | 1 | P0 | package | No | TP-04.01, TP-04.02 | - | No | No | 执行 targeted tests、lint、local-ci、diff check、提交推送并观察远端 CI。 |
| TP-05.01 | TP-05 | 2 | P0 | action | Yes | TP-04.01, TP-04.02 | 6 | No | No | 运行任务文档校验、测试、lint、format、local-ci 和 diff check。 |
| TP-05.02 | TP-05 | 2 | P0 | action | Yes | TP-04.01, TP-04.02, TP-05.01 | 7 | No | No | 完成版本控制交付并记录当前 commit 的远端 CI 证据。 |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
