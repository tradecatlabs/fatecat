# ADR-0001: FateCat Web Native Workbench Compatibility Profile

- 状态：`accepted-as-compatibility-profile`
- 日期：2026-08-21
- 产品：FateCat `/web`
- 基线：`c82b58a`

## 背景

FateCat `/web` 是动态 FastAPI 交付页，不是静态产品。项目自身的零美化语义界面门禁禁止 CSS、`class`、style 属性和视觉组件；页面还必须保留服务端表单校验、异步报告任务、API 轮询和 Markdown 输出。

因此不能直接套用静态工作台的绝对定位覆盖层，也不能删除 API 或把报告变成静态 JSON。

## 决策

FateCat 采用兼容性 profile，不登记为根模板的直接 adopted 产品：

```text
Top    页面与项目说明、原生导航、状态提示
Middle 原生表单参数控件与服务端输入契约
Bottom 报告状态、Markdown 输出、工作台结果文本
```

三层是语义职责边界，不增加 CSS、视觉 class、定位、颜色、圆角、卡片或新的客户端框架。现有 `/web` 的原生 HTML 结构和 API 行为优先级更高。

## 保留边界

- `web_report_service.py`、`web_forms.py` 和服务端校验逻辑不变。
- `/api/v1/report/jobs/web`、异步 job 状态和 Markdown 输出协议不变。
- 现有元素 ID、原生表单、`pre/code` 输出和回归测试不删除。
- 不引入 React、Next.js、组件库或共享工作台运行时。
- 不修改 Hugging Face Space 部署入口、域名或 secrets。

## 开始条件

源代码变化前必须先补充：

1. `tests/regression/test_web_html.py` 的 Top/Control/Report 语义边界断言。
2. 表单提交、异步任务、失败状态和 Markdown 复制的浏览器回归。
3. 与 `GATE-0001` 零美化语义 HTML 标准一致的契约更新。
4. 独立提交和可回滚标签；不覆盖并行工作树。

## 验证

```bash
bash scripts/local-ci.sh --profile quick
```

该 ADR 不授权生产部署；发布仍需项目既有 `hf-space-deploy` 门禁和明确授权。
