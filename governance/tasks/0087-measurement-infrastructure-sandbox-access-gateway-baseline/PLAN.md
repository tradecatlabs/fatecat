# Planning Summary

0087 advances developer platform runtime access by adding a local sandbox access gateway baseline. The proof is a dedicated sandbox endpoint guarded by env-only scoped smoke tokens, with contract and gate evidence proving auth failure, wrong-scope failure, successful capability execution, rate limit and audit redaction.

# Lifecycle Gates

SPEC -> PLAN -> BUILD -> TEST -> REVIEW -> SHIP 不得跳过 gate；任一阶段缺少证据时，后续阶段只能记录为 pending，不能声明完成。

| Phase | Gate |
| --- | --- |
| SPEC | Existing developer contracts and delivery runtime controls inspected. |
| PLAN | Public issuer/revocation/gateway live evidence kept out of scope. |
| BUILD | Endpoint reuses `CapabilityExecutor`, existing rate limit and audit logger. |
| TEST | Sandbox gateway gate, developer gates, focused pytest, ruff, secret scan and quick CI pass. |
| REVIEW | Document drift, no-live-overclaim and secret leakage reviewed. |
| SHIP | Task docs closeout, commit, push and remote acceptance. |

# Simplest Path

- Add one local gateway contract.
- Add one dedicated sandbox endpoint family.
- Add one gate script and one regression file.
- Reuse existing OpenAPI, capability executor, rate limit, metrics and audit primitives.

# Split Strategy

- TP-01/02 define evidence and boundary.
- TP-03 implements code/contracts/docs/tests.
- TP-04 validates locally.
- TP-05 handles delivery closeout.

# Execution Waves

| Wave | Nodes |
| --- | --- |
| W1 | TP-01, TP-02 |
| W2 | TP-03 |
| W3 | TP-04 |
| W4 | TP-05 |

# Runtime Workflow Contract

- Input: sandbox fixture payload + `Authorization: Bearer <sandbox-token>`.
- Token source: local `FATE_SANDBOX_TOKENS` env only.
- Control flow: parse token -> verify scope -> execute `CapabilityExecutor` -> emit redacted audit -> return branded capability payload.
- Side effects: audit log only; no database writes and no external calls.

# Next Executable Leaves

| Node ID | Action |
| --- | --- |
| - | - |

# Dependency Graph

```text
TP-01 -> TP-02 -> TP-03 -> TP-04 -> TP-05
```

# Rollback Protocol

- Remove sandbox endpoint helpers and routes from `src/main.py`.
- Remove sandbox gateway contract/gate/test/local-ci wiring.
- Revert docs and AGENTS changes.
- Public capability endpoint remains unchanged, so rollback does not require API migration.

# Plan

## TP-01 SPEC

- 复核 developer contracts、portal、sandbox fixture、delivery API、rate limit、audit、metadata 和 local-ci。
- 确认不能宣称公网 live。

## TP-02 PLAN

- 设计 `sandbox-access-gateway.json`：
  - scope -> capability -> fixture -> endpoint。
  - runtime controls：scope、rate limit、audit、metrics。
  - validation gate 和 negative rules。
- 定义 endpoint：
  - `/sandbox/capabilities/{capability_id}/calculate`
  - `/api/v1/sandbox/capabilities/{capability_id}/calculate`

## TP-03 BUILD

- 在 `src/main.py` 复用 `CapabilityExecutor` 实现 sandbox endpoint。
- 新增 gate 脚本和 regression。
- 更新 developer platform/portal gate、docs、AGENTS、roadmap、INDEX 和 local-ci。

## TP-04 TEST

- `bash scripts/sandbox-access-gateway-gate.sh`
- `bash scripts/developer-platform-gate.sh`
- `bash scripts/developer-portal-gate.sh`
- focused pytest。
- ruff check / format check。
- quick CI。

## TP-05 SHIP

- closeout 任务包。
- 提交并推送。
- 触发远端 acceptance。
