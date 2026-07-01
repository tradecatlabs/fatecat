# Task Overview
- Task ID: `0006`
- Slug: `business-logic-audit-remediation`
- Objective: `修复 REVIEW-0001 业务代码业务模型与业务逻辑审计发现的阻塞级和警告级问题，恢复 fate-core 领域边界、业务选项语义一致性、入口真相源一致性、坐标边界校验和治理汇报准确性。`
- Status: `Done`

## In Scope
- 以 governance/evidence/reviews/REVIEW-0001-业务代码业务模型与业务逻辑审计.md 的 F-001 到 F-005 为修复真相源。
- 修复 fate-core 反向依赖 fatecat-delivery 的领域边界问题。
- 修复 BaziOptions 中未实现选项静默忽略和响应回显不一致问题。
- 收敛 Web/API/Bot 的业务计算入口，减少 legacy raw calculator 旁路。
- 补充 Web/Bot 直接坐标输入范围校验。
- 把治理资产变更、索引刷新和校验证据整理成可提交、可审计状态。

## Out of Scope
- 不在本任务内宣称八字专业体系 100%。
- 不重做完整命理规则体系，不扩展高级格局、合化、用神或岁运专题。
- 不引入 Redis/Celery/Kubernetes 或高并发公共服务架构。
- 不改变 /web 的已批准黄金三块布局和零美化语义界面规则。
- 不删除已公开 API、Bot、Web 入口，除非另有兼容账本和显式迁移 gate。

## Task Package Tree
- ROOT
  ├─ TP-01 [branch] [P0] PRECHECK：冻结审计基线与治理资产边界
  │  ├─ TP-01.01 [leaf] [P0] 盘点当前治理资产 dirty diff
  │  ├─ TP-01.02 [leaf] [P0] 复现 REVIEW-0001 关键证据
  │  └─ TP-01.03 [leaf] [P0] 建立当前测试基线
  ├─ TP-02 [branch] [P0] F-001：修复 fate-core 反向依赖 delivery
  │  ├─ TP-02.01 [leaf] [P0] 绘制 integration ownership map
  │  ├─ TP-02.02 [leaf] [P0] 迁移核心 adapter/provider
  │  └─ TP-02.03 [leaf] [P0] 新增领域边界防回潮测试
  ├─ TP-03 [branch] [P0] F-002/F-003：修复业务选项语义和响应回显
  │  ├─ TP-03.01 [leaf] [P0] 先补业务选项失败测试
  │  ├─ TP-03.02 [leaf] [P0] 未实现业务选项显式拒绝
  │  ├─ TP-03.03 [leaf] [P0] 修复 useTrueSolarTime 响应回显
  │  └─ TP-03.04 [leaf] [P1] 记录 raw options 与 normalized options
  ├─ TP-04 [branch] [P1] F-004：统一 Web/API/Bot 业务真相源
  │  ├─ TP-04.01 [leaf] [P1] 绘制 Web/API/Bot 当前业务流
  │  ├─ TP-04.02 [leaf] [P1] 建立 canonical calculation service
  │  └─ TP-04.03 [leaf] [P1] 入口一致性回归
  ├─ TP-05 [branch] [P1] F-005：补坐标输入边界校验
  │  ├─ TP-05.01 [leaf] [P1] 补 location 坐标边界测试
  │  └─ TP-05.02 [leaf] [P1] 实现坐标范围校验
  └─ TP-06 [branch] [P0] REVIEW/CLOSEOUT：回归、审查和治理收口
     ├─ TP-06.01 [leaf] [P0] 运行本地回归门禁
     ├─ TP-06.02 [leaf] [P0] 更新 REVIEW-0001 修复状态
     └─ TP-06.03 [leaf] [P0] 提交前交付包

