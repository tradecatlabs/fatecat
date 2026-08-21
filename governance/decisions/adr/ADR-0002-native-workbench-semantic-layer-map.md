# ADR-0002: FateCat Web Semantic Workbench Layer Map

- 状态：`candidate`
- 日期：2026-08-21
- 产品：FateCat `/web`
- 基线回滚点：`pre-native-workbench-fatecat-20260821`
- 前置 ADR：`ADR-0001-native-workbench-compatibility-profile.md`

## 决策

在不改变 FateCat 动态服务模型和零美化语义 HTML 的前提下，登记三层职责：

```text
Top    项目说明与原生链接导航
Middle 原生表单输入与服务端输入契约
Bottom 报告状态、错误、Markdown 输出和工作台结果
```

页面使用 `data-workbench-profile="tradecatlabs.native-workbench.v0.1.compatibility"` 和 `data-layer` / `data-workbench-layer` 作为机器可审计标记。标记不引入 CSS、class、style、定位、颜色、组件库或客户端框架。

## 保留不变量

- 保留 `/web`、`POST /api/v1/report/jobs/web`、job 状态轮询和 Markdown 输出协议。
- 保留服务端校验、无 JavaScript fallback、原生 form/fieldset/input/select/button、`pre/code` 和现有元素 ID。
- 不把报告计算搬到浏览器，不新增第二数据源，不改变任何报告字段、数据库或任务 TTL。
- 不将静态产品的绝对定位控制面或 z-index 规则套入 FateCat。

## 验收

```bash
bash scripts/local-ci.sh --profile quick
```

`tests/regression/test_web_html.py` 必须验证 Top/Middle/Bottom 标记、零美化规则、表单提交入口、异步 job 入口、失败状态和 Markdown 复制入口；既有服务契约测试继续运行。

## 回滚

候选失败时使用普通 `git revert <adoption-commit>`，或在隔离 worktree 回到 `pre-native-workbench-fatecat-20260821`。禁止 `reset --hard`、`clean`、覆盖并行 worktree 或部署生产。
