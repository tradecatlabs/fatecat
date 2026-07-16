# Execution Checklist
[x] TP-01 | P0 | 建立公开报告字段允许契约 | Verify: 公开报告契约测试与多样本回归通过 | Gate: 公开输出只含允许字段，结构化证据无损 | Parallelizable: No
[x] TP-02 | P0 | 优化完整八字冷启动热路径 | Verify: 冷/热 benchmark 与结果等价测试 | Gate: 月份数量和语义完全一致，冷启动获得稳定收益 | Parallelizable: No
[x] TP-03 | P0 | 建立独立准确性评测入口 | Verify: 独立 runner schema/source/failure tests | Gate: 不能用自产 fixture 通过独立门禁，缺专家证据时状态明确 pending | Parallelizable: Yes
[x] TP-04 | P0 | 统一 capability 生命周期语义 | Verify: registry schema 与 executor/API 契约测试 | Gate: planned 拒绝执行，validated 不再被误报 production | Parallelizable: Yes
[x] TP-05 | P1 | 收敛核心与报告职责复杂度 | Verify: 行为快照、复杂度检查和定向回归 | Gate: 职责边界清晰，未新增无消费者抽象 | Parallelizable: No
[x] TP-06 | P0 | 补齐异步报告端到端指标 | Verify: report job lifecycle metrics tests 与 /metrics smoke | Gate: 固定低基数标签覆盖全部终态 | Parallelizable: Yes
[x] TP-07 | P0 | 建立许可证安全的公开客户端闭包 | Verify: clean-room install/smoke + archive content inspection + restricted gate negative test | Gate: 公开闭包无未知许可证资产且仍可调用生产 API | Parallelizable: Yes
[x] TP-08 | P0 | 全量验证、审查与仓库卫生收口 | Verify: quick CI + governance/task strict + auto-review + git status | Gate: 无 BLOCK、无未解释失败、无未提交文件 | Parallelizable: No

说明：
- 每一行后续必须绑定 `TP-XX(.YY...)`
- 不允许出现无归属 TODO
