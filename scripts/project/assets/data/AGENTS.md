# AGENTS.md - assets/data 目录说明

## 目录用途

`assets/data/` 存放 FateCat 的静态数据与可复核来源资料。这里是算法输入、语料输入和人工校验材料的资产层，不保存运行时数据库、日志、缓存或用户输出。

## 目录结构

```text
data/
├── AGENTS.md
├── README.md
├── china_coordinates.csv
├── calendar/
│   └── solar_terms/
│       ├── README.md
│       ├── source_manifest.tsv
│       └── raw/                 # 本地原始交节时间表，Git 与导出包排除
└── classics/
    ├── *.txt                    # 已整理、可直接纳入代码/检索流程的轻量语料
    ├── README.md
    ├── source_manifest.tsv
    └── raw/                     # 本地原始书籍资料，Git 与导出包排除
```

## 职责边界

- `china_coordinates.csv`：地点解析与经纬度静态数据源。
- `classics/*.txt`：已经整理到轻量文本层的古籍语料，可作为检索、切片与规则提炼输入。
- `classics/raw/`：PDF、原始 TXT、讲义、未清洗 OCR 资料和外部分发包，只做本地私有来源与人工复核，不作为默认运行依赖。
- `calendar/solar_terms/raw/`：交节时间 CSV/XLS/XLSX 原始表格，只做节气算法交叉校验来源，不作为默认运行依赖。
- `source_manifest.tsv`：记录本地 raw 资料的文件名、大小、哈希、体系归属与来源路径，便于审计和后续清洗。

## 开发规则

- 新增原始书籍、表格或外部分发包时，先放入对应 `raw/`，再刷新 `source_manifest.tsv`。
- 不得把 `raw/` 下大文件纳入 Git 或 skill 导出包。
- 只有完成版权/来源复核、编码清洗、去重、结构化切片和测试后，才能把资料晋升为 `classics/*.txt` 或算法数据。
- 业务代码不得直接依赖 `raw/` 路径；运行期只能依赖已整理的轻量数据或显式配置的数据源。
