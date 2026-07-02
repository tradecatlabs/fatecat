# Execution Checklist

[x] TP-01.01 | P0 | 读取 roadmap、0058/0059、webhook/report job 源码和 smoke | Verify: `rg` / `sed` | Gate: lease baseline 边界明确 | Parallelizable: Yes
[x] TP-02.01 | P0 | 增加 store claim/release 接口和 SQLite lease schema | Verify: focused pytest | Gate: atomic claim 防止第二 owner 领取 | Parallelizable: No
[x] TP-02.02 | P0 | Manager redelivery 接入 claim/release | Verify: focused pytest / smoke | Gate: claim 失败不 dispatch | Parallelizable: No
[x] TP-03.01 | P0 | 新增 webhook outbox lease Python smoke 和 shell wrapper | Verify: smoke CLI | Gate: 输出 JSON 且不依赖公网 | Parallelizable: No
[x] TP-03.02 | P0 | 增加 smoke summary、CLI、claim/release、payload 内部字段测试 | Verify: focused pytest | Gate: 新增断言通过 | Parallelizable: No
[x] TP-03.03 | P0 | 接入 local-ci quick 门禁 | Verify: quick local CI | Gate: smoke 稳定通过 | Parallelizable: No
[x] TP-04.01 | P0 | 更新 API 文档、roadmap、AGENTS 和 INDEX | Verify: docs diff + validators | Gate: 文档不夸大能力 | Parallelizable: No
[x] TP-04.02 | P0 | 运行 focused tests、task validators、lint/hygiene、quick local CI 和 git 交付 | Verify: validators、pytest、ruff、secret scan、local-ci、git status | Gate: 全部通过并推送 | Parallelizable: No
