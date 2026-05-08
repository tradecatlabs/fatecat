# AGENTS.md - fate_core adapters

## 目录用途

`fate_core/adapters/` 是成熟外部库与遗留实现进入核心用例层的唯一适配边界；它只做路径注入、接口收敛和兼容封装，不承载业务报告逻辑。

## 目录结构

```text
adapters/
├── AGENTS.md
├── __init__.py
├── legacy_bazi.py
└── lunar_calendar.py
```

## 职责边界

- `legacy_bazi.py`：封装遗留 `BaziCalculator`，为综合八字纯分析保留稳定入口。
- `lunar_calendar.py`：封装 `lunar-python` 公历转农历/黄历入口，供黄历择日等独立 capability 复用。
- `__init__.py`：对外暴露经过适配的稳定符号，避免上层散落 vendor 路径处理。

## 依赖方向

- 允许依赖 `fate_core.support.paths` 和 `assets/vendor/github/*` 的成熟库快照。
- 禁止依赖 FastAPI、Bot、Web UI 或报告渲染层。
- 新增外部库入口必须先在这里收敛，再由 `usecases/` 编排。
