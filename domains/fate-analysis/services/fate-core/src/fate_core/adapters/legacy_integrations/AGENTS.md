# AGENTS.md - legacy_integrations

## 目录用途

`legacy_integrations/` 是 fate-core 对历史扩展模块的收敛区：保留外部成熟库 glue 行为，同时切断核心对交付层源码目录的反向依赖。

## 目录结构

```text
legacy_integrations/
├── AGENTS.md
├── __init__.py
├── advanced_calendar_integration.py
├── astro_integration.py
├── bazi1_integration.py
├── dantalion_integration.py
├── enhanced_yijing_integration.py
├── fortel_ziwei_integration.py
├── liuren.py
├── liuyao.py
├── meihua.py
├── mikaboshi_fengshui_integration.py
├── qimen.py
├── sxwnl_integration.py
├── system_optimization.py
├── true_solar_time.py
├── zeri.py
└── ziwei.py
```

## 职责边界

- 本目录只负责把历史扩展模块接到 `fate_core.support.paths`、`fate_core.support.timezone` 和 reference repo 快照。
- 不负责 Web、Bot、API、Markdown 报告渲染或持久化。
- 不允许新增交付层源码路径注入；新增依赖必须先进入 `fate_core.support.paths`。

## 依赖方向

- 允许依赖 `fate_core.support`、标准库和 `tools/reference-repos/github/*`。
- 允许被 `fate_core.kernel.bazi_calculator` 和独立 adapter 调用。
- 禁止反向依赖交付服务源码、FastAPI、Bot、Web UI 或报告生成器。
