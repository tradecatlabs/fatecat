# Acceptance Checklist

# Global Standards
- [x] 所有文本 UTF-8，JSON 使用稳定字段名，URL canonicalization 不丢失语义路径
- [x] 所有网络请求有超时、有限重试、指数退避、限速和可观察日志
- [x] 抓取输出写入 Git 忽略的本地 exports，版权状态标记 review_required/reference_only/distribution_not_allowed
- [x] 不以 404 stale sitemap 条目冒充抓取故障，也不吞掉 5xx、解析失败或媒体失败

# Task Package Checklists
## TP-01
- 标题: 锁定抓取边界与数据契约
- 验收项:
  - [x] 三源发现策略和目标范围过滤规则明确
  - [x] 缺失字段和不可访问 URL 的处理明确
- Verify: 任务 CONTEXT/PLAN 包含截图、robots、sitemap、入口、详情和旧路径实测证据
- Gate: 不存在会改变实现路径的未决范围歧义
- 输出物:
  - [x] 稳定抓取规格
  - [x] URL/字段/输出契约
  - [x] 风险与停止条件
- 标准清单:
  - [x] Verify: 任务 CONTEXT/PLAN 包含截图、robots、sitemap、入口、详情和旧路径实测证据
  - [x] Gate: 不存在会改变实现路径的未决范围歧义
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

## TP-02
- 标题: 建立离线解析与安全回归契约
- 验收项:
  - [x] 覆盖 URL canonicalization、scope、metadata、body、noise、links、media 和 filename
- Verify: pytest 先出现目标缺失红灯，完成实现后全部转绿
- Gate: 测试不访问公网且覆盖正负边界
- 输出物:
  - [x] tests/regression/test_suanzhun_corpus_crawl.py
- 标准清单:
  - [x] Verify: pytest 先出现目标缺失红灯，完成实现后全部转绿
  - [x] Gate: 测试不访问公网且覆盖正负边界
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检
  - [x] 维护 `DEBUG.md` 并保留回归证据

## TP-03
- 标题: 实现可恢复全量抓取器
- 验收项:
  - [x] 支持断点续跑和增量刷新
  - [x] 保存原始响应与规范化输出
  - [x] 生成机器可读失败和完整性报告
- Verify: 目标 pytest 与 ruff 通过，--help 和 --validate-only 可执行
- Gate: 无无界队列、无静默失败、所有输出限定在显式目录
- 输出物:
  - [x] scripts/suanzhun-corpus-crawl.py
- 标准清单:
  - [x] Verify: 目标 pytest 与 ruff 通过，--help 和 --validate-only 可执行
  - [x] Gate: 无无界队列、无静默失败、所有输出限定在显式目录
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

## TP-04
- 标题: 执行基础与典籍全量抓取
- 验收项:
  - [x] 入口、分类、分页、详情和正文媒体均有映射
  - [x] 中断后原命令可续跑
- Verify: 抓取命令正常退出且 manifest 记录 complete 或明确 residual failures
- Gate: robots 允许、页面上限未触发、无活动 transient failure
- 输出物:
  - [x] infra/runtime/local-state/exports/suanzhun-corpus
- 标准清单:
  - [x] Verify: 抓取命令正常退出且 manifest 记录 complete 或明确 residual failures
  - [x] Gate: robots 允许、页面上限未触发、无活动 transient failure
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

## TP-05
- 标题: 审计链接、内容、媒体和失败闭包
- 验收项:
  - [x] 所有 record/file 引用存在且 hash 匹配
  - [x] URL 和内容重复均有 alias 记录
  - [x] sitemap 差异有解释
- Verify: --validate-only 通过，completeness.json 无未解释 dangling target URL 或 active failure
- Gate: 可访问目标与失效/拒绝/失败状态严格区分
- 输出物:
  - [x] 完整性报告
  - [x] 重复组
  - [x] 失败与不可用明细
  - [x] 文件 sha256 清单
- 标准清单:
  - [x] Verify: --validate-only 通过，completeness.json 无未解释 dangling target URL 或 active failure
  - [x] Gate: 可访问目标与失效/拒绝/失败状态严格区分
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

