# Planning Summary
按净删除路径撤销三块工作台例外：先保持外部行为地移除 CSS/class/布局容器，再把测试从“要求例外存在”反转为“禁止例外回潮”，最后同步治理真相源并验证。

# Lifecycle Gates
- SPEC：用户撤销范围明确，目标是无例外零美化 HTML；不得跳过 gate。
- PLAN：行为边界、kill list、验证和文档同步范围已记录；不得跳过 gate。
- BUILD：只删除布局实现，不改命理计算或公共 API；不得跳过 gate。
- TEST：目标回归、源码扫描、治理校验和 quick CI 必须通过；不得跳过 gate。
- REVIEW：检查 correctness、architecture、test-quality、document drift 和 complexity；不得跳过 gate。
- SHIP：本轮不执行 commit/push；closeout 记录工作树状态和未授权的 Git 交付；不得跳过 gate。

# Simplest Path
使用现有服务端字符串渲染、原生 HTML 元素、tabulate、GET 表单和既有 JavaScript 增强；删除整个样式函数和所有布局 class，不引入新前端技术。

# Split Strategy
- TP-01：实现净删除并保持行为。
- TP-02：更新机械门禁和长期文档。
- TP-03：验证与独立审查。

# Execution Waves
- Wave 1: TP-01
- Wave 2: TP-02
- Wave 3: TP-03

# Runtime Workflow Contract
- 不使用子代理；当前改动集中在同一 HTML/测试/治理边界，单一执行者更容易保持一致。
- 每一步保留可复核 diff 和命令证据。
- 验证失败时回到对应文件修复，不用跳过或弱化断言换绿。

# Next Executable Leaves
- TP-01：删除布局例外并恢复语义 HTML。

# Dependency Graph
TP-01 -> TP-02 -> TP-03

# Rollback Protocol
- 回滚边界是本任务 diff；不触碰命理算法、API 或持久化数据。
- 若语义重构导致功能回归，恢复最近一个通过目标测试的 HTML 结构，再在无 CSS 前提下修复。
- 不恢复已被用户撤销的布局授权作为长期方案。
