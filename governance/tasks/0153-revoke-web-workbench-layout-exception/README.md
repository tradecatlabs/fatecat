# Task Overview
- Task ID: `0153`
- Slug: `revoke-web-workbench-layout-exception`
- Objective: `撤销 /web 黄金三块工作台布局授权，恢复严格零美化语义 HTML，并同步实现、测试与治理真相源`
- Status: `Done`

## In Scope
- 删除 `/web` 的全部 CSS、视觉 class、三块工作台布局和无必要布局容器。
- 保留 GET 表单、异步任务、服务端报告、Markdown 复制、八字/紫微工作台与隐私规则。
- 将 Web 回归门禁改为无例外零美化断言。
- 同步根与 delivery 的 AGENTS/README、标准、Gate、lesson、agent feedback、module context 和任务级 lesson。

## Out of Scope
- 不改变命理计算、capability、Markdown 报告结构、API 路径、Bot 或任务队列语义。
- 不新增前端框架、模板引擎、CSS、组件库或视觉资产。
- 不改写已完成历史任务包；历史记录只在当前 DEBUG 中标明授权已撤销。
- 不提交或推送；版本控制由用户后续明确指令触发。

## Task Package Tree
- ROOT
  - TP-01：删除布局例外并恢复语义 HTML
  - TP-02：同步测试与长期真相源
  - TP-03：执行验证、审查和 closeout

## Requirement Alignment
- 用户最新指令明确撤销此前三块工作台布局授权。
- 最新指令覆盖 2026-06-15 的历史授权，当前目标是严格执行 `/home/lenovo/.codex/Design.md`。
- 采用净删除方案，不建立兼容开关或双轨页面。

## Task Package Overview
| Task Package ID | Parent | Priority | Type | Depends On | Objective |
| --- | --- | --- | --- | --- | --- |
| TP-01 | ROOT | P0 | refactor | - | 删除 CSS、视觉 class、布局容器并保留 Web 行为。 |
| TP-02 | ROOT | P0 | governance | TP-01 | 更新回归测试和所有当前真相源。 |
| TP-03 | ROOT | P0 | verification | TP-02 | 执行测试、治理校验、quick CI 与独立审查。 |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
