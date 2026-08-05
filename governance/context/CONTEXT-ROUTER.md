---
id: GOV-CONTEXT-ROUTER
type: process
status: current
owner: engineering
created: 2026-06-06
last_reviewed: 2026-06-06
review_cycle: P90D
---

# Context Router

## 默认入口

所有任务先读：

1. `governance/INDEX.md`
2. `governance/context/PROJECT-TOPOLOGY.md`
3. `governance/context/CONTEXT-MAP.md`

## 任务类型路由

| 任务类型 | 必读文档 | 可选文档 | 必须产出 |
|---|---|---|---|
| 新功能 | 工程质量标准、非功能性需求标准、QA计划标准、代理协作协议 | 相关 ADR、术语表 | QA 计划或验证证据 |
| Bug 修复 | 劣质代码定义、本地工具与验证入口 | postmortems、lessons | 复现步骤、回归测试 |
| 性能优化 | 性能效率优化标准、门禁与护栏 | 历史性能复盘 | benchmark/profile 证据 |
| 架构变更 | 架构设计原则、ADR 索引、非功能性需求标准 | tech-debt | ADR 或 ADR 更新 |
| Review | 代码评审标准、门禁与护栏 | lessons、agent-feedback | PASS/WARN/BLOCK finding |
| 复盘 | 文档治理规则、门禁与护栏 | postmortems/INDEX.md | 防复发动作 |
| 重复作业执行 | `processes/sops/INDEX.md` 与唯一命中的 SOP | 相关 module context、ADR、contract | SOP 规定的运行记录与验收证据 |
