# Execution Checklist

[x] TP-01.01 | P0 | 读取 roadmap、0056/0058、webhook/report job 源码、依赖和测试 | Verify: `rg` / `sed` 读取相关文件 | Gate: encrypted config vault 边界明确 | Parallelizable: Yes
[x] TP-02.01 | P0 | 引入 cryptography 和 Fernet codec | Verify: focused pytest | Gate: 不自研密码学 | Parallelizable: No
[x] TP-02.02 | P0 | 增加 SQLite encrypted config 存储、读取、删除和 key rotation | Verify: focused pytest | Gate: 原始 SQLite 不含明文 URL/secret | Parallelizable: No
[x] TP-02.03 | P0 | Manager 接入 encrypted config redelivery fallback 和成功删除逻辑 | Verify: API contract test | Gate: 无 vault 时兼容 0058 | Parallelizable: No
[x] TP-03.01 | P0 | 新增 webhook encrypted config vault Python smoke 和 shell wrapper | Verify: smoke CLI | Gate: 输出 JSON 且不依赖公网 | Parallelizable: No
[x] TP-03.02 | P0 | 增加 smoke summary、CLI、encrypted redelivery、delete、rotation、privacy 测试 | Verify: focused pytest | Gate: 新增断言通过 | Parallelizable: No
[x] TP-03.03 | P0 | 接入 local-ci quick 门禁 | Verify: quick local CI | Gate: smoke 稳定通过 | Parallelizable: No
[x] TP-04.01 | P0 | 更新 API 文档、roadmap、scripts/tests AGENTS 和 INDEX | Verify: docs diff + validators | Gate: 文档不夸大能力 | Parallelizable: No
[x] TP-04.02 | P0 | 运行 focused tests、task validators、lint/hygiene、quick local CI 和 git 交付 | Verify: validators、pytest、ruff、secret scan、local-ci、git status | Gate: 全部通过并推送 | Parallelizable: No
