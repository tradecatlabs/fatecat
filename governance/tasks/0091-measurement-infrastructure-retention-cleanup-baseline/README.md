# Task Overview
- Task ID: `0091`
- Slug: `measurement-infrastructure-retention-cleanup-baseline`
- Objective: `把 retention cleanup 从计划和 evidence contract 推进为本地可执行 SQLite records/report jobs 清理 baseline，并接入 security contract、production-security gate、local-ci 和回归测试。`
- Status: `Done`

## In Scope

- 新增本地 `retention_cleanup.py` 领域薄编排，覆盖 SQLite `records` 与 `report_jobs` 过期终态数据清理。
- 新增 `scripts/retention-cleanup.py/.sh` 和 `scripts/retention-cleanup-smoke.py/.sh`。
- 新增 `contracts/fate/security/retention-cleanup.json`，并接入 `registry.json`、`production-security-policy.json`、`externalization-evidence-contract.json`。
- 将 smoke 接入 `scripts/local-ci.sh` quick profile 和 `summary.json` artifact。
- 新增 `tests/regression/test_retention_cleanup.py` 与 production security gate 断言。
- 更新相关 AGENTS、roadmap 和 task index。

## Out of Scope

- 不接入生产 scheduler、cron 或长期后台 worker。
- 不执行真实 Postgres production cleanup live smoke。
- 不接入外部 SIEM/WORM/不可变审计存储 retention。
- 不删除真实生产数据，不保存真实删除 proof。
- 不把本地 smoke 写成 public production release evidence。

## Future-Optimal Task Contract

| Field | Value |
| --- | --- |
| Target end state | retention 是可执行、可审计、可复核的基础设施控制面：policy/contract/script/local-ci/evidence 一致，生产 live 由外部证据证明。 |
| Real constraints | 当前仓库可本地验证 SQLite records/report jobs；生产 scheduler、Postgres production cleanup 和 SIEM retention 依赖外部环境。 |
| Inertia constraints | 0038/0065 已有 policy/evidence contract，但缺少真实本地清理器，容易停在“计划已写”的假完成。 |
| Wrong concept / wrong boundary | 把 retention policy 登记或 externalization evidence schema 当成清理器实现。 |
| Kill list | 删除真实生产数据；输出 recordId/jobId/userId；把 dry-run 写成 execute；把本地 SQLite smoke 写成生产 live。 |
| Proof point | `retention-cleanup-smoke.sh` 显示 dry-run 候选但不删，execute 删除过期 record/终态 job 及关联行，并保持 summary 脱敏。 |
| Falsifier | smoke 输出用户/任务明文；running job 被删；缺库时报错；production-security gate 不知道 retention cleanup script。 |
| Migration slice | 先做本地 SQLite baseline；后续做 scheduler、Postgres live、SIEM retention 和生产删除审计 evidence。 |
| Rejected short-term patches | 不只改文档；不只在 production-security gate 里加检查；不绕过 contract/registry。 |
| Future-optimal review owner | `auto-review: future-optimal-drift` |

## Ponytail Task Contract

| Field | Value |
| --- | --- |
| Existence check | 持久记录和异步报告任务一旦进入生产，必须具备可验证保留和清理路径；本地清理 baseline 是进入外部生产 evidence 前的最小必要对象。 |
| Selected ladder rung | project-native script + existing SQLite stores；自研只做薄编排、计数、删除和脱敏 summary。 |
| Skipped scope | scheduler、Postgres production cleanup live、SIEM retention、WORM、真实 production delete audit proof。 |
| Ceiling / upgrade path | 后续把同一 contract 扩展到 scheduled runner、Postgres adapter 和外部 SIEM proof refs。 |
| Do-not-simplify | 不删除非终态 running job；不输出明文 ID；不在缺外部证据时声明 live passed。 |
| Minimal runnable check | `bash scripts/retention-cleanup-smoke.sh --output-json <path>` |
| Complexity review owner | `auto-review: ponytail-complexity` |

## Document-Driven Task Contract

| Field | Value |
| --- | --- |
| Operating model update | not needed：项目定位不变。 |
| Toolchain model update | updated：新增 retention cleanup runner/smoke 并进入 quick local-ci。 |
| Process update | updated：retention policy 变更需要 smoke 和脱敏 summary。 |
| Source-of-truth updates | updated：security contract、registry、policy、externalization contract、roadmap、task index。 |
| Local README/AGENTS impact | updated：delivery/security/contracts/scripts/tests AGENTS。 |
| Contract/catalog/schema impact | updated：新增 `contracts/fate/security/retention-cleanup.json`。 |
| ADR/Gate/module-context impact | not needed：沿用 SecurityControl registry 和 production-security gate。 |
| Documentation exemption reason | none。 |
| Validation evidence | retention smoke、focused pytest、production-security gate、ruff、secret scan、quick CI 和 post-push remote CI。 |

## Task Package Tree

```text
TP-01 SPEC: 确认 retention cleaner 灯下黑缺口
TP-02 PLAN: 定义本地 SQLite baseline、脱敏 summary 和外部 pending 边界
TP-03 BUILD: 实现清理器、脚本、contract、gate/local-ci/docs/tests
TP-04 TEST: 运行 retention smoke、focused pytest、ruff、secret scan、quick CI
TP-05 SHIP: commit/push，触发远端 CI，收集证据
```

## Key Deliverables

- `domains/experience-delivery/services/fatecat-delivery/src/retention_cleanup.py`
- `contracts/fate/security/retention-cleanup.json`
- `scripts/retention-cleanup.py`
- `scripts/retention-cleanup.sh`
- `scripts/retention-cleanup-smoke.py`
- `scripts/retention-cleanup-smoke.sh`
- `tests/regression/test_retention_cleanup.py`
- `scripts/local-ci.sh`

## Reading Order

1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
