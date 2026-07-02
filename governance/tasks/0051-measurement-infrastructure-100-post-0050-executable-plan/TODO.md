# Execution Checklist

[x] TP-01.01 | P0 | 读取路线图、任务索引、0050 状态和未提交 diff | Verify: `git status` and file reads | Gate: 不覆盖既有 0050 事实 | Parallelizable: Yes
[x] TP-02.01 | P0 | 查询并归纳成熟 infra 同构资料 | Verify: official source URLs in roadmap | Gate: 不使用二手猜测替代官方依据 | Parallelizable: Yes
[x] TP-03.01 | P0 | 更新主路线图 post-0050 实现计划 | Verify: `rg "0.6"` | Gate: 不宣称 100% 已完成 | Parallelizable: No
[x] TP-03.02 | P0 | 新建 0051 任务包并同步任务索引 | Verify: task docs exist | Gate: 不创建平行路线图 | Parallelizable: No
[x] TP-04.01 | P0 | 运行任务校验并记录结果 | Verify: validators + diff check | Gate: 文档口径一致 | Parallelizable: No

说明：
- 每一行后续必须绑定 `TP-XX(.YY...)`。
- 本任务只做计划与治理落盘，不实现业务功能。
