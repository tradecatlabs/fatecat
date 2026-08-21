# AGENTS.md - FateCat Enterprise Repo

## 目录用途

当前根目录是 FateCat 企业级系统仓库真相源：结构采用 `apps`、`ai`、`domains`、`platform`、`infra`、`contracts`、`catalog`、`governance`、`shared`、`tools`、`docs`、`scripts`、`tests` canonical roots；运行、测试、导出和治理入口全部从企业根解析。

项目主旨：FateCat 是面向 Agent 与应用开发者的测算基础设施，提供统一的能力协议、可复现计算核心、证据化解释层和多端交付接口。八字、紫微、黄历、梅花等体系都是独立 capability provider；复用成熟开源和稳定平台能力先于自写。

## 目录结构

```text
fatecat/
├── AGENTS.md
├── compose.yaml
├── DEBUG.md
├── llms.txt
├── README.md
├── REVIEW.md
├── SKILL.md
├── apps/
├── ai/
├── domains/
│   ├── fate-analysis/
│   │   └── services/fate-core/
│   │       ├── src/
│   │       └── tests/
│   └── experience-delivery/
│       └── services/fatecat-delivery/
│           ├── src/
│           ├── scripts/
│           └── tests/
├── platform/
├── infra/
│   └── docker/
│       ├── Dockerfile.delivery
│       └── entrypoint.delivery.sh
├── contracts/
├── catalog/
├── governance/
├── shared/
├── tools/
├── docs/
│   └── deployment/
│       └── huggingface-space.md
├── tests/
├── .github/
│   ├── AGENTS.md
│   └── workflows/
│       ├── acceptance.yml
│       ├── container.yml
│       ├── hf-space-deploy.yml
│       └── quick.yml
├── references/
│   ├── commands.md
│   ├── execution-playbook.md
│   └── troubleshooting.md
└── scripts/
│   ├── acceptance.sh
│   ├── check-structure.sh
│   ├── container-build.sh
│   ├── container-release.sh
│   ├── container-smoke.sh
│   ├── check-export-hygiene.sh
│   ├── check-source-hygiene.sh
│   ├── clean-runtime.sh
│   ├── delivery-smoke.sh
│   ├── export-runtime.sh
│   ├── live-bot-smoke.sh
│   ├── production-readiness.sh
│   ├── preflight.sh
│   └── vendor-health.sh
```

## 职责边界

- `SKILL.md`：标准 skill 入口说明。
- `compose.yaml`：本地和单机容器编排入口，只编排 delivery 容器与运行态 volume。
- `DEBUG.md`：当前调试证据、根因和回归验证记录；只承载已复现问题的诊断闭环。
- `llms.txt`：公开站点根级 AI/Agent 发现文档；集中说明 Web/API 输入、端点、证据、存储和风险边界，避免把机器契约全部堆在 Web 顶部表格。
- `REVIEW.md`：当前仓库审计结果与 release gate 结论；只记录证据、风险与交接，不承载业务源码。
- `apps/`：用户体验入口和渠道壳层。
- `ai/`：Agent、skill、Prompt、评估和 AI 监管相关入口。
- `domains/`：领域服务根；当前承载 `fate-core` 与 `fatecat-delivery` 两个生产候选服务源码、契约和测试入口。
- `platform/`：Golden Path、CI/CD、供应链和开发者平台能力。
- `infra/`：环境、容器、数据库、运行准入、安全和观测期望状态。
- `contracts/`：API、数据集、capability、profile、evidence 和策略契约。
- `catalog/`：组件发现、owner、生命周期和依赖关系。
- `governance/`：标准、流程、ADR、风险、门禁、baseline evidence、任务和迁移账本。
- `shared/`：真实复用后的薄共享库，不作为 common 垃圾桶。
- `tools/`：迁移工具、参考仓和供应链快照。
- `docs/`：人类文档入口，不替代机器契约和治理证据；`docs/deployment/` 说明用户和维护者的云端部署路径。
- `tests/`：仓库级结构、契约、导出和跨服务测试入口。
- `.github/`：GitHub Actions 远端验收配置；只调用仓库脚本，不保存业务代码或 secret。
- `references/`：长文档、阶段门禁、输入输出契约、迁移与排障材料；其中 `execution-playbook.md` 是统一执行顺序真相源。
- `scripts/`：本地可重复执行入口；其中 `preflight.sh` 是默认预检入口，`acceptance.sh` 是发布门禁入口，`check-structure.sh` 是企业结构门禁，`container-*.sh` 是容器构建、烟雾和发布入口。

## Web HTML 设计硬规则

- `GET /web` 和同类工程报表页必须遵守 `/home/lenovo/.codex/Design.md` 的零美化语义界面规范。
- FateCat `/web` 只采用 `governance/decisions/adr/ADR-0001-native-workbench-compatibility-profile.md` 的语义兼容性 profile，不直接采用静态产品的绝对定位工作台；不得以工作台名义加入 CSS、class、视觉组件或删除现有 API/报告协议。
- 禁止加入 CSS、`style`、视觉 class、颜色、圆角、卡片、响应式布局、装饰性容器或前端视觉效果；当前不存在授权例外。
- 页面结构只允许服务信息结构和操作结构：原生表单、真实链接、`dl` 元信息、`pre/code` 原始数据、`details/summary` 非核心长内容。
- 修改 `domains/experience-delivery/services/fatecat-delivery/src/web_ui.py` 前必须读取 `governance/standards/零美化语义界面标准.md`、`GATE-0001` 和对应 module context。
- 验证必须覆盖 `tests/regression/test_web_html.py::assert_zero_beauty_semantic_html`，默认跑 `bash scripts/local-ci.sh --profile quick`。

## 依赖方向

- `apps/ai -> domains + contracts`
- `domains/experience-delivery -> domains/fate-analysis + contracts + infra`
- `domains/fate-analysis -> contracts + tools/reference-repos`
- `catalog -> domains + contracts + governance`
- `.github/workflows/acceptance.yml -> scripts/acceptance.sh`
- `.github/workflows/container.yml -> scripts/container-build.sh + scripts/container-smoke.sh`
- `.github/workflows/hf-space-deploy.yml -> scripts/hf-space-deploy.sh + infra/huggingface-space`
- `.github/workflows/quick.yml -> scripts/local-ci.sh --profile quick`
- `scripts/* -> domains + contracts + infra + governance`
- 禁止新增旧路径 fallback；退役路径只允许出现在迁移账本、历史证据、负例测试和防回潮规则中。
