# Execution Checklist

[x] TP-01.01 | P0 | 读取 0052、roadmap、report job 源码、API 文档和生产预检 | Verify: `rg` / `sed` 读取相关文件 | Gate: retry/timeout 切片边界明确 | Parallelizable: Yes
[x] TP-02.01 | P0 | 新增 execution policy 模型、job 字段、SQLite schema 兼容和 API payload 字段 | Verify: py_compile + API contract tests | Gate: 默认 `maxAttempts=1` 且 API 字段稳定 | Parallelizable: No
[x] TP-02.02 | P0 | 修改状态机，支持 retry、timeout、non-retryable 事件和最终状态 | Verify: focused tests | Gate: retry 有界、timeout 有事件、non-retryable 不重试 | Parallelizable: No
[x] TP-03.01 | P0 | 增加 retry 成功、non-retryable 不重试、timeout 失败和 SQLite policy persistence 测试 | Verify: focused pytest | Gate: 新增断言通过 | Parallelizable: No
[x] TP-03.02 | P0 | 更新 API 文档、roadmap、deployment docs、production-readiness、AGENTS 和 INDEX | Verify: docs diff + validators | Gate: 文档不夸大能力 | Parallelizable: No
[x] TP-04.01 | P0 | 运行 focused tests、task validators、lint/hygiene、quick local CI 和 git 交付 | Verify: validators、pytest、ruff、local-ci、git status | Gate: 全部通过并推送 | Parallelizable: No
