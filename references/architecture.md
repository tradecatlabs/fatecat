# FateCat Skill 架构说明

## 目标

把 FateCat 从“完整应用仓库”包成“可触发、可治理、可沉淀”的 Agent skill，同时保持现有 CLI / API / Bot 能力不漂移。

## 当前阶段设计

```text
fatecat/
├── SKILL.md                  # 触发入口
├── references/              # 长文档
├── scripts/                 # 包装脚本、生命周期脚手架与导出脚本
│   ├── *.sh                 # 直接调用 FateCat CLI 或治理入口
│   ├── check-export-hygiene.sh # 导出包卫生门禁，拒绝缓存、运行态与 secret
│   └── export-runtime.sh    # 物化独立 single-skill bundle，支持 full / lite 导出
└── scripts/project/         # FateCat 真实源码根，内含项目资产与生命周期治理资产
    └── assets/docs/lifecycle/
        ├── templates/       # 阶段模板
        └── packs/           # 生命周期包默认落点
```

## 双层结构

- 治理层：根级 `SKILL.md`、`references/`、`scripts/` 负责触发入口、阶段约束、文档导航、运维脚本与 bundle 导出。
- 项目层：`scripts/project/` 负责真实业务代码、运行时目录、配置模板、测试、项目元数据与生命周期治理资产。
- 这样拆开以后，Agent 可以在不污染业务源码的前提下记录需求、阶段状态、运维证据和退役材料。

## 依赖边界

- 纯分析核心：`scripts/project/modules/fate_core/`
- 交付层：`scripts/project/modules/telegram/`
- 配置、profile、schema、vendor：`scripts/project/assets/`
- 运行态数据：`scripts/project/runtime/`
- 生命周期模板：`scripts/project/assets/docs/lifecycle/templates/`
- 生命周期包默认落点：`scripts/project/assets/docs/lifecycle/packs/`
- skill 外壳不重写业务逻辑，只包装入口、阶段治理与迁移路径

## 生命周期映射

- 需求：`00-context.md`、`01-requirements.md`
- 原型：`02-prototype.md`
- 迭代：`03-iteration.md`
- 成熟方案重构：`04-mature-refactor.md`
- 生产优化：`05-production-hardening.md`
- 运维加固：`06-operations.md`
- 退役：`07-retirement.md`

## 运维边界

- 当前 skill 提供的是 repo 内可执行的健康检查、启动入口、生命周期状态查看和运维包沉淀。
- 默认执行入口应优先收敛到 `preflight.sh`，而不是让 agent 每次手工拼接检查步骤。
- 进程级自动救活、外部监控告警、容器编排和云资源编排仍属于部署环境层，不在当前仓库直接自动创建。
