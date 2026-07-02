# Acceptance Checklist

## Global Standards

- [x] 变更边界限定在 report job event history、API envelope、测试与文档。
- [x] 不读取、不提交、不输出真实 `.env`、token、secret、webhook secret 或生产 DSN。
- [x] 不改命理计算核心、报告正文结构或 Web HTML 视觉。
- [x] focused tests、task docs validators 和 diff hygiene 全部通过。
- [x] 任务状态和 INDEX 与真实 worktree 状态一致。

## Task Package Checklists

## TP-01.01

- [x] 已读取 0030/0031 任务事实和现有 report job 源码。
- [x] 已确认当前缺口是 event history、retry/timeout、restart recovery、callback retry 和 external backend。
- [x] 已把本任务范围缩到 event history first slice。
Verify: `rg` / `sed` 读取相关文件。
Gate: 不基于聊天记忆脑补缺口。

## TP-02.01

- [x] 已新增 `ReportJobEvent`。
- [x] 已给 memory store 增加 event list。
- [x] 已给 SQLite store 增加 `report_job_events` 表和查询方法。
- [x] 已在 queued/running/succeeded/failed/cancelled/expired/recovered_failed/webhook delivery 写入事件。
Verify: focused pytest + py_compile。
Gate: 状态变化可写入并读取事件历史。

## TP-02.02

- [x] API `CalculationJob` 响应包含 `events`。
- [x] 每个 event 输出 `resourceType=CalculationJobEvent`、`eventId`、`jobId`、`eventType`、`status`、`createdAt`、`message`、`metadata`。
Verify: focused API contract test。
Gate: `events` 字段结构稳定。

## TP-03.01

- [x] 成功异步报告断言事件序列。
- [x] SQLite 完成任务重建后断言事件序列。
- [x] SQLite 旧 running/queued recovery failed 断言 `job.recovered_failed`。
- [x] 事件 JSON 隐私断言不含姓名和地区。
Verify: `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py -k 'report_job or sqlite_report_job_store'`。
Gate: 成功、重建、recovery failed、隐私断言通过。

## TP-03.02

- [x] API 接入文档说明 event history。
- [x] roadmap 标记 event history first slice 已落地，剩余缺口仍保留。
- [x] delivery AGENTS 说明 `report_jobs.py` 管理状态机与事件历史。
- [x] `governance/tasks/INDEX.md` 增加 0052。
Verify: `git diff -- docs governance domains/experience-delivery/services/fatecat-delivery/AGENTS.md`。
Gate: 文档口径不夸大能力。

## TP-04.01

- [x] focused pytest 通过。
- [x] task docs validators 通过。
- [x] ruff / py_compile / diff hygiene 通过。
- [x] git status 与提交推送状态完成记录。
Verify: pytest、validators、ruff/py_compile、`git diff --check`。
Gate: 全部通过且无活动 blocker。
