# Task Overview
- Task ID: `0087`
- Slug: `measurement-infrastructure-sandbox-access-gateway-baseline`
- Objective: `把 sandbox token contract 从纯契约推进为本地可执行的 sandbox access gateway baseline，验证 scope、限流、审计脱敏和 OpenAPI 暴露。`
- Status: `Done`

## In Scope

- 新增 `sandbox-access-gateway.json` 机器契约。
- 新增 `/sandbox/capabilities/{capability_id}/calculate` 与 `/api/v1/sandbox/capabilities/{capability_id}/calculate` 本地 sandbox gateway。
- 复用 `CapabilityExecutor`、全局 rate limit、metrics 和 audit event，不新建第二套计算或限流核心。
- 新增 `sandbox-access-gateway-gate.py/.sh`，验证缺 token、错 scope、成功执行、限流、audit 脱敏和 OpenAPI path。
- 更新 developer platform/portal gate、docs、AGENTS、local-ci 和 regression。

## Out of Scope

- 不实现公网 sandbox token issuer。
- 不实现 token revocation service。
- 不实现生产 API gateway、租户计费或 quota backend。
- 不保存真实 token、secret、生产 URL、用户输入、报告正文或非北京真实地区。

## Future-Optimal Task Contract

| Field | Value |
| --- | --- |
| Target end state | 开发者 access gateway 是统一 capability runtime 前的标准入口，scope、rate limit、audit、metrics、OpenAPI、SDK 与 sandbox issuer 可逐步外部化。 |
| Real constraints | 现有 public `/capabilities/...` 不能破坏；公网 issuer/secret 不在当前环境；必须继续保护隐私示例和 no-live-overclaim。 |
| Inertia constraints | 旧 sandbox fixture endpoint、docs smoke 和本地 token contract 不能决定最终公网 issuer 形态。 |
| Wrong concept / wrong boundary | 把 fixture/snapshot 当成 token service；把本地 env smoke token 当成生产密钥。 |
| Kill list | 纯文档 token contract、无 runtime enforcement、无 audit/rate-limit evidence 的 developer sandbox。 |
| Proof point | `sandbox-access-gateway-gate.sh` 真实通过 TestClient 打 sandbox endpoint，并记录脱敏 summary。 |
| Falsifier | sandbox endpoint 绕过 `CapabilityExecutor`、输出 token、不能拒绝错 scope，或 gate 把公网 live 写成 true。 |
| Migration slice | 先落本地 executable gateway，未来替换 token 来源为外部 issuer/gateway 而不改 capability executor。 |
| Rejected short-term patches | 不在原 public capability endpoint 上加隐藏条件；不把 docs smoke 伪造成 token issuer。 |
| Future-optimal review owner | `auto-review: future-optimal-drift` |

## Ponytail Task Contract

| Field | Value |
| --- | --- |
| Existence check | 0086 已有 developer portal 和 token contract，但没有可执行 access-control 证据；基础设施接入必须验证运行时护栏。 |
| Selected ladder rung | project-native capability + direct implementation，复用现有 FastAPI、CapabilityExecutor、rate limiter、audit logger。 |
| Skipped scope | 公网 issuer、revocation、billing/quota、external gateway、OIDC、SDK 发布。 |
| Ceiling / upgrade path | 当需要真实外部开发者接入时，升级为外部 token issuer、gateway rate-limit backend、revocation smoke 和 quota store。 |
| Do-not-simplify | 不泄露 token/subject/request/report；不改变旧 public capability endpoint；不跳过 scope enforcement。 |
| Minimal runnable check | `bash scripts/sandbox-access-gateway-gate.sh` |
| Complexity review owner | `auto-review: ponytail-complexity` |

## Document-Driven Task Contract

| Field | Value |
| --- | --- |
| Operating model update | not needed：项目定位不变。 |
| Toolchain model update | updated：新增 `sandbox-access-gateway-gate.sh` 并接入 `local-ci.sh`。 |
| Process update | not needed：仍按本地 gate + CI 口径执行。 |
| Source-of-truth updates | updated：developer contracts、API changelog、roadmap、docs、AGENTS。 |
| Local README/AGENTS impact | updated：delivery/scripts/contracts/tests AGENTS 与 developer docs。 |
| Contract/catalog/schema impact | updated：新增 developer gateway contract，未新增 catalog resource。 |
| ADR/Gate/module-context impact | not needed：本轮是已有 developer platform 的可执行切片。 |
| Documentation exemption reason | none。 |
| Validation evidence | gate、focused pytest、quick CI 待 closeout 填充。 |

## Task Package Tree

```text
TP-01 SPEC: 识别 0086 后 developer runtime access 缺口
TP-02 PLAN: 定义本地 sandbox gateway baseline
TP-03 BUILD: 实现 gateway endpoint、contract、gate、docs 和 wiring
TP-04 TEST: 运行 gate、focused pytest、ruff、quick CI
TP-05 SHIP: 更新任务状态、提交、推送、远端 acceptance
```

## Key Deliverables

- `contracts/fate/developer/sandbox-access-gateway.json`
- `domains/experience-delivery/services/fatecat-delivery/src/main.py`
- `scripts/sandbox-access-gateway-gate.py`
- `scripts/sandbox-access-gateway-gate.sh`
- `tests/regression/test_sandbox_access_gateway_gate.py`

## Requirement Alignment

| Requirement | Implementation |
| --- | --- |
| local executable sandbox gateway | `src/main.py` adds `/sandbox/capabilities/{capability_id}/calculate` and `/api/v1/sandbox/capabilities/{capability_id}/calculate` |
| sandbox token scope enforcement | `FATE_SANDBOX_TOKENS` parser + `capability:calculate:<id>` scope checks |
| rate-limit and audit proof | `sandbox-access-gateway-gate.py` verifies 429 and redacted `sandbox.capability.calculate` audit event |
| no public issuer overclaim | contracts keep live public token service `not_implemented` |
| CI coverage | `local-ci.sh` runs sandbox gateway gate and focused regression |

## Task Package Overview

| Node ID | Title | Status | Acceptance |
| --- | --- | --- | --- |
| TP-01 | SPEC | Done | 0086 gap and existing runtime controls inspected |
| TP-02 | PLAN | Done | gateway contract and endpoint boundary defined |
| TP-03 | BUILD | Done | code, contract, gate, docs and tests implemented |
| TP-04 | TEST | Done | gates, focused tests, secret scan and quick CI passed |
| TP-05 | SHIP | Done | local closeout done; remote CI handled after commit/push |

## Reading Order

1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
