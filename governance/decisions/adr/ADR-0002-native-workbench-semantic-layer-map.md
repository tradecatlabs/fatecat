# ADR-0002: FateCat Web Native Workbench Shell

- 状态：`candidate`
- 日期：2026-08-21
- 产品：FateCat `/web`
- 基线回滚点：`pre-native-workbench-fatecat-20260821`
- 前置 ADR：`ADR-0001-native-workbench-compatibility-profile.md`

## 决策

在不改变 FateCat 动态服务模型、报告协议和核心内容直出的前提下，落实三层工作台结构：

```text
Top    #top-layer：原生 Emoji 开关，z-index 3
Middle #control-plane：项目说明与参数表单，z-index 2，宽度 clamp(320px, 28vw, 440px)
Bottom #data-plane：报告状态、错误、Markdown 输出和工作台结果，z-index 1
```

页面使用 `div#workspace`、`div#top-layer`、`aside#control-plane`、`main#data-plane` 和 `data-sidebar` 表达结构；各层同时使用 `data-layer` / `data-workbench-layer` 作为机器可审计标记。`<style>` 只包含 GATE-0001 白名单中的结构 CSS；无 CSS/JavaScript 时核心表单和报告仍按源代码顺序直接可见。

## 保留不变量

- 保留 `/web`、`POST /api/v1/report/jobs/web`、job 状态轮询和 Markdown 输出协议。
- 保留服务端校验、无 JavaScript fallback、原生 form/fieldset/input/select/button、`pre/code` 和现有元素 ID。
- 不把报告计算搬到浏览器，不新增第二数据源，不改变任何报告字段、数据库或任务 TTL。
- 允许且仅允许登记的绝对定位控制面、z-index `3/2/1`、系统 `Canvas` 背景和窄屏宽度适配；不引入静态产品的业务 renderer、数据模型或共享运行时。
- `sidebar-toggle` 只更新 `data-sidebar` 和 ARIA 状态，不隐藏核心内容的唯一入口，不改变报告协议。

## 验收

```bash
bash scripts/local-ci.sh --profile quick
```

`tests/regression/test_web_html.py` 必须验证固定三层 id、z-index 顺序、控制面宽度声明、零品牌美化规则、无 CSS fallback、表单提交入口、异步 job 入口、失败状态和 Markdown 复制入口；既有服务契约测试继续运行。

## 回滚

候选失败时使用普通 `git revert <adoption-commit>`，或在隔离 worktree 回到 `pre-native-workbench-fatecat-20260821`。禁止 `reset --hard`、`clean`、覆盖并行 worktree 或部署生产。
