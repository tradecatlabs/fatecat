# AGENTS.md - discovery contracts

## 目录用途

`contracts/fate/discovery/` 保存公开发现与 GEO 效果验证所需的机器契约。这里定义稳定问题、事实边界和官方来源，不保存营销文案、真实用户输入或伪造的平台答案。

## 目录结构

```text
discovery/
├── AGENTS.md
└── query-set.json
```

## 职责边界

- `query-set.json`：跨周期复用的 AI 问答采样题集；每题必须有稳定 ID、问题组、目标实体、预期事实、官方来源和禁止声明。
- 题集不代表任何平台已经收录、提及、引用或推荐 FateCat。
- 真实平台样本、截图、答案和指标属于外部验证证据，不得写入公开契约。
- 新增题目必须描述项目真实能力，并通过 `scripts/geo-query-set-gate.py`。

## 依赖方向

- `scripts/geo-query-set-gate.py -> contracts/fate/discovery/query-set.json`
- `domains/experience-delivery -> contracts/fate/discovery/query-set.json` 只读公开输出
- discovery 契约可引用 capability/API 真相源，但不得反向定义测算能力。
