---
id: CTX-DOMAINS-EXPERIENCE-DELIVERY-SERVICES-FATECAT-DELIVERY
type: module-context
status: current
owner: fatecat-delivery
created: 2026-07-13
last_reviewed: 2026-07-13
code_path: domains/experience-delivery/services/fatecat-delivery
---

# FateCat Delivery Context

## 模块职责

- 提供 FastAPI、Web、Telegram、异步报告任务和兼容 API 投影。
- 所有测算必须委托 `CapabilityExecutor`；交付层只做校验、编排、限流、持久化和渲染。
- 核心 readiness 与可选 DeliverySurface 状态分层，渠道故障必须可观测但不得拖垮核心服务。

## 上下游

- 上游：`fate-core`、delivery/capability/security/observability contracts。
- 下游：浏览器、API 客户端、Telegram、HF Space 和容器运行时。
- Web/API/Bot 不得自行定义命理规则或拼接第二份报告数据。

## 关键门禁

- `tests/regression/test_api_contracts.py`
- `tests/regression/test_entrypoint_consistency.py`
- `tests/regression/test_multi_surface_semantic_diff.py`
- `tests/regression/test_telegram_webhook.py`
- `bash scripts/delivery-smoke.sh --target api`

## 禁止事项

- 禁止把 legacy calculator 设为公开入口默认引擎。
- 禁止日志记录用户输入、token、secret、DSN 或完整报告。
- 禁止用可选 Bot/Webhook 状态替代核心服务 readiness。
