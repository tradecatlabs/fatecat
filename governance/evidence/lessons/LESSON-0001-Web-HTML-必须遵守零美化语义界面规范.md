---
id: LESSON-0001
type: record
status: current
owner: engineering
created: 2026-06-15
last_reviewed: 2026-07-12
source: user-correction-2026-06-15-web-css-regression
related_gates:
  - GATE-0001
---

# LESSON-0001 Web HTML 必须遵守零美化语义界面规范

## 背景

2026-06-15 的 Web 页面改动中，代理在 `/web` 页面加入了自定义 CSS、响应式布局、颜色、边框、圆角、视觉 class 和包装容器。该行为违背了用户提供的 `/home/lenovo/.codex/Design.md`：FateCat Web 页面应是“零美化语义界面”，只允许信息结构和操作结构设计，不允许视觉美化设计。

这不是风格偏好问题，而是项目界面契约被破坏：页面应依赖浏览器默认渲染，用服务端直出的语义 HTML 暴露表单、链接、psql ASCII 表格、Markdown 和机器可读片段。

## 决策或结论

FateCat `/web` 和同类工程报表页必须遵守零美化语义界面规范：

- 禁止 `<style>`、外部 CSS、行内 `style`；当前不存在授权例外。
- 禁止自定义颜色、背景、字体、间距、圆角、阴影、卡片、响应式布局优化。
- 禁止仅用于视觉的 `class`、视觉容器、卡片包装、装饰性分组。
- 禁止把普通链接伪装成按钮，或把按钮用于普通跳转。
- 允许使用原生语义结构：`h1-h6`、`p`、`dl`、`ul/ol/li`、`nav`、`form/fieldset/legend/label/input/select/button`、`pre/code`、`details/summary`。
- 允许 JavaScript 仅用于复制 Markdown 等渐进增强；核心内容必须服务端直出且无脚本可读。
- 所有结构化数据必须优先用 `tabulate(tablefmt="psql")` 输出到 `<pre><code>`。

2026-07-12 用户明确撤销此前 `/web` 三块工作台布局授权。自此 `/web` 与其他 HTML 页面统一执行无例外的零美化语义界面规则。

## 证据

- 设计真相源：`/home/lenovo/.codex/Design.md`
- 修复提交：`d66a9d8 fix: restore semantic web html`
- 机械回归：`tests/regression/test_web_html.py::assert_zero_beauty_semantic_html`
- 本地验证：`bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-design-postcommit`
- 实际页面扫描必须确认 `<style>`、`style=`、外部 CSS、`class=`、`@media`、`main`、`section` 和无必要 `div` 均不存在。

## 影响范围

直接影响：

- `domains/experience-delivery/services/fatecat-delivery/src/web_ui.py`
- `tests/regression/test_web_html.py`
- 任何未来新增的 HTML 优先工程报表页、状态页、调试页、工具页和服务端直出页面。

不影响：

- API JSON 契约。
- Telegram Bot 输出。
- Markdown 报告内容本身。
- 必要的复制按钮渐进增强脚本。

## 后续动作

- [x] 删除 `/web` 自定义 CSS、视觉 class、`main` 和 `section` 包装。
- [x] 将 TradeCat Labs 项目归属改为 `h2 + p + ul/li/a` 语义结构。
- [x] 在 Web 回归测试中加入零美化禁用项断言。
- [x] 新增架构门禁 `GATE-0001`。
- [x] 新增模块上下文，声明 `web_ui.py` 的单一真相源和禁止事项。
- [ ] 后续任何 Web HTML 变更必须先读取 `/home/lenovo/.codex/Design.md` 和 `GATE-0001`。
