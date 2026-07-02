# Planning Summary

本任务按“测算基础设施”的正确终态倒推：第三方审计必须能拿到一键生成、机器可读、路径可复核、风险不隐藏的 handoff bundle。最小切片不完成外部 live evidence，也不替代第三方审计；只把仓库内证据和所有 pending external validations 聚合成 Markdown/JSON。

# Lifecycle Gates

禁止跳过任何 gate；如果某个 gate 失败，0068 不能标记 Done，也不能声明 audit handoff bundle 可交付。

| Gate | Evidence |
| --- | --- |
| SPEC | 0061 roadmap、任务 closeout 分散现状、release gate 和 pending external validation 事实已复核。 |
| PLAN | 本任务文档定义范围、非目标、任务树和验证命令。 |
| BUILD | 新增 audit handoff contract、generator、local-ci artifact、tests 和文档接线。 |
| TEST | 运行 generator、focused pytest、ruff、secret scan、quick local-ci。 |
| REVIEW | 检查 pending external validations 不遗漏、敏感赋值不输出、live claim 不夸大。 |
| SHIP | 本地 quick CI 通过后提交推送；远端 GitHub Actions 作为交付事实在最终汇报中记录。 |

# Simplest Path

- 不引入外部审计 SaaS、数据库或新依赖。
- 不解析所有历史 closeout packet 的自由文本结论。
- 复用 Git、任务索引、关键 contracts、local-ci summary 和 GitHub acceptance 查询入口。
- 用一个 generator 同时写 JSON 和 Markdown，并由回归测试锁定输出。

# Split Strategy

1. 静态契约：audit handoff contract。
2. 生成器：Git/task/contracts/pending scan -> JSON/Markdown。
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

- 运行入口：`bash scripts/audit-handoff.sh --output-dir <dir>`
- 输出：`audit-handoff.json` 和 `AUDIT_HANDOFF.md`
- 成功条件：`kind=fatecat.audit_handoff_bundle`、`status=passed`、`pendingExternalValidationCount == tracked + untracked non-ignored occurrence count`、Markdown 包含必备审计区块。
- 失败处理：任何 contract 缺失、pending count 不一致、必备 Markdown 区块缺失或敏感 assignment pattern 出现都直接失败。

# Next Executable Leaves

- 无。任务树已完成；后续只剩 Git 交付与远端 CI 证据。

# Dependency Graph

```text
TP-01.01 -> TP-02.01 -> TP-02.02 -> TP-03.01 -> TP-03.02 -> TP-03.03 -> TP-04.01 -> TP-04.02
```

# Rollback Protocol

- 回滚新增 `contracts/fate/audit/`、`scripts/audit-handoff.*`、local-ci/test 接线和相关文档。
- 不执行 `git reset --hard` 或破坏性命令。
- 若 generator 或 tests 失败，优先修复证据聚合逻辑，而不是降低 pending external validation 覆盖要求。

## Target End State

FateCat 可以一键生成第三方审计交接包，包含 Git 状态、任务索引、代码资产、证据入口、风险登记、验证结果和所有 pending external validations；任何生产 live claim 都必须有外部证据，否则保持 blocked/pending。

## Future-Optimal Framing

- 正确终态：audit handoff 是测算基础设施 release gate 的外部审计接口，而不是聊天总结。
- 本轮切片：先做本地可复现 bundle，再把外部审计流程和 live evidence 闭合留给后续。
- Proof point：生成器输出的 pendingExternalValidationCount 与 tracked + untracked non-ignored occurrence count 完全一致。
- Falsifier：审计包遗漏任何 tracked `外部连通验证待执行`，或把本地 contract baseline 说成 live evidence。

## Ponytail Existence Check

- audit contract 应该存在：第三方审计输出结构必须机器可读。
- generator 应该存在：手工拼 Markdown 容易遗漏 pending external validations。
- regression test 应该存在：防止未来新增外部待验证项后审计包漏列。
- local-ci artifact 应该存在：审计包是基础设施发布证据的一部分。
