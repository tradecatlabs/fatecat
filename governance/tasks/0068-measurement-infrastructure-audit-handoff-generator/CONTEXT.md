# Context

## Current Facts

- 当前 0061 后续路线图把 0068 定义为 `audit handoff generator`。
- 0010-0067 已经有分散的任务 closeout、gate、registry、release evidence 和 local-ci artifact。
- `scripts/live-release-gate.py` 已能标注 live release 仍 blocked，但缺第三方审计包聚合。
- `governance/tasks/INDEX.md` 是任务状态入口。
- 仓库内多处明确写有 `外部连通验证待执行`；0068 的核心风险是审计包遗漏这些待验证项。

## Constraints Matrix

| Constraint | Decision |
| --- | --- |
| 不遗漏 pending external validations | generator 使用 `git grep -n -I 外部连通验证待执行` 扫描 tracked files，并补扫 untracked non-ignored first-party text files，在 JSON 中逐条列出 path/line/excerpt。 |
| 不伪造 live evidence | audit handoff 明确只是 repository-local handoff bundle，不替代 production API/Bot/OIDC/SIEM/monitoring live proof。 |
| 不泄露敏感信息 | bundle 校验禁止 `token=`、`secret=`、`password=` 等敏感赋值片段进入输出。 |
| 复用已有证据入口 | 聚合 Git、任务索引、release gate、local-ci summary、GitHub acceptance run 查询入口和关键 contracts。 |
| Change boundary | 只改 audit contracts、scripts、local-ci、tests、AGENTS、roadmap 和 0068 任务文档。 |
| Debug Evidence Contract | 调试模式: Optional。0068 是 generator/gate 新增，不是已复现 bug；若 gate/test 失败再补 DEBUG 证据。 |

## Change Boundary

- 允许修改：`contracts/fate/audit/`、`scripts/audit-handoff.*`、`scripts/local-ci.sh`、`tests/regression/test_audit_handoff.py`、`contracts/fate/AGENTS.md`、`scripts/AGENTS.md`、roadmap 和 0068 任务文档。
- 禁止修改：生产算法、真实外部凭证、真实生产域名配置、公网 Bot/live evidence、用户报告正文、外部审计结论。
- 本轮只落本地 audit handoff generator baseline；第三方审计人员独立复核和 live evidence 全闭环归后续任务。

## Repo Evidence

- `docs/reference-materials/roadmap/测算基础设施100%实现计划.md`
- `governance/tasks/INDEX.md`
- `contracts/fate/delivery/release-gate.json`
- `contracts/fate/security/registry.json`
- `contracts/fate/observability/registry.json`
- `scripts/live-release-gate.py`
- `scripts/local-ci.sh`
- `contracts/fate/audit/handoff.json`
- `scripts/audit-handoff.py`
- `tests/regression/test_audit_handoff.py`

## Critical Ambiguities

- “audit handoff” 不是“第三方审计已完成”；它只是可交付给第三方复核的 evidence bundle。
- “pending external validations” 不能靠人工挑选摘要；本轮用 tracked + untracked non-ignored occurrence 全量扫描防遗漏。
- “local-ci artifact” 不能写成 live production evidence。

## Debug Evidence Contract

- 调试模式: Optional
- 0068 是 generator/gate 新增，不是已复现 bug；如果 JSON、generator、pytest、secret scan、local-ci 或 CI 失败，必须记录最小复现、根因、修复和回归证据。

## Risk Matrix

| Risk | Mitigation |
| --- | --- |
| 审计包遗漏待外部验证项 | 测试断言 generator count 等于 tracked + untracked non-ignored occurrence count。 |
| 审计包夸大本地 contract baseline | Final Conclusion 明确生产 100% 和 live claim 仍 blocked。 |
| 审计包泄露敏感赋值片段 | generator 和测试禁止敏感 assignment pattern。 |
| local-ci 未产出审计包 | quick profile 增加 `auditHandoff` artifact。 |
| 任务 closeout 与真实验证不一致 | 任务 closeout 前运行 task validators 和 quick local-ci。 |

## Assumptions and Falsification

- 假设：0068 的最小正确切片是本地可复现生成审计 Markdown/JSON，而不是实际完成第三方人工审计。
- 证伪条件：如果 bundle 中 pendingExternalValidationCount 小于 tracked + untracked non-ignored occurrence 结果、或输出把外部 live 验证写成已完成，本任务失败。

## Task Package Context Map

| Node ID | Context |
| --- | --- |
| TP-01.01 | 0061 roadmap、governance/tasks/INDEX、release gate、local-ci 和外部待验证文本。 |
| TP-02.01 | `contracts/fate/audit/handoff.json` 是 audit handoff 契约。 |
| TP-02.02 | `scripts/audit-handoff.py` 生成 Markdown/JSON bundle。 |
| TP-03.01 | `tests/regression/test_audit_handoff.py` 锁定不遗漏外部待验证项。 |
| TP-03.02 | `scripts/local-ci.sh` 和 AGENTS 是接入点。 |
| TP-03.03 | roadmap 和任务索引是状态同步点。 |
| TP-04.01 | generator、pytest、ruff、secret scan 是 focused validation。 |
| TP-04.02 | quick local-ci、task validators、commit/push、remote CI 是 closeout 证据。 |
