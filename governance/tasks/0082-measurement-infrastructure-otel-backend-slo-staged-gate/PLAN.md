# Planning Summary
0064 已经证明 OTel collector/SLO dry-run contract baseline，但它不能证明真实 trace backend、metrics backend、SLO dashboard、alert route、error budget 或 incident drill。0082 的最小正确切片是建立 staged backend/SLO evidence gate：本地只验证 contract、registry 接线和反伪造规则；真实 live evidence 由外部 operator 后续提供脱敏 proof refs。

# Lifecycle Gates
不得跳过 gate：SPEC、PLAN、BUILD、TEST、REVIEW、SHIP 每一阶段必须有对应证据；本地 gate 不能替代外部 OTel backend/SLO live evidence。

| Phase | Gate | Status |
| --- | --- | --- |
| SPEC | 缺口来自 0064 gate、registry 和 roadmap | Done |
| PLAN | 只新增 staged evidence gate，不改 collector/runtime core | Done |
| BUILD | Contract + Python + shell wrapper + CI/docs 接线 | Done |
| TEST | regression、focused gates、quick CI | Done |
| REVIEW | no overclaim、no secret、no scope creep | Done |
| SHIP | task closeout and delivery handoff | Done |

# Simplest Path
使用 Python 标准库实现一个薄 gate：

1. 无 `--evidence-json` 时输出 pending summary。
2. `--evidence-json` 指向 live evidence 时，只接受字段完整、proof refs 脱敏、backend 类型合法、redaction boundary 正确的 evidence。
3. gate 同时校验 contract、registry、observability signal schema 和 negative cases。
4. local-ci 只跑 pending/staged artifact，不访问外部服务。
5. 真实 live 以后由外部 operator 提供 evidence JSON，再交给同一个 gate。

# Split Strategy
- TP-01/02 负责边界，防止把 dry-run、localhost 或 placeholder 写成 live。
- TP-03 只做 gate/contract/schema/docs 接线，避免影响 runtime core。
- TP-04 用 regression + negative cases 证明可接受和可拒绝。
- TP-05 负责 closeout 和远端证据，不把本地结果说成生产 live。

# Execution Waves
```text
Wave 1: TP-03.01
Wave 2: TP-03.02, TP-04.01
Wave 3: TP-04.02
Wave 4: TP-05.01
Wave 5: TP-05.02
```

# Future-Optimal Task Contract
Target end state: FateCat 的 observability live evidence 与 runtime/security evidence 一样，必须机器可读、可脱敏复核、可拒绝伪证。
Real constraints: 真实 OTel backend、SLO dashboard、alert platform、生产流量窗口和 incident drill 需要外部权限。
Inertia constraints: 0064 dry-run gate 只证明 collector/SLO policy 装配，不能因为名字相近被当作 live backend gate。
Wrong concept / wrong boundary: “有 collector dry-run 就等于 production observability ready”是错误边界。
Kill list: raw URL evidence；placeholder backend；localhost 伪 live；debug exporter 伪 live；生产 metrics snapshot；incident drill overclaim。
Proof point: `otel-backend-slo-gate` 能验证 contract、registry 接线、negative cases 和可选 redacted live fixture。
Falsifier: gate 接受 localhost、raw URL、placeholder proof、token/secret、缺少 error budget 或 alert proof。
Migration slice: 本轮只建立 staged evidence gate；后续真实 runner 只需要把外部 backend/SLO 证据喂给本 gate。
Rejected short-term patches: 不把 0064 gate 改名冒充 live gate；不新增 README 让 operator 手写无约束 JSON。
Future-optimal review owner: `auto-review` future-optimal-drift.

# Ponytail Task Contract
Existence check: 0064 已有 dry-run gate，但缺真实 backend/SLO staged evidence validator；新增薄 gate 能降低伪证和泄密风险。
Selected ladder rung: project-native thin gate over JSON contracts and existing local-ci pattern.
Skipped scope: 真实 collector runtime、OTel SDK/exporter、Grafana/Alertmanager/PagerDuty API、incident drill automation。
Ceiling / upgrade path: 当有真实 observability backend 后，gate 继续作为 live evidence verifier；可另开 runner 采集外部证据。
Do-not-simplify: 不删除 pending boundary、proof ref allowlist、sensitive scan、negative cases、non-claim invariant。
Minimal runnable check: `bash scripts/otel-backend-slo-gate.sh --output-json <path>`。
Complexity review owner: `auto-review` ponytail-complexity.

# Runtime Workflow Contract
- Input: optional evidence JSON path.
- Output: `kind=fatecat.otel_backend_slo_gate_summary` JSON summary.
- Side effects: write one local JSON summary when requested.
- External calls: none.
- Privacy: no raw credential, URL, production trace, metrics snapshot, log body, report body or user input.
- Validation: contract/registry/schema links, allowed backend types, required live proof refs and negative cases.

# Next Executable Leaves
| Node ID | Action |
| --- | --- |
| - | - |

# Dependency Graph
```text
TP-01.01 -> TP-01.02
TP-01.02 -> TP-02.01
TP-02.01 -> TP-02.02
TP-02.02 -> TP-03.01
TP-03.01 -> TP-03.02
TP-03.01 -> TP-04.01
TP-03.02 + TP-04.01 -> TP-04.02
TP-04.02 -> TP-05.01
TP-05.01 -> TP-05.02
```

# Rollback Protocol
- 删除 `contracts/fate/observability/otel-backend-slo-evidence-contract.json`。
- 删除 `scripts/otel-backend-slo-gate.py/.sh`。
- 删除 `tests/regression/test_otel_backend_slo_gate.py`。
- 恢复 observability registry/schema、local-ci、AGENTS、roadmap/API docs 和任务索引。
- 不回滚 0064 dry-run gate。
