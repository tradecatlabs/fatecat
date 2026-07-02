# Planning Summary
本轮把散落的数据来源、典籍版权状态、vendor 资格和 benchmark 边界收束成一个机器可读供应链 baseline。正确终态是 SBOM/provenance、license inventory、导出包 manifest、人工版权复核和生产发布 provenance 全部接入。本轮只做本地可验证切片：registry/schema/gate/test/local-ci/docs。

# Lifecycle Gates
不得跳过 gate；每个 gate 必须有证据或保留为 Pending。

| Gate | Status | Evidence |
| --- | --- | --- |
| SPEC | Done | README/CONTEXT 已定义 scope、anti-goals 和隐私边界。 |
| PLAN | Done | 本文件拆出 contract、gate、tests、docs、closeout。 |
| BUILD | Done | registry/schema/gate/test/local-ci hook 已落地。 |
| TEST | Done | gate、focused pytest、ruff、format 和 quick CI 已通过。 |
| REVIEW | Done | closeout validator 已通过；diff check 和 tree validator 作为最终仓库校验执行。 |
| SHIP | Done | closeout packet 已生成。 |

# Simplest Path
- 不新增数据库或服务 API；供应链先以 contract registry + local gate 存在。
- 不复制外部资料；registry 只引用现有 manifest 和 tracked paths。
- 不把 `classics/*.txt` 直接生产化；只做 rule index seed 并保持 review_required。

# Split Strategy
- TP-01：确认当前数据供应链事实。
- TP-02：新增 registry/schema 并补齐 manifest coverage。
- TP-03：新增 gate、pytest、quick CI hook。
- TP-04：同步文档、运行验证、生成 closeout。

# Execution Waves
| Wave | Leaves | Status |
| --- | --- | --- |
| Wave 1 | TP-01.01 | Done |
| Wave 2 | TP-02.01, TP-02.02 | Done |
| Wave 3 | TP-03.01, TP-03.02 | Done |
| Wave 4 | TP-04.01 | Done |
| Wave 5 | TP-04.02, TP-04.03 | Done |

# Runtime Workflow Contract
- Input: `contracts/fate/data-supply-chain/registry.json`、schema、classics source/copyright TSV、solar terms source TSV、vendor_sources。
- Gate: required path exists, sha256 matches, enum/policy valid, canonical classics coverage complete, vendor production dependency license policy valid。
- Output: machine-readable JSON summary under `infra/runtime/local-state/exports/supply-chain/data-supply-chain-gate.json` by default。
- Privacy: no raw private files, no user input, no token, no secret, no DSN。
- Failure: any missing path, hash mismatch, missing copyright/source row or policy violation returns non-zero。

# Next Executable Leaves
- 无；任务完成。

# Dependency Graph
```text
TP-01.01 -> TP-02.01 -> TP-02.02 -> TP-03.01 -> TP-03.02 -> TP-04.01 -> TP-04.02 -> TP-04.03
```

# Rollback Protocol
- 移除 `contracts/fate/data-supply-chain/`。
- 移除 `scripts/data-supply-chain-gate.*` 和 `tests/regression/test_data_supply_chain_gate.py`。
- 从 `scripts/local-ci.sh` 移除 data supply chain gate step 和 focused test。
- 恢复 data-products/source/copyright manifest 与文档口径。
- 不回滚 0009-0034 已完成测算基础设施切片。
