# Repo Evidence
- 调试模式: Optional
- `main.py` 已有结构化 `http_request` 日志，但缺少面向敏感资源访问的 `audit_event`。
- 记录接口已有 token/owner 边界：`_require_record_access`、`_require_owner_or_admin`、`get_record`、`get_user_records`、`delete_record`。
- 报告 job 已有 TTL：`ReportJobManager(ttl_seconds=REPORT_JOB_TTL_SECONDS)` 与 `cleanup_expired()`。
- `contracts/fate/security/registry.json` 原先把审计日志、retention policy 作为未完成缺口。
- `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` IMP-10 仍列出审计日志和 retention 未完成。

# Constraints Matrix
| Constraint | Handling |
| --- | --- |
| 不泄露敏感原文 | audit_event 不记录 token、请求体、报告正文、姓名、出生地区、recordId、jobId 或 userId 原文。 |
| 不伪造生产审计平台 | 只做本地结构化日志与 registry 登记；外部 SIEM/不可变审计存储仍待执行。 |
| 不改变业务语义 | 只新增日志事件和 registry/docs/tests，不改变权限判断和数据模型。 |
| retention 不夸大 | 明确 report job TTL 已有，用户记录默认显式删除，自动按年龄清理仍后续。 |

# Change Boundary
- 可改：`main.py`、security schema/registry、API/contract tests、docs、AGENTS、0026 任务文档。
- 不改：数据库 schema、生产日志后端、OAuth/OIDC、RBAC、真实 secret、记录自动清理机制。

# Risk Matrix
| Risk | Impact | Mitigation |
| --- | --- | --- |
| 审计日志泄露敏感数据 | 二次隐私事故 | 只输出短哈希和安全 metadata，测试断言不含 token/userId/jobId 原文。 |
| 把本地日志误读成生产审计 | 审计结论夸大 | registry/docs 明确外部 SIEM/不可变审计存储待执行。 |
| audit_event 影响接口行为 | API 回归 | 只调用 logger，不改变响应；API contract tests 覆盖。 |
| retention policy 过度承诺 | 生产治理虚假完成 | 明确记录默认显式删除，自动清理后续实现。 |

# Assumptions and Falsification
- 假设：结构化 logger 能被现有 TestClient/caplog 验证。反证：audit_event tests 失败。
- 假设：新增 audit_event 不影响 API 响应和 job lifecycle。反证：API contract tests 或 quick CI 失败。
- 假设：retention baseline 只需要资源化现有 job TTL 和显式删除口径。反证：需求变成生产数据库自动清理或外部日志平台，则另起任务。

# Critical Ambiguities
- 外部审计平台、生产日志保留周期和不可变存储未提供；本任务不接入。
- `FATE_RECORD_RETENTION_DAYS>0` 的自动清理机制未实现；本任务只登记配置口径和当前风险。

# Debug Evidence Contract
- 本任务不是 bugfix；无需 `DEBUG.md` 根因闭环。
- 若 audit_event 测试失败，失败日志必须保持脱敏，修复证据回填 `STATUS.md`。

# Task Package Context Map
| Node | Context |
| --- | --- |
| TP-01 | 读取记录接口、job TTL、security registry 和 roadmap。 |
| TP-02 | 新增 audit helper 并接入关键 runtime action。 |
| TP-03 | 补 registry/schema/API tests 和文档。 |
| TP-04 | 执行 focused tests、secret scan、ruff/format、quick CI、diff check 和 validators。 |
