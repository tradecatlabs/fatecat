# AGENTS.md - infra/runtime/local-state

## 目录用途

`infra/runtime/local-state/` 是本地开发和 smoke 的可清理运行态目录。

## 目录结构

```text
infra/runtime/local-state/
├── AGENTS.md
├── database/
│   └── bazi/
│       └── .gitkeep
└── exports/                         # 本地生成、整体忽略
    └── suanzhun-corpus/             # 可恢复研究语料交付目录
```

## 职责边界

- 只提交 `.gitkeep` 与必要目录说明。
- 真实数据库、日志、队列文件、缓存和用户报告不得提交。
- `exports/suanzhun-corpus/` 只承载抓取器生成的 SQLite、按逻辑文章聚合的结构化正文、逐物理详情页来源清单、媒体、失败明细和校验和；它是本地研究交付物，不是 canonical classics 或可公开分发资产。
- 清理入口由 `scripts/clean-runtime.sh` 和 hygiene 门禁维护。
