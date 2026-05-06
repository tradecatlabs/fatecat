# AGENTS.md - assets 目录说明

## 目录用途

`assets/` 是 FateCat 的静态资产真相源，承载配置模板、静态数据、schema、部署脚本、文档、字段 profile 与外部依赖快照。

## 目录结构

```text
assets/
├── AGENTS.md
├── config/
├── data/
│   └── classics/     # 命理古籍与基础语料文本
├── database/
├── deploy/
├── docs/          # 文档资产，内部按 architecture/operations/reference/roadmap/vendor/archive 分类
├── fate/
├── tasks/
└── vendor/
```

## 职责边界

- `config/`：配置模板、运行配置与品牌真相源入口；不放业务代码。
- `data/`：静态数据文件；不放运行时生成的数据。
  - `data/classics/`：命理古籍、基础知识语料与后续检索/切片输入源。
- `database/`：数据库 schema 与静态定义；不放 `.db` 实库。
- `deploy/`：打包、Agent 引导、环境自举脚本与机器可读部署清单。
- `docs/`：文档资产真相源；架构、运维、参考、路线图、供应链研究与本地归档分区存放。
- `fate/`：命理字段 profile、标准报告边界与未来功能登记真相源。
- `tasks/`：执行教训、任务记忆与过程资产。
- `vendor/`：外部成熟仓库快照，只读；`vendor_sources.json` 记录来源与分发边界。

## 开发规则

- 修改输出字段前，先检查 `assets/fate/`。
- 修改数据库结构前，先改 `assets/database/` 中的 schema。
- 文档落地统一写入 `assets/docs/`。
- 禁止把运行时文件重新放入 `assets/`。
