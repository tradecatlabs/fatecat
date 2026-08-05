# Task Overview
- Task ID: `0166`
- Slug: `sop-library-and-natural-language-routing`
- Objective: `基于当前 capability、仓库工具链和历史成功任务，建立一任务一文档、可由自然语言唯一定位、可机械校验的标准作业程序库`
- Status: `Done`

## Task Package Overview
| Field | Value |
| --- | --- |
| Owner | governance |
| Source of Truth | `governance/processes/sops/` |
| Route Contract | `governance/processes/sops/INDEX.md` |
| Validation | `tests/regression/test_sop_library.py` |
| External Side Effects | None |

## In Scope
- 盘点 production、validated、planned capability 和长期运维任务。
- 在 `governance/processes/sops/` 为每个独立任务建立单独 SOP。
- 建立自然语言路由总索引、目录职责文档和机械回归门禁。
- 明确成熟参数、固定路径、运行证据、外部依赖和未投产边界。

## Out of Scope
- 不改变业务算法、API、报告结构、部署配置或生产状态。
- 不把历史一次性任务逐条复制成 SOP。
- 不执行真实生产发布、外部凭证验证或计划 capability 实现。
- 不新增第二套命令入口或流程运行时。

## Task Package Tree
- ROOT
  - TP-01 [P0] 任务分类与唯一路由契约
  - TP-02 [P0] capability SOP
  - TP-03 [P0] 数据、评测与开发 SOP
  - TP-04 [P0] 分发、生产、发布与审计 SOP
  - TP-05 [P0] 机械校验、治理同步与审查

## Requirement Alignment
- 每个独立任务只对应一个 Markdown 文件。
- 每份 SOP 具备用户要求的全部固定章节。
- 生产状态只取自 tracked contract；planned 能力必须 fail closed。
- 工具、参数和路径只复用仓库现有入口与历史通过证据。
- 总索引用唯一 `route_key` 和不重复别名支持自然语言路由。

## Reading Order
1. `README.md`
2. `CONTEXT.md`
3. `PLAN.md`
4. `ACCEPTANCE.md`
5. `ACCEPTANCE_CHECKLIST.md`
6. `TODO.md`
7. `STATUS.md`
