# Acceptance Checklist

# Global Standards

- [x] 任务边界明确：0080 只做 multi-replica runtime evidence gate baseline。
- [x] 单副本、短运行、本地 SQLite 不被写成多副本 live。
- [x] Contract、gate、registry、local-ci、tests 和 docs 已接线。
- [x] 外部待验证项未被伪造成完成。

# Task Package Checklists

## TP-01 现状复核与任务定界

Verify: roadmap、runtime registry、local-ci、tests 已读取。

Gate: 任务边界不包含真实多副本 live 执行。

- [x] TP-01.01 复核 durable runtime 当前缺口。
- [x] TP-01.02 复核 runtime registry、local-ci 和测试接线点。

## TP-01.01 复核 0078/0079 后 durable runtime 缺口

Verify: `runtime-backends.json` and roadmap inspected.

Gate: worker heartbeat/polling 和 secret provider gate 不被写成 multi-replica live。

- [x] 已确认 0078 只证明 worker heartbeat/polling baseline。
- [x] 已确认 0079 只证明 external secret provider evidence gate baseline。

## TP-01.02 复核 runtime registry、local-ci 和测试接线点

Verify: registry/local-ci/tests inspected.

Gate: 新 contract 必须接入可执行 gate 和 quick CI。

- [x] Runtime registry touch point located。
- [x] local-ci artifact touch point located。

## TP-02 多副本运行证据契约

Verify: JSON parse and gate validation.

Gate: contract must not contain raw secret values or live overclaim.

- [x] TP-02.01 新增 multi-replica runtime evidence contract。
- [x] TP-02.02 新增反伪造负例。

## TP-02.01 新增 multi-replica runtime evidence contract

Verify: `python3 -m json.tool contracts/fate/delivery/multi-replica-runtime-contract.json`.

Gate: contract includes privacy and exactly-once non-claim boundary.

- [x] Contract file exists.
- [x] Contract defines minimum replicas, duration and completed jobs.

## TP-02.02 新增 single-replica、short-run、sqlite 和 exactly-once overclaim 负例

Verify: `bash scripts/multi-replica-runtime-gate.sh`.

Gate: fake evidence must be rejected.

- [x] Negative cases present.
- [x] Live schema requires public webhook、external secret provider and metrics proof refs.

## TP-03 Runtime gate 接线

Verify: runtime-backend-gate and local-ci.

Gate: Postgres remains planned/external pending.

- [x] TP-03.01 更新 runtime backend registry 与 delivery registry。
- [x] TP-03.02 新增 multi-replica-runtime-gate.py/.sh。
- [x] TP-03.03 接入 runtime-backend-gate 与 local-ci artifact。

## TP-03.01 更新 runtime backend registry 与 delivery registry

Verify: `bash scripts/runtime-backend-gate.sh`.

Gate: `backend.postgres` keeps production-ready blocked claims.

- [x] Postgres remains planned.
- [x] Multi-replica evidence contract and gate linked.

## TP-03.02 新增 multi-replica-runtime-gate.py/.sh

Verify: gate output JSON.

Gate: summary redacted and fake evidence rejected.

- [x] Python gate added.
- [x] Shell wrapper executable.

## TP-03.03 接入 runtime-backend-gate 与 local-ci artifact

Verify: `local-ci.sh` step and summary artifact key.

Gate: quick CI must run the gate.

- [x] runtime-backend-gate checks new links.
- [x] local-ci run step and summary artifact key added.

## TP-04 Tests and docs

Verify: focused tests and docs grep.

Gate: no live overclaim.

- [x] TP-04.01 增加 regression tests。
- [x] TP-04.02 更新 roadmap、operations docs 和 AGENTS。

## TP-04.01 增加 regression tests

Verify: focused pytest.

Gate: tests cover contract, negative cases, redacted live evidence and privacy.

- [x] Regression test file added.
- [x] Existing runtime tests updated.

## TP-04.02 更新 roadmap、operations docs 和 AGENTS

Verify: docs updated.

Gate: multi-replica live remains pending.

- [x] Roadmap updated.
- [x] Operations docs updated.
- [x] AGENTS updated.

## TP-05 Verify/closeout/ship

Verify: focused gates, quick CI, task validators, git/CI evidence.

Gate: no failing required checks.

- [x] TP-05.01 运行完整验证命令。
- [x] TP-05.02 回填 closeout、提交、推送并记录 CI。

## TP-05.01 运行 focused gates、pytest、ruff/format 和 quick CI

Verify: command output.

Gate: failures fixed or explicitly blocked.

- [x] Focused gates complete.
- [x] Focused tests and ruff complete.
- [x] Quick CI complete.
- [x] Task validators complete.

## TP-05.02 回填 closeout、提交、推送并记录 CI

Verify: git status/commit/push/CI evidence in delivery closeout.

Gate: tracked task docs must not pre-claim remote CI before the commit exists.

- [x] Task docs closed.
- [x] Commit/push handled by delivery closeout outside the committed task snapshot.
- [x] Remote CI evidence will be reported from the actual post-push GitHub Actions run.

# Completion Standard

- 本地 gate 和 quick CI 通过。
- 文档不宣称真实多副本 live passed。
- Postgres 仍保持 planned/candidate，不升级成 production ready。
- 未泄露 secret、token、DSN、webhook URL 或报告正文。
