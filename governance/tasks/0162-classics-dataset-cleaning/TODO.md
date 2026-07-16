# Execution Checklist
[x] TP-01 | P0 | 定义清洗数据契约、范围和版权边界 | Verify: JSON parse + task docs | Gate: no overclaim | Parallelizable: No
[x] TP-02 | P0 | 实现确定性典籍清洗与切片工具 | Verify: CLI fixture run | Gate: deterministic manifest | Parallelizable: No
[x] TP-03 | P0 | 添加回归测试并同步 README/AGENTS | Verify: focused pytest | Gate: docs drift closed | Parallelizable: No
[x] TP-04 | P0 | 生成 14 本本地清洗数据集 | Verify: quality report | Gate: 14 documents, zero lineage errors | Parallelizable: No
[x] TP-05 | P0 | 执行 review、quick CI 与版本控制收口 | Verify: diff/CI/task validation | Gate: review PASS | Parallelizable: No

说明：
- 每一行后续必须绑定 `TP-XX(.YY...)`
- 不允许出现无归属 TODO
