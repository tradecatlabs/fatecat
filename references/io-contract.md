# FateCat Skill 输入输出契约

## 纯分析最小输入

```json
{
  "birthDateTime": "1990-01-01 08:00:00",
  "gender": "男",
  "longitude": 116.4074,
  "latitude": 39.9042,
  "birthPlace": "北京市"
}
```

这个最小 JSON 就是推荐的 smoke test 输入，无需再维护单独的 `request-examples/` 目录。

`gender` 接受 `male` / `female` / `男` / `女`；计算前会统一归一为 `male` / `female`，输出展示层仍可能翻译为 `男` / `女`。

## 可接受别名

- `birth_datetime`
- `birth_dt`
- `datetime`
- `sex`
- `lng`
- `lat`
- `birth_place`

这些别名由 `scripts/project/modules/fate_core/src/fate_core/cli.py` 中的输入归一化逻辑处理。

## 纯分析输出顶层

```json
{
  "disclaimer": "...",
  "success": true,
  "profile": "pure_analysis",
  "data": {},
  "branding": {}
}
```

## 交付层入口

- CLI：`.venv/bin/fatecat pure-analysis`
- Health：`.venv/bin/fatecat health --mode pure|delivery`
- API：`POST /api/v1/bazi/pure-analysis`
- API：`POST /api/v1/bazi/calculate`
- Bot：`.venv/bin/fatecat serve bot`
