# Planning Summary
目标终态是 canonical 原文、正文派生、书目事实和人工判断四层分离：原文不可变，正文选择可重建，候选书目不冒充事实，问题进入显式复核队列。

# Lifecycle Gates
1. 所有阶段必须按 `SPEC -> PLAN -> BUILD -> TEST -> REVIEW -> SHIP` 执行，不得跳过 gate。
2. SPEC：定位污染、书目边界和禁止声明。
3. PLAN：先锁 policy schema、正文选择与 fail-closed 规则。
4. BUILD：增强现有清洗器，不新建平行管线。
5. TEST：合成负例和真实 14 本重建。
6. REVIEW：正确性、知识资产、性能和文档漂移深审。
7. SHIP：只提交 policy、工具、测试、文档和任务证据。

# Simplest Path
增强一期标准库清洗器，增加一个显式 JSON policy；不引入数据库、分词器、模糊去噪模型、向量库或第二套脚本。

# Split Strategy
- TP-01/02 先固定事实与契约，防止实现中隐藏删除规则。
- TP-03 只增强现有 owner script。
- TP-04 用真实重建证明范围与正文血缘。
- TP-05 在新鲜 CI 后关闭任务。

# Execution Waves
| Wave | Nodes |
| --- | --- |
| 1 | TP-01 |
| 2 | TP-02 |
| 3 | TP-03 |
| 4 | TP-04 |
| 5 | TP-05 |

# Runtime Workflow Contract
- 输入：canonical TXT、source/copyright manifests、curation policy。
- 输出：一期 7 个文件，加书目/正文选择元数据和人工复核队列。
- 副作用：只原子替换 ignored local-state 输出。
- 失败：source hash、行范围、策略覆盖或权限边界不匹配时立即终止。

# Next Executable Leaves
- 无；全部节点已验收。

# Dependency Graph
`TP-01 -> TP-02 -> TP-03 -> TP-04 -> TP-05`

# Rollback Protocol
- 恢复 `INDEX.md` 当前任务行
- 恢复本任务目录到初始化状态
- 不得影响其他任务目录
