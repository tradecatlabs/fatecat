# Planning Summary

本任务按“测算基础设施”的正确终态倒推：核心能力进入生产前必须有统一质量语料清单、报告结构 diff 策略、隐私边界和本地门禁。最小切片不重写八字/紫微算法，只把已有 fixture 和 smoke 提升为一等质量资产。

# Lifecycle Gates

禁止跳过任何 gate；如果某个 gate 失败，0066 不能标记 Done，也不能声明核心质量语料或 report diff policy 已可发布。

| Gate | Evidence |
| --- | --- |
| SPEC | 0061 roadmap、现有 golden fixture、evaluation registry 已复核。 |
| PLAN | 本任务文档定义范围、非目标、任务树和验证命令。 |
| BUILD | 新增 manifest、policy、gate、紫微样本、registry/local-ci 接线。 |
| TEST | 运行 core-quality-corpus gate、focused pytest、ruff、quick local-ci。 |
| REVIEW | 检查隐私边界、productionBoundary、registry 资源和文档一致性。 |
| SHIP | 本地 quick CI 通过后提交推送；远端 GitHub Actions 作为交付事实在最终汇报中记录。 |

# Simplest Path

- 不引入外部评测服务或新依赖。
- 不新增 provider 抽象。
- 复用已有 JSON fixture、CapabilityExecutor、L4 smoke 和 local-ci。
- 只新增一个专用 gate 校验 corpus manifest、report diff policy 和匿名 fixture 边界。

# Split Strategy

1. 静态资产：manifest、report diff policy、schema/registry。
2. 样本资产：紫微基础 cases 扩容、八字 statement source 元数据。
3. 执行入口：core-quality-corpus-gate + local-ci artifact。
4. 证据：regression tests、任务文档、roadmap、quick local-ci。

# Execution Waves

| Wave | Tasks |
| --- | --- |
| 1 | TP-01.01 |
| 2 | TP-02.01、TP-02.02 |
| 3 | TP-03.01、TP-03.02、TP-03.03 |
| 4 | TP-04.01、TP-04.02 |

# Runtime Workflow Contract

- 运行入口：`bash scripts/core-quality-corpus-gate.sh --output-json <path>`
- 输出：`kind=fatecat.core_quality_corpus_gate`
- 成功条件：status=passed、corpusCount=5、totalCaseCount>=325、failedCheckCount=0。
- 失败处理：任何 fixture 缺失、case 数不足、非北京 birthPlace、source 缺失或 registry 链接断裂都直接失败。

# Next Executable Leaves

- 无；0066 本地 contract/gate baseline 已通过 quick local-ci。

# Dependency Graph

```text
TP-01.01 -> TP-02.01 -> TP-02.02 -> TP-03.01 -> TP-03.02 -> TP-03.03 -> TP-04.01 -> TP-04.02
```

# Rollback Protocol

- 回滚新增 `core-quality-corpus*`、`report-diff-policy.json`、registry/local-ci/test 接线和紫微 fixture 扩容。
- 不执行 `git reset --hard` 或破坏性命令。
- 若 gate 失败，优先修复 manifest/fixture/registry 不一致，而不是降低门槛。
