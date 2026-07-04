# Planning Summary

本任务把 0141 规划中的“八字/紫微核心质量扩容”落成本地可验证切片：在不改变 production provider 算法的前提下，扩展匿名 golden corpus，补齐 professional quality rubric，把 core-quality gate 从“样本数量和结构策略”升级为“样本数量 + 覆盖标签 + report diff + rubric + registry 链接”的复合门禁。

目标不是证明真实命例准确率，而是让八字/紫微作为测算基础设施核心 capability 具备更硬的本地回归、评审准入和不可伪造边界。

# Lifecycle Gates

| Gate | Status | Evidence |
| --- | --- | --- |
| SPEC | Done | 0141 后续质量切片范围收敛为 evaluation contract、golden fixture、gate/test 和文档。 |
| PLAN | Done | TP-01 到 TP-05 的依赖、验证和回滚路径已写入本计划。 |
| BUILD | Done | rubric、manifest/policy/registry、fixture、gate、tests 和 docs 已落盘。 |
| TEST | Done | JSON parse、core-quality gate、data supply chain gate、L4 smoke、pytest regression 通过。 |
| REVIEW | Done | privacy/no-overclaim/production-boundary 自审完成。 |
| SHIP | Done | 0142 任务包和 `governance/tasks/INDEX.md` 同步，准备提交。 |

不得跳过 gate；任何 gate 失败必须修复后重新执行对应验证。

# Simplest Path

1. 在现有 core-quality corpus 上扩容，不引入新评测框架。
2. 用 `CapabilityExecutor` 当前输出生成新增匿名 fixture 的 expected 字段，只锁结构化 guard 和 evidence 字段。
3. 新增单独 rubric contract，不把主观专家评审混入 production runtime。
4. 让现有 `core-quality-corpus-gate` 读取并校验 rubric，避免新增散落脚本。
5. 更新现有 regression tests 和 L4 smoke 阈值，不创建重复测试体系。

# Split Strategy

| TP | Why |
| --- | --- |
| TP-01 | rubric 与 manifest/policy/registry 是后续样本门禁的契约真相源。 |
| TP-02 | fixture 扩容先锁匿名样本数量和覆盖标签，不动生产算法。 |
| TP-03 | gate/test 把契约和 fixture 变成可执行发布门禁。 |
| TP-04 | 文档说明新增契约职责和任务 closeout，防止文档漂移。 |
| TP-05 | 统一跑 JSON、gate、pytest、smoke，形成可复核证据。 |

# Execution Waves

| Wave | Leaves | Status |
| --- | --- | --- |
| Wave 1 | TP-01, TP-02 | Done |
| Wave 2 | TP-03 | Done |
| Wave 3 | TP-04, TP-05 | Done |

# Runtime Workflow Contract

- Production runtime 不读取本任务新增的 golden fixture 或 professional rubric。
- Gate runtime 只输出 summary JSON，不保存完整报告正文、真实用户资料、benchmark 标准答案或外部凭证。
- 新增 fixture 只允许通过 `tests/regression/*` 和 `scripts/core-quality-corpus-gate.py` 消费。
- 真实专家评审、真实命例库和生产 live 仍属于外部验证，不因本地 gate 通过而自动完成。

# Next Executable Leaves

No remaining executable leaf in this task.

# Dependency Graph

```text
TP-01 -> TP-03
TP-02 -> TP-03
TP-03 -> TP-05
TP-04 -> TP-05
```

# Rollback Protocol
- 恢复 `INDEX.md` 当前任务行
- 恢复 `contracts/fate/evaluations/*` 中本任务新增/修改的 rubric、manifest、policy、registry。
- 恢复 `domains/fate-analysis/data-products/{bazi,ziwei}/golden/*` 新增匿名 fixture。
- 恢复 `scripts/core-quality-corpus-gate.py` 与相关 regression tests。
- 不得影响 production provider、运行时记录、外部凭证或历史任务目录。
