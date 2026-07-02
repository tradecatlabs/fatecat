# Repo Evidence
- 调试模式: Optional
- `report_jobs.py` 原实现是有界内存队列：`_jobs`、`_idempotency_index`、`Queue`、worker thread、TTL cleanup 全在单进程内。
- `/api/v1/report/jobs`、`/api/v1/report/jobs/{job_id}` 和 cancel API 已有，测试覆盖状态查询、幂等键、取消和 queue full。
- `/metrics` 已暴露 report job queue/status 指标，但没有 store backend 信息。
- `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` 明确 MI-03 缺 Job store 抽象与 SQLite backend。
- `docs/reference-materials/operations/测算基础设施 API 接入.md` 原文仍写“当前单进程内存队列”，需要同步。

# Constraints Matrix
| Constraint | Handling |
| --- | --- |
| 默认兼容 | 默认 `FATE_REPORT_JOB_STORE=memory`，现有 API/Web 行为保持。 |
| 最小依赖 | 使用 Python 标准库 `sqlite3`，不引入 Redis/Celery/RQ/Temporal。 |
| 单副本边界 | SQLite backend 只声明单副本本地持久化，多副本 production-readiness 直接拒绝。 |
| 不伪造继续执行 | manager 重建时将旧 `queued/running` 标为 `failed`，不假装 callable 可恢复。 |
| 隐私边界 | SQLite store 保存任务状态、输入摘要和结果，不保存 secret；运行态 DB 位于 `infra/runtime/local-state/`。 |

# Change Boundary
- 可改：`report_jobs.py`、`main.py`、`scripts/production-readiness.sh`、env examples、observability/security registry、API 文档、roadmap、fatecat-delivery AGENTS、regression tests、0030 任务文档。
- 不改：Markdown 生成、capability 计算、Web UI 布局、Bot、数据库记录 schema、外部部署脚本、真实生产配置。

# Risk Matrix
| Risk | Impact | Mitigation |
| --- | --- | --- |
| 默认行为被 SQLite 改变 | 公开服务回归 | 默认仍为 memory，metadata/metrics 测试锁定。 |
| SQLite 被误认为分布式队列 | 生产口径夸大 | production-readiness 多副本拒绝 memory/sqlite；文档明确单副本。 |
| result 序列化丢失 | 成功 job 查询不完整 | JSON-safe serializer 持久化 dict/dataclass，回归测试验证 dict result。 |
| 重启中的 running 任务语义错误 | 用户误以为任务还会完成 | 重建时标记 failed 并保留错误原因。 |
| 运行态 DB 入仓 | 仓库卫生风险 | 默认路径在 `infra/runtime/local-state/`，由现有 runtime hygiene 管理。 |

# Assumptions and Falsification
- 假设：本轮只需跨 manager 查询状态和结果，不需要跨进程继续执行。反证：如果验收要求 crash 后自动继续 queued/running callable，则必须引入外部任务系统。
- 假设：SQLite 单副本足以作为本地持久化 baseline。反证：如果部署副本数 >1 或多个 worker 进程共享任务，则进入 external backend 任务。
- 假设：现有 report job result 可用 JSON-safe 编码表达。反证：若出现不可恢复复杂对象，需给 job result 引入显式 schema。

# Critical Ambiguities
- 外部 backend 类型未定；本任务不选 Redis/Celery/RQ/Temporal。
- webhook 和 retry policy 未定；本任务只保留后续任务。
- SQLite DB retention 清理粒度未扩展到物理删除；本轮只标记 expired，后续可加压缩/清理任务。

# Debug Evidence Contract
- 本任务不是 bugfix；无需 `DEBUG.md`。
- 若 SQLite 持久化测试失败，必须记录失败命令、失败状态和修复结果到 `STATUS.md`。

# Task Package Context Map
| Node | Context |
| --- | --- |
| TP-01 | 盘点内存 job manager、API、metrics、tests、docs 缺口。 |
| TP-02 | 修改 runtime store、配置、metadata、metrics、production readiness。 |
| TP-03 | 补 SQLite 回归测试和文档/registry。 |
| TP-04 | 执行本地门禁并 closeout。 |

# Blockers
- 无当前本地阻塞。
- 外部连通验证待执行：外部任务系统、多副本生产锁、webhook 接收端、真实生产重启演练。
