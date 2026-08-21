# ADR-0001: FateCat Web Native Workbench Compatibility Profile

- 状态：`accepted-as-compatibility-profile`
- 日期：2026-08-21
- 产品：FateCat `/web`
- 基线：`c82b58a`

## 背景

FateCat `/web` 是动态 FastAPI 交付页，不是静态产品。页面必须保留服务端表单校验、异步报告任务、API 轮询和 Markdown 输出；同时零美化语义规范仍禁止品牌视觉、组件库、卡片、圆角、阴影、动画和装饰。

用户现已重新授权一个窄范围结构例外：允许使用原生 HTML/CSS 实现三层工作台的覆盖关系，但不得改变服务端直出、无 CSS fallback、报告协议或动态 API 边界。

## 决策

FateCat 采用兼容性 profile，不登记为根模板 renderer 的直接 adopted 产品；但 `/web` 落地结构性三层工作台：

```text
Top    #top-layer：Emoji 开关，z-index 3
Middle #control-plane：项目说明与原生表单，z-index 2，宽度 clamp(320px, 28vw, 440px)
Bottom #data-plane：报告状态、Markdown 输出和工作台结果，z-index 1
```

例外只允许 GATE-0001 白名单中的结构 CSS、系统 `Canvas` 背景、原生开关和必要窄屏宽度适配；不得加入品牌视觉或客户端渲染核心数据。无 CSS 时页面仍按源代码顺序完整可读。

## 保留边界

- `web_report_service.py`、`web_forms.py` 和服务端校验逻辑不变。
- `/api/v1/report/jobs/web`、异步 job 状态和 Markdown 输出协议不变。
- 现有元素 ID、原生表单、`pre/code` 输出和回归测试不删除。
- 不引入 React、Next.js、组件库或共享工作台运行时。
- 不修改 Hugging Face Space 部署入口、域名或 secrets。
- 控制面开关只改变 `data-sidebar` 显示状态，不改变 `#data-plane` 几何或报告内容。

## 开始条件

源代码变化前必须先补充：

1. `tests/regression/test_web_html.py` 的 Top/Control/Report 语义边界断言。
2. 表单提交、异步任务、失败状态和 Markdown 复制的浏览器回归。
3. 与 `GATE-0001` 结构性工作台例外和零美化核心内容标准一致的契约更新。
4. 独立提交和可回滚标签；不覆盖并行工作树。

## 验证

```bash
bash scripts/local-ci.sh --profile quick
```

该 ADR 不授权生产部署；发布仍需项目既有 `hf-space-deploy` 门禁和明确授权。
