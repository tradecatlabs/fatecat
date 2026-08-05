---
id: AGENTS-GOVERNANCE-PROCESSES
type: context
status: current
owner: governance
created: 2026-07-24
last_reviewed: 2026-07-24
review_cycle: P90D
---

# AGENTS.md - governance/processes

## 目录用途

`governance/processes/` 保存长期有效、可重复执行的工程流程；任务级过程留在 `governance/tasks/`，机器契约留在 `contracts/`。

## 目录结构

```text
processes/
├── AGENTS.md
├── QA计划标准.md
├── RPI研究计划实施流程.md
├── 代理协作协议.md
├── 代码评审标准.md
├── 文档治理规则.md
├── 本地工具与验证入口.md
└── sops/
    ├── AGENTS.md
    ├── INDEX.md
    └── *.md
```

## 职责边界

- 顶层流程文档定义跨任务的标准和治理规则。
- `sops/` 定义单一具体任务的可执行标准作业程序。
- 每个 SOP 只负责一个任务意图，不拥有业务代码、运行时状态或外部凭证。
- SOP 必须复用 `scripts/`、`contracts/` 和现有证据，不创建平行命令入口。

## 依赖方向

- `sops -> scripts + contracts + governance standards`
- `governance/tasks -> processes/sops` 可引用，反向不得把一次性任务状态写入长期 SOP。
