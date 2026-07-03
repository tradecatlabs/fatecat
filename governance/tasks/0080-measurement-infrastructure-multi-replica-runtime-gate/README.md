# Task Overview

- Task ID: `0080`
- Slug: `measurement-infrastructure-multi-replica-runtime-gate`
- Objective: `执行 0079 之后的本地可执行 P0 durable runtime 切片：为 Postgres 长期多副本运行建立 evidence contract、反伪造门禁、runtime registry 接线、local-ci artifact 和回归测试。无真实多副本环境、公网 webhook、外部 secret provider 与监控平台证据时，只输出外部连通验证待执行，不声明 production ready、exactly-once 或多副本 live passed。`
- Status: `Done`

## In Scope

- 新增 `multi-replica-runtime-contract.json`，定义长期多副本 live evidence schema。
- 新增 `multi-replica-runtime-gate.py/.sh`，验证 contract、registry 接线、反伪造负例和可选 live evidence。
- 更新 runtime backend registry、delivery registry、local-ci summary artifact 和 focused regression tests。
- 更新 roadmap、operations docs、AGENTS 与任务文档。

## Out of Scope

- 不启动真实多副本服务。
- 不连接真实 Postgres、公网 webhook receiver、外部 Vault/KMS/secret manager 或监控平台。
- 不声明 production ready、exactly-once、public webhook live passed 或 long-running multi-replica live passed。
- 不修改八字/紫微业务能力。

## Task Package Tree

```text
TP-01 现状复核与任务定界
  TP-01.01 复核 0078/0079 后 durable runtime 缺口
  TP-01.02 复核 runtime registry、local-ci 和测试接线点
TP-02 多副本运行证据契约
  TP-02.01 新增 multi-replica runtime evidence contract
  TP-02.02 新增 single-replica、short-run、sqlite 和 exactly-once overclaim 负例
TP-03 Runtime gate 接线
  TP-03.01 更新 runtime backend registry 与 delivery registry
  TP-03.02 新增 multi-replica-runtime-gate.py/.sh
  TP-03.03 接入 runtime-backend-gate 与 local-ci artifact
TP-04 Tests and docs
  TP-04.01 增加 regression tests
  TP-04.02 更新 roadmap、operations docs 和 AGENTS
TP-05 Verify/closeout/ship
  TP-05.01 运行 focused gates、pytest、ruff/format 和 quick CI
  TP-05.02 回填 closeout；提交、推送和 CI 证据由交付 closeout 记录
```

## Requirement Alignment

- 0078 证明 worker heartbeat/polling baseline；0079 证明外部 secret provider evidence gate baseline。
- 当前仍缺真实公网 webhook live passed、外部 Vault/KMS live passed、长期多副本 live evidence 和 exactly-once。
- 本任务只把“长期多副本运行证据如何才算数”落成机器门禁，不伪造外部生产运行。

## Task Package Overview

| Node ID | Title | Status | Verify |
| --- | --- | --- | --- |
| TP-01.01 | durable runtime 缺口复核 | Done | roadmap/runtime registry |
| TP-01.02 | 接线点复核 | Done | registry/local-ci/tests |
| TP-02.01 | evidence contract | Done | JSON parse + gate |
| TP-02.02 | negative/live schema | Done | regression tests |
| TP-03.01 | runtime registry 接线 | Done | runtime-backend-gate |
| TP-03.02 | multi-replica runtime gate | Done | gate summary |
| TP-03.03 | local-ci 接入 | Done | local-ci artifact |
| TP-04.01 | regression tests | Done | focused pytest |
| TP-04.02 | docs/AGENTS | Done | docs review |
| TP-05.01 | validation gates | Done | focused gates + quick CI |
| TP-05.02 | closeout/git/CI | Done | task closeout ready; delivery closeout records git/CI evidence |

## Reading Order

1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
