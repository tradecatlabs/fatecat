# AGENTS.md - domains

## 目录用途

`domains/` 是 FateCat 企业级仓库的领域能力根。核心项目主旨：FateCat 是面向 Agent 与应用开发者的测算基础设施，提供统一的能力协议、可复现计算核心、证据化解释层和多端交付接口。

## 目录结构

```text
domains/
├── AGENTS.md
├── fate-analysis/
│   └── services/fate-core/
└── experience-delivery/
    └── services/fatecat-delivery/
```

## 职责边界

- `fate-analysis/`：测算能力、字段组装、能力 usecase、底层成熟算法适配。
- `experience-delivery/`：Web/API/Bot/Markdown 等交付编排。
- 领域服务只能依赖 `contracts/`、`infra/` 配置入口和 `tools/reference-repos` 中登记的外部成熟资产。

## 依赖方向

- `experience-delivery -> fate-analysis + contracts`
- `fate-analysis -> contracts + tools/reference-repos`
- 禁止 `fate-analysis` 反向依赖 Web/API/Bot 交付细节。
