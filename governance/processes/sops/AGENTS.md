---
id: AGENTS-GOVERNANCE-PROCESS-SOPS
type: context
status: current
owner: governance
created: 2026-07-24
last_reviewed: 2026-07-24
review_cycle: P90D
---

# AGENTS.md - governance/processes/sops

## 目录用途

本目录是 FateCat 标准作业程序唯一真相源，用于把自然语言任务路由到唯一、可验证、可恢复的仓库操作。

## 文件规则

```text
sops/
├── AGENTS.md
├── INDEX.md
└── <single-task-slug>.md
```

- 一个文件只描述一个任务目标。
- `INDEX.md` 维护类别、状态、唯一 route key、自然语言别名、排除条件和文档链接。
- 每份 SOP 必须包含统一的 20 个必备章节。
- `route_key` 与全部 `route_aliases` 在目录内全局唯一。
- capability 状态只能来自 `contracts/fate/capabilities/registry.json`。
- planned 能力只能描述研发接入和投产门禁，禁止提供伪生产执行步骤。

## 依赖与输出

- 输入真相源：`contracts/`、`scripts/`、`infra/environments/`、`governance/tasks/` 的已验证历史证据。
- 默认运行产物：`infra/runtime/local-state/exports/` 或 `/tmp/fatecat-*`。
- 持久运行记录：任务状态、审计证据或 release evidence；不得提交含隐私、密钥或大体积派生正文的运行产物。
