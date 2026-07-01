# Task Status
- Overall Status: `Done`

# Next Executable Leaves
- 无

# Task Package Status Table
| Node ID | Parent | Depth | Depends On | Ready | Status | Recent Evidence | Blocker | Unblock Needed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TP-01 | ROOT | 1 | - | No | Done | 定位基线提交 `ee36710`；路线图和治理规则补齐。 | - | - |
| TP-01.01 | TP-01 | 2 | - | No | Done | `ee36710 docs: define measurement infrastructure baseline`。 | - | - |
| TP-01.02 | TP-01 | 2 | - | No | Done | `docs/reference-materials/roadmap/测算基础设施路线图.md` 已新增。 | - | - |
| TP-01.03 | TP-01 | 2 | - | No | Done | `governance/processes/文档治理规则.md` 已新增，governance context bundle PASS。 | - | - |
| TP-02 | ROOT | 1 | TP-01.01, TP-01.02, TP-01.03 | No | Done | registry/schema/tests 已支持基础设施字段。 | - | - |
| TP-02.01 | TP-02 | 2 | TP-01.01, TP-01.02, TP-01.03 | No | Done | registry 增加 maturity、engineVersion、evidencePolicy、testGate。 | - | - |
| TP-02.02 | TP-02 | 2 | TP-02.01 | No | Done | `test_capability_protocol.py` 覆盖 schema 和新增字段。 | - | - |
| TP-03 | ROOT | 1 | TP-02.02 | No | Done | executor 已按 provider map 执行。 | - | - |
| TP-03.01 | TP-03 | 2 | TP-02.02 | No | Done | `_provider_handlers()` 复用 registry provider。 | - | - |
| TP-03.02 | TP-03 | 2 | TP-03.01 | No | Done | planned 能力拒绝执行测试通过。 | - | - |
| TP-04 | ROOT | 1 | TP-03.02 | No | Done | bazi/ziwei 样板字段已暴露。 | - | - |
| TP-04.01 | TP-04 | 2 | TP-03.02 | No | Done | bazi/ziwei maturity 为 L4，engineVersion 已写入 registry。 | - | - |
| TP-04.02 | TP-04 | 2 | TP-04.01 | No | Done | API 返回 maturity、testGate、evidencePolicy。 | - | - |
| TP-05 | ROOT | 1 | TP-04.02 | No | Done | API alias、metadata 和 quick CI 完成。 | - | - |
| TP-05.01 | TP-05 | 2 | TP-04.02 | No | Done | 已补 `/capabilities`、`/capabilities/{id}/calculate`、`/reports`、`/metadata`。 | - | - |
| TP-05.02 | TP-05 | 2 | TP-05.01 | No | Done | `test_api_contracts.py` 覆盖新入口。 | - | - |
| TP-05.03 | TP-05 | 2 | TP-05.02 | No | Done | quick CI 61 passed；governance strict PASS；git diff --check PASS。 | - | - |

# Blockers
- 无本地阻塞。外部生产域名、真实 token、Bot live smoke 不在本任务内执行，后续仍需外部连通验证。

# Runtime State
- 当前分支：`main`
- 当前策略：定位基线已提交；协议/API 实现待提交并推送。
- Resume rule：继续前读取本 STATUS、TODO 和 `git status --short --branch`。
