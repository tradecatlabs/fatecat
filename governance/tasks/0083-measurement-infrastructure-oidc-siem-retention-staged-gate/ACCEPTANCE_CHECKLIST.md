# Acceptance Checklist

# Global Standards

- [x] 任务边界明确：0083 只加固 OIDC/SIEM/retention staged evidence gate。
- [x] 不把 staged gate 写成真实 live passed。
- [x] 不读取真实外部 URL、token、secret、audit payload 或生产数据。
- [x] 外部待验证项保留为 `外部连通验证待执行`。

# Task Package Checklists

## TP-01 SPEC: 复核 0065 与 0082 后的 security externalization 缺口

Verify: security registry、contract、policy、roadmap inspected.

Gate: 不新建第二套 security externalization gate。

- [x] TP-01.01 读取 security registry、externalization contract、production security policy 和 roadmap。
- [x] TP-01.02 定义 proof-ref/raw URL/production deletion non-claim 边界。

## TP-01.01 读取 security registry、externalization contract、production security policy 和 roadmap

Verify: security files and roadmap inspected.

Gate: 确认缺的是 gate hardening，不是新功能。

- [x] 0065 baseline confirmed as existing externalization gate.
- [x] Roadmap still marks OIDC/SIEM/retention live as external pending.
- [x] local-ci already hosts the security externalization artifact.

## TP-01.02 定义 proof-ref/raw URL/production deletion non-claim 边界

Verify: task docs boundary.

Gate: raw URL 和 production deletion marker 不能被写成 live proof。

- [x] Proof-ref allowlist defined.
- [x] Raw URL rejection defined.
- [x] Retention production deletion marker remains non-claim.

## TP-02 PLAN: 设计 0083 staged hardening

Verify: PLAN has Future/Ponytail and hardening direction.

Gate: 不引入 OIDC/JWKS/SIEM API 依赖。

- [x] TP-02.01 定义 proofRefPrefixes 和 live evidence 输入约束。
- [x] TP-02.02 定义 raw URL、retention production marker 和敏感值负例。

## TP-02.01 定义 proofRefPrefixes 和 live evidence 输入约束

Verify: `externalization-evidence-contract.json`.

Gate: live evidence proof refs 必须覆盖 identity、SIEM、retentionCleaner。

- [x] Required live fields preserved.
- [x] Proof ref prefixes allowlisted.
- [x] Raw URL endpoint evidence disallowed.

## TP-02.02 定义 raw URL、retention production marker 和敏感值负例

Verify: tests and built-in gate checks.

Gate: fake/raw/sensitive/overclaim rejected.

- [x] Raw OIDC URL evidence rejected.
- [x] Placeholder SIEM evidence rejected.
- [x] Production deletion marker evidence rejected.
- [x] token/secret fragments rejected.

## TP-03 BUILD: 加固 contract/gate/docs

Verify: contract/scripts/docs updated.

Gate: no external service connection.

- [x] TP-03.01 更新 contract 与 gate validation。
- [x] TP-03.02 更新 schema invariant、AGENTS、roadmap 和 task index。

## TP-03.01 更新 contract 与 gate validation

Verify: JSON syntax, gate smoke and tests.

Gate: gate rejects non-allowlisted proof refs.

- [x] Contract proofRefPrefixes added.
- [x] Gate proof-ref validation added.
- [x] Raw URL submitted evidence scan added.
- [x] Built-in negative cases expanded to 5.

## TP-03.02 更新 schema invariant、AGENTS、roadmap 和 task index

Verify: grep and task docs.

Gate: docs keep external live pending.

- [x] Security schema invariant updated.
- [x] `contracts/fate/security/AGENTS.md` updated.
- [x] `scripts/AGENTS.md` updated.
- [x] Roadmap 0083 row updated.
- [x] Task index updated.

## TP-04 TEST: 回归和门禁

Verify: focused tests and gates.

Gate: required checks pass.

- [x] TP-04.01 更新 focused regression tests。
- [x] TP-04.02 运行 JSON、gate、pytest、ruff、secret scan、quick CI 和任务校验。

## TP-04.01 更新 focused regression tests

Verify: focused pytest.

Gate: tests cover positive and negative paths.

- [x] Pending output test.
- [x] Proof ref prefix checks asserted.
- [x] Raw OIDC URL negative fixture rejected.
- [x] Retention production deletion marker rejected.

## TP-04.02 运行 JSON、gate、pytest、ruff、secret scan、quick CI 和任务校验

Verify: command output.

Gate: failures fixed or explicitly blocked.

- [x] JSON checks complete.
- [x] Security externalization gate complete.
- [x] Production security gate complete.
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

- OIDC/SIEM/retention staged gate validates pending contract state.
- Fake/raw/sensitive/overclaim fixtures are rejected.
- Quick CI includes security externalization gate artifact.
- Docs do not claim real OIDC/IdP、external SIEM、immutable audit storage or retention cleaner live passed.
