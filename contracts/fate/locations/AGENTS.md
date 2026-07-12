# AGENTS.md - contracts/fate/locations

## 目录用途

`contracts/fate/locations/` 定义出生地点解析、稳定地点 ID、坐标、IANA 时区和出生钟表口径的机器契约；不保存地点数据、用户输入或运行时索引。

## 目录结构

```text
contracts/fate/locations/
├── AGENTS.md
├── registry.json
└── schemas/
    └── location.schema.json
```

## 职责边界

- `registry.json`：地点模式、稳定 ID、坐标系、时区、时间口径、API 和数据产品引用的真相源。
- `schemas/location.schema.json`：地点事实与出生时间规范化结果的字段契约。
- 地点名称重名时必须返回候选并要求稳定 ID，禁止默认选择第一条。
- IANA 时区负责历史 UTC offset 与 DST；固定 GMT 偏移不得代替地点时区。
- 运行时索引属于 `infra/runtime/local-state/`，不得进入本目录或 Git。

## 依赖方向

- `contracts/fate/locations -> contracts/fate/data-supply-chain + domains/fate-analysis/data-products/locations`
- `fatecat-delivery/src/location.py -> contracts/fate/locations + location data product`
