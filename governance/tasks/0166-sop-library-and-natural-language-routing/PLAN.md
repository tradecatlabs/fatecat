# Planning Summary

目标终态是“一个任务意图、一个稳定 SOP、一个现有工具链、一个证据出口”。SOP 不复制实现历史，而把成功历史提炼成可重复运行的最小流程。

# Lifecycle Gates
所有阶段必须按顺序通过，任何节点不得跳过 gate。

1. SPEC：锁定任务分类、route key、必备章节和状态来源。
2. PLAN：分 capability、数据评测、开发质量、分发部署、生产运行、发布审计六类。
3. BUILD：先索引和目录边界，再逐份 SOP，最后机械校验。
4. TEST：校验 frontmatter、章节、路由、链接、路径和 capability 状态。
5. REVIEW：检查重叠任务、虚假生产声明、外部副作用和文档漂移。
6. SHIP：任务文档、治理索引和验证证据收口；不自动执行外部发布。

# Simplest Path
使用 Markdown frontmatter、单一 `INDEX.md` 和 Python 标准库回归测试，不新增数据库、路由服务、生成器或运行时依赖。

# Split Strategy
- 以独立成功标准作为拆分边界，不按目录数量或历史 task package 数量拆分。
- capability 执行、能力投产、数据构建、质量验证、部署运行和发布审计分别建 SOP。
- 多个命令只有在共同完成一个不可分割目标时才允许出现在同一 SOP。

# Next Executable Leaves
- TP-05：运行专项测试、任务文档校验、治理 strict/health 和 Quick CI。

# Dependency Graph
```text
TP-01
├── TP-02
├── TP-03
└── TP-04
    └── TP-05 依赖 TP-02、TP-03、TP-04
```

# Execution Waves
| Wave | Nodes |
| --- | --- |
| 1 | TP-01 |
| 2 | TP-02、TP-03、TP-04 |
| 3 | TP-05 |

# Runtime Workflow Contract
- 输入：tracked contracts、scripts、历史任务和现有治理流程。
- 输出：tracked SOP 文档、索引、AGENTS 和回归测试。
- 副作用：只修改文档、测试和治理索引。
- 失败：路由重复、脚本缺失、章节缺失、状态漂移时 fail closed。

# Rollback Protocol
- 回退本任务提交即可移除 SOP 库和校验。
- 不影响业务数据、运行时状态、生产部署或 capability registry。
