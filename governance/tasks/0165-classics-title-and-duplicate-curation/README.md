# Task Overview
- Task ID: `0165`
- Slug: `classics-title-and-duplicate-curation`
- Objective: `修正典籍重复书名记录类型，分类重复正文关系并生成可操作的人工复核统计，不自动删除或改写 canonical 正文`
- Status: `Done`

## In Scope
- 每本文档最多保留一个真实 `document_title`；后续重复书名转为 heading 并形成边界。
- 为 exact paragraph、exact passage 与 document overlap 证据增加确定性关系分类。
- 在质量报告聚合人工复核 issue/severity/block 与重复关系统计。
- 增加真实 14 本数据和 validator tamper 回归。

## Out of Scope
- 不修改、删除、覆盖或校勘 canonical TXT。
- 不自动删除同书重复、原文/评注共享文本或跨书引用。
- 不代替人类完成作者、底本、版权、缺卷和截断判断。
- 不新增脚本、依赖、数据库、向量库或平行数据集版本。

## Task Package Tree
- ROOT
  - TP-01 [P0] 契约与 red evidence
  - TP-02 [P0] 文档标题唯一性与边界修复
  - TP-03 [P0] 重复关系分类和复核摘要
  - TP-04 [P0] 真实语料重建与 fail-closed 门禁
  - TP-05 [P0] 深审、Quick CI 和本地交付

## Requirement Alignment
- 用户要求继续整理现有命理资料；本轮承接 0164 的 v3 数据，不扩展到典籍内容校勘。
- 实证显示 14 本数据产生 29 个 `document_title`，同一本最多 8 个，属于记录类型错误。
- 基线 478 个 exact paragraph group 中 404 个是同家族共享文本，不能与 46 个同书重复、28 个跨家族共享文本混为一类；关系名称不推断版本传承方向。
- 使用现有 cleaner、schema、quality report 和 tests，避免新增所有权面。

## Task Package Overview
| Task Package ID | Parent | Priority | Type | Depends On | Objective |
| --- | --- | --- | --- | --- | --- |
| TP-01 | ROOT | P0 | Contract/Test | - | 锁定标题唯一性、关系枚举、统计字段和 red tests |
| TP-02 | ROOT | P0 | Bugfix | TP-01 | 首次书名为 title，后续重复书名作为 heading |
| TP-03 | ROOT | P0 | Feature | TP-02 | 分类重复证据并聚合复核统计 |
| TP-04 | ROOT | P0 | Verification | TP-03 | 真实 14 本构建、tamper 负例和确定性验证 |
| TP-05 | ROOT | P0 | Review/Ship | TP-04 | 完成深审、Quick CI、任务 closeout 和本地提交 |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
