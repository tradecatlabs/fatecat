# AGENTS.md - contracts/fate

## 目录用途

`contracts/fate/` 存放 FateCat 测算基础设施的能力协议、字段、profile、权重和规则深度契约，是输出字段口径的配置真相源。

## 目录结构

```text
contracts/fate/
├── AGENTS.md
├── capabilities/
│   ├── registry.json
│   ├── schemas/
│   └── profiles/
├── classics_rule_index.json
├── evidence_schema.json
├── future_features.json
├── rule_depth_registry.json
├── weight_policy.json
└── profiles/
    └── pure_analysis.json
```

## 职责边界

- `capabilities/`：统一测算能力协议与注册表；默认能力只能是 `bazi`，其他体系必须独立输出或保持 planned。
- `capabilities/registry.json` 的每个能力必须声明 `maturity`、`engine.engineVersion`、`evidencePolicy` 和 `testGate`；这些字段是测算基础设施成熟度、可复现计算和发布门禁的审计入口。
- `future_features.json`：记录不再进入标准报告、后续需按新功能重新设计契约的候选能力。
- `evidence_schema.json`：综合八字机器可读 evidence 字段契约；默认不渲染到 Markdown。
- `weight_policy.json`：综合八字核心、动态、辅助、民俗权重边界。
- `classics_rule_index.json`：典籍规则索引种子，只保存短规则与来源，不保存大段原文。
- `rule_depth_registry.json`：八字/紫微规则深度配置，只保存规则条件、证据字段、冲突策略与风险边界。
- `owner` / `governance.extensionPolicy`：规则和候选能力的变更口径；新增规则必须有来源、适用条件、不适用条件和风险边界，不得写入确定性断语字段。
- `profiles/`：定义某个输出 profile 允许返回哪些字段。
- 这里不放算法代码，不依赖 Telegram / FastAPI / 数据库。
- 新增字段时，先更新这里的 profile，再更新 `domains/fate-analysis/services/fate-core/` 的 provider / usecase。
