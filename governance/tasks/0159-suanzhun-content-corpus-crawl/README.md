# Task Overview
- Task ID: `0159`
- Slug: `suanzhun-content-corpus-crawl`
- Objective: `完整抓取算准网基础与典籍栏目，交付可追溯、可增量、可重复执行的结构化语料与媒体资产`
- Status: `Done`

## In Scope
- 从 https://www.suanzhun.net/jichu/ 和 https://www.suanzhun.net/dianji/ 递归发现分类、分页、当前详情页、旧层级详情页和目标范围内关联详情页
- 保存 UTF-8 结构化记录、清洗正文 HTML/Markdown、正文媒体、压缩原始响应、URL 到本地文件映射、失败明细和完整性报告
- 实现 robots 遵循、同站限速、超时重试、断点续跑、条件刷新、URL 去重、内容去重、内容哈希与可执行校验
- 实际执行一次全量抓取并审计结果

## Out of Scope
- 绕过登录、验证码、IP 限制、robots.txt 或其他访问控制
- 抓取基础与典籍之外的工具、排盘、名人、黄历或用户数据
- 把未经版权复核的站点全文晋升为生产输入、公开发行物或 canonical classics
- 为提高速度使用无界并发或侵入式浏览器自动化

## Task Package Tree
- ROOT
  ├─ TP-01 [leaf] [P0] 锁定抓取边界与数据契约
  ├─ TP-02 [leaf] [P0] 建立离线解析与安全回归契约
  ├─ TP-03 [leaf] [P0] 实现可恢复全量抓取器
  ├─ TP-04 [leaf] [P0] 执行基础与典籍全量抓取
  ├─ TP-05 [leaf] [P0] 审计链接、内容、媒体和失败闭包
  ├─ TP-06 [leaf] [P1] 同步工具链、架构与版权边界文档
  ├─ TP-07 [leaf] [P0] 完成独立审查与任务收口
  ├─ TP-08 [leaf] [P0] 固化详情续页漏抓根因与 RED 契约
  ├─ TP-09 [leaf] [P0] 实现逐页存证与逻辑文章聚合
  ├─ TP-10 [leaf] [P0] 增量补抓并独立审计详情分页闭包
  └─ TP-11 [leaf] [P0] 同步防复发治理并重新审查收口

## Requirement Alignment
- 目标: 完整抓取算准网基础与典籍栏目，交付可追溯、可增量、可重复执行的结构化语料与媒体资产
- approved plan 顶层步骤数: 11
- 编译后节点总数: 11
- 编译后叶子节点数: 11
- 对齐项: 用户明确要求完整覆盖基础与典籍两栏目、全部分页分类详情、正文资源、噪声清洗、追溯映射、去重重试失败记录和完整性校验
- 对齐项: 两张本地截图已从 /mnt/c/Users/13208/Desktop 读取，确认基础 9 类、典籍 28 类的下拉导航和每页 25 条摘要列表
- 对齐项: 入口页、robots.txt、sitemap.xml、当前详情页和旧层级详情页均已真实访问验证
- 计划摘要: 先锁定边界和离线解析契约，再实现单进程限速、SQLite 可恢复抓取器，随后实际全量运行、交叉审计、同步文档并独立审查。

## Task Package Overview
| Task Package ID | Parent | Depth | Priority | Type | Leaf | Depends On | Wave | Ready | Parallelizable | Objective |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TP-01 | ROOT | 1 | P0 | 分析 | Yes | - | 1 | No | No | 用真实站点证据确定 URL 类型、栏目闭包、正文边界、输出 schema、版权与停止条件 |
| TP-02 | ROOT | 1 | P0 | 测试 | Yes | TP-01 | 2 | No | No | 用最小 fixture 锁定分页发现、详情元数据、正文噪声裁剪、格式和媒体引用行为 |
| TP-03 | ROOT | 1 | P0 | 开发 | Yes | TP-02 | 3 | No | No | 实现 robots/限速/重试/SQLite 状态、递归发现、正文媒体抽取、去重导出和内置校验 |
| TP-04 | ROOT | 1 | P0 | 数据 | Yes | TP-03 | 4 | No | No | 在有界速率下实际跑完页面和媒体闭包并持续写入可恢复状态 |
| TP-05 | ROOT | 1 | P0 | 验收 | Yes | TP-04 | 5 | No | No | 交叉核对导航、分页、详情、sitemap、内容哈希、文件哈希和失败终态，证明覆盖边界 |
| TP-06 | ROOT | 1 | P1 | 文档 | Yes | TP-05 | 6 | No | No | 更新脚本与测试目录说明、治理工具入口和任务证据，明确本地输出与分发边界 |
| TP-07 | ROOT | 1 | P0 | 审查 | Yes | TP-06 | 7 | No | No | 按 correctness/security/reliability/performance/architecture/document lenses 审查并生成可复核 closeout |
| TP-08 | ROOT | 1 | P0 | 调试 | Yes | TP-07 | 8 | No | No | 把续页分类失明、假通过和元数据污染固化为可复现根因与 RED 契约 |
| TP-09 | ROOT | 1 | P0 | 开发 | Yes | TP-08 | 9 | No | No | 在单一 SQLite 真相源内实现逐页存证、逻辑聚合、原位迁移和独立门禁 |
| TP-10 | ROOT | 1 | P0 | 数据 | Yes | TP-09 | 10 | No | No | 恢复旧原始响应中的分页发现，增量补抓并独立审计完整闭包 |
| TP-11 | ROOT | 1 | P0 | 审查 | Yes | TP-10 | 11 | No | No | 同步防复发门禁，替换旧假 PASS 证据并重新 closeout |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
8. DEBUG.md
9. REVIEW.md
