# Task Overview
- Task ID: `0031`
- Slug: `measurement-infrastructure-webhook-callbacks`
- Objective: `把异步报告任务推进为本地可验证 webhook callback baseline：定义 webhook callback 契约、HMAC-SHA256 签名、终态事件 payload、可插拔 dispatcher 和本地 simulator/smoke，接入 report job succeeded/failed/cancelled 终态；保留默认无 webhook、且不做真实公网连通、持久重试队列、分布式 worker 或外部任务系统。`
- Status: `Done`

## In Scope
- 新增 report job webhook callback payload、HMAC-SHA256 签名、URL 基础安全校验和可注入 HTTP dispatcher。
- 将 callback 接入 `succeeded`、`failed`、`cancelled` 三类终态；callback 失败不得反向破坏任务终态。
- FastAPI report job endpoint 支持可选 `X-FateCat-Webhook-Url` 与 `X-FateCat-Webhook-Secret`，但默认环境关闭。
- 新增本地 webhook simulator/smoke，接入 quick CI。
- 更新 security/delivery/resource 契约、环境示例、API 文档、路线图和目录级 AGENTS。

## Out of Scope
- 不做真实公网 webhook 接收端连通验证。
- 不做持久 retry queue、dead letter queue、指数退避或 non-retryable error policy。
- 不做外部分布式任务系统、跨进程继续执行或多副本任务锁。
- 不发送 Markdown 正文、姓名、出生地区、请求体或 webhook secret。
- 不改变八字、紫微或 Markdown 报告生成逻辑。

## Task Package Tree
```text
TP-01 现状审计与任务边界
  TP-01.01 盘点 report job 状态机、API、registry、roadmap 缺口
TP-02 webhook callback runtime baseline
  TP-02.01 新增 webhook payload/signature/dispatcher
  TP-02.02 接入 report job terminal transitions
  TP-02.03 接入 API header 和安全默认关闭
TP-03 smoke、测试与门禁
  TP-03.01 新增 webhook smoke simulator
  TP-03.02 新增 API/manager/smoke 回归测试
  TP-03.03 接入 quick local-ci
TP-04 契约、文档和治理同步
  TP-04.01 更新 contracts/env/docs/AGENTS/roadmap
  TP-04.02 回填任务 closeout 证据
```

## Requirement Alignment
- 对齐 `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` 的 `MI-03.03 webhook callback contract 和签名`。
- 对齐测算基础设施目标：长任务必须能被外部调用方以可验证事件接收终态。
- 保持基础设施安全边界：默认关闭、显式启用、URL 校验、HMAC 签名、不泄露报告正文和 secret。

## Task Package Overview
| Package | Status | Evidence |
| --- | --- | --- |
| TP-01 | Done | 已用 `rg` 和 targeted reads 盘点 report job/API/registry/roadmap。 |
| TP-02 | Done | 已新增 `webhook_callbacks.py`，扩展 `report_jobs.py` 和 `main.py`。 |
| TP-03 | Done | webhook focused tests 和 quick CI 已通过。 |
| TP-04 | Done | contracts/docs/env/AGENTS 已同步；closeout packet 已生成。 |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
