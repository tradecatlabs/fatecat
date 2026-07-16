---
id: MIG-FATECAT-DIRECTORY-MAPPING
type: migration-mapping
status: current
owner: engineering
created: 2026-06-06
last_reviewed: 2026-07-16
review_cycle: P30D
---

# FateCat 企业目录映射

## 映射原则

- 目录名可以调整，职责边界不能混。
- 旧路径只允许作为迁移账本、历史证据、负例测试和防回潮规则存在。
- 复用先于自写：成熟开源命理、历法和排盘仓库继续作为供应链资产登记，不在 vendor 内魔改。

## 顶层目标

```text
fatecat/
├── apps/
├── ai/
├── domains/
├── platform/
├── infra/
├── contracts/
├── catalog/
├── governance/
├── shared/
├── tools/
├── docs/
├── scripts/
└── tests/
```

## 旧路径到新路径

## Principle Gate Evidence

- target end state: canonical roots are the only active source, runtime, contract, and data roots.
- real constraints: migration records must preserve old-to-new provenance for audit and rollback.
- inertia constraints: old paths explain history but cannot define current architecture.
- kill list: active fallback roots, source imports from retired trees, and unowned migration leftovers.
- proof point: structure/source/export gates pass with active roots only.
- falsifier: runtime code or catalog points back to `scripts/project/`.
- migration slice: keep historical mapping here while active services consume canonical roots.

| 旧路径 | 目标路径 | 处理方式 | 当前状态 |
| --- | --- | --- | --- |
| `scripts/project/modules/fate_core/` | `domains/fate-analysis/services/fate-core/src/` | 领域服务迁移 | active catalog 已指向 canonical service root；旧路径仅保留历史证据/负例语境 |
| `scripts/project/modules/telegram/` | `domains/experience-delivery/services/fatecat-delivery/src/` | 交付服务迁移 | active catalog 已指向 canonical service root；旧路径仅保留历史证据/负例语境 |
| `scripts/project/assets/fate/` | `contracts/fate/` | capability/profile/evidence/risk 契约迁移 | canonical contract root 已接管；旧路径已退役 |
| `scripts/project/assets/data/` | `domains/fate-analysis/data-products/` 与 `contracts/datasets/` | 静态数据与 golden 数据分层迁移 | 轻量数据产品已迁入；`classics/raw` 与 `calendar/solar_terms/raw` 按治理边界不进入 canonical root |
| `scripts/project/assets/database/` | `infra/databases/` | schema 和 migration 迁移 | 已复制 schema；真实 `.db` 不迁移、不提交 |
| `scripts/project/assets/config/` | `infra/environments/` | env template 与 branding 配置迁移 | 已复制 `.env.example`、`agent.env.example`、`branding.json`；真实 `.env` 禁止提交 |
| `scripts/project/assets/deploy/` | `infra/` 与 `scripts/` | 运行期望状态与可执行入口分流 | canonical infra 与根脚本已接管；旧路径已退役 |
| `scripts/project/assets/docs/` | `docs/` 与 `governance/evidence/` | 人类文档和治理证据分流 | canonical 文档与治理根已接管；旧路径已退役 |
| `scripts/project/assets/tasks/` | `governance/tasks/` | 任务包迁移 | canonical 任务根已接管；旧路径已退役 |
| `scripts/project/assets/vendor/` | `tools/reference-repos/` 或 `platform/supply-chain/vendor-snapshots/` | vendor 快照登记迁移，禁止改源码 | 已复制到 `tools/reference-repos/`；`node_modules` 不进入 canonical vendor |
| `scripts/project/runtime/` | `infra/runtime/local-state/` 或 ignored runtime root | 运行态骨架迁移 | 已建立本地运行态骨架；真实 `bazi.db` 留在旧 runtime/忽略运行态，不迁移 |
| `scripts/project/tests/` | `tests/` 或服务内 tests | 仓库级与服务级测试分流 | 已复制到 `tests/regression/`；service tests 位于 `domains/*/services/*/tests/` |
| `scripts/project/pyproject.toml` | `pyproject.toml` | Python 项目配置提升到企业仓库根 | root `pyproject.toml` 已成为 active Python 工程入口 |
| `scripts/project/README.md` | 根 `README.md` 与 `docs/` | 产品说明迁移 | canonical 文档入口已接管；旧路径已退役 |
| `SKILL.md` | 根 `SKILL.md` | 保留标准 skill 导出入口 | 根入口继续作为公开安装契约，AI 治理资产归 `ai/` |
| `references/` | 根 `references/` | 保留长文档与执行参考入口 | 已纳入企业根 canonical roots |
| `.github/workflows/acceptance.yml` | `.github/workflows/acceptance.yml` | 保留位置并复用根脚本 | 已调用 canonical `scripts/acceptance.sh` |
| `scripts/*.sh` | `scripts/*.sh` | 保留本地可重复执行入口 | 已从企业根解析；不存在 legacy source/runtime fallback |

## 当前 canonical 资产根

| 资产类型 | canonical root | 禁止进入 |
| --- | --- | --- |
| 命理契约 | `contracts/fate/` | 算法代码、运行输出、数据库 |
| 静态数据产品 | `domains/fate-analysis/data-products/` | raw 私有资料、大文件、未复核外部分发包 |
| 配置模板 | `infra/environments/local/` | 真实 `.env`、secret、token |
| 数据库 schema | `infra/databases/` | `*.db`、`*.sqlite`、备份 |
| 本地运行态 | `infra/runtime/local-state/` | 除 `.gitkeep` 外的运行数据 |
| 供应链参考仓 | `tools/reference-repos/` | `node_modules`、未登记 vendor、魔改 vendor 源码 |

## 兼容盒退役状态

| 兼容盒 | owner | 状态 | 保留引用边界 |
| --- | --- | --- | --- |
| `scripts/project/` | engineering | active compatibility box retired | 只允许出现在迁移账本、历史证据、负例测试和防回潮规则；active catalog、service contract、source root、runtime root 不得引用 |

## 禁止项

- 不在根目录创建第二套业务源码并同时保留 active `scripts/project` 多头写入。
- 不让 active code/config 继续优先读取旧路径。
- 不用 ignore/exclude 掩盖旧路径回潮。
- 不把 vendor 缺许可证问题通过复制改名隐藏。
