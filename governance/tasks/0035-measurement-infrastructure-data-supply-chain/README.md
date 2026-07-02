# Task Overview
- Task ID: `0035`
- Slug: `measurement-infrastructure-data-supply-chain`
- Objective: `把数据、典籍、vendor、benchmark 供应链从散落 source_manifest/copyright_review/vendor_sources/evaluation registry 推进为本地可验证 DataSupplyChain baseline：新增统一 data supply chain manifest 和 schema，登记 raw/canonical/derived/export/runtime 分层、来源 hash、许可/版权状态、usageRole、productionEligibility、exportPolicy 与 verification commands；新增 data-supply-chain-gate 脚本和回归测试，接入 quick CI、API 文档、roadmap、data-products AGENTS 和任务 closeout；不引入新外部资料、不做法律意见、不生成 SBOM/provenance、不改变 production provider 算法。`
- Status: `Done`

## In Scope
- 新增 `contracts/fate/data-supply-chain/registry.json` 与 schema。
- 补齐 canonical `classics/*.txt` 的 `source_manifest.tsv` 与 `copyright_review.tsv` 覆盖。
- 新增 `scripts/data-supply-chain-gate.py/.sh`，校验 registry、classics manifest、solar terms source manifest 和 vendor production dependency policy。
- 新增回归测试并接入 `scripts/local-ci.sh --profile quick`。
- 同步 contracts/data-products/scripts 文档、API 接入文档、100% roadmap 和任务 closeout。

## Out of Scope
- 不引入新外部资料。
- 不做法律意见或版权最终判定。
- 不生成 SBOM/provenance artifact。
- 不改变 production provider 算法、运行时依赖或报告输出。
- 不读取 raw 私有资料、不访问外部网络、不验证真实生产账号。

## Task Package Tree
```text
TP-01 现状审计与范围确认
  TP-01.01 盘点 source_manifest、copyright_review、vendor_sources、evaluation registry 和 data-products 目录
TP-02 data supply chain contract
  TP-02.01 新增 data-supply-chain registry/schema/AGENTS
  TP-02.02 补齐 canonical classics source/copyright manifest 覆盖
TP-03 gate runtime
  TP-03.01 新增 data-supply-chain-gate 脚本和 shell wrapper
  TP-03.02 新增 gate pytest 并接入 quick local-ci
TP-04 文档与验证
  TP-04.01 同步 API 文档、roadmap、contracts/data-products/scripts AGENTS
  TP-04.02 运行 gate、pytest、ruff、format、quick CI
  TP-04.03 生成任务 closeout packet
```

## Requirement Alignment
- 对齐 `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` 的 `MI-06 数据与供应链`。
- 对齐胶水原则：复用已有 `source_manifest.tsv`、`copyright_review.tsv`、`vendor_sources.json` 和 evaluation registry，不另造大文件仓。
- 对齐供应链边界：review_required、source_archive_only、evaluation_only、reference_only 不得被宣称为生产输入。
- 对齐隐私治理：gate 只读 tracked metadata/hash，不读取 raw 私有资料、真实用户、token、secret、DSN 或生产账号。

## Task Package Overview
| Package | Status | Evidence |
| --- | --- | --- |
| TP-01 | Done | 已盘点 data-products、classics manifest、solar terms manifest、vendor_sources 和 evaluations registry。 |
| TP-02 | Done | data-supply-chain registry/schema/AGENTS 已新增，canonical classics manifest coverage 已补齐。 |
| TP-03 | Done | data supply chain gate、pytest 和 local-ci hook 已落地；focused gate/test 已通过。 |
| TP-04 | Done | 文档已同步；quick CI 已通过；closeout packet 待生成。 |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
