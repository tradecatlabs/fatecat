# Planning Summary
本轮把 report job 从“只能轮询状态”推进到“可选 webhook 终态 callback baseline”。正确终态是长任务控制面具备 durable state、idempotency、cancel、callback、retry、external backend 和 observability。本轮只实现 callback contract/signature/simulator，避免把范围扩大成 workflow platform。

# Lifecycle Gates
不得跳过 gate；每个 gate 必须有证据或保留为 Pending。

| Gate | Status | Evidence |
| --- | --- | --- |
| SPEC | Done | README/CONTEXT 已定义范围和 anti-goals。 |
| PLAN | Done | 本文件拆出 runtime、API、smoke、contract/docs 四层。 |
| BUILD | Done | runtime/API/scripts/tests/docs 已落地。 |
| TEST | Done | focused tests 和 quick CI 已通过。 |
| REVIEW | Done | task validator、lint/format、secret scan、production readiness static 已通过。 |
| SHIP | Done | closeout packet 已生成。 |

# Simplest Path
- 复用现有 `ReportJobManager` 状态机，不引入新队列或外部依赖。
- 新增薄 `webhook_callbacks.py`，使用标准库 HTTP，并通过 transport 注入做本地 smoke。
- callback 配置只挂在单个 `_ReportJob` 内存对象，SQLite 不保存 secret。
- API header 只转换成 `WebhookConfig`，不让前端或报告层参与拼 payload。

# Split Strategy
- TP-01：先审计缺口，确认 webhook 是 roadmap 中 MI-03.03，而不是临时需求。
- TP-02：先做 runtime 终态事件，再接 API header。
- TP-03：先做本地 simulator，再接 quick CI。
- TP-04：最后同步 registry、文档、env、AGENTS 和任务证据。

# Execution Waves
| Wave | Leaves | Status |
| --- | --- | --- |
| Wave 1 | TP-01.01 | Done |
| Wave 2 | TP-02.01, TP-02.02, TP-02.03 | Done |
| Wave 3 | TP-03.01, TP-03.02, TP-03.03 | Done |
| Wave 4 | TP-04.01, TP-04.02 | Done |

# Runtime Workflow Contract
- Input: report job request plus optional `X-FateCat-Webhook-Url` and `X-FateCat-Webhook-Secret` headers.
- State: queued/running/succeeded/failed/cancelled/expired remains owned by `ReportJobManager`.
- Event: only `succeeded` / `failed` / `cancelled` emits `report_job.terminal`.
- Output: `WebhookEvent` payload with HMAC header when secret exists.
- Privacy: no report markdown, no input summary, no secret.
- Failure: callback errors are logged and swallowed; status remains terminal.

# Next Executable Leaves
- 无；任务已完成。

# Dependency Graph
```text
TP-01.01 -> TP-02.01 -> TP-02.02 -> TP-02.03 -> TP-03.01 -> TP-03.02 -> TP-03.03 -> TP-04.01 -> TP-04.02
```

# Rollback Protocol
- 回退 `webhook_callbacks.py`、`report_jobs.py` webhook 字段、`main.py` webhook header 接入。
- 移除 `scripts/webhook-smoke.*` 和 `tests/regression/test_webhook_smoke.py`。
- 恢复 contracts/docs/env/AGENTS/roadmap 到 0030 口径。
- 不回滚其他任务目录或前序 0009-0030 改动。
