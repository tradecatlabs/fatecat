# Execution Checklist

[x] TP-01.01 | P0 | 读取 0054、roadmap、report job 源码、SQLite rebuild tests 和 local-ci | Verify: `rg` / `sed` 读取相关文件 | Gate: restart recovery smoke 切片边界明确 | Parallelizable: Yes
[x] TP-02.01 | P0 | 新增 restart recovery Python smoke 和 shell wrapper | Verify: smoke CLI | Gate: 输出 JSON 且不依赖真实环境 | Parallelizable: No
[x] TP-02.02 | P0 | 接入 local-ci quick 门禁 | Verify: quick local CI | Gate: smoke 稳定通过 | Parallelizable: No
[x] TP-03.01 | P0 | 增加 smoke summary、CLI 和隐私边界测试 | Verify: focused pytest | Gate: 新增断言通过 | Parallelizable: No
[x] TP-03.02 | P0 | 更新 API 文档、roadmap、scripts AGENTS 和 INDEX | Verify: docs diff + validators | Gate: 文档不夸大能力 | Parallelizable: No
[x] TP-04.01 | P0 | 运行 focused tests、task validators、lint/hygiene、quick local CI 和 git 交付 | Verify: validators、pytest、ruff、local-ci、git status | Gate: 全部通过并推送 | Parallelizable: No
