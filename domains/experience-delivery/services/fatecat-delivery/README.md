# fatecat-delivery

FateCat 交付服务，负责把纯分析与独立 capability 结果输出到 Web、API、Telegram 和 Markdown 报告。

## 当前状态

- Lifecycle: `active-canonical`
- 当前源码根：`domains/experience-delivery/services/fatecat-delivery/src/`
- 运行资产：`contracts/fate/`、`infra/environments/local/`、`tools/reference-repos/`

## 验证入口

```bash
python -m pytest -q domains/experience-delivery/services/fatecat-delivery/tests
bash scripts/preflight.sh --mode delivery --bootstrap --pretty
bash scripts/delivery-smoke.sh --target api
bash scripts/delivery-smoke.sh --target bot
```

## 维护原则

- 不改变 API 路径和响应模型。
- 不改变 Web 表单语义和 Markdown 输出边界。
- 公开 Web 工作台默认走进程内有界异步任务队列；免费 Space 不保存任务到数据库，多副本生产需要 Redis/RQ/Celery 等外部队列。
- Telegram Webhook 是 FastAPI 内嵌的可选 DeliverySurface，复用 `src/bot.py` 的 Application 与 handler，不拥有或复制测算逻辑。
- Webhook 只负责鉴权、反序列化、去重和有界入队；启用时必须配置 token、secret 与固定 HTTPS URL，默认关闭。
- 不把未来 capability 混入默认综合八字报告。
- Web HTML 必须遵守 `/home/lenovo/.codex/Design.md` 的零美化语义界面规范：禁止 CSS、视觉 class、颜色、圆角、卡片、响应式布局和装饰性容器。
- `/web` 当前不存在布局授权例外；浏览器默认渲染即为预期呈现。
- 修改 `src/web_ui.py` 后必须跑 `python -m pytest -q tests/regression/test_web_html.py` 或 `bash scripts/local-ci.sh --profile quick`。
