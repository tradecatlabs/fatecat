# Acceptance Checklist

# Global Standards

- [x] 任务边界明确：0084 只做本地 provider drift scanner。
- [x] 不把 drift scanner 写成外部 live smoke 或法律复核。
- [x] 不读取真实外部 URL、token、secret、DSN、用户输入或报告正文。
- [x] 外部待验证项保留为 `外部连通验证待执行`。

# Task Package Checklists

## TP-01 SPEC: 复核 0032/0033 provider baseline 和 0083 后续队列

Verify: provider gates、registry、vendor manifest、roadmap inspected.

Gate: 不重写 provider runtime 协议。

- [x] TP-01.01 读取 provider lifecycle/dependency gate、registry、vendor manifest 和 roadmap。
- [x] TP-01.02 定义 dependency/source/license/trace drift 边界。

## TP-01.01 读取 provider lifecycle/dependency gate、registry、vendor manifest 和 roadmap

Verify: files inspected.

Gate: 确认缺的是 drift scanner，不是新 provider。

- [x] Provider lifecycle gate inspected.
- [x] Provider dependency smoke inspected.
- [x] Vendor manifest and observability trace signal inspected.

## TP-01.02 定义 dependency/source/license/trace drift 边界

Verify: task docs boundary.

Gate: local drift report 不能替代 external live。

- [x] Dependency drift boundary defined.
- [x] Source/license drift boundary defined.
- [x] Trace span boundary defined.

## TP-02 PLAN: 设计 provider drift scanner

Verify: PLAN has Future/Ponytail and scanner direction.

Gate: 不引入外部 OTel client 或公网依赖。

- [x] TP-02.01 定义 drift report contract 和 required provider fields。
- [x] TP-02.02 定义 provider span、dependency smoke、vendor license/source 校验。

## TP-02.01 定义 drift report contract 和 required provider fields

Verify: `provider-drift-contract.json`.

Gate: report fields cover provider, dependency, trace and findings.

- [x] Required report fields defined.
- [x] Required provider fields defined.
- [x] Forbidden report fragments defined.

## TP-02.02 定义 provider span、dependency smoke、vendor license/source 校验

Verify: scanner checks.

Gate: missing evidence creates finding.

- [x] provider.validate span required.
- [x] provider.calculate span required.
- [x] dependency smoke refs compared.
- [x] source/license/vendor refs checked.

## TP-03 BUILD: 实现 scanner 与接线

Verify: scripts/contracts/docs/local-ci updated.

Gate: no external service connection.

- [x] TP-03.01 新增 scanner Python 和 shell wrapper。
- [x] TP-03.02 更新 provider schema、local-ci、AGENTS、operations docs、roadmap 和 task index。

## TP-03.01 新增 scanner Python 和 shell wrapper

Verify: syntax and CLI smoke.

Gate: wrapper executable.

- [x] Python script added.
- [x] Shell wrapper added.
- [x] CLI writes report.

## TP-03.02 更新 provider schema、local-ci、AGENTS、operations docs、roadmap 和 task index

Verify: grep and tests.

Gate: docs keep external live pending.

- [x] Provider schema invariant updated.
- [x] local-ci quick writes `provider-drift-scanner.json`.
- [x] `scripts/AGENTS.md` and `contracts/fate/capabilities/AGENTS.md` updated.
- [x] operations docs updated.
- [x] roadmap and task index updated.

## TP-04 TEST: 回归和门禁

Verify: focused tests and gates.

Gate: required checks pass.

- [x] TP-04.01 新增 focused regression tests。
- [x] TP-04.02 运行 JSON、scanner、pytest、ruff、secret scan、quick CI 和任务校验。

## TP-04.01 新增 focused regression tests

Verify: focused pytest.

Gate: tests cover report, CLI and contract.

- [x] Drift report test.
- [x] CLI output test.
- [x] Contract assertion test.

## TP-04.02 运行 JSON、scanner、pytest、ruff、secret scan、quick CI 和任务校验

Verify: command output.

Gate: failures fixed or explicitly blocked.

- [x] JSON checks complete.
- [x] Scanner CLI complete.
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

- Provider drift scanner validates current production provider baseline.
- Drift report has 4 providers, 4 capabilities, 12 local provider spans and 0 findings.
- Quick CI includes provider drift scanner artifact.
- Docs do not claim real external provider live smoke、external trace backend or legal review passed.
