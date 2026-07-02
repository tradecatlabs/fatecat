# Planning Summary
把 release artifact 生成作为 0039 之后的最小可验证切片：先生成本地 SBOM/provenance，再让 live release gate 消费它们；真实远端 attestation 留给后续有 CI/registry 环境时完成。

# Lifecycle Gates
| Phase | Gate | Status |
| --- | --- | --- |
| SPEC | SBOM/provenance 本地 baseline 边界明确 | Done |
| PLAN | 任务树、依赖、验收和反证写入任务包 | Done |
| BUILD | 脚本、gate 接入、测试、文档完成 | Done |
| TEST | JSON、shell、ruff、pytest、release gate smoke | Done |
| REVIEW | 不伪造远端 attestation 或 container digest | Done |
| SHIP | closeout packet 生成 | Done |

禁止跳过任何 gate；本地 artifact 生成不能替代远端 CI attestation、container digest 或 registry signature。

# Simplest Path
使用标准库读取 lockfile 和关键文件 hash，生成 CycloneDX 兼容 SBOM、SLSA/in-toto 风格 provenance 和 manifest；不接外部工具，避免引入供应链复杂度。

# Split Strategy
- `TP-01` 做证据盘点。
- `TP-02` 做生成器和校验器。
- `TP-03` 接入 release gate。
- `TP-04` 做测试与文档。
- `TP-05` 做验证 closeout。

# Execution Waves
| Wave | Nodes | Status |
| --- | --- | --- |
| 1 | TP-01.01 | Done |
| 2 | TP-02.01, TP-02.02 | Done |
| 3 | TP-03.01, TP-03.02 | Done |
| 4 | TP-04.01, TP-04.02 | Done |
| 5 | TP-05.01 | Done |

# Runtime Workflow Contract
- allowed_tools: shell read/verify、apply_patch、pytest、ruff、auto-tasks validation scripts。
- forbidden_actions: push、registry upload、真实生产发布、输出 secret、删除历史任务。
- expected_output_schema: SBOM JSON、provenance JSON、manifest JSON、task closeout packet。
- evidence_required: 命令输出、测试结果、artifact path、manifest hash、文档路径。
- stop_conditions: 本地 artifact 生成失败且无法定位；外部 registry 缺失不是本地 baseline 阻塞。

# Next Executable Leaves
- None. 本地 release artifact baseline 已完成。

# Dependency Graph
```text
TP-01.01
  -> TP-02.01 -> TP-02.02
  -> TP-03.01 -> TP-03.02
  -> TP-04.01 -> TP-04.02
  -> TP-05.01
```

# Rollback Protocol
- 移除 `scripts/release-artifacts.py` / `.sh` 时，必须同步移除 public-release/local-ci 调用、测试、release-gate localVerification 和文档引用。
- 不回滚 0039 live release gate。
