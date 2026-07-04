# Planning Summary

目标终态：生产交付 live evidence 先由外部 operator 执行，再以脱敏 summary JSON 进入仓库；仓库内装配器把 summary 转换为统一 live evidence bundle，0123 live proof gate 负责校验绑定和反伪造，certification 继续保持最终阻断。

# Lifecycle Gates

不得跳过 gate。每个 phase 必须有对应证据后才能进入下一 phase。

| Phase | Gate |
| --- | --- |
| SPEC | MI-100.B.01 scope、supported categories、privacy boundary 明确 |
| PLAN | 不执行真实外部请求，只装配已有 live summaries |
| BUILD | contract、script、wrapper、local-ci wiring、AGENTS、tests 完成 |
| TEST | targeted pytest、ruff check、ruff format、real artifact chain、quick CI |
| REVIEW | no raw URL/secret output、no 100% over-claim、runbook command executable |
| SHIP | commit/push and remote CI observation |

# Simplest Path

复用现有 `live-release-gate.py`、`postgres-public-webhook-live-smoke.py`、`multi-surface-semantic-diff.py` 输出，不新增新的外部请求实现。自研部分只做 adapter/assembler。

# Split Strategy

```text
TP-01 confirm categories and existing summaries
TP-02 implement assembler
TP-03 wire local-ci and docs
TP-04 validate
TP-05 ship
```

# Execution Waves

| Wave | Nodes | Status |
| --- | --- | --- |
| W1 | TP-01, TP-02 | Done |
| W2 | TP-03 | Done |
| W3 | TP-04 | In Progress |
| W4 | TP-05 | Pending |

# Runtime Workflow Contract

1. Operator runs live checks outside the repo with real credentials.
2. Operator stores only redacted summary JSON locally.
3. `production-live-delivery-evidence-bundle.py` consumes the summaries and emits `fatecat.external_validation_live_evidence_bundle`.
4. `external-validation-live-proof-gate.py` validates the bundle against work queue/proof-ref/runbooks/current commit.
5. Certification consumes live proof gate summary and stays blocked until audit review closes.

# Next Executable Leaves

- TP-04: complete validation gates.
- TP-05: commit/push and observe remote CI.

# Dependency Graph

```text
TP-01 -> TP-02 -> TP-03 -> TP-04 -> TP-05
```

# Rollback Protocol

- Revert `production-live-delivery-evidence-bundle.*` files and local-ci wiring.
- Restore Telegram Bot runbook command if needed, though current fix aligns with existing scripts.
- Keep generated runtime artifacts under `/tmp` or ignored runtime paths only.
