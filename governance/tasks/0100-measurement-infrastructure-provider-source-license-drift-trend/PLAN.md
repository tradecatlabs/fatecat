# Planning Summary
0084 已有单次 provider drift scanner，但缺少“时间维度”的 tracked baseline。0100 的最小正确切片是新增 baseline + trend gate：当前 scanner 结果必须和 baseline 指纹一致；有意变化必须显式更新 baseline。

# Lifecycle Gates
不得跳过 gate；每个阶段必须以文件证据、命令输出或明确外部 pending 结论收口后，才能进入下一阶段。

| Phase | Gate | Status |
| --- | --- | --- |
| SPEC | Existing scanner and Wave A A1 inspected | Done |
| PLAN | Baseline/trend gate design documented and scoped | Done |
| BUILD | Baseline, contract, script and CI wiring created | Done |
| TEST | Focused tests, ruff, format and task docs validator | Done |
| REVIEW | Diff boundary and privacy/overclaim self-check | Done |
| SHIP | Commit and push current slice | Pending |

# Simplest Path
1. Reuse `provider-drift-scanner.py` output.
2. Normalize provider/source/license/vendor metadata.
3. Compute stable SHA-256 fingerprints.
4. Compare with tracked baseline.
5. Fail on missing/extra provider, identity drift, source/license/vendor fingerprint drift, license/vendor production regressions or scanner findings.

# Split Strategy
- Keep trend gate independent from provider runtime.
- Keep baseline in contracts so changes are reviewable.
- Keep tests focused on contract behavior and negative cases.

# Execution Waves
| Wave | Nodes | Parallelizable |
| --- | --- | --- |
| W1 | TP-01 | Yes |
| W2 | TP-02.01, TP-02.02 | Partly |
| W3 | TP-02.03, TP-03.01 | Partly |
| W4 | TP-03.02, TP-04 | No |

# Runtime Workflow Contract
- Command: `bash scripts/provider-drift-trend-gate.sh --output-json <path>`
- Optional reuse: `--scanner-report-json <provider-drift-scanner-output>`
- Output kind: `fatecat.provider_drift_trend_report`
- Pass criteria: `status=passed` and `findingCount=0`
- External boundary: always `外部连通验证待执行` unless a future external live task provides separate evidence.

# Next Executable Leaves
| Node ID | Action |
| --- | --- |
| TP-04.02 | Commit and push current slice |

# Dependency Graph
```text
TP-01 -> TP-02 -> TP-03 -> TP-04
```

# Rollback Protocol
- Remove `provider-drift-baseline.json` and `provider-drift-trend-contract.json`.
- Remove `provider-drift-trend-gate.py/.sh`.
- Remove `test_provider_drift_trend_gate.py`.
- Revert local-ci, AGENTS, provider schema and docs wiring.
- Do not revert existing provider lifecycle/dependency/drift scanner baseline.
