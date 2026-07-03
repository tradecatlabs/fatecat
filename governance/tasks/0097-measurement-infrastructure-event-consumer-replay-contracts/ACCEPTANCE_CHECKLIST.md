# Acceptance Checklist

# Global Standards
- 每个 leaf 必须有 Verify 和 Gate。
- 不得跳过 gate；缺验证证据时不能 closeout。
- 本任务不得声明外部 broker、公网 webhook live、生产 replay worker、生产 DLQ 或 exactly-once 已完成。
- 示例、summary 和任务文档不得包含真实 webhook URL、secret、token、用户输入、报告正文、DSN 或生产日志。

# Task Package Checklists

## TP-01.01 复核现有事件契约
Verify: `sed`/`rg` 读取 events registry、schema、gate、tests、docs。
Gate: 不创建平行事件系统，不修改 runtime 逻辑。

- [x] 已读取 `contracts/fate/delivery/events.json`。
- [x] 已读取 `events.asyncapi.json` 与 `async-event.schema.json`。
- [x] 已读取 `scripts/event-contract-gate.py` 和 `test_event_contract_gate.py`。

## TP-02.01 Consumer Compatibility
Verify: `python3 -m json.tool contracts/fate/delivery/events.json`。
Gate: 每个 event 有 `consumerContract.requiredConsumers`，且至少一个非 `future.*` consumer。

- [x] `events.json` 包含 top-level `consumerCompatibility`。
- [x] 每个 event 包含 `consumerContract`。
- [x] 每个 `consumerContract.requiredConsumers` 至少包含一个非 `future.*` consumer。
- [x] gate 会验证 producer path 存在。

## TP-02.02 Replay/DLQ
Verify: `python3 -m json.tool contracts/fate/delivery/examples/event-replay/*.json`。
Gate: replay/DLQ 示例只保存 synthetic/redacted references，不保存完整 payload 或敏感值。

- [x] `events.json` 包含 top-level `replayPolicy`。
- [x] `replayPolicy.deadLetter` 包含 `redactedPayloadRef` required field。
- [x] `contracts/fate/delivery/examples/event-replay/replay-request.json` 已新增。
- [x] `contracts/fate/delivery/examples/event-replay/dead-letter-record.json` 已新增。

## TP-03.01 Gate
Verify: `bash scripts/event-contract-gate.sh --output-json /tmp/fatecat-event-contract-0097.json`。
Gate: gate 检查数不低于 240，并覆盖 producer path、consumer、replay/DLQ。

- [x] gate 校验 consumer policy required fields。
- [x] gate 校验 replay policy required fields。
- [x] gate 校验 replay examples 脱敏和本地边界。
- [x] gate summary 输出 consumer/replay/DLQ 指标。

## TP-03.02 Tests
Verify: `.venv/bin/python -m pytest -q tests/regression/test_event_contract_gate.py tests/regression/test_report_job_replayable_recovery_smoke.py tests/regression/test_webhook_outbox_redelivery_smoke.py`。
Gate: 缺 required real consumer、缺 producer path 和敏感 replay 示例会被拒绝。

- [x] summary 正向断言覆盖 consumer/replay/DLQ 指标。
- [x] 缺 required real consumer 负向拒绝。
- [x] 缺 producer path 负向拒绝。
- [x] replay examples redaction 断言。

## TP-04.01 Docs
Verify: `git diff -- docs/reference-materials/operations/测算基础设施 API 接入.md docs/reference-materials/roadmap/测算基础设施100%实现计划.md contracts/fate/delivery/AGENTS.md scripts/AGENTS.md tests/AGENTS.md`。
Gate: 文档不得声明外部 live 或生产 replay/DLQ 已完成。

- [x] `contracts/fate/delivery/AGENTS.md` 已同步。
- [x] `scripts/AGENTS.md` 已同步。
- [x] `tests/AGENTS.md` 已同步。
- [x] API 接入文档已同步。
- [x] 100% 路线图已同步。

## TP-05.01 Final Validation
Verify: closeout validator、secret scan、quick local-ci、git diff check。
Gate: 无 placeholders、无 secret findings、quick local-ci pass。

- [x] closeout validator 通过。
- [x] secret scan 通过。
- [x] quick local-ci 通过。
- [x] git diff check 通过。
