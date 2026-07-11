---
id: GATE-0001
type: gate
status: active
owner: engineering
created: 2026-06-15
last_reviewed: 2026-07-12
source: user-revocation-2026-07-12-web-layout-exception
severity: BLOCK
detectability: automated
related_gates:
  - LESSON-0001
---

# GATE-0001 Web HTML 禁止自定义前端样式

## 阻止条件

任一面向 `/web` 或同类工程报表页的 HTML 变更出现以下内容，必须阻止合并或提交：

- 任意 `<style>`、外部 CSS、行内 `style=`。
- 任意 `@media`、响应式布局 CSS、自定义颜色、背景、字体、字号、间距、边框、圆角、阴影。
- 任意视觉布局或美化 `class`、卡片、装饰性容器。
- 无必要语义的 `main`、`section`、`div` 包装。
- 依赖 JavaScript 才能看到核心结果。
- 把 Markdown、JSON、日志或链接改造成不可复制的视觉组件。

当前无布局例外。此前 `/web` 三块工作台授权已于 2026-07-12 被用户撤销。

`/web` 允许使用无 CSS 的原生 `table/thead/tbody/tr/th/td` 表达结构化数据；这是用户明确要求的浏览器语义表格，不是布局或美化例外。

## 原因

FateCat Web 页面不是营销页、SaaS 后台或品牌视觉入口，而是服务端直出的工程语义页面。用户提供的 `/home/lenovo/.codex/Design.md` 明确要求“零美化语义界面”：默认浏览器渲染就是期望效果，页面价值来自稳定字段、原生表单、真实链接、psql ASCII 表格和可审计上下文。

代理曾擅自加入 CSS 和视觉包装，造成项目设计契约偏移。该问题必须以 BLOCK 级 gate 防复发。psql ASCII 表格在浏览器中受中英文后备字体宽度影响而错位，因此 `/web` 使用原生语义表格承载结构化数据。

## 检查方式

- automated: `python -m pytest -q tests/regression/test_web_html.py`
- automated: `bash scripts/local-ci.sh --profile quick`
- manual: 变更 `/web` 前必须读取 `/home/lenovo/.codex/Design.md`
- manual: 审查 `domains/experience-delivery/services/fatecat-delivery/src/web_ui.py` 是否只使用语义 HTML 和服务端直出内容。

当前测试中的硬断言：

```text
assert "style=" not in text
assert "<style" not in text
assert 'rel="stylesheet"' not in text
assert "class=" not in text
assert "<main>" not in text
assert "<section" not in text
assert "<div" not in text
assert "<h1>faetcat</h1>" in text
assert forbidden visual CSS tokens not in text
```

## 可操作错误提示

Web HTML 违反零美化语义界面规范。删除全部 CSS、视觉 class、视觉容器和响应式布局；使用 `h1/h2/p/dl/ul/form/fieldset/pre/code/details/summary/a` 表达信息结构与操作结构。

## 最小修复

- [ ] 删除全部 `<style>`、外部 CSS、`style=`、视觉 class 和 CSS 相关输出。
- [ ] 把视觉容器改成标题、段落、列表、定义列表、表单和 `<pre><code>`。
- [ ] 保留真实链接和原始文本，不添加卡片、圆角、阴影、动画或布局优化。
- [ ] 跑 `python -m pytest -q tests/regression/test_web_html.py`。
- [ ] 跑 `bash scripts/local-ci.sh --profile quick`。
