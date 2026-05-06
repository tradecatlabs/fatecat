# AGENTS.md - modules

## 目录用途

`modules/` 是 FateCat 的代码骨架层：上承 `assets/` 的静态配置与数据，下接 `runtime/` 的运行态结果。

## 目录结构

```text
modules/
├── AGENTS.md
├── fate_core/   # 纯命理分析内核
└── telegram/    # Bot / API 交付模块
```

## 职责边界

- `fate_core/`：只负责字段契约、分析管线、provider 与 usecase。
- `telegram/`：只负责 Telegram、FastAPI、报告生成与遗留适配。
- 禁止把配置模板、schema、文档重新塞回 `modules/`。

## 依赖方向

- `modules/fate_core -> assets/fate + assets/vendor`
- `modules/telegram -> modules/fate_core + assets/* + runtime/*`
- 禁止 `fate_core` 反向依赖 `telegram`。
