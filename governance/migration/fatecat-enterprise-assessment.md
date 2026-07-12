---
id: MIG-FATECAT-ENTERPRISE-ASSESSMENT
type: migration-assessment
status: archived
owner: engineering
created: 2026-06-06
last_reviewed: 2026-07-13
review_cycle: P30D
---

# FateCat 企业级迁移前审计

> 历史快照：本文描述迁移前状态，不能用于判断当前目录、Git 状态或生产能力。

## 目标

把 FateCat 从“根目录 skill 外壳 + `scripts/project/` 真实源码根”迁移为企业级系统仓库。目标状态必须具备 canonical roots、服务契约、catalog、governance、结构门禁、导出门禁和可重复验收。

项目一句话主旨：整理综合全部预测流派，首先完善中国传统主流和有效开源仓库，复用先于自写。

## 审计命令

```bash
git status --short --branch
git rev-list --left-right --count @{u}...HEAD 2>/dev/null || true
git ls-files --others --ignored --exclude-standard
find . -maxdepth 2 -type d | sort
rg -n 'scripts/project|services/|products/|assets/|config/|libs/|middle-platform|internal-platform' README.md AGENTS.md SKILL.md references scripts .github --glob '!scripts/project/assets/vendor/**' --glob '!governance/**'
find scripts/project/modules -maxdepth 2 -type d | sort
```

## Git 状态

- 分支：`main...origin/main`
- ahead/behind：`0 0`
- 当前存在用户未提交业务改动，必须保留，不得回滚。

已分类的用户改动：

```text
scripts/project/assets/data/bazi/golden/rule_depth_cases.json
scripts/project/assets/data/ziwei/golden/rule_depth_cases.json
scripts/project/assets/docs/reference/八字紫微规则深度扩展.md
scripts/project/assets/fate/classics_rule_index.json
scripts/project/assets/fate/rule_depth_registry.json
scripts/project/modules/fate_core/src/fate_core/usecases/calculate_pure_analysis.py
scripts/project/modules/fate_core/src/fate_core/usecases/calculate_ziwei.py
scripts/project/modules/fate_core/src/fate_core/usecases/rule_depth.py
scripts/project/modules/telegram/src/report_generator.py
scripts/project/tests/test_bazi_ziwei_rule_depth.py
```

这些文件属于规则深度与八字紫微增强工作，不在本阶段改写内容；后续物理迁移时只允许移动并保留内容。

## ignored / untracked 分类

`git ls-files --others --ignored --exclude-standard` 显示主要 ignored 文件来自：

- `scripts/project/.venv/`
- `scripts/project/.pytest_cache/`
- `scripts/project/.ruff_cache/`
- `scripts/project/.mypy_cache/`

结论：这些是本地运行态、缓存和虚拟环境，不是迁移真相源，不得进入 Git 或导出包。

## 当前目录事实

迁移前根目录只有 `.github/`、`references/`、`scripts/`；初始化治理包后新增 `governance/`。企业 canonical roots 此前不存在。

当前真实源码与项目资产仍在：

```text
scripts/project/
├── assets/
├── modules/
├── runtime/
├── scripts/
├── tests/
└── pyproject.toml
```

## 服务清单

| 服务 | 当前 source root | 目标 root | 状态 |
| --- | --- | --- | --- |
| fate-core | `scripts/project/modules/fate_core` | `domains/fate-analysis/services/fate-core` | migration-transitional |
| fatecat-delivery | `scripts/project/modules/telegram` | `domains/experience-delivery/services/fatecat-delivery` | migration-transitional |

## active 旧路径引用

`rg` 证明 `scripts/project` 仍被以下 active 面保活：

- 根 `AGENTS.md`、`README.md`、`SKILL.md`
- `references/*`
- `.github/workflows/acceptance.yml`
- 根 `scripts/common.sh`
- 根 `scripts/export-runtime.sh`
- 根 `scripts/check-source-hygiene.sh`
- 根 `scripts/check-export-hygiene.sh`
- 根 `scripts/check-privacy-fixtures.sh`
- 根 `scripts/live-bot-smoke.sh`
- 根 `scripts/clean-runtime.sh`
- `scripts/project/pyproject.toml`
- `scripts/project/modules/telegram/src/_paths.py`
- `scripts/project/modules/fate_core/src/fate_core/support/paths.py`

结论：`scripts/project` 当前是 P0 风险面，不能直接删除；必须先抽象运行根，再逐步迁移并更新门禁。

## CI / 脚本 / 导出影响面

| 入口 | 当前依赖 | 迁移风险 |
| --- | --- | --- |
| `.github/workflows/acceptance.yml` | `scripts/project/pyproject.toml` cache path、`scripts/acceptance.sh` | 移动 pyproject 后 CI cache 与安装路径会失效 |
| `scripts/common.sh` | `project_root="${skill_scripts_dir}/project"` | 所有 preflight/acceptance/export 间接受影响 |
| `scripts/export-runtime.sh` | 多处 `scripts/project/...` exclude 与 runtime skeleton | 导出包卫生和 strict skill 校验会失效 |
| `scripts/check-source-hygiene.sh` | raw/env/output 旧路径模式 | 旧路径迁移后可能漏检 secret/runtime |
| `scripts/check-export-hygiene.sh` | 导出包旧路径模式 | 新路径可能混入 `.env`、cache 或 `.db` |
| `scripts/check-privacy-fixtures.sh` | 多处 allowlist 与 vendor web 旧路径 | 迁移后隐私门禁可能误报或漏报 |
| `scripts/project/modules/telegram/src/_paths.py` | `REPO_ROOT = MODULE_ROOT.parent.parent` | 物理迁移后 assets/runtime/module 路径全部变化 |

## 初始风险等级

- P0：运行根解析、CI cache path、导出卫生、source hygiene、隐私门禁、`_paths.py`。
- P1：服务 source root 物理迁移、pyproject/testpaths、mypy/ruff path。
- P2：文档地图、catalog、baseline ledgers。
- P3：归档命名和非阻断 polish。

## 下一阶段退出条件

- 企业 canonical roots 已存在且有目录边界说明。
- 两个生产候选服务已具备 `README.md`、`AGENTS.md`、`service.yaml`。
- `scripts/project` 兼容盒有 owner、删除条件和风险记录。
- 运行根解析脚本支持目标企业结构。
