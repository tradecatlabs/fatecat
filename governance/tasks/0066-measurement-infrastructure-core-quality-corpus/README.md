# Task Overview

- Task ID: `0066`
- Slug: `measurement-infrastructure-core-quality-corpus`
- Objective: `执行 0061 后续任务树的 core quality corpus expansion 切片：新增八字/紫微核心质量语料 manifest、完整报告 diff 策略、语料门禁和匿名紫微样本扩容，并接入 quick CI；不使用真实用户隐私样例，不把 evaluation fixture 变成生产输入。`
- Status: `Done`

## In Scope

- 新增 `contracts/fate/evaluations/core-quality-corpus.json`，统一登记八字/紫微核心质量语料、最小样本数、隐私边界和 gate。
- 新增 `contracts/fate/evaluations/report-diff-policy.json`，定义 production report 的结构 diff 策略、体系隔离和隐私边界。
- 扩容 `domains/fate-analysis/data-products/ziwei/golden/cases.json`，从 1 个匿名北京样本扩到 4 个匿名北京样本。
- 给 `domains/fate-analysis/data-products/bazi/golden/statement_cases.json` 补 `source=synthetic_anonymous_fixture`。
- 新增 `scripts/core-quality-corpus-gate.py` 与 shell wrapper，并接入 `scripts/local-ci.sh`。
- 更新 evaluation registry、dataset schema、目录级 AGENTS/README、roadmap 和回归测试。

## Out of Scope

- 不引入真实用户命例、真实姓名、真实非北京地区样例或生产数据。
- 不声明八字/紫微专业准确率 100%。
- 不把 golden fixture 注入 production provider。
- 不锁定完整自然语言断语正文。
- 不接外部专家评测平台、模型评测平台、公网 API 或 Bot live smoke。

## Requirement Alignment

- 对齐 0061 推荐任务：`0066 core quality corpus expansion`，最小交付物为 corpus manifest、bazi/ziwei sample expansion、full report diff policy。
- 对齐基础设施目标：质量语料、报告结构、隐私边界和发布门禁必须是机器可读、可复核、可持续扩展的资产。
- 对齐隐私治理：默认样本只允许北京/测试样本，evaluation fixture 不得成为生产输入。

## Task Package Tree

```text
TP-01 Context audit
  TP-01.01 复核现有 golden fixture、evaluation registry、local-ci 和 L4 smoke
TP-02 Corpus and report policy
  TP-02.01 新增核心质量语料 manifest
  TP-02.02 新增完整报告 diff 策略
TP-03 Gate and samples
  TP-03.01 扩容紫微匿名 fixture
  TP-03.02 新增 core-quality-corpus gate
  TP-03.03 接入 local-ci quick 与 evaluation registry
TP-04 Tests and docs
  TP-04.01 新增回归测试并同步 AGENTS/README/roadmap
  TP-04.02 运行验证并收口本地交付证据
```

## Task Package Overview

| Task Package ID | Parent | Priority | Type | Leaf | Depends On | Objective |
| --- | --- | --- | --- | --- | --- | --- |
| TP-01.01 | TP-01 | P0 | action | Yes | - | 明确现有八字/紫微 fixture、registry 和 local-ci 接线。 |
| TP-02.01 | TP-02 | P0 | action | Yes | TP-01.01 | 新增核心质量语料 manifest。 |
| TP-02.02 | TP-02 | P0 | action | Yes | TP-02.01 | 新增 report diff policy。 |
| TP-03.01 | TP-03 | P0 | action | Yes | TP-02.02 | 扩容紫微匿名基础样本。 |
| TP-03.02 | TP-03 | P0 | action | Yes | TP-03.01 | 新增语料 gate。 |
| TP-03.03 | TP-03 | P0 | action | Yes | TP-03.02 | 接入 registry、local-ci 和 runner。 |
| TP-04.01 | TP-04 | P0 | action | Yes | TP-03.03 | 补回归测试和文档。 |
| TP-04.02 | TP-04 | P0 | action | Yes | TP-04.01 | 完成验证并收口本地交付证据。 |

## Reading Order

1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
