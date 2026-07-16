# Task Overview
- Task ID: `0163`
- Slug: `classics-curation-policy`
- Objective: `建立源哈希绑定的典籍正文选择、书目角色、完整性问题和人工复核队列，清除派生数据中的来源说明与推广噪声`
- Status: `Done`

## In Scope
- 为 14 本 canonical TXT 建立 source-hash 绑定的整理策略。
- 显式登记文献家族、文本角色、完整性状态、书目待审项和正文选择规则。
- 从派生 passages 中排除项目自写来源说明、ctext 章节 URL 与已确认推广包装，canonical TXT 不变。
- 增加人工复核队列、正文选择血缘、负向测试和真实数据集重建证据。

## Out of Scope
- 不改写、重命名或覆盖 canonical TXT。
- 不把候选作者、年代、底本或版权判断写成已核实事实。
- 不修复古籍 OCR、异体字、标点、缺卷或截断正文。
- 不创建训练/验证/测试集，不授权模型训练、生产运行或公开分发。

## Task Package Tree
- ROOT
  - TP-01 [P0] 污染与书目边界审计
  - TP-02 [P0] 源 hash 绑定整理策略
  - TP-03 [P0] 清洗器策略接入
  - TP-04 [P0] 回归与真实数据集重建
  - TP-05 [P0] 深审、CI 与版本控制收口

## Requirement Alignment
- 用户要求继续整理；本轮承接一期清洗数据集，不扩张到未经授权的训练或专家标注。
- 采用显式 policy 而非隐藏关键词删除，保证每条正文排除规则可审计、可失效、可回滚。

## Task Package Overview
| Task Package ID | Parent | Priority | Type | Depends On | Objective |
| --- | --- | --- | --- | --- | --- |
| TP-01 | ROOT | P0 | Audit | - | 识别正文污染、缺卷、截断、书名/作者混写和高重叠家族 |
| TP-02 | ROOT | P0 | Contract | TP-01 | 建立 source-hash 绑定的文档角色、问题和正文选择策略 |
| TP-03 | ROOT | P0 | Implementation | TP-02 | 让现有清洗器消费 policy 并输出可追溯整理元数据 |
| TP-04 | ROOT | P0 | Verification | TP-03 | 证明策略失效保护、正文排除、无损切片与真实重建 |
| TP-05 | ROOT | P0 | Review | TP-04 | 完成审查、Quick CI、任务和本地版本控制收口 |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
