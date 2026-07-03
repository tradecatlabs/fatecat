# Acceptance Checklist

# Global Standards

- [x] 任务边界明确：0081 只做 multi-replica runtime evidence assembler。
- [x] 不把 assembler 生成能力写成真实 live passed。
- [x] Assembler 必须复用 0080 gate。
- [x] 外部待验证项保留为 `外部连通验证待执行`。

# Task Package Checklists

## TP-01 SPEC: 证据链缺口复核

Verify: roadmap、0080 contract/gate inspected.

Gate: 任务目标不是重写 runtime core。

- [x] TP-01.01 复核 0080 contract/gate 与 roadmap 剩余缺口。
- [x] TP-01.02 定义 assembler live/pending 边界。

## TP-01.01 复核 0080 contract/gate 与 roadmap 剩余缺口

Verify: `multi-replica-runtime-contract.json` and roadmap inspected.

Gate: 确认缺的是受控 evidence producer。

- [x] 0080 gate 可消费 `--evidence-json`。
- [x] roadmap 仍标记长期多副本运行 live evidence 未完成。

## TP-01.02 定义 assembler live/pending 边界

Verify: task docs boundary.

Gate: pending 不能被写成 live passed。

- [x] pending mode defined.
- [x] external live mode requires explicit ack and proof refs.
- [x] exactly-once remains non-claim.

## TP-02 PLAN: 证据装配器设计

Verify: PLAN has Future/Ponytail and CLI/schema direction.

Gate: 不复制 0080 gate 判定逻辑。

- [x] TP-02.01 设计 CLI 输入、输出 schema 和防敏感值策略。
- [x] TP-02.02 定义 0080 gate 复用路径和反伪造负例。

## TP-02.01 设计 CLI 输入、输出 schema 和防敏感值策略

Verify: generated evidence shape.

Gate: output is `kind=fatecat.multi_replica_runtime_evidence`.

- [x] Required runtime fields mapped.
- [x] Operator attestation and run metadata required for live mode.

## TP-02.02 定义 0080 gate 复用路径和反伪造负例

Verify: tests and CLI behavior.

Gate: fake/secret/overclaim rejected.

- [x] Gate reuse required.
- [x] Negative cases identified.

## TP-03 BUILD: 代码与接线

Verify: scripts and docs updated.

Gate: no external service connection.

- [x] TP-03.01 新增 assembler Python 与 shell wrapper。
- [x] TP-03.02 接入 local-ci artifact、scripts AGENTS 和 docs。

## TP-03.01 新增 assembler Python 与 shell wrapper

Verify: syntax and CLI smoke.

Gate: wrapper executable.

- [x] Python script added.
- [x] Shell wrapper added.
- [x] Pending CLI works.
- [x] Live fixture CLI works and validates against gate.

## TP-03.02 接入 local-ci artifact、scripts AGENTS 和 docs

Verify: local-ci and docs grep.

Gate: docs keep external live pending.

- [x] local-ci quick runs assembler pending artifact.
- [x] `scripts/AGENTS.md` updated.
- [x] roadmap/API docs updated.

## TP-04 TEST: 回归与门禁

Verify: focused tests and gates.

Gate: no failing required checks.

- [x] TP-04.01 增加 assembler regression tests。
- [x] TP-04.02 运行 focused gates、ruff/format、secret scan、quick CI 和任务校验。

## TP-04.01 增加 assembler regression tests

Verify: focused pytest.

Gate: tests cover positive and negative paths.

- [x] Pending output test.
- [x] Live fixture accepted by gate.
- [x] Missing ack rejected.
- [x] Secret/raw URL rejected.
- [x] Exactly-once overclaim rejected.

## TP-04.02 运行 focused gates、ruff/format、secret scan、quick CI 和任务校验

Verify: command output.

Gate: failures fixed or explicitly blocked.

- [x] Syntax checks complete.
- [x] Focused pytest complete.
- [x] Ruff complete.
- [x] Secret scan complete.
- [x] Quick CI complete.
- [x] Task validators complete.

## TP-05 REVIEW/SHIP

Verify: closeout + git/CI evidence.

Gate: no document overclaim.

- [x] TP-05.01 回填 closeout 与剩余外部验证项。
- [x] TP-05.02 明确 git/CI 交付证据外置边界。

## TP-05.01 回填 closeout 与剩余外部验证项

Verify: task docs validate closeout.

Gate: no placeholder remains.

- [x] STATUS/ACCEPTANCE updated.
- [x] Remaining external items listed.

## TP-05.02 明确 git/CI 交付证据外置边界

Verify: task snapshot does not pre-claim git status/commit/push/CI evidence.

Gate: tracked task docs must not pre-claim remote CI before the commit exists.

- [x] Commit/push handled by delivery closeout outside the committed task snapshot.
- [x] Remote CI evidence will be reported from the actual post-push GitHub Actions run.

# Completion Standard

- Assembler output is accepted by existing multi-replica runtime gate.
- Sensitive values are rejected.
- Quick CI includes assembler pending artifact.
- Docs do not claim real multi-replica live passed.
