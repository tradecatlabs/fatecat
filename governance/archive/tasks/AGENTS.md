---
id: ARCHIVE-ARCHIVE-TASKS-AGENTS
type: archive
status: archived
owner: engineering
created: 2026-06-17
last_reviewed: 2026-06-17
review_cycle: P365D
---
# AGENTS.md - Archived Governance Tasks

## 目录用途

`governance/archive/tasks/` 保存已经退役或被替代的历史任务包。这里是证据归档区，不是 active 任务调度根。

## 目录结构

```text
tasks/
├── AGENTS.md
└── project-history/
    ├── INDEX.md
    ├── lessons.md
    ├── 0001-comprehensive-bazi-statement-service-hardening/
    └── 0002-bazi-ziwei-benchmark-hardening/
```

## 职责边界

- `project-history/`：历史任务包归档，保留计划、验收、执行证据和 closeout。
- 归档任务不得作为 `governance/tasks/` 的 active ready queue 来源。
- 运行时代码、CI/CD 和业务模块不得依赖本目录。

## 依赖方向

- `governance/archive/tasks/* -> governance/evidence/*`：历史任务可被治理证据引用。
- `governance/tasks/* -> governance/archive/tasks/*`：active 任务可以引用历史证据，但不得把归档任务重新纳入 active 调度。
