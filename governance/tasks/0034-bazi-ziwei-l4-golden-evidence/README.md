# Task Overview
- Task ID: `0034`
- Slug: `bazi-ziwei-l4-golden-evidence`
- Objective: `把八字/紫微两个核心 production capability 推进为本地可验证 L4 golden/evidence baseline：复用现有匿名 golden fixture，新增 bazi/ziwei L4 golden smoke，统一验证八字节气/真太阳时/起运代表边界、格局/用神/调候/evidence coverage、紫微十二宫/星曜/四化/运限 golden、Markdown profile snapshot gate、冲突解释和反证说明，并接入 quick CI、文档、roadmap 与任务 closeout；不新增真实命例、不做全文断语 golden、不声明专业能力 100%。`
- Status: `Done`

## In Scope
- 新增 `scripts/bazi-ziwei-l4-golden-smoke.py/.sh`，输出机器可读 JSON summary。
- 复用现有匿名北京/测试 fixture，覆盖八字矩阵、八字规则深度、八字断语、紫微 golden、紫微规则深度和 Markdown profile gate。
- 提供 `quick` 与 `full` 两档：`quick` 进入本地 quick CI，`full` 用于发布前加严执行。
- 验证 `analysisEvidence`、规则 ID、冲突解释、反证字段、`policyGate` 和 `snapshotGate` 不断链。
- 同步 quick CI、回归测试、API 文档、roadmap、专项基线文档、`scripts/AGENTS.md` 和任务 closeout。

## Out of Scope
- 不新增真实命例，不读取真实用户或真实非北京地区样例。
- 不锁定完整断语正文，不做全文 golden diff。
- 不宣称八字或紫微专业能力 100%。
- 不做真实公网 API、真实 token、Bot、webhook 或生产部署 live smoke。
- 不新增六爻、奇门、大六壬等其他体系。

## Task Package Tree
```text
TP-01 现状审计与范围确认
  TP-01.01 盘点 MI-05、现有 bazi/ziwei fixture、CapabilityExecutor 和 Markdown gate
TP-02 L4 golden smoke runtime
  TP-02.01 新增 bazi/ziwei L4 golden smoke 脚本
  TP-02.02 支持 quick/full profile 与脱敏 summary 输出
  TP-02.03 接入 quick local-ci
TP-03 回归测试与验证
  TP-03.01 新增 L4 golden smoke pytest
  TP-03.02 运行 smoke、focused tests、ruff、format 和 quick CI
TP-04 文档和 closeout
  TP-04.01 同步 API 文档、roadmap、专项基线、AGENTS 和任务索引
  TP-04.02 生成任务 closeout packet
```

## Requirement Alignment
- 对齐 `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` 的 `MI-05 八字/紫微 L4 样板`。
- 对齐测算基础设施目标：核心 production capability 必须有可复现计算、证据字段、报告门禁和本地可执行验证。
- 对齐隐私治理：fixture 和 Markdown smoke 只使用北京/测试样本，不输出真实地区、token、secret、DSN 或生产账号。
- 对齐不夸大原则：本轮是本地 L4 baseline，不是全文断语 golden、真实命例大 corpus 或专业能力 100%。

## Task Package Overview
| Package | Status | Evidence |
| --- | --- | --- |
| TP-01 | Done | 已盘点 MI-05、现有 fixtures、executor、Markdown API 和 quick CI。 |
| TP-02 | Done | `bazi-ziwei-l4-golden-smoke.py/.sh` 已新增，quick/full profile 已支持，local-ci hook 已添加。 |
| TP-03 | Done | focused tests、ruff、format 和 quick CI 已通过。 |
| TP-04 | Done | docs/roadmap/AGENTS 已同步；closeout packet 已生成。 |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
