# 命理典籍与语料资产

本目录存放 FateCat 的命理典籍、基础知识语料与本地原始资料。

## 分层

| 层级 | 路径 | 说明 |
| --- | --- | --- |
| 整理语料 | `*.txt` | 已进入仓库的轻量文本，可用于检索、切片、规则提炼与人工复核 |
| 原始资料 | `raw/` | 本地 PDF、原始 TXT、讲义、OCR 材料和外部分发包，不进入 Git 与导出包 |
| 内部派生数据集 | `infra/runtime/local-state/exports/datasets/classics-clean-v1/` | 从 canonical TXT 确定性生成的文档、段落、切片、重复标记和质量报告；不进入 Git |
| 清单 | `source_manifest.tsv` | raw 资料索引，记录体系、文件名、大小、哈希与来源路径 |
| 版权分级 | `copyright_review.tsv` | 外部分发包、典籍、案例、知识图谱和脚本的可用性分级 |

## 使用边界

- 当前代码不得直接依赖 `raw/`。
- 新功能需要引用典籍时，应先从 raw 中提炼成小型结构化资料或测试 fixture。
- 外部分发包只能作为来源归档和方法论参考；其中 PDF、电子书、知识图谱和案例资料需完成版权、隐私与来源复核后，才能晋升为可发布资产。
- 任何现代讲义、笔记、PDF 在确认授权前只作为本地研究材料，不随 skill 发布。
- `copyright_review.tsv` 中 `review_required` / `blocked` 的资产不得被运行时代码直接读取。

## 清洗与验证

```bash
.venv/bin/python scripts/classics-dataset-clean.py
.venv/bin/python scripts/classics-dataset-clean.py --validate-only
.venv/bin/python -m pytest -q tests/regression/test_classics_dataset_clean.py
bash scripts/data-supply-chain-gate.sh
```

清洗采用严格 UTF-8、Unicode NFC、允许的不可见字符清理、行内空白规范化和最多 1200 字符的可追溯切片。重复段落、重复切片和跨书重叠只写入 `duplicates.ndjson`，不自动删除或合并；原文、评注、命例和短干支行全部保留。派生数据继承 `review_required`，并固定 `distributionAllowed=false`、`productionUseAllowed=false`、`trainingUseAllowed=false`。
