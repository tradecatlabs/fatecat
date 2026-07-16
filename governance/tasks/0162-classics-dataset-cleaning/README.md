# Task Overview
- Task ID: `0162`
- Slug: `classics-dataset-cleaning`
- Objective: `建立不覆盖原典、可复现、可追溯、版权边界明确的命理典籍清洗与结构化数据集一期`
- Status: `Done`

## In Scope
- 盘点并清洗 `domains/fate-analysis/data-products/classics/*.txt` 的 14 本 canonical 典籍。
- 新增标准库实现的确定性清洗器，输出文档、段落、检索切片、血缘、哈希、重复和质量报告。
- 清洗结果只写入 `infra/runtime/local-state/exports/datasets/`，不进入公开 Git 资产。
- 增加离线回归测试、数据契约和目录级文档。

## Out of Scope
- 不修改或覆盖原始 canonical TXT。
- 不清洗算准网语料、raw 私有资料、Gem 合并包或外部仓库源码。
- 不把 `review_required` 语料声明为可公开训练、生产依赖或可分发数据。
- 不生成训练/验证/测试划分，不进行专家标注和模型训练。

## Task Package Tree
- ROOT
  ├─ TP-01 [leaf] [P0] 数据契约与边界
  ├─ TP-02 [leaf] [P0] 确定性清洗器
  ├─ TP-03 [leaf] [P0] 回归测试与文档
  ├─ TP-04 [leaf] [P0] 本地数据集生成与质量门禁
  └─ TP-05 [leaf] [P0] 审查与版本控制收口

## Requirement Alignment
- 用户要求先开始清洗整理，当前切片选择版权风险最低、来源边界最清晰的 14 本 canonical 典籍。
- 使用“原文不可变、派生结果可重建”原则，避免一次清洗破坏来源证据。
- 先形成可复现数据管线，再进入版权复核、规则标注和专家数据集阶段。

## Task Package Overview
| Task Package ID | Parent | Depth | Priority | Type | Leaf | Depends On | Wave | Ready | Parallelizable | Objective |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TP-01 | ROOT | 1 | P0 | Contract | Yes | - | 1 | Yes | No | 定义清洗记录、血缘、质量和版权边界 |
| TP-02 | ROOT | 1 | P0 | Implementation | Yes | TP-01 | 2 | No | No | 实现确定性标准库清洗器 |
| TP-03 | ROOT | 1 | P0 | Verification | Yes | TP-02 | 3 | No | No | 添加回归测试并同步目录文档 |
| TP-04 | ROOT | 1 | P0 | DataProduct | Yes | TP-03 | 4 | No | No | 生成并验证 14 本本地派生数据集 |
| TP-05 | ROOT | 1 | P0 | Review | Yes | TP-04 | 5 | No | No | 完成审查、CI、任务和 Git 收口 |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
