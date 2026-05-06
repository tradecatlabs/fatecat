# AGENTS.md - runtime 目录说明

## 目录用途

`runtime/` 只存放运行时状态，是 FateCat 的可变层。

## 目录结构

```text
runtime/
├── AGENTS.md
└── database/
    └── bazi/
        └── bazi.db
```

## 职责边界

- `runtime/database/`：SQLite 实库与后续运行态数据库文件。
- 不放 schema、配置模板、部署脚本、文档、外部依赖。
- 这里的数据默认可重建，结构定义应回到 `assets/database/`。

## 开发规则

- 新增运行态目录时，保持“可变数据”与“静态资产”严格分离。
- 若代码需要数据库路径，只能通过 `_paths.py` 读取。
