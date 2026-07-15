---
id: CTX-ARCHITECTURE-GATE-RULES
type: context
status: current
owner: engineering
created: 2026-07-15
last_reviewed: 2026-07-15
---

# AGENTS.md - Architecture Gate Rules

## 目录用途

本目录是可执行架构阻断规则的真相源：每条 `GATE-*` 只描述阻止条件、原因、检查方式、可操作错误和最小修复，不保存任务运行状态或临时审查日志。

## 目录结构

```text
rules/
├── AGENTS.md                                      # 本目录职责、依赖和变更记录
├── GATE-0001-Web-HTML-禁止自定义前端样式.md        # 零美化语义 HTML 门禁
├── GATE-0002-抓取完整性不得与发现规则共因失明.md   # 抓取发现与验收独立性门禁
└── INDEX.md                                       # 自动生成的规则索引
```

## 职责与依赖

- `GATE-*` 上游来自已证实的 review/debug/lesson，下游由测试、脚本或人工检查执行。
- 任务证据留在 `governance/tasks/`；长期规则只保留可复用阻断条件，禁止复制运行态数据。
- 新增或修改 Gate 后运行 `governance/tools/rebuild_governance_index.py`、strict validator 与 health report。
- `INDEX.md` 由工具生成，不手工维护条目。

## 变更记录

- 2026-07-15：记录 GATE-0002 的抓取共因失明防复发边界，并补齐目录架构镜像。
