# Task-Level Acceptance

本任务完成必须满足：

- `ReportJobEvent` 存在，并记录 job id、event type、状态、时间、消息和最小 metadata。
- memory backend 能在当前进程内返回 event history。
- SQLite backend 能持久化并按写入顺序读取 event history。
- API `CalculationJob` payload 包含 `events`，每项为 `CalculationJobEvent`。
- 事件历史不包含姓名、出生地区、Markdown 正文或 webhook secret。
- 文档明确剩余缺口：retry/timeout、callback retry/outbox、external backend、跨进程继续执行和真实 webhook live smoke。

## Validation Plan

| 验证项 | 命令 | 期望 |
| --- | --- | --- |
| report job focused tests | `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py -k 'report_job or sqlite_report_job_store'` | pass |
| webhook smoke regression | `.venv/bin/python -m pytest -q tests/regression/test_webhook_smoke.py` | pass |
| Python syntax | `python3 -m py_compile domains/experience-delivery/services/fatecat-delivery/src/report_jobs.py domains/experience-delivery/services/fatecat-delivery/src/main.py` | pass |
| task docs validator | `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0052-measurement-infrastructure-durable-runtime-event-history --phase closeout` | pass at closeout |
| task tree validator | `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_tasks_tree.py --tasks-dir governance/tasks --phase auto` | pass |
| diff hygiene | `git diff --check` | pass |

## Review Gate

| 维度 | Gate |
| --- | --- |
| 正确性 | 状态变化事件与 job 生命周期一致，SQLite 重建后历史仍可查询。 |
| 可读性 | event append 辅助函数集中，API serializer 独立。 |
| 架构 | 复用 ReportJobStore，不新增外部 runtime。 |
| 安全 | 事件 metadata 不记录真实用户输入、报告正文或 secret。 |
| 性能 | 每个 job 只追加少量事件；SQLite event 查询按 `job_id, sequence` 索引。 |

## Runtime Verification Gate

- 当前 runtime gate 只验证本地 memory/sqlite。
- 外部连通验证待执行：真实 webhook 接收端、外部 durable backend、多副本 worker、生产监控。
- 不能把本任务视为 durable runtime 100% 完成。

## Ship Readiness

- 所有 leaf TODO 勾选。
- `STATUS.md` 全节点 Done 且无 blocker。
- 验证命令结果写入 `Recent Evidence`。
- 当前 diff 不包含 secret、真实非北京地区示例或未跟踪运行态文件。

## Task Package Acceptance

- 任务文档无模板占位符。
- `TODO.md` 只包含叶子节点。
- `STATUS.md` 依赖图无环、ready 结果符合状态。
- `governance/tasks/INDEX.md` 新增 0052 行。

## Anti-Goals

- 不声明测算基础设施 100%。
- 不声明 job retry、timeout、outbox 或 external backend 已完成。
- 不引入新术数能力。
- 不新增前端视觉或报告正文结构变化。
