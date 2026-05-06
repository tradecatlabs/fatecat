# FateCat Skill 单仓布局与导出计划

## 当前布局

- 根目录直接作为 skill 根
- `SKILL.md`、`references/`、`scripts/` 位于根目录
- FateCat 项目整体收口到 `scripts/project/`
- 生命周期治理资产收口到 `scripts/project/assets/docs/lifecycle/`
- 包装脚本只依赖 `scripts/project/` 这一处源码真相源

## 导出 bundle

- 通过 `export-runtime.sh` 复制运行所需骨架到导出目录
- 导出目标结构保持当前单-skill 布局
- 默认支持两种模式：
  - `full`：保留 lifecycle packs
  - `lite`：排除 lifecycle packs，只保留模板与运行所需骨架
- 若导出产物还要跑 strict skill 校验，导出目录 basename 必须保持为 `fatecat`
- 排除 `.git/`、`.venv/`、`node_modules/`、缓存、字节码、真实 `.db` / `.sqlite`、真实 `.env`
- 生命周期模板与治理资产默认随 bundle 一起导出

## 后续优化

- 视情况增加校验脚本，确保导出后命令仍可用
- 视情况增加更细粒度的导出清单，例如只导出某个指定 lifecycle pack

## 导出边界

必须带走：

- `README.md`
- `AGENTS.md`
- `SKILL.md`
- `references/`
- `scripts/`
- `scripts/project/`

必须排除：

- `.git/`
- `.history/`
- `.venv/`
- `node_modules/`
- `.pytest_cache/`
- `.ruff_cache/`
- `.mypy_cache/`
- `__pycache__/`
- `*.pyc`
- `*.pyo`
- `scripts/project/assets/config/.env`
- `*.db`
- `*.sqlite`
- `*.sqlite3`
- `scripts/project/assets/docs/lifecycle/packs/` 在 `lite` 模式下也必须排除

## 风险

- 包体积仍然很大，因为 `scripts/project/assets/vendor/` 是运行时依赖的一部分
- 若把大量生命周期历史包沉淀在 `scripts/project/assets/docs/lifecycle/packs/`，`full` bundle 体积会继续增长
- 若未来路径发现逻辑变化，包装脚本与导出脚本需要一起更新
