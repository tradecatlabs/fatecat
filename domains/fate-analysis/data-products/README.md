# FateCat 数据产品

`domains/fate-analysis/data-products/` 是 FateCat 命理分析领域的静态数据产品层。

## 分区

| 路径 | 用途 | 是否默认运行依赖 |
| --- | --- | --- |
| `locations/location_catalog.ndjson.gz` | 全球地点、稳定 ID、WGS84 坐标、IANA 时区与别名目录 | 是 |
| `classics/*.txt` | 已整理命理古籍与基础语料 | 可选 |
| `bazi/golden/coverage_matrix_cases.json` | 100+ 匿名八字结构覆盖矩阵，用于锁定四柱、起运、覆盖标签和失败解释 | 测试依赖 |
| `ziwei/golden/cases.json` | 匿名紫微基础盘面样本，用于锁定十二宫、命身宫、四化数量和核心规则 id | 测试依赖 |
| `ziwei/golden/rule_depth_cases.json` | 匿名紫微规则深度样本，用于锁定规则、组合主题和冲突解释 | 测试依赖 |
| `calendar/solar_terms/golden/` | 节气 golden fixture，用于测试成熟历法库输出 | 测试依赖 |

## 供应链门禁

```bash
bash scripts/data-supply-chain-gate.sh \
  --output-json infra/runtime/local-state/exports/supply-chain/data-supply-chain-gate.json
```

核心质量语料门禁：

```bash
bash scripts/core-quality-corpus-gate.sh \
  --output-json infra/runtime/local-state/exports/quality/core-quality-corpus-gate.json
```

该门禁校验八字/紫微匿名 fixture、核心质量语料 manifest、完整报告 diff 策略和北京测试样本隐私边界。

该门禁校验：

- `contracts/fate/data-supply-chain/registry.json` 的资产字段、usageRole、productionEligibility、exportPolicy。
- `locations/` 数据产品、manifest 与 source lock 的内容 hash、来源许可和生产边界。
- `classics/*.txt` 是否全部进入 `source_manifest.tsv` 和 `copyright_review.tsv`，并且 bytes / sha256 与文件一致。
- 节气 raw 来源 manifest 是否具备完整 hash 字段。
- `vendor_sources.json` 中 production dependency 是否满足 SPDX license 与 `productionUseAllowed=true`。

该门禁不提供法律意见，不读取 raw 私有资料，不改变 production provider 算法。

## 原始资料规则

- raw 私有资料只作为本地来源资料和人工复核材料，不进入此 canonical 数据产品目录。
- raw 路径已被 `.gitignore` 和导出脚本排除，避免大文件、版权不明资料或未清洗 OCR 进入发布包。
- 后续要用于生产逻辑时，必须先完成来源复核、结构化抽取、字段契约和回归测试。
- golden fixture 只作为测试门禁，运行期仍调用 `lunar-python`。
