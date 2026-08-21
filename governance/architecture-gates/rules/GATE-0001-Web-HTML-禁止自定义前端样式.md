---
id: GATE-0001
type: gate
status: active
owner: engineering
created: 2026-06-15
last_reviewed: 2026-08-21
source: user-authorization-2026-08-21-workbench-structure-exception
severity: BLOCK
detectability: automated
related_gates:
  - LESSON-0001
---

# GATE-0001 Web HTML 零美化与工作台结构例外

## 阻止条件

任一面向 `/web` 或同类工程报表页的 HTML 变更出现以下内容，必须阻止合并或提交：

- 外部 CSS、行内 `style=`、视觉 class、品牌颜色、品牌字体、圆角、阴影、动画、卡片或装饰性组件。
- 任何不在 FateCat 工作台白名单内的 `<style>` 规则、布局规则或响应式规则。
- 依赖 JavaScript 才能看到核心表单、报告、错误、Markdown 或原始数据。
- 把 psql ASCII 表格、Markdown、JSON、日志或链接改造成不可复制的视觉组件。
- 通过控制面开关隐藏核心内容的唯一入口、改变报告协议或改变异步 API 行为。

## FateCat 工作台结构白名单

用户于 2026-08-21 重新授权一个窄范围结构例外。`GET /web` 只能使用以下结构：

```text
#workspace       工作台根节点，data-sidebar=expanded|collapsed
#top-layer       z-index: 3，只承载功能性 Emoji 开关
#control-plane   z-index: 2，覆盖层宽度 clamp(320px, 28vw, 440px)
#data-plane      z-index: 1，全屏报告数据面
```

允许的 `<style>` 规则只包括：

- `html` / `body` / `#workspace` 的全屏、溢出和隔离设置。
- `#top-layer`、`#sidebar-toggle`、`#control-plane`、`#data-plane` 的定位、层级、宽度、padding、overflow、display、box-sizing 和系统 `Canvas` 背景。
- `#workspace[data-sidebar="collapsed"] #control-plane` 的显示切换。
- `#report-content` 的最大宽度、居中、在控制面展开时向可见数据区偏移，以及内部 `pre` 的有界溢出。
- 只把 `#control-plane` 在窄屏设为 `width: 100%`、并将报告内容恢复为窄屏全宽的 `@media` 规则。

不得把该例外扩展为主题、视觉设计系统、品牌组件或隐藏核心信息。关闭 CSS 后，页面必须按源代码顺序完整可读；关闭 JavaScript 后，原生表单和服务端报告入口仍必须可用。

## 原因

FateCat Web 页面仍是服务端直出的工程语义页面。工作台例外只表达控制面、数据面和功能性开关的几何职责；页面价值仍来自稳定字段、原生表单、真实链接、psql ASCII 表格和可审计上下文。

## 检查方式

- automated: `python -m pytest -q tests/regression/test_web_html.py`
- automated: `bash scripts/local-ci.sh --profile quick`
- manual: 变更 `/web` 前必须读取 `/home/lenovo/.codex/Design.md`
- manual: 审查 `domains/experience-delivery/services/fatecat-delivery/src/web_ui.py` 是否只使用结构白名单 CSS，且保留服务端直出内容。

当前测试中的硬断言：

```text
assert 'id="workspace" data-sidebar="expanded"' in text
assert 'id="top-layer" data-layer="top"' in text
assert 'id="control-plane" data-layer="middle"' in text
assert 'id="data-plane" data-layer="bottom"' in text
assert 'z-index: 3' in text
assert 'z-index: 2' in text
assert 'z-index: 1' in text
assert 'width: clamp(320px, 28vw, 440px)' in text
assert visual-decoration-tokens not in text
assert core-form-and-report-remain-readable without CSS/JavaScript
```

## 可操作错误提示

Web HTML 违反 GATE-0001。保留服务端直出、原生表单、真实链接、psql ASCII 文本和 Markdown；若使用工作台例外，只能使用登记的三层 id、z-index、覆盖宽度、系统背景和功能性开关，不得加入品牌视觉或隐藏核心内容。

## 最小修复

- [ ] 删除白名单之外的 CSS、`style=`、视觉 class、品牌视觉和装饰性组件。
- [ ] 确认 `#top-layer` / `#control-plane` / `#data-plane` 与 `data-layer` / `data-workbench-layer` 同时存在。
- [ ] 确认 z-index 为 `3/2/1`、控制面宽度为 `clamp(320px, 28vw, 440px)`。
- [ ] 确认 CSS/JavaScript 关闭后核心表单、报告、错误和原始数据仍可读。
- [ ] 跑 `python -m pytest -q tests/regression/test_web_html.py`。
- [ ] 跑 `bash scripts/local-ci.sh --profile quick`。
