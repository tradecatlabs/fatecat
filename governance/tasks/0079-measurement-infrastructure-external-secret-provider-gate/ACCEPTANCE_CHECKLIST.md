# Acceptance Checklist

# Global Standards

- [x] 任务边界明确：0079 只做 external secret provider evidence gate baseline。
- [x] 本地 Fernet vault 不被写成 external Vault/KMS。
- [x] Contract、gate、registry/schema/policy、local-ci、tests 和 docs 已接线。
- [x] 外部待验证项未被伪造成完成。
- [x] quick CI 和 task validators 通过。

# Task Package Checklists

## TP-01 现状复核与任务定界

Verify: 0059/0078 docs、runtime backend contract、security gate files 已读取。

Gate: 不重复 local vault smoke，不把旧证据写成 production secret lifecycle。

- [x] TP-01.01 已复核本地 vault 与 runtime 缺口。
- [x] TP-01.02 已复核 security 接线点。

## TP-01.01 复核 0059/0078 本地 vault 与 runtime 缺口

Verify: `webhook_config_store.py`、`webhook-config-vault-smoke.py`、runtime backend contract inspected.

Gate: 0079 scope does not include real external Vault/KMS live.

- [x] 已确认 0059 只证明 local Fernet encrypted-at-rest。
- [x] 已确认 0078 不证明 external secret lifecycle。

## TP-01.02 复核 security registry/schema/gate 接线点

Verify: security schema/registry/policy/gate/local-ci inspected.

Gate: new contract must be wired into an executable gate.

- [x] Registry and schema touch points located.
- [x] local-ci artifact touch point located.

## TP-02 外部 secret provider 契约

Verify: JSON parse and gate validation.

Gate: contract must not contain raw secret values.

- [x] TP-02.01 evidence contract added.
- [x] TP-02.02 negative/live schema added.

## TP-02.01 新增 external-secret-provider evidence contract

Verify: `python3 -m json.tool contracts/fate/security/external-secret-provider-contract.json`.

Gate: contract includes privacy and release boundary.

- [x] Contract file exists.
- [x] Contract parses.

## TP-02.02 新增反伪造负例与 live evidence schema

Verify: `bash scripts/external-secret-provider-gate.sh`.

Gate: fake local/placeholder/missing-audit evidence rejected.

- [x] Negative cases present.
- [x] Live schema requires key reference, rotation, access audit and application injection proof.

## TP-03 Security control/gate 接线

Verify: production-security gate and local-ci.

Gate: security registry status remains manual/external pending.

- [x] TP-03.01 schema/registry/policy updated.
- [x] TP-03.02 gate script added.
- [x] TP-03.03 local-ci connected.

## TP-03.01 更新 SecurityControl schema/registry/policy

Verify: `bash scripts/production-security-gate.sh`.

Gate: `control.external_secret_provider_kms` is manual/external pending.

- [x] `secret_provider` control type added.
- [x] Registry and policy metadata linked.

## TP-03.02 新增 external-secret-provider-gate.py/.sh

Verify: gate output JSON.

Gate: summary redacted and fake evidence rejected.

- [x] Python gate added.
- [x] Shell wrapper executable.

## TP-03.03 接入 local-ci artifact

Verify: `local-ci.sh` step and summary artifact key.

Gate: quick CI must run the gate.

- [x] local-ci run step added.
- [x] summary artifact key added.

## TP-04 Tests and docs

Verify: focused tests and docs grep.

Gate: no live overclaim.

- [x] TP-04.01 regression tests added.
- [x] TP-04.02 docs/AGENTS updated.

## TP-04.01 增加 regression tests

Verify: focused pytest.

Gate: tests cover contract, negative cases, redacted live evidence and privacy.

- [x] Regression test file added.
- [x] Existing security tests updated.

## TP-04.02 更新 roadmap、operations docs 和 AGENTS

Verify: docs updated.

Gate: external Vault/KMS remains pending.

- [x] Roadmap updated.
- [x] Operations docs updated.
- [x] AGENTS updated.

## TP-05 Verify/closeout/ship

Verify: focused gates, quick CI, task validators, git/CI evidence.

Gate: no failing required checks.

- [x] TP-05.01 validation gates complete.
- [x] TP-05.02 closeout and Git delivery complete.

## TP-05.01 运行 focused gates、ruff/format 和 quick CI

Verify: command output.

Gate: failures fixed or explicitly blocked.

- [x] Focused gates complete.
- [x] Focused tests and ruff complete.
- [x] Quick CI complete.
- [x] Task validators complete.

## TP-05.02 回填任务 closeout、提交、推送并记录 CI

Verify: git status/commit/push/CI evidence.

Gate: worktree clean and remote evidence recorded.

- [x] Task docs closed.
- [x] Commit pushed.
- [x] Remote CI evidence recorded.
