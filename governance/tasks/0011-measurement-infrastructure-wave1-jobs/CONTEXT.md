# Repo Evidence
- 现有 `report_jobs.py` 已支持 `queued/running/succeeded/failed/expired`、TTL、队列、worker、metrics。
- 现有 `main.py` 已有 `/api/v1/report/jobs` 和 `/api/v1/report/jobs/{job_id}`。
- 现有 API tests 已覆盖基本异步报告任务。

# Constraints Matrix
| 约束 | 处理 |
| --- | --- |
| 单进程内存队列 | 幂等只承诺当前 TTL 生命周期内 |
| running 线程不可安全强杀 | cancel 只标记 cancelled，任务完成后丢弃结果 |
| 不改变报告计算 | 只包 job lifecycle |
| 不引入新 infra | 不新增 Redis/Celery |

# Change Boundary
- 可改：`report_jobs.py`、`main.py`、API/协议测试、docs/reference-materials、0011 任务容器。
- 不改：provider、报告算法、数据库 schema、部署配置。

# Risk Matrix
| 风险 | 等级 | 缓解 |
| --- | --- | --- |
| cancel 与 worker 竞态 | 中 | worker 写结果前检查 cancelled |
| 幂等键复用语义过度承诺 | 中 | 文档写明 TTL/单进程边界 |
| 状态计数遗漏 cancelled | 低 | metrics stats 加 cancelled |

# Assumptions and Falsification
- 假设：现有内存 job manager 可承载 Wave 1 的最小幂等和取消需求。
- 证伪：如果回归测试出现 cancel 后又 succeeded，说明必须先重写 job 状态机。

# Critical Ambiguities
- 跨进程/跨重启幂等需要外部 job store，后续单独做。

# Debug Evidence Contract
- 调试模式: Optional
- 本任务有并发边界，必须用 API 回归测试验证 cancel 后状态保持 `cancelled`。

# Task Package Context Map
- `report_jobs.py`：job lifecycle 真相源。
- `main.py`：API 和 payload 真相源。
- `test_api_contracts.py`：idempotency/cancel 回归。
- `resource.schema.json`：CalculationJob 字段和状态契约。
