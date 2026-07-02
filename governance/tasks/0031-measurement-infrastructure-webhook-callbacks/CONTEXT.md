# Repo Evidence
- `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` 已列出 `MI-03.03 webhook callback contract 和签名`。
- `domains/experience-delivery/services/fatecat-delivery/src/report_jobs.py` 已有 bounded queue、TTL、cancel、SQLite store，但本任务前无终态 callback 出口。
- `domains/experience-delivery/services/fatecat-delivery/src/main.py` 已有 `/api/v1/report/jobs`、`/api/v1/report/jobs/web` 和 status/cancel endpoint。
- `contracts/fate/security/registry.json` 已有安全门禁登记模式，适合新增 webhook signature control。
- `scripts/local-ci.sh` 已是 quick gate 聚合入口，适合加入本地 webhook smoke。

# Constraints Matrix
| 约束 | 处理 |
| --- | --- |
| 安全默认 | API 默认不接受 callback URL，必须 `FATE_REPORT_JOB_WEBHOOKS_ENABLED=1`。 |
| 隐私 | webhook payload 不包含 Markdown 正文、姓名、出生地区、请求体或 secret。 |
| SSRF | 默认只允许 https，拒绝本机/内网/保留地址和带用户名密码 URL；支持可选 host allowlist。 |
| 可靠性 | callback 失败只记录日志，不改变 report job 终态。 |
| 存储 | webhook secret 只驻留内存，不写 SQLite、不写 audit_event、不回显响应。 |
| 范围 | 本任务不实现重试策略、分布式 worker 或真实公网 live smoke。 |

# Change Boundary
- 可改：`report_jobs.py`、`main.py`、新增 `webhook_callbacks.py`、相关 tests/scripts/contracts/docs/env/AGENTS/task docs。
- 不改：命理计算、Markdown 报告生成、Web UI 布局、Bot live 逻辑、数据库记录接口语义。

# Risk Matrix
| 风险 | 级别 | 缓解 |
| --- | --- | --- |
| 任意 URL 触发 SSRF | High | 默认关闭、https 默认、拒绝本机/内网/保留地址、allowlist 支持。 |
| secret 泄露到响应或日志 | High | 只记录 enabled/signature，不记录 URL/secret；测试覆盖不回显。 |
| callback 阻塞 job 状态锁 | Medium | dispatcher 在锁外执行。 |
| callback 失败导致主任务失败 | Medium | 捕获异常并记录，不反向修改终态。 |
| payload 混入报告正文 | High | payload builder 不读取 result 正文；smoke 和测试覆盖。 |

# Assumptions and Falsification
- 假设：当前 baseline 只需终态事件，不需进度事件。反证：调用方要求实时进度，则需要 job event history 和 progress callback。
- 假设：HMAC-SHA256 足以作为当前签名机制。反证：需要 replay protection 窗口、签名版本和 secret rotation 时，进入 webhook security v2。
- 假设：不持久化 webhook secret 是正确边界。反证：需要跨重启继续投递未完成 webhook，则必须接入安全 secret store 和 external job backend。

# Critical Ambiguities
- 真实接收端域名、SLA、重试策略和 dead letter policy 尚未定义，属于后续任务。
- 多租户生产中 webhook allowlist 是平台级还是租户级未定，当前只提供环境级 allowlist。

# Debug Evidence Contract
- 调试模式: Optional
- 本任务不是 bugfix；不需要 `DEBUG.md`。
- 若 webhook 投递、签名或隐私测试失败，必须记录最小失败 payload、触发命令和修复后回归结果。

# Task Package Context Map
| Area | Files |
| --- | --- |
| Runtime | `src/report_jobs.py`, `src/webhook_callbacks.py`, `src/main.py` |
| Tests | `tests/regression/test_api_contracts.py`, `tests/regression/test_webhook_smoke.py` |
| Scripts | `scripts/webhook-smoke.py`, `scripts/webhook-smoke.sh`, `scripts/local-ci.sh` |
| Contracts | `contracts/fate/security/registry.json`, `contracts/fate/delivery/registry.json`, `contracts/fate/capabilities/schemas/resource.schema.json` |
| Docs | `docs/reference-materials/operations/测算基础设施 API 接入.md`, `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` |
