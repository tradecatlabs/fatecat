# Task Overview
- Task ID: `0084`
- Slug: `measurement-infrastructure-provider-drift-scanner`
- Objective: `把 provider lifecycle 和 dependency smoke baseline 推进为可审计的 provider drift scanner：生成 provider.validate/provider.calculate trace span、dependency/source/license/vendor drift report，并接入 quick CI；不连接真实公网外部依赖、不接外部 trace backend、不宣称许可证人工法律复核完成。`
- Status: `Done`

## In Scope
- 新增 `contracts/fate/capabilities/provider-drift-contract.json`。
- 新增 `scripts/provider-drift-scanner.py/.sh`。
- 更新 provider schema invariant、local-ci、AGENTS、operations docs、roadmap 和回归测试。
- 建立 drift report：provider lifecycle、dependency smoke、trace span、source refs、license refs、vendor supply-chain refs。

## Out of Scope
- 不接真实公网外部依赖 live smoke。
- 不接外部 OpenTelemetry collector、trace backend、dashboard 或告警平台。
- 不做许可证法律意见或人工法务复核。
- 不保存真实用户输入、报告正文、token、secret、DSN 或生产账号。

## Task Package Tree
```text
TP-01 SPEC: 复核 0032/0033 provider baseline 和 0083 后续队列
  TP-01.01 读取 provider lifecycle/dependency gate、registry、vendor manifest 和 roadmap
  TP-01.02 定义 dependency/source/license/trace drift 边界
TP-02 PLAN: 设计 provider drift scanner
  TP-02.01 定义 drift report contract 和 required provider fields
  TP-02.02 定义 provider span、dependency smoke、vendor license/source 校验
TP-03 BUILD: 实现 scanner 与接线
  TP-03.01 新增 scanner Python 和 shell wrapper
  TP-03.02 更新 provider schema、local-ci、AGENTS、operations docs、roadmap 和 task index
TP-04 TEST: 回归和门禁
  TP-04.01 新增 focused regression tests
  TP-04.02 运行 JSON、scanner、pytest、ruff、secret scan、quick CI 和任务校验
TP-05 REVIEW/SHIP: 收口
  TP-05.01 回填 closeout 与剩余外部验证项
  TP-05.02 明确 git/CI 交付证据外置边界
```

## Requirement Alignment
| Requirement | Implementation |
| --- | --- |
| provider trace span | scanner 捕获本地 `provider.validate` / `provider.calculate` spans |
| dependency drift report | 复用 `provider-dependency-smoke.py` 并对比 provider dependency refs |
| source/license drift report | 校验 source/runtime/contract/test/license refs 与 vendor manifest |
| 不伪造外部 live | summary 固定 `外部连通验证待执行`，不连接外部 backend |
| 任务树推进 | 本任务按 SPEC -> PLAN -> BUILD -> TEST -> REVIEW -> SHIP 执行 |

## Task Package Overview
| Node ID | Title | Status | Acceptance |
| --- | --- | --- | --- |
| TP-01 | SPEC | Done | 缺口来自 repo evidence，不靠猜测 |
| TP-01.01 | 复核 provider baseline | Done | lifecycle/dependency gate、registry、vendor manifest、roadmap 已读取 |
| TP-01.02 | 定义 drift 边界 | Done | dependency/source/license/trace drift 明确 |
| TP-02 | PLAN | Done | scanner report contract 和校验策略明确 |
| TP-02.01 | report contract | Done | `provider-drift-contract.json` 定义 required fields |
| TP-02.02 | drift checks | Done | trace、dependency、source、license、vendor checks 明确 |
| TP-03 | BUILD | Done | scanner、contract、schema、docs 接线完成 |
| TP-03.01 | scanner 脚本 | Done | Python + shell wrapper 可执行 |
| TP-03.02 | docs 接线 | Done | provider schema、local-ci、AGENTS、docs、roadmap、task index 更新 |
| TP-04 | TEST | Done | regression、focused checks、secret scan 和 quick CI 完成 |
| TP-04.01 | regression tests | Done | 覆盖 report、CLI 和 contract |
| TP-04.02 | validation gates | Done | JSON、scanner、pytest、ruff、secret scan、quick CI 和 task validators 完成 |
| TP-05 | REVIEW/SHIP | Done | closeout 完成；git/CI 由外层交付流记录 |
| TP-05.01 | closeout | Done | 文档无 overclaim，外部验证项保留 |
| TP-05.02 | git/CI boundary | Done | 任务包不预声明 commit/push/remote CI；真实证据由外层交付汇报记录 |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
