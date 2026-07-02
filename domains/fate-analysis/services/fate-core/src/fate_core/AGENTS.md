# AGENTS.md - fate_core root

## 目录用途

`fate_core/` 是 FateCat 领域核心包根目录。这里承载可被 API、Web、Bot、CLI 和 Agent Skill 复用的领域能力、provider 协议、观测上下文和支撑工具；不承载 FastAPI、Telegram、HTML 或数据库交付逻辑。

## 目录结构

```text
fate_core/
├── AGENTS.md
├── __init__.py
├── cli.py
├── observability.py
├── adapters/
├── capabilities/
├── evaluation/
├── kernel/
├── providers/
├── support/
└── usecases/
```

## 职责边界

- `observability.py`：W3C `traceparent`、trace context 和 OpenTelemetry 语义兼容本地 span 日志的薄共享层；只记录 trace/span ID、span 名称、耗时、状态、错误类别和低敏属性，不记录用户输入、报告正文或 secret。
- `capabilities/`：统一 capability 协议、provider registry、execution admission 和 report policy。
- `usecases/`：组合 adapters/providers，输出结构化领域结果。
- `kernel/`：命理核心算法与稳定胶水层。
- `adapters/`：成熟外部库和遗留实现适配边界。
- `providers/`：八字结构化字段组装器。
- `evaluation/`：离线 benchmark 和评测基线，不参与生产推理。
- `support/`：无业务副作用的路径、时间、品牌支撑工具。
- `cli.py`：本地命令行入口。

## 依赖方向

- 允许依赖标准库、包内 `adapters`、`capabilities`、`kernel`、`providers`、`support`、`usecases` 和已登记的成熟依赖。
- 禁止依赖 FastAPI request/response、Telegram Bot、Web HTML、数据库连接或交付层渲染。
- `observability.py` 可被 delivery 读取 trace context，但不得反向导入 delivery。
