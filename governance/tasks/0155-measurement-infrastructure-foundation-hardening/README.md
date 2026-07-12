# Task Overview
- Task ID: `0155`
- Slug: `measurement-infrastructure-foundation-hardening`
- Objective: `全面修复当前测算基础设施审查发现的本地可处理阻断项：线上渠道就绪隔离、可独立分发包、综合八字单一生产引擎、自动 CI 与发布证明、供应链/导出卫生、治理文档和性能基线；真实专家评审与外部生产凭证保持为不可伪造外部门禁。`
- Status: `In Progress`

## In Scope
- 可独立安装运行的 fatecat core wheel 与精简 skill 导出闭包
- 综合八字统一使用 capability 生产引擎并治理旧接口
- Telegram 渠道故障隔离、退避重试与可观测错误摘要
- PR/push quick CI 与当前提交发布证明入口
- vendor 只读卫生、导出体积和供应链许可门禁
- 治理必需文档、module context、任务状态和事实文档同步
- 八字性能基线与现有专业质量外部门禁接线

## Out of Scope
- 伪造真实专家命例评审、外部 benchmark、no-leak 签字或第三方审计结果
- 伪造生产 token、外部 Postgres、SIEM、OIDC、OTel、Bot live 或其他外部连通证据
- 新增黄历、六爻、梅花、奇门等业务体系
- 无行为证据支撑的大规模重写

## Task Package Tree
- ROOT
  ├─ TP-01 [leaf] [P0] 建立可独立分发闭包
  ├─ TP-02 [leaf] [P0] 统一综合八字生产引擎
  ├─ TP-03 [leaf] [P0] 隔离 Telegram 渠道就绪状态
  ├─ TP-04 [leaf] [P0] 补齐自动 CI 与发布证明
  ├─ TP-05 [leaf] [P1] 加固供应链与 vendor 卫生
  ├─ TP-06 [leaf] [P1] 恢复治理真相源
  └─ TP-07 [leaf] [P0] 性能、质量与交付收口

## Requirement Alignment
- 目标: 修复当前测算基础设施审查发现的本地可处理阻断项，使核心计算、分发包、交付面、CI、供应链和治理证据形成同一可验证闭环。
- approved plan 顶层步骤数: 7
- 编译后节点总数: 7
- 编译后叶子节点数: 7
- 对齐项: 用户要求先控制版本，再全面处理审查发现的问题
- 对齐项: 当前 main/acd17d7 与 origin/main 同步且工作树干净，作为修复基线
- 对齐项: FateCat 定位是面向 Agent 与应用开发者的测算基础设施
- 计划摘要: 先把可交付对象收敛为可独立运行的最小闭包，再统一计算真相源和渠道健康语义，随后补自动 CI、供应链与治理门禁，最后用性能和质量证据收口。

## Task Package Overview
| Task Package ID | Parent | Depth | Priority | Type | Leaf | Depends On | Wave | Ready | Parallelizable | Objective |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TP-01 | ROOT | 1 | P0 | Packaging | Yes | - | 1 | Yes | No | 让 core wheel 和 lite skill 在仓库外独立运行，并阻止运行态、嵌套导出和无关大资产进入发布包。 |
| TP-02 | ROOT | 1 | P0 | Architecture | Yes | TP-01 | 2 | No | No | 所有公开交付面通过 CapabilityExecutor 执行综合八字，旧接口只保留明确兼容契约。 |
| TP-03 | ROOT | 1 | P0 | Reliability | Yes | TP-02 | 3 | No | No | 核心 readiness 与渠道 readiness 分层，Telegram 使用有界指数退避并输出脱敏失败类型。 |
| TP-04 | ROOT | 1 | P0 | CI | Yes | TP-03 | 4 | No | No | quick gate 自动覆盖 PR/main push，重型容器发布保持受控并可生成当前提交证明。 |
| TP-05 | ROOT | 1 | P1 | Supply Chain | Yes | TP-04 | 5 | No | No | 阻止测试污染 reference repo，并让分发许可、revision 与分发允许状态可机械复核。 |
| TP-06 | ROOT | 1 | P1 | Governance | Yes | TP-05 | 6 | No | No | 补齐 review standard/module contexts，刷新过期事实文档并收敛任务索引。 |
| TP-07 | ROOT | 1 | P0 | Verification | Yes | TP-06 | 7 | No | No | 建立八字性能预算、执行完整门禁与审查，提交并推送所有已验证本地改动。 |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
