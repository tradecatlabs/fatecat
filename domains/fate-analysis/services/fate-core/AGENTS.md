# AGENTS.md - fate-core

## 目录用途

`fate-core` 是 FateCat 纯分析领域服务。本服务根是源码真相源，运行资产从 `contracts/`、`infra/`、`tools/` 和 `domains/fate-analysis/data-products/` 读取。

## 目录结构

```text
fate-core/
├── AGENTS.md
├── README.md
├── service.yaml
├── src/
│   └── fate_core/
│       ├── adapters/
│       ├── evaluation/
│       ├── kernel/
│       ├── providers/
│       └── usecases/
├── scripts/
│   ├── dantalion_bridge.js
│   └── true_solar_time.js
└── tests/
    └── test_service_contract.py
```

## 职责边界

- 负责纯命理分析内核、capability registry 执行、字段契约加载、provider/usecase 编排。
- `src/fate_core/evaluation/` 负责离线 benchmark 与预测 baseline；只能读取领域用例输出，不反向影响生产排盘。
- `src/fate_core/adapters/` 负责外部库、历史扩展模块和迁移中 kernel 的适配边界。
- `scripts/` 负责 fate-core 自有的 Node glue 脚本，禁止从交付服务目录读取运行脚本。
- 保持 CLI `fatecat pure-analysis`、`fatecat capability` 和 `fatecat health` 外部行为不变。
- 不新增旧路径 fallback；行为保持验证先于大规模重构。

## 依赖方向

- 当前状态：`domains/fate-analysis/services/fate-core -> contracts/fate + domains/fate-analysis/data-products + infra/databases + tools/reference-repos`
- 运行态只允许写入 `infra/runtime/local-state/`，不得写回 vendor 或契约目录。
- 禁止反向依赖 `fatecat-delivery`。
