# Execution Checklist

[x] TP-01.01 | P0 | 读取现有事件契约、gate、tests、docs | Verify: `sed`/`rg` evidence | Gate: 不重复创建事件系统 | Parallelizable: Yes
[x] TP-02.01 | P0 | 增加 consumer compatibility 与 per-event consumerContract | Verify: `python3 -m json.tool contracts/fate/delivery/events.json` | Gate: 每个事件有 required real consumer | Parallelizable: No
[x] TP-02.02 | P0 | 增加 replay/DLQ policy 与脱敏示例 | Verify: `python3 -m json.tool contracts/fate/delivery/examples/event-replay/*.json` | Gate: 示例不保存完整 payload 或敏感值 | Parallelizable: No
[x] TP-03.01 | P0 | 强化 event-contract gate | Verify: `bash scripts/event-contract-gate.sh --output-json /tmp/fatecat-event-contract-0097.json` | Gate: 检查 producer path、consumer、replay/DLQ | Parallelizable: No
[x] TP-03.02 | P0 | 增加 regression 正向和负向测试 | Verify: focused pytest | Gate: 缺 required consumer / producer path 会被拒绝 | Parallelizable: No
[x] TP-04.01 | P0 | 同步 AGENTS、API 接入文档、路线图和任务包 | Verify: docs diff | Gate: 不声明外部 live 已完成 | Parallelizable: Yes
[x] TP-05.01 | P0 | 运行最终验证并 closeout | Verify: task validator, secret scan, quick local-ci | Gate: 无 placeholders、无 secret、local-ci pass | Parallelizable: No
