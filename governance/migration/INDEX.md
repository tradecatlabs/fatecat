---
id: MIG-INDEX
type: index
status: current
owner: engineering
created: 2026-06-06
last_reviewed: 2026-07-16
review_cycle: P30D
---

# 迁移索引

本目录记录 FateCat 从 `scripts/project/` 内嵌源码根升级为企业级系统仓库结构的迁移事实。

## 当前记录

- `fatecat-enterprise-assessment.md`：迁移前事实审计。
- `fatecat-enterprise-directory-mapping.md`：旧路径到 canonical roots 的映射。
- `compatibility-ledger.md`：active 兼容入口的 owner、真实契约、保留原因和移除条件。

## 当前结论

`scripts/project/` 兼容盒已从 active catalog 和结构门禁中退役，不再是目标架构真相源，也不再作为 active fallback。旧路径只允许出现在迁移账本、历史证据、负例测试和防回潮规则中。
