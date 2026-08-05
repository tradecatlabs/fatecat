# Task Context

## Current Facts
- capability 真相源是 `contracts/fate/capabilities/registry.json`。
- 可执行入口集中在 `scripts/`，CI 只调用仓库脚本。
- 长期流程真相源是 `governance/processes/`，任务历史位于 `governance/tasks/`。
- 当前可执行 capability 为 `bazi`、`ziwei`、`almanac`、`meihua`。
- `liuyao`、`qimen`、`daliuren`、`fengshui_nine_stars`、`name_marriage` 为 L0 planned，调用必须拒绝。

## Target End State
- 所有稳定重复任务都能由自然语言命中唯一 SOP。
- SOP 只编排已有脚本、contract 和证据，不制造第二套工具链。
- 同类历史任务被收敛成稳定操作，而不是复制 165 个一次性实现记录。
- 文档结构和路由唯一性由回归测试机械保护。

## Real Constraints
- 真实 token、生产数据库、公网 webhook、外部 OTel/IdP/SIEM/Vault 和第三方专家权限不能在仓库内伪造。
- 报告、数据集和抓取产物可能包含个人数据或受版权约束内容，默认写 ignored runtime 目录。
- Git/HF/Telegram 等外部副作用必须显式授权、显式凭证、显式目标。

## Inertia Constraints
- 历史任务数量多，但大部分是实现切片或证据桥，不应一任务一 SOP 机械复制。
- `scripts/AGENTS.md` 很长，但它是工具职责说明，不替代面向操作者的 SOP。

## Kill List
- 第二套命令 wrapper。
- 一个 SOP 承担多个互不相同的目标。
- planned capability 的“伪生产”说明。
- 无输出路径、无失败语义、无清理和无运行记录的操作文档。

## Proof Point
- 索引覆盖所有 SOP，route key/alias 不重复。
- 每份 SOP 包含统一的 20 个必备章节。
- capability 状态与 registry 完全一致。
- 文档链接、治理 strict 和 Quick CI 通过。

## Falsifier
- 任一自然语言别名对应多个 SOP。
- 任一 planned capability 被写成可以生成生产结果。
- 任一 SOP 引用不存在的脚本或缺少必备章节。

# Repo Evidence
- `contracts/fate/capabilities/registry.json`：capability 生命周期和成熟度真相源。
- `scripts/AGENTS.md`：仓库级命令职责和调用边界。
- `governance/tasks/INDEX.md`：历史执行任务和成功证据入口。
- `governance/processes/文档治理规则.md`：长期流程文档治理边界。
- `tests/regression/test_sop_library.py`：SOP 结构、路由、状态和路径机械门禁。

# Constraints Matrix
| Constraint | Evidence | Effect |
| --- | --- | --- |
| 一任务一文档 | 用户明确要求 | 任一 SOP 不得承载第二个独立目标 |
| 复用成熟工具 | `scripts/` 与历史任务 | SOP 只编排已有入口，不新增 wrapper |
| planned fail closed | capability registry | 未投产能力只能描述接入和投产流程 |
| 外部验证不得伪造 | token、网络和账号不在仓库 | live 步骤必须标记外部执行条件 |
| 机器可路由 | 唯一 route key/alias | 重复路由直接阻断验收 |

# Change Boundary
- 允许：新增长期 SOP、目录职责文档、治理索引和专项回归测试。
- 禁止：修改测算算法、服务 API、生产配置、capability 状态或外部系统。
- 回滚：移除本任务新增文档和测试，并恢复治理索引引用。

# Risk Matrix
| Risk | Impact | Control |
| --- | --- | --- |
| 命令或路径漂移 | SOP 不可执行 | 路径存在性测试和治理 strict |
| 路由别名冲突 | 自然语言误路由 | 全局唯一性测试 |
| 状态过度声明 | planned 被误用 | registry 对照测试 |
| 外部副作用误触发 | 发布或数据风险 | 每份 SOP 明确前置授权和禁止事项 |

# Assumptions and Falsification
- 假设：长期重复任务可归并为稳定任务意图；若一个 SOP 出现两个独立成功标准，则拆分。
- 假设：`scripts/` 是成熟工具入口；若文档引用脚本不存在，测试必须失败。
- 假设：registry 是 capability 状态真相源；若状态不一致，以 registry 为准并阻断 SOP。

# Critical Ambiguities
- “全部任务”不是把全部历史 task package 复制为 SOP，而是覆盖稳定、可重复、可独立验收的操作意图。
- 外部 live 操作可以有 SOP，但仓库内文档不能证明其已经执行。
- 没有 canonical 生成器的节气 golden 重建任务必须标记 blocked，不得借用 archive 伪装成熟入口。

# Debug Evidence Contract
- 调试模式: Optional
- 若专项测试失败，记录首个失败断言、对应 SOP 路径、最小修复和复跑结果。
- 若治理校验失败，区分本任务新增问题与既有无关历史问题。

# Task Package Context Map
| Node | Inputs | Outputs |
| --- | --- | --- |
| TP-01 | registry、scripts、历史任务 | 任务分类和路由契约 |
| TP-02 | capability 分类 | capability SOP |
| TP-03 | 数据、评测和开发入口 | 数据与质量 SOP |
| TP-04 | 分发、生产和审计入口 | 交付与运行 SOP |
| TP-05 | TP-02/03/04 产物 | 测试、治理同步和审查证据 |
