# Planning Summary
0065 已经建立 OIDC/SIEM/retention cleaner externalization evidence contract 和反伪造 gate，但 staged evidence 仍需要更硬的输入边界：所有 live proof refs 必须是脱敏证据句柄，不能把 raw OIDC/SIEM URL、endpoint、payload 或 production deletion marker 写进仓库。本任务的最小正确切片是加固现有 gate，而不是新增外部连接器。

# Lifecycle Gates
不得跳过 gate：SPEC、PLAN、BUILD、TEST、REVIEW、SHIP 每一阶段必须有对应证据；本地 staged gate 不能替代真实 OIDC/IdP、SIEM 或 retention cleaner live evidence。

| Phase | Gate | Status |
| --- | --- | --- |
| SPEC | 缺口来自 0065 contract/gate、policy 和 roadmap | Done |
| PLAN | 只加固 existing gate，不新建外部 runner | Done |
| BUILD | Contract + Python gate + schema/docs 接线 | Done |
| TEST | regression、focused gates、quick CI | Done |
| REVIEW | no overclaim、no secret、no scope creep | Done |
| SHIP | task closeout and delivery handoff | Done |

# Simplest Path
使用现有 `security-externalization-gate.py` 薄 gate：

1. Contract 中为 identity、SIEM、retentionCleaner 定义统一 `proofRefPrefixes`。
2. Gate 对 live evidence 的 `*ProofRef` / `*SummaryRef` 执行 prefix 白名单。
3. Gate 对外部 submitted evidence 执行 raw URL 和敏感片段扫描。
4. Built-in negative cases 增加 raw OIDC URL 和 retention production deletion marker。
5. quick CI 继续跑 pending/staged artifact，不访问外部服务。

# Split Strategy
- TP-01/02 负责边界，防止把真实 URL、endpoint、payload 或 production deletion marker 写成 evidence。
- TP-03 只做 contract/gate/schema/docs 接线，避免影响 runtime core。
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
Target end state: FateCat 的 security externalization live evidence 与 observability/runtime evidence 一样，必须机器可读、可脱敏复核、可拒绝伪证。
Real constraints: 真实 OIDC/IdP、外部 SIEM、不可变审计存储和 retention cleaner 需要外部权限。
Inertia constraints: 0065 已有 gate，不能因为想做 0083 就复制一套名字相近的新 gate。
Wrong concept / wrong boundary: “有 scoped token 或本地 audit_event 就等于 production OIDC/SIEM ready”是错误边界。
Kill list: raw issuer URL；raw JWKS URL；raw SIEM endpoint；日志 payload；token/secret；production_deleted marker；hard_delete；dryRun=false。
Proof point: `security-externalization-gate` 能验证 proofRefPrefixes、拒绝 raw URL、拒绝 production deletion marker，并保持 pending 非 live。
Falsifier: gate 接受 raw URL、非白名单 proof ref、token/secret、placeholder SIEM 或 production_deleted evidence。
Migration slice: 本轮只加固 staged evidence gate；后续真实 runner 只需要把外部 OIDC/SIEM/retention 证据喂给本 gate。
Rejected short-term patches: 不把 production-readiness warning 改成 live；不新增 README 让 operator 手写无约束 evidence。
Future-optimal review owner: `auto-review` future-optimal-drift.

# Ponytail Task Contract
Existence check: 0065 已有 gate，但缺 proof-ref whitelist 和 raw URL/production deletion 泛化拒绝；加固现有 gate 能降低伪证和泄密风险。
Selected ladder rung: project-native thin gate over JSON contracts and existing local-ci pattern.
Skipped scope: 真实 OIDC/JWKS 验证、SIEM API、WORM storage、retention cleaner runtime、生产数据库清理。
Ceiling / upgrade path: 当有真实外部平台后，gate 继续作为 live evidence verifier；可另开 runner 采集外部证据。
Do-not-simplify: 不删除 pending boundary、proof ref allowlist、sensitive scan、negative cases、non-claim invariant。
Minimal runnable check: `bash scripts/security-externalization-gate.sh --output-json <path>`。
Complexity review owner: `auto-review` ponytail-complexity.

# Runtime Workflow Contract
- Input: optional evidence JSON path.
- Output: `kind=fatecat.security_externalization_gate_summary` JSON summary.
- Side effects: write one local JSON summary when requested.
- External calls: none.
- Privacy: no raw credential, URL, production audit payload, report body, birth region, user input or deletion result.
- Validation: contract/policy/registry links, proof-ref allowlist, required live fields, sensitive scan and negative cases.

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
- 恢复 `contracts/fate/security/externalization-evidence-contract.json` 到 0082 前状态。
- 恢复 `scripts/security-externalization-gate.py` 到 0082 前状态。
- 恢复 `tests/regression/test_production_security_gate.py` 和 `test_capability_protocol.py`。
- 恢复 security schema、AGENTS、roadmap 和任务索引。
- 不删除 0065 原有 security externalization baseline。
