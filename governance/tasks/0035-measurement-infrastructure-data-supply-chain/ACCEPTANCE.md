# Task-Level Acceptance
- `contracts/fate/data-supply-chain/registry.json` 存在并覆盖至少 8 类资产。
- `data-supply-chain-gate` 校验 registry、canonical classics、solar terms source manifest 和 vendor production dependency policy。
- canonical `classics/*.txt` 全部具备 `source_manifest.tsv` 和 `copyright_review.tsv` 覆盖，且 hash/bytes 匹配。
- `review_required` 资产不能被声明为 production allowed。
- quick local-ci 包含 data supply chain gate 和 pytest。
- docs/AGENTS/roadmap 明确本轮不提供法律意见、不生成 SBOM/provenance、不读取 raw 私有资料。

# Validation Plan
| 验证项 | 命令 | 状态 |
| --- | --- | --- |
| data supply chain gate | `bash scripts/data-supply-chain-gate.sh --output-json /tmp/fatecat-data-supply-chain-gate.json` | Passed; assets=8, classics=14, checks=162 |
| focused pytest | `.venv/bin/python -m pytest -q tests/regression/test_data_supply_chain_gate.py` | Passed; 2 passed |
| ruff check | `.venv/bin/python -m ruff check scripts/data-supply-chain-gate.py tests/regression/test_data_supply_chain_gate.py` | Passed |
| ruff format check | `.venv/bin/python -m ruff format --check scripts/data-supply-chain-gate.py tests/regression/test_data_supply_chain_gate.py` | Passed |
| quick local-ci | `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-data-supply-chain` | Passed; 110 passed |

# Review Gate
- 检查 gate 是否只读 metadata/hash，不读取 raw 私有资料。
- 检查 canonical classics coverage 是否覆盖全部 14 个 TXT。
- 检查 registry 是否区分 production_input、evaluation_only、rule_index_seed、reference_only 和 source_archive_only。
- 检查 docs 是否标注 SBOM/provenance 和法律复核仍待后续。

# Runtime Verification Gate
- gate、focused pytest、ruff、format 和 quick local-ci 已通过。
- task validator、tree validator 待执行。
- 外部连通验证待执行：人工法律复核、SBOM/provenance、外部 raw 授权、真实生产发布。

# Ship Readiness
- 当前本地验证、closeout validator 和 closeout packet 已完成；外部法律复核、SBOM/provenance 与真实生产发布仍待后续任务。
- 任务完成后可进入 `0036-measurement-infrastructure-eval-dashboard-nightly` 或先做 export hygiene 扩展。

# Task Package Acceptance
| Package | Acceptance |
| --- | --- |
| TP-02 | registry/schema 和 classics manifest coverage 落地。 |
| TP-03 | gate script、pytest 和 quick local-ci hook 落地。 |
| TP-04 | docs/AGENTS/roadmap 同步，quick CI 通过，closeout packet 生成。 |

# Anti-Goals
- 不引入新外部资料。
- 不做法律意见。
- 不生成 SBOM/provenance。
- 不读取 raw 私有资料。
- 不改 production provider 算法。
