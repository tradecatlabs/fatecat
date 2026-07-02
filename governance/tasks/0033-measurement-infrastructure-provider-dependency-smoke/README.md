# Task Overview
- Task ID: `0033`
- Slug: `measurement-infrastructure-provider-dependency-smoke`
- Objective: `把 provider health 从静态 in-process metadata 推进为本地可执行 dependency smoke baseline：为每个 production capability 准备固定脱敏样例，通过统一 CapabilityExecutor 执行 provider validate/calculate，输出机器可读 provider dependency smoke summary，接入 quick CI、API 文档、roadmap 和任务 closeout；不做真实公网外部依赖、OpenTelemetry trace span、SBOM、法律审计或新 provider。`
- Status: `Done`

## In Scope
- 新增 production provider dependency smoke 脚本，通过统一 `CapabilityExecutor` 执行每个 production capability。
- 为 bazi、ziwei、almanac、meihua 准备北京/测试用户脱敏固定样例。
- 验证 provider health ready、validate/calculate 链路、输出关键字段和 evidence 最小结构。
- 输出机器可读 summary JSON，明确 smoke scope 与外部连通边界。
- 接入 quick local-ci、回归测试、API 文档、roadmap 和目录级 AGENTS。

## Out of Scope
- 不访问公网、不调用真实外部 API、不读取真实 token、Bot、webhook、生产账号或 `.env`。
- 不接 OpenTelemetry trace span、collector、dashboard 或 SLO。
- 不生成 SBOM/provenance，不做许可证人工法律审计。
- 不新增 provider、不改命理算法、不扩大默认八字报告。

## Task Package Tree
```text
TP-01 现状审计与范围确认
  TP-01.01 盘点 MI-04.03、provider registry、executor 和现有 smoke 模式
TP-02 dependency smoke runtime
  TP-02.01 新增 provider dependency smoke 脚本和脱敏 fixture
  TP-02.02 接入 quick local-ci
TP-03 回归测试与验证
  TP-03.01 新增 provider dependency smoke pytest
  TP-03.02 运行 focused tests、ruff、smoke、quick CI
TP-04 文档和 closeout
  TP-04.01 同步 API 文档、roadmap、AGENTS 和任务索引
  TP-04.02 生成任务 closeout packet
```

## Requirement Alignment
- 对齐 `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` 的 `MI-04.03 provider health 和 external dependency smoke`。
- 对齐 provider 生命周期目标：生产 provider 不仅要有 metadata，还必须能用固定样例真实执行。
- 对齐隐私治理：样例只使用北京/测试用户，不输出报告正文、不读取真实用户数据。
- 对齐不夸大原则：本轮只是本地 dependency fixture smoke，真实公网 live smoke 仍标注外部连通验证待执行。

## Task Package Overview
| Package | Status | Evidence |
| --- | --- | --- |
| TP-01 | Done | 已读取 roadmap、provider registry、executor、usecase 输入和现有 smoke 模式。 |
| TP-02 | Done | `provider-dependency-smoke.py/.sh` 已新增并接入 `local-ci.sh`。 |
| TP-03 | Done | focused tests、smoke 和 quick CI 已通过。 |
| TP-04 | Done | docs/AGENTS/roadmap 已同步；closeout packet 已生成。 |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
