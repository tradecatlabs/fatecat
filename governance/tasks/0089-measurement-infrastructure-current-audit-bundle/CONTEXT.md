# Context

0088 已完成 current release proof：可以聚合当前 commit 的 acceptance、container workflow、GHCR digest、GitHub attestation、release artifacts、rollback drill 和 git clean 证据。但第三方审计交接仍缺一个“当前 commit 审计包”：审计人员需要一份可以直接复核的 Markdown/JSON，里面包含 evidence index、risk register、pending external validations、release proof 摘要和最终 no-overclaim 结论。

## Current Facts

- `scripts/audit-handoff.py` 已能生成仓库级审计交接 Markdown/JSON。
- `scripts/audit-handoff-dry-run.py` 已能验证 handoff 结构、敏感 marker、pending 和 risk 口径。
- `scripts/current-release-proof.py` 已能在 required 模式验证当前 commit 远端发布证据。
- `scripts/release-artifacts.py` 已能生成 SBOM、provenance 和 manifest。
- `scripts/rollback-drill.py` 已能生成本地 dry-run rollback evidence。
- `scripts/local-ci.sh` quick profile 尚未把 rollback drill、current release proof 和 current audit bundle 作为一个完整审计链条输出。

## External Research Mapping

本任务延续 100% 测算基础设施同构调研：

| Infra Pattern | FateCat Mapping |
| --- | --- |
| OpenAPI / API platform contract | 审计包必须机器可读，不能只靠手写说明。 |
| Kubernetes conformance / controller evidence | 当前状态必须和期望状态逐项对照，缺证据不能 pass。 |
| SLSA / GitHub artifact attestation | release proof 必须绑定当前 commit 和可验证 provenance。 |
| CycloneDX SBOM | release artifacts 需要可校验 manifest/SBOM/provenance。 |
| OpenTelemetry evidence discipline | evidence index 应保留来源路径和状态，而不是复制敏感日志正文。 |

## Design Decision

新增 `current-audit-bundle`，而不是扩写 `audit-handoff`：

- `audit-handoff` 是仓库级审计交接包，能在本地生成，不要求 current release proof。
- `audit-dry-run` 是结构验证器，不负责聚合 release proof。
- `current-audit-bundle` 是当前 commit 交付汇总器，聚合上述产物并给出 `auditGate`。

## Risk Level

`medium`：新增发布/审计门禁脚本和 quick CI wiring；不改业务计算、不写生产数据、不访问外部 secret。

## External Pending

- 外部连通验证待执行：真实生产 API/HF live。
- 外部连通验证待执行：Telegram Bot live。
- 外部连通验证待执行：OIDC/IdP、SIEM、外部监控、告警平台。
- 外部连通验证待执行：真实第三方审计签署。

## Repo Evidence

- `contracts/fate/audit/handoff.json`
- `contracts/fate/audit/dry-run.json`
- `contracts/fate/delivery/release-gate.json`
- `scripts/audit-handoff.py`
- `scripts/audit-handoff-dry-run.py`
- `scripts/current-release-proof.py`
- `scripts/release-artifacts.py`
- `scripts/rollback-drill.py`

## Constraints Matrix

| Constraint | Decision |
| --- | --- |
| local CI cannot require remote systems | local mode allows `auditGate=blocked` but command passes when structure is valid |
| final release audit needs stronger proof | `--require-current-release` requires local-ci summary and current release proof |
| no sensitive output | forbidden marker scan and existing secret scan |
| no duplicate source of truth | consume existing audit/release/rollback outputs instead of reimplementing them |

## Change Boundary

- Changed: audit contract, scripts, local-ci, tests, AGENTS, roadmap, task index and task docs.
- Not changed: bazi/ziwei calculation, provider registry, delivery API behavior, external deployment, production credentials.

## Risk Matrix

| Risk | Level | Mitigation |
| --- | --- | --- |
| False pass from historical evidence | High | current HEAD commit checks on all supplied commit-bearing artifacts |
| Local-contract proof mistaken for release pass | High | required mode rejects local current release proof |
| Sensitive marker in bundle | Medium | forbidden marker scan + secret scan |
| Audit handoff drift | Medium | current bundle consumes handoff JSON/Markdown and dry-run output |

## Assumptions and Falsification

- Assumption: current audit bundle is the smallest useful next audit infrastructure slice after 0088.
- Falsifier: script accepts旧 commit、遗漏 pending external validations、required 模式接受 local-contract proof，或 quick CI 不能生成 bundle。

## Critical Ambiguities

- 第三方审计平台/签署格式未选型，保留为后续外部集成。
- 真实生产 API/HF/Bot live 仍由 release/live gates 单独证明，不在本任务伪造。

## Debug Evidence Contract

- 调试模式: Optional
- If bundle generation fails, capture exact failing evidence ID and command before changing gate policy.

## Task Package Context Map

## TP-01 SPEC

Context: Inspect current 0088 release proof and missing audit aggregation layer.

## TP-02 PLAN

Context: Define current audit bundle contract, modes and non-claims.

## TP-03 BUILD

Context: Implement generator, wrapper, contract, local-ci wiring and regression.

## TP-04 TEST

Context: Execute focused checks and quick CI.

## TP-05 SHIP

Context: Commit/push, then run required release proof and current audit bundle for final HEAD.
