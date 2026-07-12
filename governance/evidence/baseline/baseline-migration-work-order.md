---
id: BASELINE-MIGRATION-WORK-ORDER-FATECAT
type: baseline-migration-work-order
status: archived
owner: engineering
created: 2026-06-06
last_reviewed: 2026-07-13
review_cycle: P30D
---

# Baseline Migration Work Order

> 历史快照：该迁移工单已结束，`scripts/project` 不再是活动运行根。

## Scope

将 FateCat 从 `scripts/project` 内嵌项目结构迁移到企业 canonical roots。

## Steps

1. Phase 0：事实审计和 migration mapping。
2. Phase 1：建立 canonical roots、服务契约、catalog 和 governance。
3. Phase 2：抽象 runtime root，更新 P0 scripts/CI/path 常量。
4. Phase 3：迁移 `fate-core` 与 `fatecat-delivery` 源码和测试。
5. Phase 4：迁移 contracts、docs、infra、vendor manifest、tasks。
6. Phase 5：清退 `scripts/project` 兼容盒。
7. Phase 6：完整 acceptance、导出 smoke、governance strict validate。

## Rollback

每个阶段只做可验证的小步。若 P0 验证失败，保留 `scripts/project` 兼容盒，回退本阶段路径解析或脚本改动，不删除用户业务改动。
