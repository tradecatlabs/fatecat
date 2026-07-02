# Execution Checklist

[x] TP-01.01 | P0 | 读取 0061、roadmap、delivery contracts、job store docs 和 gate 风格 | Verify: `sed` / `rg` | Gate: 缺口明确 | Parallelizable: Yes
[x] TP-02.01 | P0 | 新增 RuntimeBackend schema、registry 和 resource schema link | Verify: focused tests | Gate: resource model 可发现 | Parallelizable: No
[x] TP-02.02 | P0 | 更新 delivery registry 与 AGENTS | Verify: focused tests / docs diff | Gate: contract link 一致 | Parallelizable: No
[x] TP-03.01 | P0 | 新增 runtime-backend-gate Python/sh wrapper | Verify: gate CLI | Gate: 无外部依赖 | Parallelizable: No
[x] TP-03.02 | P0 | 新增 regression tests 覆盖 contract、CLI 和边界声明 | Verify: focused pytest | Gate: 边界断言通过 | Parallelizable: No
[x] TP-03.03 | P0 | 接入 local-ci quick artifact | Verify: local-ci summary artifact | Gate: quick CI 运行新 gate | Parallelizable: No
[x] TP-04.01 | P0 | 更新 API 文档、roadmap、scripts AGENTS 和 INDEX | Verify: docs diff + rg | Gate: 文档不夸大 | Parallelizable: No
[x] TP-04.02 | P0 | 运行 focused tests、validators、lint/hygiene、quick local CI 并收口 | Verify: validation evidence | Gate: 全部通过 | Parallelizable: No
