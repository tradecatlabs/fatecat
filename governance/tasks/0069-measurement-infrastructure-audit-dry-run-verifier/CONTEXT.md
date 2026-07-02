# Context

## Current Facts

- 0068 已新增 `contracts/fate/audit/handoff.json`、`scripts/audit-handoff.py` 和 local-ci `auditHandoff` artifact。
- 0068 明确不执行真实第三方审计，MI-100.10.04 `third-party audit dry-run` 仍未落本地 verifier。
- 当前 `scripts/local-ci.sh --profile quick` 已能生成 audit handoff bundle，但没有独立 dry-run artifact 对 bundle 做 auditor-readiness 检查。
- Roadmap 总验收仍要求第三方审计包能从 Git、CI、artifact、contract、registry、script 输出逐项复核。

## Constraints Matrix

| Constraint | Decision |
| --- | --- |
| 不替代真实第三方审计 | verifier 命名为 dry-run，只证明本地审计前置检查通过。 |
| 不伪造 live evidence | dry-run 输出包含 `shipGate.status=blocked`，只要 pending external validations 或外部 live evidence 缺口仍存在。 |
| 不遗漏 pending external validations | verifier 读取 handoff bundle 的 `pendingExternalValidationCount` 与数组长度，并要求 risk register 包含 pending risk。 |
| 不泄露敏感信息 | verifier 对 bundle JSON/Markdown 执行敏感 assignment pattern 检查。 |
| 复用 0068 输出 | dry-run 消费 `audit-handoff.json` 与 `AUDIT_HANDOFF.md`，不另建审计事实源。 |
| Change boundary | 只改 audit contracts、scripts、local-ci、tests、AGENTS、roadmap 和 0069 任务文档。 |
| Debug Evidence Contract | 调试模式: Optional。若 verifier/gate/CI 失败，再补最小复现、根因和回归证据。 |

## Change Boundary

- 允许修改：`contracts/fate/audit/`、`scripts/audit-handoff-dry-run.*`、`scripts/local-ci.sh`、`tests/regression/test_audit_handoff_dry_run.py`、`contracts/fate/AGENTS.md`、`contracts/fate/audit/AGENTS.md`、`scripts/AGENTS.md`、roadmap 和 0069 任务文档。
- 禁止修改：生产算法、真实外部凭证、真实生产域名配置、公网 Bot/live evidence、用户报告正文、外部审计结论。

## Repo Evidence

- `contracts/fate/audit/handoff.json`
- `scripts/audit-handoff.py`
- `scripts/audit-handoff.sh`
- `scripts/local-ci.sh`
- `tests/regression/test_audit_handoff.py`
- `docs/reference-materials/roadmap/测算基础设施100%实现计划.md`
- `governance/tasks/0068-measurement-infrastructure-audit-handoff-generator/`

## Critical Ambiguities

- “dry-run passed” 只表示审计包结构和风险声明可被预检，不表示审计通过。
- `shipGate=blocked` 可以和 `dryRun.status=passed` 同时成立；前者是 live/生产声明门禁，后者是本地预检门禁。
- 本任务不消除 `外部连通验证待执行`，只确保它们不会被隐藏或误写成已完成。

## Debug Evidence Contract

- 调试模式: Optional
- 0069 是 verifier/gate 新增，不是已复现 bug；如果 JSON、generator、verifier、pytest、secret scan、local-ci 或 CI 失败，必须记录最小复现、根因、修复和回归证据。

## Risk Matrix

| Risk | Mitigation |
| --- | --- |
| dry-run 被误解成真实审计通过 | contract、Markdown 和 tests 明确 non-claim 与 blocked ship gate。 |
| handoff bundle 结构坏但 local-ci 未发现 | local-ci 增加 `auditDryRun` artifact。 |
| pending external validations 被隐藏 | verifier 强制检查 count、列表和 risk register。 |
| 敏感赋值片段进入审计包 | verifier 和 regression test 禁止敏感 assignment pattern。 |

## Assumptions and Falsification

- 假设：0069 的正确最小切片是本地 dry-run verifier，而不是真实第三方审计服务接入。
- 证伪条件：如果 dry-run 允许 pending external validations 被省略、允许 final conclusion 写成 100% live complete、或缺失 risk register 仍通过，本任务失败。

## Task Package Context Map

| Node ID | Context |
| --- | --- |
| TP-01.01 | 0068 handoff bundle、local-ci artifact、roadmap MI-100.10.04 缺口。 |
| TP-02.01 | `contracts/fate/audit/dry-run.json` 是 verifier 契约。 |
| TP-02.02 | `scripts/audit-handoff-dry-run.py` 消费 handoff bundle 并输出 dry-run report。 |
| TP-03.01 | `tests/regression/test_audit_handoff_dry_run.py` 锁定 dry-run 语义。 |
| TP-03.02 | `scripts/local-ci.sh` 和 AGENTS 是接入点。 |
| TP-03.03 | roadmap 和任务索引是状态同步点。 |
| TP-04.01 | generator、verifier、pytest、ruff、secret scan 是 focused validation。 |
| TP-04.02 | quick local-ci、task validators、commit/push、remote CI 是 closeout 证据。 |
