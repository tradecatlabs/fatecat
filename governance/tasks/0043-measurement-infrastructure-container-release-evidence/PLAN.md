# Planning Summary
把 container evidence 从裸 `sha256` 字符串升级为“本地构建 + smoke + imageId + commit”的证据包；真实 registry digest 仍保留给外部发布路径。

# Lifecycle Gates
| Phase | Gate | Status |
| --- | --- | --- |
| SPEC | 本地 imageId 与 registry digest 边界明确 | Done |
| PLAN | 任务树、验收和反证写入任务包 | Done |
| BUILD | 脚本、gate 接入、测试、文档完成 | In Progress |
| TEST | JSON、shell、pytest、真实 container smoke | Pending |
| REVIEW | 不伪造 registry digest | Pending |
| SHIP | closeout packet 生成 | Pending |

禁止跳过任何 gate；不得把本地 imageId 说成 GHCR/registry RepoDigest。

# Simplest Path
复用现有 `container-build.sh` 与 `container-smoke.sh`，新增薄证据脚本读取 `docker image inspect`，live gate 增加 JSON 校验。

# Split Strategy
- TP-01 做现状盘点。
- TP-02 做 evidence 生成器。
- TP-03 做 live gate 校验。
- TP-04 做 public-release 接入与文档。
- TP-05 做真实 build/smoke 和 closeout。

# Execution Waves
| Wave | Nodes | Status |
| --- | --- | --- |
| 1 | TP-01.01 | Done |
| 2 | TP-02.01 | In Progress |
| 3 | TP-03.01 | Pending |
| 4 | TP-04.01 | Pending |
| 5 | TP-05.01 | Pending |

# Runtime Workflow Contract
- risk_level: medium
- affected_flows: container build/smoke, public release gate, live release gate
- external_contracts: `contracts/fate/delivery/release-gate.json`
- data_flow: container evidence script writes JSON; live gate consumes it
- state_changes: local Docker image and temporary smoke container only
- side_effects: no registry push, no remote network beyond package build dependencies already defined by Dockerfile
- rollback: remove local image if needed; revert script/test/doc changes
- required_tests: targeted pytest, shell syntax, container evidence smoke, task docs validation

# Next Executable Leaves
TP-02.01

# Dependency Graph
```text
TP-01.01 -> TP-02.01 -> TP-03.01 -> TP-04.01 -> TP-05.01
```

# Rollback Protocol
- 恢复 `INDEX.md` 当前任务行
- 恢复本任务目录到初始化状态
- 不得影响其他任务目录
