# AGENTS.md - domains/fate-analysis/data-products

## 目录用途

`domains/fate-analysis/data-products/` 存放 FateCat 命理分析领域的静态数据与可复核来源资料。这里是算法输入、语料输入和人工校验材料的数据产品层，不保存运行时数据库、日志、缓存或用户输出。

## 目录结构

```text
domains/fate-analysis/data-products/
├── AGENTS.md
├── README.md
├── locations/
│   ├── location_catalog.ndjson.gz # 全球地点、WGS84 坐标与 IANA 时区 canonical 数据
│   ├── manifest.json              # 输出统计、内容 hash、许可和精度边界
│   └── sources.lock.json          # 上游 URL、版本、hash 与许可锁
├── bazi/
│   └── golden/                  # 综合八字陈述服务、历法边界、mismatch report 与覆盖矩阵轻量 golden fixture
├── ziwei/
│   └── golden/                  # 紫微斗数基础盘面与规则深度轻量 golden fixture
├── calendar/
│   └── solar_terms/
│       ├── README.md
│       ├── golden/              # 可提交的轻量节气 golden fixture
│       └── source_manifest.tsv
└── classics/
    ├── *.txt                    # 已整理、可直接纳入代码/检索流程的轻量语料
    ├── README.md
    ├── curation_policy.json     # source-hash 绑定的正文选择、文本角色、完整性和复核策略
    ├── copyright_review.tsv
    └── source_manifest.tsv
```

## 职责边界

- `locations/`：生产地点目录数据产品；稳定 ID、WGS84 坐标、IANA 时区、别名和精度标记必须由同一生成流程产出。
- `bazi/golden/statement_cases.json`：综合八字陈述服务命例回归 fixture，只锁定结构化盘面、边界、格局、调候、强弱、干支关系和起运字段。
- `bazi/golden/calendar_boundary_cases.json`：历法边界回归 fixture，只锁定真太阳时、早晚子时、时区转换、经纬度偏移、节气边界和起运锚点。
- `bazi/golden/calendar_oracle_mismatch_report.json`：历法 provider/oracle 差异报告，只覆盖 `runtime_full` 边界样本，未解释差异不得标绿。
- `bazi/golden/coverage_matrix_cases.json`：100+ 匿名结构覆盖矩阵，只锁定历法四柱、起运、覆盖标签和失败解释，不替代专业命例库。
- `ziwei/golden/cases.json`：紫微基础盘面匿名 fixture，只锁定十二宫、命身宫、四化数量、覆盖标签和规则 id，不替代真实紫微命例库。
- `ziwei/golden/rule_depth_cases.json`：紫微规则深度匿名 fixture，只锁定规则应用、冲突裁决、组合主题和核心盘面字段。
- `classics/*.txt`：已经整理到轻量文本层的古籍语料，可作为检索、切片与规则提炼输入。
- `classics/copyright_review.tsv`：标记典籍、外部分发包、案例和知识图谱的版权/隐私/发布可用性。
- `classics/curation_policy.json`：绑定 canonical source hash，显式登记正文选择、文献家族、文本角色、完整性问题和人工复核项；不得把候选书目包装成已核实事实。
- `scripts/classics-dataset-clean.py`：从 `classics/*.txt` 确定性生成 ignored `classics-clean-v3` 内部派生数据集；按 source-hash policy 分离目录、重建语义段落并在章节内切片，不改变 canonical 原文或版权状态。
- `calendar/solar_terms/golden/`：从 raw 表提炼的轻量回归 fixture，用于锁定节气、月令、立春年界与起运边界。
- `source_manifest.tsv`：记录来源文件名、大小、哈希、体系归属与来源路径，便于审计和后续清洗。
- `contracts/fate/data-supply-chain/registry.json`：跨数据产品、vendor 和 benchmark 的供应链注册表；`scripts/data-supply-chain-gate.sh` 会校验 canonical TXT 是否同时具备 source manifest、copyright review 和 hash。

## 开发规则

- 新增原始书籍、表格或外部分发包时，先放入私有 raw 暂存区，再刷新 `source_manifest.tsv`，不得直接进入此目录。
- 不得把 raw 私有资料、大文件或未复核外部分发包纳入 Git 或 skill 导出包。
- 只有完成版权/来源复核、编码清洗、去重、结构化切片和测试后，才能把资料晋升为 `classics/*.txt` 或算法数据。
- `copyright_review.tsv` 标记为 `blocked` 或 `review_required` 的资产不得被运行时代码直接依赖。
- 业务代码不得直接依赖 `raw/` 路径；运行期只能依赖已整理的轻量数据或显式配置的数据源。
- golden fixture 只允许测试读取，不能替换生产期 `lunar-python` 历法计算。
- 八字/紫微核心质量语料统一登记在 `contracts/fate/evaluations/core-quality-corpus.json`，并由 `bash scripts/core-quality-corpus-gate.sh` 校验。
- 新增、删除或重命名 `classics/*.txt` 时，必须同步 `source_manifest.tsv`、`copyright_review.tsv` 并运行 `bash scripts/data-supply-chain-gate.sh`。
- 生成内部检索/规则提炼语料时，必须使用 `scripts/classics-dataset-clean.py`；派生结果只能留在 `infra/runtime/local-state/exports/`，不得直接提交或发布。
- 任何正文排除都必须进入 `curation_policy.json` 并留下 line/hash/rule/reason 血缘；禁止在清洗器中新增通用广告关键词、模糊模型或静默删除逻辑。
- 刷新 `locations/` 前必须先更新并核对 `sources.lock.json` 的版本、下载 hash 和许可；禁止把上游临时下载文件或运行时 SQLite 索引提交入库。