## TP-06
- 标题: 同步工具链、架构与版权边界文档
- 验收项:
  - [x] Operating model: not needed 有具体理由
  - [x] Toolchain/process/source-of-truth 影响有 owner 与证据
  - [x] 版权边界明确
- Verify: 结构检查、governance index 重建与 strict validate 通过
- Gate: 文档描述与实际 CLI、路径和验证证据一致
- 输出物:
  - [x] AGENTS/治理/任务文档更新
- 标准清单:
  - [x] Verify: 结构检查、governance index 重建与 strict validate 通过
  - [x] Gate: 文档描述与实际 CLI、路径和验证证据一致
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

## TP-07
- 标题: 完成独立审查与任务收口
- 验收项:
  - [x] 发现的问题已修或明确阻塞
  - [x] 效率检查含复杂度、瓶颈、验证指标和权衡
  - [x] 用户可按命令复跑
- Verify: review 无 BLOCK，任务 closeout validator 和 closeout packet 通过
- Gate: 所有叶子完成、Recent Evidence 非空、无活动 blocker
- 输出物:
  - [x] REVIEW 结论
  - [x] 任务 closeout packet
  - [x] 最终交付摘要
- 标准清单:
  - [x] Verify: review 无 BLOCK，任务 closeout validator 和 closeout packet 通过
  - [x] Gate: 所有叶子完成、Recent Evidence 非空、无活动 blocker
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
  - [x] 交付前完成 REVIEW / SHIP 自检

## TP-08
- 标题: 固化详情续页漏抓根因与 RED 契约
- Verify: DEBUG.md 通过 hypothesize 校验，新增测试在修复前按预期失败
- Gate: 根因由只读最小实验确认，RED 与 756 页现场证据一致
- 验收项:
  - [x] 三条可证伪假设与最小实验落盘
  - [x] 当前/旧式续页、隐藏页、聚合、作者隔离和缺页门禁产生预期 RED
- 输出物:
  - [x] DEBUG.md
  - [x] RED 回归证据
- 标准清单:
  - [x] DEBUG hypothesize validator 通过
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`

## TP-09
- 标题: 实现逐页存证与逻辑文章聚合
- Verify: 目标 pytest 与 ruff 全绿，v1 可原位迁移，缺页 fixture 被 validator 拒绝
- Gate: 页面与逻辑文章职责分离，`1..N` 有唯一约束和独立门禁
- 验收项:
  - [x] 物理页身份和 `1..N` 唯一约束
  - [x] v1 原位迁移、逻辑文章有序聚合与 metadata 隔离
  - [x] validator 独立拒绝缺页和原始 href 漏入 frontier
- 输出物:
  - [x] v2 抓取器
  - [x] 15 项离线回归
- 标准清单:
  - [x] 目标 pytest 与 ruff 通过
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`

## TP-10
- 标题: 增量补抓并独立审计详情分页闭包
- Verify: 756 个续页全部终态，序列缺口为 0，3344 篇逻辑文档完整，校验和通过
- Gate: 内置 validator 与独立 SQLite/文件审计同时通过
- 验收项:
  - [x] 756 个详情续页全部完成
  - [x] 4100 个物理详情页映射为 3344 篇逻辑文章
  - [x] 页序列、聚合正文、来源映射、作者污染和文件哈希均无缺口
- 输出物:
  - [x] 更新后的本地语料
  - [x] completeness、manifest、失败/不可用明细与 files.sha256
- 标准清单:
  - [x] 内置 validator 与独立审计同时通过
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`

## TP-11
- 标题: 同步防复发治理并重新审查收口
- Verify: DEBUG conclude、auto-review、任务 closeout、governance strict/health 全部通过
- Gate: 旧 PASS 已被新证据取代，防假闭包规则进入 owning source，最终无 BLOCK
- 验收项:
  - [x] BLOCK 级共因失明 Gate 落盘
  - [x] 旧 REVIEW 和 closeout 由新证据替换
  - [x] DEBUG conclude、governance、review 与 task closeout 通过
- 输出物:
  - [x] Gate、AUDIT_CASE_SAMPLING、REVIEW、TASK_CLOSEOUT_PACKET
- 标准清单:
  - [x] 无 BLOCK finding 或活动 blocker
  - [x] 完成后更新 `STATUS.md` 的 `Recent Evidence`
