# Execution Checklist

[x] TP-01.01 | P0 | 读取 roadmap、0054/0056/0057、report job webhook 源码和测试 | Verify: `rg` / `sed` 读取相关文件 | Gate: redelivery baseline 边界明确 | Parallelizable: Yes
[x] TP-02.01 | P0 | 增加 pending/failed outbox 查询和 redelivery API | Verify: focused pytest | Gate: 不改变已有 outbox persisted record 语义 | Parallelizable: No
[x] TP-02.02 | P0 | 增加 delivery resolver 与重投调度逻辑 | Verify: focused pytest | Gate: 不持久保存 secret/完整 URL | Parallelizable: No
[x] TP-02.03 | P0 | 增加 redelivery 事件和隐私边界 | Verify: API contract test | Gate: summary/API 不泄露 webhook 配置 | Parallelizable: No
[x] TP-03.01 | P0 | 新增 webhook outbox redelivery Python smoke 和 shell wrapper | Verify: smoke CLI | Gate: 输出 JSON 且不依赖公网 | Parallelizable: No
[x] TP-03.02 | P0 | 增加 smoke summary、CLI、resolver success / resolver missing / resolver error 测试 | Verify: focused pytest | Gate: 新增断言通过 | Parallelizable: No
[x] TP-03.03 | P0 | 接入 local-ci quick 门禁 | Verify: quick local CI | Gate: smoke 稳定通过 | Parallelizable: No
[x] TP-04.01 | P0 | 更新 API 文档、roadmap、scripts/tests AGENTS 和 INDEX | Verify: docs diff + validators | Gate: 文档不夸大能力 | Parallelizable: No
[x] TP-04.02 | P0 | 运行 focused tests、task validators、lint/hygiene、quick local CI 和 git 交付 | Verify: validators、pytest、ruff、secret scan、local-ci、git status | Gate: 全部通过并推送 | Parallelizable: No
