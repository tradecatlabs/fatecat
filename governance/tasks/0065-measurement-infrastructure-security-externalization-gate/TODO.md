# Execution Checklist

[x] TP-01.01 | P0 | 读取 0061/0064、security registry、production-security-gate、local-ci 和 API 文档 | Verify: `git status` / `rg` / `sed` | Gate: 当前事实和 0065 边界明确 | Parallelizable: Yes
[x] TP-02.01 | P0 | 新增 OIDC/SIEM/retention cleaner evidence contract | Verify: JSON syntax + gate | Gate: contract 可机器读取 | Parallelizable: No
[x] TP-02.02 | P0 | 更新 security registry、schema 和 AGENTS | Verify: focused tests / docs diff | Gate: registry/schema/AGENTS 链接一致 | Parallelizable: No
[x] TP-03.01 | P0 | 新增 security-externalization-gate Python/sh wrapper | Verify: gate CLI | Gate: 无外部账号依赖 | Parallelizable: No
[x] TP-03.02 | P0 | 新增 regression tests 覆盖 contract、CLI 和 fake evidence negative cases | Verify: focused pytest | Gate: 边界断言通过 | Parallelizable: No
[x] TP-03.03 | P0 | 接入 local-ci quick artifact | Verify: local-ci summary artifact | Gate: quick CI 运行新 gate | Parallelizable: No
[x] TP-04.01 | P0 | 更新 API 文档、roadmap、scripts AGENTS 和 INDEX | Verify: docs diff + rg | Gate: 文档不夸大 | Parallelizable: No
[x] TP-04.02 | P0 | 运行 focused tests、validators、lint/hygiene、quick local CI 并收口 | Verify: validation evidence | Gate: 全部通过 | Parallelizable: No
