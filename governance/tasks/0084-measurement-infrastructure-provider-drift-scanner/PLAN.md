# Planning Summary
0032/0033 已有 provider lifecycle gate 和 dependency smoke，但缺一个能把 provider trace span、dependency refs、source refs、license evidence 和 vendor manifest 放在同一份报告里对比的 drift scanner。0084 的最小正确切片是新增本地 scanner 和机器契约，并接入 quick CI；真实公网 live smoke 和法律复核继续外置。

# Lifecycle Gates
不得跳过 gate：SPEC、PLAN、BUILD、TEST、REVIEW、SHIP 每一阶段必须有对应证据；本地 drift report 不能替代真实公网外部依赖 live evidence 或法务复核。

| Phase | Gate | Status |
| --- | --- | --- |
| SPEC | 缺口来自 provider gates、registry、vendor manifest 和 roadmap | Done |
| PLAN | 只新增 scanner，不改 provider runtime 协议 | Done |
| BUILD | Contract + Python + shell wrapper + CI/docs 接线 | Done |
| TEST | regression、focused gates、quick CI | Done |
| REVIEW | no overclaim、no secret、no scope creep | Done |
| SHIP | task closeout and delivery handoff | Done |

# Simplest Path
使用 Python 标准库实现一个薄 scanner：

1. 调用现有 provider lifecycle gate。
2. 调用现有 provider dependency smoke。
3. 用 `CapabilityExecutor` 和脱敏固定样例捕获本地 provider spans。
4. 校验 source/runtime/contract/test/license refs 与 vendor supply-chain refs。
5. 输出 `kind=fatecat.provider_drift_report`，0 findings 才通过。

# Split Strategy
- TP-01/02 负责边界，防止 drift scanner 变成另一个 live smoke 或法律审计。
- TP-03 只做 scanner/contract/schema/docs/local-ci 接线，避免影响 provider runtime core。
- TP-04 用 regression + quick CI 证明 report 可生成且不泄露样例。
- TP-05 负责 closeout 和远端证据，不把本地结果说成公网 live。

# Execution Waves
```text
Wave 1: TP-03.01
Wave 2: TP-03.02, TP-04.01
Wave 3: TP-04.02
Wave 4: TP-05.01
Wave 5: TP-05.02
```

# Future-Optimal Task Contract
Target end state: FateCat 的 production provider 必须具备可机器复核的 source/license/dependency/trace drift 证据链。
Real constraints: 真实公网依赖、外部 trace backend、法律许可复核和跨版本升级需要外部流程或人工权限。
Inertia constraints: provider lifecycle gate 和 dependency smoke 已存在，不能复制成新 provider registry。
Wrong concept / wrong boundary: “provider health ready 等于没有供应链/trace/license drift”是错误边界。
Kill list: missing source ref；missing license evidence；vendor no SPDX；vendor productionUseAllowed=false；missing provider.validate span；missing provider.calculate span；sample payload leak。
Proof point: `provider-drift-scanner` 输出 4 providers、4 capabilities、12 spans、0 findings。
Falsifier: scanner 接受缺 trace span、缺 source/license ref、vendor license 非 SPDX 或 productionUseAllowed=false。
Migration slice: 本轮只做本地 drift scanner；后续外部 provider live smoke 可以把外部证据追加到同类 report。
Rejected short-term patches: 不把 lifecycle gate 重命名冒充 drift scanner；不在 README 里手写 drift 结论。
Future-optimal review owner: `auto-review` future-optimal-drift.

# Ponytail Task Contract
Existence check: 已有 lifecycle/dependency 两个分散门禁，但缺聚合 drift report；新增薄 scanner 能降低 silent drift 风险。
Selected ladder rung: project-native thin gate over existing provider metadata, local spans and JSON contracts.
Skipped scope: 外部 OTel collector、trace backend、真实公网 API、法务复核、版本升级机器人。
Ceiling / upgrade path: 有真实外部依赖后，scanner 可新增 external proof refs 字段，不改变 provider runtime 协议。
Do-not-simplify: 不删除 trace span、source refs、license refs、vendor refs、privacy assertion 和 non-live boundary。
Minimal runnable check: `bash scripts/provider-drift-scanner.sh --output-json <path>`。
Complexity review owner: `auto-review` ponytail-complexity.

# Runtime Workflow Contract
- Input: none; optional output JSON path.
- Output: `kind=fatecat.provider_drift_report` JSON summary.
- Side effects: write one local JSON summary when requested.
- External calls: none.
- Privacy: no raw payload, report body, user input, credential, URL secret, DSN or production account.
- Validation: lifecycle/dependency smoke status、provider spans、source refs、license refs、vendor refs、contract and observability signal.

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
- 删除 `contracts/fate/capabilities/provider-drift-contract.json`。
- 删除 `scripts/provider-drift-scanner.py/.sh`。
- 删除 `tests/regression/test_provider_drift_scanner.py`。
- 恢复 provider schema、local-ci、AGENTS、operations docs、roadmap 和 task index。
- 不回滚 provider lifecycle gate 或 dependency smoke。
