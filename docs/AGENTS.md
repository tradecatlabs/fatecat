# AGENTS.md - docs

## 目录用途

`docs/` 是人类文档入口，负责解释系统、使用方式和路线图，不替代 `contracts/`、`catalog/`、`infra/` 或 `governance/` 的机器事实源。

## 目录结构

```text
docs/
├── AGENTS.md
├── geo.md
├── deployment/
│   └── huggingface-space.md
└── reference-materials/
    ├── AGENTS.md
    ├── architecture/
    ├── operations/
    ├── prompts/
    ├── reference/
    ├── roadmap/
    ├── vendor/
    ├── 生产故障/
    └── 经验/
```

## 职责边界

- `reference-materials/`：原项目文档资产的企业根归位入口，按 architecture、operations、reference、roadmap、vendor、incident 和 lessons 分类。
- `deployment/`：面向用户和维护者的云端部署说明；当前承载 Hugging Face Space 自助部署路径。
- `geo.md`：公开机器发现、项目与旗舰 capability 权威页、实体引用、稳定 query set、GEO 基线、指标口径与复测命令；不保存无法验证的平台排名或引用承诺。
- 事故、任务、门禁和 baseline 证据迁入 `governance/`。

## 依赖方向

- `docs -> contracts + catalog + governance`
