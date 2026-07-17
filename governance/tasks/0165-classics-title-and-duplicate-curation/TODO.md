# Execution Checklist
[x] TP-01 | P0 | 建立 title/duplicate/review 摘要契约与 red tests | Verify: focused tests | Gate: red reproduced | Parallelizable: No
[x] TP-02 | P0 | 修复 document_title 唯一性和重复书名边界 | Verify: focused tests | Gate: title <=1 | Parallelizable: No
[x] TP-03 | P0 | 实现重复关系分类与复核聚合 | Verify: focused tests | Gate: recomputable | Parallelizable: No
[x] TP-04 | P0 | 重建真实 14 本并强化 validator/data gate | Verify: build/validate/gate/hash | Gate: PASS | Parallelizable: No
[x] TP-05 | P0 | 深审、Quick CI、任务与本地版本收口 | Verify: review/CI/task/Git | Gate: PASS | Parallelizable: No

说明：
- 每一行后续必须绑定 `TP-XX(.YY...)`
- 不允许出现无归属 TODO
