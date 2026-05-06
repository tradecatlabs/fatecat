# AGENTS.md - fate_core

## 目录用途

`modules/fate_core/` 是命理胶水层内核：负责字段契约、profile、adapter、pipeline 与 usecase，不承载 Telegram / FastAPI 交付逻辑。

## 目录结构

```text
modules/fate_core/
├── AGENTS.md
└── src/fate_core/
    ├── cli.py
    ├── __main__.py
    ├── adapters/
    ├── contracts/
    ├── kernel/
    ├── providers/
    ├── support/
    └── usecases/
```

## 职责边界

- `cli.py` / `__main__.py`：命令行入口；负责 Agent / OpenClaw / Harness 的标准化调用面，不下沉到底层算法。
- `support/branding.py`：统一品牌真相源读取与广告拼装；CLI / API / Telegram 只消费，不各自硬编码。
- `contracts/`：字段契约与 profile 加载；禁止依赖 Telegram / FastAPI。
- `adapters/`：唯一允许接触外部成熟 repo 或遗留 calculator 的地方；对内导出稳定适配符号。
- `providers/`：按字段组装配纯命理输出；只能通过 `adapters/` 调用遗留 calculator / helper，不直接导入 `bazi_calculator`。
- `kernel/`：结果投影与管线拼装；不实现底层算法。
- `usecases/`：对外暴露 `pure_analysis` / `full_report` 等应用入口。

## 依赖方向

- `usecases -> providers/kernel/contracts/adapters`
- `providers -> contracts/adapters`
- `kernel -> contracts`
- `adapters -> 外部库 / 遗留模块`
- 禁止 `contracts` 反向依赖 `usecases` 或 `telegram/api`
