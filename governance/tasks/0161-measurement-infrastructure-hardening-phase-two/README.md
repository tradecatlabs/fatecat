# Task Overview
- Task ID: `0161`
- Slug: `measurement-infrastructure-hardening-phase-two`
- Objective: `完成测算基础设施第二阶段加固：公开字段契约、冷启动性能、独立评测、成熟度语义、复杂度、异步指标、分发许可与仓库卫生`
- Status: `Done`

## In Scope
- 为公开 Markdown 建立明确字段允许清单，并保证机器证据继续保留在结构化结果中
- 在不减少 98 年和 1176 月完整输出的前提下优化八字冷启动计算热路径
- 建立与引擎自生成样本分离的独立准确性评测入口，人工专家结论继续标记待执行
- 统一 capability 可执行状态、生命周期和成熟度语义
- 拆分八字核心计算与报告生成中的超长职责，保持行为和公共契约不变
- 为异步报告任务补充排队、执行、结果大小和状态指标
- 在未知许可证资产继续受限的前提下形成可公开分发的客户端闭包
- 完成全量验证、审查、治理同步、语义提交和干净工作树

## Out of Scope
- 修改神煞、格局、用神或其他专业断语内容；该项等待人类命理专家处理
- 缩短完整报告的年份或月份范围
- 把本地自洽测试伪装成第三方准确性认证
- 把 bazi-1、sxwnl 或其他未知许可证资产声明为可公开分发
- 新增预测体系或改变 Web 视觉设计

## Task Package Tree
- ROOT
  ├─ TP-01 [leaf] [P0] 建立公开报告字段允许契约
  ├─ TP-02 [leaf] [P0] 优化完整八字冷启动热路径
  ├─ TP-03 [leaf] [P0] 建立独立准确性评测入口
  ├─ TP-04 [leaf] [P0] 统一 capability 生命周期语义
  ├─ TP-05 [leaf] [P1] 收敛核心与报告职责复杂度
  ├─ TP-06 [leaf] [P0] 补齐异步报告端到端指标
  ├─ TP-07 [leaf] [P0] 建立许可证安全的公开客户端闭包
  └─ TP-08 [leaf] [P0] 全量验证、审查与仓库卫生收口

## Requirement Alignment
- 目标: 完成测算基础设施第二阶段加固：公开字段契约、冷启动性能、独立评测、成熟度语义、复杂度、异步指标、分发许可与仓库卫生
- approved plan 顶层步骤数: 8
- 编译后节点总数: 8
- 编译后叶子节点数: 8
- 对齐项: 用户明确要求处理审查问题 2 到 9，第 1 项交由人类专家处理
- 对齐项: 此前明确要求保持每次完整计算 98 年和全部流月，不引入近期报告降级
- 对齐项: FateCat 的定位是面向 Agent 与应用开发者的测算基础设施
- 计划摘要: 先锁公开投影和 capability 语义，再优化确定性热路径并接入独立评测；随后拆分职责、补异步观测和公开分发闭包，最后执行隔离审查与仓库卫生收口。

## Task Package Overview
| Task Package ID | Parent | Depth | Priority | Type | Leaf | Depends On | Wave | Ready | Parallelizable | Objective |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TP-01 | ROOT | 1 | P0 | Contract | Yes | - | 1 | Yes | No | 明确公开 Markdown 与机器证据的字段边界，并建立多样本防泄露门禁 |
| TP-02 | ROOT | 1 | P0 | Performance | Yes | TP-01 | 2 | No | No | 消除逐月重复父级计算，保持完整输出和历法结果不变 |
| TP-03 | ROOT | 1 | P0 | Quality | Yes | TP-01 | 2 | No | Yes | 把外部 fixture、来源和容差与引擎自生成 golden 分离，并保留专家待审状态 |
| TP-04 | ROOT | 1 | P0 | Contract | Yes | TP-01 | 2 | No | Yes | 让可执行状态、生命周期和成熟度在 registry/schema/executor/API 中含义一致 |
| TP-05 | ROOT | 1 | P1 | Refactor | Yes | TP-02, TP-04 | 3 | No | No | 拆分超长计算与渲染职责，不改变结果和公共接口 |
| TP-06 | ROOT | 1 | P0 | Observability | Yes | TP-04 | 3 | No | Yes | 记录排队、执行、结果大小、终态和过期，不采集用户输入标签 |
| TP-07 | ROOT | 1 | P0 | Packaging | Yes | TP-04 | 3 | No | Yes | 公开包只含客户端、契约和文档，受限计算资产继续留在服务端并由门禁阻断 |
| TP-08 | ROOT | 1 | P0 | Verification | Yes | TP-03, TP-05, TP-06, TP-07 | 4 | No | No | 统一验证所有切片，更新治理真相源，形成语义提交并恢复干净工作树 |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
