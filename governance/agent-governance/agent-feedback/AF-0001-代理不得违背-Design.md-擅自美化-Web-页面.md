---
id: AF-0001
type: record
status: converted
owner: engineering
created: 2026-06-15
last_reviewed: 2026-07-12
source: user-correction-2026-06-15-web-css-regression
related_gates:
  - GATE-0001
---

# AF-0001 代理不得违背 Design.md 擅自美化 Web 页面

## 反馈来源

用户在 2026-06-15 明确指出：此前代理违背其前端设计要求，擅自为 `/web` 加入过多 CSS、样式和效果。用户要求把这次问题写入记忆文件和相关治理位置，确保不再复发。

## 代理失败模式

失败模式：

- 未先读取用户指定的 `/home/lenovo/.codex/Design.md` 即按一般前端审美补样式。
- 把“公共入口可读性”错误理解成“增加 CSS/视觉包装”。
- 在原本应为工程语义页面的 `/web` 中加入颜色、边框、圆角、响应式布局和视觉 class。
- 没有把用户既有设计原则作为更高优先级的项目契约。

## 期望行为

后续代理处理 FateCat Web 页面时必须：

- 先读取 `/home/lenovo/.codex/Design.md`。
- 禁止未登记 CSS、视觉 class、品牌视觉布局和卡片包装；2026-08-21 新授权仅限 GATE-0001 的三层结构几何例外。
- 只做信息结构、操作结构和可审计数据结构。
- 用测试或 `rg` 证明没有禁用项。
- 如需偏离零美化语义界面，必须先得到用户新的明确许可，并记录原因、结构白名单和回滚路径；2026-08-21 的授权已登记在 GATE-0001、ADR-0001/0002 和工作台候选标签中，不得扩展为视觉美化。

## 处理状态

resolved

## 转化结果

- [x] lesson: `governance/evidence/lessons/LESSON-0001-Web-HTML-必须遵守零美化语义界面规范.md`
- [x] gate: `governance/architecture-gates/rules/GATE-0001-Web-HTML-禁止自定义前端样式.md`
- [x] module context: `governance/context/module-contexts/domains-experience-delivery-services-fatecat-delivery-src-web-ui-py/CONTEXT.md`
- [x] regression: `tests/regression/test_web_html.py::assert_zero_beauty_semantic_html`
