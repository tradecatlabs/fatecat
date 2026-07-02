# Execution Checklist

[x] TP-01.01 | P0 | 读取 roadmap、0055/0056、report job 源码、API submit 路径和测试 | Verify: `rg` / `sed` 读取相关文件 | Gate: replayable recovery baseline 边界明确 | Parallelizable: Yes
[x] TP-02.01 | P0 | 增加 task_payload 持久化和 store schema | Verify: focused pytest | Gate: 不保存 callable、secret 或 Markdown 正文 | Parallelizable: No
[x] TP-02.02 | P0 | 增加 task_factories 与重建重新入队逻辑 | Verify: focused pytest | Gate: 兼容 0055 restart-safe failure | Parallelizable: No
[x] TP-02.03 | P0 | Web/Markdown 报告任务接入可重建 payload | Verify: API contract test | Gate: 生产报告任务可恢复执行 | Parallelizable: No
[x] TP-03.01 | P0 | 新增 replayable recovery Python smoke 和 shell wrapper | Verify: smoke CLI | Gate: 输出 JSON 且不依赖公网 | Parallelizable: No
[x] TP-03.02 | P0 | 增加 smoke summary、CLI、replayable success / non-replayable failure 测试 | Verify: focused pytest | Gate: 新增断言通过 | Parallelizable: No
[x] TP-03.03 | P0 | 接入 local-ci quick 门禁 | Verify: quick local CI | Gate: smoke 稳定通过 | Parallelizable: No
[x] TP-04.01 | P0 | 更新 API 文档、roadmap、scripts/tests AGENTS 和 INDEX | Verify: docs diff + validators | Gate: 文档不夸大能力 | Parallelizable: No
[x] TP-04.02 | P0 | 运行 focused tests、task validators、lint/hygiene、quick local CI 和 git 交付 | Verify: validators、pytest、ruff、secret scan、local-ci、git status | Gate: 全部通过并推送 | Parallelizable: No
