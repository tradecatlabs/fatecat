# Planning Summary
0080 解决了“什么证据才算多副本 runtime live evidence”的 gate，但没有解决“真实环境如何生成一个受控、脱敏、可被 gate 消费的 evidence JSON”。0081 的最小正确切片是新增 assembler：它不跑真实 24h soak，只把 operator 提供的外部证据句柄封装成标准 evidence，并立即用 0080 gate 校验。

# Lifecycle Gates
不得跳过 gate：SPEC、PLAN、BUILD、TEST、REVIEW、SHIP 每一阶段必须有对应证据；本地 gate 不能替代外部 live evidence。

| Phase | Gate | Status |
| --- | --- | --- |
| SPEC | 缺口来自 roadmap 和 0080 gate | Done |
| PLAN | 只新增 evidence assembler，不改 runtime core | Done |
| BUILD | Python + shell wrapper + CI/docs 接线 | Done |
| TEST | regression、focused gates、quick CI | Done |
| REVIEW | no overclaim、no secret、no scope creep | Done |
| SHIP | task closeout and delivery handoff | Done |

# Simplest Path
使用 Python 标准库实现一个薄 assembler：

1. `--pending` 输出 pending evidence。
2. `--external-live` + `--ack-external-live` 输出 external evidence。
3. live 模式要求所有 0080 required runtime fields、operator attestation、run id、started/finished 时间。
4. 写出 evidence JSON 后调用/复用 `multi-replica-runtime-gate` validation。
5. local-ci 只跑 pending/fixture artifact，不访问外部服务。

# Split Strategy
- TP-01/02 负责边界，防止目标滑成“再写一个计划”。
- TP-03 只做脚本和接线，避免影响 runtime core。
- TP-04 用 regression + existing gate 证明可消费和可拒绝。
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
Target end state: FateCat 的外部 live evidence 不是聊天记录或手写散文，而是由受控工具生成、由 gate 验证、由 CI/审计复核的机器证据。
Real constraints: 真实 DSN、webhook URL、Vault/KMS、metrics backend 和 24h soak 需要外部环境；仓库不能保存秘密或生产日志。
Inertia constraints: 现有 0080 gate 只消费 JSON，不代表 evidence 生成流程已经存在。
Wrong concept / wrong boundary: “有 contract 就等于 live 可验证”是错误边界。
Kill list: 手写 JSON 直接冒充 live evidence；pending summary 冒充 production ready；exactly-once 口头 overclaim。
Proof point: assembler 生成的 live fixture 能通过 0080 gate，fake/secret/overclaim fixture 会失败。
Falsifier: assembler 不经 0080 gate 也能输出 passing live，或输出中出现敏感值。
Migration slice: 先建立 evidence 生成入口；未来真实 runner 只需要把 runtime results 喂给 assembler。
Rejected short-term patches: 不新增“README 教用户手写 JSON”；不把 0080 gate 再复制一份。
Future-optimal review owner: `auto-review` future-optimal-drift.

# Ponytail Task Contract
Existence check: 0080 contract 已存在但缺受控 evidence producer；新增薄 assembler 能降低伪证和泄密风险。
Selected ladder rung: project-native thin glue over existing gate.
Skipped scope: 真实 24h runner、外部平台接入、database worker 改造、exactly-once proof。
Ceiling / upgrade path: 当有真实 Kubernetes/worker runtime 后，assembler 升级为读取真实 run manifest/metrics，而不是接收手工参数。
Do-not-simplify: 不删除 ack、redaction、secret scan、gate validation、non-claim 字段。
Minimal runnable check: assembler pending CLI、assembler live fixture -> gate pass、secret fixture -> fail。
Complexity review owner: `auto-review` ponytail-complexity.

# Runtime Workflow Contract
- Input: command-line args and proof refs only.
- Output: `kind=fatecat.multi_replica_runtime_evidence` JSON.
- Side effects: write one local JSON file.
- External calls: none.
- Privacy: no raw credential, URL, report, user input or production log body.
- Validation: call existing `validate_multi_replica_evidence` from `multi-replica-runtime-gate.py`.

# Next Executable Leaves
| Node ID | Action |
| --- | --- |
| - | - |

# Dependency Graph
```text
TP-03.01 -> TP-03.02
TP-03.01 -> TP-04.01
TP-03.02 + TP-04.01 -> TP-04.02
TP-04.02 -> TP-05.01
TP-05.01 -> TP-05.02
```

# Rollback Protocol
- 删除 `scripts/multi-replica-runtime-evidence-assembler.py/.sh`。
- 删除 assembler regression test。
- 恢复 `local-ci.sh`、AGENTS、roadmap/docs 和任务索引。
- 不回滚 0080 contract/gate。
