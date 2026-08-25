# AGENTS.md - docs/reference-materials

## 目录用途

`docs/reference-materials/` 保存 FateCat 人类阅读文档、路线图、运营说明、参考资料和历史事故记录；它替代旧 `assets/docs/` 的 active 文档入口。

## 目录结构

```text
docs/reference-materials/
├── AGENTS.md
├── README.md
├── architecture/
├── developer/
├── operations/
├── prompts/
├── reference/
├── roadmap/
├── vendor/
├── 生产故障/
└── 经验/
```

## 职责边界

- `architecture/`：架构图、序列图和目录结构说明。
- `developer/`：OpenAPI、sandbox fixture、curl/Python/Node/Agent 示例和本地 docs smoke 说明；只承载开发者接入文档，不保存真实凭证或生产报告。
- `operations/`：部署、启动、重启和运维说明。
- `reference/`：功能清单、能力协议、基线矩阵、规则扩展和人类可读数学形式化资料；可执行 schema、Profile、有限映射和规则契约仍必须进入 `contracts/fate/`。
- `roadmap/`：后续补齐计划和性能路线图。
- `vendor/`：第三方来源说明和供应链参考分析。
- `生产故障/` 与 `经验/`：历史复盘材料；可沉淀为长期规则时迁入 `governance/evidence/` 或 `governance/processes/`。
- 机器可执行契约不放这里；契约进入 `contracts/`，服务清单进入 `catalog/`，治理证据进入 `governance/`。
