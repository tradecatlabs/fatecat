# Acceptance Checklist

# Global Standards

- [x] 任务边界明确：0082 只做 OTel backend/SLO staged gate。
- [x] 不把 staged gate 写成真实 live passed。
- [x] 不读取真实外部 URL、token、secret、trace、metrics 或日志。
- [x] 外部待验证项保留为 `外部连通验证待执行`。

# Task Package Checklists

## TP-01 SPEC: 复核 0064 与 0081 后的 observability 缺口

Verify: registry、0064 gate、roadmap inspected.

Gate: 不重写 0064 dry-run gate。

- [x] TP-01.01 读取 registry、SLO evidence contract、roadmap 和 local-ci。
- [x] TP-01.02 定义 staged gate 的 pending/live/non-claim 边界。

## TP-01.01 读取 registry、SLO evidence contract、roadmap 和 local-ci

Verify: observability files and roadmap inspected.

Gate: 确认缺的是 backend/SLO staged evidence gate。

- [x] 0064 gate confirmed as dry-run collector/SLO baseline.
- [x] Roadmap still marks OTel backend/SLO live as external pending.
- [x] local-ci can host a staged artifact.

## TP-01.02 定义 staged gate 的 pending/live/non-claim 边界

Verify: task docs boundary.

Gate: pending 不能被写成 live passed。

- [x] Pending mode defined.
- [x] Live evidence mode requires complete redacted proof refs.
- [x] Production SLO/alert/incident drill remain non-claims until external evidence exists.

## TP-02 PLAN: 设计 OTel backend/SLO evidence contract

Verify: PLAN has Future/Ponytail and schema direction.

Gate: 不引入 OTel SDK/exporter 依赖。

- [x] TP-02.01 定义 live evidence schema 与 proof ref 白名单。
- [x] TP-02.02 定义反伪造负例和敏感值防护。

## TP-02.01 定义 live evidence schema 与 proof ref 白名单

Verify: `otel-backend-slo-evidence-contract.json`.

Gate: live evidence 字段必须覆盖 backend、SLO、alert、incident drill。

- [x] Required backend/SLO fields mapped.
- [x] Proof ref prefixes allowlisted.
- [x] Backend types allowlisted.

## TP-02.02 定义反伪造负例和敏感值防护

Verify: tests and built-in gate checks.

Gate: fake/local/sensitive/overclaim rejected.

- [x] localhost/backend fake fragments rejected.
- [x] placeholder/sample/debug fragments rejected.
- [x] token/secret/raw URL fragments rejected.

## TP-03 BUILD: 实现 gate 与接线

Verify: scripts/contracts/docs/local-ci updated.

Gate: no external service connection.

- [x] TP-03.01 新增 Python gate 与 shell wrapper。
- [x] TP-03.02 更新 observability registry/schema、local-ci 和文档。

## TP-03.01 新增 Python gate 与 shell wrapper

Verify: syntax and CLI smoke.

Gate: wrapper executable.

- [x] Python script added.
- [x] Shell wrapper added.
- [x] Pending CLI works.
- [x] Live fixture validates through tests.

## TP-03.02 更新 observability registry/schema、local-ci 和文档

Verify: local-ci and docs grep.

Gate: docs keep external live pending.

- [x] observability registry links contract and signal.
- [x] observability schema includes staged evidence fields and invariant.
- [x] local-ci quick writes `otel-backend-slo-gate.json`.
- [x] `scripts/AGENTS.md` and `contracts/fate/observability/AGENTS.md` updated.
- [x] roadmap/API docs updated.

## TP-04 TEST: 回归和门禁

Verify: focused tests and gates.

Gate: required checks pass.

- [x] TP-04.01 新增 focused regression tests。
- [x] TP-04.02 运行 syntax、pytest、ruff、secret scan、quick CI 和任务校验。

## TP-04.01 新增 focused regression tests

Verify: focused pytest.

Gate: tests cover positive and negative paths.

- [x] Pending output test.
- [x] Live fixture accepted.
- [x] Missing required live proof rejected.
- [x] Sensitive/raw URL evidence rejected.
- [x] Registry/schema linkage tested.

## TP-04.02 运行 syntax、pytest、ruff、secret scan、quick CI 和任务校验

Verify: command output.

Gate: failures fixed or explicitly blocked.

- [x] Syntax checks complete.
- [x] Focused pytest complete.
- [x] Ruff complete.
- [x] Secret scan complete.
- [x] Quick CI complete.
- [x] Task validators complete.

## TP-05 REVIEW/SHIP: 收口

Verify: no overclaim.

Gate: tracked task docs do not pre-claim remote CI.

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

- OTel backend/SLO staged gate validates pending contract state.
- Complete redacted live fixture is accepted; fake/local/sensitive/overclaim fixtures are rejected.
- Quick CI includes staged gate artifact.
- Docs do not claim real OTel backend, production SLO, alert live or incident drill passed.
