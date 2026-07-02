# Acceptance Checklist

# Global Standards

- [x] 计划不宣称 100% 已完成。
- [x] 外部 live evidence 明确保留为待执行。
- [x] 0050 registry attestation 完成状态已同步。
- [x] 0048 Bot live blocker 未被覆盖。
- [x] 不新增平行路线图。
- [x] 不改业务代码。
- [x] 任务文档校验通过。
- [x] 任务树校验通过。
- [x] diff hygiene 通过。

# Task Package Checklists

## TP-01.01

- [x] 当前路线图、任务索引和 0050 状态已读取。
- Verify: `git status --short --branch` and file reads。
- Gate: 不基于聊天记忆脑补。

## TP-02.01

- [x] 外部基础设施同构资料已归纳。
- Verify: roadmap `0.6` source mapping。
- Gate: 不用二手猜测替代官方依据。

## TP-03.01

- [x] 主路线图新增 post-0050 实现计划。
- Verify: `rg "0.6 2026-07-02 Post-0050"`。
- Gate: 不新建平行路线图。

## TP-03.02

- [x] 0051 任务包已创建。
- [x] 任务索引已新增 0051 行。
- Verify: `rg "0051" governance/tasks/INDEX.md`。
- Gate: 不影响 0050 事实。

## TP-04.01

- [x] 任务文档校验通过。
- [x] 任务树校验通过。
- [x] diff hygiene 通过。
- Verify: validator commands。
- Gate: 未跑命令不能写通过。

# Lifecycle Checklist

- [x] SPEC gate：100% 定义为基础设施成熟度。
- [x] RESEARCH gate：外部 infra 同构资料已归纳。
- [x] PLAN gate：post-0050 资源缺口和任务树已落盘。
- [x] BUILD gate：主路线图和 0051 任务包已创建。
- [x] TEST gate：任务文档和 diff 校验通过。
- [x] REVIEW gate：确认无伪证、无过度声明、无平行口径。
- [x] SHIP gate：交付给后续 MI-NEXT-03 等执行任务。

# Evidence To Record

| Evidence | Status |
| --- | --- |
| `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` includes `0.6` | Done |
| `governance/tasks/0051-measurement-infrastructure-100-post-0050-executable-plan/` exists | Done |
| `governance/tasks/INDEX.md` includes 0051 | Done |
| validators pass | Done |
