# AGENTS.md - fatecat-delivery

## 目录用途

`fatecat-delivery` 是 FateCat 的交付服务。本服务根是源码真相源，运行资产从 `contracts/`、`infra/`、`tools/` 和上游 `fate-core` 读取。

## 目录结构

```text
fatecat-delivery/
├── AGENTS.md
├── README.md
├── service.yaml
├── start.py
├── scripts/
├── src/
│   ├── bot_progress.py
│   ├── calculation_service.py
│   ├── report_jobs.py
│   ├── webhook_callbacks.py
│   ├── report_markdown.py
│   ├── service_config.py
│   ├── web_report_service.py
│   └── web_forms.py
└── tests/
```

## 职责边界

- 负责 FastAPI、Web HTML、Telegram Bot、标准 Markdown 报告和 legacy 交付适配。
- 不定义 capability registry、字段 profile 或底层命理算法。
- `src/bazi_calculator.py` 只保留兼容导出入口，真实八字 legacy 核心归属 `fate_core.kernel.bazi_calculator`；新增命理规则必须进入 `fate-core`，不能扩散到 API/Web/Bot/报告层。
- `src/calculation_service.py` 只收敛 Web/API/Bot 到 fate-core/capability 的共享计算编排，不承载命理规则、HTML 渲染、Bot 文案或数据库写入。
- 不读取真实 secret 入仓；delivery smoke 可临时生成本地 `.env` 并清理。
- `src/web_ui.py` 只负责零美化语义 HTML：服务端直出、原生表单、真实链接、psql ASCII 表格、Markdown 原文和机器可读片段。
- `src/web_forms.py` 只定义 Web 原生表单输入和服务端报告结果模型，不渲染 HTML、不调用命理计算。
- `src/web_report_service.py` 只连接 Web 表单、地区解析、capability 执行和 Markdown 生成；不得渲染 HTML 或管理任务生命周期。
- `src/report_jobs.py` 只承载公开服务报告任务的队列、状态机、TTL、指标、CalculationJob event history 和可选 SQLite job store；不得实现命理规则。`memory` 是默认单进程后端，`sqlite` 只提供单副本本地持久状态与事件历史查询，多副本生产扩容应替换为外部队列或数据库任务系统。
- `src/webhook_callbacks.py` 只承载 report job 终态 callback payload、HMAC-SHA256 签名、URL 基础校验和可注入 HTTP dispatcher；不得保存 webhook secret、发送报告正文或实现持久重试队列。
- `src/report_markdown.py` 只承载 Markdown 表格、转义和行内文本压缩工具；报告层可复用，但不得写入命理规则。
- `src/main.py` 负责 HTTP requestId、W3C `traceparent` 传播、OpenTelemetry 语义兼容本地 span 日志接入、metrics 和结构化日志；trace context 真相源在 `fate_core.observability`，delivery 不自建第二套 trace 协议。
- `src/bot_progress.py` 只承载 Telegram Bot 进度项和提示文案；Bot 主流程仍在 `src/bot.py`。
- `src/service_config.py` 只读取交付服务环境配置；运行期常量仍由 `src/main.py` 初始化，便于测试 monkeypatch 和 FastAPI 启动时固定配置。
- `tests/test_bot_send_queue.py` 覆盖 Telegram Bot 本地补发 outbox 的幂等入队、原子保存和 ACK 删除；不得把它误认为跨进程分布式队列测试。
- `/web` 当前唯一授权布局例外是 `D:\.projects\pdf` 工作台同类的黄金比例三块全屏生产空间：左上 TradeCat Labs 资产声明、右上服务端生成报告、底部参数输入；只允许 `web-production-*` 结构 class、必要 grid CSS、面板边界和控件可读性 CSS。
- Web HTML 禁止授权例外之外的 CSS、视觉 class、颜色、圆角、卡片、响应式布局和装饰性容器；修改前必须读取 `/home/lenovo/.codex/Design.md` 与 `GATE-0001`。

## Principle Gate Evidence

- target end state: delivery only transports, renders, observes, and protects fate-core outputs.
- real constraints: old public imports, Bot messages, API contracts, and Markdown fields still exist.
- inertia constraints: legacy delivery names are migration windows, not owners of domain rules.
- kill list: delivery-owned rules, unregistered wrappers, visual CSS drift, and hidden fallbacks.
- proof point: delivery service contract, API contract, Web HTML, and Bot queue tests pass.
- falsifier: new fate rules appear under delivery `src/` or `/web` violates `Design.md`.
- migration slice: retain registered exports while moving calculation ownership into fate-core.
- existence: `AGENTS.md` is required because this directory owns multiple user-facing channels.
- owner: tradecatlabs/fatecat-delivery.
- verification: `domains/experience-delivery/services/fatecat-delivery/tests/test_service_contract.py`.

## 依赖方向

- 当前状态：`domains/experience-delivery/services/fatecat-delivery -> domains/fate-analysis/services/fate-core + contracts/fate + infra + tools/reference-repos`
- 运行态输出只允许进入本服务 `output/` 或 `infra/runtime/local-state/`，不得写回 vendor 快照。
- `/web` 页面设计真相源：`/home/lenovo/.codex/Design.md`、`governance/standards/零美化语义界面标准.md`、`governance/context/module-contexts/domains-experience-delivery-services-fatecat-delivery-src-web-ui-py/CONTEXT.md`。
