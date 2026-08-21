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
- Web HTML 必须遵守 `/home/lenovo/.codex/Design.md` 的零美化语义核心内容规范；允许的工作台 CSS 仅限 GATE-0001 白名单中的三层结构、系统背景、z-index、覆盖宽度和功能性开关，不得加入品牌视觉、视觉 class、圆角、卡片、阴影或动画。
- `/web` 当前只具有 GATE-0001 登记的结构性工作台例外；浏览器无 CSS 时仍保持完整可读。工作台由 `#top-layer` / `#control-plane` / `#data-plane` 表达，固定 z-index `3/2/1` 和 `clamp(320px, 28vw, 440px)` 控制面，`#report-content` 在控制面展开时避让到可见中部，视觉美化仍被禁止；映射见 `governance/decisions/adr/ADR-0002-native-workbench-semantic-layer-map.md`。
- Web 出生地区只显示一个原生 `input+datalist`：输入任意一个或多个地区字符后查询本地点目录，候选展示完整行政区路径，选择后提交稳定 `cn:{code}`；输入过程不显示查找、候选数量或选择状态等动态提醒，未选候选时仅在提交时使用浏览器原生校验。无 JavaScript 时可提交唯一完整地区名称由服务端解析。海外、直接坐标、IANA 时区与 DST 能力保留在 API/后端，不作为 Web 默认控件。
- Web 顶部表格只保留人类需要的项目与使用摘要；公开端点、字段契约、地点解析、任务协议和 AI 风险边界集中由根级 `llms.txt` 与 `GET /llms.txt` 提供。
- `src/location_catalog.py` 从 canonical gzip NDJSON 确定性构建只读 SQLite 查询索引；索引仅写入 `infra/runtime/local-state/`，可删除重建，不是数据真相源。
- `src/location.py` 统一承担稳定地点 ID、WGS84、IANA 时区和 `local_civil/beijing_time/utc` 出生钟表口径标准化；Web 与 Bazi API 必须复用该链路。
- 修改 `src/web_ui.py` 后必须跑 `python -m pytest -q tests/regression/test_web_html.py` 或 `bash scripts/local-ci.sh --profile quick`。
