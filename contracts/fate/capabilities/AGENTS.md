# AGENTS.md - capability 协议资产

## 目录用途

`assets/fate/capabilities/` 是新增预测体系的协议真相源。它定义哪些能力存在、是否生产化、需要哪些输入、输出走哪个 profile、证据链和风险边界如何约束。

## 目录结构

```text
capabilities/
├── AGENTS.md
├── provider-drift-contract.json
├── registry.json
├── schemas/
│   ├── capability.schema.json
│   ├── evidence.schema.json
│   ├── error.schema.json
│   ├── input.schema.json
│   ├── output.schema.json
│   ├── provider.schema.json
│   ├── report.schema.json
│   └── resource.schema.json
├── errors.json
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
- `provider-drift-contract.json`：production provider drift report 契约；要求 provider lifecycle、dependency smoke、trace span、source/license/vendor refs 一起参与漂移检查，不保存真实用户输入或外部凭证。
- `schemas/`：协议说明与静态校验口径，不引入运行时算法；`provider.schema.json` 声明 Provider resource、versionLock、lifecycle、source/license/resource manifest、promotionGate 与 deprecation，`report.schema.json` 声明 Report resource envelope 和最小 `policyGate` 门禁，`resource.schema.json` 同时声明 Capability、Provider、CalculationJob、Report、Dataset、EvaluationRun、ObservabilitySignal、SecurityControl、DeliverySurface 等资源字段。
- `errors.json`：测算基础设施标准错误码字典；API `/errors` 读取该契约。
- `profiles/`：各能力独立报告结构；除 `bazi` 外全部 `markdownDefault=false`。
- planned 能力只允许登记，不允许被 executor 当成生产能力执行。
- 新体系上线流程：先补 registry/profile/schema 测试，再实现 `ProviderProtocol` adapter/usecase，补齐 provider lifecycle metadata 并通过 `bash scripts/provider-lifecycle-gate.sh`，最后才把 status 改为 `production`。
