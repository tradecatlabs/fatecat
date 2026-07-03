# Task Overview
- Task ID: `0096`
- Slug: `measurement-infrastructure-bazi-ziwei-corpus-report-diff-expansion`
- Objective: `执行 0095 Wave A Next-01：扩容八字/紫微核心质量 corpus 与 report diff gate，使核心测算质量不只依赖少量代表样本；新增或强化本地可复核的 fixture/manifest/contract/tests，覆盖更多八字与紫微结构标签、报告结构摘要、evidence coverage 和 privacy/no-leak 边界；只保存匿名合成样本、hash/结构化摘要，不保存真实用户资料、完整报告正文或 benchmark 标准答案；不改生产 provider 算法，不宣称预测准确率或专业能力 100%。`
- Status: `Done`

## In Scope
- 扩容紫微 basic anonymous fixture。
- 强化 `core-quality-corpus.json` 的最小样本数、coverage tags 和 report diff policy 引用。
- 强化 `report-diff-policy.json` 的 summary-only 结构 diff 策略。
- 强化 `core-quality-corpus-gate.py` 和回归测试。
- 同步 evaluation registry、AGENTS、路线图和任务文档。

## Out of Scope
- 不修改八字/紫微 production provider 算法。
- 不新增真实命例、真实非北京地区、真实姓名或完整报告正文。
- 不把 corpus 扩容声明为八字/紫微专业能力 100%。
- 不接入外部 live、专家人工复核或 benchmark 标准答案。

## Task Package Tree
```text
TP-01 现状复核
  TP-01.01 读取现有 corpus/report diff/gate/test
TP-02 语料与契约扩容
  TP-02.01 扩容紫微 basic fixture
  TP-02.02 更新 core-quality manifest 与 report diff policy
TP-03 Gate 与测试强化
  TP-03.01 更新 core-quality gate
  TP-03.02 更新 regression tests
TP-04 文档与路线图同步
  TP-04.01 更新 registry/AGENTS/roadmap/task docs
TP-05 验证与收口
  TP-05.01 运行 gate、focused pytest、task validator
```

## Requirement Alignment
| 用户/路线图要求 | 落盘方式 |
| --- | --- |
| 以任务树为执行框架 | 0096 拆为 TP-01 到 TP-05，并在 TODO/STATUS 中记录。 |
| 扩容八字/紫微 core corpus | 紫微 basic corpus 从 4 个样本扩为 8 个；八字 300 矩阵保持既有强基线。 |
| 强化 report diff | `report-diff-policy.json` 增加 summary-only structural diff 和 forbidden stored fields。 |
| 不泄露隐私 | 所有新增样本均为北京/测试样本，gate 校验 birthPlace/name 和 no full report body。 |
| 不改生产算法 | 只改 data-products、contracts、gate、tests 和 docs。 |

## Task Package Overview
| Node ID | Title | Status |
| --- | --- | --- |
| TP-01.01 | 读取现有 corpus/report diff/gate/test | Done |
| TP-02.01 | 扩容紫微 basic fixture | Done |
| TP-02.02 | 更新 core-quality manifest 与 report diff policy | Done |
| TP-03.01 | 更新 core-quality gate | Done |
| TP-03.02 | 更新 regression tests | Done |
| TP-04.01 | 更新 registry/AGENTS/roadmap/task docs | Done |
| TP-05.01 | 运行 gate、focused pytest、task validator | Done |

## Reading Order
1. `IMPLEMENTATION.md`
2. `README.md`
3. `CONTEXT.md`
4. `PLAN.md`
5. `ACCEPTANCE.md`
6. `ACCEPTANCE_CHECKLIST.md`
7. `TODO.md`
8. `STATUS.md`
