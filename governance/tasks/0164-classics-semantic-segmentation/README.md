# Task Overview
- Task ID: `0164`
- Slug: `classics-semantic-segmentation`
- Objective: `将 14 本 canonical 命理典籍从物理换行重建为可追溯语义段落，分离目录导航并确保检索切片不跨章节边界`
- Status: `Done`

## In Scope
- 升级典籍派生数据契约，区分 document title、heading、navigation 与 body 记录。
- 将被排版换行拆碎的正文无损重建为语义段落，并保留精确源行血缘。
- 通过 source-hash 绑定策略显式登记目录行范围，不用模糊模型猜测目录。
- 让 passage 只在同一 heading path 内组合，禁止跨章节、跨卷和目录污染。
- 增加真实 14 本数据集的结构质量、确定性和 canonical 不变回归。

## Out of Scope
- 不修改、覆盖、重命名或校勘 canonical TXT。
- 不自动纠正 OCR、异体字、标点、作者、底本、缺卷和版权结论。
- 不删除跨书或同书重复正文；只继续生成重复证据。
- 不引入分词器、向量库、LLM 清洗、数据库或另一套平行清洗脚本。
- 不把派生数据声明为可训练、可生产运行或可公开分发。

## Task Package Tree
- ROOT
  - TP-01 [P0] 语义结构契约与目录范围
  - TP-02 [P0] 源行到语义段落的无损重建
  - TP-03 [P0] 章节边界内 passage 与血缘验证
  - TP-04 [P0] 真实 14 本 v3 重建和质量门禁
  - TP-05 [P0] 深审、Quick CI 与本地版本收口

## Requirement Alignment
- 用户要求继续整理；本轮承接 0162/0163，只处理已确认的结构质量缺陷。
- 当前 v2 中 12,125/32,931 个段落短于 12 字，142 个 passage 跨越已识别标题；这些是可机械证明的检索质量问题。
- 采用标准库、现有 policy 和现有 owner script，不引入新依赖或平行管线。

## Task Package Overview
| Task Package ID | Parent | Priority | Type | Depends On | Objective |
| --- | --- | --- | --- | --- | --- |
| TP-01 | ROOT | P0 | Contract | - | 定义 v3 语义段落、记录类型、精确血缘和目录范围契约 |
| TP-02 | ROOT | P0 | Implementation | TP-01 | 重建被排版换行拆碎的语义段落并维护标题层级 |
| TP-03 | ROOT | P0 | Implementation | TP-02 | passage 不跨 heading path，navigation 不进入检索正文 |
| TP-04 | ROOT | P0 | Verification | TP-03 | 真实 14 本重建、确定性、无损和结构质量回归 |
| TP-05 | ROOT | P0 | Review | TP-04 | 完成审查、Quick CI、任务和本地 Git 收口 |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
