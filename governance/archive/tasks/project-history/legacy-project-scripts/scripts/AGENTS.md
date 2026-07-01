---
id: ARCHIVE-ARCHIVE-TASKS-PROJECT-HISTORY-LEGACY-PROJECT-SCRIPTS-SCRIPTS-AGENTS
type: archive
status: archived
owner: engineering
created: 2026-06-17
last_reviewed: 2026-06-17
review_cycle: P365D
---
# AGENTS.md - project scripts

## 目录用途

`scripts/project/scripts/` 放置 FateCat 项目内部维护脚本；这些脚本服务于数据生成、构建、测试、部署和外部评测资产验证，不作为用户报告逻辑入口。

## 目录结构

```text
scripts/
├── AGENTS.md
├── README.md
├── build_solar_terms_golden.py
├── run-mingli-bench.sh
├── test_all.sh
└── ...
```

## 职责边界

- `build_solar_terms_golden.py`：从本地交节 raw 表生成节气 golden fixture。
- `run-mingli-bench.sh`：离线读取 MingLi-Bench 资产，输出统计、prompt JSONL 与 predictions 评分；默认不调用外部模型 API。
- `test_all.sh` / `build_all.sh`：项目历史批处理入口。

## 依赖方向

- 允许读取 `assets/` 下已登记的 raw、golden、vendor 和文档资产。
- 禁止在默认脚本中调用真实外部模型、Bot、生产 API 或写入未声明的运行态目录。
- 新增脚本必须能非交互执行，并在 README 或相关文档中说明是否会联网、写文件或依赖密钥。
