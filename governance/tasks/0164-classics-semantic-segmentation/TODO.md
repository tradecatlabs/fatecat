# Execution Checklist
[x] TP-01 | P0 | 建立 v3 语义结构契约与目录范围 | Verify: schema/policy/data gate | Gate: fail closed | Parallelizable: No
[x] TP-02 | P0 | 实现源行到语义段落的无损重建 | Verify: focused tests | Gate: semantic replay zero | Parallelizable: No
[x] TP-03 | P0 | 实现章节边界内 passage 与精确血缘验证 | Verify: boundary tests | Gate: zero violations | Parallelizable: No
[x] TP-04 | P0 | 重建真实 14 本 v3 并加质量门禁 | Verify: build/validate/data gate | Gate: deterministic | Parallelizable: No
[x] TP-05 | P0 | 深审、Quick CI、任务和本地版本收口 | Verify: review/CI/task/Git | Gate: PASS | Parallelizable: No

说明：
- 每一行后续必须绑定 `TP-XX(.YY...)`
- 不允许出现无归属 TODO
