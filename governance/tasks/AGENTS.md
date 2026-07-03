# AGENTS.md - Governance Tasks

## 目录用途

`governance/tasks/` 是 active 任务治理根，保存当前任务包、执行证据、closeout 和候选 lessons。它只服务工程治理，不参与运行时加载；历史任务归档统一迁入 `governance/archive/tasks/`。

## 目录结构

```text
tasks/
├── AGENTS.md
├── README.md
├── INDEX.md
├── lessons.md
├── 0001-quality-standards-100/
├── 0002-quality-completion-to-100/
├── ...
└── 0089-measurement-infrastructure-current-audit-bundle/
```

## 职责边界

- `README.md`：说明任务治理目录的维护规则。
- `INDEX.md`：active 任务包索引，只登记 `<task-id>-<slug>/` 任务目录。
- `lessons.md`：当前任务级候选教训池；长期规则需要晋升到治理包对应目录。
- `<task-id>-<slug>/`：active 或当前阻塞任务包，必须符合 auto-tasks 文档契约。
- 禁止在这里放运行时配置、业务源码、依赖缓存或测试输出。

## 依赖方向

- `governance/archive/tasks/* -> governance/evidence/*`：历史任务证据可被治理证据引用。
- `lessons.md -> governance/evidence/lessons/* + governance/standards/* + governance/processes/*`：候选教训拆分后晋升。
- 运行时代码不得依赖 `governance/tasks/`。
