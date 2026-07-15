# Execution Checklist
[x] TP-01 | P0 | 锁定抓取边界与数据契约 | Verify: 任务 CONTEXT/PLAN 包含截图、robots、sitemap、入口、详情和旧路径实测证据 | Gate: 不存在会改变实现路径的未决范围歧义 | Parallelizable: No
[x] TP-02 | P0 | 建立离线解析与安全回归契约 | Verify: pytest 先出现目标缺失红灯，完成实现后全部转绿 | Gate: 测试不访问公网且覆盖正负边界 | Parallelizable: No
[x] TP-03 | P0 | 实现可恢复全量抓取器 | Verify: 目标 pytest 与 ruff 通过，--help 和 --validate-only 可执行 | Gate: 无无界队列、无静默失败、所有输出限定在显式目录 | Parallelizable: No
[x] TP-04 | P0 | 执行基础与典籍全量抓取 | Verify: 抓取命令正常退出且 manifest 记录 complete 或明确 residual failures | Gate: robots 允许、页面上限未触发、无活动 transient failure | Parallelizable: No
[x] TP-05 | P0 | 审计链接、内容、媒体和失败闭包 | Verify: --validate-only 通过，completeness.json 无未解释 dangling target URL 或 active failure | Gate: 可访问目标与失效/拒绝/失败状态严格区分 | Parallelizable: No
[x] TP-06 | P1 | 同步工具链、架构与版权边界文档 | Verify: 结构检查、governance index 重建与 strict validate 通过 | Gate: 文档描述与实际 CLI、路径和验证证据一致 | Parallelizable: No
[x] TP-07 | P0 | 完成独立审查与任务收口 | Verify: review 无 BLOCK，任务 closeout validator 和 closeout packet 通过 | Gate: 所有叶子完成、Recent Evidence 非空、无活动 blocker | Parallelizable: No
[x] TP-08 | P0 | 固化详情续页漏抓根因与 RED 契约 | Verify: DEBUG.md 通过 hypothesize 校验，新增测试在生产修复前按预期失败 | Gate: 根因由只读最小实验确认，RED 失败原因与 756 页现场证据一致 | Parallelizable: No
[x] TP-09 | P0 | 实现逐页存证与逻辑文章聚合 | Verify: 目标 pytest 与 ruff 全绿，旧数据库可原位迁移，缺页 fixture 被 validator 拒绝 | Gate: 页面与逻辑文章职责分离，1..N 序列有唯一约束和独立门禁，不新增平行真相源 | Parallelizable: No
[x] TP-10 | P0 | 增量补抓并独立审计详情分页闭包 | Verify: 756 个已知续页全部终态，详情页序列缺口为 0，3344 个逻辑文档完整聚合，files.sha256 全部通过 | Gate: 内置 validator 与独立 SQLite/文件审计同时通过，无活动失败或未解释缺口 | Parallelizable: No
[x] TP-11 | P0 | 同步防复发治理并重新审查收口 | Verify: DEBUG conclude、auto-review、任务 closeout、governance strict/health 全部通过 | Gate: 旧 PASS 已被新证据取代，防详情分页假闭包规则进入 owning source，最终无 BLOCK | Parallelizable: No

说明：
- 每一行后续必须绑定 `TP-XX(.YY...)`
- 不允许出现无归属 TODO
