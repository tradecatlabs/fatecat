# AGENTS.md - fate_core adapters

## 目录用途

`fate_core/adapters/` 是成熟外部库与遗留实现进入核心用例层的唯一适配边界；它只做路径注入、接口收敛和兼容封装，不承载业务报告逻辑。

## 目录结构

```text
adapters/
├── AGENTS.md
├── __init__.py
├── legacy_integrations/
├── legacy_bazi.py
├── lunar_calendar.py
└── ziwei_iztro.py
```

## 职责边界

- `legacy_bazi.py`：封装 `fate_core.kernel.bazi_calculator.BaziCalculator`，为综合八字纯分析保留稳定入口；不得再从 delivery `src/bazi_calculator.py` 取领域算法。
- `legacy_integrations/`：承载已从交付层剥离到核心包的外部库 glue 模块；只做成熟库编排和历史扩展入口收敛。
- `lunar_calendar.py`：封装已声明生产依赖 `lunar-python` 的公历日/时转农历黄历入口；仅在开发环境缺安装包时回退到 reference repo。
- `ziwei_iztro.py`：封装紫微斗数 iztro 入口；只借用遗留真太阳时管线，不调用八字扩展链生成紫微结果。
- `__init__.py`：对外暴露经过适配的稳定符号，避免上层散落 vendor 路径处理。

## 依赖方向

- 允许依赖 `fate_core.kernel`、`fate_core.support.paths` 和 `tools/reference-repos/github/*` 的成熟库快照。
- 禁止依赖 FastAPI、Bot、Web UI 或报告渲染层。
- 新增外部库入口必须先在这里收敛，再由 `usecases/` 编排。
- 禁止通过 `sys.path` 指向交付服务源码目录；核心只能通过包内 adapter 或 reference repo 路径读取依赖。

## Principle Gate Evidence

- target end state: adapters isolate mature libraries and migration kernels behind stable contracts.
- real constraints: usecases need stable imports while kernel/provider slices continue to move.
- inertia constraints: adapter names record integration history, not long-term domain ownership.
- kill list: adapter business logic, report rendering, and hidden vendor path mutation.
- proof point: fate-core service contract and capability protocol tests pass.
- falsifier: adapter imports FastAPI/Bot/Web/report or emits user-facing report prose.
- migration slice: keep thin adapters until each provider has direct production contract coverage.
- existence: adapters are the lowest viable boundary for external libraries and current kernels.
- owner: tradecatlabs/fate-core.
- verification: `domains/fate-analysis/services/fate-core/tests/test_service_contract.py`.
