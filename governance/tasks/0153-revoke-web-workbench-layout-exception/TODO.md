# Execution Checklist
[x] TP-01 | P0 | 删除三块工作台布局例外并恢复语义 HTML | Verify: `.venv/bin/python -m pytest -q tests/regression/test_web_html.py` | Gate: 11 passed，响应无 CSS/class/layout 容器。 | Parallelizable: No
[x] TP-02 | P0 | 更新 Web 门禁和长期真相源 | Verify: `rg` 扫描活动真相源无旧授权残留 | Gate: 当前标准统一声明无例外。 | Parallelizable: No
[x] TP-03 | P0 | 执行完整本地验证、审查和 closeout | Verify: governance strict + quick CI + lint/format + diff check + review | Gate: quick CI `401 passed`，治理与审查 PASS。 | Parallelizable: No

说明：
- 每一行绑定唯一 TP。
- 当前无未归属 TODO。
