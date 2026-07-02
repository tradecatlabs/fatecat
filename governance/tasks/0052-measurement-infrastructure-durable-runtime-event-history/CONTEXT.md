# Task Context

## Repo Evidence

- 当前仓库根：`/home/lenovo/.projects/fatecat`
- 当前分支：`main`
- 前置任务：`0051-measurement-infrastructure-100-post-0050-executable-plan` 已把 `MI-NEXT-03 durable runtime 二期`列为 P0。
- 既有能力：
  - `0030` 已完成 memory/sqlite report job store baseline。
  - `0031` 已完成本地 webhook callback baseline。
  - `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` 明确剩余缺口包含 event history、retry/timeout、restart recovery、callback retry 和 external backend。
- 当前切片相关文件：
  - `domains/experience-delivery/services/fatecat-delivery/src/report_jobs.py`
  - `domains/experience-delivery/services/fatecat-delivery/src/main.py`
  - `tests/regression/test_api_contracts.py`
  - `tests/regression/test_webhook_smoke.py`
  - `docs/reference-materials/operations/测算基础设施 API 接入.md`
  - `docs/reference-materials/roadmap/测算基础设施100%实现计划.md`

## Constraints Matrix

| 约束 | 处理方式 |
| --- | --- |
| 不能伪造 100% 基础设施完成 | 文档只声明 event history first slice，retry/outbox/external backend 继续标为剩余缺口。 |
| 不泄露用户隐私 | event metadata 只记录 kind、reportSystem、idempotencyKeyProvided、webhookEnabled、状态和内部错误摘要，不记录姓名、出生地区、Markdown 正文或 webhook secret。 |
| 保持默认 memory backend 兼容 | `InMemoryReportJobStore` 保存进程内 event list，不改变默认配置。 |
| SQLite 只能是单副本 baseline | 文档明确不能把本地 SQLite 解释为生产分布式任务系统。 |
| Web/API/Bot 同源报告不应被扰动 | 本任务只改 report job envelope，不改报告生成逻辑。 |

## Change Boundary

允许修改：

- report job 状态机、store 抽象和 API serialization。
- report job 相关回归测试。
- API 接入文档、基础设施路线图、delivery 模块说明。
- `governance/tasks/0052-*` 任务包和 `governance/tasks/INDEX.md`。

不允许顺手修改：

- 命理计算核心、八字/紫微 provider、Markdown 正文结构。
- Web HTML 视觉、Telegram Bot 文案和 webhook payload 正文。
- 外部 job backend、真实 token、生产域名、SIEM/OIDC/监控平台。

## Risk Matrix

| 风险 | 影响 | 控制 |
| --- | --- | --- |
| 事件重复或乱序 | 审计历史不可信 | SQLite 使用 `sequence AUTOINCREMENT` 排序，event id 唯一；memory 保持 append 顺序。 |
| 事件泄露用户输入 | 隐私风险 | 测试断言 events JSON 不含 `测试样本` 和 `北京`。 |
| 状态恢复口径被误读 | 误宣称跨进程继续执行 | 文档明确 rebuild 只把未完成任务标为 failed，不继续执行。 |
| webhook 事件被误认作 retry | 交付能力夸大 | webhook delivery event 只记录一次投递结果，不实现 retry/outbox。 |
| 文档漂移 | 审计看到代码和路线图冲突 | 同步 API 文档、roadmap、AGENTS 和 task index。 |

## Assumptions and Falsification

- 假设：本轮只需要 `CalculationJob` event history，不需要同时实现 retry/timeout。
  - 推翻条件：测试或用户要求必须马上具备 retry/outbox 才能验收，则拆出后续任务，不能混入本任务。
- 假设：事件 metadata 可以保持最小字段，避免隐私和稳定性风险。
  - 推翻条件：下游 API 客户端需要 CloudEvents/AsyncAPI envelope，则新建契约任务处理，而不是改本切片目标。
- 假设：SQLite event table 在旧数据库上用 `CREATE TABLE IF NOT EXISTS` 增量创建即可。
  - 推翻条件：兼容测试发现旧库不可打开或 schema 冲突，则增加 migration regression。

## Critical Ambiguities

- 是否要选 external backend：本任务不决定；后续 `MI-NEXT-03.05` 单独决策。
- 是否要采用 Temporal/Celery：本任务不引入；当前规模下只做 event history baseline。
- 是否要 CloudEvents 规范化所有内部 job events：本任务暂不做，避免扩大 API 契约面。

## Debug Evidence Contract

- 调试模式: Optional
- 当前不是 bugfix；若验证失败，需把失败命令、最小复现、根因和回归证据补到任务 closeout 或 `DEBUG.md`。

## Task Package Context Map

| Node ID | Context |
| --- | --- |
| TP-01.01 | 读取 0030/0031 前置任务、report job 源码、API 文档和路线图缺口。 |
| TP-02.01 | 修改 `report_jobs.py` 的模型、store、SQLite schema 和状态机事件写入。 |
| TP-02.02 | 修改 `main.py` 的 report job payload serialization。 |
| TP-03.01 | 修改 `tests/regression/test_api_contracts.py` 并运行 focused tests。 |
| TP-03.02 | 修改 docs、AGENTS 和任务索引。 |
| TP-04.01 | 运行 validators、pytest、ruff、diff hygiene 和 git 状态检查。 |
