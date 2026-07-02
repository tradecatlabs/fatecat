# Planning Summary

本任务按 MI-100.10.04 倒推：真实第三方审计之前，FateCat 需要一个本地可重复的 audit dry-run verifier，证明 0068 handoff bundle 的结构、风险声明和外部待验证项可被审计人员预检。最小切片不接入外部审计 SaaS，不消除 live blockers，只把“审计包是否准备好交给人审”变成机器门禁。

# Lifecycle Gates

禁止跳过任何 gate；如果某个 gate 失败，0069 不能标记 Done，也不能声明 audit dry-run verifier 可交付。

| Gate | Evidence |
| --- | --- |
| SPEC | 0068 handoff 输出和 roadmap MI-100.10.04 缺口已复核。 |
| PLAN | 本任务文档定义范围、非目标、任务树和验证命令。 |
| BUILD | 新增 dry-run contract、verifier、local-ci artifact、tests 和文档接线。 |
| TEST | 运行 generator、verifier、focused pytest、ruff、secret scan、quick local-ci。 |
| REVIEW | 检查 dry-run 不夸大第三方审计或 live 证据，且 ship gate 在 pending 时保持 blocked。 |
| SHIP | 本地 quick CI 通过后提交推送；远端 GitHub Actions 作为交付事实在最终汇报中记录。 |

# Simplest Path

- 不引入外部审计 SaaS、数据库或新依赖。
- 不重复生成 handoff 事实源；只消费 0068 `audit-handoff.json` 和 `AUDIT_HANDOFF.md`。
- 用一个 verifier 同时写 JSON 和 Markdown dry-run report，并由回归测试锁定输出。
- ship/live 状态和 dry-run 状态分开表达，避免本地预检被误读成生产验收。

# Split Strategy

1. 静态契约：audit dry-run contract。
2. 验证器：handoff JSON/Markdown -> dry-run JSON/Markdown。
3. 门禁：regression tests、local-ci artifact、secret scan。
4. 文档：AGENTS、roadmap、任务容器。

# Execution Waves

| Wave | Tasks |
| --- | --- |
| 1 | TP-01.01 |
| 2 | TP-02.01、TP-02.02 |
| 3 | TP-03.01、TP-03.02、TP-03.03 |
| 4 | TP-04.01、TP-04.02 |

# Runtime Workflow Contract

- 运行入口：`bash scripts/audit-handoff-dry-run.sh --bundle-json <json> --bundle-markdown <md> --output-dir <dir>`
- 输出：`audit-dry-run.json` 和 `AUDIT_DRY_RUN.md`
- 成功条件：`kind=fatecat.audit_handoff_dry_run`、`status=passed`、必备字段/区块存在、pending count/list 一致、ship gate 在 pending 时 blocked。
- 失败处理：任何 contract 缺失、必备字段缺失、敏感 assignment pattern 出现或 false live claim 出现都直接失败。

# Next Executable Leaves

- 无。任务树已完成；后续只剩 Git 交付与远端 CI 证据。

# Dependency Graph

```text
TP-01.01 -> TP-02.01 -> TP-02.02 -> TP-03.01 -> TP-03.02 -> TP-03.03 -> TP-04.01 -> TP-04.02
```

# Rollback Protocol

- 回滚新增 `contracts/fate/audit/dry-run.json`、`scripts/audit-handoff-dry-run.*`、local-ci/test 接线和相关文档。
- 不执行 `git reset --hard` 或破坏性命令。
- 若 verifier 或 tests 失败，优先修复 dry-run 判定逻辑，而不是降低 pending/live claim 覆盖要求。

## Target End State

FateCat 可以一键生成审计交接包，并对该交接包执行本地 auditor-readiness dry-run；任何第三方审计、生产 live 或 100% 基础设施 claim 都必须继续依赖真实外部证据，否则保持 blocked/pending。

## Future-Optimal Framing

- 正确终态：audit handoff 是外部审计接口，audit dry-run 是交付前的本地预检 gate。
- 本轮切片：先做本地 dry-run verifier，再把真实第三方审计流程和 live evidence 闭合留给后续。
- Proof point：valid handoff bundle 通过 dry-run，同时输出 `shipGate.status=blocked`。
- Falsifier：dry-run 在 pending external validations 存在时输出可 ship/live complete。

## Ponytail Existence Check

- dry-run contract 应该存在：审计预检输出结构必须机器可读。
- verifier 应该存在：手工审计包检查容易遗漏 risk/non-claim 断言。
- regression test 应该存在：防止未来 dry-run 被误改成 production/live 通过。
- local-ci artifact 应该存在：审计预检是基础设施发布证据的一部分。
