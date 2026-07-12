---
id: CTX-DOMAINS-EXPERIENCE-DELIVERY-SERVICES-FATECAT-DELIVERY-SRC-LOCATION-PY
type: module-context
status: current
owner: engineering
created: 2026-07-12
last_reviewed: 2026-07-12
code_path: domains/experience-delivery/services/fatecat-delivery/src/location.py
---

# FateCat 出生地点与时间口径 Context

## 模块职责

- 把稳定地点 ID、文本唯一匹配或 WGS84 坐标解析为统一 `ResolvedLocation`。
- 使用 IANA tzdb 处理出生地历史 UTC offset、DST 缺口和回拨重复时刻。
- 把 `local_civil`、`beijing_time` 或 `utc` 钟表时间转换为现有计算引擎使用的北京时间墙上时间。

## 单一真相源

- 协议：`contracts/fate/locations/registry.json`
- 数据：`domains/fate-analysis/data-products/locations/`
- 运行索引：`src/location_catalog.py`
- 边界回归：`tests/regression/test_location.py`、`tests/regression/test_location_catalog.py`

## 禁止事项

- 禁止用固定 UTC offset 代替 IANA 时区。
- 禁止对重名地点、时间口径或 DST fold 做默认猜测。
- 禁止把中心点坐标包装成精确出生地址。
- 禁止写回 canonical 数据或把运行时 SQLite 提交入库。
