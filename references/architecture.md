# FateCat 企业架构说明

## 目标

以企业级系统仓库承载 FateCat 的领域源码、运行资产、契约、治理、测试和导出入口，同时保持 CLI / API / Bot / Web / pure-analysis 能力可重复验证。

项目主旨：FateCat 是面向 Agent 与应用开发者的测算基础设施，提供统一的能力协议、可复现计算核心、证据化解释层和多端交付接口。八字、紫微、黄历、梅花等体系都是独立 capability provider；复用成熟开源和稳定平台能力先于自写。

## 当前结构

```text
fatecat/
├── apps/
├── ai/
├── domains/
│   ├── fate-analysis/services/fate-core/
│   └── experience-delivery/services/fatecat-delivery/
├── platform/
├── infra/
├── contracts/
├── catalog/
├── governance/
├── shared/
├── tools/
├── docs/
├── scripts/
├── tests/
├── SKILL.md
└── references/
```

## 分层结构

- 企业根：`apps`、`ai`、`domains`、`platform`、`infra`、`contracts`、`catalog`、`governance`、`shared`、`tools`、`docs`、`tests` 是架构真相源。
- 服务源码：`domains/fate-analysis/services/fate-core/src/` 与 `domains/experience-delivery/services/fatecat-delivery/src/` 承载生产候选源码。
- 执行层：根 `scripts/` 负责本地可重复验证、导出、卫生门禁、delivery smoke 和 production readiness。
- Agent 入口：`SKILL.md` 继续作为当前 skill 触发入口，后续可迁入 `ai/skills/fatecat/` 并由导出脚本物化根 skill 包。
- 历史证据：旧组织映射和任务包保存在 `governance/migration/` 与 `governance/tasks/project-history/`，不参与运行时解析。

## 依赖边界

- 纯分析核心目标：`domains/fate-analysis/services/fate-core/`
- 交付层目标：`domains/experience-delivery/services/fatecat-delivery/`
- capability、profile、evidence、risk policy 目标：`contracts/fate/`
- 配置、数据库、容器、运行准入目标：`infra/`
- vendor 快照目标：`tools/reference-repos/` 或 `platform/supply-chain/`
- 任务、ADR、risk、baseline evidence 目标：`governance/`
- 退役路径不得作为 fallback；旧路径只允许出现在迁移账本、历史证据、负例测试和防回潮规则中。

## 生命周期映射

- 需求：`00-context.md`、`01-requirements.md`
- 原型：`02-prototype.md`
- 迭代：`03-iteration.md`
- 成熟方案重构：`04-mature-refactor.md`
- 生产优化：`05-production-hardening.md`
- 运维加固：`06-operations.md`
- 退役：`07-retirement.md`

## 运维边界

- 当前根脚本提供的是 repo 内可执行的健康检查、启动入口、结构门禁、卫生门禁、导出和运维包沉淀。
- 默认执行入口应优先收敛到 `preflight.sh`，而不是让 agent 每次手工拼接检查步骤。
- 进程级自动救活、外部监控告警、容器编排和云资源编排仍属于部署环境层，不在当前仓库直接自动创建。

## 当前迁移证据

- `governance/migration/fatecat-enterprise-assessment.md`
- `governance/migration/fatecat-enterprise-directory-mapping.md`
- `governance/evidence/baseline/baseline-migration-work-order.md`
- `governance/evidence/baseline/baseline-gate-execution-report.md`