## Requirement Alignment
- 目标: 修复 REVIEW-0001 业务代码业务模型与业务逻辑审计发现的阻塞级和警告级问题，恢复 fate-core 领域边界、业务选项语义一致性、入口真相源一致性、坐标边界校验和治理汇报准确性。
- approved plan 顶层步骤数: 6
- 编译后节点总数: 24
- 编译后叶子节点数: 18
- 对齐项: 用户要求使用 auto-tasks 设计修复计划。
- 对齐项: 上一轮事实核查确认 REVIEW-0001 审计文档真实存在，治理校验通过，但当前治理变更未提交且汇报漏报了额外标准和索引变更。
- 对齐项: 本计划只设计修复 REVIEW-0001 的业务代码/业务模型/业务逻辑问题和治理资产卫生，不扩大到八字专业体系 100% 路线图。
- 计划摘要: 按 REVIEW-0001 的 BLOCK/WARN 顺序修复：先冻结治理与基线，再断开 fate-core 到 delivery 的反向依赖，然后修业务选项语义，统一入口真相源，补坐标校验，最后做 release gate 和审计 closeout。

## Task Package Overview
| Task Package ID | Parent | Depth | Priority | Type | Leaf | Depends On | Wave | Ready | Parallelizable | Objective |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TP-01 | ROOT | 1 | P0 | package | No | - | - | No | No | 确认当前未提交治理资产、REVIEW-0001 finding、现有测试基线和执行边界，避免修复过程混入无关变更。 |
| TP-01.01 | TP-01 | 2 | P0 | action | Yes | - | 1 | Yes | Yes | 列出当前 governance 变更、未跟踪文件和它们是否属于本任务前置资产。 |
| TP-01.02 | TP-01 | 2 | P0 | action | Yes | - | 1 | Yes | Yes | 用 rg 和最小测试复现 F-001 到 F-005 的当前状态，建立修复前证据。 |
| TP-01.03 | TP-01 | 2 | P0 | action | Yes | TP-01.01, TP-01.02 | 2 | No | No | 运行目标回归，确认开始修复前哪些测试已经通过，哪些测试需要先补失败用例。 |
| TP-02 | ROOT | 1 | P0 | package | No | TP-01.03 | - | No | No | 迁移被领域内核使用的 delivery integration 到 fate-core adapter/provider，删除 TELEGRAM_SRC_DIR/sys.path 反向依赖。 |
| TP-02.01 | TP-02 | 2 | P0 | action | Yes | TP-01.03 | 3 | No | No | 列出 bazi_calculator.py 和 ziwei_iztro.py 通过 delivery src 动态导入的模块、调用点和迁移目标。 |
| TP-02.02 | TP-02 | 2 | P0 | action | Yes | TP-01.03, TP-02.01 | 4 | No | No | 把核心计算需要的旧 integration 移入 fate_core.adapters/providers 或 reference adapter，delivery 只保留交付入口。 |
| TP-02.03 | TP-02 | 2 | P0 | action | Yes | TP-01.03, TP-02.02 | 5 | No | No | 新增结构测试，禁止 fate-core 源码再次引用 delivery 路径或 TELEGRAM_SRC_DIR。 |
| TP-03 | ROOT | 1 | P0 | package | No | TP-01.03 | - | No | No | 建立 canonical options，未实现语义显式 422，useTrueSolarTime 回显与真实计算一致。 |
| TP-03.01 | TP-03 | 2 | P0 | action | Yes | TP-01.03 | 3 | No | No | 为 calendarType=lunar、midnightMode=late、daylightSaving 非默认、useTrueSolarTime=false 写失败用例。 |
| TP-03.02 | TP-03 | 2 | P0 | action | Yes | TP-01.03, TP-03.01 | 4 | No | No | 对未支持的 lunar/DST/late-midnight 语义返回 422，避免保存成已应用状态。 |
| TP-03.03 | TP-03 | 2 | P0 | action | Yes | TP-01.03, TP-03.01 | 4 | No | Yes | 让 input.options.useTrueSolarTime 与 inputTrace.useTrueSolarTime 和真实计算配置一致。 |
| TP-03.04 | TP-03 | 2 | P1 | action | Yes | TP-01.03, TP-03.02, TP-03.03 | 5 | No | No | 持久化只保存实际参与计算的 normalized options，同时保留 raw input 供审计。 |
| TP-04 | ROOT | 1 | P1 | package | No | TP-02.01, TP-02.02, TP-02.03, TP-03.01, TP-03.02, TP-03.03, TP-03.04 | - | No | No | 将 Web/API/Bot 的八字/紫微业务计算收敛到同一 canonical calculation usecase，delivery 仅负责适配和交付。 |
| TP-04.01 | TP-04 | 2 | P1 | action | Yes | TP-02.01, TP-02.02, TP-02.03, TP-03.01, TP-03.02, TP-03.03, TP-03.04 | 6 | No | Yes | 列出 Web、API markdown、API pure-analysis、Bot report 的当前计算入口、输出字段和差异。 |
| TP-04.02 | TP-04 | 2 | P1 | action | Yes | TP-02.01, TP-02.02, TP-02.03, TP-03.01, TP-03.02, TP-03.03, TP-03.04, TP-04.01 | 7 | No | No | 优先复用 CapabilityExecutor/calculate_pure_analysis，形成 Web/API/Bot 可共享的薄服务层。 |
| TP-04.03 | TP-04 | 2 | P1 | action | Yes | TP-02.01, TP-02.02, TP-02.03, TP-03.01, TP-03.02, TP-03.03, TP-03.04, TP-04.02 | 8 | No | No | 同一输入经 Web/API/Bot 或其服务层生成的 canonical calculation 字段一致。 |
| TP-05 | ROOT | 1 | P1 | package | No | TP-01.03 | - | No | Yes | 让 Web/Bot 直接 lng,lat 输入复用经纬度范围验证，无效坐标返回明确错误。 |
| TP-05.01 | TP-05 | 2 | P1 | action | Yes | TP-01.03 | 3 | No | No | 覆盖 999,999、181,0、0,91、-181,0、0,-91 和合法边界坐标。 |
| TP-05.02 | TP-05 | 2 | P1 | action | Yes | TP-01.03, TP-05.01 | 4 | No | No | 在 location.get 或共享 validator 中校验经纬度范围，并让 Web/Bot 得到清晰错误。 |
| TP-06 | ROOT | 1 | P0 | package | No | TP-02.01, TP-02.02, TP-02.03, TP-03.01, TP-03.02, TP-03.03, TP-03.04, TP-04.01, TP-04.02, TP-04.03, TP-05.01, TP-05.02 | - | No | No | 运行完整本地门禁，更新 REVIEW-0001 修复状态，整理治理资产和提交边界。 |
| TP-06.01 | TP-06 | 2 | P0 | action | Yes | TP-02.01, TP-02.02, TP-02.03, TP-03.01, TP-03.02, TP-03.03, TP-03.04, TP-04.01, TP-04.02, TP-04.03, TP-05.01, TP-05.02 | 9 | No | No | 运行 focused regression、ruff、format、mypy、local-ci quick 和治理 strict。 |
| TP-06.02 | TP-06 | 2 | P0 | action | Yes | TP-02.01, TP-02.02, TP-02.03, TP-03.01, TP-03.02, TP-03.03, TP-03.04, TP-04.01, TP-04.02, TP-04.03, TP-05.01, TP-05.02, TP-06.01 | 10 | No | No | 把 F-001 到 F-005 的状态、证据命令、剩余 WARN 和 owner 写回审计记录或 follow-up review。 |
| TP-06.03 | TP-06 | 2 | P0 | action | Yes | TP-02.01, TP-02.02, TP-02.03, TP-03.01, TP-03.02, TP-03.03, TP-03.04, TP-04.01, TP-04.02, TP-04.03, TP-05.01, TP-05.02, TP-06.02 | 11 | No | No | 整理 git diff、任务 closeout、提交说明和回滚路径。 |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
