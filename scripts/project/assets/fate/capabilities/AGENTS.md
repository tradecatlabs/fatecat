# AGENTS.md - capability 协议资产

## 目录用途

`assets/fate/capabilities/` 是新增预测体系的协议真相源。它定义哪些能力存在、是否生产化、需要哪些输入、输出走哪个 profile、证据链和风险边界如何约束。

## 目录结构

```text
capabilities/
├── AGENTS.md
├── registry.json
├── schemas/
│   ├── capability.schema.json
│   ├── evidence.schema.json
│   ├── input.schema.json
│   └── output.schema.json
└── profiles/
    ├── almanac.json
    ├── bazi.json
    ├── daliuren.json
    ├── fengshui_nine_stars.json
    ├── liuyao.json
    ├── meihua.json
    ├── name_marriage.json
    ├── qimen.json
    └── ziwei.json
```

## 职责边界

- `registry.json`：统一能力注册表；`bazi` 是唯一默认 production 能力。
- `schemas/`：协议说明与静态校验口径，不引入运行时算法。
- `profiles/`：各能力独立报告结构；除 `bazi` 外全部 `markdownDefault=false`。
- planned 能力只允许登记，不允许被 executor 当成生产能力执行。
- 新体系上线流程：先补 registry/profile/schema 测试，再实现 provider/usecase，最后才把 status 改为 `production`。
