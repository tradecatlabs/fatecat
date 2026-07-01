# AGENTS.md - tools

## 目录用途

`tools/` 承载开发工具、迁移工具、参考仓和供应链快照，不作为生产运行路径。

## 目录结构

```text
tools/
├── AGENTS.md
└── reference-repos/
    ├── AGENTS.md
    ├── README.md
    ├── vendor_sources.json
    ├── github/
    └── web/
```

## 职责边界

- `reference-repos/`：第三方开源仓与网页参考快照，配套 manifest、hash、license 和运行态污染门禁。
- 任何 vendor 迁移只能移动和登记，不得魔改外部源码。

## 依赖方向

- `domains -> tools/reference-repos` 只能通过 adapter 或 manifest 消费。
