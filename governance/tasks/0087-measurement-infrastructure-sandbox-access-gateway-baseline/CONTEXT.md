# Context

0086 已完成 developer portal、SDK release-readiness 和 fixed sandbox output snapshot，但 sandbox token 仍是纯合同。基础设施接入不能只靠文档，需要至少一个本地可执行的 runtime access-control proof。

## Current Facts

- `contracts/fate/developer/sandbox-token-contract.json` 已定义 scope、claim 和 live negative rules。
- `src/main.py` 已有 `CapabilityExecutor` capability endpoint、global rate limit、Prometheus metrics 和 audit logger。
- `security-smoke.py` 已验证通用 API 安全护栏，但不覆盖 sandbox token scope。
- 公网 sandbox token issuer、revocation、external gateway 和生产 quota backend 当前没有真实凭证或环境。

## Design Decision

本任务新增 sandbox 专用 endpoint，而不是改变既有 public capability endpoint：

- 保持旧调用方兼容。
- 让 SDK/portal 能显式演示 sandbox auth。
- 将来接外部 issuer 时只替换 token source，不替换 capability executor。

## Risk Level

`medium`：新增 API endpoint、auth/scope 行为和 gate。无持久数据写入，无外部服务调用，无真实 secret 入仓。

## External Pending

- 外部连通验证待执行：公网 sandbox token issuer。
- 外部连通验证待执行：revocation service。
- 外部连通验证待执行：生产 API gateway / rate-limit backend。

# Repo Evidence

- `contracts/fate/developer/sandbox-token-contract.json` 已声明 sandbox token claims 和 scopes。
- `contracts/fate/developer/sandbox.json` 提供北京/测试 fixture。
- `domains/experience-delivery/services/fatecat-delivery/src/main.py` 已承载 FastAPI、rate limit、metrics 和 audit。
- `scripts/local-ci.sh` 是本地 quick gate 真相源。

# Constraints Matrix

| Constraint | Decision |
| --- | --- |
| Existing public capability endpoint compatibility | Add dedicated sandbox endpoint; do not change public endpoint behavior. |
| No real token in repo | Use local smoke env var only; summary redacts token and subject. |
| No external issuer available | Keep public token service status `not_implemented`. |
| Reuse project-native capability | Reuse FastAPI, TestClient, CapabilityExecutor, rate limit and audit logger. |

# Change Boundary

- Changed: developer contracts, delivery API endpoint, local gate, regression, docs, AGENTS, local-ci and task docs.
- Not changed: production capability registry, report profiles, bazi/ziwei logic, external deployment, SDK package publication.

# Risk Matrix

| Risk | Level | Mitigation |
| --- | --- | --- |
| Auth behavior regression | Medium | Dedicated endpoint and focused regression; old endpoint unchanged. |
| Secret leakage in gate output | Medium | secret scan, redacted summary, no request/report body persistence. |
| Live overclaim | Medium | contract booleans keep live issuer/gateway false; docs state external pending. |

# Assumptions and Falsification

- Assumption: local env-token gateway is the smallest useful proof before external issuer exists.
- Falsifier: gateway bypasses CapabilityExecutor, leaks token/subject, or cannot reject wrong scope.

# Critical Ambiguities

- Public issuer choice is intentionally unresolved: external gateway, IdP, or custom token service remains future work.
- Revocation and quota storage are future live-service tasks, not part of 0087.

# Debug Evidence Contract

- 调试模式: Optional
- This is a feature baseline, not a bugfix. If gate or CI fails, record command output and root cause before closeout.

# Task Package Context Map

## TP-01 SPEC

Context: Inspect current developer platform and runtime access gap.

## TP-02 PLAN

Context: Define local gateway contract and non-live boundaries.

## TP-03 BUILD

Context: Implement endpoint, gate, tests and docs.

## TP-04 TEST

Context: Execute local gates, focused tests, secret scan and quick CI.

## TP-05 SHIP

Context: Close task package and hand off commit/push/remote CI to delivery flow.
