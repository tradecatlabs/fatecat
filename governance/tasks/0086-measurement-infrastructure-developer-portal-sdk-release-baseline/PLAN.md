# Planning Summary

0086 把 0067 的“本地开发者平台 baseline”推进到“本地 release-readiness baseline”：外部开发者不读源码即可从 portal 文档和机器契约找到 OpenAPI、SDK examples、sandbox fixture、fixed snapshot、API changelog 和 validation commands。

# Lifecycle Gates

不得跳过 gate：SPEC、PLAN、BUILD、TEST、REVIEW、SHIP 每一阶段必须有对应证据；本任务不能把本地 gate 写成公网 portal、PyPI/npm 或 sandbox token live evidence。

| Phase | Gate | Status |
| --- | --- | --- |
| SPEC | repo evidence 证明 0067 已有 baseline 和 0086 缺口 | Done |
| PLAN | release baseline / no-overclaim / snapshot boundary 明确 | Done |
| BUILD | contracts + docs + gate + CI wiring | Done |
| TEST | syntax、gate、focused tests、quick CI | Pending final verification |
| REVIEW | no report body、no token、no public release overclaim | Pending final verification |
| SHIP | local task closeout and git/remote CI | Pending outer delivery flow |

# Simplest Path

1. 保留既有 developer docs smoke 与 developer platform gate。
2. 新增薄 portal gate，复用既有 app/TestClient 和 contracts。
3. fixed snapshot 只保存 canonical digest 和稳定结构字段。
4. local-ci 增加一个 developer portal gate step 和 focused regression。
5. 文档明确 external portal、PyPI/npm 和 public sandbox token 仍未上线。

# Split Strategy

- TP-01/02 锁定 0067 baseline 与 0086 release-readiness 缺口。
- TP-03 只新增机器契约和人类文档，不新增生产 API 语义。
- TP-04 新增一个薄 gate 并复用既有 docs/platform smoke。
- TP-05 用 focused tests 和 quick CI 证明常规门禁覆盖。

# Execution Waves
```text
Wave 1: TP-01.01
Wave 2: TP-02.01
Wave 3: TP-03.01
Wave 4: TP-04.01, TP-04.02
Wave 5: TP-05.01, TP-05.02
```

# Future-Optimal Task Contract
Target end state: FateCat developer platform can be consumed as infra: discoverable contracts, stable examples, fixed snapshots, changelog and gates.
Real constraints: no package registry publication evidence, no public sandbox token service, no hosted developer portal.
Inertia constraints: existing examples are not full SDK packages; do not overbuild package code before publish channel exists.
Wrong boundary: local docs smoke is not external developer portal live evidence.
Kill list: real token in repo; response body snapshot; non-Beijing real sample; package publish claim; public portal live claim.
Proof point: `developer-portal-gate` passes and summary reports 4 SDK candidates, 2 snapshots, 0 published SDK packages and externalPortalLive=false.
Falsifier: snapshot contains full response body, or gate reports published SDK/public portal live without external proof.
Migration slice: 本轮只做 local release baseline；真实 registry publish 和 public sandbox token 另开任务。

# Ponytail Task Contract
Existence check: 需要新 portal gate，因为 0067 gate 不验证 fixed output snapshot 或 portal release baseline。
Selected ladder rung: project-native thin gate over existing docs/platform smoke and FastAPI TestClient.
Skipped scope: real SDK package publish、hosted portal、sandbox token issuer、external gateway.
Ceiling / upgrade path: 未来可接 package registry install smoke、public portal live smoke 和 sandbox token live smoke。
Do-not-simplify: no-overclaim booleans、snapshot digest、privacy scan 不可删除。
Minimal runnable check: `bash scripts/developer-portal-gate.sh --output-json <path>`。

# Runtime Workflow Contract
- Input: optional paths for portal、platform、SDK release、sandbox、snapshot、API changelog and output JSON。
- Output: `kind=fatecat.developer_portal_gate` JSON summary。
- Side effects: writes one local JSON summary when requested。
- External calls: none。
- Privacy: no real token、secret、DSN、production URL、non-Beijing real place、real user or report body。
- Validation: portal contract、SDK smoke、snapshot digest、changelog、platform/docs smoke、privacy fragments。

# Next Executable Leaves
| Node ID | Action |
| --- | --- |
| - | - |

# Dependency Graph
```text
TP-01.01 -> TP-02.01
TP-02.01 -> TP-03.01
TP-03.01 -> TP-04.01
TP-04.01 -> TP-04.02
TP-04.02 -> TP-05.01
TP-05.01 -> TP-05.02
```

# Rollback Protocol
- Revert `developer-portal-gate.*` and remove its local-ci step if gate creates false positives.
- Revert new developer contracts/docs as one slice if release baseline boundary proves wrong.
- Do not delete existing 0067 developer platform baseline during rollback.
