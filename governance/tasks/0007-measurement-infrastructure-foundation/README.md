# Task Overview
- Task ID: `0007`
- Slug: `measurement-infrastructure-foundation`
- Objective: `把 FateCat 从命理工具集合升级为面向 Agent 与应用开发者的测算基础设施基线：统一能力协议、可复现计算核心、证据化解释层、多端交付接口、能力成熟度和生产门禁。`
- Status: `Done`

## In Scope
- 提交当前“测算基础设施”定位基线。
- 补充测算基础设施路线图和文档治理规则。
- 升级 capability registry，使其表达成熟度、provider、engineVersion、evidencePolicy 和 testGate。
- 让生产 capability 通过统一 CapabilityExecutor 执行，planned 能力继续拒绝执行。
- 建立 bazi / ziwei 作为生产 capability 样板的协议字段和回归断言。
- 补齐基础设施 API 别名和 metadata 入口，保持兼容旧 `/api/v1/*` 路径。

## Out of Scope
- 不在本任务内新增六爻、奇门、大六壬等新生产能力。
- 不把非八字体系混入默认综合八字报告。
- 不承诺真实生产域名、真实 token、Bot live smoke 已完成；这些仍属于外部连通验证。
- 不改写 vendor 第三方源码。
- 不重做完整 UI 视觉设计。

## Task Package Tree
- TP-01 定位基线
  - TP-01.01 提交 README / SKILL / AGENTS / branding 口径更新
  - TP-01.02 补 `docs/reference-materials/roadmap/测算基础设施路线图.md`
  - TP-01.03 补 `governance/processes/文档治理规则.md`
- TP-02 协议基线
  - TP-02.01 registry 增加 maturity、engineVersion、evidencePolicy、testGate
  - TP-02.02 schema 和协议测试覆盖新增字段
- TP-03 执行器基线
  - TP-03.01 executor 使用 provider registry 而不是硬编码 capability 分支
  - TP-03.02 planned / experimental 能力继续明确拒绝执行
- TP-04 八字/紫微标杆
  - TP-04.01 bazi/ziwei 标记 L4 production candidate 模板字段
  - TP-04.02 API 返回成熟度、测试门禁和 evidence policy
- TP-05 生产基础设施
  - TP-05.01 补 `/capabilities`、`/capabilities/{id}/calculate`、`/reports`、`/metadata` 兼容入口
  - TP-05.02 API contract tests 覆盖新入口
  - TP-05.03 quick CI、governance strict、Git diff hygiene

## Requirement Alignment
- 用户明确要求按“定位基线 -> 协议基线 -> 执行器基线 -> 八字/紫微标杆 -> 生产基础设施”顺序开始实现。
- 当前已有定位文案更新和 quick CI 通过证据；本任务把这些纳入版本基线并继续做协议与 API 落地。
- 核心判断是“协议统一、计算可复现、证据可审计、输出可交付、能力可插拔、质量可验证”，不是继续堆功能模块。

## Task Package Overview
| Task | Status | Evidence |
| --- | --- | --- |
| TP-01 | Done | `ee36710` 已提交定位基线；路线图和治理规则补齐。 |
| TP-02 | Done | registry/schema/tests 已支持 maturity、engineVersion、evidencePolicy、testGate。 |
| TP-03 | Done | executor 已按 `engine.provider` 路由，planned 能力继续拒绝执行。 |
| TP-04 | Done | bazi/ziwei 已作为 L4 样板暴露成熟度、engine 和门禁字段。 |
| TP-05 | Done | 已补 `/capabilities`、`/capabilities/{id}/calculate`、`/reports`、`/metadata`，quick CI 通过。 |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
