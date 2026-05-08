# AGENTS.md - fate_core usecases

## 目录用途

`fate_core/usecases/` 是面向产品能力的应用编排层：它组合 adapters、providers 与 profile 投影，输出 capability 可复用的结构化结果。

## 目录结构

```text
usecases/
├── AGENTS.md
├── __init__.py
├── calculate_almanac.py
└── calculate_pure_analysis.py
```

## 职责边界

- `calculate_pure_analysis.py`：综合八字默认生产报告的数据用例。
- `calculate_almanac.py`：黄历择日独立 capability 的数据用例，只输出结构化择日结果和证据。
- `__init__.py`：统一导出稳定用例入口，供 CLI、API 与 capability executor 调用。

## 依赖方向

- 允许依赖 `fate_core.adapters`、`fate_core.providers`、`fate_core.kernel` 和标准库。
- 禁止依赖 Telegram Bot、Web 表单、FastAPI request/response model 或数据库。
- 新体系必须先成为独立用例，再接入 capability executor；不得回写综合八字默认报告。
