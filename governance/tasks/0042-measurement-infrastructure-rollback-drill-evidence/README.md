# Task Overview
- Task ID: `0042`
- Slug: `measurement-infrastructure-rollback-drill-evidence`
- Objective: `把 live release gate 中的 evidence.rollback_drill 从纯路径存在推进为本地可生成、可校验、可交给发布门禁消费的 rollback drill evidence baseline：新增 rollback-drill 脚本，dry-run 校验回滚前置条件、候选回滚命令、相关 runbook/部署文档、release artifacts 和 delivery smoke 证据，输出机器可读 rollback-drill.json；让 live-release-gate 校验 rollback drill JSON 内容；让 public-release-gate 生成并传递该 evidence；补回归测试、文档、任务 closeout。范围不包含真实生产流量切换、真实 registry rollback、真实 HF/Bot 外部回滚或改写 Git 历史。`
- Status: `Done`

## In Scope
- 新增 `scripts/rollback-drill.py` 与 `scripts/rollback-drill.sh`。
- 生成 `rollback-drill.json`，记录 dry-run、commit、precheck、candidate commands、runbook/document paths、artifact paths 和 limitations。
- `live-release-gate.py` 校验 rollback drill JSON 内容，而不是只检查路径存在。
- `public-release-gate.sh` 生成并传递 rollback drill evidence。
- 回归测试、文档、任务 closeout。

## Out of Scope
- 不执行真实生产流量切换。
- 不推送或回滚真实 container registry。
- 不改写 Git 历史。
- 不调用真实 HF Space、Bot 或生产 API。
- 不把 dry-run 证据说成真实生产回滚演练。

## Task Package Tree
```text
ROOT
├── TP-01 现状与边界确认
│   └── TP-01.01 盘点 rollback gate 和现有 runbook/部署脚本
├── TP-02 rollback drill evidence 生成
│   └── TP-02.01 新增 dry-run rollback drill 脚本
├── TP-03 live gate 校验
│   └── TP-03.01 校验 rollback drill JSON 内容
├── TP-04 发布门禁接入
│   └── TP-04.01 public-release/local-ci 文档契约接入
└── TP-05 验证与 closeout
    └── TP-05.01 运行验证并生成 closeout packet
```

## Requirement Alignment
- 对齐 0039 live release gate：`evidence.rollback_drill` 是 required evidence，不应只凭路径存在通过。
- 对齐基础设施目标：回滚必须可演练、可审计、可机器验证。
- 对齐安全边界：本任务只生成 dry-run 证据，不进行真实生产破坏性操作。

## Task Package Overview
| ID | Name | Status | Verify |
| --- | --- | --- | --- |
| TP-01.01 | rollback 现状盘点 | Done | `rg -n "rollback/回滚"` |
| TP-02.01 | rollback drill 生成器 | Done | `bash scripts/rollback-drill.sh --output-json /tmp/fatecat-rollback-drill-0042.json` |
| TP-03.01 | live gate 内容校验 | Done | pytest pass/fail |
| TP-04.01 | public-release 接入 | Done | public-release final live gate `passed=4,pending=6` |
| TP-05.01 | 验证 closeout | Done | task tree valid |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
