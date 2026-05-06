# AGENTS.md - assets/docs 文档区说明

## 目录用途

`assets/docs/` 只承载项目级文档资产，不承载运行态输出、数据库实库或业务源码。根层只保留索引、维护说明与 README 使用素材。

## 目录结构

```text
docs/
├── AGENTS.md
├── README.md
├── fatecat-readme-banner.svg
├── architecture/
├── operations/
├── reference/
├── roadmap/
├── vendor/
├── prompts/
├── 生产故障/
├── 经验/
└── archive/
    ├── audit/
    └── raw-notes/
```

## 职责边界

- `architecture/`：架构图、目录结构、序列图与模块边界。
- `operations/`：部署、自举、启动、接口集成与运行说明。
- `reference/`：当前可复核的功能清单、功能状态与字段边界。
- `roadmap/`：未来功能、性能优化与尚未生产落地的计划。
- `vendor/`：外部成熟仓库、供应链研究、复用判断与 vendor 示例隔离说明。
- `prompts/`：Prompt 资产与审查提示词。
- `生产故障/`：事故复盘、生产故障记录与外部化方案。
- `经验/`：已验证的工程经验与教训。
- `archive/`：本地历史输出、生成样例、原始笔记；默认不作为当前真相源。

## 维护规则

- 修改文档路径时同步更新 `scripts/project/README.md` 的文档地图。
- 当前能力边界写入 `reference/`，不要写进 `roadmap/`。
- 未来能力登记写入 `roadmap/`，不要混入当前生产说明。
- 第三方 web 示例只允许作为 vendor 隔离资产；生产 Web 入口必须使用 `modules/telegram/src/web_ui.py`。
- 生成 JSON、原始 TXT 笔记与一次性审计输出不要纳入版本，归档到 `archive/` 并由 `.gitignore` 排除。
