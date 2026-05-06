# AGENTS.md - FateCat Skill Repo

## 目录用途

当前根目录就是单 skill 仓库根：对外暴露标准 skill 入口，对内托管生命周期治理层与 FateCat 项目源码。

## 目录结构

```text
fatecat/
├── AGENTS.md
├── README.md
├── REVIEW.md
├── SKILL.md
├── .github/
│   ├── AGENTS.md
│   └── workflows/
│       └── acceptance.yml
├── assets/
│   ├── AGENTS.md
│   └── lifecycle/
│       ├── AGENTS.md
│       ├── README.md
│       ├── packs/
│       └── templates/
├── references/
│   ├── commands.md
│   ├── execution-playbook.md
│   └── troubleshooting.md
├── scripts/
│   ├── acceptance.sh
│   ├── check-export-hygiene.sh
│   ├── clean-runtime.sh
│   ├── delivery-smoke.sh
│   ├── export-runtime.sh
│   ├── live-bot-smoke.sh
│   ├── production-readiness.sh
│   ├── preflight.sh
│   └── vendor-health.sh
└── project/
    ├── AGENTS.md
    ├── pyproject.toml
    ├── assets/
    ├── modules/
    ├── runtime/
    ├── scripts/
    └── tests/
```

## 职责边界

- `SKILL.md`：标准 skill 入口说明。
- `REVIEW.md`：当前仓库审计结果与 release gate 结论；只记录证据、风险与交接，不承载业务源码。
- `.github/`：GitHub Actions 远端验收配置；只调用仓库脚本，不保存业务代码或 secret。
- `assets/`：生命周期模板、治理资产与可沉淀的 agent 运维材料。
- `references/`：长文档、阶段门禁、输入输出契约、迁移与排障材料；其中 `execution-playbook.md` 是统一执行顺序真相源。
- `scripts/`：skill 包装脚本、生命周期脚手架与导出脚本；其中 `preflight.sh` 是默认预检入口，`acceptance.sh` 是发布门禁入口，`delivery-smoke.sh` 负责可回收启动验证，`check-export-hygiene.sh` 负责导出包卫生门禁，`vendor-health.sh` 负责 vendor 快照健康检查，`live-bot-smoke.sh` 负责真实 Telegram token 验收，`production-readiness.sh` 负责生产配置与 live 验收总门禁。
- `project/`：FateCat 项目的真实源码根、运行时骨架与项目文档真相源。

## 依赖方向

- `README.md -> SKILL.md + assets/* + references/*`
- `.github/workflows/* -> scripts/acceptance.sh`
- `assets/* -> scripts/* + references/*`
- `scripts/* -> project/*`
- `SKILL.md -> scripts/preflight.sh + scripts/delivery-smoke.sh + references/execution-playbook.md`
- 禁止在根目录重新散落与 `project/` 平行的第二套业务源码目录
