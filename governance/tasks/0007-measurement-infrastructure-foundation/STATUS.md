# Task Status
- Overall Status: `In Progress`

# Next Executable Leaves
- TP-01.02
- TP-01.03
- TP-02.01

# Task Package Status Table
| Node ID | Parent | Depth | Depends On | Ready | Status | Recent Evidence | Blocker | Unblock Needed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TP-01 | ROOT | 1 | - | No | In Progress | 定位文案已改；路线图和治理规则本轮补齐。 | - | - |
| TP-01.01 | TP-01 | 2 | - | Yes | Not Started | 待定位基线提交。 | - | - |
| TP-01.02 | TP-01 | 2 | - | No | Done | `docs/reference-materials/roadmap/测算基础设施路线图.md` 已新增。 | - | - |
| TP-01.03 | TP-01 | 2 | - | No | Done | `governance/processes/文档治理规则.md` 已新增，governance context bundle PASS。 | - | - |
| TP-02 | ROOT | 1 | TP-01.01, TP-01.02, TP-01.03 | No | Not Started | 待 registry/schema/tests。 | - | - |
| TP-02.01 | TP-02 | 2 | TP-01.01, TP-01.02, TP-01.03 | No | Not Started | 待 registry 新字段实现。 | - | - |
| TP-02.02 | TP-02 | 2 | TP-02.01 | No | Not Started | 待 schema 和协议测试。 | - | - |
| TP-03 | ROOT | 1 | TP-02.02 | No | Not Started | 待 executor provider map。 | - | - |
| TP-03.01 | TP-03 | 2 | TP-02.02 | No | Not Started | 待 provider registry 实现。 | - | - |
| TP-03.02 | TP-03 | 2 | TP-03.01 | No | Not Started | 待 planned 拒绝策略回归。 | - | - |
| TP-04 | ROOT | 1 | TP-03.02 | No | Not Started | 待 bazi/ziwei 样板字段。 | - | - |
| TP-04.01 | TP-04 | 2 | TP-03.02 | No | Not Started | 待 bazi/ziwei 标杆协议字段。 | - | - |
| TP-04.02 | TP-04 | 2 | TP-04.01 | No | Not Started | 待 API 返回成熟度字段。 | - | - |
| TP-05 | ROOT | 1 | TP-04.02 | No | Not Started | 待 API alias、metadata 和 quick CI。 | - | - |
| TP-05.01 | TP-05 | 2 | TP-04.02 | No | Not Started | 待新基础设施 API alias。 | - | - |
| TP-05.02 | TP-05 | 2 | TP-05.01 | No | Not Started | 待 API contract tests。 | - | - |
| TP-05.03 | TP-05 | 2 | TP-05.02 | No | Not Started | 待 quick CI 和提交前 hygiene。 | - | - |

# Blockers
- 外部生产域名、真实 token、Bot live smoke 不在本任务内执行，后续仍需外部连通验证。

# Runtime State
- 当前分支：`main`
- 当前策略：分阶段提交，先定位基线，再协议/API 实现。
- Resume rule：继续前读取本 STATUS、TODO 和 `git status --short --branch`。
